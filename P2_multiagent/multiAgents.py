# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        
        if successorGameState.isWin():
            return float("inf")
        
        foodlist = newFood.asList()
        foodDist = [util.manhattanDistance(food, newPos) for food in foodlist]
        minFoodDist = min(foodDist) if len(foodDist)>0 else 0

        minGhostDist = 300
        for i,ghostState in enumerate(newGhostStates):
            if newScaredTimes[i]<2:
                if util.manhattanDistance(ghostState.getPosition(), newPos) < 2:
                    return float("-inf")
           
                newGhostDist=util.manhattanDistance(ghostState.getPosition(), newPos)
                minGhostDist = min(newGhostDist,minGhostDist)
##        
##        eaten = 0
##        if (currentGameState.getNumFood() > successorGameState.getNumFood()):
##            eaten = 300
        #successorGameState.getScore()
        return -minFoodDist + minGhostDist - len(foodlist)*100

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        PacmanActions  = gameState.getLegalActions(0)
        return max(PacmanActions,key = lambda x:self.score(gameState.generateSuccessor(0, x), 1, 1))

    def score(self, state, depth, agent):
        ## return minimax score of the agent,depending on the scores
        ## of nextstate and the type of the agent

        if agent == state.getNumAgents():
            if depth == self.depth:
                return self.evaluationFunction(state)
            else:
                return self.score(state,depth + 1,0)
        else:
            actions = state.getLegalActions(agent)

            if len(actions) == 0: ##state.isWin() or state.isLose()
                return self.evaluationFunction(state)

            nextscores = (self.score(state.generateSuccessor(agent, action),
                    depth, agent + 1) for action in actions)
            
            return (max if agent == 0 else min)(nextscores)

                 

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        PacmanActions  = gameState.getLegalActions(0)
        alpha,beta = float("-inf"),float("inf")
        max_action = max(PacmanActions,key = lambda x:self.score(gameState.generateSuccessor(0, x), 1, 1,alpha,beta))
        ## for debug
