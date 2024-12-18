# Uninformed Search

- no additional information about states beyond problem defination
- generate successors and determine if a state is goal state or not

## Breadth First Search

- root node is expanded
- then its successors
- then their successors
- **Performance Measure**
  - Time Complexity: $\mathcal{O}(b^d)$
  - Space Complexity: $\mathcal{O}(b^d)$
  - Completeness: It is complete
  - Optimality: is optimal if path cost is non decreasing function of depth of node.

## Depth First Search

- expands the deepest node in current open list
- uses LIFO queue
- **Performance Measure**
  - Time Complexity: $\mathcal{O}(b^d)$
  - Space Complexity: $\mathcal{O}(bd)$
  - Completeness:
    - complete for graph with finite state when avoiding repeated states or redundant path.
    - not complete for tree-search
  - Optimality: is not optimal
  -

## Depth Limited Search

- DFS but
- nodes at depth `l` are treated as if they have no successors; where `l` is predetermined limit
- **Performance Measure**
  - Time Complexity: $\mathcal{O}(b^l)$
  - Space Complexity: $\mathcal{O}(bl)$
  - Completeness: incomplete if $l \lt d$
  - Optimality: not optimal if $l \gt d$
  -

## Iterative Deepening DFS

- gradually increaing the limit `l` on depth limited search from 0, 1 and so-on
