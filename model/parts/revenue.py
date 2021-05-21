
import scipy.stats as stats


def revenue_amt(params, step, sL, prev_state):
    # placeholder for query fee revenue
    revenue_amt = params["expected_revenue"] * stats.expon.rvs()
    # print(f'{revenue_amt=}')
    R_i_rate = params['R_i_rate']
    allocation_days = params['allocation_days']
    timestep = prev_state['timestep']
    if timestep % allocation_days == 0:
        GRT = prev_state['GRT']
        minted_rewards = GRT * R_i_rate * allocation_days/ 365 # annual inflation
    else:
        minted_rewards = 0
    return {'revenue_amt': revenue_amt, 'minted_rewards': minted_rewards}

def mint_GRT(params, step, sL, prev_state, inputs):
    # print('storing revenue')
    key = 'GRT'
    GRT = prev_state['GRT']
    
    delta = inputs['minted_rewards']
    
    return key, GRT + delta

def store_query_revenue(params, step, sL, s, inputs):
    # print('storing revenue')
    key = 'query_revenue'
    # indexer_allocation_rate = params['indexer_allocation_rate']
    query_fees =  inputs['revenue_amt']

    return key, query_fees

def store_indexing_revenue(params, step, sL, s, inputs):
    # print('storing revenue')
    key = 'indexing_revenue'
    indexer_allocation_rate = params['indexer_allocation_rate']
    minted_rewards = inputs['minted_rewards']
    indexer_rewards = minted_rewards * indexer_allocation_rate

    return key, indexer_rewards

def store_revenue(params, step, sL, s, inputs):
    # print('storing revenue')
    key = 'period_revenue'
    indexer_allocation_rate = params['indexer_allocation_rate']
    query_fees =  inputs['revenue_amt']
    minted_rewards = inputs['minted_rewards']
    indexer_rewards = minted_rewards * indexer_allocation_rate

    return key, indexer_rewards + query_fees


def distribute_revenue(params, step, sL, s, inputs):
    revenue = s['period_revenue']
    indexer_revenue_cut = params['indexer_revenue_cut']
    shares = s['shares']

    # step 1: collect revenue from the state
    non_indexer_revenue_cut = ((1-indexer_revenue_cut) * revenue)
    revenue_per_share = non_indexer_revenue_cut / shares

    for id, delegator in s['delegators'].items():
        if id == 0:
            # step 2: get owners share, theta
            delegator.revenue_token_holdings += indexer_revenue_cut * revenue
        
        #  step 3: distribute non-owners share
        # print(f'{delegator.shares=}')
        delegator.revenue_token_holdings += delegator.shares * revenue_per_share
    
    key = 'delegators'
    value = s['delegators']
    return key, value
