"""
Fractional Knapsack Implementation (Greedy)
"""
from typing import Dict, Any, List
from app.algorithms.base import BaseAlgorithm, ExecutionMetrics, ExecutionStep, AlgorithmExecutionResult


class FractionalKnapsack(BaseAlgorithm):
    slug = "fractional-knapsack"
    name = "Fractional Knapsack (Greedy)"
    category = "Greedy"
    paradigm = "Greedy"

    def _parse_input(self, input_data: Any):
        if isinstance(input_data, dict):
            if "items" in input_data:
                items_raw = input_data["items"]
                weights = [it["weight"] if isinstance(it, dict) else it[0] for it in items_raw]
                values = [it["value"] if isinstance(it, dict) else it[1] for it in items_raw]
            else:
                weights = input_data.get("weights", [])
                values = input_data.get("values", [])
            capacity = input_data.get("capacity", 50)
        else:
            weights, values, capacity = input_data
        return weights, values, capacity

    def run(self, input_data: Any) -> Dict[str, Any]:
        weights, values, capacity = self._parse_input(input_data)

        items = []
        for i in range(len(weights)):
            items.append({
                "id": i,
                "weight": weights[i],
                "value": values[i],
                "ratio": values[i] / weights[i] if weights[i] > 0 else 0
            })

        items.sort(key=lambda x: x["ratio"], reverse=True)

        total_value = 0.0
        remaining_capacity = float(capacity)
        fractions = [0.0] * len(weights)

        for item in items:
            if remaining_capacity <= 0:
                break
            if item["weight"] <= remaining_capacity:
                fractions[item["id"]] = 1.0
                total_value += item["value"]
                remaining_capacity -= item["weight"]
            else:
                fraction = remaining_capacity / item["weight"]
                fractions[item["id"]] = round(fraction, 4)
                total_value += item["value"] * fraction
                remaining_capacity = 0.0
                break

        val = round(total_value, 4)
        return {
            "max_value": val,
            "total_value": val,
            "fractions": fractions,
            "remaining_capacity": round(remaining_capacity, 4)
        }

    def run_instrumented(self, input_data: Any, max_steps: int = 500) -> AlgorithmExecutionResult:
        weights, values, capacity = self._parse_input(input_data)

        metrics = ExecutionMetrics()
        steps: List[ExecutionStep] = []
        step_id = 0

        items = []
        for i in range(len(weights)):
            items.append({
                "id": i,
                "weight": weights[i],
                "value": values[i],
                "ratio": round(values[i] / weights[i] if weights[i] > 0 else 0, 4)
            })

        items.sort(key=lambda x: x["ratio"], reverse=True)
        metrics.operations += len(items)

        steps.append(ExecutionStep(
            step_id=step_id,
            action="sort_densities",
            state_snapshot=items,
            description=f"Computed value/weight densities and sorted {len(items)} items descending."
        ))
        step_id += 1

        total_value = 0.0
        remaining_capacity = float(capacity)
        fractions = [0.0] * len(weights)

        for item in items:
            if remaining_capacity <= 0:
                break

            metrics.comparisons += 1
            metrics.operations += 1

            if item["weight"] <= remaining_capacity:
                fractions[item["id"]] = 1.0
                total_value += item["value"]
                remaining_capacity -= item["weight"]

                if len(steps) < max_steps:
                    steps.append(ExecutionStep(
                        step_id=step_id,
                        action="take_whole",
                        indices=[item["id"]],
                        values=[item["value"], item["weight"]],
                        state_snapshot=list(fractions),
                        description=f"Took 100% of item #{item['id']} (wt={item['weight']}, val={item['value']}). Remaining capacity={remaining_capacity}",
                        highlight_line=5
                    ))
                    step_id += 1
            else:
                fraction = remaining_capacity / item["weight"]
                fractions[item["id"]] = round(fraction, 4)
                added_val = item["value"] * fraction
                total_value += added_val

                if len(steps) < max_steps:
                    steps.append(ExecutionStep(
                        step_id=step_id,
                        action="take_fraction",
                        indices=[item["id"]],
                        values=[round(fraction, 4), added_val],
                        state_snapshot=list(fractions),
                        description=f"Took {round(fraction*100, 2)}% fraction of item #{item['id']} to fill remaining capacity. Added value={round(added_val, 2)}.",
                        highlight_line=8
                    ))
                    step_id += 1
                remaining_capacity = 0.0
                break

        out = {
            "max_value": round(total_value, 4),
            "fractions": fractions,
            "remaining_capacity": round(remaining_capacity, 4)
        }
        return AlgorithmExecutionResult(
            algorithm_slug=self.slug,
            output=out,
            metrics=metrics,
            steps=steps
        )
