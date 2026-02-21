import logging
import seaborn as sns

class Cards():
    
    def __init__(self, data, show_logs=False, show_plots=False):
        """
        """
        logging.info("Initialising Cards QA")
        self.data = data
        self.show_logs = show_logs
        self.show_plots = show_plots
    
    def unique_card_types(self):
        """
        """
        nunique_card_types_per_card = self.data.groupby(by=['card_hash'], as_index=False, dropna=False).agg({'card_type':'nunique'})
        card_type_payment_totals = self.data.groupby(by=['card_type', 'transaction_payment_method'], as_index=False, dropna=False).agg({'transaction_hash':'size', 'transaction_amount':'sum'})
        # test assertions
        assert nunique_card_types_per_card['card_type'].max() == 1
        assert nunique_card_types_per_card['card_type'].min() == 0
        assert not nunique_card_types_per_card['card_type'].isnull().any()
        if self.show_plots:
            # plot distribution
            sns.histplot(data=nunique_card_types_per_card,x='card_type', bins = 20)
        if self.show_logs:
            # show logs
            logging.info(card_type_payment_totals)
    
    def unique_country_codes(self):
        """
        """
        nunique_country_codes_per_card = self.data.groupby(by=['card_hash'], as_index=False, dropna=False).agg({'card_country_code':'nunique'})
        card_country_code_payment_totals = self.data.assign(card_country_code=self.data['card_country_code'].notnull().astype(int)).groupby(by=['card_country_code', 'transaction_payment_method'], as_index=False, dropna=False).agg({'transaction_hash':'size', 'transaction_amount':'sum'})
        # test assertions
        assert nunique_country_codes_per_card['card_country_code'].max() == 1
        assert nunique_country_codes_per_card['card_country_code'].min() == 0
        assert not nunique_country_codes_per_card['card_country_code'].isnull().any()
        if self.show_plots:
            # plot distribution
            sns.histplot(data=nunique_country_codes_per_card,x='card_country_code', bins = 20)
        if self.show_logs:
            # show logs
            logging.info(card_country_code_payment_totals)
    
    def run_all(self):
        """
        """
        self.unique_card_types()
        self.unique_country_codes()
        logging.info("All Cards QA checks passed.")