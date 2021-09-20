# def compute_and_store_private_prices(params, step, sL, s, inputs):
#     delegators = s['delegators']
#     shares = s['shares']
#     pool_delegated_stake = s['pool_delegated_stake']
#     timestep = s['timestep']
#     indexer_revenue_cut = s['indexer_revenue_cut']
#     risk_adjustment = params['risk_adjustment']
#     pool_delegated_stake_to_revenue_token_exchange_rate = params['pool_delegated_stake_to_revenue_token_exchange_rate']
#     private_price = 0
    
#     for delegator in delegators.values():
#         # NOTE: this is the discounted value of the dividends
#         dividend_value = delegator.dividend_value(shares, indexer_revenue_cut, pool_delegated_stake_to_revenue_token_exchange_rate)
        
#         # NOTE: this is the current spot price, from the invariant
#         share_value = pool_delegated_stake / shares
        
#         risk_adjusted_share_value = share_value * risk_adjustment
        
#         private_price = dividend_value + risk_adjusted_share_value
#         # print(f'{timestep=}, {private_price=}')
#         delegator.private_prices[timestep] = private_price
    
#     # print(delegators)
#     key = 'delegators'
#     value = delegators
#     return key, value
