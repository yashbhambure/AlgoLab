"""
Multistage Graph Problem Implementation (Dynamic Programming O(V + E))
Finds the minimum cost path from source to sink across k partitioned stages.
"""
from typing import Dict, Any, List, Optional
from app.algorithms.base import BaseAlgorithm, ExecutionMetrics, ExecutionStep, AlgorithmExecutionResult


class MultistageGraphDP(BaseAlgorithm):
    slug = "multistage-graph-dp"
    name = "Multistage Graph (Dynamic Programming)"
    category = "Dynamic Programming"
    paradigm = "Dynamic Programming"

    time_complexity_best = "O(V + E)"
    time_complexity_average = "O(V + E)"
    time_complexity_worst = "O(V^2)"
    space_complexity = "O(V)"
    is_stable = True
    is_in_place = False

    def _parse_input(self, input_data: Any):
        """Parse multistage graph representation."""
        if isinstance(input_data, dict):
            num_vertices = input_data.get("num_vertices", input_data.get("n", 8))
            edges = input_data.get("edges", [])
            stages = input_data.get("stages", 4)
            stage_map = input_data.get("stage_map", {})
            source = input_data.get("source", 1)
            sink = input_data.get("sink", num_vertices)
        else:
            # Default canonical textbook 4-stage 8-vertex graph
            num_vertices = 8
            stages = 4
            source = 1
            sink = 8
            stage_map = {1: 1, 2: 2, 3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 4}
            edges = [
                {"from": 1, "to": 2, "weight": 2},
                {"from": 1, "to": 3, "weight": 1},
                {"from": 1, "to": 4, "weight": 3},
                {"from": 2, "to": 5, "weight": 2},
                {"from": 2, "to": 6, "weight": 3},
                {"from": 3, "to": 5, "weight": 6},
                {"from": 3, "to": 6, "weight": 7},
                {"from": 4, "to": 6, "weight": 6},
                {"from": 4, "to": 7, "weight": 8},
                {"from": 5, "to": 8, "weight": 1},
                {"from": 6, "to": 8, "weight": 4},
                {"from": 7, "to": 8, "weight": 2},
            ]

        # Build adjacency list
        adj: Dict[int, List[Dict[str, Any]]] = {i: [] for i in range(1, num_vertices + 1)}
        for e in edges:
            if isinstance(e, dict):
                u, v, w = e["from"], e["to"], e["weight"]
            else:
                u, v, w = e[0], e[1], e[2]
            if u in adj:
                adj[u].append({"to": v, "weight": w})

        return num_vertices, stages, source, sink, stage_map, adj, edges

    def run(self, input_data: Any) -> Dict[str, Any]:
        n, stages, source, sink, stage_map, adj, edges = self._parse_input(input_data)

        # Dynamic programming backward approach:
        # cost[i] = min_{j in outgoing(i)} { weight(i, j) + cost[j] }
        cost: Dict[int, float] = {i: float('inf') for i in range(1, n + 1)}
        next_hop: Dict[int, Optional[int]] = {i: None for i in range(1, n + 1)}
        cost[sink] = 0.0

        # Process vertices in reverse topological order (from sink backward to source)
        for u in range(n - 1, 0, -1):
            for edge in adj.get(u, []):
                v = edge["to"]
                w = edge["weight"]
                if cost[v] != float('inf') and w + cost[v] < cost[u]:
                    cost[u] = w + cost[v]
                    next_hop[u] = v

        # Reconstruct path
        path = []
        curr = source
        while curr is not None:
            path.append(curr)
            if curr == sink:
                break
            curr = next_hop[curr]

        return {
            "num_vertices": n,
            "stages": stages,
            "min_cost": cost[source] if cost[source] != float('inf') else None,
            "shortest_path": path,
            "path": path,
            "cost_table": {k: (v if v != float('inf') else None) for k, v in cost.items()},
            "next_hop_table": next_hop
        }

    def run_instrumented(self, input_data: Any, max_steps: int = 500) -> AlgorithmExecutionResult:
        n, stages, source, sink, stage_map, adj, edges = self._parse_input(input_data)
        metrics = ExecutionMetrics()
        steps: List[ExecutionStep] = []
        step_id = [0]

        cost: Dict[int, float] = {i: float('inf') for i in range(1, n + 1)}
        next_hop: Dict[int, Optional[int]] = {i: None for i in range(1, n + 1)}
        cost[sink] = 0.0

        steps.append(ExecutionStep(
            step_id=step_id[0],
            action="init",
            state_snapshot={"cost": {k: (v if v != float('inf') else "inf") for k, v in cost.items()}, "path": []},
            description=f"Initialized Multistage Graph DP. Sink node {sink} base cost = 0."
        ))
        step_id[0] += 1

        for u in range(n - 1, 0, -1):
            metrics.operations += 1
            outgoing = adj.get(u, [])
            if not outgoing:
                continue

            for edge in outgoing:
                metrics.comparisons += 1
                v = edge["to"]
                w = edge["weight"]

                candidate_cost = w + cost[v] if cost[v] != float('inf') else float('inf')

                if candidate_cost < cost[u]:
                    cost[u] = candidate_cost
                    next_hop[u] = v

                    if len(steps) < max_steps:
                        steps.append(ExecutionStep(
                            step_id=step_id[0],
                            action="update_dp",
                            indices=[u, v],
                            values=[w, cost[u]],
                            state_snapshot={"cost": {k: (v if v != float('inf') else "inf") for k, v in cost.items()}, "current_node": u},
                            description=f"Stage DP: Updated vertex {u} via neighbor {v}: cost({u}) = {w} + {cost[v]} = {cost[u]}.",
                            highlight_line=4
                        ))
                        step_id[0] += 1

        # Reconstruct path
        path = []
        curr = source
        while curr is not None:
            path.append(curr)
            if curr == sink:
                break
            curr = next_hop[curr]

        steps.append(ExecutionStep(
            step_id=step_id[0],
            action="reconstruct_path",
            state_snapshot={"shortest_path": path, "min_cost": cost[source]},
            description=f"Optimal multistage path reconstructed: {' -> '.join(map(str, path))} with total minimum cost {cost[source]}."
        ))
        step_id[0] += 1

        out = {
            "num_vertices": n,
            "stages": stages,
            "min_cost": cost[source] if cost[source] != float('inf') else None,
            "shortest_path": path,
            "cost_table": {k: (v if v != float('inf') else None) for k, v in cost.items()},
            "next_hop_table": next_hop
        }
        return AlgorithmExecutionResult(
            algorithm_slug=self.slug,
            output=out,
            metrics=metrics,
            steps=steps
        )
