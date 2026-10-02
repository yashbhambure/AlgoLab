"""
Prim's Minimum Spanning Tree Algorithm (Greedy + Priority Queue)
"""
import heapq
from typing import Dict, Any, List
from collections import defaultdict
from app.algorithms.base import BaseAlgorithm, ExecutionMetrics, ExecutionStep, AlgorithmExecutionResult


class PrimMST(BaseAlgorithm):
    slug = "prim-mst"
    name = "Prim's Algorithm (MST)"
    category = "Greedy"
    paradigm = "Greedy"

    def _parse_input(self, input_data: Any):
        if isinstance(input_data, dict):
            vertices = [str(v) for v in input_data.get("vertices", [])]
            raw_edges = input_data.get("edges", [])
        else:
            vertices, raw_edges = input_data
            vertices = [str(v) for v in vertices]

        edges = []
        for e in raw_edges:
            if isinstance(e, dict):
                u = e.get("source", e.get("u", e.get("from", 0)))
                v = e.get("target", e.get("v", e.get("to", 1)))
                w = e.get("weight", e.get("w", 1))
                edges.append([u, v, w])
            elif isinstance(e, (list, tuple)):
                edges.append(list(e))
        return vertices, edges

    def run(self, input_data: Any) -> Dict[str, Any]:
        vertices, edges = self._parse_input(input_data)

        if not vertices:
            return {"mst_edges": [], "total_weight": 0, "mst_weight": 0}

        # Build adjacency list
        adj = defaultdict(list)
        for u, v, w in edges:
            u_str, v_str = str(u), str(v)
            adj[u_str].append((v_str, w))
            adj[v_str].append((u_str, w))

        mst = []
        visited = set()
        total_weight = 0

        # Min-Heap stores (weight, from_vertex, to_vertex)
        start_v = vertices[0]
        visited.add(start_v)
        pq = []
        for neighbor, weight in adj[start_v]:
            heapq.heappush(pq, (weight, start_v, neighbor))

        while pq and len(visited) < len(vertices):
            weight, u, v = heapq.heappop(pq)
            if v in visited:
                continue

            visited.add(v)
            mst.append([u, v, weight])
            total_weight += weight

            for next_neighbor, next_w in adj[v]:
                if next_neighbor not in visited:
                    heapq.heappush(pq, (next_w, v, next_neighbor))

        return {
            "mst_edges": mst,
            "total_weight": total_weight,
            "mst_weight": total_weight,
            "is_connected": len(mst) == max(0, len(vertices) - 1)
        }

    def run_instrumented(self, input_data: Any, max_steps: int = 500) -> AlgorithmExecutionResult:
        vertices, edges = self._parse_input(input_data)

        metrics = ExecutionMetrics()
        steps: List[ExecutionStep] = []
        step_id = 0

        if not vertices:
            return AlgorithmExecutionResult(algorithm_slug=self.slug, output={}, metrics=metrics, steps=[])

        adj = defaultdict(list)
        for u, v, w in edges:
            u_str, v_str = str(u), str(v)
            adj[u_str].append((v_str, w))
            adj[v_str].append((u_str, w))

        mst = []
        visited = set()
        total_weight = 0

        start_v = vertices[0]
        visited.add(start_v)
        pq = []
        for neighbor, weight in adj[start_v]:
            heapq.heappush(pq, (weight, start_v, neighbor))

        steps.append(ExecutionStep(
            step_id=step_id,
            action="init_root",
            indices=[start_v],
            state_snapshot=list(visited),
            description=f"Prim's MST initialized at arbitrary root vertex '{start_v}'."
        ))
        step_id += 1

        while pq and len(visited) < len(vertices):
            metrics.comparisons += 1
            metrics.operations += 1
            weight, u, v = heapq.heappop(pq)

            if v in visited:
                continue

            visited.add(v)
            mst.append([u, v, weight])
            total_weight += weight

            if len(steps) < max_steps:
                steps.append(ExecutionStep(
                    step_id=step_id,
                    action="grow_cut",
                    indices=[u, v],
                    values=[weight],
                    state_snapshot=list(visited),
                    description=f"Cheapest cut-crossing edge ({u}, {v}, wt={weight}) added to MST. Vertex '{v}' absorbed.",
                    highlight_line=6
                ))
                step_id += 1

            for next_neighbor, next_w in adj[v]:
                if next_neighbor not in visited:
                    heapq.heappush(pq, (next_w, v, next_neighbor))
                    metrics.operations += 1

        out = {
            "mst_edges": mst,
            "total_weight": total_weight,
            "is_connected": len(mst) == max(0, len(vertices) - 1)
        }

        return AlgorithmExecutionResult(
            algorithm_slug=self.slug,
            output=out,
            metrics=metrics,
            steps=steps
        )
