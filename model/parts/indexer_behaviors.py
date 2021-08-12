from . import utils


""" this just gets all of the events at this timestep into policy variables """
def indexer_actions(params, step, sL, s):
    # who delegates, 
    # how many tokens.
    timestep = s['timestep']
    stake_deposited_events = params['stake_deposited_events'].get(timestep)
    return {'stake_deposited_events': stake_deposited_events}

def deposit_stake(params, step, sL, s, inputs):
    stake_deposited_events = inputs['stake_deposited_events'] if inputs['stake_deposited_events'] is not None else []    
    pool_delegated_stake = s['pool_delegated_stake']
    if stake_deposited_events:
        print(f"""ACTION: DEPOSIT STAKE (before)--
                {pool_delegated_stake=}""")
        pool_delegated_stake = utils.calculated_pool_delegated_stake(s)
        print(f"""ACTION: DEPOSIT STAKE (after)--
                {pool_delegated_stake=}""")

    key = 'pool_delegated_stake'
    value = pool_delegated_stake
    return key, value

def cumulative_deposited_stake(params, step, sL, s, inputs):    
    cumulative_deposited_stake = s['cumulative_deposited_stake']
    stake_deposited_events = inputs['stake_deposited_events'] if inputs['stake_deposited_events'] is not None else []    
    
    total_stake_deposited_this_timestep = utils.total_stake_deposited(stake_deposited_events)    
    cumulative_deposited_stake += total_stake_deposited_this_timestep

    key = 'cumulative_deposited_stake'
    value = cumulative_deposited_stake
    return key, value

def add_shares_to_indexer(params, step, sL, s, inputs):
    stake_deposited_events = inputs['stake_deposited_events'] if inputs['stake_deposited_events'] is not None else []    
    pool_delegated_stake = s['pool_delegated_stake']
    shares = s['shares']
    delegators = s['delegators']
    
    total_stake_deposited_this_timestep = utils.total_stake_deposited(stake_deposited_events)
    new_shares = total_stake_deposited_this_timestep if pool_delegated_stake == 0 else total_stake_deposited_this_timestep * shares / pool_delegated_stake
    
    delegators['indexer'].shares += new_shares    

    key = 'delegators'
    value = delegators
    return key, value

def add_shares_to_pool(params, step, sL, s, inputs):
    stake_deposited_events = inputs['stake_deposited_events'] if inputs['stake_deposited_events'] is not None else []    
    pool_delegated_stake = s['pool_delegated_stake']
    shares = s['shares']
    
    total_stake_deposited_this_timestep = utils.total_stake_deposited(stake_deposited_events)
    new_shares = total_stake_deposited_this_timestep if pool_delegated_stake == 0 else total_stake_deposited_this_timestep * shares / pool_delegated_stake
    shares += new_shares

    key = 'shares'
    value = shares
    return key, value

