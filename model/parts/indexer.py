from delegator import Delegator

class Indexer(object):
    def __init__(self, id = '', pool_delegated_stake = 0, shares = 0, delegators = {}):
        self.id = id
        self.pool_delegated_stake = pool_delegated_stake
        self.shares = shares
        self.delegators = delegators

        