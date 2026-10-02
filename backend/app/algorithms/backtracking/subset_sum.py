"""
Subset Sum Problem Implementation (Backtracking with Pruning)
"""
from typing import Dict, Any, List, Tuple
from app.algorithms.base import BaseAlgorithm, ExecutionMetrics, ExecutionStep, AlgorithmExecutionResult


class SubsetSum(BaseAlgorithm):
    slug = "subset-sum-backtracking"
    name = "Subset Sum (Backtracking)"
    category = "Backtracking"
    paradigm = "Backtracking"

    def _parse_input(self, input_data: Any) -> Tuple[List[int], int]:
        if isinstance(input_data, dict):
            arr = input_data.get("numbers", input_data.get("array", []))
            target = input_data.get("target_sum", input_data.get("target", 0))
        elif isinstance(input_data, (list, tuple)) and len(input_data) == 2:
            arr, target = input_data[0], input_data[1]
        else:
            arr, target = [3, 5, 6, 7], 15
        return [int(x) for x in arr], int(target)

    def run(self, input_data: Any) -> Dict[str, Any]:
        raw_arr, target = self._parse_input(input_data)
        arr = sorted([x for x in raw_arr if x <= target])
        subset: List[int] = []
        found_subsets: List[List[int]] = []

        def _backtrack(idx: int, current_sum: int):
            if current_sum == target:
                found_subsets.append(list(subset))
                return
            if idx >= len(arr) or current_sum > target:
                return

            for i in range(idx, len(arr)):
                if current_sum + arr[i] > target:
                    break  # Pruning: since sorted, subsequent elements will also exceed target

                subset.append(arr[i])
                _backtrack(i + 1, current_sum + arr[i])
                subset.pop()  # Backtrack

        _backtrack(0, 0)

        return {
            "has_solution": len(found_subsets) > 0,
            "target": target,
            "solution": found_subsets[0] if found_subsets else [],
            "solutions": found_subsets,
            "solution_count": len(found_subsets),
            "total_solutions": len(found_subsets)
        }

    def run_instrumented(self, input_data: Any, max_steps: int = 500) -> AlgorithmExecutionResult:
        raw_arr, target = self._parse_input(input_data)
        metrics = ExecutionMetrics()
        steps: List[ExecutionStep] = []
        step_id = [0]

        arr = sorted([x for x in raw_arr if x <= target])
        subset: List[int] = []
        found_subsets: List[List[int]] = []

        steps.append(ExecutionStep(
            step_id=step_id[0],
            action="init",
            state_snapshot={"sorted_array": arr, "target": target},
            description=f"Sorted array {arr} and target {target} for Branch and Bound pruning."
        ))
        step_id[0] += 1

        def _backtrack_instrumented(idx: int, current_sum: int):
            metrics.recursive_calls += 1
            metrics.operations += 1

            if current_sum == target:
                found_subsets.append(list(subset))
                if len(steps) < max_steps:
                    steps.append(ExecutionStep(
                        step_id=step_id[0],
                        action="target_reached",
                        values=list(subset),
                        state_snapshot=list(subset),
                        description=f"Match found! Subset {list(subset)} sums exactly to {target}!",
                        highlight_line=4
                    ))
                    step_id[0] += 1
                return

            if idx >= len(arr) or current_sum > target:
                return

            for i in range(idx, len(arr)):
                metrics.comparisons += 1
                if current_sum + arr[i] > target:
                    if len(steps) < max_steps:
                        steps.append(ExecutionStep(
                            step_id=step_id[0],
                            action="prune_branch",
                            indices=[i],
                            values=[arr[i]],
                            description=f"Pruned branch: current_sum({current_sum}) + arr[{i}]({arr[i]}) > target({target})."
                        ))
                        step_id[0] += 1
                    break

                subset.append(arr[i])
                if len(steps) < max_steps:
                    steps.append(ExecutionStep(
                        step_id=step_id[0],
                        action="include_element",
                        indices=[i],
                        values=[arr[i]],
                        state_snapshot=list(subset),
                        description=f"Included {arr[i]} in subset. Current sum is now {current_sum + arr[i]}.",
                        highlight_line=8
                    ))
                    step_id[0] += 1

                _backtrack_instrumented(i + 1, current_sum + arr[i])

                subset.pop()
                if len(steps) < max_steps:
                    steps.append(ExecutionStep(
                        step_id=step_id[0],
                        action="backtrack",
                        indices=[i],
                        values=[arr[i]],
                        state_snapshot=list(subset),
                        description=f"Backtracked: Excluded {arr[i]} from subset."
                    ))
                    step_id[0] += 1

        _backtrack_instrumented(0, 0)

        out = {
            "has_solution": len(found_subsets) > 0,
            "target": target,
            "solution": found_subsets[0] if found_subsets else [],
            "total_solutions": len(found_subsets)
        }
        return AlgorithmExecutionResult(
            algorithm_slug=self.slug,
            output=out,
            metrics=metrics,
            steps=steps
        )
