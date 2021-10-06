import random
from indexer import Indexer
""" A Delegator is an actor who delegates native tokens to the revenue sharing pool
for shares in the revenue stream. """


class Delegator(Indexer):
    def __init__(self, id, shares=0, holdings=0, discount_rate=.9,
                 minimum_shares=0, delegated_tokens=0):
        # initialize delegator state
        self.id = id

        self.shares = shares

        # Tokens locked in undelegation, l  
        self.undelegated_tokens = 0

        # Freeze time (measure in block time)
        self.locked_until = 0

        # Amount of free/withdrawn token the delegator is holding, h
        self.holdings = holdings

        # used to discount cash flows. 1 / (1 - discount_rate)
        # self.time_factor = 1 / (1 - discount_rate)
        
        # Not allowed to sell below this amount
        self.minimum_shares = minimum_shares

    def __repr__(self):
        return f'{self.id=}, {self.shares=}'

    # member of the sharing pool (True/False)
    def is_member(self):
        return self.shares > 0

    def getWithdrawableDelegatedTokens(self, timestep):
        if timestep > self.locked_until:
            return self.undelegated_tokens
        else:
            return 0

    def withdraw(self, tokens):
        self.holdings += tokens
        self.undelegated_tokens -= tokens
        self.locked_until = 0


    def set_undelegated_tokens(self, unbonding_timeblock, undelegated_tokens):
        self.undelegated_tokens += undelegated_tokens
        self.locked_until = unbonding_timeblock
   
    def will_act(self):
        return 1

