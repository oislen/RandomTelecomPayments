from sklearn.ensemble import IsolationForest
import pickle

def gen_anomaly_score(group, model_fpath):
    """
    """
    # initiate and load isolation forest model
    model = IsolationForestsModel()
    model = model.read(model_fpath)
    # split data
    id_cols = ['userid', 'transaction_week']
    X_cols = ['E901_size', 'E901_sum', 'E902_size', 'E902_sum', 'n_comps', 'total_comp_size']
    train_group = group[X_cols]
    score_group = group[id_cols+X_cols]
    # train isolation forests and score data
    model = model.fit(train_group)
    score_group['score'] = model.decision_function(train_group)
    # write model to disk
    model.write(model_fpath)
    return score_group

def gen_cumulative_anomaly_score(group):
    """
    """
    group_sort = group.sort_values('transaction_week')
    group_sort['anomaly_score'] = group_sort['score'].cumsum()
    return group_sort

class IsolationForestsModel():
    def __init__(self, n_estimators=20, random_state=None, warm_start=False, n_jobs=None):
        self.model = IsolationForest(n_estimators=n_estimators, random_state=random_state, warm_start=warm_start)
        self.n_estimators = n_estimators
    def fit(self, X):
        if self.model.warm_start:
            self.model.n_estimators += self.n_estimators
        self.model = self.model.fit(X)
        return self
    def decision_function(self, X):
        return self.model.decision_function(X)
    def write(self, model_fpath):
        with open(model_fpath,'wb') as f:
            pickle.dump(self,f)
    def read(self, model_fpath):
        with open(model_fpath, 'rb') as f:
            return pickle.load(f)
