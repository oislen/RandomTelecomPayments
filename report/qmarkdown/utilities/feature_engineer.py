import pandas as pd

def feature_engineer(data, ids, groups, target, func):
    """
    """
    # aggregate across the ids and group, applying the function to the target
    data_agg = data.copy().groupby(by=ids+groups, as_index=False).agg({target:func})
    # pivot the target results across each group
    data_pivot = pd.pivot_table(data=data_agg, index=ids, values=target, columns=groups)
    # rename and format the columns
    data_pivot.columns = data_pivot.columns.str.split(':').str[0] + f'_{func}'
    data_pivot = data_pivot.reset_index()
    data_pivot.columns.name = None
    return data_pivot

def merge_features(feat_objs):
    """
    """
    feat_data = pd.DataFrame(columns=['userid', 'transaction_week'])
    # join objects
    for feat_obj in feat_objs:
        feat_data = pd.merge(left=feat_data, right=feat_obj, how='outer', on=['userid', 'transaction_week'])
    # fill for missing values
    feat_data = feat_data.fillna(0)
    return feat_data