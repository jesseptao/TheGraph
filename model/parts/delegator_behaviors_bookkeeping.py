def store_shares(params, step, sL, s, inputs):
    key = 'shares'
    # add shares of all delegators
    shares = sum([d.shares for d in s['delegators'].values()])    
    # print(f'{shares=}')
    return key, shares


def store_pool_delegated_stake(params, step, sL, s, inputs):
    key = 'pool_delegated_stake'
    # print(f'{s["cumulative_non_indexer_revenue"]=}')
    pool_delegated_stake = sum([d.delegated_tokens for d in s['delegators'].values()]) + s['cumulative_non_indexer_revenue']
    # print(f'{pool_delegated_stake=}, {s["cumulative_non_indexer_revenue"]=}')
    return key, pool_delegated_stake

