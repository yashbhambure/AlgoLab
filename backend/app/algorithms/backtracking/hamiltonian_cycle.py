"""
Hamiltonian Cycle Implementation (Backtracking)
"""
from typing import Dict, Any, List
from collections import defaultdict
from app.algorithms.base import BaseAlgorithm, ExecutionMetrics, ExecutionStep, AlgorithmExecutionResult


class HamiltonianCycle(BaseAlgorithm):
    slug = "hamiltonian-cycle-backtracking"
    name = "Hamiltonian Cycle (Backtracking)"
    category = "Backtracking"
    paradigm = "Backtracking"

    def run(self, input_data: Any) -> Dict[str, Any]:
        if isinstance(input_data, dict):
            vertices = [str(v) for v in input_data.get("vertices", [])]
            raw_edges = input_data.get("edges", [])
        else:
            vertices, raw_edges = input_data
            vertices = [str(v) for v in vertices]

        n = len(vertices)
        if n == 0:
            return {"has_cycle": False, "cycle_found": False, "cycle": []}

        v_map = {v: i for i, v in enumerate(vertices)}
        adj_matrix = [[0] * n for _ in range(n)]
        for edge in raw_edges:
            if isinstance(edge, dict):
                u = str(edge.get("source", edge.get("u", "")))
                v = str(edge.get("target", edge.get("v", "")))
            elif isinstance(edge, (list, tuple)):
                u, v = str(edge[0]), str(edge[1])
            else:
                continue
            if u in v_map and v in v_map:
                adj_matrix[v_map[u]][v_map[v]] = 1
                adj_matrix[v_map[v]][v_map[u]] = 1

        path = [-1] * n
        path[0] = 0  # Start path at vertex index 0

        def _is_safe(v: int, pos: int) -> bool:
            if adj_matrix[path[pos - 1]][v] == 0:
                return False
            for vertex in path[:pos]:
                if vertex == v:
                    return False
            return True

        def _solve(pos: int) -> bool:
            if pos == n:
                # Check if there is an edge from last vertex back to starting vertex
                return adj_matrix[path[pos - 1]][path[0]] == 1

            for v in range(1, n):
                if _is_safe(v, pos):
                    path[pos] = v
                    if _solve(pos + 1):
                        return True
                    path[pos] = -1

            return False

        has_cycle = _solve(1)
        cycle_names = [vertices[i] for i in path] + [vertices[path[0]]] if has_cycle else []

        return {
            "has_cycle": has_cycle,
            "cycle_found": has_cycle,
            "cycle": cycle_names,
            "vertex_count": n
        }

    def run_instrumented(self, input_data: Any, max_steps: int = 500) -> AlgorithmExecutionResult:
        if isinstance(input_data, dict):
            vertices = [str(v) for v in input_data.get("vertices", [])]
            edges = input_data.get("edges", [])
        else:
            vertices, edges = input_data
            vertices = [str(v) for v in vertices]

        metrics = ExecutionMetrics()
        steps: List[ExecutionStep] = []
        step_id = [0]
        n = len(vertices)

        if n == 0:
            return AlgorithmExecutionResult(algorithm_slug=self.slug, output={}, metrics=metrics, steps=[])

        v_map = {v: i for i, v in enumerate(vertices)}
        adj_matrix = [[0] * n for _ in range(n)]
        for edge in edges:
            if isinstance(edge, dict):
                u = str(edge.get("source", edge.get("u", "")))
                v = str(edge.get("target", edge.get("v", "")))
            elif isinstance(edge, (list, tuple)):
                u, v = str(edge[0]), str(edge[1])
            else:
                continue
            if u in v_map and v in v_map:
                adj_matrix[v_map[u]][v_map[v]] = 1
                adj_matrix[v_map[v]][v_map[u]] = 1

        path = [-1] * n
        path[0] = 0

        steps.append(ExecutionStep(
            step_id=step_id[0],
            action="init",
            state_snapshot=[vertices[path[0]]],
            description=f"Initialized Hamiltonian cycle search from starting vertex '{vertices[0]}'."
        ))
        step_id[0] += 1

        def _is_safe(v: int, pos: int) -> bool:
            metrics.comparisons += 1
            if adj_matrix[path[pos - 1]][v] == 0:
                return False
            for vertex in path[:pos]:
                metrics.comparisons += 1
                if vertex == v:
                    return False
            return True

        def _solve_instrumented(pos: int) -> bool:
            metrics.recursive_calls += 1
            metrics.operations += 1

            if pos == n:
                if adj_matrix[path[pos - 1]][path[0]] == 1:
                    if len(steps) < max_steps:
                        steps.append(ExecutionStep(
                            step_id=step_id[0],
                            action="cycle_complete",
                            state_snapshot=[vertices[i] for i in path] + [vertices[path[0]]],
                            description=f"Hamiltonian Cycle found! Closed loop visits all {n} vertices exactly once.",
                            highlight_line=4
                        ))
                        step_id[0] += 1
                    return True
                return False

            for v in range(1, n):
                if _is_safe(v, pos):
                    path[pos] = v
                    if len(steps) < max_steps:
                        steps.append(ExecutionStep(
                            step_id=step_id[0],
                            action="extend_path",
                            indices=[pos],
                            values=[vertices[v]],
                            state_snapshot=[vertices[i] for i in path if i != -1],
                            description=f"Extended path: added vertex '{vertices[v]}' at position {pos}.",
                            highlight_line=7
                        ))
                        step_id[0] += 1

                    if _solve_instrumented(pos + 1):
                        return True

                    path[pos] = -1
                    if len(steps) < max_steps:
                        steps.append(ExecutionStep(
                            step_id=step_id[0],
                            action="backtrack",
                            indices=[pos],
                            state_snapshot=[vertices[i] for i in path if i != -1],
                            description=f"Backtracked: Removed vertex '{vertices[v]}' from path."
                        ))
                        step_id[0] += 1

            return False

        has_cycle = _solve_instrumented(1)
        cycle_names = [vertices[i] for i in path] + [vertices[path[0]]] if has_cycle else []

        out = {
            "has_cycle": has_cycle,
            "cycle": cycle_names,
            "vertex_count": n
        }
        return AlgorithmExecutionResult(
            algorithm_slug=self.slug,
            output=out,
            metrics=metrics,
            steps=steps
        )
