"""
0/1 Knapsack Implementation (Dynamic Programming Tabulation)
"""
from typing import Dict, Any, List
from app.algorithms.base import BaseAlgorithm, ExecutionMetrics, ExecutionStep, AlgorithmExecutionResult


class Knapsack01(BaseAlgorithm):
    slug = "0-1-knapsack-dp"
    name = "0/1 Knapsack (DP)"
    category = "Dynamic Programming"
    paradigm = "Dynamic Programming"

    def _parse_input(self, input_data: Any):
        if isinstance(input_data, dict):
            if "items" in input_data and isinstance(input_data["items"], list):
                weights = []
                values = []
                for item in input_data["items"]:
                    if isinstance(item, dict):
                        weights.append(item.get("weight", item.get("w", 1)))
                        values.append(item.get("value", item.get("v", 0)))
                    elif isinstance(item, (list, tuple)) and len(item) >= 2:
                        weights.append(item[0])
                        values.append(item[1])
                capacity = input_data.get("capacity", input_data.get("W", 50))
                return weights, values, capacity
            weights = input_data.get("weights", [])
            values = input_data.get("values", [])
            capacity = input_data.get("capacity", input_data.get("W", 50))
            return weights, values, capacity
        elif isinstance(input_data, (list, tuple)):
            if len(input_data) == 3:
                return input_data[0], input_data[1], input_data[2]
            elif len(input_data) == 2:
                return input_data[0], input_data[1], 50
        return [], [], 50

    def run(self, input_data: Any) -> Dict[str, Any]:
        weights, values, capacity = self._parse_input(input_data)

        n = len(weights)
        W = int(capacity)
        if n == 0 or W <= 0:
            return {
                "max_value": 0,
                "total_value": 0,
                "selected_items": [],
                "total_weight_used": 0
            }

        # 2D DP Table
        dp = [[0] * (W + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            wt = weights[i - 1]
            val = values[i - 1]
            for w in range(W + 1):
                if wt <= w:
                    dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - wt] + val)
                else:
                    dp[i][w] = dp[i - 1][w]

        # Reconstruct selected items
        selected_items = []
        w_curr = W
        for i in range(n, 0, -1):
            if dp[i][w_curr] != dp[i - 1][w_curr]:
                selected_items.append(i - 1)
                w_curr -= weights[i - 1]

        selected_items.reverse()

        return {
            "max_value": dp[n][W],
            "total_value": dp[n][W],
            "selected_items": selected_items,
            "total_weight_used": sum(weights[i] for i in selected_items)
        }

    def run_instrumented(self, input_data: Any, max_steps: int = 500) -> AlgorithmExecutionResult:
        weights, values, capacity = self._parse_input(input_data)

        metrics = ExecutionMetrics()
        steps: List[ExecutionStep] = []
        step_id = 0

        n = len(weights)
        W = int(capacity)

        dp = [[0] * (W + 1) for _ in range(n + 1)]

        steps.append(ExecutionStep(
            step_id=step_id,
            action="init_table",
            state_snapshot={"rows": n + 1, "cols": W + 1},
            description=f"Initialized DP table of size ({n+1}) x ({W+1}) with base cases DP[0][w] = 0 and DP[i][0] = 0."
        ))
        step_id += 1

        for i in range(1, n + 1):
            wt = weights[i - 1]
            val = values[i - 1]
            for w in range(W + 1):
                metrics.operations += 1
                if wt <= w:
                    metrics.comparisons += 1
                    take = dp[i - 1][w - wt] + val
                    skip = dp[i - 1][w]
                    dp[i][w] = max(skip, take)

                    if len(steps) < max_steps:
                        steps.append(ExecutionStep(
                            step_id=step_id,
                            action="set_dp_cell",
                            indices=[i, w],
                            values=[dp[i][w]],
                            state_snapshot=[row[:min(W + 1, 10)] for row in dp[:min(n + 1, 10)]],
                            description=f"Item #{i-1} (wt={wt}, val={val}) at cap={w}: max(skip={skip}, take={take}) = {dp[i][w]}",
                            highlight_line=6
                        ))
                        step_id += 1
                else:
                    dp[i][w] = dp[i - 1][w]

        # Reconstruct items
        selected_items = []
        w_curr = W
        for i in range(n, 0, -1):
            if dp[i][w_curr] != dp[i - 1][w_curr]:
                selected_items.append(i - 1)
                w_curr -= weights[i - 1]

        selected_items.reverse()

        out = {
            "max_value": dp[n][W],
            "total_value": dp[n][W],
            "selected_items": selected_items,
            "total_weight_used": sum(weights[i] for i in selected_items)
        }
        return AlgorithmExecutionResult(
            algorithm_slug=self.slug,
            output=out,
            metrics=metrics,
            steps=steps
        )
