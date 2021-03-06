import os
import boto3
from ec2 import EC2
from thresholds import Thresholds
from datapoint import Datapoint
from decimal import Decimal
from datetime import datetime, timedelta
from utility import Utility

class AwsService: 

    def get_supported_metrics(self, ec2):
        
        metric_list = []
        
        client = boto3.client('cloudwatch')

        response = client.list_metrics(Namespace='AWS/EC2',
            Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': ec2.instance_id
            },
        ])

        for metric in response['Metrics']:
            metric_list.append(metric['MetricName'])

        return metric_list

    def get_aws_cost_forecast(self, start, end, granularity, metrics, groupby):
        
        response = ""

        client = boto3.client('ce')
        
        try:
            response = response = client.get_cost_forecast(
                TimePeriod={
                'Start': start,
                'End': end
                },
                Granularity=granularity,
                Metric=metrics,            
                Filter={      
                    "Dimensions": {
                    "Key": "SERVICE",
                    "Values": [
                        groupby
                    ]
                    }
                },
                PredictionIntervalLevel=80,
            )
        except Exception as e:
            if type(Exception) == "botocore.errorfactory.DataUnavailableException":
                pass
                return

        return response


    def get_aws_cost_and_usage(self, account_number, start, end, granularity, metrics, groupby):
        
        client = boto3.client('ce')

        response = client.get_cost_and_usage(
            TimePeriod={
                'Start': start,
                'End': end
            },
            Granularity=granularity,
            Metrics=[metrics],
            GroupBy=[
            {
                'Type': 'DIMENSION',
                'Key': groupby
            }]
        )

        return response
       
    def get_aws_describe_instances(self,account):
        
        ec2_list = []
        session = boto3.Session()
        ec2 = session.resource('ec2')
        instances = ec2.instances.filter()

        for instance in instances:
            availability_zone = instance.placement["AvailabilityZone"]           
            state = instance.state['Name']                                                             
            
            if state == "running":
           
                ec2 = EC2(availability_zone, instance.id, instance.instance_type, instance.launch_time, state,  instance.ebs_optimized, account.account_number, account.department, account.account_name)
                ec2_list.append(ec2)

        return ec2_list    
    
    def get_aws_metric_statistics(self, instance_id, instance_value, metric_name, period, start_time, end_time, namespace, statistics):
        
        cloudwatch = boto3.client('cloudwatch')

        start_time = start_time + 'T00:00:00Z'
        end_time = end_time + 'T00:00:00Z'

        start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ')
        end_time = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%SZ')        
        
        response = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        Dimensions=[
            {
                'Name': instance_id,
                'Value': instance_value
            }
        ],
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=[statistics]
        )        

        results = response["Datapoints"]

        datapoints = []

        
        for row in results:
            start_time = row["Timestamp"].strftime("%Y-%m-%d %H:%M:%S")
            start = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            end = start + timedelta(seconds=period)
            end = end.strftime("%Y-%m-%d %H:%M:%S")
            value = row["Average"]
            
            datapoint = Datapoint(value, start_time, end)
            datapoints.append(datapoint)

        return datapoints
