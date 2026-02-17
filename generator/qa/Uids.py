import logging
import seaborn as sns

class Uids():

    def __init__(self, data):
        """
        """
        self.data = data
    
    def unique_user_ids(self):
        """
        """
        nunique_user_ids_per_uid = self.data.groupby(by='uid', dropna=False, as_index=False).agg({'userid':'nunique'}).sort_values(by=['userid'])
        # test assertions
        assert nunique_user_ids_per_uid['userid'].max() == 1
        assert nunique_user_ids_per_uid['userid'].min() == 1
        assert not self.data['userid'].isnull().any()
        # plot distribution
        sns.histplot(data=nunique_user_ids_per_uid,x='userid', bins = 20)
    
    def unique_names(self):
        """
        """
        tmp_data = self.data.copy()
        tmp_data['fullname'] = tmp_data['first_name'] + ' ' + tmp_data['last_name']
        nunique_names_per_uid = tmp_data.groupby(['userid'], dropna=False, as_index=False).agg({'fullname':'nunique'}).sort_values(by=['fullname'])
        # test assertions
        assert nunique_names_per_uid['fullname'].max() == 1
        assert nunique_names_per_uid['fullname'].min() == 1
        assert not tmp_data['fullname'].isnull().any()
        # plot distribution
        sns.histplot(data=nunique_names_per_uid,x='fullname', bins = 20)
    
    def unique_reg_dates(self):
        """
        """
        nunique_reg_date_per_uid = self.data.groupby(by='uid', dropna=False, as_index=False).agg({'registration_date':'nunique'}).sort_values(by=['registration_date'])
        # test assertions
        assert nunique_reg_date_per_uid['registration_date'].max() == 1
        assert nunique_reg_date_per_uid['registration_date'].min() == 1
        assert not self.data['registration_date'].isnull().any()
        # plot distribution
        sns.histplot(data=nunique_reg_date_per_uid,x='registration_date', bins = 20)
    
    def nunique_reg_countries(self):
        """
        """
        nunique_reg_country_per_uid = self.data.groupby(by='uid', dropna=False, as_index=False).agg({'registration_country_code':'nunique'}).sort_values(by=['registration_country_code'])
        # test assertions
        assert nunique_reg_country_per_uid['registration_country_code'].max() == 1
        assert nunique_reg_country_per_uid['registration_country_code'].min() == 1
        assert not self.data['registration_country_code'].isnull().any()
        # plot distribution
        sns.histplot(data=nunique_reg_country_per_uid,x='registration_country_code', bins = 20)
    
    def unique_email_domains(self):
        """
        """
        nunique_email_domains_per_uid = self.data.groupby(by='uid', dropna=False, as_index=False).agg({'email_domain':'nunique'}).sort_values(by=['email_domain'])
        # test assertions
        assert nunique_email_domains_per_uid['email_domain'].max() == 1
        assert nunique_email_domains_per_uid['email_domain'].min() == 1
        assert not self.data['email_domain'].isnull().any()
        # plot distribution
        sns.histplot(data=nunique_email_domains_per_uid,x='email_domain', bins = 20)
    
    def unique_devices(self):
        """
        """
        nunique_devices_per_uid = self.data.groupby(by='uid', dropna=False, as_index=False).agg({'device_hash':'nunique'}).sort_values(by=['device_hash'])
        # test assertions
        assert nunique_devices_per_uid['device_hash'].max() <= 3
        assert nunique_devices_per_uid['device_hash'].min() == 1
        assert not self.data['device_hash'].isnull().any()
        # plot distribution
        sns.histplot(data=nunique_devices_per_uid,x='device_hash', bins = 20)

    def unique_cards(self):
        """
        """
        nunique_cards_per_uid = self.data.groupby(by='uid', dropna=False, as_index=False).agg({'card_hash':'nunique'}).sort_values(by=['card_hash'])
        # test assertions
        assert nunique_cards_per_uid['card_hash'].max() <= 2
        assert nunique_cards_per_uid['card_hash'].min() == 1
        assert self.data['card_hash'].isnull().any()
        # plot distribution
        sns.histplot(data=nunique_cards_per_uid,x='card_hash', bins = 20)
    
    def unique_ips(self):
        """
        """
        nunique_ips_per_uid = self.data.groupby(by='uid', dropna=False, as_index=False).agg({'ip_hash':'nunique'}).sort_values(by=['ip_hash'])
        # test assertions
        assert nunique_ips_per_uid['ip_hash'].max() <= 30
        assert nunique_ips_per_uid['ip_hash'].min() == 1
        assert not self.data['ip_hash'].isnull().any()
        # plot distribution
        sns.histplot(data=nunique_ips_per_uid,x='ip_hash', bins = 10)

    def unique_apps(self):
        """
        """
        nunique_apps_per_uid = self.data.groupby(by='uid', dropna=False, as_index=False).agg({'application_hash':'nunique'}).sort_values(by=['application_hash'])
        # test assertions
        assert nunique_apps_per_uid['application_hash'].max() <= 30
        assert nunique_apps_per_uid['application_hash'].min() == 1
        assert not self.data['application_hash'].isnull().any()
        # plot distribution
        sns.histplot(data=nunique_apps_per_uid,x='application_hash', bins = 10)

    def unique_transactions(self):
        """
        """
        nunique_ips_per_uid = self.data.groupby(by='uid', dropna=False, as_index=False).agg({'transaction_hash':'nunique'}).sort_values(by=['transaction_hash'])
        transaction_payment_rel = self.data.assign(transaction_hash=self.data['transaction_hash'].notnull().astype(int)).groupby(by=['transaction_hash', 'transaction_payment_method'], as_index=False, dropna=False).agg({'transaction_amount':'sum'})
        assert transaction_payment_rel['transaction_hash'].max() <= 300
        assert transaction_payment_rel['transaction_hash'].min() == 1
        assert not self.data['transaction_hash'].isnull().any()
        assert transaction_payment_rel.loc[transaction_payment_rel['transaction_payment_method'] == "Card", "transaction_amount"].iloc[0] > 0
        assert transaction_payment_rel.loc[transaction_payment_rel['transaction_payment_method'] == "Points", "transaction_amount"].iloc[0] > 0
        assert transaction_payment_rel.loc[transaction_payment_rel['transaction_payment_method'] == "Wallet", "transaction_amount"].iloc[0] > 0
        assert transaction_payment_rel.loc[transaction_payment_rel['transaction_payment_method'].isnull(), "transaction_amount"].iloc[0] == 0
        # plot distribution
        sns.histplot(data=nunique_ips_per_uid,x='transaction_hash', bins=10)
        logging.info(transaction_payment_rel.to_markdown())