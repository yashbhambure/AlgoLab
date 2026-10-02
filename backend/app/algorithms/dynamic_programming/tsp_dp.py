"""
Traveling Salesman Problem (Held-Karp Dynamic Programming O(n^2 2^n))
Computes exact optimal Hamiltonian tour using bitmask DP state-space.
"""
from typing import Dict, Any, List, Tuple, Optional
from app.algorithms.base import BaseAlgorithm, ExecutionMetrics, ExecutionStep, AlgorithmExecutionResult


class TravelingSalesmanDP(BaseAlgorithm):
    slug = "traveling-salesman-dp"
    name = "Traveling Salesman (Held-Karp DP)"
    category = "Dynamic Programming"
    paradigm = "Dynamic Programming"

    time_complexity_best = "O(n^2 2^n)"
    time_complexity_average = "O(n^2 2^n)"
    time_complexity_worst = "O(n^2 2^n)"
    space_complexity = "O(n 2^n)"
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
                [0, 10, 15, 20],
                [10, 0, 35, 25],
                [15, 35, 0, 30],
                [20, 25, 30, 0]
            ]
            city_names = ["City 0", "City 1", "City 2", "City 3"]

        n = len(dist_matrix)
        if not city_names or len(city_names) < n:
            city_names = [f"City {i}" for i in range(n)]

        return n, dist_matrix, city_names

    def run(self, input_data: Any) -> Dict[str, Any]:
        n, dist, cities = self._parse_input(input_data)
        if n <= 1:
            return {"min_cost": 0.0, "tour": [0, 0], "city_names": cities, "num_cities": n}

        # memo[mask][u] = min cost to visit subset `mask` ending at vertex `u`
        # parent[mask][u] = predecessor vertex
        memo: Dict[Tuple[int, int], float] = {}
        parent: Dict[Tuple[int, int], Optional[int]] = {}

        # Base case: from start node 0 to each node j
        for j in range(1, n):
            mask = (1 << 0) | (1 << j)
            memo[(mask, j)] = float(dist[0][j])
            parent[(mask, j)] = 0

        # Subsets of increasing size
        for size in range(3, n + 1):
            for mask in range(1 << n):
                # Must contain start city 0 and have exact size
                if not (mask & (1 << 0)) or bin(mask).count("1") != size:
                    continue

                for j in range(1, n):
                    if not (mask & (1 << j)):
                        continue
                    prev_mask = mask ^ (1 << j)
                    best_cost = float('inf')
                    best_p = None

                    for i in range(1, n):
                        if i == j or not (prev_mask & (1 << i)):
                            continue
                        if (prev_mask, i) in memo:
                            cost = memo[(prev_mask, i)] + dist[i][j]
                            if cost < best_cost:
                                best_cost = cost
                                best_p = i

                    if best_p is not None:
                        memo[(mask, j)] = best_cost
                        parent[(mask, j)] = best_p

        # Find min cost to return to city 0 from full mask
        full_mask = (1 << n) - 1
        optimal_cost = float('inf')
        last_city = None

        for j in range(1, n):
            if (full_mask, j) in memo:
                total_cost = memo[(full_mask, j)] + dist[j][0]
                if total_cost < optimal_cost:
                    optimal_cost = total_cost
                    last_city = j

        # Reconstruct tour
        tour = [0]
        curr_mask = full_mask
        curr_city = last_city

        rev_path = []
        while curr_city is not None and curr_city != 0:
            rev_path.append(curr_city)
            prev_city = parent.get((curr_mask, curr_city))
            curr_mask = curr_mask ^ (1 << curr_city)
            curr_city = prev_city

        tour.extend(reversed(rev_path))
        tour.append(0)

        tour_city_labels = [cities[idx] for idx in tour]

        return {
            "min_cost": round(optimal_cost, 4),
            "tour": tour,
            "tour_city_labels": tour_city_labels,
            "num_cities": n,
            "states_computed": len(memo)
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

        steps.append(ExecutionStep(
            step_id=step_id[0],
            action="init",
            state_snapshot={"num_cities": n, "cities": cities},
            description=f"Initialized Held-Karp TSP DP on {n} cities ({cities})."
        ))
        step_id[0] += 1

        memo: Dict[Tuple[int, int], float] = {}
        parent: Dict[Tuple[int, int], Optional[int]] = {}

        # Base case
        for j in range(1, n):
            mask = (1 << 0) | (1 << j)
            cost = float(dist[0][j])
            memo[(mask, j)] = cost
            parent[(mask, j)] = 0
            metrics.operations += 1

            if len(steps) < max_steps:
                steps.append(ExecutionStep(
                    step_id=step_id[0],
                    action="base_case",
                    indices=[0, j],
                    values=[cost],
                    state_snapshot={"mask": bin(mask), "last": j, "cost": cost},
                    description=f"Base DP state: City 0 -> {cities[j]} cost = {cost}."
                ))
                step_id[0] += 1

        # DP transitions
        for size in range(3, n + 1):
            for mask in range(1 << n):
                if not (mask & (1 << 0)) or bin(mask).count("1") != size:
                    continue

                for j in range(1, n):
                    if not (mask & (1 << j)):
                        continue
                    prev_mask = mask ^ (1 << j)
                    best_cost = float('inf')
                    best_p = None

                    for i in range(1, n):
                        if i == j or not (prev_mask & (1 << i)):
                            continue
                        metrics.comparisons += 1
                        metrics.operations += 1

                        if (prev_mask, i) in memo:
                            cand_cost = memo[(prev_mask, i)] + dist[i][j]
                            if cand_cost < best_cost:
                                best_cost = cand_cost
                                best_p = i

                    if best_p is not None:
                        memo[(mask, j)] = best_cost
                        parent[(mask, j)] = best_p

                        if len(steps) < max_steps:
                            steps.append(ExecutionStep(
                                step_id=step_id[0],
                                action="update_subproblem",
                                indices=[best_p, j],
                                values=[best_cost],
                                state_snapshot={"subset_size": size, "end_city": cities[j], "cost": best_cost},
                                description=f"Optimal subset tour ending at {cities[j]} via {cities[best_p]}: min cost = {best_cost}.",
                                highlight_line=6
                            ))
                            step_id[0] += 1

        full_mask = (1 << n) - 1
        optimal_cost = float('inf')
        last_city = None

        for j in range(1, n):
            if (full_mask, j) in memo:
                total_cost = memo[(full_mask, j)] + dist[j][0]
                if total_cost < optimal_cost:
                    optimal_cost = total_cost
                    last_city = j

        # Reconstruct tour
        tour = [0]
        curr_mask = full_mask
        curr_city = last_city

        rev_path = []
        while curr_city is not None and curr_city != 0:
            rev_path.append(curr_city)
            prev_city = parent.get((curr_mask, curr_city))
            curr_mask = curr_mask ^ (1 << curr_city)
            curr_city = prev_city

        tour.extend(reversed(rev_path))
        tour.append(0)
        tour_city_labels = [cities[idx] for idx in tour]

        steps.append(ExecutionStep(
            step_id=step_id[0],
            action="optimal_tour_found",
            state_snapshot={"tour": tour_city_labels, "cost": round(optimal_cost, 4)},
            description=f"Optimal TSP tour complete: {' -> '.join(tour_city_labels)} with exact minimum tour cost = {round(optimal_cost, 4)}."
        ))
        step_id[0] += 1

        out = {
            "min_cost": round(optimal_cost, 4),
            "tour": tour,
            "tour_city_labels": tour_city_labels,
            "num_cities": n,
            "states_computed": len(memo)
        }
        return AlgorithmExecutionResult(
            algorithm_slug=self.slug,
            output=out,
            metrics=metrics,
            steps=steps
        )
