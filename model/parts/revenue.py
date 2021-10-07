from model.parts.delegator_behaviors import process_delegation_event

""" indexing fees increase shares
query fees do not increase shares """

def revenue_amt(params, step, sL, prev_state):
    timestep = prev_state['timestep']
    
    indexer_id = None
    rewards_assigned_events = params['rewards_assigned_events'].get(timestep)
    indexing_fee_amt = 0
    if rewards_assigned_events is not None:
        indexing_fee_amt = sum([e['amount'] for e in rewards_assigned_events])
        indexer_id = rewards_assigned_events[0]['indexer']
    
    query_fee_events = params['query_fee_events'].get(timestep)
    # print(query_fee_events)
    if query_fee_events is None:
        query_fee_amt = 0
    else:
        query_fee_amt = sum([e['tokens'] for e in query_fee_events])
        indexer_id = query_fee_events[0]['indexer']
    

    return {'indexer_id': indexer_id,
            'indexing_fee_amt': indexing_fee_amt,
            'query_fee_amt': query_fee_amt}

def mint_GRT(params, step, sL, s, inputs):
    key = 'indexers'
    if inputs['indexer_id']:
        # GRT Increases from indexing and not querying.
        s['indexers'][inputs['indexer_id']].GRT += inputs['indexing_fee_amt']
    value = s['indexers']
    return key, value

def distribute_revenue_to_indexer(params, step, sL, s, inputs):
    """ Calculate and distribute query and indexing rewards to indexer """
    indexer_id = inputs['indexer_id']
    indexing_revenue = inputs['indexing_fee_amt']
    query_revenue = inputs['query_fee_amt']   
    
    # step 1: collect revenue from the state
    if indexing_revenue != 0 or query_revenue != 0:
        indexer = s['indexers'][indexer_id]
        query_fee_cut = indexer.query_fee_cut
        indexing_revenue_cut = indexer.indexer_revenue_cut

        print(f'ACTION: DISTRIBUTE REVENUE TO INDEXER')
        
        # take indexer cut here, the rest goes to indexer pool
        revenue_to_indexer = (indexing_revenue + 
                                query_revenue -
                                calculate_revenue_to_indexer_pool(indexing_revenue, query_revenue, query_fee_cut, indexing_revenue_cut))
        print(f'''  {s["timestep"]=}, {indexing_revenue=}, {query_revenue=}, {indexer.holdings=} (before)''')
        indexer.holdings += revenue_to_indexer
        print(f'''  {s["timestep"]=}, {indexing_revenue=}, {query_revenue=}, {indexer.holdings=} (after)''')
        ## NOTE: Non-indexer delegators get nothing.  Their rewards are added back to the pool and no new shares are issues.
        
    key = 'indexers'
    value = s['indexers']
    return key, value

def distribute_revenue_to_pool(params, step, sL, s, inputs):
    """ Calculate and distribute query and indexing rewards to indexer pool """
    indexer_id = inputs['indexer_id']
    indexing_revenue = inputs['indexing_fee_amt']
    query_revenue = inputs['query_fee_amt']
    
    indexers = s['indexers']
    if indexing_revenue != 0 or query_revenue != 0:
        print(f'ACTION: DISTRIBUTE REVENUE TO POOL')

        indexer = s['indexers'][indexer_id]
        pool_delegated_stake = indexer.pool_delegated_stake
        query_fee_cut = indexer.query_fee_cut
        indexing_revenue_cut = indexer.indexer_revenue_cut

        # 5.2 D+ = D + Ri * (1 - phi)
        non_indexer_revenue = calculate_revenue_to_indexer_pool(indexing_revenue, query_revenue, query_fee_cut, indexing_revenue_cut)

        print(f'  {indexing_revenue=}, {query_revenue=}, {pool_delegated_stake=} (before)')
        pool_delegated_stake += non_indexer_revenue
        print(f'  {indexing_revenue=}, {query_revenue=}, {pool_delegated_stake=} (after)')
    key = 'indexers'
    return key, indexers

def cumulative_non_indexer_revenue(params, step, sL, s, inputs):
    indexing_revenue = inputs['indexing_fee_amt']
    query_revenue = inputs['query_fee_amt']
    if indexing_revenue != 0 or query_revenue != 0:
        indexer = s['indexers'][inputs['indexer_id']]
        query_fee_cut = indexer.query_fee_cut
        indexing_revenue_cut = indexer.indexer_revenue_cut
        # print(f'  {indexing_revenue=}, {query_revenue=}, {cumulative_non_indexer_revenue=} (before)')
        indexer.cumulative_non_indexer_revenue += calculate_revenue_to_indexer_pool(indexing_revenue, query_revenue, query_fee_cut, indexing_revenue_cut)
        # print(f'  {indexing_revenue=}, {query_revenue=}, {cumulative_non_indexer_revenue=} (after)')
        
    key = 'indexers'
    return key, s['indexers']


def store_indexing_revenue(params, step, sL, s, inputs):
    key = 'cumulative_indexing_revenue'
    if inputs['indexer_id']:
        indexer = s['indexers'][inputs['indexer_id']]
        indexer.cumulative_indexing_revenue += inputs['indexing_fee_amt']

    return key, s['indexers']

def store_query_revenue(params, step, sL, s, inputs):
    key = 'cumulative_query_revenue'
    if inputs['indexer_id']:
        indexer = s['indexers'][inputs['indexer_id']]
        indexer.cumulative_query_revenue += inputs['query_fee_amt']
    return key, s['indexers']

# helper function
def calculate_revenue_to_indexer_pool(indexing_revenue, query_revenue, query_fee_cut, indexing_revenue_cut):
    """ Calculate and distribute query and indexing rewards to indexer pool """
    # D+ = D + Ri * (1 - alpha)
    # Indexing rewards - indexer cut.    
    non_indexer_revenue_cut = (1 - indexing_revenue_cut) * indexing_revenue    

    # D+ = D + Rq * (1 - phi)
    # Query rewards - indexer cut.   
    # TODO: is this right?!    
    non_indexer_query_fee_cut = 0
    # non_indexer_query_fee_cut = (1 - query_fee_cut) * query_revenue

    non_indexer_revenue_net = non_indexer_revenue_cut + non_indexer_query_fee_cut   
    return non_indexer_revenue_net    

