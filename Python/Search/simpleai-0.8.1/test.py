'''
    Basic search example
    Override actions, result, is_goal and heuristic to implement any search problem
    Connect to the web viewer to follow the execution step by step
    http://localhost:8000/#

    Initial state: void
    Actions: add letter to the start of the string
    Objective: HELLO WORLD
    Heuristic: Disimilarity
    Algorithm: A*
'''
from simpleai.search import SearchProblem, astar
from simpleai.search import breadth_first
from simpleai.search.viewers import WebViewer, BaseViewer

GOAL = 'HELLO WORLD'

class HelloProblem(SearchProblem):
    def actions(self, state):
        if len(state) < len(GOAL):
            return list(' ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        else:
            return []

    def result(self, state, action):
        return state + action

    def is_goal(self, state):
        return state == GOAL

    def heuristic(self, state):
        # how far are we from the goal?
        wrong = sum([1 if state[i] != GOAL[i] else 0  for i in range(len(state))])
        missing = len(GOAL) - len(state)
        return wrong + missing

my_viewer = BaseViewer()

problem = HelloProblem(initial_state='')
# result = astar(problem)

result = astar(problem,viewer=my_viewer)

print(result.state)
print(result.path())