##        max_score = self.score(gameState.generateSuccessor(0, max_action), 1, 1,alpha,beta)
##        print(max_score)
        return max_action

    def score(self, state, depth, agent,alpha,beta):
        ## return minimax score of the agent,depending on the scores
        ## of nextstate and the type of the agent

        if agent == state.getNumAgents():
            if depth == self.depth:
                return self.evaluationFunction(state)
            else:
                return self.score(state,depth + 1,0,alpha,beta)
        else:
            actions = state.getLegalActions(agent)

            if len(actions) == 0: ##state.isWin() or state.isLose()
                return self.evaluationFunction(state)
            
            #the max_value() and min_value() map state to max/min nextscore
            # state->nextstate->nextscore
            
            if agent == 0: return self.max_value(state,alpha,beta,agent,depth)
            else: return self.min_value(state,alpha,beta,agent,depth)
            
    def max_value(self,state,alpha,beta,agent,depth):
        v = float("-inf")
        for action in state.getLegalActions(agent):
            successor = state.generateSuccessor(agent, action)
            v = max(v,self.score(successor,depth,agent+1,alpha,beta))
            if v > beta: return v
            alpha = max(alpha,v)
        return v
    
    def min_value(self,state,alpha,beta,agent,depth):
        v = float("inf")
        for action in state.getLegalActions(agent):
            successor = state.generateSuccessor(agent,action)
            v = min(v,self.score(successor,depth,agent+1,alpha,beta))
            if v <alpha: return v
            beta = min(beta,v)
        return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        PacmanActions  = gameState.getLegalActions(0)
        return max(PacmanActions,
                   key = lambda x:self.score(gameState.generateSuccessor(0, x), 1, 1))
    

    def score(self, state, depth, agent):
        ## return minimax score of the agent,depending on the scores
        ## of nextstate and the type of the agent

        if agent == state.getNumAgents():
            if depth == self.depth:
                return self.evaluationFunction(state)
            else:
                return self.score(state,depth + 1,0)
        else:
            actions = state.getLegalActions(agent)

            if len(actions) == 0: ##state.isWin() or state.isLose()
                return self.evaluationFunction(state)

            nextscores = [self.score(state.generateSuccessor(agent, action),
                    depth, agent + 1) for action in actions]
            
            return (max if agent == 0 else self.ave)(nextscores)

    def ave(self,l):
        return sum(l)/float(len(l))

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    score = scoreEvaluationFunction(currentGameState)
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghosts = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()

    if currentGameState.isWin():
        return float("inf")

    food_left = len(food.asList())

    #The score drop due to the increased distance to the next
    # nearest pellet should be less than the score gain from
    # eating the pellet.

    #A close food pellet is a good thing, but we want grabbing
    #one to have a limited value on the change in score.So the reciprocal is used.

    ## the max of eating a food is 1, and the increase of the dist is bounded by 1.
    ## before eating, the mindist = 1, after eating,less than inf.

    problem = AnyFoodSearchProblem(currentGameState)
    shortest_food = aStarSearch(problem, heuristic = nearest_food_heuristic)
    if shortest_food:
        shortest_food = 1 / len(shortest_food)
    else:
        shortest_food = 1000

    #The negative reciprocal of the distance to the closest ghost
    # A close ghost makes the state less desirable, but variances
    # in ghosts far away should have little impact

    ghosts = [ghost for ghost in ghosts if ghost.scaredTimer == 0]
    if ghosts:
        ghost_distances = [manhattanDistance(ghost.getPosition(), pos)
                           for ghost in ghosts]
        shortest_ghost = min(ghost_distances)

        if shortest_ghost == 0:
            shortest_ghost = float('inf')
        else:
            shortest_ghost = 1 / shortest_ghost
    else:
        shortest_ghost = 0

    capsules_left = len(capsules)
    if capsules:
        capsule_distances = [manhattanDistance(capsule, pos)
                             for capsule in capsules]
        shortest_capsule = 1 / min(capsule_distances)
    else:
        shortest_capsule = 0

    weights = [5, 10, -5, -50, -100]
    scores = [shortest_food, shortest_capsule, shortest_ghost,
              food_left, capsules_left]

    score = sum(i * j  for i, j in zip(scores, weights))

    return score
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."

    visited = set()
    p_queue = util.PriorityQueue()
    p_queue.push((problem.getStartState(), []), 0)

    while not p_queue.isEmpty():
        state, actions = p_queue.pop()

        if state in visited:
            continue

        visited.add(state)

        if problem.isGoalState(state):
            return actions

        for successor, action, stepCost in problem.getSuccessors(state):
            if successor not in visited:
                p_queue.push(
                    (successor, actions + [action]),
                    stepCost + problem.getCostOfActions(actions) +
                    heuristic(successor, problem = problem))

from game import Actions
class PositionSearchProblem:
    """
    A search problem defines the state space, start state, goal test,
    successor function and cost function.  This search problem can be
    used to find paths to a particular point on the pacman board.
    The state space consists of (x,y) positions in a pacman game.
    Note: this search problem is fully specified; you should NOT change it.
    """

    def __init__(self, gameState, costFn = lambda x: 1, goal=(1,1), start=None, warn=True, visualize=True):
        """
        Stores the start and goal.
        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start != None: self.startState = start
        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print 'Warning: this does not look like a regular search maze'

        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal

        # For display purposes only
        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display): #@UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist) #@UndefinedVariable

        return isGoal

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.
         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append( ( nextState, action, cost) )

        # Bookkeeping for display purposes
        self._expanded += 1
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999
        """
        if actions == None: return 999999
        x,y= self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x,y))
        return cost

class AnyFoodSearchProblem(PositionSearchProblem):
    """
      A search problem for finding a path to any food.
      This search problem is just like the PositionSearchProblem, but
      has a different goal test, which you need to fill in below.  The
      state space and successor function do not need to be changed.
      The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
      inherits the methods of the PositionSearchProblem.
      You can use this search problem to help you fill in
      the findPathToClosestDot method.
    """

    def __init__(self, gameState):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test
        that will complete the problem definition.
        """
        x,y = state
        return self.food[x][y]

def manhattanHeuristic(position, problem, info={}):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def nearest_food_heuristic(pos, problem, info={}):
    food = problem.food
    food_distances = [
        manhattanDistance(pos, (x, y))
        for x, row in enumerate(food)
        for y, food_bool in enumerate(row)
        if food_bool
        ]

    return min(food_distances) if food_distances else 0

# Abbreviation
better = betterEvaluationFunction

