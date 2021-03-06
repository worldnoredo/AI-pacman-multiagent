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

        "*** YOUR CODE HERE ***"
        totalScore=0
        for ghost in newGhostStates:
          d=manhattanDistance(ghost.getPosition(), newPos)
          
          if(d<=1):
            if(ghost.scaredTimer!=0):
              totalScore+=2000
            else:
              totalScore-=200
          elif (d <= 2) and (ghost.scaredTimer==0):
            totalScore-=1/(d*d*d)

        for capsule in currentGameState.getCapsules():
          d=manhattanDistance(capsule,newPos)
          if(d==0):
            totalScore+=100
          else:
            totalScore+=10.0/d
        nearDistance = float('inf')
        for food in currentGameState.getFood().asList():
          d=manhattanDistance(food,newPos)
          if (d == 0):
            totalScore += 100
            print 'eat'
          elif (d<nearDistance):
            nearDistance = d
        if (nearDistance!=0):
          totalScore +=10/(nearDistance)
        return totalScore

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
        bestScore,bestMove=self.maxFunction(gameState,self.depth)
        return bestMove


    def maxFunction(self,gameState,depth):
        if depth==0 or gameState.isWin() or gameState.isLose(): 
          return self.evaluationFunction(gameState), "noMove"

        moves=gameState.getLegalActions()

        scores = [self.minFunction(gameState.generateSuccessor(self.index,move),1, depth) for move in moves]

        bestScore=max(scores)

        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = bestIndices[0]
        return bestScore,moves[chosenIndex]


    def minFunction(self,gameState,agent, depth):  
        if depth==0 or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState), "noMove"
        moves=gameState.getLegalActions(agent) #get legal actions.
        scores=[]

        if(agent!=gameState.getNumAgents()-1):
          scores =[self.minFunction(gameState.generateSuccessor(agent,move),agent+1,depth) for move in moves]
          
        else:
          scores =[self.maxFunction(gameState.generateSuccessor(agent,move),(depth-1))[0] for move in moves]
          
        minScore=min(scores)
        worstIndices = [index for index in range(len(scores)) if scores[index] == minScore]
        chosenIndex = worstIndices[0]
        return minScore, moves[chosenIndex]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        bestScore,bestMove=self.maxFunction(gameState,self.depth,-float('inf'),float('inf'))
        return bestMove
    def maxFunction(self,gameState,depth,alpha,beta):
        if depth==0 or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState), "noMove"

        bestScore,bestMove = (-float('inf'),None)
        moves=gameState.getLegalActions()

        for move in moves:
          score = self.minFunction(gameState.generateSuccessor(self.index,move),1,depth,alpha,beta)[0]
          if score > bestScore:
            bestScore = score
            bestMove = move
          if bestScore > beta:
            return bestScore,bestMove
          else:
            alpha = max(bestScore,alpha)
        return bestScore,bestMove
    def minFunction(self,gameState,agent, depth, alpha, beta):  
        if depth==0 or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState), "noMove"
        moves=gameState.getLegalActions(agent) #get legal actions.
        worstScore,worstMove = (float('inf'),None)

        if(agent!=gameState.getNumAgents()-1):
          for move in moves:
            score = self.minFunction(gameState.generateSuccessor(agent,move),agent+1,depth,alpha,beta)[0]
            if score < worstScore:
              worstScore = score
              worstMove = move
            if worstScore < alpha:
              return worstScore,worstMove
            else:
              beta = min(worstScore,beta)
          return worstScore,worstMove        
        else:
          for move in moves:
            score = self.maxFunction(gameState.generateSuccessor(agent,move),depth-1,alpha,beta)[0]
            if score < worstScore:
              worstScore = score
              worstMove = move
            if worstScore < alpha:
              return worstScore,worstMove
            else:
              beta = min(worstScore,beta)
          return worstScore,worstMove
        

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
        return self.getActionHelper(gameState, self.depth, 0)[1]

    def getActionHelper(self, gameState, depth, agentIndex):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            eval_result = self.evaluationFunction(gameState)
            return (eval_result, '')
        else:
            if agentIndex == gameState.getNumAgents() - 1:
                depth -= 1
            if agentIndex == 0:
                maxAlpha = -float('inf')
            else:
                maxAlpha = 0
            maxAction = ''
            nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()
            actions = gameState.getLegalActions(agentIndex)
            for action in actions:
                result = self.getActionHelper(gameState.generateSuccessor(agentIndex, action), depth, nextAgentIndex)
                if agentIndex == 0:
                    if result[0] > maxAlpha:
                        maxAlpha = result[0]
                        maxAction = action
                else:
                    maxAlpha += 1.0/len(actions) * result[0]
                    maxAction = action
            return (maxAlpha, maxAction)
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # evalNum = 0
    # pacmanPosition = currentGameState.getPacmanPosition()
    # foodPositions = currentGameState.getFood().asList()
    # minDistance = float('inf')
    # for foodPosition in foodPositions:
    #     foodDistance = util.manhattanDistance(pacmanPosition, foodPosition)
    #     if foodDistance < minDistance:
    #         minDistance = foodDistance
    # evalNum += minDistance
    # evalNum += 1000*currentGameState.getNumFood()
    # evalNum += 10*len(currentGameState.getCapsules())
    # ghostPositions = currentGameState.getGhostPositions()
    # for ghostPosition in ghostPositions:
    #     ghostDistance = util.manhattanDistance(pacmanPosition, ghostPosition)
    #     if ghostDistance < 2:
    #         evalNum = 9999999999999999
    # evalNum -= 10*currentGameState.getScore()
    # return evalNum*(-1)
    
    pacmanPos = currentGameState.getPacmanPosition()
    foodPos = currentGameState.getFood().asList()
    ghostState = currentGameState.getGhostStates()

    "*** YOUR CODE HERE ***"
    totalScore=0
    for ghost in ghostState:
      d=manhattanDistance(ghost.getPosition(), pacmanPos)
      if(d<=1):
        if(ghost.scaredTimer!=0):
          totalScore+=2000
        else:
          totalScore-=20000000
      elif (d <= 2) and (ghost.scaredTimer==0):
        totalScore-=1000/(d*d*d)
    nearCapsule = float('inf')
    for capsule in currentGameState.getCapsules():
      totalScore -= 1000
      d=manhattanDistance(capsule, pacmanPos)
      if (d< nearCapsule):
        nearCapsule = d
    if (nearCapsule <= 1):
      totalScore += 100
    nearFood = float('inf')
    for food in foodPos:
      totalScore -= 100
      d=manhattanDistance(food,pacmanPos)
      if (d<nearFood):
        nearFood = d
    if (len(foodPos)):
      totalScore -= nearFood
    return totalScore+10*currentGameState.getScore()

# Abbreviation
better = betterEvaluationFunction

