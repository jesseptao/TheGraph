# BlockScience collaboration with The Graph
The goal of this collaboration is to come up with proposed V2 mechanisms for The Graph’s delegator subsystem. BlockScience will develop a cadCAD model, a “Design Digital Twin”, of the current V1 delegator subsystem with the goal of utilizing the model to assist in the design of the V2 mechanisms. 

## Stage 1 (In Progress)

### As-Is V1 cadCAD Model

We will develop a cadCAD model of the  As-is V1 delegator subsystem based upon the current Solidity implementation. The V1 mechanisms in our model will be verified through a number of discrete event simulations to ensure that the model is an accurate representation of the V1 implementation. This model will then be utilized to assist in the design of V2 mechanisms. 

Deliverables:
* [V1 Mathematical Specification](https://hackmd.io/7UvPze36RbyjfJ9-F9mHTQ?view)
* [V1 cadCAD Model](model)
* [V1 Verification Process](https://hackmd.io/@SBmoxUc1RD-orQSa-5V6XA/rkjQ7cb1K)
* [V1 Verification Test Plan](https://docs.google.com/spreadsheets/d/111Bu-iVg6MCYzfU5lNSElLRw19JH81O_6U0Go9bD4Is/edit#gid=0)
* V1 Verification Tests
  * [Delegate](test_delegation.ipynb)
  * [Undelegate](test_undelegation.ipynb)
  * [Withdraw](test_withdraw.ipynb)
  * [Indexing Rewards](test_indexing_rewards.ipynb)
  * [Query Fee Rewards](test_query_rewards.ipynb)

### Null hypothesis V2 Design

We will design V2 mechanisms following our typical Engineering Design Process (Requirements -> Design -> Validation). We will work together with The Graph to ensure design goals and requirements are well understood and documented. Implementation limitations and considerations will be taken into account to ensure practicality of the design. At this stage, we will come up with a null hypothesis and in the next stage we will develop behavioural models and run experiments to iterate and validate the design.

Deliverables:
* V2 Mathematical Specification - Work In Progress
* V2 cadCAD Model - Work In Progress

## Stage 2 (Upcoming)

### Behavioural Models

We will develop behavioural models in order to test the V2 design against various scenarios/assumptions about the way actors may interact with the system. We will run a series of experiments/simulations to iterate on and refine the proposed V2 mechanisms. 

Deliverables:
* V2 Revised Mathematical Specification
* V2 Revised cadCAD Model
* V2 Experiments

## Model employs cadCAD simulation framework
```
                  ___________    ____
  ________ __ ___/ / ____/   |  / __ \
 / ___/ __` / __  / /   / /| | / / / /
/ /__/ /_/ / /_/ / /___/ ___ |/ /_/ /
\___/\__,_/\__,_/\____/_/  |_/_____/
by cadCAD                  ver. 0.4.23
======================================
       Complex Adaptive Dynamics       
       o       i        e
       m       d        s
       p       e        i
       u       d        g
       t                n
       e
       r
```
cadCAD (complex adaptive dynamics Computer-Aided Design) is a python based modeling framework for research, validation, and Computer Aided Design of complex systems. Given a model of a complex system, cadCAD can simulate the impact that a set of actions might have on it. This helps users make informed, rigorously tested decisions on how best to modify or interact with the system in order to achieve their goals. cadCAD supports different system modeling approaches and can be easily integrated with common empirical data science workflows. Monte Carlo methods, A/B testing and parameter sweeping features are natively supported and optimized for.

cadCAD links for more information:
* https://community.cadcad.org/t/introduction-to-cadcad/15
* https://community.cadcad.org/t/putting-cadcad-in-context/19
* https://github.com/cadCAD-org/demos

# Getting Started


#### Change Log: [ver. 0.4.23](CHANGELOG.md)

[Previous Stable Release (No Longer Supported)](https://github.com/cadCAD-org/cadCAD/tree/b9cc6b2e4af15d6361d60d6ec059246ab8fbf6da)

## 0. Pre-installation Virtual Environments with [`venv`](https://docs.python.org/3/library/venv.html) (Optional):
If you wish to create an easy to use virtual environment to install cadCAD inside of, please use the built in `venv` package.

***Create** a virtual environment:*
```bash
$ python3 -m venv ~/cadcad
```

***Activate** an existing virtual environment:*
```bash
$ source ~/cadcad/bin/activate
(cadcad) $
```

***Deactivate** virtual environment:*
```bash
(cadcad) $ deactivate
$
```

## 1. Installation: 
Requires [>= Python 3.6](https://www.python.org/downloads/) 

**Option A: Install Using [pip](https://pypi.org/project/cadCAD/)** 
```bash
$ pip3 install cadCAD
```

