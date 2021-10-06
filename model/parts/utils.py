import pandas as pd
from decimal import *

getcontext().prec = 6
print(getcontext())
from pandas.core.accessor import delegate_names
def convertFromLongStrToDecimal(d, field, GRT_conversion_rate):
    for events in d.values():
        for event in events:                       
            # sometimes it comes in as a number, sometimes as a string
            event[field] = str(event[field])

            # put in a decimal place 18 chars from the right then convert to Decimal to avoid overflow error.
            try:
                strValue = event[field][:len(event[field]) - -GRT_conversion_rate] + "." + event[field][GRT_conversion_rate:]
                # print(strValue)
                event[field] = Decimal(strValue)
            except:
                # print(event[field])
                # print("Unexpected error:", sys.exc_info()[0])
                event[field] = Decimal(0)

def convertFromLongStrToDecimalPercent(d, field):
    # 1000000 is 100%
    # so divide by a million to get percent.
    for events in d.values():
        for event in events:                       
            # sometimes it comes in as a number, sometimes as a string
            event[field] = Decimal(event[field])

            # put in a decimal place 18 chars from the right then convert to Decimal to avoid overflow error.
            event[field] = event[field] / 1000000

def load_all_events(path,GRT_conversion_rate = -18):
    # make them ordered by blockNumber
    # squish them because time between doesn't matter
    # **but they have to be interleaved between all event types.
    # reset index
    # break back out to distinct types
    # use block number, resolve conflicts with log index.
    all_events = pd.read_csv(f'{path}/singleIndexer.csv')
    all_events.reset_index(inplace=True)
    all_events = all_events.rename(columns={'index': 'timestep'})
    all_events.set_index('timestep', inplace=True, drop=False)
    all_events.sort_values(['blockNumber', 'logIndex'], ascending=[True, True])

    # print(all_events.loc[:, ['blockNumber', 'logIndex']])    

    # create a dict from the df where duplicate timesteps appear in a list of dicts under the same timestep index. 
    # NOTE: there should be no duplicates anymore.
    event_types = ['stakeDelegateds', 'stakeDelegatedLockeds', 'stakeDelegatedWithdrawns', 'allocationCloseds', 
                   'allocationCollecteds', 'stakeDepositeds', 'rewardsAssigneds', 'delegationParametersUpdateds']
    events_list_of_dicts = []
    for event_type in event_types:
        events = all_events[all_events['type'] == event_type]
        print(f'{event_type}: {len(events)} events')
        # print(events['timestep'])
        d = events.groupby(level=0).apply(lambda x: x.to_dict('records')).to_dict()
        
        # print(d)
        convertFromLongStrToDecimal(d, 'tokens', GRT_conversion_rate)
        # print(d)
        try:
            convertFromLongStrToDecimal(d, 'shares', GRT_conversion_rate) 
            convertFromLongStrToDecimal(d, 'amount', GRT_conversion_rate)            
            convertFromLongStrToDecimalPercent(d, 'indexingRewardCut')
            convertFromLongStrToDecimalPercent(d, 'queryFeeCut')
        except KeyError:
            print('KEYERROR!!!')
            pass
        events_list_of_dicts.append(d)
    print(f'TOTAL NUMBER OF EVENTS: {len(all_events)}')
    print(f'You should set SIMULATION_TIME_STEPS in config.py to a minimum of {len(all_events)} to capture all events.')
    print()
    return events_list_of_dicts


def load_delegation_event_sequence_from_csv(path, blockNumberShift = 11474307, blocksPerEpoch = 6500, limit = None, GRT_conversion_rate = -18):
    df = pd.read_csv(path)
    # limit number of records read in 
    if limit is not None:
        df = df.head(limit)
    else:
        pass
    # print(f'loading {path}...')
    
    df['timestep'] = (df.blockNumber - blockNumberShift) / blocksPerEpoch + 1
    df.timestep = df.timestep.astype(int)
    
    # set the index to timestep inplace and don't drop timestep from the df.
    df.set_index('timestep', inplace=True, drop=False)

    # create a dict from the df where duplicate timesteps appear in a list of dicts under the same timestep index.
    d = df.groupby(level=0).apply(lambda x: x.to_dict('records')).to_dict()
    # print(f'{d=}')
    
    convertFromLongStrToDecimal(d, 'tokens', GRT_conversion_rate)
    try:
        convertFromLongStrToDecimal(d, 'shares', GRT_conversion_rate) 
        convertFromLongStrToDecimal(d, 'amount', GRT_conversion_rate)
    except KeyError:
        pass
    # d['tokens'] = d['tokens'].apply(lambda x: int(x) * GRT_conversion_rate)
    print(f'loaded {path}.')
    return d
    

def total_stake_deposited(stake_deposited_events):
    total = 0
    if stake_deposited_events:
        for stake_deposited_event in stake_deposited_events:
            total += stake_deposited_event['tokens']    
    return total

if __name__ == '__main__':
    event_path = 'another_indexer/single_indexer'
    delegation_events, undelegation_events, withdraw_events, indexing_fee_events, query_fee_events, stake_deposited_events, rewards_assigned_events = load_all_events(event_path)
