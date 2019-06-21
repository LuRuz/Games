## Javier Huertas (2017-18)
## Alejandro Cervantes (2017-18)
'''
    Performs the search for the game agent

    If a WebViewer() is used, the server is in:
      http://localhost:8000/#
'''
import os
import sys
sys.path.append(os.path.abspath("../simpleai-0.8.1"))
from simpleai.search import breadth_first,depth_first,astar
from simpleai.search.viewers import BaseViewer,ConsoleViewer,WebViewer
sys.path.append(os.path.abspath("../student"))
from gameProblem import GameProblem


def searchSolution(map,configuration,state,aiBaseName,tracep):
    
    ''' Creates a gameProblem object, and calls its initialization
        Passes the description of the map both in matrix and in dictionary form
        Then executes the search algorithm defined upon initialization
        Transforms the solution in a plan in the format required by the game
    '''
    
    result = False
    
    if tracep:
        debugCall(map,configuration,state)

    mapAsPositions=transformMap(map,configuration)

    problem = GameProblem()
    problem.initializeProblem(map=map,positions=mapAsPositions,conf=configuration,aiBaseName=aiBaseName)
    algorithm=problem.ALGORITHM
    useViewer=BaseViewer()

    print ("----------------------- PROBLEM INFORMATION ------------------")
    print ("-- Initial State  --")
    print (problem.initial_state)

    print ("-- Final State  --")
    print (problem.GOAL)

    print ("-- Search Algorithm --")
    print (problem.ALGORITHM)
    
    print ("-------------   EXECUTING SEARCH   -------------------")
    result = algorithm(problem,graph_search=True,viewer=useViewer)

    
    if result:
        print ("-------------   SEARCH RESULTS   -------------------")
        print("Reached final state: {0}".format(result.state))
        
        print (searchInfo(problem,result,useViewer))
        
        print("Solution as path (length:{0}): {1}".format(len(result.path()),result.path()))
                
        detailed_path = result.path()[1:]

        plan = list ( (a[0],{'showText': 'Executing {0} -> State {1}'.format(a[0],problem.printState(a[1])),
                             'onState': problem.getStateData(a[1])
                             } 
                    )  for a in detailed_path)

        return plan,problem,result,useViewer
    else:
        print ("WARNING: A solution was not found for the final state: {0}".format(problem.GOAL))
        return None,None,None,None


# END searchSolution

# ------------------------UTILITY FUNCTIONS --------------
def transformMap (map,configuration):
    mapDict={}
    mapitems = set(j[0] for i in map for j in i)
    for itemName in mapitems:
        positions = []
        position_rows = [r for r,v in enumerate(map) if itemName in [c[0] for c in v]]
        for r in position_rows:
            position_cols = [c for c,v in enumerate(map[r]) if v[0]==itemName ]
            for c in position_cols:
                positions.append((r,c))
        mapDict[itemName]=positions
    
    agentPos = []
    agentName = configuration['agent']['id']
    position_rows = [r for r,v in enumerate(map) if agentName in [c[3]['agent'] for c in v]]
    for r in position_rows:
        position_cols = [c for c,v in enumerate(map[r]) if v[3]['agent']==agentName ]
        for c in position_cols:
            agentPos.append((r,c))
    mapDict[agentName] = agentPos
    return mapDict
# END transformMap

def getTotalCost (problem,result):
    originState = problem.initial_state
    totalCost = 0
    for action,endingState in result.path():
        if action is not None:
            totalCost += problem.cost(originState,action,endingState)
            originState = endingState
    return totalCost
    
def searchInfo (problem,result,useViewer):
    
    res = "total length of solution: {0}\n".format(len(result.path())-1)
    res += "total cost of solution: {0}\n".format(getTotalCost(problem,result))
        
    if useViewer:
        stats = [{'name': stat.replace('_', ' '), 'value': value}
                         for stat, value in list(useViewer.stats.items())]
        
        for s in stats:
            res+= '{0}: {1}\n'.format(s['name'],s['value'])
    return res
    

def debugCall (map,configuration,state):
    print ("---------------- Map -----------------")
    print (map)
    print ("---------------- Configuration ------------------")
    print (configuration)
    print ("---------------- Game State -----------------")
    print (state)
    print ("---------------- Elements of the map -----------------")
    mapAsPositions=transformMap(map,configuration)
    for k,v in mapAsPositions.items():
        print ('Elements of type "{0}":{1}'.format(k,v))
        
    
# ------------   END OF UTILITY FUNCTIONS -------------





    
