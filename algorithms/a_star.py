import heapq
import itertools
from puzzle.state import State, GOAL_STATE
from puzzle.base_search import BaseSearch
from puzzle.result import SearchResult

class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        # Distância de Manhattan: soma, para cada peça (exceto o espaço vazio),
        # da distância entre sua posição atual e sua posição no objetivo.
        goal_index = {value: idx for idx, value in enumerate(GOAL_STATE)}

        total = 0
        for current_idx, value in enumerate(state.tiles):
            if value == 0:
                continue
            target_idx = goal_index[value]
            cur_row, cur_col = divmod(current_idx, 3)
            tgt_row, tgt_col = divmod(target_idx, 3)
            total += abs(cur_row - tgt_row) + abs(cur_col - tgt_col)

        return total

    def search(self, initial: State) -> SearchResult:
        counter = itertools.count()
        nodes_generated = 1
        nodes_expanded = 0

        frontier = [(self.heuristic(initial), initial.cost, next(counter), initial)]
        best_cost = {initial: initial.cost}
        max_frontier_size = 1

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            _, _, _, current = heapq.heappop(frontier)

            if current.cost > best_cost.get(current, float("inf")):
                continue

            if current.is_goal:
                return SearchResult(
                    solution=current,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=current.cost,
                )

            nodes_expanded += 1

            for child in current.neighbors():
                nodes_generated += 1
                if child.cost < best_cost.get(child, float("inf")):
                    best_cost[child] = child.cost
                    f_score = child.cost + self.heuristic(child)
                    heapq.heappush(frontier, (f_score, child.cost, next(counter), child))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
        )