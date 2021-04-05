from utility import Utility
from forecast import Forecast
from aws_service import AwsService

class Service:

    def __init__(self, name, datapoints):

        self.name = name
        self.namespace = Utility.get_service_namespace(name)
        self.datapoints = datapoints        

    
    def calc_forecast(self):
        self.forecast = Forecast()
        self.forecast.calc_forecast(self.name)
        

    

