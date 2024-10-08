import cons
from datetime import datetime

class ProgrammeParams():
    
    def __init__(self, n_users=100, random_seed=None, n_applications=20000, registration_start_date='2020-01-01', registration_end_date='2020-12-31', transaction_start_date='2021-01-01', transaction_end_date='2021-12-31'):
        # take programme parameters from class parameters
        self.random_seed = random_seed
        self.n_users = n_users
        self.n_applications = n_applications
        self.registration_start_date = registration_start_date
        self.registration_end_date = registration_end_date
        self.transaction_start_date = transaction_start_date
        self.transaction_end_date = transaction_end_date
        transaction_start_date_strftime = datetime.strptime(self.transaction_start_date, cons.date_date_strftime)
        transaction_end_date_strftime = datetime.strptime(self.transaction_end_date, cons.date_date_strftime)
        self.transaction_timescale = ((transaction_end_date_strftime - transaction_start_date_strftime).days + 1) / 365