# myTeam.py
# ---------
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


from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'Agent1', second = 'Agent2'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

# The maximum number of food carrying before deposit
MAX_CAPACITY = 4

class AttackAgent(CaptureAgent):

  def registerInitialState(self, gameState):
    CaptureAgent.registerInitialState(self, gameState)
    self.carrying = 0
    self.current_target = None
    self.position = gameState.getAgentPosition(self.index)
    self.boundary = self.getBoundary(gameState)
    self.height = gameState.data.layout.height
    self.width = gameState.data.layout.width

  def getClosestPos(self, gameState, pos_list):
    min_length = 9999
    min_pos = None
    my_local_state = gameState.getAgentState(self.index)
    my_pos = my_local_state.getPosition()
    for pos in pos_list:
      temp_length = self.getMazeDistance(my_pos, pos)
      if temp_length < min_length:
        min_length = temp_length
        min_pos = pos
    return min_pos

  def getBoundary(self, gameState):
    boundary_location = []
    height = gameState.data.layout.height
    width = gameState.data.layout.width
    for i in range(height):
      if self.red:
        j = int(width / 2) - 1
      else:
        j = int(width / 2)
      if not gameState.hasWall(j, i):
        boundary_location.append((j, i))
    return boundary_location

  def aStarSearch(self, problem):
    """Search the node that has the lowest combined cost and heuristic first."""

    from util import PriorityQueue
    myPQ = util.PriorityQueue()
    startState = problem.getStartState()
    # print(f"start states {startState}")
    startNode = (startState, '', 0, [])
    heuristic = problem._manhattanDistance
    myPQ.push(startNode, heuristic(startState))
    visited = set()
    best_g = dict()
    while not myPQ.isEmpty():
      node = myPQ.pop()
      state, action, cost, path = node
      # print(cost)
      # print(f"visited list is {visited}")
      # print(f"best_g list is {best_g}")
      if (not state in visited) or cost < best_g.get(str(state)):
        visited.add(state)
        best_g[str(state)] = cost
        if problem.isGoalState(state):
          path = path + [(state, action)]
          actions = [action[1] for action in path]
          del actions[0]
          return actions
        for succ in problem.getSuccessors(state):
          succState, succAction, succCost = succ
          newNode = (succState, succAction, cost + succCost, path + [(node, action)])
          myPQ.push(newNode, heuristic(succState) + cost + succCost)
    return []

  """
  Check whether the agent is on the home side (i.e. blue->right, red->left)
  Return True if the agent is on the home side (not Pacman), False otherwise
  """
  def onHomeSide(self, gameState, index):
    return not gameState.getAgentState(index).isPacman

  """
  Calculate the adjacent points for a given point (x, y)
  """
  def get_adjacent_points(self, x, y):
    x = int(x)
    y= int(y)

    first_layer = [
      (x, y),
      (x - 1, y),
      (x + 1, y),
      (x, y - 1),
      (x, y + 1),
      (x - 1, y - 1),
      (x + 1, y - 1),
      (x - 1, y + 1),
      (x + 1, y + 1)
    ]

    second_layer = [
      (x - 2, y),
      (x + 2, y),
      (x, y - 2),
      (x, y + 2),
      (x - 1, y - 2),
      (x + 1, y - 2),
      (x - 1, y + 2),
      (x + 1, y + 2),
      (x - 2, y - 1),
      (x + 2, y - 1),
      (x - 2, y + 1),
      (x + 2, y + 1),
      (x - 2, y - 2),
      (x + 2, y - 2),
      (x - 2, y + 2),
      (x + 2, y + 2)
    ]

    third_layer = []
    for i in range(-3, 4):
      for j in range(-3, 4):
        if abs(i) == 3 or abs(j) == 3:
          third_layer.append((x + i, y + j))

    return first_layer + second_layer + third_layer

  def chooseAction(self, gameState):

    # If agent is on the opponent side
    if not self.onHomeSide(gameState, self.index):
      # Iterate over the opponent indices and record the scared timers
      opponent_indices = self.getOpponents(gameState)

      # Record close opponent with observable position
      close_opponent = []
      for opponent_index in opponent_indices:
        if self.onHomeSide(gameState, opponent_index) and gameState.getAgentPosition(opponent_index) != None:
          close_opponent.append(opponent_index)

      if len(close_opponent) >= 1:
        # If there is at least one close opponent
        li_scaredTimer = []
        for opponent_index in close_opponent:
          li_scaredTimer.append(gameState.getAgentState(opponent_index).scaredTimer)
        # Set the remaining scared time for pacman as the minimum scared timer of the close opponents
        remaining_scared_time = min(li_scaredTimer)

      else:
        # If there is no close opponent
        li_scaredTimer = []
        for opponent_index in opponent_indices:
          li_scaredTimer.append(gameState.getAgentState(opponent_index).scaredTimer)
        # Set the remaining scared time for pacman as the maximum scared timer in the list
        remaining_scared_time = max(li_scaredTimer)

      # Record three layers of positions surrounding the opponent
      avoid_pos = []
      avoid_posL2 = []
      avoid_posL3 = []

      # If the remaining scared time is less than 15
      if remaining_scared_time <= 15:
        # Iterate over the opponent indices and record the avoid positions in a list
        for opponent_index in opponent_indices:
          if self.onHomeSide(gameState, opponent_index) and gameState.getAgentPosition(opponent_index) != None:
            # If the opponent is on enemy side and it is observable to Pacman -> append avoid positions
            x, y = gameState.getAgentPosition(opponent_index)
            for (x, y) in self.get_adjacent_points(int(x), int(y)):

              if x >= 0 and x < self.width and y >= 0 and y < self.height:
                # If the position is within the map and not a wall
                if not gameState.hasWall(x, y):
                  # Calculate the distance to opponent position
                  risk_distance = self.getMazeDistance(gameState.getAgentPosition(opponent_index), (x, y))
                  if risk_distance <= 1:
                    # Add to first layer
                    avoid_pos.append((x, y))
                  elif risk_distance == 2:
                    # Add to second layer
                    avoid_posL2.append((x, y))
                  elif risk_distance == 3:
                    # Add to third layer
                    avoid_posL3.append((x, y))

        if not self.current_target == None:
          # If agent already have a goal
          if (gameState.data.timeleft)/4 <= 10:
            # If the time left is less than 10 -> reach to the closest boundary to deposit the food
            self.current_target = self.getClosestPos(gameState, self.boundary)
          else:
            pass

        elif self.carrying >= MAX_CAPACITY or len(self.getFood(gameState).asList()) <= 2 or (gameState.data.timeleft)/4 <= 10:
          # If agent got all the food it needed or the time left is less than 10
          # It will reach to the closest boundary with A* search (manhattanDistance as heuristic) to deposit the food
          self.current_target = self.getClosestPos(gameState, self.boundary)

        else:
          # Retrieve the capsule and food position
          capsule_pos = self.getCapsules(gameState)
          foodGrid = self.getFood(gameState)
          if len(capsule_pos) >= 1:
            # If there is at least one capsule -> find the next closest capsule
            self.current_target = self.getClosestPos(gameState, capsule_pos)
          else:
            # Find the next closest food
            self.current_target = self.getClosestPos(gameState, foodGrid.asList())

      # If the remaining scared time is larger than 15
      else:
        if not self.current_target == None:
          # If agent already have a goal
          if (gameState.data.timeleft)/4 <= 10:
            # If the time left is less than 10 -> reach to the closest boundary to deposit the food
            self.current_target = self.getClosestPos(gameState, self.boundary)
          else:
            pass

        # If agent does not have a target
        else:
          if len(self.getFood(gameState).asList()) <= 2 or (gameState.data.timeleft)/4 <= 10:
            # If agent got all the food it needed or the time left is less than 10
            # It will reach to the closest boundary with A* search (manhattanDistance as heuristic) to deposit the food
            self.current_target = self.getClosestPos(gameState, self.boundary)
          else:
            # Find the next closest food
            foodGrid = self.getFood(gameState)
            self.current_target = self.getClosestPos(gameState, foodGrid.asList())

      # Configure the problem with avoid positions
      problem = PositionSearchProblemAvoid(gameState, self.current_target, self.index, avoid_pos, avoid_posL2, avoid_posL3)

    # If agent is on home side
    else:
      opponent_indices = self.getOpponents(gameState)

      # Check if there is a nearby opponent on the boundary
      # If there is no observable opponent -> 0
      # Otherwise detect_opponent -> 1
      detect_opponent = 0
      if self.position in self.boundary:
        for opponent_index in opponent_indices:
          if self.onHomeSide(gameState, opponent_index) and gameState.getAgentPosition(opponent_index) != None:
            # If the opponent is on enemy side and it is observable to Pacman
            if self.getMazeDistance(self.position, gameState.getAgentPosition(opponent_index)) <= 4:
              # Activate detect_opponent to 1 and break
              detect_opponent = 1
              break

      if detect_opponent == 0:
        if not self.current_target == None:
          # If agent already have a goal
          pass
        else:
          # Find the next closest food
          foodGrid = self.getFood(gameState)
          self.current_target = self.getClosestPos(gameState, foodGrid.asList())

      elif detect_opponent == 1:
        # Find another position to enter enemy side
        other_boundary = []
        for pos in self.boundary:
          if pos != self.position and self.getMazeDistance(self.position, pos) >= 4:
            other_boundary.append(pos)
        self.current_target = random.choice(other_boundary)

      # Record three layers of positions surrounding the opponent
      avoid_pos = []
      avoid_posL2 = []
      avoid_posL3 = []

      # If the opponent has eaten a capsule and activate the scared timer
      if gameState.getAgentState(self.index).scaredTimer > 0:
        # Iterate over the opponent indices and record the avoid positions in a list
        opponent_indices = self.getOpponents(gameState)
        for opponent_index in opponent_indices:
          if not self.onHomeSide(gameState, opponent_index) and gameState.getAgentPosition(opponent_index) != None:
            # If the opponent is on our side and it is observable to Pacman -> append avoid positions
            x, y = gameState.getAgentPosition(opponent_index)
            for (x, y) in self.get_adjacent_points(int(x), int(y)):

              if x >= 0 and x < self.width and y >= 0 and y < self.height:
                # If the position is within the map and not a wall
                if not gameState.hasWall(x, y):
                  # Calculate the distance to opponent position
                  risk_distance = self.getMazeDistance(gameState.getAgentPosition(opponent_index), (x, y))
                  if risk_distance <= 1:
                    # Add to first layer
                    avoid_pos.append((x, y))
                  elif risk_distance == 2:
                    # Add to second layer
                    avoid_posL2.append((x, y))
                  elif risk_distance == 3:
                    # Add to third layer
                    avoid_posL3.append((x, y))

      # Configure the problem with avoid positions
      problem = PositionSearchProblemAvoid(gameState, self.current_target, self.index, avoid_pos, avoid_posL2, avoid_posL3)

    path = self.aStarSearch(problem)

    if path == []:
      actions = gameState.getLegalActions(self.index)
      return random.choice(actions)
    else:
      action = path[0]
      dx, dy = game.Actions.directionToVector(action)
      x, y = gameState.getAgentState(self.index).getPosition()
      new_x, new_y = int(x + dx), int(y + dy)
      if (new_x, new_y) == self.current_target:
        self.current_target = None
      if self.getFood(gameState)[new_x][new_y]:
        self.carrying += 1
      elif (new_x, new_y) in self.boundary:
        self.carrying = 0
      return path[0]


