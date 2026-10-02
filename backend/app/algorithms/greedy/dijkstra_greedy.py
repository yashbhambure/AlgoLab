"""
Dijkstra's Single Source Shortest Path Implementation (Greedy)
"""
import heapq
from typing import Dict, Any, List
from collections import defaultdict
from app.algorithms.base import BaseAlgorithm, ExecutionMetrics, ExecutionStep, AlgorithmExecutionResult


class DijkstraGreedy(BaseAlgorithm):
    slug = "dijkstra-sssp"
    name = "Dijkstra's Algorithm (SSSP)"
    category = "Graph"
    paradigm = "Greedy"

    def _parse_input(self, input_data: Any):
        if isinstance(input_data, dict):
            vertices = [str(v) for v in input_data.get("vertices", [])]
            raw_edges = input_data.get("edges", [])
            source = str(input_data.get("source", input_data.get("start_vertex", vertices[0] if vertices else "0")))
            is_directed = input_data.get("is_directed", False)
        else:
            if isinstance(input_data, (list, tuple)) and len(input_data) >= 3:
                vertices, raw_edges, source = input_data[0], input_data[1], input_data[2]
            else:
                vertices, raw_edges = input_data
                source = vertices[0] if vertices else "0"
            vertices = [str(v) for v in vertices]
            source = str(source)
            is_directed = False

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
        return vertices, edges, source, is_directed

    def run(self, input_data: Any) -> Dict[str, Any]:
        vertices, edges, source, is_directed = self._parse_input(input_data)

        adj = defaultdict(list)
        for u, v, w in edges:
            u_str, v_str = str(u), str(v)
            adj[u_str].append((v_str, float(w)))
            # Assume undirected if not specified in flags
            if not is_directed:
                adj[v_str].append((u_str, float(w)))

        dist = {v: float("inf") for v in vertices}
        parent = {v: None for v in vertices}
        dist[source] = 0.0

        pq = [(0.0, source)]

        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue

            for v, weight in adj[u]:
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    parent[v] = u
                    heapq.heappush(pq, (dist[v], v))

        # Format distances for JSON response
        formatted_dist = {k: (v if v != float("inf") else -1) for k, v in dist.items()}
        return {
            "source": source,
            "distances": formatted_dist,
            "predecessors": parent
        }

    def run_instrumented(self, input_data: Any, max_steps: int = 500) -> AlgorithmExecutionResult:
        vertices, edges, source, is_directed = self._parse_input(input_data)

        metrics = ExecutionMetrics()
        steps: List[ExecutionStep] = []
        step_id = 0

        adj = defaultdict(list)
        for u, v, w in edges:
            u_str, v_str = str(u), str(v)
            adj[u_str].append((v_str, float(w)))
            if not is_directed:
                adj[v_str].append((u_str, float(w)))

        dist = {v: float("inf") for v in vertices}
        parent = {v: None for v in vertices}
        dist[source] = 0.0

        steps.append(ExecutionStep(
            step_id=step_id,
            action="init",
            indices=[source],
            state_snapshot={k: (v if v != float("inf") else "inf") for k, v in dist.items()},
            description=f"Initialized Dijkstra shortest path distances from source vertex '{source}'."
        ))
        step_id += 1

        pq = [(0.0, source)]

        while pq:
            d, u = heapq.heappop(pq)
            metrics.operations += 1

            if d > dist[u]:
                continue

            if len(steps) < max_steps:
                steps.append(ExecutionStep(
                    step_id=step_id,
                    action="extract_min",
                    indices=[u],
                    values=[d],
                    state_snapshot={k: (v if v != float("inf") else "inf") for k, v in dist.items()},
                    description=f"Extracted minimum distance vertex '{u}' (dist={d}) from Priority Queue.",
                    highlight_line=4
                ))
                step_id += 1

            for v, weight in adj[u]:
                metrics.comparisons += 1
                metrics.operations += 1

                if dist[u] + weight < dist[v]:
                    old_dist = dist[v]
                    dist[v] = dist[u] + weight
                    parent[v] = u
                    heapq.heappush(pq, (dist[v], v))

                    if len(steps) < max_steps:
                        steps.append(ExecutionStep(
                            step_id=step_id,
                            action="relax_edge",
                            indices=[u, v],
                            values=[weight, dist[v]],
                            state_snapshot={k: (v_d if v_d != float("inf") else "inf") for k, v_d in dist.items()},
                            description=f"Relaxed edge ({u} -> {v}, wt={weight}): updated dist[{v}] from {old_dist if old_dist != float('inf') else 'inf'} to {dist[v]}.",
                            highlight_line=8
                        ))
                        step_id += 1

        formatted_dist = {k: (v if v != float("inf") else -1) for k, v in dist.items()}
        out = {
            "source": source,
            "distances": formatted_dist,
            "predecessors": parent
        }
        return AlgorithmExecutionResult(
            algorithm_slug=self.slug,
            output=out,
            metrics=metrics,
            steps=steps
        )
