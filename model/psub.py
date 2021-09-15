from .parts.indexer_behaviors import (cumulative_deposited_stake, indexer_actions,
                                      is_initial_stake_deposited)
                                      
# , deposit_stake, add_shares_to_indexer, add_shares_to_pool)

from .parts.delegator_behaviors import (delegate, undelegate, withdraw,
                                        delegate_actions,
                                        undelegate_actions,
                                        withdraw_actions,
                                        account_for_tax)

from .parts.revenue import (revenue_amt, distribute_revenue_to_indexer, 
                            mint_GRT, distribute_revenue_to_pool,
                            store_indexing_revenue, store_query_revenue,
                            cumulative_non_indexer_revenue)

# from .parts.private_price import compute_and_store_private_prices

from .parts.delegator_behaviors_bookkeeping import (store_shares, add_delegated_stake_to_pool,
                                                    subtract_undelegated_stake_from_pool)


psubs = [
    {
        'label': 'Stake Deposit',
        'policies': {
            'indexer_actions': indexer_actions
        },
        'variables': {
            # 'pool_delegated_stake': deposit_stake,
            # 'shares': add_shares_to_pool,
            # 'delegators': add_shares_to_indexer,
            'cumulative_deposited_stake': cumulative_deposited_stake,
            'initial_stake_deposited': is_initial_stake_deposited
        },
    },
    {
        'label': 'Revenue Process',
        'policies': {
            'revenue_amt': revenue_amt, # indexing and query rewards 
        },
        'variables': {
            'GRT': mint_GRT,
            'pool_delegated_stake': distribute_revenue_to_pool,   
            'cumulative_indexing_revenue': store_indexing_revenue,
            'cumulative_query_revenue': store_query_revenue, 
            'cumulative_non_indexer_revenue': cumulative_non_indexer_revenue,
            'delegators': distribute_revenue_to_indexer,
        },
    },
    {
        'label': 'Delegate',
        'policies': {
            'delegate_actions': delegate_actions,
        },
        'variables': {
            'pool_delegated_stake': add_delegated_stake_to_pool,
            'GRT': account_for_tax,
            'delegators': delegate,
        },
    },
    {
        'label': 'Undelegate',
        'policies': {
            'undelegate_actions': undelegate_actions
        },
        'variables': {
            'pool_delegated_stake': subtract_undelegated_stake_from_pool,            
            'delegators': undelegate,
        },
    },    
    {
        'label': 'Withdraw',
        'policies': {
            'withdraw_actions': withdraw_actions
        },
        'variables': {
            'delegators': withdraw,
        },
    },        
    {
        'label': 'Delegator Behaviors Bookkeeping',
        'policies': {
            'indexer_actions': indexer_actions
        },
        'variables': {
            # 'pool_delegated_stake': store_pool_delegated_stake,
            'shares': store_shares,
        },
    },
]

