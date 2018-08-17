# search.py

"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

class Path(object):
    def __init__(self, locations, directions, cost):
        self.locations = locations
        self.directions = directions
        self.cost = cost

        
def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    states = set(problem.getStartState())
    start = (problem.getStartState(),[])


    stack = util.Stack()
    stack.push(start)
    
    while not stack.isEmpty():
        state,actions = stack.pop()

        if problem.isGoalState(state):return actions
        
        nextSteps = problem.getSuccessors(state) # 4 directions

        for nextStep in nextSteps:
            nextstate,nextaction,_ = nextStep
            if nextstate not in states:
                states.add(nextstate)
                nextactions = actions[:]
                nextactions.append(nextaction)
                stack.push((nextstate,nextactions))
   
    return []
                  

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    states = set(problem.getStartState())
    start = (problem.getStartState(),[])
             
    queue = util.Queue()
    queue.push(start)

    while not queue.isEmpty():
        state,actions = queue.pop()
        if problem.isGoalState(state):return actions
        successors = problem.getSuccessors(state) # 4 directions
        for successor in successors:
            nextstate,nextaction,_ = successor
            if nextstate not in states:
                states.add(nextstate)
                nextactions = actions[:]
                nextactions.append(nextaction)
                queue.push((nextstate,nextactions))

    return []
    

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    states = set(problem.getStartState())
    start = (problem.getStartState(),[],0)
             
    queue = util.PriorityQueue()
    queue.push(start,0)

    while not queue.isEmpty():
        state,actions,cost = queue.pop()
        if problem.isGoalState(state):return actions
        
        successors = problem.getSuccessors(state) # 4 directions
        for successor in successors:
            nextstate,nextaction,nextcost = successor
            if nextstate not in states:
                states.add(nextstate)
                nextactions = actions[:]
                nextactions.append(nextaction)
                nextcost += cost
                queue.push((nextstate,nextactions,nextcost),nextcost)

    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    
    states = set(problem.getStartState())
    start = (problem.getStartState(),[],0)
             
    queue = util.PriorityQueue()
    queue.push(start,0)

    while not queue.isEmpty():
        state,actions,cost= queue.pop()
#        print(h)
        if problem.isGoalState(state):return actions
        
        successors = problem.getSuccessors(state) # 4 directions
        for successor in successors:
            nextstate,nextaction,nextcost = successor
            if nextstate not in states:
                states.add(nextstate)
                nextactions = actions + [nextaction]
                nextcost += cost
                nextHeuristic = heuristic(nextstate, problem)
                queue.push((nextstate,nextactions,nextcost),nextcost+nextHeuristic)

    return []
    


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
