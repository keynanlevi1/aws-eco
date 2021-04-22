import traceback 
from performance_counters import PerformanceCounters
from thresholds import Thresholds
from datapoint import Datapoint
from elasticsearch import Elasticsearch
import elasticsearch.helpers as helpers
from datetime import datetime
import os
from decimal import Decimal
from elasticsearch.client.ingest import IngestClient
from utility import Utility

class DbService:
    
    def account_bulk_insert_elastic(self, account):

        ElasticConnectionString = os.getenv("ELASTIC_CONNECTIONSTRING")
        
        targetES = Elasticsearch(ElasticConnectionString)

        p = IngestClient(targetES)

        if not p.get_pipeline(id = "account-cost-threshold"):        
            p.put_pipeline(id='account-cost-threshold', body={
                'description': "add threshold",
                'processors': [
                {
                    "set": {
                    "field": "_source.ingest_time",
                    "value": "{{_ingest.timestamp}}"
                    }
                },
                {
                    "script": {
                    "lang": "painless",
                    "source": "\r\n          if (ctx.containsKey(\"department\")) { \r\n            String unit = ctx['department'];\r\n            int value;\r\n            if (unit == \"SAST\") { \r\n              value = 25000; \r\n            } \r\n            else if (unit == \"CxGo\") { \r\n              value = 15000; \r\n            } \r\n            else if (unit == \"AST\") { \r\n              value = 7000; \r\n            } \r\n            else if (unit == \"AST Integration\") { \r\n              value = 1000; \r\n            } \r\n            else if (unit == \"CB\") { \r\n              value = 5000; \r\n            } \r\n            else if (unit == \"SCA\") {\r\n              value = 85000; \r\n            } \r\n            else {\r\n              value = 20000; \r\n            }\r\n            ctx['threshold_value'] = value;\r\n          }\r\n        "
                    }
                }
                ]
            })

        now = datetime.now()
        target_index_name = "aws-eco-account-cost-" + now.strftime("%m-%Y")        
        index_template_name = "aws-eco-account-cost-template"

        #targetES.indices.delete(index=target_index_name, ignore=[400, 404])
        request_body = {
        "index_patterns": ["aws-eco-account-cost-*"],
        "settings" : {
            "number_of_shards": 1,
            "number_of_replicas": 1,
            "index": {"codec": "best_compression"},
            "default_pipeline": "account-cost-threshold",

        },
        'mappings': {            
            'properties': { 
                'department': {'type': 'keyword'},   
                'account_name': {'type': 'keyword'},          
                'account_number': {'type': 'keyword'},
                'keys': {'type': 'keyword'},
                'value': {'type': 'float'},
                'dimension_name': {'type': 'keyword'},
                'dimension_value': {'type': 'keyword'},
                'start_time': {'format': 'dateOptionalTime', 'type': 'date'},
                'end_time': {'format': 'dateOptionalTime', 'type': 'date'},                        
                'metrics': {'type': 'keyword'},
                'forecast_mean_value': {'type': 'float'},
                'forecast_prediction_interval_lowerbound': {'type': 'float'},
                'forecast_prediction_interval_upperbound': {'type': 'float'},
            }}
        }

        if not targetES.indices.exists_template(index_template_name):
            targetES.indices.put_template(index_template_name, request_body, create=True)
               
        documents =[]
      
        for service in account.services:
            for metric in service.metrics:
                for datapoint in metric.datapoints:
                    
                    if datapoint != []:                       
    
                        new_row = {"_id": (account.account_number + "-" + metric.dimension_name + "-"+metric.dimension_value + "-" + datetime.strptime(datapoint.start, "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d%H%M%S")).replace(" ", ""), \
                            "department": account.department, \
                            "account_name":account.account_name, \
                            "account_number":account.account_number,\
                            "keys":service.name,\
                            "value":datapoint.value, \
                            "dimension_name":metric.dimension_name, \
                            "dimension_value":metric.dimension_value, \
                            "start_time": datetime.strptime(datapoint.start, "%Y-%m-%d %H:%M:%S"), \
                            "end_time": datetime.strptime(datapoint.end, "%Y-%m-%d %H:%M:%S"),\
                            "metrics": metric.name, \
                            "forecast_mean_value": service.forecast.forecast_mean_value, \
                            "forecast_prediction_interval_lowerbound": service.forecast.forecast_prediction_interval_lowerbound, \
                            "forecast_prediction_interval_upperbound": service.forecast.forecast_prediction_interval_upperbound  }

                        documents.append(new_row)
        
        if documents != []:
            
            helpers.bulk(targetES, documents, index=target_index_name,doc_type='_doc', raise_on_error=True)     

    def create_performance_counters_list(self, df_merged, metric_list):

        performance_counters_list = []

        for index, row in df_merged.iterrows():
            
            start_time = row['start_time'] 
            cost = row['cost']
            cpu_utilization = row['CPUUtilization'] if 'CPUUtilization' in metric_list and 'CPUUtilization' in df_merged.columns else 0
            network_in = row['NetworkIn'] if 'NetworkIn' in metric_list and 'NetworkIn' in df_merged.columns else 0
            network_out = row['NetworkOut'] if 'NetworkOut' in metric_list and 'NetworkOut' in df_merged.columns else 0                  
            disk_write_ops = row['DiskWriteOps'] if 'DiskWriteOps' in metric_list and 'DiskWriteOps' in df_merged.columns else 0
            disk_read_ops = row['DiskReadOps'] if 'DiskReadOps' in metric_list and 'DiskReadOps' in df_merged.columns else 0
            disk_write_bytes = row['DiskWriteBytes'] if 'DiskWriteBytes' in metric_list and 'DiskWriteBytes' in df_merged.columns else 0
            disk_read_bytes = row['DiskReadBytes'] if 'DiskReadBytes' in metric_list and 'DiskReadBytes' in df_merged.columns else 0
            ebs_read_bytes = row['EBSReadBytes'] if 'EBSReadBytes' in metric_list and 'EBSReadBytes' in df_merged.columns else 0
            ebs_write_bytes = row['EBSWriteBytes'] if 'EBSWriteBytes' in metric_list and 'EBSWriteBytes' in df_merged.columns else 0
            is_idle = row['is_cpu_utilization_idle'] if 'CPUUtilization' in metric_list and 'is_cpu_utilization_idle' in df_merged.columns else 1 * \
                row['is_network_in_idle'] if 'NetworkIn' in metric_list and 'is_network_in_idle' in df_merged.is_network_in_idle else 1 * \
                row['is_network_out_idle'] if 'NetworkOut' in metric_list and 'is_network_out_idle' in df_merged.columns else 1 
                

            performance_counters = PerformanceCounters(start_time = start_time,cpu_utilization = cpu_utilization, network_in = network_in, network_out = network_out, disk_write_ops = disk_write_ops, disk_read_ops = disk_read_ops, ebs_write_bytes = ebs_write_bytes, ebs_read_bytes = ebs_read_bytes,  disk_write_bytes = disk_write_bytes, disk_read_bytes = disk_read_bytes, is_idle = is_idle, cost = cost)
            performance_counters_list.append(performance_counters)  

        return performance_counters_list
                
            
           
        
        

