# Problem Solving

## Key Notes

- Goal formulation, based on the current situation and the agent’s performance measure, is the first step in problem solving.
- Problem formulation is the process of deciding what actions and states to consider, given a goal.
- an agent with several immediate options of unknown value can decide what to do by first examining future actions that eventually lead to states of known value.
- The process of looking for a sequence of actions that reaches the goal is called search.
- formulate, search, execute

### Five Components of Well-defined Problem

- Initial state: the state agent starts in
- Actions: descriptions of possible actions available to agent (given a state)
- Transition Model: description of what each action does.
  - Successor: any state reachable from a given state by a single action.
  - State Space: set of all possible states reachable from initial state by a sequence of action
  - Path: sequence of states in state space connected by a sequence of action
- Goal Test: whether given state is a goal state
- Path Cost: assigns numeric cost to each path

### Example of a simple problem solving agent

```vim
function SIMPLE-PROBLEM-SOLVING-AGENT(percept) returns an action
    persistent: seq, an action sequence, initially empty
                state, some description of the current world state
                goal, a goal, initially null
                problem, a problem formulation
    state ←UPDATE-STATE(state,percept)
    if seq is empty then
        goal ←FORMULATE-GOAL(state)
        problem ←FORMULATE-PROBLEM(state,goal)
        seq ←SEARCH(problem)
        if seq = failure then return a null action
    action ←FIRST(seq)
    seq ←REST(seq)
    return action
```

### Formulating Problems

- The process of removing detail from a representation is called abstraction.
- The abstraction is valid if we can expand any abstract solution into a solution in the more detailed world
