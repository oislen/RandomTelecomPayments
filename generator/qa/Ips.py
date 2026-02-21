import logging
import seaborn as sns

class Ips():
    
    def __init__(self, data, show_logs=False, show_plots=False):
        """
        """
        logging.info("Initialising Ips QA")
        self.data = data
        self.show_logs = show_logs
        self.show_plots = show_plots
    
    def unique_country_codes(self):
        """
        """
        nunique_country_codes_per_ip = self.data.groupby(by=['ip_hash'], as_index=False, dropna=False).agg({'ip_country_code':'nunique'})
        ip_country_codes_totals = self.data.groupby(by=['ip_country_code'], as_index=False, dropna=False).size()
        # test assertions
        assert nunique_country_codes_per_ip['ip_country_code'].max() == 1
        assert nunique_country_codes_per_ip['ip_country_code'].min() == 1
        assert not nunique_country_codes_per_ip['ip_country_code'].isnull().any()
        if self.show_plots:
            # plot distribution
            sns.histplot(data=nunique_country_codes_per_ip,x='ip_country_code', bins = 20)
        if self.show_logs:
            # show logs
            logging.info(ip_country_codes_totals.to_markdown())
    
    def run_all(self):
        """
        """
        self.unique_country_codes()
        logging.info("All Ips QA checks passed.")