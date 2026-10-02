"""
Input Data Characteristics Analyzer.
Extracts mathematical and structural traits (size, sortedness, range, sparsity, negative weights, etc.)
to guide heuristic recommendation scoring.
"""
import math
from typing import Any, Dict, List


class InputAnalyzer:
    """
    Inspects user input data and derives structural properties.
    """

    @classmethod
    def analyze(cls, input_data: Any) -> Dict[str, Any]:
        """
        Derives comprehensive dataset metadata from raw input.
        """
        properties: Dict[str, Any] = {
            "type": "unknown",
            "size": 0,
            "is_sorted": False,
            "sortedness_ratio": 0.0,
            "is_reverse_sorted": False,
            "is_nearly_sorted": False,
            "has_duplicates": False,
            "duplicate_ratio": 0.0,
            "is_integer_only": False,
            "min_val": None,
            "max_val": None,
            "value_range": None,
            "has_negative_values": False,
            "graph_vertices": 0,
            "graph_edges": 0,
            "graph_density": 0.0,
            "has_negative_weights": False,
        }

        # Case 1: Simple 1D list (Sorting / Searching / Array DP)
        if isinstance(input_data, list):
            cls._analyze_list(input_data, properties)

        # Case 2: Dictionary input (e.g. searching, knapsack, graph)
        elif isinstance(input_data, dict):
            if "array" in input_data and isinstance(input_data["array"], list):
                cls._analyze_list(input_data["array"], properties)
            elif "vertices" in input_data and "edges" in input_data:
                cls._analyze_graph(input_data, properties)
            elif "weights" in input_data and "values" in input_data:
                cls._analyze_knapsack(input_data, properties)
            elif "matrix_a" in input_data:
                cls._analyze_matrix(input_data, properties)
            elif "n" in input_data:
                properties["type"] = "scalar"
                properties["size"] = int(input_data["n"])

        return properties

    @classmethod
    def _analyze_list(cls, arr: List[Any], props: Dict[str, Any]):
        n = len(arr)
        props["type"] = "array"
        props["size"] = n

        if n == 0:
            return

        # Check numeric
        all_numeric = all(isinstance(x, (int, float)) for x in arr)
        all_integers = all(isinstance(x, int) for x in arr)
        props["is_integer_only"] = all_integers

        if all_numeric:
            min_v = min(arr)
            max_v = max(arr)
            props["min_val"] = min_v
            props["max_val"] = max_v
            props["value_range"] = max_v - min_v
            props["has_negative_values"] = min_v < 0

            # Count inversions or sorted pairs for sortedness ratio
            if n > 1:
                sorted_pairs = sum(1 for i in range(n - 1) if arr[i] <= arr[i + 1])
                sorted_ratio = sorted_pairs / (n - 1)
                props["sortedness_ratio"] = round(sorted_ratio, 4)
                props["is_sorted"] = sorted_ratio == 1.0
                props["is_nearly_sorted"] = sorted_ratio >= 0.85

                rev_pairs = sum(1 for i in range(n - 1) if arr[i] >= arr[i + 1])
                props["is_reverse_sorted"] = (rev_pairs / (n - 1)) == 1.0
            else:
                props["sortedness_ratio"] = 1.0
                props["is_sorted"] = True

            # Duplicate ratio
            unique_count = len(set(arr))
            props["has_duplicates"] = unique_count < n
            props["duplicate_ratio"] = round(1.0 - (unique_count / n), 4)

    @classmethod
    def _analyze_graph(cls, data: Dict[str, Any], props: Dict[str, Any]):
        props["type"] = "graph"
        v = len(data.get("vertices", []))
        edges = data.get("edges", [])
        e = len(edges)

        props["graph_vertices"] = v
        props["graph_edges"] = e
        props["size"] = v

        if v > 1:
            max_possible_edges = v * (v - 1)
            props["graph_density"] = round(e / max_possible_edges, 4) if max_possible_edges > 0 else 0.0

        # Negative weights check
        has_neg = False
        for edge in edges:
            if isinstance(edge, (list, tuple)) and len(edge) >= 3:
                if edge[2] < 0:
                    has_neg = True
                    break
            elif isinstance(edge, dict):
                w = edge.get("weight", edge.get("w", edge.get("cost", 0)))
                if w < 0:
                    has_neg = True
                    break
        props["has_negative_weights"] = has_neg

    @classmethod
    def _analyze_knapsack(cls, data: Dict[str, Any], props: Dict[str, Any]):
        props["type"] = "knapsack"
        weights = data.get("weights", [])
        props["size"] = len(weights)
        props["capacity"] = data.get("capacity", 0)

    @classmethod
    def _analyze_matrix(cls, data: Dict[str, Any], props: Dict[str, Any]):
        props["type"] = "matrix"
        mat = data.get("matrix_a", [])
        props["size"] = len(mat)
        if len(mat) > 0:
            props["matrix_dim"] = (len(mat), len(mat[0]))
