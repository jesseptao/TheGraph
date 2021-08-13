from .parts.indexer_behaviors import (cumulative_deposited_stake, indexer_actions)
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

from .parts.delegator_behaviors_bookkeeping import (store_pool_delegated_stake,
                                                    store_shares)


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
            'cumulative_deposited_stake': cumulative_deposited_stake

        },
    },
    {
        'label': 'Revenue Process',
        'policies': {
            'revenue_amt': revenue_amt, # indexing and query rewards 
        },
        'variables': {
            'GRT': mint_GRT,
            'delegators': distribute_revenue_to_indexer,
            'pool_delegated_stake': distribute_revenue_to_pool,   
            'indexing_revenue': store_indexing_revenue,
            'query_revenue': store_query_revenue, 
            'cumulative_non_indexer_revenue': cumulative_non_indexer_revenue,
        },
    },
    {
        'label': 'Delegate',
        'policies': {
            'delegate_actions': delegate_actions,
        },
        'variables': {
            'delegators': delegate,
            'GRT': account_for_tax,
        },
    },
    {
        'label': 'Undelegate',
        'policies': {
            'undelegate_actions': undelegate_actions
        },
        'variables': {
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
            'pool_delegated_stake': store_pool_delegated_stake,
            'shares': store_shares,
        },
    },
]

