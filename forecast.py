
from datetime import datetime, date
from dateutil.relativedelta import *
from decimal import Decimal
from aws_service import AwsService

class Forecast:
    
    def __init__(self):
        
        self.forecast_mean_value = 0
        self.forecast_prediction_interval_lowerbound = 0    
        self.forecast_prediction_interval_upperbound = 0
    
    
    def calc_forecast(self, service_name):
                
        #aws forecast get only string days. The calculation is done from today till the end of the month.

        today = date.today()
        start = today.strftime('%Y-%m-%d')
        start_datetime = datetime.strptime(start, '%Y-%m-%d')
        end_datetime = start_datetime.replace(day=1) + relativedelta(months=+1)
        end = end_datetime.strftime('%Y-%m-%d')

        aws_service = AwsService()

        response = aws_service.get_aws_cost_forecast(start, end, "MONTHLY", "AMORTIZED_COST", service_name)

        if response != "":

            self.forecast_mean_value = round(Decimal(response['ForecastResultsByTime'][0]['MeanValue']),2)
            self.forecast_prediction_interval_lowerbound = round(Decimal(response['ForecastResultsByTime'][0]['PredictionIntervalLowerBound']),2)
            self.forecast_prediction_interval_upperbound = round(Decimal(response['ForecastResultsByTime'][0]['PredictionIntervalUpperBound']),2)
            