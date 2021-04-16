
class Metric:
    
    def __init__(self, name, namespace, dimension_name, dimension_value, statistics_type, period, start_date, end_date):
        
        self.name = name
        self.namespace = namespace
        self.dimension_name = dimension_name
        self.dimension_value = dimension_value
        self.statistics_type = statistics_type
        self.period = period
        self.start_date = start_date
        self.end_date = end_date

    def __init__(self, name):
        
        self.name = name
         #metric_name like EBSReadBytes 
        self.name = ""

        #metric_namespace like AWS/EC2
        self.namespace = ""

        #like InstanceId
        self.dimension_name = "" 

        #like i-0c825168d7ad6093a 
        self.dimension_value = ""

        #sum/avg
        self.statistics_type = "Average"

        #3600(hour)
        self.period = 3600

        self.start_date = ""
        
        self.end_date = ""

        self.datapoints = []
        


