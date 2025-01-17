


from .parts.add_delegator import instantiate_delegate, should_instantiate_delegate

from .parts.delegator_behaviors import (delegate, undelegate, withdraw,
                                        may_act_this_timestep, delegator_action,
                                        account_for_tax)

from .parts.revenue import (revenue_amt, store_revenue, distribute_revenue, mint_GRT,
                                                    store_indexing_revenue,
                                                    store_query_revenue,
                                                    distribute_indexer_revenue,
                                                    distribute_revenue_to_pool)

# from .parts.private_price import compute_and_store_private_prices

from .parts.delegator_behaviors_bookkeeping import (store_pool_delegated_stake,
                                                    store_shares, increment_epoch)


psubs = [
    {
        'label': 'Revenue Arrival Process',
        'policies': {
            'revenue_amt': revenue_amt  # how much is paid in.
        },
        'variables': {
            'period_revenue': store_revenue,
            'GRT': mint_GRT,
            'indexing_revenue': store_indexing_revenue, 
            'query_revenue': store_query_revenue,         
        },
    },
    {
        'label': 'Distribute Revenue',
        'policies': {
        },
        'variables': {
            'delegators': distribute_revenue,
            'indexer_revenue': distribute_indexer_revenue,
            'pool_delegated_stake': distribute_revenue_to_pool,

        }
    },
    {
        # if there's a vacant spot, flip a coin
        # (heads, they join, tails nobody joins)
        'label': 'Add Delegator',
        'policies': {
            'should_instantiate_delegate': should_instantiate_delegate
            },
        'variables': {
            'delegators': instantiate_delegate,
            },
    },
    {
        'label': 'Delegate',
        'policies': {
            # outputs ordered list of acting delegatorIds this timestep
            'may_act_this_timestep': may_act_this_timestep,
            'delegator_action': delegator_action
        },
        'variables': {
            'delegators': delegate,
            'GRT': account_for_tax,
        },
    },
    {
        'label': 'Undelegate',
        'policies': {
            # outputs ordered list of acting delegatorIds this timestep
            'may_act_this_timestep': may_act_this_timestep,
            'delegator_action': delegator_action
        },
        'variables': {
            'delegators': undelegate,
        },
    },    
    {
        'label': 'Withdraw',
        'policies': {
            # outputs ordered list of acting delegatorIds this timestep
            'may_act_this_timestep': may_act_this_timestep,
            'delegator_action': delegator_action
        },
        'variables': {
            'delegators': withdraw,
        },
    },        
    {
        'label': 'Delegator Behaviors Bookkeeping',
        'policies': {
            # 'account_global_state_from_delegator_states': account_global_state_from_delegator_states
        },
        'variables': {
            'pool_delegated_stake': store_pool_delegated_stake,
            'shares': store_shares,
            'epoch': increment_epoch,
        },
    },
]

