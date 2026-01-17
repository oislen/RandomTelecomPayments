from datetime import datetime
from beartype import beartype

import cons

class ProgrammeParams():
    """
    Class to manage and store programme parameters for the telecom payment generator.
    This class validates and initializes all configuration parameters needed for the
    payment generation process, including user counts, application volumes, and date ranges
    for registration and transaction periods.

    Parameters
    ----------
    n_users : int, optional
        Number of users. Defaults to 100.
    random_seed : int, optional
        Seed for reproducible randomization. Defaults to None.
    n_applications : int, optional
        Number of applications. Defaults to 20000.
    registration_start_date : str, optional
        Registration period start date. Defaults to cons.default_registration_start_date.
    registration_end_date : str, optional
        Registration period end date. Defaults to cons.default_registration_end_date.
    transaction_start_date : str, optional
        Transaction period start date. Defaults to cons.default_transaction_start_date.
    transaction_end_date : str, optional
        Transaction period end date. Defaults to cons.default_transaction_end_date.
    
    Attributes
    ----------
    random_seed : int, optional
        Seed for random number generation for reproducibility.
    n_users : int
        Number of users to generate. Defaults to 100.
    n_applications : int
        Number of applications to generate. Defaults to 20000.
    registration_start_date : str
        Start date for user registration (format: YYYY-MM-DD).
    registration_end_date : str
        End date for user registration (format: YYYY-MM-DD).
    transaction_start_date : str
        Start date for transactions (format: YYYY-MM-DD).
    transaction_end_date : str
        End date for transactions (format: YYYY-MM-DD).
    transaction_timescale : float
        The transaction period duration in years.
    """
    
    @beartype
    def __init__(
        self,
        n_users:int=100,
        random_seed:int=None,
        n_applications:int=20000,
        registration_start_date:str=cons.default_registration_start_date,
        registration_end_date:str=cons.default_registration_end_date,
        transaction_start_date:str=cons.default_transaction_start_date,
        transaction_end_date:str=cons.default_transaction_end_date,
        ):
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