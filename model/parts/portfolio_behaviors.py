from .portfolio import Portfolio

def delegate_portfolio(params, step, sL, s, inputs):
    portfolios = s['delegator_portfolios']
    event = inputs['delegation_events'][0] if inputs['delegation_events'] is not None else None
    delegation_tax_rate = params['delegation_tax_rate']
    if event:
        indexerID = event['indexer']
        delegatorID = event['delegator']
        indexer = s['indexers'][event['indexer']]
        pool_delegated_stake = indexer.pool_delegated_stake
        if delegatorID not in portfolio.keys():
            portfolio = Portfolio(delegatorID)
            portfolios['delegatorID'] = portfolio
        else:
            portfolio = portfolios['delegatorID']
        portfolio.holdings -= event['tokens'] / (1 - delegation_tax_rate)
        shares = sum([d.shares for d in indexer.delegators.values()])
        portfolio.indexer_in_tokens[indexerID] += event['tokens'] * (1 - delegation_tax_rate)
        portfolio.indexer_shares[indexerID] += event['tokens'] * (1 - delegation_tax_rate) if pool_delegated_stake.is_zero() \
                 else ((event['tokens'] * (1 - delegation_tax_rate)) / pool_delegated_stake) * shares
        portfolio.indexer_price[indexerID] = portfolio.indexer_shares[indexerID] / portfolio.indexer_tokens[indexerID]
    
    key = 'delegator_portfolios'
    return key, s['delegator_portfolios']

def undelegate_portfolio(params, step, sL, s, inputs):
    portfolios = s['delegator_portfolios']
    event = inputs['undelegation_events'][0] if inputs['undelegation_events'] is not None else None    
    if event:
        indexerID = event['indexer']
        delegatorID = event['delegator']
        indexer = s['indexers'][event['indexer']]
        portfolio = portfolios['delegatorID']
        portfolio.holdings += event['tokens']
        portfolio.indexer_revenues[indexerID] += event['tokens']
        portfolio.indexer_realized_price[indexerID] = portfolio.indexer_shares[indexerID] / portfolio.indexer_revenues[indexerID]
        portfolio.indexer_yield[indexerID] = portfolio.indexer_revenues[indexerID] / portfolio.indexer_in_tokens[indexerID]
        portfolio.ROI = sum(portfolio.indexer_yield.values() / len(portfolio.indexer_yield.values()))
    key = 'delegator_portfolios'
    return key, s['delegator_portfolios']
        
    
        
        