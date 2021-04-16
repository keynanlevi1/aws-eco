import boto3
from service import Service
from utility import Utility
from aws_service import AwsService
from decimal import Decimal
from datapoint import Datapoint
from metric import Metric
from collections import defaultdict

class Account:

    def __init__(self):
        
        self.account_number = self.get_account_number()
        self.department = Utility.map_department_to_account(self.account_number)
        self.account_name = Utility.map_account_name_to_account_number(self.account_number)        
        self.services = []
    
    def get_account_number(self):

        client = boto3.client('sts')
        response = client.get_caller_identity()
        account_number = str(response['Account'])

        return account_number

    def get_cost_and_usage(self, start_date, end_date):        

        granularity = 'DAILY'
        metrics = 'AMORTIZED_COST'
        groupby = 'SERVICE' # like EC2, RDS, ...

        aws_service = AwsService()

        #response holds the cost per service but needs to be parse
        response = aws_service.get_aws_cost_and_usage(self.account_number, start_date, end_date, granularity, metrics, groupby)

        self.services = self.set_account_services_cost(response)         

    def set_account_services_cost(self, response):

        services = []

        service_list = defaultdict(list)
        metric_list = defaultdict(list)
        

        for row in response['ResultsByTime']:
            start = row['TimePeriod']['Start']
            end = row['TimePeriod']['End']
            for group in row['Groups']:     
                service_name = group['Keys'][0]  #keys = service   
                for metric in group['Metrics']:
                    metric_name = metric
                    amount = round(Decimal(group['Metrics'][metric]['Amount']),4)
                    datapoint = Datapoint(amount = amount, start = start, end = end)
                    metric_list[metric_name].append(datapoint)

                
                service_list[service_name].append(dict(metric_list.copy()))

                metric_list.clear()
        
      
        
        service_list = dict(service_list)
        datapoints = []
       
        
        services = defaultdict(list)
        metrics = defaultdict(list)

        for service_name in service_list:
            #print(service_name)
            if service_name not in services.keys():
                service = Service(service_name)
                services[service_name] = service
            else:
                service = services[service_name]

            for row in service_list[service_name]:
                                
                for metric_name in row:
                    #print(metric_name)
                
                    if metric_name not in metrics.keys():
                        metric = Metric(metric_name)                        
                        metrics[metric_name] = metric
                        #print("once " + metric_name + " " + service_name)
                    else:
                        metric = metrics[metric_name]
                        #print("many " + metric_name + " " + service_name)
                        
                    metric.datapoints.append(row[metric_name])

            for key in metrics:  
                #print(key + " " + service_name)
                #print(service.name)
                #print(metrics[key])
                
                service.metrics.append(metrics[key])
                print(service.name)
                print(service.metrics)
            
            metrics.clear()
            
        
        
        '''
        for service in services:
            print(service)
            print(services[service].metrics)  
        '''
            #print(services[service].metrics)
            #print("type:")
            #print(type(services[service].metrics))
        '''
        for metric in services[service].metrics:
            print(metric)     
            print(type(metric))
        '''
                #for datapoint in 
            
                    #datapoints.append(metric[metric_name])
                    

        
            #print(service_name)
            #print(service_list[service_name])
            #print("******************************")
        
       
        
        '''
        for row in service_list:

            print(row)
            for metric in service_list[row]:
                
                for metric_name in metric:
                    print(metric_name)
                    print(metric[metric_name])
                    
        '''
           
            
            
           
    
                

        #print(service_list)


        return services

    def calc_services_forecast(self):

        for service in self.services:
            service.calc_forecast()


