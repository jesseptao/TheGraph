import random
from model.parts.delegator import Delegator
from . import utils
from decimal import *


""" this just gets all of the events at this timestep into policy variables """
def delegate_actions(params, step, sL, s):
    # who delegates, 
    # how many tokens.
    timestep = s['timestep']
    delegation_events = params['delegation_tokens_events'].get(timestep)
    return {'delegation_events': delegation_events}

""" this just gets all of the events at this timestep into policy variables """
def undelegate_actions(params, step, sL, s):
    # who delegates, 
    # how many tokens.
    timestep = s['timestep']
    undelegation_events = params['undelegation_shares_events'].get(timestep)
    return {'undelegation_events': undelegation_events}

""" this just gets all of the events at this timestep into policy variables """
def withdraw_actions(params, step, sL, s):
    # who delegates, 
    # how many tokens.
    timestep = s['timestep']
    withdraw_events = params['withdraw_tokens_events'].get(timestep)
    return {'withdraw_events': withdraw_events}

def delegate(params, step, sL, s, inputs):
            #     'pool_delegated_stake': add_delegated_stake_to_pool,
            # 'GRT': account_for_tax,
            # 'delegators': delegate,
    event = inputs['delegation_events'][0] if inputs['delegation_events'] is not None else None    
    if event:
        indexer = s['indexers'][event['indexer']]
        # print("DELEGATE EVENT", event)
        # # Step 1: Account for Tax
        # # sum up the number of tokens delegated this timestep        
        
        # # print(f'{delegation_tokens_quantity=}')
        # delegation_tax_rate = params['delegation_tax_rate']        
        # tax = delegation_tax_rate * event['tokens']
        # indexer.GRT -= tax

        # # Step 2: Add Delegated Stake to Pool
        # indexer.pool_delegated_stake += event['tokens']

        # Step 3: Delegate        
        # NOTE: must recompute global shares each time because it affects how many tokens go where.
        # TODO: don't think we need to compute shares each time because we have only one event per timestep.
        shares = sum([d.shares for d in indexer.delegators.values()])
        
        delegation_tax_rate = params['delegation_tax_rate']        
        initial_holdings = params['delegator_initial_holdings']
        delegators = indexer.delegators

        delegator_id = event['delegator']
        if delegator_id not in delegators:
            delegators[delegator_id] = Delegator(delegator_id, holdings = initial_holdings)
        
        delegator = delegators[delegator_id]        
        delegation_tokens_quantity = event['tokens']

        
        print(f"""EVENT: DELEGATE (before)--
                    {indexer.id=},
                    {delegator_id=}, 
                    {indexer.pool_delegated_stake=},
                    {delegation_tokens_quantity=},
                    {shares=},
                    {delegator.holdings=}, 
                    {delegator.shares=}""")

        indexer.pool_delegated_stake = process_delegation_event(delegation_tokens_quantity, delegator, initial_holdings, 
                                            delegation_tax_rate, indexer.pool_delegated_stake, shares)        

        print(f"""  (after)--
                    {indexer.id=},
                    {delegator.id=}, 
                    {indexer.pool_delegated_stake=},
                    {delegation_tokens_quantity=},
                    {shares=},                
                    {delegator.holdings=}, 
                    {delegator.shares=}""")


    key = 'indexers'
    return key, s['indexers']



def process_delegation_event(delegation_tokens_quantity, delegator, initial_holdings, delegation_tax_rate, pool_delegated_stake, shares):




    # NOTE: allow this for now.
    # if delegation_tokens_quantity >= delegator.holdings:
    #     delegation_tokens_quantity = delegator.holdings        
    delegator.holdings -= delegation_tokens_quantity
    
    # 5 * (0.995) / 10 * 10 = 4.975
    print(f'{pool_delegated_stake=}, {shares=}, {delegation_tax_rate=}, {delegation_tokens_quantity=}')
    new_shares = delegation_tokens_quantity * (1 - delegation_tax_rate) if pool_delegated_stake == 0 \
                 else ((delegation_tokens_quantity * (1 - delegation_tax_rate)) / pool_delegated_stake) * shares
    
    # NOTE: pool_delegated_stake must be updated AFTER new_shares is calculated
    pool_delegated_stake += delegation_tokens_quantity * (1 - delegation_tax_rate)
    delegator.shares += new_shares
    shares += new_shares
    # store shares locally only--it has to be recomputed each action block because we don't save it until bookkeeping
    return pool_delegated_stake


