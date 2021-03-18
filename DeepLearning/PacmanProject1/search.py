# search.py
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

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"


    explored = set()
    legacy = {}

    start = problem.getStartState()

    stack = util.Stack()
    parent = (start, (0,0), 1)
    stack.push(parent)

    while not stack.isEmpty():

        parent = stack.pop()
        explored.add(parent)

        if problem.isGoalState(parent[0]):
            
            ret_list = []
            actual = parent
            while actual in legacy.keys():
                ret_list.insert(0, actual[1])
                actual = legacy[actual]
            
            return ret_list

        children = problem.getSuccessors(parent[0])
        for child in children:

            if child[0] not in [exp[0] for exp in explored]:
                stack.push(child)
                legacy[child] = parent

#my way takes less memory but there was a problem with multitarget mazes
#(need of different code in if statement). Worked but bruteforce. Check in github repo
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    import copy

    queue = util.Queue()

    start = [problem.getStartState(), ""]
    queue.push([start])

    visited_state = [start[0]]

    while not queue.isEmpty():
        node = queue.pop()
        end = node[-1]

        if problem.isGoalState(end[0]):
            return [state[1] for state in node[1:]]

        successors = problem.getSuccessors(end[0])
        for succ in successors:
            if succ[0] not in visited_state:
                visited_state.append(succ[0])
                new_node = copy.deepcopy(node)
                new_node.append(succ)
                queue.push(new_node)

    return []


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    import copy

    prio_queue = util.PriorityQueue()

    start_state = problem.getStartState()
    start = (start_state, "", 0)
    prio_queue.push([start], 0)

    visited_state = {start_state: 0}

    while not prio_queue.isEmpty():
        node = prio_queue.pop()
        end = node[-1]

        if end[0] not in visited_state or end[2] <= visited_state[end[0]]:
            if problem.isGoalState(end[0]):
                return [state[1] for state in node[1:]]

            successors = problem.getSuccessors(end[0])
            for succ in successors:
                if succ[0] not in visited_state or (end[2] + succ[2]) < visited_state[succ[0]]:
                    visited_state[succ[0]] = end[2] + succ[2]
                    new_node = copy.deepcopy(node)
                    new_succ = (succ[0], succ[1], end[2] + succ[2])
                    new_node.append(new_succ)
                    prio_queue.push(new_node, end[2] + succ[2])

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

    import copy

    prio_queue = util.PriorityQueue()

    start_state = problem.getStartState()
    start = (start_state, "", (0, heuristic(start_state, problem)))
    prio_queue.push([start], sum(start[2]))

    visited_state = {start_state[0]: sum(start[2])}

    while not prio_queue.isEmpty():
        node = prio_queue.pop()

        if not prio_queue.isEmpty():
            next_node = prio_queue.pop()
            temp = [node, next_node]

            while not prio_queue.isEmpty() and sum(node[-1][2]) == sum(next_node[-1][2]):
                next_node = prio_queue.pop()
                temp.append(next_node)

            same_priority_nodes = temp if sum(node[-1][2]) == sum(next_node[-1][2]) else temp[:-1]

            for n in same_priority_nodes:
                if node[-1][2][0] < n[-1][2][0]:
                    node = n
            
            for n in temp:
                if n != node:
                    prio_queue.push(n, sum(n[-1][2]))

        end = node[-1]

        if end[0] not in visited_state or sum(end[2]) <= visited_state[end[0]]:
            if problem.isGoalState(end[0]):
                return [state[1] for state in node[1:]]

            successors = problem.getSuccessors(end[0])
            for succ in successors:
                m_val = end[2][0] + succ[2]
                h_val = heuristic(succ[0], problem)
                sum_val = m_val + h_val
                if succ[0] not in visited_state or sum_val < visited_state[succ[0]]:
                    visited_state[succ[0]] = sum_val
                    new_node = copy.deepcopy(node)
                    new_succ = (succ[0], succ[1], (m_val, h_val))
                    new_node.append(new_succ)
                    prio_queue.push(new_node, sum_val)

    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
