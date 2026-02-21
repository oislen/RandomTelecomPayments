import logging
import seaborn as sns

class Transactions():
    
    def __init__(self, data):
        """
        """
        self.data = data
    
    def unique_trans_hash(self):
        """
        """
        unique_trans_hash_cnt = self.data['transaction_hash'].value_counts().sort_values(ascending=False)
        # test assertions
        assert unique_trans_hash_cnt.max() == 1
        assert unique_trans_hash_cnt.min() == 1
        assert not unique_trans_hash_cnt.isnull().any()
        # plot distribution
        sns.histplot(data=unique_trans_hash_cnt.to_frame(),x='count', bins = 10)
    
    def unique_dates(self):
        """
        """
        nunique_trans_dates_per_trans = self.data.groupby(by=['transaction_hash'], dropna=False, as_index=False).agg({'transaction_date':'nunique'})
        # test assertions
        assert nunique_trans_dates_per_trans['transaction_date'].max() == 1
        assert nunique_trans_dates_per_trans['transaction_date'].min() == 1
        assert not nunique_trans_dates_per_trans['transaction_date'].isnull().any()
        # plot distribution
        sns.histplot(data=nunique_trans_dates_per_trans,x='transaction_date', bins = 20)
    
    def unique_trans_amount(self):
        """
        """
        nunique_trans_amounts_per_trans = self.data.groupby(by=['transaction_hash'], dropna=False, as_index=False).agg({'transaction_amount':'nunique'})
        # test assertions
        assert nunique_trans_amounts_per_trans['transaction_amount'].max() == 1
        assert nunique_trans_amounts_per_trans['transaction_amount'].min() == 1
        assert not nunique_trans_amounts_per_trans['transaction_amount'].isnull().any()
        # plot distribution
        sns.histplot(data=nunique_trans_amounts_per_trans,x='transaction_amount', bins = 20)
    
    def unique_payment_method(self):
        """
        """
        nunique_payment_method_per_trans = self.data.groupby(by=['transaction_hash'], dropna=False, as_index=False).agg({'transaction_payment_method':'nunique'}).sort_values('transaction_payment_method')
        unique_payment_method_per_trans_hash = self.data.groupby(by=['card_type', 'transaction_payment_method'], as_index=False, dropna=False).agg({'transaction_hash':'size', 'transaction_amount':'sum'})
        # test assertions
        assert nunique_payment_method_per_trans['transaction_payment_method'].max() == 1
        assert nunique_payment_method_per_trans['transaction_payment_method'].min() == 0
        assert not nunique_payment_method_per_trans['transaction_payment_method'].isnull().any()
        assert unique_payment_method_per_trans_hash['card_type'].isnull().any()
        assert unique_payment_method_per_trans_hash['card_type'].dropna().isin(['Mastercard', 'Visa']).all()
        assert unique_payment_method_per_trans_hash['transaction_payment_method'].isnull().any()
        assert unique_payment_method_per_trans_hash['transaction_payment_method'].dropna().isin(['Card', 'Points', 'Wallet']).all()
        assert (unique_payment_method_per_trans_hash.loc[unique_payment_method_per_trans_hash['transaction_payment_method'].isnull(), 'transaction_amount'] == 0).all()
        assert (unique_payment_method_per_trans_hash.loc[unique_payment_method_per_trans_hash['transaction_payment_method'].notnull(), 'transaction_amount'] > 0).all()
        assert unique_payment_method_per_trans_hash.loc[unique_payment_method_per_trans_hash['transaction_payment_method'] == 'Card', 'card_type'].isin(['Mastercard', 'Visa']).all()
        assert unique_payment_method_per_trans_hash.loc[unique_payment_method_per_trans_hash['transaction_payment_method'] != 'Card', 'card_type'].isnull().all()
        # plot distribution
        sns.histplot(data=nunique_payment_method_per_trans,x='transaction_payment_method', bins = 20)
        logging.info(unique_payment_method_per_trans_hash.to_markdown())
    
    def unique_payment_channel(self):
        """
        """
        nunique_payment_channel_per_trans = self.data.groupby(by=['transaction_hash'], as_index=False).agg({'card_payment_channel':'nunique'}, dropna=False).sort_values('card_payment_channel')
        unique_payment_channel_per_trans_hash = self.data.groupby(by=['transaction_payment_method', 'card_payment_channel'], as_index=False, dropna=False).agg({'transaction_hash':'size', 'transaction_amount':'sum'})
        # test assertions
        assert nunique_payment_channel_per_trans['card_payment_channel'].max() == 1
        assert nunique_payment_channel_per_trans['card_payment_channel'].min() == 0
        assert not nunique_payment_channel_per_trans['card_payment_channel'].isnull().any()
        assert unique_payment_channel_per_trans_hash['transaction_payment_method'].isnull().any()
        assert unique_payment_channel_per_trans_hash['transaction_payment_method'].dropna().isin(['Card', 'Points', 'Wallet']).all()
        assert unique_payment_channel_per_trans_hash['card_payment_channel'].isnull().any()
        assert unique_payment_channel_per_trans_hash['card_payment_channel'].dropna().isin(['Adyen', 'AppStore', 'Docomo', 'PayPal', 'WorldPay']).all()
        assert (unique_payment_channel_per_trans_hash.loc[unique_payment_channel_per_trans_hash['transaction_payment_method'].isnull(), 'transaction_amount'] == 0).all()
        assert (unique_payment_channel_per_trans_hash.loc[unique_payment_channel_per_trans_hash['transaction_payment_method'].notnull(), 'transaction_amount'] > 0).all()
        assert unique_payment_channel_per_trans_hash.loc[unique_payment_channel_per_trans_hash['transaction_payment_method'] == 'Card', 'card_payment_channel'].isin(['Adyen', 'AppStore', 'Docomo', 'PayPal', 'WorldPay']).all()
        assert unique_payment_channel_per_trans_hash.loc[unique_payment_channel_per_trans_hash['transaction_payment_method'] != 'Card', 'card_payment_channel'].isnull().all()
        # plot distribution
        sns.histplot(data=nunique_payment_channel_per_trans,x='card_payment_channel', bins = 20)
        logging.info(unique_payment_channel_per_trans_hash.to_markdown())
    
    def unique_trans_status(self):
        """
        """
        nunique_trans_status_per_trans = self.data.groupby(by=['transaction_hash'], as_index=False).agg({'transaction_status':'nunique'})
        unique_trans_status_per_trans_hash = self.data.groupby(by=['transaction_error_code', 'transaction_status'], as_index=False, dropna=False).size()
        # test assertions
        assert nunique_trans_status_per_trans['transaction_status'].max() == 1
        assert nunique_trans_status_per_trans['transaction_status'].min() == 1
        assert not nunique_trans_status_per_trans['transaction_status'].isnull().any()
        assert unique_trans_status_per_trans_hash['transaction_error_code'].isnull().any()
        assert unique_trans_status_per_trans_hash['transaction_error_code'].dropna().isin(['E900:ConnectionTimeout', 'E901:SuspectedFraud', 'E902:AuthenicationFailure', 'E903:UserCancelled', 'E904:InsufficientFunds']).all()
        assert unique_trans_status_per_trans_hash['transaction_status'].notnull().all()
        assert unique_trans_status_per_trans_hash['transaction_status'].dropna().isin(['Rejected', 'Pending', 'Successful']).all()
        assert unique_trans_status_per_trans_hash.loc[unique_trans_status_per_trans_hash['transaction_error_code'].notnull(), 'transaction_status'].isin(['Rejected']).all()
        assert unique_trans_status_per_trans_hash.loc[unique_trans_status_per_trans_hash['transaction_error_code'].isnull(), 'transaction_status'].isin(['Pending', 'Successful']).all()
        # plot distribution
        sns.histplot(data=nunique_trans_status_per_trans,x='transaction_status', bins = 20)
        logging.info(unique_trans_status_per_trans_hash.to_markdown())
    
    def unique_error_codes(self):
        """
        """
        nunique_errorcodes_per_trans = self.data.groupby(by=['transaction_hash']).agg({'transaction_error_code':'nunique'}, dropna=False, as_index=False)
        unique_error_codes_statuses_per_trans_hash = self.data.groupby(by=['transaction_error_code', 'transaction_status'], as_index=False, dropna=False).size()
        # test assertions
        assert nunique_errorcodes_per_trans['transaction_error_code'].max() == 1
        assert nunique_errorcodes_per_trans['transaction_error_code'].min() == 0
        assert not nunique_errorcodes_per_trans['transaction_error_code'].isnull().any()
        assert unique_error_codes_statuses_per_trans_hash['transaction_error_code'].isnull().any()
        assert unique_error_codes_statuses_per_trans_hash['transaction_error_code'].dropna().isin(['E900:ConnectionTimeout', 'E901:SuspectedFraud', 'E902:AuthenicationFailure', 'E903:UserCancelled', 'E904:InsufficientFunds']).all()
        assert unique_error_codes_statuses_per_trans_hash['transaction_status'].notnull().all()
        assert unique_error_codes_statuses_per_trans_hash['transaction_status'].dropna().isin(['Rejected', 'Pending', 'Successful']).all()
        assert unique_error_codes_statuses_per_trans_hash.loc[unique_error_codes_statuses_per_trans_hash['transaction_error_code'].notnull(), 'transaction_status'].isin(['Rejected']).all()
        assert unique_error_codes_statuses_per_trans_hash.loc[unique_error_codes_statuses_per_trans_hash['transaction_error_code'].isnull(), 'transaction_status'].isin(['Pending', 'Successful']).all()
        # plot distribution
        sns.histplot(data=nunique_errorcodes_per_trans,x='transaction_error_code', bins = 20)
        logging.info(unique_error_codes_statuses_per_trans_hash.to_markdown())
    
    def uid_max_device_trans_error_counts(self):
        """
        """
        nunique_devices_per_uid = self.data.groupby(by='uid', as_index=False).agg({'device_hash':'nunique'}).sort_values(by='device_hash')
        uids_max_devices = self.data.loc[self.data['uid'].isin(nunique_devices_per_uid['uid'].tail()), :].sort_values(by=['uid', 'device_hash', 'transaction_date'])
        uids_with_high_device_hash_counts = uids_max_devices.groupby(by=['userid'], as_index=False).agg({'device_hash':'nunique', 'transaction_hash':'count', 'transaction_error_code':'count'})
        uids_with_high_device_hash_counts_error_codes = uids_max_devices.groupby(by=['transaction_error_code'], as_index=False).size().sort_values(by='size', ascending=False)
        # plot distribution
        logging.info(uids_with_high_device_hash_counts.to_markdown())
        logging.info(uids_with_high_device_hash_counts_error_codes.to_markdown())
    
    def uid_max_card_trans_error_counts(self):
        """
        """
        nunique_cards_per_uid = self.data.groupby(by='uid', as_index=False).agg({'card_hash':'nunique'}).sort_values(by='card_hash')
        uids_max_cards = self.data.loc[self.data['uid'].isin(nunique_cards_per_uid['uid'].tail()), :].sort_values(by=['uid', 'card_hash', 'transaction_date'])
        uids_with_high_card_hash_counts = uids_max_cards.groupby(by=['userid'], as_index=False).agg({'card_hash':'nunique', 'transaction_hash':'count', 'transaction_error_code':'count'})
        uids_with_high_card_hash_counts_error_codes = uids_max_cards.groupby(by=['transaction_error_code'], as_index=False).size().sort_values(by='size', ascending=False)
        # plot distribution
        logging.info(uids_with_high_card_hash_counts.to_markdown())
        logging.info(uids_with_high_card_hash_counts_error_codes.to_markdown())

    def uid_max_ip_trans_error_counts(self):
        """
        """
        nunique_ips_per_uid = self.data.groupby(by='uid', as_index=False, dropna=False).agg({'ip_hash':'nunique'}).sort_values(by='ip_hash')
        uids_max_ips = self.data.loc[self.data['uid'].isin(nunique_ips_per_uid['uid'].tail()), :].sort_values(by=['uid', 'ip_hash', 'transaction_date'])
        uids_with_high_ip_hash_counts = uids_max_ips.groupby(by=['userid'], as_index=False).agg({'ip_hash':'nunique', 'transaction_hash':'count', 'transaction_error_code':'count'})
        uids_with_high_ip_hash_counts_error_codes = uids_max_ips.groupby(by=['transaction_error_code'], as_index=False).size().sort_values(by='size', ascending=False)
        # plot distribution
        logging.info(uids_with_high_ip_hash_counts.to_markdown())
        logging.info(uids_with_high_ip_hash_counts_error_codes.to_markdown())