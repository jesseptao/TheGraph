from . import utils


""" this just gets all of the events at this timestep into policy variables """
def indexer_actions(params, step, sL, s):
    # who delegates, 
    # how many tokens.
    timestep = s['timestep']
    stake_deposited_events = params['stake_deposited_events'].get(timestep)
    return {'stake_deposited_events': stake_deposited_events}

# def deposit_stake(params, step, sL, s, inputs):
#     stake_deposited_events = inputs['stake_deposited_events'] if inputs['stake_deposited_events'] is not None else []    
#     pool_delegated_stake = s['pool_delegated_stake']
#     if stake_deposited_events:
#         print(f"""ACTION: DEPOSIT STAKE (before)--
#                 {pool_delegated_stake=}""")
#         # have to add in stake deposited here, but we save it as cumulative_deposited_stake for future calculations
#         total_stake_deposited_this_timestep = utils.total_stake_deposited(stake_deposited_events)  
#         pool_delegated_stake = utils.calculated_pool_delegated_stake(s) + total_stake_deposited_this_timestep
#         print(f"""ACTION: DEPOSIT STAKE (after)--
#                 {pool_delegated_stake=}""")

#     key = 'pool_delegated_stake'
#     value = pool_delegated_stake
#     return key, value

def cumulative_deposited_stake(params, step, sL, s, inputs):    
    cumulative_deposited_stake = s['cumulative_deposited_stake']
    stake_deposited_events = inputs['stake_deposited_events'] if inputs['stake_deposited_events'] is not None else []    
    total_stake_deposited_this_timestep = utils.total_stake_deposited(stake_deposited_events)    
    
    if s['initial_stake_deposited']:
        # initial stake has already been deposited, so TODO: what happens here?
        pass
    else:        
        cumulative_deposited_stake += total_stake_deposited_this_timestep

    key = 'cumulative_deposited_stake'
    value = cumulative_deposited_stake
    return key, value

def is_initial_stake_deposited(params, step, SL, s, inputs):
    stake_deposited_events = inputs['stake_deposited_events'] if inputs['stake_deposited_events'] is not None else []    
    
    initial_stake_deposited = s['initial_stake_deposited']
    
    if stake_deposited_events:
        initial_stake_deposited = True
    
    key = 'initial_stake_deposited'
    value = initial_stake_deposited
    return key, value

