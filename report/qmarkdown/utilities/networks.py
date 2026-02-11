import pandas as pd
import networkx as nx

def gen_base_network_data(entity_networks, user_cols=['userid_x','userid_y']):
    """
    """
    # create a base data of users from all entity networks
    base_data = pd.concat(objs=[df[user_cols] for df in entity_networks], ignore_index=True, axis=0).drop_duplicates().reset_index(drop=True)
    # generate full base data by joining on all entity networks
    for entity_network in entity_networks:
        base_data = pd.merge(left=base_data, right=entity_network, on=user_cols, how='left')
    return base_data

def gen_entity_network_data(data, entity, userid = 'userid', trans_week = 'transaction_week'):
    """
    """
    # extract out the unique userids and device hashes
    user_entity_data = data[[userid, entity, trans_week]].dropna().drop_duplicates()
    # inner join users to users based on shared device hash
    user_entity_network_data = pd.merge(left = user_entity_data, right = user_entity_data, on = [entity, trans_week], how = 'inner')
    # drop rows where userid_x = userid_y
    user_entity_network_data = user_entity_network_data.loc[user_entity_network_data[f'{userid}_x'] != user_entity_network_data[f'{userid}_y'], :]
    # set col order
    col_order = [f'{userid}_x', f'{userid}_y', entity, trans_week]
    user_entity_network_data = user_entity_network_data[col_order]
    return user_entity_data, user_entity_network_data

def gen_comp_data(network_data, entity_data, edge_attr):
    """
    """
    # apply graphs for each week
    trans_week_graphs = network_data.groupby(by='transaction_week').apply(lambda group: nx.from_pandas_edgelist(df = group, source = 'userid_x', target = 'userid_y', edge_attr = [edge_attr])).rename('G').reset_index()
    # extract connected components for each week
    trans_week_comps = trans_week_graphs.apply(lambda series: pd.DataFrame([{'transaction_week':series['transaction_week'], 'compid':i, 'userid':cc} for i, cc in enumerate(nx.connected_components(series['G']))]).explode('userid').reset_index(drop = True), axis=1).to_list()
    trans_week_comps = pd.concat(trans_week_comps, axis=0)
    # calculate compid sizes across each week
    trans_week_comps_size = trans_week_comps.groupby(by = ['transaction_week', 'compid'], as_index = False).agg({'userid':'nunique'}).rename(columns={'userid':'compsize'})
    # generate the component data
    comp_data = pd.merge(left = entity_data, right = trans_week_comps, left_on = ['transaction_week', 'userid'], right_on = ['transaction_week', 'userid'], how = 'inner')
    comp_data = pd.merge(left = comp_data, right = trans_week_comps_size, on = ['transaction_week', 'compid'], how = 'inner')
    # order by comp size
    comp_data = comp_data.sort_values(by = ['transaction_week', 'compid', 'userid', edge_attr]).reset_index(drop=True)
    # normalise data with respect to edge attribute
    comp_data = comp_data.rename(columns={edge_attr:'idhashes'})
    comp_data['type'] = edge_attr
    return comp_data