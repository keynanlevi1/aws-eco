import json, sys, os
import subprocess
import threading
import boto3
from datetime import datetime, date
from dateutil.relativedelta import *
from decimal import Decimal
from account import Account
import traceback 


subprocess.call('pip3 install pandas -t /tmp/ --no-cache-dir'.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.call('pip3 install elasticsearch -t /tmp/ --no-cache-dir'.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.call('pip3 install python-dotenv -t /tmp/ --no-cache-dir'.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


sys.path.insert(1, '/tmp/')

from ec2 import EC2
from aws_service import AwsService
from db_service import DbService
from performance_counters import PerformanceCounters
from dotenv import load_dotenv
import pandas
from functools import reduce

def merge_ec2_metrics_on_start_time (frames):

        df_merged = reduce(lambda  left,right: pandas.merge(left,right,on=['start_time'], how='outer').fillna(0), frames)  
        return df_merged  


def collect_ec2_utilization(ec2, metric_list, account_number, start_date, end_date):

    aws_service = AwsService()    
    db_service = DbService()

    specific_instance_metric_list = aws_service.get_supported_metrics(ec2)
    #remove metrics that are not supported in this instance
    for metric_name in metric_list:
        if not metric_name in specific_instance_metric_list:
            metric_list.remove(metric_name)

    frames = []
                
    for metric_name in metric_list:        
        statistics = 'Average'
        namespace = 'AWS/EC2'
        instance_id = ec2.instance_id
        period = 3600
        start_time = start_date
        end_time = end_date
                                            
        df = aws_service.get_aws_metric_statistics(ec2, metric_name, period, start_time, end_time, namespace, statistics)   
                    
        if not df.empty:
            frames.append(df)              

    df_cost = aws_service.get_aws_cost_and_usage_with_resources(ec2 = ec2, start_time = start_date, end_time = end_date, granularity = "HOURLY", metrics = "AmortizedCost")           

    if not df_cost.empty:
        frames.append(df_cost)    
        
    # merge the different dataframes (cpu_utilization, network_in...) into one dataframe based on start_time    
    try:    
        if not frames == []:

            df_merged = merge_ec2_metrics_on_start_time(frames)           

            df_merged['account_number'] = account_number
                    
            #convert the merged dataframe to class members to ease insert to Elasticsearch
            ec2.performance_counters_list = db_service.create_performance_counters_list(df_merged, metric_list)

            #insert the data into proper elastic index
            response =  db_service.ec2_bulk_insert_elastic(ec2)

    except ValueError as e:
        #happens when aws returns empty values 
        pass   
    
def collect_ec2_all(account, start_date, end_date):
    
        ec2_metric_list =  list(os.environ.get('EC2_PERFORMANCE_METRIC').split(","))      
        ec2_instances = []
        number_of_threads =  int(os.environ.get('EC2_NUMBER_OF_THREADS'))
        
        aws_service = AwsService()    

        ec2_list = aws_service.get_aws_describe_instances(account)

        threads = []

        for i in range(0,len(ec2_list), number_of_threads):
            chunk = ec2_list[i:i + number_of_threads]
            for ec2 in chunk:
                x = threading.Thread(target=collect_ec2_utilization, args=(ec2, ec2_metric_list, account.account_number, start_date, end_date,))
                threads.append(x)
                x.start()
            for index, thread in enumerate(threads):                
                thread.join()                

            threads = []    
        
        for ec2 in ec2_list:
            print(f"instance_id: {ec2.instance_id} ,department = {ec2.department}, account_number: {ec2.account_number}, launch_time: {ec2.launch_time}")                
                
    

def collect_account_services_cost(start_date, end_date):

    aws_service = AwsService() 
    db_service = DbService()

    account = Account(start_date, end_date)
   
    account.get_cost_and_usage(start_date, end_date)

    account.calc_services_forecast()       

    db_service.account_bulk_insert_elastic(account)

    return account

def collect_performance_metrics(account, start_date, end_date):

    aws_service = AwsService()
    db_service = DbService()

    for service in account.services:        

        #if service.name == "Amazon Elastic Compute Cloud - Compute":  
        print(service.name)          
            
        metrics = service.list_metrics(start_date, end_date)
        
        for metric in metrics:
            
            statistics = 'Average'
            namespace =  metric.namespace
            instance_value = metric.dimension_value
            instance_id = metric.dimension_name
            period = 3600
            start_time = start_date
            end_time = end_date

            #if instance_value == "i-02117d25eecd0c8d9":

            datapoints = aws_service.get_aws_metric_statistics(instance_id, instance_value, metric.name, period, start_time, end_time, namespace, statistics) 

            if datapoints != []:

                #print(service.name + "," + metric.name + ", " + metric.dimension_name + ", " + metric.dimension_value)
                metric.datapoints = datapoints
                service.metrics.append(metric)
            
        db_service.account_bulk_insert_elastic(account)
                

    #return acccount


def save_records_in_elasticsearch(account):

    db_service = DbService()
    #insert accounts to elastic
    db_service.account_bulk_insert_elastic(account)

def calc_billing_optimizations(event, context):

    try:    
        

        start_date = os.environ.get('LAMBDA_LAST_UPDATE')
        end_date = date.today().strftime('%Y-%m-%d')
        
        if start_date < end_date:                
            print (f"Running lambda from start_date = {start_date} to {end_date}")
            account = collect_account_services_cost(start_date, end_date)
            #collect_ec2_all(account, start_date, end_date)    
            collect_performance_metrics(account, start_date, end_date)    

            #save_records_in_elasticsearch(account)

        else:
            print(f"start date {start_date} and end date {end_date} are equal. exit...")

        client = boto3.client('lambda')

        response = client.update_function_configuration(
        FunctionName='aws-eco-prod-calc-billing-optimizations',
        Environment={
            'Variables': {
                'LAMBDA_LAST_UPDATE': end_date,            
                'ELASTIC_CONNECTIONSTRING': os.environ.get('ELASTIC_CONNECTIONSTRING'),
                'EC2_PERFORMANCE_METRIC': os.environ.get('EC2_PERFORMANCE_METRIC'),               
                'EC2_NUMBER_OF_THREADS': os.environ.get('EC2_NUMBER_OF_THREADS') 
            }
        },
        )
            
        body = {'message':'Cost Optimization lambda executed successfully!',  'input':event}
        response = {'statusCode':200, 'body':json.dumps(body)}
        return response

    except Exception as e:
        traceback.print_exc()
        body = {'message':'Cost Optimization lambda exits with error! ' + str(e),  'input':event}
        response = {'statusCode':400, 'body':json.dumps(body)}
        return response
