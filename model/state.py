# from model.parts import delegator
from .parts.delegator import Delegator
from .parts.indexer import Indexer
from decimal import Decimal

initial_shares = 0
initial_stake = Decimal(0)
# id_indexer = "indexer"

""" System state/state of the delegation pool for multiple indexers. """
genesis_state = {
    # 'indexers': {'0x0000000': Indexer(), '0x000001': Indexer()},
    'indexers': {},
    ## DELEGATION POOL of Indexer State ##
    # A_ind
    #'id_indexer': id_indexer,

    # D
    #'pool_delegated_stake': initial_stake,  # amount of GRT delegated to the indexer
    
    # L
    # 'pool_locked_stake': 0,  # amount of GRT locked in undelegation process.  these are NO LONGER in the delegated pool and also not owned by delegator yet.
    
    # # S
    # 'shares': initial_shares,  # shares--this is only added to when a delegator delegates
    
    # # f: A_del -> A_ind
    # 'delegators': {'indexer': Delegator(id=id_indexer, shares=initial_shares, delegated_tokens=initial_stake)},

    # 'query_fee_cut': Decimal(0.0),
    # 'indexer_revenue_cut': Decimal(0.0),

    # I_r: This is the same as delegators['indexer'].holdings.
    # 'indexer_revenue': 0,

    # # S_i: Same as pool_locked_stake in simplified single-indexer model.
    # # 'indexer_stake': 
    # ## END DELEGATION POOL of Indexer State


    # ## Token State ##
    # # Start at 0, so it is a count of how many have been added/subtracted
    # 'GRT': 0,

    # # R_i
    # 'cumulative_indexing_revenue': 0,

    # # R_q
    # 'cumulative_query_revenue': 0,

    # # needed for bookkeeping step
    # 'cumulative_non_indexer_revenue': 0,
    # 'cumulative_deposited_stake': 0,
    # 'initial_stake_deposited': False,
    ## END Token State    
    
}
