"""
Bellman-Ford Algorithm Implementation (SSSP with Negative Weights & Cycle Detection)
"""
from typing import Dict, Any, List
from app.algorithms.base import BaseAlgorithm, ExecutionMetrics, ExecutionStep, AlgorithmExecutionResult


class BellmanFord(BaseAlgorithm):
    slug = "bellman-ford-sssp"
    name = "Bellman-Ford Algorithm (SSSP)"
    category = "Graph"
    paradigm = "Dynamic Programming"

    def _parse_input(self, input_data: Any):
        if isinstance(input_data, dict):
            vertices = [str(v) for v in input_data.get("vertices", [])]
            raw_edges = input_data.get("edges", [])
            source = str(input_data.get("source", input_data.get("start_vertex", input_data.get("start", vertices[0] if vertices else "0"))))
        else:
            if isinstance(input_data, (list, tuple)) and len(input_data) >= 3:
                vertices, raw_edges, source = input_data[0], input_data[1], input_data[2]
            else:
                vertices, raw_edges = input_data
                source = vertices[0] if vertices else "0"
            vertices = [str(v) for v in vertices]
            source = str(source)

        edges = []
        for e in raw_edges:
            if isinstance(e, dict):
                u = e.get("source", e.get("u", e.get("from", 0)))
                v = e.get("target", e.get("v", e.get("to", 1)))
                w = e.get("weight", e.get("w", 1))
                edges.append([u, v, w])
            elif isinstance(e, (list, tuple)):
                if len(e) >= 3:
                    edges.append(list(e))
                elif len(e) == 2:
                    edges.append([e[0], e[1], 1])
        return vertices, edges, source

    def run(self, input_data: Any) -> Dict[str, Any]:
        vertices, edges, source = self._parse_input(input_data)

        dist = {v: float("inf") for v in vertices}
        parent = {v: None for v in vertices}
        dist[source] = 0.0

        n = len(vertices)

        # Relax all edges |V| - 1 times
        for _ in range(n - 1):
            updated = False
            for edge in edges:
                u, v, w = str(edge[0]), str(edge[1]), float(edge[2])
                if dist[u] != float("inf") and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    parent[v] = u
                    updated = True
            if not updated:
                break

        # Check for negative weight cycles on V-th pass
        has_negative_cycle = False
        for edge in edges:
            u, v, w = str(edge[0]), str(edge[1]), float(edge[2])
            if dist[u] != float("inf") and dist[u] + w < dist[v]:
                has_negative_cycle = True
                break

        formatted_dist = {k: (v if v != float("inf") else -1) for k, v in dist.items()}
        return {
            "source": source,
            "distances": formatted_dist,
            "predecessors": parent,
            "has_negative_cycle": has_negative_cycle
        }

    def run_instrumented(self, input_data: Any, max_steps: int = 500) -> AlgorithmExecutionResult:
        vertices, edges, source = self._parse_input(input_data)

        metrics = ExecutionMetrics()
        steps: List[ExecutionStep] = []
        step_id = 0

        dist = {v: float("inf") for v in vertices}
        parent = {v: None for v in vertices}
        dist[source] = 0.0
        n = len(vertices)

        steps.append(ExecutionStep(
            step_id=step_id,
            action="init",
            indices=[source],
            state_snapshot={k: (v if v != float("inf") else "inf") for k, v in dist.items()},
            description=f"Initialized Bellman-Ford distances from source '{source}'. Running up to {n-1} relaxation passes."
        ))
        step_id += 1

        for i in range(n - 1):
            updated = False
            for edge in edges:
                metrics.operations += 1
                u, v, w = str(edge[0]), str(edge[1]), float(edge[2])

                if dist[u] != float("inf"):
                    metrics.comparisons += 1
                    if dist[u] + w < dist[v]:
                        old_d = dist[v]
                        dist[v] = dist[u] + w
                        parent[v] = u
                        updated = True

                        if len(steps) < max_steps:
                            steps.append(ExecutionStep(
                                step_id=step_id,
                                action="relax_edge",
                                indices=[u, v],
                                values=[w, dist[v]],
                                state_snapshot={k: (val if val != float("inf") else "inf") for k, val in dist.items()},
                                description=f"Pass {i+1}: Relaxed ({u} -> {v}, wt={w}): dist[{v}] reduced from {old_d if old_d != float('inf') else 'inf'} to {dist[v]}.",
                                highlight_line=5
                            ))
                            step_id += 1

            if not updated:
                if len(steps) < max_steps:
                    steps.append(ExecutionStep(
                        step_id=step_id,
                        action="early_converge",
                        state_snapshot={k: (val if val != float("inf") else "inf") for k, val in dist.items()},
                        description=f"Early convergence achieved at pass {i+1}. No further edge relaxations possible."
                    ))
                    step_id += 1
                break

        has_negative_cycle = False
        for edge in edges:
            u, v, w = str(edge[0]), str(edge[1]), float(edge[2])
            if dist[u] != float("inf") and dist[u] + w < dist[v]:
                has_negative_cycle = True
                if len(steps) < max_steps:
                    steps.append(ExecutionStep(
                        step_id=step_id,
                        action="negative_cycle_found",
                        indices=[u, v],
                        values=[w],
                        description=f"Negative cycle detected! Edge ({u} -> {v}) can still be relaxed after {n-1} passes."
                    ))
                    step_id += 1
                break

        formatted_dist = {k: (v if v != float("inf") else -1) for k, v in dist.items()}
        out = {
            "source": source,
            "distances": formatted_dist,
            "predecessors": parent,
            "has_negative_cycle": has_negative_cycle
        }
        return AlgorithmExecutionResult(
            algorithm_slug=self.slug,
            output=out,
            metrics=metrics,
            steps=steps
        )
