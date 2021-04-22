import json, sys, os
import subprocess
import threading
import boto3
from datetime import datetime, date
from dateutil.relativedelta import *
from decimal import Decimal
from account import Account
import traceback 


subprocess.call('pip3 install elasticsearch -t /tmp/ --no-cache-dir'.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.call('pip3 install python-dotenv -t /tmp/ --no-cache-dir'.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
sys.path.insert(1, '/tmp/')

from ec2 import EC2
from aws_service import AwsService
from db_service import DbService
from performance_counters import PerformanceCounters
from dotenv import load_dotenv
from functools import reduce


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

            datapoints = aws_service.get_aws_metric_statistics(instance_id, instance_value, metric.name, period, start_time, end_time, namespace, statistics) 

            if datapoints != []:

                metric.datapoints = datapoints
                service.metrics.append(metric)
            
        db_service.account_bulk_insert_elastic(account)
                

def calc_billing_optimizations(event, context):

    try:    
        

        start_date = os.environ.get('LAMBDA_LAST_UPDATE')
        end_date = date.today().strftime('%Y-%m-%d')
        
        if start_date < end_date:                
            print (f"Running lambda from start_date = {start_date} to {end_date}")
            account = collect_account_services_cost(start_date, end_date)
            collect_performance_metrics(account, start_date, end_date)    

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
