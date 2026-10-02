"""
Kruskal's Minimum Spanning Tree Algorithm (Greedy + Disjoint Set Union)
"""
from typing import Dict, Any, List
from app.algorithms.base import BaseAlgorithm, ExecutionMetrics, ExecutionStep, AlgorithmExecutionResult


class DisjointSetUnion:
    def __init__(self, elements: List[Any]):
        self.parent = {el: el for el in elements}
        self.rank = {el: 0 for el in elements}

    def find(self, i: Any) -> Any:
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])  # Path compression
        return self.parent[i]

    def union(self, i: Any, j: Any) -> bool:
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            # Union by rank
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_j] = root_i
                self.rank[root_i] += 1
            return True
        return False


class KruskalMST(BaseAlgorithm):
    slug = "kruskal-mst"
    name = "Kruskal's Algorithm (MST)"
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

        # Edges format: [u, v, weight]
        sorted_edges = sorted(edges, key=lambda x: x[2])
        dsu = DisjointSetUnion(vertices)

        mst = []
        total_weight = 0

        for u, v, w in sorted_edges:
            u_str, v_str = str(u), str(v)
            if dsu.find(u_str) != dsu.find(v_str):
                dsu.union(u_str, v_str)
                mst.append([u_str, v_str, w])
                total_weight += w
                if len(mst) == len(vertices) - 1:
                    break

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

        sorted_edges = sorted(edges, key=lambda x: x[2])
        metrics.operations += len(edges)
        dsu = DisjointSetUnion(vertices)

        steps.append(ExecutionStep(
            step_id=step_id,
            action="sort_edges",
            state_snapshot=sorted_edges,
            description=f"Sorted {len(sorted_edges)} edges ascending by weight for Kruskal greedy selection."
        ))
        step_id += 1

        mst = []
        total_weight = 0

        for u, v, w in sorted_edges:
            metrics.comparisons += 1
            metrics.operations += 1
            u_str, v_str = str(u), str(v)

            root_u = dsu.find(u_str)
            root_v = dsu.find(v_str)

            if root_u != root_v:
                dsu.union(u_str, v_str)
                mst.append([u_str, v_str, w])
                total_weight += w

                if len(steps) < max_steps:
                    steps.append(ExecutionStep(
                        step_id=step_id,
                        action="add_edge",
                        indices=[u_str, v_str],
                        values=[w],
                        state_snapshot=list(mst),
                        description=f"Edge ({u_str}, {v_str}, wt={w}) connects different components ({root_u} and {root_v}). Added to MST.",
                        highlight_line=5
                    ))
                    step_id += 1

                if len(mst) == len(vertices) - 1:
                    break
            else:
                if len(steps) < max_steps:
                    steps.append(ExecutionStep(
                        step_id=step_id,
                        action="reject_cycle",
                        indices=[u_str, v_str],
                        values=[w],
                        state_snapshot=list(mst),
                        description=f"Edge ({u_str}, {v_str}, wt={w}) rejected because vertices are already in same component ({root_u}). Prevents cycle."
                    ))
                    step_id += 1

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
