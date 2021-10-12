from . import utils
from .indexer import Indexer


""" this just gets all of the events at this timestep into policy variables """
def indexer_actions(params, step, sL, s):
    # who delegates, 
    # how many tokens.
    timestep = s['timestep']
    stake_deposited_events = params['stake_deposited_events'].get(timestep)
    delegation_parameter_events = params['delegation_parameter_events'].get(timestep)
    # print(f'DELEGATION PARAMETER EVENTS {delegation_parameter_events}')
    return {'stake_deposited_events': stake_deposited_events,
            'delegation_parameter_events': delegation_parameter_events}

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
    key = 'indexers'
    timestep = s['timestep']
    print(f'{timestep=} beginning...')

    # stake_deposited_events = inputs['stake_deposited_events'] if inputs['stake_deposited_events'] is not None else []    
    event = inputs['stake_deposited_events'][0] if inputs['stake_deposited_events'] is not None else None
    indexers = s['indexers']

    if event:
        indexer_id = event['indexer']
        if indexer_id not in indexers:
            indexers[indexer_id] = Indexer()

        
        indexer = indexers[indexer_id]
        indexer.cumulative_deposited_stake += event['tokens']
        indexer.initial_stake_deposited = True
        print(f'STAKE DEPOSITED: {event["tokens"]}')
    
    value = indexers
    return key, value

def store_query_fee_cut(params, step, SL, s, inputs):
    key = 'indexers'
    indexers = s[key]

    delegation_parameter_events = inputs['delegation_parameter_events'] if inputs['delegation_parameter_events'] is not None else []        
    
    for event in delegation_parameter_events:
        indexer = indexers[event['indexer']]
        print(f'''ACTION: QUERY FEE CUT (before)--
                {indexer.query_fee_cut=}
        ''')        
        indexer.query_fee_cut = event['queryFeeCut']
        print(f'''ACTION: QUERY FEE CUT (after)--
                {indexer.query_fee_cut=}
        ''')
    
    value = indexers
    return key, value
    
def store_indexer_fee_cut(params, step, SL, s, inputs):    
    key = 'indexers'    
    indexers = s[key]
    delegation_parameter_events = inputs['delegation_parameter_events'] if inputs['delegation_parameter_events'] is not None else []    
    
    for event in delegation_parameter_events:
        indexer = indexers[event['indexer']]
        
        print(f'''ACTION: INDEXING REWARD CUT (before)--
                {indexer.indexer_revenue_cut=}
        ''')        
        indexer.indexer_revenue_cut = event['indexingRewardCut']
        print(f'''ACTION: INDEXING REWARD CUT (after)--
                {indexer.indexer_revenue_cut=}
        ''')

    value = indexers
    return key, value
