import logging
import seaborn as sns

class Ips():
    
    def __init__(self, data):
        """
        """
        self.data = data
    
    def unique_country_codes(self):
        """
        """
        nunique_country_codes_per_ip = self.data.groupby(by=['ip_hash'], as_index=False, dropna=False).agg({'ip_country_code':'nunique'})
        ip_country_codes_totals = self.data.groupby(by=['ip_country_code'], as_index=False, dropna=False).size()
        # test assertions
        assert nunique_country_codes_per_ip['ip_country_code'].max() == 1
        assert nunique_country_codes_per_ip['ip_country_code'].min() == 1
        assert not nunique_country_codes_per_ip['ip_country_code'].isnull().any()
        # plot distribution
        sns.histplot(data=nunique_country_codes_per_ip,x='ip_country_code', bins = 20)
        logging.info(ip_country_codes_totals.to_markdown())