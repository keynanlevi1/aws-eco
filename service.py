from utility import Utility
from forecast import Forecast
from aws_service import AwsService
import boto3
from metric import Metric

class Service:


    def __init__(self, name, datapoints):

        self.name = name
        self.namespace = Utility.get_service_namespace(name)
        self.datapoints = datapoints  
        self.metrics = []
        self.name = ""
        self.namespace = ""

    def __init__(self, name):
        
        self.name = name
        self.metrics = []        
        self.namespace = Utility.get_service_namespace(name)
        
        

    
    def calc_forecast(self):
        self.forecast = Forecast()
        self.forecast.calc_forecast(self.name)

    def list_metrics(self, start_date, end_date):

        # Create CloudWatch client
        cloudwatch = boto3.client('cloudwatch')

        metrics = []

        statistics_type = 'Average'
        period = 3600 #hour

        # List metrics through the pagination interface
        paginator = cloudwatch.get_paginator('list_metrics')
        for response in paginator.paginate(Namespace=self.namespace):
            for row in response['Metrics']:
                metric_name = row['MetricName']
                
                for row2 in row['Dimensions']:
                    dimension_name = row2['Name']
                    dimension_value = row2['Value']

                    metric = Metric(metric_name, self.namespace,  dimension_name, dimension_value, statistics_type, period, start_date, end_date)
                    metrics.append(metric)

        return metrics

        

    

