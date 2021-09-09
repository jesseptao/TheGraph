from . import utils

def store_shares(params, step, sL, s, inputs):
    key = 'shares'
    # add shares of all delegators
    shares = sum([d.shares for d in s['delegators'].values()])    
    # print(f'{shares=}')
    return key, shares


# def store_pool_delegated_stake(params, step, sL, s, inputs):
#     key = 'pool_delegated_stake'
#     pool_delegated_stake = utils.calculated_pool_delegated_stake(s)

#     return key, pool_delegated_stake

def add_delegated_stake_to_pool(params, step, sL, s, inputs):
    key = 'pool_delegated_stake'
    delegation_events = inputs['delegation_events'] if inputs['delegation_events'] is not None else []    
    pool_delegated_stake = s['pool_delegated_stake']
    
    for delegation in delegation_events:
        pool_delegated_stake += delegation['tokens']   

    return key, pool_delegated_stake    

def subtract_undelegated_stake_from_pool(params, step, sL, s, inputs):
    key = 'pool_delegated_stake'
    undelegation_events = inputs['undelegation_events'] if inputs['undelegation_events'] is not None else []    
    pool_delegated_stake = s['pool_delegated_stake']

    # shares needs to be kept updated
    shares = sum([d.shares for d in s['delegators'].values()])
    for undelegation in undelegation_events:
        undelegation_shares_quantity = undelegation['shares']

        if undelegation_shares_quantity < 0:
            # require a non-zero amount of shares
            continue

        # if undelegation_shares_quantity > delegator.shares:
        #     # require delegator to have enough shares in the pool to undelegate
        #     undelegation_shares_quantity = delegator.shares

        undelegated_tokens = undelegation_shares_quantity * pool_delegated_stake / shares
        pool_delegated_stake -= undelegated_tokens

    return key, pool_delegated_stake    