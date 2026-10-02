"""
Optimal Merge Patterns Implementation (Greedy / Min-Heap O(n log n))
Finds optimal 2-way merge pattern minimizing total record movements across sorted files.
"""
import heapq
from typing import Dict, Any, List
from app.algorithms.base import BaseAlgorithm, ExecutionMetrics, ExecutionStep, AlgorithmExecutionResult


class OptimalMergePatterns(BaseAlgorithm):
    slug = "optimal-merge-patterns-greedy"
    name = "Optimal Merge Patterns (Greedy)"
    category = "Greedy"
    paradigm = "Greedy"

    time_complexity_best = "O(n log n)"
    time_complexity_average = "O(n log n)"
    time_complexity_worst = "O(n log n)"
    space_complexity = "O(n)"
    is_stable = True
    is_in_place = False

    def _parse_input(self, input_data: Any):
        if isinstance(input_data, dict):
            sizes = input_data.get("files", input_data.get("file_sizes", [20, 30, 10, 5, 30]))
            names = input_data.get("names", [])
        elif isinstance(input_data, list):
            sizes = input_data
            names = []
        else:
            sizes = [20, 30, 10, 5, 30]
            names = []

        n = len(sizes)
        if not names or len(names) < n:
            names = [f"F{i+1}" for i in range(n)]

        return [int(x) for x in sizes], names

    def run(self, input_data: Any) -> Dict[str, Any]:
        sizes, names = self._parse_input(input_data)
        n = len(sizes)
        if n <= 1:
            return {
                "num_files": n,
                "total_merge_cost": 0,
                "merge_steps": [],
                "merge_tree": {"label": names[0] if names else "F1", "size": sizes[0] if sizes else 0}
            }

        # Min-heap items: (size, tie_breaker_id, tree_node)
        heap = []
        counter = 0
        for i in range(n):
            node = {"label": names[i], "size": sizes[i], "left": None, "right": None}
            heapq.heappush(heap, (sizes[i], counter, node))
            counter += 1

        total_cost = 0
        merge_steps = []

        while len(heap) > 1:
            size1, _, node1 = heapq.heappop(heap)
            size2, _, node2 = heapq.heappop(heap)

            cost = size1 + size2
            total_cost += cost

            merged_node = {
                "label": f"({node1['label']}+{node2['label']})",
                "size": cost,
                "left": node1,
                "right": node2
            }

            merge_steps.append({
                "step": len(merge_steps) + 1,
                "merged": [node1["label"], node2["label"]],
                "sizes": [size1, size2],
                "merge_cost": cost,
                "running_total_cost": total_cost
            })

            heapq.heappush(heap, (cost, counter, merged_node))
            counter += 1

        root_size, _, root_tree = heap[0]

        return {
            "num_files": n,
            "total_merge_cost": total_cost,
            "merge_steps": merge_steps,
            "merge_tree": root_tree
        }

    def run_instrumented(self, input_data: Any, max_steps: int = 500) -> AlgorithmExecutionResult:
        sizes, names = self._parse_input(input_data)
        metrics = ExecutionMetrics()
        steps: List[ExecutionStep] = []
        step_id = [0]
        n = len(sizes)

        if n <= 1:
            return AlgorithmExecutionResult(
                algorithm_slug=self.slug,
                output={"num_files": n, "total_merge_cost": 0, "merge_steps": [], "merge_tree": None},
                metrics=metrics,
                steps=steps
            )

        steps.append(ExecutionStep(
            step_id=step_id[0],
            action="init",
            state_snapshot={"sizes": sizes, "names": names},
            description=f"Initialized Optimal Merge Patterns with {n} files: {list(zip(names, sizes))}."
        ))
        step_id[0] += 1

        heap = []
        counter = 0
        for i in range(n):
            node = {"label": names[i], "size": sizes[i], "left": None, "right": None}
            heapq.heappush(heap, (sizes[i], counter, node))
            counter += 1

        total_cost = 0
        merge_steps = []

        while len(heap) > 1:
            metrics.comparisons += 2
            metrics.operations += 2

            size1, _, node1 = heapq.heappop(heap)
            size2, _, node2 = heapq.heappop(heap)

            cost = size1 + size2
            total_cost += cost

            merged_node = {
                "label": f"({node1['label']}+{node2['label']})",
                "size": cost,
                "left": node1,
                "right": node2
            }

            merge_steps.append({
                "step": len(merge_steps) + 1,
                "merged": [node1["label"], node2["label"]],
                "sizes": [size1, size2],
                "merge_cost": cost,
                "running_total_cost": total_cost
            })

            heapq.heappush(heap, (cost, counter, merged_node))
            counter += 1

            if len(steps) < max_steps:
                steps.append(ExecutionStep(
                    step_id=step_id[0],
                    action="greedy_merge",
                    indices=[size1, size2],
                    values=[cost, total_cost],
                    state_snapshot={"step": len(merge_steps), "merged": [node1['label'], node2['label']], "cost": cost, "total": total_cost},
                    description=f"Greedy Choice: Picked 2 smallest files {node1['label']} ({size1}) and {node2['label']} ({size2}) -> Merged size={cost}, Running Total={total_cost}.",
                    highlight_line=5
                ))
                step_id[0] += 1

        root_size, _, root_tree = heap[0]

        steps.append(ExecutionStep(
            step_id=step_id[0],
            action="merge_tree_completed",
            state_snapshot={"total_merge_cost": total_cost},
            description=f"Optimal 2-Way Merge Tree complete. Minimum total record movement = {total_cost}."
        ))
        step_id[0] += 1

        out = {
            "num_files": n,
            "total_merge_cost": total_cost,
            "merge_steps": merge_steps,
            "merge_tree": root_tree
        }
        return AlgorithmExecutionResult(
            algorithm_slug=self.slug,
            output=out,
            metrics=metrics,
            steps=steps
        )
