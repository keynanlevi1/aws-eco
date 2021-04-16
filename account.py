import boto3
from service import Service
from utility import Utility
from aws_service import AwsService
from decimal import Decimal
from datapoint import Datapoint
from metric import Metric
from collections import defaultdict

class Account:

    def __init__(self, start_date, end_date):
        
        self.account_number = self.get_account_number()
        self.department = Utility.map_department_to_account(self.account_number)
        self.account_name = Utility.map_account_name_to_account_number(self.account_number)        
        self.services = []
        self.start_date = start_date
        self.end_date = end_date
    
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

        self.set_account_services_cost(response)         

    def set_account_services_cost(self, response):


        service_list = defaultdict(list)
        metric_list = defaultdict(list)
        

        for row in response['ResultsByTime']:
            start = row['TimePeriod']['Start']
            end = row['TimePeriod']['End']
            for group in row['Groups']:     
                service_name = group['Keys'][0]  #keys = service   
                for metric in group['Metrics']:
                    metric_name = metric
                    value = round(Decimal(group['Metrics'][metric]['Amount']),4)
                    datapoint = Datapoint(value = value, start = start, end = end)
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
                        metric = Metric(name = metric_name, dimension_name = "Service", dimension_value = service.name, start_date = self.start_date, end_date = self.end_date,  statistics_type = "sum", period=1440)                        
                        metrics[metric_name] = metric
                        #print("once " + metric_name + " " + service_name)
                    else:
                        metric = metrics[metric_name]
                        #print("many " + metric_name + " " + service_name)
                    #print(type(row[metric_name]))
                    #print(row[metric_name])
                    metric.datapoints.append(row[metric_name][0])

            for key in metrics:  
                #print(key + " " + service_name)
                #print(service.name)
                #print(metrics[key])
                
                service.metrics.append(metrics[key])
                #print(service.name)
                #print(service.metrics)
            
            metrics.clear()
            
        for service in services:
            self.services.append(services[service])
        
        print(self.services)
        
        '''
        for service in services:
            print(services[service].name)
            #print(services[service].metrics)  
            for metric in services[service].metrics:
                print(metric.name)
                for datapoint in metric.datapoints:
                    #print(type(datapoint))
                    print(datapoint.value)
                    print(datapoint.start)
                    print(datapoint.end)
        '''
        

    def calc_services_forecast(self):

        for service in self.services:
            service.calc_forecast()


