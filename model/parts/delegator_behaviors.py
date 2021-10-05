import random
from model.parts.delegator import Delegator
from . import utils


def may_act_this_timestep(params, step, sL, s):
    acting_delegator_ids = []
    for id, delegator in s['delegators'].items():
        if delegator.will_act():
            acting_delegator_ids.append(id)

    # randomize list.
    random.shuffle(acting_delegator_ids)

    return {'acting_delegator_ids': acting_delegator_ids}

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
    pool_delegated_stake = s['pool_delegated_stake']
    
    # NOTE: must recompute global shares each time because it affects how many tokens go where.
    shares = sum([d.shares for d in s['delegators'].values()])
    
    delegation_tax_rate = params['delegation_tax_rate']
    delegation_events = inputs['delegation_events'] if inputs['delegation_events'] is not None else []    
    initial_holdings = params['delegator_initial_holdings']
    delegators = s['delegators']
    # print(f'act: {acting_delegator_ids=}')
    
    for delegation in delegation_events:
        # this updates the delegators object.
        pool_delegated_stake, shares, delegators = process_delegation_event(delegation, delegators, initial_holdings, 
                                            delegation_tax_rate, pool_delegated_stake, shares)        

    key = 'delegators'
    value = delegators
    return key, value

def process_delegation_event(delegation, delegators, initial_holdings, delegation_tax_rate, pool_delegated_stake, shares):
    delegator_id = delegation['delegator']
    if delegator_id not in delegators:
        delegators[delegator_id] = Delegator(delegator_id, holdings = initial_holdings)
    
    delegator = delegators[delegator_id]        
    delegation_tokens_quantity = delegation['tokens']

    print(f"""ACTION: DELEGATE (before)--
                {delegator_id=}, 
                {pool_delegated_stake=},
                {delegation_tokens_quantity=},
                {shares=},
                {delegator.holdings=}, 
                {delegator.undelegated_tokens=}, 
                {delegator.shares=}""")

    # NOTE: allow this for now.
    # if delegation_tokens_quantity >= delegator.holdings:
    #     delegation_tokens_quantity = delegator.holdings        
    print(type(delegator.holdings))
    print(type(delegation_tokens_quantity))
    delegator.holdings -= delegation_tokens_quantity
    
    # 5 * (0.995) / 10 * 10 = 4.975
    # print(f'{pool_delegated_stake=}, {shares=}, {delegation_tax_rate=}, {delegation_tokens_quantity=}')
    new_shares = delegation_tokens_quantity * (1 - delegation_tax_rate) if pool_delegated_stake == 0 \
                 else ((delegation_tokens_quantity * (1 - delegation_tax_rate)) / pool_delegated_stake) * shares
    
    # NOTE: pool_delegated_stake must be updated AFTER new_shares is calculated
    pool_delegated_stake += delegation_tokens_quantity * (1 - delegation_tax_rate)
    delegator.shares += new_shares
    # store shares locally only--it has to be recomputed each action block because we don't save it until bookkeeping
    shares += new_shares 
    print(f"""  (after)--
                {delegator_id=}, 
                {pool_delegated_stake=},
                {delegation_tokens_quantity=},
                {shares=},                
                {delegator.holdings=}, 
                {delegator.undelegated_tokens=}, 
                {delegator.shares=}""")
    return pool_delegated_stake, shares, delegators

def account_for_tax(params, step, sL, s, inputs):
    key = 'GRT'
    # sum up the number of tokens delegated this timestep
    if inputs['delegation_events'] is None:
        delegation_tokens_quantity = 0
    else:
        delegation_tokens_quantity = sum(event['tokens'] for event in inputs['delegation_events'])
    # print(f'{delegation_tokens_quantity=}')
    delegation_tax_rate = params['delegation_tax_rate']
    
    tax = delegation_tax_rate * delegation_tokens_quantity
    value = s['GRT'] - tax
    return key, value

def undelegate(params, step, sL, s, inputs):
    
    # pool_delegated_stake needs to be updated
    pool_delegated_stake = s['pool_delegated_stake']
    undelegation_events = inputs['undelegation_events'] if inputs['undelegation_events'] is not None else []    
    delegators = s['delegators']
    
    # shares needs to be kept updated
    shares = sum([d.shares for d in s['delegators'].values()])
    
    timestep = s['timestep']
    # print(undelegation_events)
    #  loop through acting delegators id list
    for undelegation in undelegation_events:        
        
        delegator_id = undelegation['delegator']

        delegator = delegators[delegator_id]        
        print(f'''ACTION: UNDELEGATE (before)--
            {delegator_id=}, 
            {delegator.holdings=}, 
            {delegator.undelegated_tokens=}, 
            {delegator.shares=}''')
        
        undelegation_shares_quantity = undelegation['shares']

        if undelegation_shares_quantity < 0:
            # require a non-zero amount of shares
            continue

        if undelegation_shares_quantity > delegator.shares:
            # require delegator to have enough shares in the pool to undelegate
            undelegation_shares_quantity = delegator.shares

        # Withdraw tokens if available
        withdrawableDelegatedTokens = delegator.getWithdrawableDelegatedTokens(timestep)
        if withdrawableDelegatedTokens > 0:
            delegator.withdraw(withdrawableDelegatedTokens)

        undelegated_tokens = undelegation_shares_quantity * pool_delegated_stake / shares
        until = undelegation['until']
        delegator.set_undelegated_tokens(until, undelegated_tokens)
        delegator.shares -= undelegation_shares_quantity
        pool_delegated_stake -= undelegated_tokens
        shares -= undelegation_shares_quantity
        print(f'''  (after)--
                    {delegator_id=}, 
                    {delegator.holdings=}, 
                    {delegator.undelegated_tokens=}, 
                    {delegator.shares=}''')
    key = 'delegators'
    value = s['delegators']
    return key, value

def withdraw(params, step, sL, s, inputs):
    #  loop through acting delegators id list
    timestep = s['timestep']
    # print(f'act: {acting_delegator_ids=}')
    
    delegators = s['delegators']
    withdraw_events = inputs['withdraw_events'] if inputs['withdraw_events'] is not None else []    
    
    for withdraw in withdraw_events:
        delegator_id = withdraw['delegator']
        delegator = delegators[delegator_id]        
        tokens = withdraw['tokens']
        withdrawableDelegatedTokens = delegator.getWithdrawableDelegatedTokens(timestep)
        if withdrawableDelegatedTokens > tokens:
            delegator.withdraw(tokens)
        elif withdrawableDelegatedTokens > 0:
            delegator.withdraw(withdrawableDelegatedTokens)
        else:
            pass

        print(f'''ACTION: WITHDRAW--
                    {delegator_id=}, 
                    {delegator.holdings=}, 
                    {delegator.undelegated_tokens=}, 
                    {delegator.shares=}''')
    key = 'delegators'
    value = s['delegators']
    return key, value
