def week_pct_score(group, score_cols = ['Successful_size','Successful_sum']):
    """
    """
    # percentile rank the score columns
    group_score = group[score_cols].rank(method='average', ascending=True, pct=True, axis=0)
    group_score.columns = group_score.columns + '_pct'
    return group_score

def gen_weekly_user_scores(group, score_cols=['Successful_size_pct', 'Successful_sum_pct']):
    """
    """
    # calculate the customer value score
    customer_value_score = group[score_cols].mean(axis=1).rename('customer_value_score')
    return customer_value_score

def apply_cum_sum(group, score_col='customer_value_score'):
    """
    """
    # sort and apply cumsum
    group_sort = group.sort_values(by='transaction_week')
    customer_value_score_cum_sum = group_sort[score_col].cumsum().rename('customer_value_score_cum_sum')
    return customer_value_score_cum_sum