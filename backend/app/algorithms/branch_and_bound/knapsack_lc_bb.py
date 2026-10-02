"""
0/1 Knapsack Problem — LC (Least Cost / Best First) Branch and Bound Implementation
Uses fractional knapsack relaxation for upper-bounding and a max-priority queue for exploration.
"""
import heapq
from typing import Dict, Any, List, Tuple
from app.algorithms.base import BaseAlgorithm, ExecutionMetrics, ExecutionStep, AlgorithmExecutionResult


class KnapsackLCBranchAndBound(BaseAlgorithm):
    slug = "0-1-knapsack-lc-bb"
    name = "0/1 Knapsack (LC Branch and Bound)"
    category = "Branch and Bound"
    paradigm = "Branch and Bound"

    time_complexity_best = "O(n)"
    time_complexity_average = "O(2^n)"
    time_complexity_worst = "O(2^n)"
    space_complexity = "O(2^n)"
    is_stable = True
    is_in_place = False

    def _parse_input(self, input_data: Any):
        if isinstance(input_data, dict):
            if "items" in input_data:
                items_raw = input_data["items"]
                weights = [it["weight"] if isinstance(it, dict) else it[0] for it in items_raw]
                values = [it["value"] if isinstance(it, dict) else it[1] for it in items_raw]
            else:
                weights = input_data.get("weights", [2, 4, 6, 9])
                values = input_data.get("values", [10, 10, 12, 18])
            capacity = input_data.get("capacity", 15)
        elif isinstance(input_data, (list, tuple)) and len(input_data) >= 3:
            weights, values, capacity = input_data[0], input_data[1], input_data[2]
        else:
            weights = [2, 4, 6, 9]
            values = [10, 10, 12, 18]
            capacity = 15
        return [float(w) for w in weights], [float(v) for v in values], float(capacity)

    def _calculate_bound(self, level: int, current_weight: float, current_value: float,
                         sorted_items: List[Dict[str, Any]], capacity: float) -> float:
        """Calculates fractional upper bound for node using remaining sorted items."""
        if current_weight > capacity:
            return 0.0

        bound = current_value
        rem_cap = capacity - current_weight
        n = len(sorted_items)

        k = level + 1
        while k < n and sorted_items[k]["weight"] <= rem_cap:
            rem_cap -= sorted_items[k]["weight"]
            bound += sorted_items[k]["value"]
            k += 1

        if k < n and rem_cap > 0:
            bound += sorted_items[k]["ratio"] * rem_cap

        return bound

    def run(self, input_data: Any) -> Dict[str, Any]:
        weights, values, capacity = self._parse_input(input_data)
        n = len(weights)

        # Sort items by value/weight ratio descending
        items = []
        for i in range(n):
            ratio = values[i] / weights[i] if weights[i] > 0 else 0
            items.append({"orig_id": i, "weight": weights[i], "value": values[i], "ratio": ratio})
        items.sort(key=lambda x: x["ratio"], reverse=True)

        # Max priority queue simulated with negative upper bound in min-heap
        # Node tuple: (-upper_bound, level, current_weight, current_value, taken_mask, counter)
        heap = []
        counter = 0

        root_bound = self._calculate_bound(-1, 0.0, 0.0, items, capacity)
        # (-bound, level, weight, value, taken_tuple, counter)
        heapq.heappush(heap, (-root_bound, -1, 0.0, 0.0, (), counter))
        counter += 1

        max_profit = 0.0
        best_taken: Tuple[int, ...] = ()
        nodes_explored = 0
        nodes_pruned = 0

        while heap:
            neg_bound, level, curr_wt, curr_val, taken, _ = heapq.heappop(heap)
            upper_bound = -neg_bound
            nodes_explored += 1

            if upper_bound <= max_profit:
                nodes_pruned += 1
                continue

            if level == n - 1:
                if curr_val > max_profit:
                    max_profit = curr_val
                    best_taken = taken
                continue

            next_level = level + 1
            next_item = items[next_level]

            # 1. Left Child: Include next_item
            if curr_wt + next_item["weight"] <= capacity:
                inc_val = curr_val + next_item["value"]
                inc_wt = curr_wt + next_item["weight"]
                inc_bound = self._calculate_bound(next_level, inc_wt, inc_val, items, capacity)
                inc_taken = taken + (next_item["orig_id"],)

                if inc_val > max_profit:
                    max_profit = inc_val
                    best_taken = inc_taken

                if inc_bound > max_profit:
                    heapq.heappush(heap, (-inc_bound, next_level, inc_wt, inc_val, inc_taken, counter))
                    counter += 1
                else:
                    nodes_pruned += 1

            # 2. Right Child: Exclude next_item
            exc_bound = self._calculate_bound(next_level, curr_wt, curr_val, items, capacity)
            if exc_bound > max_profit:
                heapq.heappush(heap, (-exc_bound, next_level, curr_wt, curr_val, taken, counter))
                counter += 1
            else:
                nodes_pruned += 1

        # Build output mask
        solution_vector = [0] * n
        for orig_idx in best_taken:
            solution_vector[orig_idx] = 1

        return {
            "max_value": round(max_profit, 4),
            "max_profit": round(max_profit, 4),
            "total_value": round(max_profit, 4),
            "capacity": capacity,
            "selected_items": sorted(list(best_taken)),
            "solution_vector": solution_vector,
            "nodes_explored": nodes_explored,
            "nodes_pruned": nodes_pruned,
            "total_nodes_generated": counter
        }

    def run_instrumented(self, input_data: Any, max_steps: int = 500) -> AlgorithmExecutionResult:
        weights, values, capacity = self._parse_input(input_data)
        metrics = ExecutionMetrics()
        steps: List[ExecutionStep] = []
        step_id = [0]
        n = len(weights)

        items = []
        for i in range(n):
            ratio = values[i] / weights[i] if weights[i] > 0 else 0
            items.append({"orig_id": i, "weight": weights[i], "value": values[i], "ratio": ratio})
        items.sort(key=lambda x: x["ratio"], reverse=True)

        steps.append(ExecutionStep(
            step_id=step_id[0],
            action="init",
            state_snapshot={"capacity": capacity, "items": items},
            description=f"Initialized LC Branch & Bound for 0/1 Knapsack ({n} items, Cap={capacity}). Sorted by density descending."
        ))
        step_id[0] += 1

        heap = []
        counter = 0
        root_bound = self._calculate_bound(-1, 0.0, 0.0, items, capacity)
        heapq.heappush(heap, (-root_bound, -1, 0.0, 0.0, (), counter))
        counter += 1

        max_profit = 0.0
        best_taken: Tuple[int, ...] = ()
        nodes_explored = 0
        nodes_pruned = 0

        while heap:
            neg_bound, level, curr_wt, curr_val, taken, _ = heapq.heappop(heap)
            upper_bound = -neg_bound
            nodes_explored += 1
            metrics.operations += 1
            metrics.comparisons += 1

            if upper_bound <= max_profit:
                nodes_pruned += 1
                if len(steps) < max_steps:
                    steps.append(ExecutionStep(
                        step_id=step_id[0],
                        action="prune_node",
                        values=[upper_bound, max_profit],
                        state_snapshot={"bound": upper_bound, "max_profit": max_profit},
                        description=f"Pruned LC-branch at level {level}: Upper Bound ({upper_bound:.2f}) <= Best Known Profit ({max_profit:.2f}).",
                        highlight_line=5
                    ))
                    step_id[0] += 1
                continue

            if level == n - 1:
                if curr_val > max_profit:
                    max_profit = curr_val
                    best_taken = taken
                continue

            next_level = level + 1
            next_item = items[next_level]

            # Left child: include
            if curr_wt + next_item["weight"] <= capacity:
                inc_val = curr_val + next_item["value"]
                inc_wt = curr_wt + next_item["weight"]
                inc_bound = self._calculate_bound(next_level, inc_wt, inc_val, items, capacity)
                inc_taken = taken + (next_item["orig_id"],)

                if inc_val > max_profit:
                    max_profit = inc_val
                    best_taken = inc_taken

                if inc_bound > max_profit:
                    heapq.heappush(heap, (-inc_bound, next_level, inc_wt, inc_val, inc_taken, counter))
                    counter += 1
                    if len(steps) < max_steps:
                        steps.append(ExecutionStep(
                            step_id=step_id[0],
                            action="expand_include",
                            indices=[next_item["orig_id"]],
                            values=[inc_val, inc_bound],
                            state_snapshot={"level": next_level, "bound": inc_bound, "curr_val": inc_val},
                            description=f"LC-Branch (Include item #{next_item['orig_id']}): Val={inc_val}, Bound={inc_bound:.2f} -> Enqueued to Max-PQ."
                        ))
                        step_id[0] += 1
                else:
                    nodes_pruned += 1

            # Right child: exclude
            exc_bound = self._calculate_bound(next_level, curr_wt, curr_val, items, capacity)
            if exc_bound > max_profit:
                heapq.heappush(heap, (-exc_bound, next_level, curr_wt, curr_val, taken, counter))
                counter += 1
                if len(steps) < max_steps:
                    steps.append(ExecutionStep(
                        step_id=step_id[0],
                        action="expand_exclude",
                        indices=[next_item["orig_id"]],
                        values=[curr_val, exc_bound],
                        state_snapshot={"level": next_level, "bound": exc_bound, "curr_val": curr_val},
                        description=f"LC-Branch (Exclude item #{next_item['orig_id']}): Val={curr_val}, Bound={exc_bound:.2f} -> Enqueued to Max-PQ."
                    ))
                    step_id[0] += 1
            else:
                nodes_pruned += 1

        solution_vector = [0] * n
        for orig_idx in best_taken:
            solution_vector[orig_idx] = 1

        steps.append(ExecutionStep(
            step_id=step_id[0],
            action="optimal_found",
            state_snapshot={"max_profit": max_profit, "selected": list(best_taken)},
            description=f"Optimal LC Branch & Bound Knapsack solved: Max Profit = {max_profit}, Explored {nodes_explored} nodes, Pruned {nodes_pruned} subtrees."
        ))
        step_id[0] += 1

        out = {
            "max_profit": round(max_profit, 4),
            "total_value": round(max_profit, 4),
            "capacity": capacity,
            "selected_items": sorted(list(best_taken)),
            "solution_vector": solution_vector,
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
