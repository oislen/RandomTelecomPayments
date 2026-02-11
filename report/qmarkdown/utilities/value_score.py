def week_pct_score(group, score_cols = ['successful_size','successful_sum']):
    """
    """
    # percentile rank the score columns
    group_score = group[score_cols].rank(method='average', ascending=True, pct=True, axis=0)
    group_score.columns = group_score.columns + '_pct'
    # join score results back to groups
    group_results = group.join(group_score)
    return group_results

def gen_weekly_user_scores(group):
    """
    """
    # define score and id columns
    id_cols = ['userid', 'transaction_week']
    score_cols=['successful_size_pct', 'successful_sum_pct']
    value_cols = ['customer_value_score']
    # calcualte the customer value score
    group['customer_value_score'] = group[score_cols].mean(axis=1)
    return group[id_cols+score_cols+value_cols]

def apply_cumsum(group):
    """
    """
    # define score and id columns
    id_cols = ['userid', 'transaction_week']
    score_cols=['successful_size_pct', 'successful_sum_pct']
    value_cols = ['customer_value_score', 'customer_value_score_cumsum']
    # sort and apply cumsum
    group_sort = group.sort_values(by='transaction_week')
    group_sort['customer_value_score_cumsum'] = group_sort['customer_value_score'].cumsum()
    return group_sort[id_cols+score_cols+value_cols]