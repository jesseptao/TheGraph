from . import utils

def store_shares(params, step, sL, s, inputs):
    key = 'shares'
    # add shares of all delegators
    shares = sum([d.shares for d in s['delegators'].values()])    
    # print(f'{shares=}')
    return key, shares


def store_pool_delegated_stake(params, step, sL, s, inputs):
    key = 'pool_delegated_stake'
    pool_delegated_stake = utils.calculated_pool_delegated_stake(s)

    return key, pool_delegated_stake

