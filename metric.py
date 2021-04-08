
class Metric:
    #metric_name like EBSReadBytes 
    name = ""

    #metric_namespace like AWS/EC2
    namespace = ""

    #like InstanceId
    dimension_name = "" 

    #like i-0c825168d7ad6093a 
    dimension_value = ""

    #sum/avg
    statistics_type = "Average"

    #3600(hour)
    period = 3600

    start_date = ""
    
    end_date = ""


    def __init__(self, name, namespace, dimension_name, dimension_value, statistics_type, period, start_date, end_date):
        
        self.name = name
        self.namespace = namespace
        self.dimension_name = dimension_name
        self.dimension_value = dimension_value
        self.statistics_type = statistics_type
        self.period = period
        self.start_date = start_date
        self.end_date = end_date
        


