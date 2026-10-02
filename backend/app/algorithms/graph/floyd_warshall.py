"""
Floyd-Warshall Algorithm Implementation (All-Pairs Shortest Path DP)
"""
from typing import Dict, Any, List
from app.algorithms.base import BaseAlgorithm, ExecutionMetrics, ExecutionStep, AlgorithmExecutionResult


class FloydWarshall(BaseAlgorithm):
    slug = "floyd-warshall-apsp"
    name = "Floyd-Warshall Algorithm (APSP)"
    category = "Graph"
    paradigm = "Dynamic Programming"

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
                if len(e) >= 3:
                    edges.append(list(e))
                elif len(e) == 2:
                    edges.append([e[0], e[1], 1])
        return vertices, edges

    def run(self, input_data: Any) -> Dict[str, Any]:
        vertices: List[str] = []
        if isinstance(input_data, dict) and "matrix" in input_data:
            matrix = input_data["matrix"]
            n = len(matrix)
            dist = [[float(val) if val != "inf" else float("inf") for val in row] for row in matrix]
            if "vertices" in input_data and len(input_data["vertices"]) == n:
                vertices = [str(v) for v in input_data["vertices"]]
            else:
                vertices = [str(i) for i in range(n)]
        elif isinstance(input_data, list) and len(input_data) > 0 and isinstance(input_data[0], list):
            matrix = input_data
            n = len(matrix)
            dist = [[float(val) for val in row] for row in matrix]
            vertices = [str(i) for i in range(n)]
        else:
            vertices, edges = self._parse_input(input_data)
            n = len(vertices)
            v_map = {v: i for i, v in enumerate(vertices)}
            dist = [[0.0 if i == j else float("inf") for j in range(n)] for i in range(n)]
            is_directed = input_data.get("is_directed", True) if isinstance(input_data, dict) else True
            for edge in edges:
                u, v, w = str(edge[0]), str(edge[1]), float(edge[2])
                if u in v_map and v in v_map:
                    dist[v_map[u]][v_map[v]] = w
                    if not is_directed:
                        dist[v_map[v]][v_map[u]] = w

        # 3-nested loops over intermediate vertices k
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] != float("inf") and dist[k][j] != float("inf"):
                        if dist[i][k] + dist[k][j] < dist[i][j]:
                            dist[i][j] = dist[i][k] + dist[k][j]

        # Clean output
        output_matrix = [[val if val != float("inf") else -1 for val in row] for row in dist]
        if vertices and len(vertices) == n:
            dist_dict = {vertices[i]: {vertices[j]: (dist[i][j] if dist[i][j] != float("inf") else -1) for j in range(n)} for i in range(n)}
        else:
            dist_dict = {}

        return {
            "matrix_size": n,
            "distance_matrix": dist_dict if dist_dict else output_matrix,
            "distance_matrix_list": output_matrix
        }

    def run_instrumented(self, input_data: Any, max_steps: int = 500) -> AlgorithmExecutionResult:
        vertices: List[str] = []
        if isinstance(input_data, dict) and "matrix" in input_data:
            matrix = input_data["matrix"]
            n = len(matrix)
            dist = [[float(val) if val != "inf" else float("inf") for val in row] for row in matrix]
            if "vertices" in input_data and len(input_data["vertices"]) == n:
                vertices = [str(v) for v in input_data["vertices"]]
            else:
                vertices = [str(i) for i in range(n)]
        elif isinstance(input_data, list) and len(input_data) > 0 and isinstance(input_data[0], list):
            matrix = input_data
            n = len(matrix)
            dist = [[float(val) for val in row] for row in matrix]
            vertices = [str(i) for i in range(n)]
        else:
            vertices, edges = self._parse_input(input_data)
            n = len(vertices)
            v_map = {v: i for i, v in enumerate(vertices)}
            dist = [[0.0 if i == j else float("inf") for j in range(n)] for i in range(n)]
            is_directed = input_data.get("is_directed", True) if isinstance(input_data, dict) else True
            for edge in edges:
                u, v, w = str(edge[0]), str(edge[1]), float(edge[2])
                if u in v_map and v in v_map:
                    dist[v_map[u]][v_map[v]] = w
                    if not is_directed:
                        dist[v_map[v]][v_map[u]] = w

        metrics = ExecutionMetrics()
        steps: List[ExecutionStep] = []
        step_id = 0

        steps.append(ExecutionStep(
            step_id=step_id,
            action="init",
            state_snapshot=[[v if v != float("inf") else "inf" for v in row] for row in dist],
            description=f"Initialized Floyd-Warshall distance matrix D^(0) of dimension {n}x{n}."
        ))
        step_id += 1

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    metrics.operations += 1
                    if dist[i][k] != float("inf") and dist[k][j] != float("inf"):
                        metrics.comparisons += 1
                        if dist[i][k] + dist[k][j] < dist[i][j]:
                            old_d = dist[i][j]
                            dist[i][j] = dist[i][k] + dist[k][j]

                            if len(steps) < max_steps:
                                steps.append(ExecutionStep(
                                    step_id=step_id,
                                    action="update_cell",
                                    indices=[i, j, k],
                                    values=[old_d, dist[i][j]],
                                    state_snapshot=[[v if v != float("inf") else "inf" for v in r] for r in dist],
                                    description=f"Via intermediate vertex {k}: path ({i}->{j}) shortened from {old_d if old_d != float('inf') else 'inf'} to {dist[i][j]}.",
                                    highlight_line=5
                                ))
                                step_id += 1

        output_matrix = [[val if val != float("inf") else -1 for val in row] for row in dist]
        if vertices and len(vertices) == n:
            dist_dict = {vertices[i]: {vertices[j]: (dist[i][j] if dist[i][j] != float("inf") else -1) for j in range(n)} for i in range(n)}
        else:
            dist_dict = {}

        out = {
            "matrix_size": n,
            "distance_matrix": dist_dict if dist_dict else output_matrix,
            "distance_matrix_list": output_matrix
        }
        return AlgorithmExecutionResult(
            algorithm_slug=self.slug,
            output=out,
            metrics=metrics,
            steps=steps
        )
