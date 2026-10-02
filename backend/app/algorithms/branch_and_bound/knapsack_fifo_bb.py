"""
0/1 Knapsack Problem — FIFO Branch and Bound Implementation
Uses breadth-first FIFO queue state-space tree traversal with bounding and pruning.
"""
from collections import deque
from typing import Dict, Any, List, Tuple
from app.algorithms.base import BaseAlgorithm, ExecutionMetrics, ExecutionStep, AlgorithmExecutionResult


class KnapsackFIFOBRanchAndBound(BaseAlgorithm):
    slug = "0-1-knapsack-fifo-bb"
    name = "0/1 Knapsack (FIFO Branch and Bound)"
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

        # FIFO Queue holds tuples: (level, current_weight, current_value, bound, taken_tuple)
        queue = deque()
        root_bound = self._calculate_bound(-1, 0.0, 0.0, items, capacity)
        queue.append((-1, 0.0, 0.0, root_bound, ()))

        max_profit = 0.0
        best_taken: Tuple[int, ...] = ()
        nodes_explored = 0
        nodes_pruned = 0
        nodes_generated = 1

        while queue:
            level, curr_wt, curr_val, upper_bound, taken = queue.popleft()
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

            # 1. Include next item (Left Child)
            if curr_wt + next_item["weight"] <= capacity:
                inc_val = curr_val + next_item["value"]
                inc_wt = curr_wt + next_item["weight"]
                inc_bound = self._calculate_bound(next_level, inc_wt, inc_val, items, capacity)
                inc_taken = taken + (next_item["orig_id"],)

                if inc_val > max_profit:
                    max_profit = inc_val
                    best_taken = inc_taken

                if inc_bound > max_profit:
                    queue.append((next_level, inc_wt, inc_val, inc_bound, inc_taken))
                    nodes_generated += 1
                else:
                    nodes_pruned += 1

            # 2. Exclude next item (Right Child)
            exc_bound = self._calculate_bound(next_level, curr_wt, curr_val, items, capacity)
            if exc_bound > max_profit:
                queue.append((next_level, curr_wt, curr_val, exc_bound, taken))
                nodes_generated += 1
            else:
                nodes_pruned += 1

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
            "total_nodes_generated": nodes_generated
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
            description=f"Initialized FIFO Branch & Bound for 0/1 Knapsack with FIFO Queue exploration."
        ))
        step_id[0] += 1

        queue = deque()
        root_bound = self._calculate_bound(-1, 0.0, 0.0, items, capacity)
        queue.append((-1, 0.0, 0.0, root_bound, ()))

        max_profit = 0.0
        best_taken: Tuple[int, ...] = ()
        nodes_explored = 0
        nodes_pruned = 0
        nodes_generated = 1

        while queue:
            level, curr_wt, curr_val, upper_bound, taken = queue.popleft()
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
                        description=f"Pruned FIFO queue node at level {level}: Bound ({upper_bound:.2f}) <= Best Profit ({max_profit:.2f})."
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

            # Include
            if curr_wt + next_item["weight"] <= capacity:
                inc_val = curr_val + next_item["value"]
                inc_wt = curr_wt + next_item["weight"]
                inc_bound = self._calculate_bound(next_level, inc_wt, inc_val, items, capacity)
                inc_taken = taken + (next_item["orig_id"],)

                if inc_val > max_profit:
                    max_profit = inc_val
                    best_taken = inc_taken

                if inc_bound > max_profit:
                    queue.append((next_level, inc_wt, inc_val, inc_bound, inc_taken))
                    nodes_generated += 1
                    if len(steps) < max_steps:
                        steps.append(ExecutionStep(
                            step_id=step_id[0],
                            action="enqueue_include",
                            indices=[next_item["orig_id"]],
                            values=[inc_val, inc_bound],
                            state_snapshot={"queue_len": len(queue), "bound": inc_bound},
                            description=f"FIFO Branch (Include item #{next_item['orig_id']}): Enqueued to tail of FIFO Queue (Bound={inc_bound:.2f}).",
                            highlight_line=4
                        ))
                        step_id[0] += 1
                else:
                    nodes_pruned += 1

            # Exclude
            exc_bound = self._calculate_bound(next_level, curr_wt, curr_val, items, capacity)
            if exc_bound > max_profit:
                queue.append((next_level, curr_wt, curr_val, exc_bound, taken))
                nodes_generated += 1
                if len(steps) < max_steps:
                    steps.append(ExecutionStep(
                        step_id=step_id[0],
                        action="enqueue_exclude",
                        indices=[next_item["orig_id"]],
                        values=[curr_val, exc_bound],
                        state_snapshot={"queue_len": len(queue), "bound": exc_bound},
                        description=f"FIFO Branch (Exclude item #{next_item['orig_id']}): Enqueued to tail of FIFO Queue (Bound={exc_bound:.2f})."
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
            description=f"FIFO Branch & Bound Knapsack solved: Max Profit = {max_profit}, Explored {nodes_explored} nodes, Pruned {nodes_pruned} subtrees."
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
            "total_nodes_generated": nodes_generated
        }
        return AlgorithmExecutionResult(
            algorithm_slug=self.slug,
            output=out,
            metrics=metrics,
            steps=steps
        )
