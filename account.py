import boto3
from service import Service
from utility import Utility
from aws_service import AwsService
from decimal import Decimal
from datapoint import Datapoint


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

        response = aws_service.get_aws_cost_and_usage(self.account_number, start_date, end_date, granularity, metrics, groupby)
        #response holds the cost and usage per service but needs to be parse

        self.services = self.set_account_services_cost(response)    


    def set_account_services_cost(self, response):

        services = []
        datapoints = []

        for row in response['ResultsByTime']:
            start = row['TimePeriod']['Start']
            end = row['TimePeriod']['End']
            for group in row['Groups']:               
                keys = group['Keys'][0]  #keys = service
                service_name = keys
                amount = round(Decimal(group['Metrics']['AmortizedCost']['Amount']),4)
                key_list = list(group['Metrics'].keys())                
                metrics = key_list[0] #metrics = 'AmortizedCost'
                
                #A single datapoint holds one sample (event) like the cost of a servive in a spesific time (hour)
                datapoint = Datapoint(department = self.department, account_name = self.account_name, account_number = self.account_number, keys = keys, amount = amount, start = start, end = end, metrics = metrics)
                datapoints.append(datapoint)

            #Service holds a set of datapoints
            service = Service(service_name, datapoints)
            #Account holds a set of services
            services.append(service)

            datapoints = []

        return services

    def calc_services_forecast(self):

        for service in self.services:
            service.calc_forecast()

