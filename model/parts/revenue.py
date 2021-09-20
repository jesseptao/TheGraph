from model.parts.delegator_behaviors import process_delegation_event

""" indexing fees increase shares
query fees do not increase shares """

def revenue_amt(params, step, sL, prev_state):
    timestep = prev_state['timestep']
    print(f'{timestep=} beginning...')
    
    rewards_assigned_events = params['rewards_assigned_events'].get(timestep)
    indexing_fee_amt = 0
    if rewards_assigned_events is not None:
        indexing_fee_amt = sum([e['amount'] for e in rewards_assigned_events])
    
    query_fee_events = params['query_fee_events'].get(timestep)
    # print(query_fee_events)
    if query_fee_events is None:
        query_fee_amt = 0
    else:
        query_fee_amt = sum([e['tokens'] for e in query_fee_events])

    return {'indexing_fee_amt': indexing_fee_amt,
            'query_fee_amt': query_fee_amt}

def mint_GRT(params, step, sL, prev_state, inputs):
    key = 'GRT'
    GRT = prev_state['GRT']
    
    # GRT Increases from indexing and not querying.
    delta = inputs['indexing_fee_amt']
    
    return key, GRT + delta

def distribute_revenue_to_indexer(params, step, sL, s, inputs):
    """ Calculate and distribute query and indexing rewards to indexer """
    indexing_revenue = inputs['indexing_fee_amt']
    query_revenue = inputs['query_fee_amt']   
    
    # step 1: collect revenue from the state
    if indexing_revenue != 0 or query_revenue != 0:
        query_fee_cut = s['query_fee_cut']
        indexing_revenue_cut = s['indexer_revenue_cut']

        print(f'ACTION: DISTRIBUTE REVENUE TO INDEXER')
        indexer = s['delegators']['indexer']
        
        # take indexer cut here, the rest goes to indexer pool
        revenue_to_indexer = (indexing_revenue + 
                                query_revenue -
                                calculate_revenue_to_indexer_pool(indexing_revenue, query_revenue, query_fee_cut, indexing_revenue_cut))
        print(f'''  {s["timestep"]=}, {indexing_revenue=}, {query_revenue=}, {indexer.holdings=} (before)''')
        indexer.holdings += revenue_to_indexer
        print(f'''  {s["timestep"]=}, {indexing_revenue=}, {query_revenue=}, {indexer.holdings=} (after)''')
        ## NOTE: Non-indexer delegators get nothing.  Their rewards are added back to the pool and no new shares are issues.
        
    key = 'delegators'
    value = s['delegators']
    return key, value

def distribute_revenue_to_pool(params, step, sL, s, inputs):
    """ Calculate and distribute query and indexing rewards to indexer pool """

    indexing_revenue = inputs['indexing_fee_amt']
    query_revenue = inputs['query_fee_amt']
    pool_delegated_stake = s['pool_delegated_stake']

    if indexing_revenue != 0 or query_revenue != 0:
        print(f'ACTION: DISTRIBUTE REVENUE TO POOL')

        
        query_fee_cut = s['query_fee_cut']
        indexing_revenue_cut = s['indexer_revenue_cut']

        # 5.2 D+ = D + Ri * (1 - phi)
        non_indexer_revenue = calculate_revenue_to_indexer_pool(indexing_revenue, query_revenue, query_fee_cut, indexing_revenue_cut)

        print(f'  {indexing_revenue=}, {query_revenue=}, {pool_delegated_stake=} (before)')
        pool_delegated_stake += non_indexer_revenue
        print(f'  {indexing_revenue=}, {query_revenue=}, {pool_delegated_stake=} (after)')
    key = 'pool_delegated_stake'
    return key, pool_delegated_stake

def cumulative_non_indexer_revenue(params, step, sL, s, inputs):
    indexing_revenue = inputs['indexing_fee_amt']
    query_revenue = inputs['query_fee_amt']
    cumulative_non_indexer_revenue = s['cumulative_non_indexer_revenue']

    if indexing_revenue != 0 or query_revenue != 0:
        query_fee_cut = s['query_fee_cut']
        indexing_revenue_cut = s['indexer_revenue_cut']
        # print(f'  {indexing_revenue=}, {query_revenue=}, {cumulative_non_indexer_revenue=} (before)')
        cumulative_non_indexer_revenue += calculate_revenue_to_indexer_pool(indexing_revenue, query_revenue, query_fee_cut, indexing_revenue_cut)
        # print(f'  {indexing_revenue=}, {query_revenue=}, {cumulative_non_indexer_revenue=} (after)')
    key = 'cumulative_non_indexer_revenue'
    return key, cumulative_non_indexer_revenue

def store_indexing_revenue(params, step, sL, s, inputs):
    key = 'cumulative_indexing_revenue'
    value = s['cumulative_indexing_revenue'] + inputs['indexing_fee_amt']
    return key, value

def store_query_revenue(params, step, sL, s, inputs):
    key = 'cumulative_query_revenue'
    value = s['cumulative_query_revenue'] + inputs['query_fee_amt']
    return key, value

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

