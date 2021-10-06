from delegator import Delegator

class Indexer():
    def __init__(self, id = '', pool_delegated_stake = 0, shares = 0, pool_locked_stake = 0,
                indexer_revenue = 0, GRT = 0, cumulative_indexing_revenue = 0, 
                cumulative_query_revenue = 0, cumulative_non_indexer_revenue = 0,
                cumulative_deposited_stake = 0, initial_stake_deposited = False):
        self.id = id
        self.pool_delegated_stake = pool_delegated_stake
        self.shares = shares
        self.delegators = []
        self.pool_locked_stake = pool_locked_stake
        self.indexer_revenue = indexer_revenue
        self.GRT = GRT
        self.cumulative_indexing_revenue = cumulative_indexing_revenue
        self.cumulative_query_revenue = cumulative_query_revenue
        self.cumulative_non_indexer_revenue = cumulative_non_indexer_revenue
        self.cumulative_deposited_stake = cumulative_deposited_stake
        self.initial_stake_deposited = initial_stake_deposited

    def add_delegator(self, Delegator, indexer_id):
        self.delegators.append(Delegator(indexer_id))