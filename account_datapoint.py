
class AccountDatapoint:

    def __init__(self, department, account_number, keys, amount, start, end, metrics, account_name):


        self.department = department
        self.account_name = account_name
        self.account_number = account_number        
        self.keys = keys  #keys = service (EC2, RDS, ...)
        self.amount = amount      
        self.start = start
        self.end = end
        self.metrics = metrics
        self.forecast_mean_value = 0
        self.forecast_prediction_interval_lowerbound = 0    
        self.forecast_prediction_interval_upperbound = 0  

