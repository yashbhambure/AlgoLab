"""
Traveling Salesman Problem — LC Branch and Bound (Reduced Cost Matrix)
Solves TSP to optimality using row/column matrix reduction lower bounds and best-first priority queue.
"""
import heapq
from typing import Dict, Any, List, Tuple, Optional
from app.algorithms.base import BaseAlgorithm, ExecutionMetrics, ExecutionStep, AlgorithmExecutionResult


class TravelingSalesmanBranchAndBound(BaseAlgorithm):
    slug = "traveling-salesman-bb"
    name = "Traveling Salesman (LC Branch and Bound)"
    category = "Branch and Bound"
    paradigm = "Branch and Bound"

    time_complexity_best = "O(n^2)"
    time_complexity_average = "O(n^2 2^n)"
    time_complexity_worst = "O(n^2 2^n)"
    space_complexity = "O(n^2 2^n)"
    is_stable = True
    is_in_place = False

    def _parse_input(self, input_data: Any) -> Tuple[int, List[List[float]], List[str]]:
        if isinstance(input_data, dict):
            dist_matrix = input_data.get("distance_matrix", input_data.get("matrix", []))
            city_names = input_data.get("cities", input_data.get("city_names", []))
        elif isinstance(input_data, list):
            dist_matrix = input_data
            city_names = []
        else:
            dist_matrix = [
                [float('inf'), 20, 30, 10, 11],
                [15, float('inf'), 16, 4, 2],
                [3, 5, float('inf'), 2, 4],
                [19, 6, 18, float('inf'), 3],
                [16, 4, 7, 16, float('inf')]
            ]
            city_names = ["A", "B", "C", "D", "E"]

        n = len(dist_matrix)
        # Convert diagonal to infinity
        clean_matrix = []
        for i in range(n):
            row = []
            for j in range(n):
                val = dist_matrix[i][j]
                if i == j or val is None or val == -1 or val == 0:
                    row.append(float('inf'))
                else:
                    row.append(float(val))
            clean_matrix.append(row)

        if not city_names or len(city_names) < n:
            city_names = [f"City {i+1}" for i in range(n)]

        return n, clean_matrix, city_names

    def _reduce_matrix(self, matrix: List[List[float]]) -> Tuple[List[List[float]], float]:
        """Reduces rows and columns of matrix and returns (reduced_matrix, reduction_cost)."""
        n = len(matrix)
        reduced = [row[:] for row in matrix]
        cost = 0.0

        # Row reduction
        for i in range(n):
            row_min = float('inf')
            for j in range(n):
                if reduced[i][j] < row_min:
                    row_min = reduced[i][j]
            if row_min != float('inf') and row_min > 0:
                cost += row_min
                for j in range(n):
                    if reduced[i][j] != float('inf'):
                        reduced[i][j] -= row_min

        # Column reduction
        for j in range(n):
            col_min = float('inf')
            for i in range(n):
                if reduced[i][j] < col_min:
                    col_min = reduced[i][j]
            if col_min != float('inf') and col_min > 0:
                cost += col_min
                for i in range(n):
                    if reduced[i][j] != float('inf'):
                        reduced[i][j] -= col_min

        return reduced, cost

    def run(self, input_data: Any) -> Dict[str, Any]:
        n, dist, cities = self._parse_input(input_data)
        if n <= 1:
            return {"min_cost": 0.0, "tour": [0, 0], "city_names": cities, "num_cities": n}

        # 1. Reduce root matrix
        root_matrix, root_cost = self._reduce_matrix(dist)

        # Priority Queue: (lower_bound, level, curr_city, path_tuple, matrix, counter)
        heap = []
        counter = 0
        heapq.heappush(heap, (root_cost, 0, 0, (0,), root_matrix, counter))
        counter += 1

        best_cost = float('inf')
        best_tour: Tuple[int, ...] = ()
        nodes_explored = 0
        nodes_pruned = 0

        while heap:
            bound, level, curr_u, path, mat, _ = heapq.heappop(heap)
            nodes_explored += 1

            if bound >= best_cost:
                nodes_pruned += 1
                continue

            if level == n - 1:
                # Close the tour back to node 0
                return_cost = mat[curr_u][0]
                total_tour_cost = bound + (return_cost if return_cost != float('inf') else 0)
                if total_tour_cost < best_cost:
                    best_cost = total_tour_cost
                    best_tour = path + (0,)
                continue

            # Branch to each unvisited city v
            for v in range(n):
                if v in path or mat[curr_u][v] == float('inf'):
                    continue

                edge_cost = mat[curr_u][v]
                child_mat = [r[:] for r in mat]

                # Invalidate row u and column v
                for k in range(n):
                    child_mat[curr_u][k] = float('inf')
                    child_mat[k][v] = float('inf')
                child_mat[v][0] = float('inf')  # Prevent early return

                child_reduced, red_cost = self._reduce_matrix(child_mat)
                child_bound = bound + edge_cost + red_cost

                if child_bound < best_cost:
                    heapq.heappush(heap, (child_bound, level + 1, v, path + (v,), child_reduced, counter))
                    counter += 1
                else:
                    nodes_pruned += 1

        tour_city_labels = [cities[idx] for idx in best_tour]

        return {
            "min_cost": round(best_cost, 4),
            "tour": list(best_tour),
            "tour_city_labels": tour_city_labels,
            "num_cities": n,
            "nodes_explored": nodes_explored,
            "nodes_pruned": nodes_pruned,
            "total_nodes_generated": counter
        }

    def run_instrumented(self, input_data: Any, max_steps: int = 500) -> AlgorithmExecutionResult:
        n, dist, cities = self._parse_input(input_data)
        metrics = ExecutionMetrics()
        steps: List[ExecutionStep] = []
        step_id = [0]

        if n <= 1:
            return AlgorithmExecutionResult(
                algorithm_slug=self.slug,
                output={"min_cost": 0.0, "tour": [0, 0], "city_names": cities, "num_cities": n},
                metrics=metrics,
                steps=steps
            )

        root_matrix, root_cost = self._reduce_matrix(dist)

        steps.append(ExecutionStep(
            step_id=step_id[0],
            action="init_reduction",
            state_snapshot={"root_bound": root_cost, "cities": cities},
            description=f"Initialized LC Branch & Bound TSP on {n} cities. Initial Reduced Cost Matrix Lower Bound = {root_cost:.2f}."
        ))
        step_id[0] += 1

        heap = []
        counter = 0
        heapq.heappush(heap, (root_cost, 0, 0, (0,), root_matrix, counter))
        counter += 1

        best_cost = float('inf')
        best_tour: Tuple[int, ...] = ()
        nodes_explored = 0
        nodes_pruned = 0

        while heap:
            bound, level, curr_u, path, mat, _ = heapq.heappop(heap)
            nodes_explored += 1
            metrics.operations += 1
            metrics.comparisons += 1

            if bound >= best_cost:
                nodes_pruned += 1
                if len(steps) < max_steps:
                    steps.append(ExecutionStep(
                        step_id=step_id[0],
                        action="prune_branch",
                        values=[bound, best_cost],
                        state_snapshot={"bound": bound, "best_cost": best_cost},
                        description=f"Pruned TSP branch from {cities[curr_u]}: Lower Bound ({bound:.2f}) >= Current Best Tour ({best_cost:.2f})."
                    ))
                    step_id[0] += 1
                continue

            if level == n - 1:
                return_cost = mat[curr_u][0]
                total_tour_cost = bound + (return_cost if return_cost != float('inf') else 0)
                if total_tour_cost < best_cost:
                    best_cost = total_tour_cost
                    best_tour = path + (0,)
                    if len(steps) < max_steps:
                        steps.append(ExecutionStep(
                            step_id=step_id[0],
                            action="tour_improved",
                            values=[best_cost],
                            state_snapshot={"tour": [cities[x] for x in best_tour], "cost": best_cost},
                            description=f"Complete tour found: {' -> '.join([cities[x] for x in best_tour])} with cost {best_cost:.2f}!",
                            highlight_line=5
                        ))
                        step_id[0] += 1
                continue

            for v in range(n):
                if v in path or mat[curr_u][v] == float('inf'):
                    continue

                edge_cost = mat[curr_u][v]
                child_mat = [r[:] for r in mat]

                for k in range(n):
                    child_mat[curr_u][k] = float('inf')
                    child_mat[k][v] = float('inf')
                child_mat[v][0] = float('inf')

                child_reduced, red_cost = self._reduce_matrix(child_mat)
                child_bound = bound + edge_cost + red_cost

                if child_bound < best_cost:
                    heapq.heappush(heap, (child_bound, level + 1, v, path + (v,), child_reduced, counter))
                    counter += 1
                    if len(steps) < max_steps:
                        steps.append(ExecutionStep(
                            step_id=step_id[0],
                            action="branch_expand",
                            indices=[curr_u, v],
                            values=[edge_cost, child_bound],
                            state_snapshot={"path": [cities[x] for x in path] + [cities[v]], "bound": child_bound},
                            description=f"LC Branch ({cities[curr_u]} -> {cities[v]}): EdgeCost={edge_cost:.1f}, ReductionCost={red_cost:.1f} -> Lower Bound={child_bound:.2f}."
                        ))
                        step_id[0] += 1
                else:
                    nodes_pruned += 1

        tour_city_labels = [cities[idx] for idx in best_tour]

        steps.append(ExecutionStep(
            step_id=step_id[0],
            action="optimal_tsp_solved",
            state_snapshot={"tour": tour_city_labels, "min_cost": best_cost},
            description=f"Optimal TSP Branch & Bound tour solved: {' -> '.join(tour_city_labels)} with exact minimum cost {best_cost:.2f}."
        ))
        step_id[0] += 1

        out = {
            "min_cost": round(best_cost, 4),
            "tour": list(best_tour),
            "tour_city_labels": tour_city_labels,
            "num_cities": n,
            "nodes_explored": nodes_explored,
            "nodes_pruned": nodes_pruned,
            "total_nodes_generated": counter
        }
        return AlgorithmExecutionResult(
            algorithm_slug=self.slug,
            output=out,
            metrics=metrics,
            steps=steps
        )
