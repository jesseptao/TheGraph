# from .delegate_front_runner import DelegateFrontRunner
def agent_actions(params, step, sL, s, inputs):
# To generate an event, two methods would need to be called on an instantiation of an agent object 
# (“agent”):
# agent.inputs(Inputs), where Inputs contains the info the agent needs to update their state and set 
# an action--in practice this could just be the previous state of the system + system parameters, 
# as per usual
# output = agent.getAction(), which triggers the agent workflow and stores the output of the agent 
# in output; this would then be parsed to extract events according to the agent’s output schema.
    
    
    agent = s['agents'][0]
    inpt = {
                'availableIndexers'         : s['indexers'],
                'currentPeriod'             : s['timestep'] / params['blocks_per_epoch'],
                'disputeChannelEpochs'      : params['dispute_channel_epochs'],
                'delegationUnbondingPeriod' : params['unbonding_days'],
                # 'accountBalance'            : newInput['accountBalance']
            }
        
    
    agent.inputs(inpt)
    action = agent.getAction()
    return action