def undelegate(params, step, sL, s, inputs):
    event = inputs['undelegation_events'][0] if inputs['undelegation_events'] is not None else None    
    if event:
        indexer = s['indexers'][event['indexer']]
    
        # shares needs to be kept updated
        shares = sum([d.shares for d in indexer.delegators.values()])
        
        # timestep = s['timestep']
        # print(undelegation_events)
        
        delegator_id = event['delegator']
        delegator = indexer.delegators[delegator_id]                
        undelegation_shares_quantity = event['shares']
        print(f'''EVENT: UNDELEGATE (before)--
            {delegator_id=}, 
            {delegator.holdings=}, 
            {delegator.undelegated_tokens=}, 
            {delegator.shares=}
            {undelegation_shares_quantity=}''')

        if undelegation_shares_quantity < 0:
            # require a non-zero amount of shares
            print(f'WARN: undelegation shares quantity < 0 ({undelegation_shares_quantity})')
        else:

            if undelegation_shares_quantity > delegator.shares:
                # require delegator to have enough shares in the pool to undelegate
                print(f'WARN: undelegation shares quantity > delegator shares held. ({undelegation_shares_quantity=}, {delegator.shares=})')
                undelegation_shares_quantity = delegator.shares

            # Withdraw tokens if available
            # TODO: make this accurate (28 days not timesteps)
            # withdrawableDelegatedTokens = delegator.getWithdrawableDelegatedTokens(timestep)
            # if withdrawableDelegatedTokens > 0:
            #     print(f'INFO: tokens withdrawn {withdrawableDelegatedTokens=}')
            #     delegator.withdraw(withdrawableDelegatedTokens)

            undelegated_tokens = undelegation_shares_quantity * (indexer.pool_delegated_stake / shares)
            until = event['until']
            delegator.set_undelegated_tokens(until, undelegated_tokens)
            delegator.shares -= undelegation_shares_quantity
            indexer.pool_delegated_stake -= undelegated_tokens
            shares -= undelegation_shares_quantity
            print(f'''  (after)--
                        {delegator_id=}, 
                        {delegator.holdings=}, 
                        {undelegated_tokens=},
                        {delegator.undelegated_tokens=}, 
                        {delegator.shares=}
                        {until=}
                        {undelegation_shares_quantity=}''')
    key = 'indexers'
    value = s['indexers']
    return key, value

def withdraw(params, step, sL, s, inputs):
    #  loop through acting delegators id list
    timestep = s['timestep']
    event = inputs['withdraw_events'][0] if inputs['withdraw_events'] is not None else None    
    if event:
        indexer = s['indexers'][event['indexer']]
    
        delegator_id = event['delegator']
        delegator = indexer.delegators[delegator_id]        
        tokens = event['tokens']
        print(f'''EVENT: WITHDRAW (before)--
                    {delegator_id=}, 
                    {delegator.holdings=}, 
                    {delegator.undelegated_tokens=}, 
                    {delegator.shares=}
                    {tokens=}''')
        withdrawableDelegatedTokens = delegator.getWithdrawableDelegatedTokens(timestep)
        if withdrawableDelegatedTokens > tokens:
            delegator.withdraw(tokens)
        elif withdrawableDelegatedTokens > 0:
            delegator.withdraw(withdrawableDelegatedTokens)
        else:
            pass

        print(f'''EVENT: WITHDRAW (after)--
                    {delegator_id=}, 
                    {delegator.holdings=}, 
                    {delegator.undelegated_tokens=}, 
                    {delegator.shares=}
                    {tokens=}
                    {withdrawableDelegatedTokens=}''')
    key = 'indexers'
    value = s['indexers']
    return key, value