# A list that records the different versions of foodGrid
foodGrid_record = []
class DefendAgent(CaptureAgent):

  def registerInitialState(self, gameState):
    CaptureAgent.registerInitialState(self, gameState)
    self.carrying = 0
    self.current_target = None
    self.position = gameState.getAgentPosition(self.index)
    self.boundary = self.getBoundary(gameState)
    self.height = gameState.data.layout.height
    self.width = gameState.data.layout.width

  def getClosestPos(self, gameState, pos_list):
    min_length = 9999
    min_pos = None
    my_local_state = gameState.getAgentState(self.index)
    my_pos = my_local_state.getPosition()
    for pos in pos_list:
      temp_length = self.getMazeDistance(my_pos, pos)
      if temp_length < min_length:
        min_length = temp_length
        min_pos = pos
    return min_pos

  def getBoundary(self, gameState):
    boundary_location = []
    height = gameState.data.layout.height
    width = gameState.data.layout.width
    for i in range(height):
      if self.red:
        j = int(width / 2) - 1
      else:
        j = int(width / 2)
      if not gameState.hasWall(j, i):
        boundary_location.append((j, i))
    return boundary_location

  def aStarSearch(self, problem):
    """Search the node that has the lowest combined cost and heuristic first."""

    from util import PriorityQueue
    myPQ = util.PriorityQueue()
    startState = problem.getStartState()
    # print(f"start states {startState}")
    startNode = (startState, '', 0, [])
    heuristic = problem._manhattanDistance
    myPQ.push(startNode, heuristic(startState))
    visited = set()
    best_g = dict()
    while not myPQ.isEmpty():
      node = myPQ.pop()
      state, action, cost, path = node
      # print(cost)
      # print(f"visited list is {visited}")
      # print(f"best_g list is {best_g}")
      if (not state in visited) or cost < best_g.get(str(state)):
        visited.add(state)
        best_g[str(state)] = cost
        if problem.isGoalState(state):
          path = path + [(state, action)]
          actions = [action[1] for action in path]
          del actions[0]
          return actions
        for succ in problem.getSuccessors(state):
          succState, succAction, succCost = succ
          newNode = (succState, succAction, cost + succCost, path + [(node, action)])
          myPQ.push(newNode, heuristic(succState) + cost + succCost)
    return []

  """
  Check whether the agent is on the home side (i.e. blue->right, red->left)
  Return True if the agent is on the home side (not Pacman), False otherwise
  """
  def onHomeSide(self, gameState, index):
    return not gameState.getAgentState(index).isPacman

  """
  Calculate the adjacent points for a given point (x, y)
  """
  def get_adjacent_points(self, x, y):
    x = int(x)
    y = int(y)

    first_layer = [
      (x, y),
      (x - 1, y),
      (x + 1, y),
      (x, y - 1),
      (x, y + 1),
      (x - 1, y - 1),
      (x + 1, y - 1),
      (x - 1, y + 1),
      (x + 1, y + 1)
    ]

    second_layer = [
      (x - 2, y),
      (x + 2, y),
      (x, y - 2),
      (x, y + 2),
      (x - 1, y - 2),
      (x + 1, y - 2),
      (x - 1, y + 2),
      (x + 1, y + 2),
      (x - 2, y - 1),
      (x + 2, y - 1),
      (x - 2, y + 1),
      (x + 2, y + 1),
      (x - 2, y - 2),
      (x + 2, y - 2),
      (x - 2, y + 2),
      (x + 2, y + 2)
    ]

    third_layer = []
    for i in range(-3, 4):
      for j in range(-3, 4):
        if abs(i) == 3 or abs(j) == 3:
          third_layer.append((x + i, y + j))

    return first_layer + second_layer + third_layer

  def getFurthestPos(self, gameState, pos_list):
    max_length = -1
    max_pos = None
    my_local_state = gameState.getAgentState(self.index)
    my_pos = my_local_state.getPosition()
    for pos in pos_list:
      temp_length = self.getMazeDistance(my_pos,pos)
      if temp_length > max_length:
        max_length = temp_length
        max_pos = pos
    return max_pos

  def chooseAction(self, gameState):

    # Initiate the list of foodGrid_record with the initial foodGrid
    if len(foodGrid_record) == 0:
      foodGrid_record.append(self.getFoodYouAreDefending(gameState).asList())

    # Iterate over the opponent indices and record the target positions in a list
    opponent_indices = self.getOpponents(gameState)
    target_pos = []
    for opponent_index in opponent_indices:
      if not self.onHomeSide(gameState, opponent_index) and gameState.getAgentPosition(opponent_index) != None:
        # If the opponent is on our side and it is observable to Pacman -> append opponent's position
        x, y = gameState.getAgentPosition(opponent_index)
        opponent_pos = (int(x), int(y))
        target_pos.append(opponent_pos)

    # Check whether the remaining_food is equal to the latest version of foodGrid in foodGrid_record
    remaining_food = self.getFoodYouAreDefending(gameState).asList()
    if set(foodGrid_record[-1]) != set(remaining_food):
      # If two sets are not equivalent -> a food has been eaten by the opponent
      # find the difference elements as target_food
      target_food = list(set(foodGrid_record[-1]) - set(remaining_food))

      # Iterate over the list of target_food and append the position to target_pos
      for food in target_food:
        target_pos.append(food)

      # Update the latest foodGrid
      foodGrid_record.append(remaining_food)

    if len(target_pos) >= 1:
      # If there is at least one target position -> move to the closest target position
      self.current_target = self.getClosestPos(gameState, target_pos)
    elif not self.current_target == None:
      # If agent already have a goal
      pass
    else:
      # If agent does not have a goal
      # It will find the furthest food to defend
      foodGrid = self.getFoodYouAreDefending(gameState)
      self.current_target = self.getFurthestPos(gameState, foodGrid.asList())

    # Record three layers of positions surrounding the opponent
    avoid_pos = []
    avoid_posL2 = []
    avoid_posL3 = []

    # If the opponent has not eaten a capsule
    if gameState.getAgentState(self.index).scaredTimer == 0:
      # Avoid position = boundary
      # Do not cross over the boundary to enemy territory, always defend on the home side
      avoid_pos = self.getBoundary(gameState)

    # If the opponent has eaten a capsule and activate the scared timer
    else:
      # Iterate over the opponent indices and record the avoid positions in a list
      opponent_indices = self.getOpponents(gameState)
      for opponent_index in opponent_indices:
        if not self.onHomeSide(gameState, opponent_index) and gameState.getAgentPosition(opponent_index) != None:
          # If the opponent is on our side and it is observable to Pacman -> append avoid positions
          x, y = gameState.getAgentPosition(opponent_index)
          for (x, y) in self.get_adjacent_points(int(x), int(y)):

            if x >= 0 and x < self.width and y >= 0 and y < self.height:
              # If the position is within the map and not a wall
              if not gameState.hasWall(x, y):
                # Calculate the distance to opponent position
                risk_distance = self.getMazeDistance(gameState.getAgentPosition(opponent_index), (x, y))
                if risk_distance <= 1:
                  # Add to first layer
                  avoid_pos.append((x, y))
                if gameState.getAgentState(self.index).scaredTimer > 40:
                  # If the scared time is larger than 40 -> maintain more distance
                  # Otherwise, only append avoid_pos (first layer of positions surrounding the opponent)
                  if risk_distance == 2:
                    # Add to second layer
                    avoid_posL2.append((x, y))
                  # elif risk_distance == 3:
                  #   avoid_posL3.append((x, y))

      # Avoid position = boundary + first layer of positions surrounding the opponent
      avoid_pos = avoid_pos + self.getBoundary(gameState)

    # Configure the problem with avoid positions
    problem = PositionSearchProblemAvoid(gameState, self.current_target, self.index, avoid_pos, avoid_posL2, avoid_posL3)

    path = self.aStarSearch(problem)

    if path == []:
      actions = gameState.getLegalActions(self.index)
      return random.choice(actions)
    else:
      action = path[0]
      dx, dy = game.Actions.directionToVector(action)
      x, y = gameState.getAgentState(self.index).getPosition()
      new_x, new_y = int(x + dx), int(y + dy)
      if (new_x, new_y) == self.current_target:
        self.current_target = None
      if self.getFood(gameState)[new_x][new_y]:
        self.carrying += 1
      elif (new_x, new_y) in self.boundary:
        self.carrying = 0
      return path[0]

