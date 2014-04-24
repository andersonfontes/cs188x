# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
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

        farest_food = 0
        nearest_food = 99999
        if newFood.count() > 0:
            for food in newFood.asList():
                farest_food = max(farest_food, manhattanDistance(newPos, food))
                nearest_food = min(nearest_food, manhattanDistance(newPos, food))
        else:
            nearest_food = 0

        c = 0
        for capsule in successorGameState.getCapsules():
            c = max(c, manhattanDistance(newPos, capsule))

        ng = 99999
        fg = 0
        for ghost in newGhostStates:
            ng = min(ng, manhattanDistance(newPos, ghost.getPosition()))
            fg = max(fg, manhattanDistance(newPos, ghost.getPosition()))

        evaluation = successorGameState.getScore() - newFood.count(False) - nearest_food + ng

        return evaluation

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

        pacman_actions = gameState.getLegalActions(0)
        # ghosts_actions = [gameState.getLegalActions(i)
        #                   for i in range(1, gameState.getNumAgents())]

        scores = []
        states = []
        print(pacman_actions)
        for action in pacman_actions:
            print(action)
            state = gameState.generateSuccessor(0, action)
            states.append(state)
            self.cur_depth = 0
            self.is_max = True
            scores.append(self.get_value(state))

        best_score = max(scores)

        best_indices = [i for i in range(len(scores)) if scores[i] == best_score]
        print(scores, best_indices, pacman_actions)
        return pacman_actions[random.choice(best_indices)]

    def get_value(self, state):
        # print(self.depth, self.cur_depth)
        if self.cur_depth >= self.depth\
                or state.isWin() or state.isLose():

            print(state.isWin(), state.isLose())
            print(self.depth, self.cur_depth)

            if self.cur_depth < self.depth:
                self.cur_depth -= 1

            self.is_max = not self.is_max

            return self.evaluationFunction(state)

        self.cur_depth += 1
        self.is_max = not self.is_max

        if self.is_max:
            print('max')
            # self.is_max = False
            v = self.get_max_value(state)
            print(v)
            return v
        else:
            print('min')
            # self.is_max = True
            v = self.get_min_value(state)
            print(v)
            return v

    def get_max_value(self, state):
        v = -99999
        for action in state.getLegalActions():
            new_state = state.generateSuccessor(0, action)
            v = max(v, self.get_value(new_state))
            print('here')
        return v

    def get_min_value(self, state):
        v = 99999
        for action in state.getLegalActions():
            new_state = state.generateSuccessor(0, action)
            v = min(v, self.get_value(new_state))
        return v


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
