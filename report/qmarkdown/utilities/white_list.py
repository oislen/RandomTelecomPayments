def gen_white_list(group):
    # create the high value user identifier
    sub_cols = ['userid', 'transaction_week', 'Successful_size',  'Successful_sum', 'E901_size', 'E901_sum', 'customer_value_score_cum_sum']
    high_value_data = group.loc[:, sub_cols].copy()
    high_value_data['customer_value_score_cum_sum_pct'] = high_value_data['customer_value_score_cum_sum'].rank(method='average', ascending=True, pct=True, axis=0)
    high_value_data['high_value_user'] = (high_value_data['customer_value_score_cum_sum_pct'] >= 0.9).astype(int)
    return high_value_data