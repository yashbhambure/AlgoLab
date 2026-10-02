"""
Finding Maximum and Minimum (Divide and Conquer O(n) with 3n/2 - 2 comparisons)
Solves simultaneous min-max extraction with optimal comparison bound.
"""
from typing import Dict, Any, List, Tuple
from app.algorithms.base import BaseAlgorithm, ExecutionMetrics, ExecutionStep, AlgorithmExecutionResult


class MaxMinDivideConquer(BaseAlgorithm):
    slug = "max-min-divide-conquer"
    name = "Finding Maximum and Minimum (D&C)"
    category = "Divide and Conquer"
    paradigm = "Divide and Conquer"

    time_complexity_best = "O(n)"
    time_complexity_average = "O(n)"
    time_complexity_worst = "O(n)"
    space_complexity = "O(log n)"
    is_stable = True
    is_in_place = False

    def _parse_input(self, input_data: Any) -> List[float]:
        if isinstance(input_data, dict):
            arr = input_data.get("array", input_data.get("data", []))
        elif isinstance(input_data, list):
            arr = input_data
        else:
            arr = [10, 20, 5, 8, 45, 2, 17, 33]
        return [float(x) for x in arr]

    def run(self, input_data: Any) -> Dict[str, Any]:
        arr = self._parse_input(input_data)
        if not arr:
            return {"min": None, "max": None, "comparisons": 0, "size": 0}

        def _find_max_min(low: int, high: int) -> Tuple[float, float, int]:
            # Base case 1: Single element
            if low == high:
                return arr[low], arr[low], 0

            # Base case 2: Two elements
            if high == low + 1:
                if arr[low] < arr[high]:
                    return arr[low], arr[high], 1
                else:
                    return arr[high], arr[low], 1

            # Divide step
            mid = (low + high) // 2
            min1, max1, c1 = _find_max_min(low, mid)
            min2, max2, c2 = _find_max_min(mid + 1, high)

            # Combine step (2 comparisons)
            overall_min = min1 if min1 < min2 else min2
            overall_max = max1 if max1 > max2 else max2
            return overall_min, overall_max, c1 + c2 + 2

        overall_min, overall_max, total_comp = _find_max_min(0, len(arr) - 1)
        return {
            "min": overall_min,
            "max": overall_max,
            "comparisons": total_comp,
            "size": len(arr),
            "theoretical_comparisons": int(1.5 * len(arr) - 2) if len(arr) >= 2 else 0
        }

    def run_instrumented(self, input_data: Any, max_steps: int = 500) -> AlgorithmExecutionResult:
        arr = self._parse_input(input_data)
        metrics = ExecutionMetrics()
        steps: List[ExecutionStep] = []
        step_id = [0]

        if not arr:
            return AlgorithmExecutionResult(
                algorithm_slug=self.slug,
                output={"min": None, "max": None, "comparisons": 0, "size": 0},
                metrics=metrics,
                steps=steps
            )

        steps.append(ExecutionStep(
            step_id=step_id[0],
            action="init",
            state_snapshot=list(arr),
            description=f"Initialized Divide & Conquer Max-Min search on array of size {len(arr)}."
        ))
        step_id[0] += 1

        def _find_max_min_instrumented(low: int, high: int) -> Tuple[float, float]:
            metrics.recursive_calls += 1
            metrics.operations += 1

            # Base case 1: 1 element
            if low == high:
                val = arr[low]
                if len(steps) < max_steps:
                    steps.append(ExecutionStep(
                        step_id=step_id[0],
                        action="base_case_1",
                        indices=[low],
                        values=[val],
                        state_snapshot=list(arr),
                        description=f"Base case (single element at index {low}): min={val}, max={val} (0 comparisons)."
                    ))
                    step_id[0] += 1
                return val, val

            # Base case 2: 2 elements
            if high == low + 1:
                metrics.comparisons += 1
                if arr[low] < arr[high]:
                    mn, mx = arr[low], arr[high]
                else:
                    mn, mx = arr[high], arr[low]

                if len(steps) < max_steps:
                    steps.append(ExecutionStep(
                        step_id=step_id[0],
                        action="base_case_2",
                        indices=[low, high],
                        values=[mn, mx],
                        state_snapshot=list(arr),
                        description=f"Base case (pair at indices {low}, {high}): compared {arr[low]} and {arr[high]} -> min={mn}, max={mx} (1 comparison)."
                    ))
                    step_id[0] += 1
                return mn, mx

            # Divide
            mid = (low + high) // 2
            if len(steps) < max_steps:
                steps.append(ExecutionStep(
                    step_id=step_id[0],
                    action="divide",
                    indices=[low, mid, high],
                    values=[low, high],
                    state_snapshot=list(arr),
                    description=f"Divided subarray [{low}..{high}] at mid={mid} into [{low}..{mid}] and [{mid+1}..{high}]."
                ))
                step_id[0] += 1

            min1, max1 = _find_max_min_instrumented(low, mid)
            min2, max2 = _find_max_min_instrumented(mid + 1, high)

            # Combine
            metrics.comparisons += 2
            overall_min = min1 if min1 < min2 else min2
            overall_max = max1 if max1 > max2 else max2

            if len(steps) < max_steps:
                steps.append(ExecutionStep(
                    step_id=step_id[0],
                    action="combine",
                    indices=[low, high],
                    values=[overall_min, overall_max],
                    state_snapshot=list(arr),
                    description=f"Combined results of [{low}..{mid}] and [{mid+1}..{high}]: min({min1}, {min2})={overall_min}, max({max1}, {max2})={overall_max} (+2 comparisons)."
                ))
                step_id[0] += 1

            return overall_min, overall_max

        overall_min, overall_max = _find_max_min_instrumented(0, len(arr) - 1)

        out = {
            "min": overall_min,
            "max": overall_max,
            "comparisons": metrics.comparisons,
            "size": len(arr),
            "theoretical_comparisons": int(1.5 * len(arr) - 2) if len(arr) >= 2 else 0
        }
        return AlgorithmExecutionResult(
            algorithm_slug=self.slug,
            output=out,
            metrics=metrics,
            steps=steps
        )