class PositionSearchProblem:
  """
  It is the ancestor class for all the search problem class.
  A search problem defines the state space, start state, goal test, successor
  function and cost function.  This search problem can be used to find paths
  to a particular point.
  """

  def __init__(self, gameState, goal, agentIndex=0, costFn=lambda x: 1):
    self.walls = gameState.getWalls()
    self.costFn = costFn
    x, y = gameState.getAgentState(agentIndex).getPosition()
    self.startState = int(x), int(y)
    self.goal_pos = goal

  def getStartState(self):
    return self.startState

  def isGoalState(self, state):
    return state == self.goal_pos

  def getSuccessors(self, state):
    successors = []
    for action in [game.Directions.NORTH, game.Directions.SOUTH, game.Directions.EAST, game.Directions.WEST]:
      x, y = state
      dx, dy = game.Actions.directionToVector(action)
      nextx, nexty = int(x + dx), int(y + dy)
      if not self.walls[nextx][nexty]:
        nextState = (nextx, nexty)
        cost = self.costFn(nextState)
        successors.append((nextState, action, cost))
    return successors

  def getCostOfActions(self, actions):
    if actions == None: return 999999
    x, y = self.getStartState()
    cost = 0
    for action in actions:
      # Check figure out the next state and see whether its' legal
      dx, dy = game.Actions.directionToVector(action)
      x, y = int(x + dx), int(y + dy)
      if self.walls[x][y]: return 999999
      cost += self.costFn((x, y))
    return cost

  def _manhattanDistance(self, pos):
    return util.manhattanDistance(pos, self.goal_pos)

