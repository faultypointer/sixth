import numpy as np
from queue import PriorityQueue

goalState = np.array([1, 2, 3, 4, 5, 6, 7, 8, 0]).reshape(3, 3)
initialState = np.random.permutation(9).reshape(3, 3)

def make_move(state, move):
    i, j = move[0], move[1]
    match move[2]:
        case "up":
            state[i][j], state[i-1][j] = state[i-1][j], state[i][j]
        case "down":
            state[i][j], state[i+1][j] = state[i+1][j], state[i][j]
        case "left":
            state[i][j], state[i][j-1] = state[i][j-1], state[i][j]
        case "right":
            state[i][j], state[i][j+1] = state[i][j+1], state[i][j]

def successors(state):
    successors = []
    indexes = np.where(state==0)
    i, j = indexes[0][0], indexes[1][0]
    if (i > 0):
        up_succ = state.copy()
        make_move(up_succ, (i, j, "up"))
        successors.append(up_succ)
    if (i < 2):
        down_succ = state.copy()
        make_move(down_succ, (i, j, "down"))
        successors.append(down_succ)
    if (j > 0):
        left_succ = state.copy()
        make_move(left_succ, (i, j, "left"))
        successors.append(left_succ)
    if (j < 2):
        right_succ = state.copy()
        make_move(right_succ, (i, j, "right"))
        successors.append(right_succ)

    return successors


def h1_score(state, goalState):
    # counting misplaced 0 too
    return np.sum(state != goalState)

def h_score(state, goalState):
    return h1_score(state, goalState)

def astar(initialState, goalState):
    PQ = PriorityQueue()
    prev = dict()
    visited = set()

    PQ.put((0 + h_score(initialState, goalState), (tuple(initialState.flatten()), 0)))
    prev[tuple(initialState.flatten())] = " "
    while not PQ.empty():
        outStateFScore, (outStateTuple, outStateGScore) = PQ.get()
        outState = np.array(outStateTuple).reshape(initialState.shape)
        visited.add(outStateTuple)
        if np.array_equal(outState, goalState):
            return True, prev, outStateGScore
        for chimeki in successors(outState):
            chimekiTuple = tuple(chimeki.flatten())
            if chimekiTuple not in visited:
                chimekiGScore = outStateGScore + 1
                chimekiFScore = h_score(chimeki, goalState) + chimekiGScore
                PQ.put((chimekiFScore, (chimekiTuple, chimekiGScore)))
                prev[chimekiTuple] = outStateTuple
    return False, prev, math.inf




goalFound, prev, cost = astar(initialState, goalState)
if (goalFound):
    goalState = tuple(goalState.flatten())
    while (goalState != " "):
        print(np.array(goalState).reshape(3, 3), "\n")
        goalState = prev[goalState]
    print("Cost: ", cost)
else:
    print("No path found")
