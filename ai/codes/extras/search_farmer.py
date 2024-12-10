"""
A farmer has a goat, a wolf, and a cabbage on the west side of a river. He wants to get all of his 
animals and his cabbage across the river onto the east side. The farmer has a rowboat, but he only
has enough room for himself and one other thing. The wolf will eat the goat if they are left 
together alone. The goat will eat the cabbage if they are left together alone. How can the farmer
get everything on the east side?

i) Formulate this puzzle as a search.

ii) Solve this problem using search (any method).
Draw the search tree and show the final solution.
"""


from enum import IntEnum
from collections import deque

initial_state = ('w', 'w', 'w', 'w')
final_state = ('e', 'e', 'e', 'e')

class Move(IntEnum):
    F = 0 # farmer
    W = 1 # wolf
    G = 2 # goat
    C = 3 # cabbage

class Solution:
    def is_fail(self, state):
        # if wolf and goat are left alone together
        if (state[Move.W] == state[Move.G] and 
            state[Move.F] != state[Move.W] and
            state[Move.C] != state[Move.W]):
            return True

        # if cababge and goat are left alone together
        if (state[Move.C] == state[Move.G] and 
            state[Move.F] != state[Move.C] and
            state[Move.W] != state[Move.C]):
            return True

        return False

    def successors(self, state): 
        possible_actions = [[Move.F]]
        for i in range(Move.W, Move.C+1):
            if state[Move.F] == state[i]:
                action = [Move.F]
                action.append(Move(i))
                possible_actions.append(action)
        return possible_actions


    def execute_action(self, state, action):
        state = list(state)
        for move in action:
            state[move] = 'e' if state[move] == 'w' else 'w' 
        return tuple(state)

    def search(self, initial_state, final_state):
        self.parents = {}
        self.parents[initial_state] = None
        visited = set()
        qqq = deque()
        qqq.append(initial_state)
        while (len(qqq) != 0):
           current_state = qqq.popleft()
           if current_state == final_state:
               self.path = []
               state = current_state
               while(self.parents[state] != None):
                   # print("state: ", state, "\t parent: ", self.parents[state])
                   # input()
                   self.path.append(str(state))
                   state = self.parents[state]
               self.path.append(str(state))
               self.path = self.path[::-1]
               return True
           visited.add(current_state)
           possible_actions = self.successors(current_state)
           for action in possible_actions:
               next_state = self.execute_action(current_state, action)
               if next_state not in visited and not self.is_fail(next_state):
                   self.parents[next_state] = current_state
                   qqq.append(next_state)
        return False






if __name__ == "__main__":
    solution = Solution()
    if solution.search(initial_state, final_state):
        print("Solution found")
        print(" -> ".join(solution.path))
    else:
        print("Solution Not Found")