"""
Add a list of positions to avoid
1. AttackAgent: observable opponent and surrounding positions
2. DefendAgent: boundary + observable opponent surrounding positions (if opponent consumes a capsule)
"""
class PositionSearchProblemAvoid(PositionSearchProblem):

  def __init__(self, gameState, goal, agentIndex=0, avoidPosition=[], avoidPositionL2=[], avoidPositionL3=[], costFn=lambda x: 1):
    super().__init__(gameState, goal, agentIndex, costFn)
    self.avoidPosition = avoidPosition
    self.avoidPositionLevel2 = avoidPositionL2
    self.avoidPositionLevel3 = avoidPositionL3

  def getSuccessors(self, state):
    successors = []
    for action in [game.Directions.NORTH, game.Directions.SOUTH, game.Directions.EAST, game.Directions.WEST]:
      x, y = state
      dx, dy = game.Actions.directionToVector(action)
      nextx, nexty = int(x + dx), int(y + dy)
      # If the next position is not wall and is not in the list of positions to avoid
      if not self.walls[nextx][nexty] and (nextx, nexty) not in self.avoidPosition:
        nextState = (nextx, nexty)
        cost = self.costFn(nextState)
        successors.append((nextState, action, cost))
    return successors

  def getCostOfActions(self, actions):
    if actions == None: return 999999
    x, y = self.getStartState()
    cost = 0
    for action in actions:
      # Check figure out the next state and see whether its' legal
      dx, dy = game.Actions.directionToVector(action)
      x, y = int(x + dx), int(y + dy)
      # If the position is wall or is in avoid_pos (first layer) -> set cost to 999999
      if self.walls[x][y] or (x, y) in self.avoidPosition: return 999999
      # If the position is in avoid_posL2 (second layer) -> set cost to 1000
      elif (x, y) in self.avoidPositionL2: return 1000
      # If the position is in avoid_posL3 (third layer) -> set cost to 100
      elif (x, y) in self.avoidPositionL3: return 100
      cost += self.costFn((x, y))
    return cost


# Set Agent1 as AttackAgent
class Agent1(AttackAgent):
  pass

# Set Agent2 as DefendAgent
class Agent2(DefendAgent):
  pass
