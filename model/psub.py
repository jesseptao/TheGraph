from .parts.indexer_behaviors import (cumulative_deposited_stake, get_delegation_parameter_events,
                                      get_stake_deposited_events, store_delegation_parameters)
                                      
from .parts.delegator_behaviors import (delegate, undelegate, withdraw,
                                        delegate_actions,
                                        undelegate_actions,
                                        withdraw_actions)

from .parts.revenue import (revenue_amt, distribute_revenue_to_indexer, 
                            mint_GRT, distribute_revenue_to_pool,
                            store_indexing_revenue, store_query_revenue,
                            cumulative_non_indexer_revenue)

psubs = [
    {
        'label': 'Initialization',
        'policies': {
        },
        'variables': {
        },
    },
    {
        'label': 'stakeDepositeds',
        'policies': {
            'stake_deposited_events': get_stake_deposited_events
        },
        'variables': {
            'indexers': cumulative_deposited_stake
        },
    },
    {
        'label': 'delegationParametersUpdateds',
        'policies': {
            'delegation_parameters_updated_events': get_delegation_parameter_events
        },
        'variables': {
            'indexers': store_delegation_parameters,
        },
    },    
    {
        'label': 'Revenue Process - Mint',
        'policies': {
            'revenue_amt': revenue_amt, # indexing and query rewards 
        },
        'variables': {
            'indexers': mint_GRT,
        },
    },
    {
        'label': 'Revenue Process - Revenue to Pool',
        'policies': {
            'revenue_amt': revenue_amt, # indexing and query rewards 
        },
        'variables': {
            'indexers': distribute_revenue_to_pool,   
        },
    },
    {
        'label': 'Revenue Process - Indexing Revenue',
        'policies': {
            'revenue_amt': revenue_amt, # indexing and query rewards 
        },
        'variables': {
            'indexers': store_indexing_revenue,
        },
    },
    {
        'label': 'Revenue Process - Query Revenue',
        'policies': {
            'revenue_amt': revenue_amt, # indexing and query rewards 
        },
        'variables': {
            'indexers': store_query_revenue, 
        },
    },
    {
        'label': 'Revenue Process - Non-Indexer Revenue',
        'policies': {
            'revenue_amt': revenue_amt, # indexing and query rewards 
        },
        'variables': {
            'indexers': cumulative_non_indexer_revenue,
        },
    },
    {
        'label': 'Revenue Process - Indexer Revenue',
        'policies': {
            'revenue_amt': revenue_amt, # indexing and query rewards 
        },
        'variables': {
            'indexers': distribute_revenue_to_indexer,
        },
    },                    
    {
        'label': 'Delegate',
        'policies': {
            'delegate_actions': delegate_actions,
        },
        'variables': {
            'indexers': delegate,
        },
    },
    {
        'label': 'Undelegate',
        'policies': {
            'undelegate_actions': undelegate_actions
        },
        'variables': {
            # 'pool_delegated_stake': subtract_undelegated_stake_from_pool,            
            'indexers': undelegate,
        },
    },    
    {
        'label': 'Withdraw',
        'policies': {
            'withdraw_actions': withdraw_actions
        },
        'variables': {
            'indexers': withdraw,
        },
    },        
]

