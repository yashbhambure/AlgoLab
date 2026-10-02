"""
Universal Problem-Aware Input Generators for DAA Benchmark Suite.
Generates mathematically valid, domain-constrained datasets tailored to each
canonical algorithmic problem and computational paradigm.
"""
import random
import math
from typing import Dict, Any, List, Optional, Tuple


def generate_sorting_input(size: int = 100, distribution: str = "random", min_val: int = 1, max_val: int = 1000) -> List[int]:
    """Generates 1D array for comparative sorting benchmarks."""
    n = max(2, size)
    dist = distribution.lower()
    if dist == "sorted":
        return sorted([random.randint(min_val, max_val) for _ in range(n)])
    elif dist == "reverse_sorted" or dist == "reversed":
        return sorted([random.randint(min_val, max_val) for _ in range(n)], reverse=True)
    elif dist == "nearly_sorted":
        arr = sorted([random.randint(min_val, max_val) for _ in range(n)])
        num_swaps = max(1, int(0.05 * n))
        for _ in range(num_swaps):
            i = random.randint(0, n - 1)
            j = random.randint(0, n - 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    elif dist == "duplicate_heavy" or dist == "few_unique":
        distinct = [random.randint(min_val, max_val) for _ in range(min(5, n))]
        return [random.choice(distinct) for _ in range(n)]
    else:
        return [random.randint(min_val, max_val) for _ in range(n)]


def generate_searching_input(size: int = 100, target_present: bool = True) -> Dict[str, Any]:
    """Generates sorted array and target key for searching algorithms."""
    arr = sorted([random.randint(1, max(1000, size * 10)) for _ in range(size)])
    # Deduplicate while preserving order if possible
    arr = sorted(list(set(arr)))
    if target_present and arr:
        target = random.choice(arr)
    else:
        target = (max(arr) + 10) if arr else 42
    return {"array": arr, "target": target}


def generate_knapsack_input(num_items: int = 10, max_weight: int = 30, max_value: int = 100) -> Dict[str, Any]:
    """Generates valid 0/1 and Fractional Knapsack payloads."""
    n = max(1, min(num_items, 1000))
    weights = [random.randint(1, max_weight) for _ in range(n)]
    values = [random.randint(5, max_value) for _ in range(n)]
    capacity = max(10, int(sum(weights) * 0.45))

    items = [
        {"name": f"I{i+1}", "weight": weights[i], "value": values[i]}
        for i in range(n)
    ]
    return {
        "weights": weights,
        "values": values,
        "capacity": capacity,
        "items": items
    }


def generate_tsp_input(num_cities: int = 5, max_dist: int = 50) -> Dict[str, Any]:
    """
    Generates symmetric distance matrix for TSP.
    Enforces safe bounds for exact bitmask DP and Branch & Bound solvers.
    """
    n = max(3, min(num_cities, 16))
    cities = [f"City_{chr(65 + i)}" if i < 26 else f"City_{i + 1}" for i in range(n)]

    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = random.randint(5, max_dist)
            matrix[i][j] = d
            matrix[j][i] = d

    return {
        "distance_matrix": matrix,
        "matrix": matrix,
        "cities": cities
    }


def generate_mst_input(num_vertices: int = 10, density: str = "medium") -> Dict[str, Any]:
    """
    Generates connected, weighted undirected graph for Kruskal and Prim MST algorithms.
    Ensures connectivity by constructing a spanning backbone before adding random edges.
    """
    v = max(3, min(num_vertices, 200))
    vertices = [str(i) for i in range(v)]
    edges_set = set()
    edge_list = []

    # 1. Random spanning tree backbone to guarantee graph connectivity
    for i in range(1, v):
        j = random.randint(0, i - 1)
        w = random.randint(1, 30)
        edges_set.add((min(j, i), max(j, i)))
        edge_list.append({"source": str(j), "target": str(i), "weight": w})

    # 2. Additional chord edges based on density
    prob = 0.4 if density == "dense" else 0.15
    for i in range(v):
        for j in range(i + 1, v):
            if (i, j) not in edges_set and random.random() < prob:
                w = random.randint(5, 50)
                edges_set.add((i, j))
                edge_list.append({"source": str(i), "target": str(j), "weight": w})

    return {
        "vertices": vertices,
        "edges": edge_list
    }


def generate_sssp_input(num_vertices: int = 8, allow_negative: bool = False) -> Dict[str, Any]:
    """
    Generates connected weighted graph with source vertex for Dijkstra and Bellman-Ford.
    Weights non-negative by default for Dijkstra safety.
    """
    v = max(3, min(num_vertices, 100))
    vertices = [chr(65 + i) if i < 26 else f"V{i}" for i in range(v)]
    edge_list = []
    edges_set = set()

    # Backbone tree from source
    for i in range(1, v):
        j = random.randint(0, i - 1)
        w = random.randint(1, 20)
        edges_set.add((j, i))
        edge_list.append({"source": vertices[j], "target": vertices[i], "weight": w})

    # Additional cross edges
    for i in range(v):
        for j in range(v):
            if i != j and (i, j) not in edges_set and random.random() < 0.25:
                w = random.randint(1, 30)
                edges_set.add((i, j))
                edge_list.append({"source": vertices[i], "target": vertices[j], "weight": w})

    return {
        "vertices": vertices,
        "edges": edge_list,
        "source": vertices[0]
    }


def generate_apsp_input(num_vertices: int = 6) -> Dict[str, Any]:
    """Generates weighted adjacency matrix and graph for Floyd-Warshall APSP."""
    v = max(3, min(num_vertices, 50))
    vertices = [chr(65 + i) if i < 26 else f"V{i}" for i in range(v)]
    matrix = [[float('inf')] * v for _ in range(v)]
    edge_list = []

    for i in range(v):
        matrix[i][i] = 0

    for i in range(v):
        for j in range(v):
            if i != j and random.random() < 0.4:
                w = random.randint(1, 20)
                matrix[i][j] = w
                edge_list.append({"source": vertices[i], "target": vertices[j], "weight": w})

    return {
        "vertices": vertices,
        "edges": edge_list,
        "matrix": matrix
    }


def generate_n_queens_input(n: int = 8) -> Dict[str, Any]:
    """Generates valid N-Queens problem dimension."""
    safe_n = max(4, min(n, 14))
    return {"n": safe_n}


def generate_subset_sum_input(size: int = 8) -> Dict[str, Any]:
    """
    Generates realistic subset sum instance.
    Calculates target sum from a subset to preserve natural solvability characteristics.
    """
    n = max(4, min(size, 25))
    numbers = [random.randint(2, 35) for _ in range(n)]
    # Pick random subset to form realistic target sum
    k = max(2, n // 2)
    sample_sub = random.sample(numbers, k)
    target = sum(sample_sub)

    return {
        "numbers": numbers,
        "array": numbers,
        "target_sum": target,
        "target": target
    }


def generate_hamiltonian_cycle_input(num_vertices: int = 5) -> Dict[str, Any]:
    """Generates graph with a guaranteed Hamiltonian cycle plus random chord edges."""
    v = max(4, min(num_vertices, 10))
    vertices = [chr(65 + i) if i < 26 else f"V{i}" for i in range(v)]
    edges_set = set()
    edge_list = []

    # Base cycle: 0-1, 1-2, ..., (v-1)-0
    for i in range(v):
        next_v = (i + 1) % v
        u_str, v_str = vertices[i], vertices[next_v]
        edges_set.add((min(u_str, v_str), max(u_str, v_str)))
        edge_list.append({"source": u_str, "target": v_str})

    # Add extra random chords
    for i in range(v):
        for j in range(i + 2, v):
            if (i, j) != (0, v - 1) and random.random() < 0.3:
                u_str, v_str = vertices[i], vertices[j]
                if (min(u_str, v_str), max(u_str, v_str)) not in edges_set:
                    edges_set.add((min(u_str, v_str), max(u_str, v_str)))
                    edge_list.append({"source": u_str, "target": v_str})

    return {
        "vertices": vertices,
        "edges": edge_list
    }


def generate_strassen_input(power_of_two_dim: int = 4) -> Dict[str, Any]:
    """Generates 2^k x 2^k square matrices for Strassen multiplication."""
    dim = 2 ** max(1, min(int(math.log2(max(2, power_of_two_dim))), 5))
    mat_a = [[random.randint(1, 10) for _ in range(dim)] for _ in range(dim)]
    mat_b = [[random.randint(1, 10) for _ in range(dim)] for _ in range(dim)]
    return {
        "matrix_a": mat_a,
        "matrix_b": mat_b
    }


def generate_defective_chessboard_input(board_size: int = 4) -> Dict[str, Any]:
    """Generates 2^k x 2^k board with a defective cell coordinate."""
    size = 2 ** max(1, min(int(math.log2(max(2, board_size))), 4))
    r = random.randint(0, size - 1)
    c = random.randint(0, size - 1)
    return {
        "size": size,
        "defect": [r, c]
    }


def generate_max_min_input(size: int = 8) -> List[int]:
    """Generates array of distinct integers for Divide & Conquer Min-Max."""
    return [random.randint(-100, 500) for _ in range(max(2, size))]


def generate_job_sequencing_input(num_jobs: int = 5) -> Dict[str, Any]:
    """Generates jobs with profits and deadlines."""
    n = max(2, min(num_jobs, 30))
    jobs = []
    for i in range(n):
        jobs.append({
            "id": f"J{i+1}",
            "deadline": random.randint(1, max(2, n // 2)),
            "profit": random.randint(10, 150)
        })
    return {"jobs": jobs}


def generate_optimal_merge_input(num_files: int = 5) -> Dict[str, Any]:
    """Generates file sizes for 2-way min-heap optimal merge patterns."""
    n = max(2, min(num_files, 50))
    files = [random.randint(5, 100) for _ in range(n)]
    names = [f"F{i+1}" for i in range(n)]
    return {"files": files, "names": names}


def generate_optimal_storage_tapes_input(num_programs: int = 6, num_tapes: int = 1) -> Dict[str, Any]:
    """Generates program lengths for tape retrieval time optimization."""
    n = max(2, min(num_programs, 50))
    lengths = [random.randint(2, 50) for _ in range(n)]
    programs = [f"P{i+1}" for i in range(n)]
    return {"lengths": lengths, "tapes": num_tapes, "programs": programs}


def generate_optimal_bst_input(num_keys: int = 4) -> Dict[str, Any]:
    """Generates key probabilities p and dummy key probabilities q for OBST."""
    n = max(2, min(num_keys, 10))
    raw_p = [random.randint(5, 20) for _ in range(n)]
    raw_q = [random.randint(1, 10) for _ in range(n + 1)]
    total = sum(raw_p) + sum(raw_q)
    p = [round(v / total, 3) for v in raw_p]
    q = [round(v / total, 3) for v in raw_q]
    return {
        "keys": [f"k{i+1}" for i in range(n)],
        "p": p,
        "q": q
    }


def generate_multistage_graph_input(stages: int = 4, vertices_per_stage: int = 2) -> Dict[str, Any]:
    """Generates directed multistage graph from stage 1 (source) to stage k (sink)."""
    k = max(3, min(stages, 6))
    stage_nodes: List[List[int]] = []
    cur_id = 1

    # Source stage: 1 node
    stage_nodes.append([cur_id])
    cur_id += 1

    # Intermediate stages
    for _ in range(k - 2):
        nodes = []
        for _ in range(vertices_per_stage):
            nodes.append(cur_id)
            cur_id += 1
        stage_nodes.append(nodes)

    # Sink stage: 1 node
    stage_nodes.append([cur_id])
    total_vertices = cur_id

    edges = []
    for s in range(k - 1):
        u_nodes = stage_nodes[s]
        v_nodes = stage_nodes[s + 1]
        for u in u_nodes:
            for v in v_nodes:
                if random.random() < 0.75:
                    edges.append({"from": u, "to": v, "weight": random.randint(1, 15)})

    # Ensure each node has at least one outgoing and incoming edge
    for s in range(k - 1):
        u_nodes = stage_nodes[s]
        v_nodes = stage_nodes[s + 1]
        for u in u_nodes:
            if not any(e["from"] == u for e in edges):
                edges.append({"from": u, "to": random.choice(v_nodes), "weight": random.randint(1, 15)})
        for v in v_nodes:
            if not any(e["to"] == v for e in edges):
                edges.append({"from": random.choice(u_nodes), "to": v, "weight": random.randint(1, 15)})

    return {
        "num_vertices": total_vertices,
        "stages": k,
        "edges": edges
    }


def generate_reliability_design_input(num_stages: int = 3, budget: int = 100) -> Dict[str, Any]:
    """Generates reliability stage probabilities and costs."""
    n = max(2, min(num_stages, 6))
    reliabilities = [round(random.uniform(0.7, 0.95), 2) for _ in range(n)]
    costs = [random.randint(10, 30) for _ in range(n)]
    req_budget = max(budget, int(sum(costs) * 1.5))
    return {
        "reliabilities": reliabilities,
        "costs": costs,
        "budget": req_budget
    }


def generate_problem_input(problem_slug: str, size: int = 10, **kwargs) -> Any:
    """
    Master dispatcher to generate a valid, authoritative input payload for any
    canonical problem or supplementary category.
    """
    clean_slug = problem_slug.lower().strip()

    if clean_slug in ("0-1-knapsack-problem", "0-1-knapsack", "knapsack"):
        return generate_knapsack_input(num_items=size)
    elif clean_slug in ("traveling-salesman-problem", "traveling-salesman", "tsp"):
        return generate_tsp_input(num_cities=size)
    elif clean_slug in ("minimum-spanning-tree", "mst"):
        return generate_mst_input(num_vertices=size)
    elif clean_slug in ("single-source-shortest-path", "sssp"):
        return generate_sssp_input(num_vertices=size)
    elif clean_slug in ("all-pairs-shortest-path", "apsp"):
        return generate_apsp_input(num_vertices=size)
    elif clean_slug in ("n-queens-problem", "n-queens"):
        return generate_n_queens_input(n=size)
    elif clean_slug in ("subset-sum-problem", "subset-sum"):
        return generate_subset_sum_input(size=size)
    elif clean_slug in ("hamiltonian-cycle-problem", "hamiltonian-cycle"):
        return generate_hamiltonian_cycle_input(num_vertices=size)
    elif clean_slug in ("matrix-multiplication-problem", "strassen-matrix-multiplication", "strassen"):
        return generate_strassen_input(power_of_two_dim=size)
    elif clean_slug in ("defective-chessboard-problem", "defective-chessboard"):
        return generate_defective_chessboard_input(board_size=size)
    elif clean_slug in ("max-min-problem", "max-min"):
        return generate_max_min_input(size=size)
    elif clean_slug in ("fractional-knapsack-problem", "fractional-knapsack"):
        return generate_knapsack_input(num_items=size)
    elif clean_slug in ("job-sequencing-problem", "job-sequencing"):
        return generate_job_sequencing_input(num_jobs=size)
    elif clean_slug in ("optimal-merge-patterns-problem", "optimal-merge-patterns"):
        return generate_optimal_merge_input(num_files=size)
    elif clean_slug in ("optimal-storage-tapes-problem", "optimal-storage-tapes"):
        return generate_optimal_storage_tapes_input(num_programs=size)
    elif clean_slug in ("optimal-bst-problem", "optimal-bst"):
        return generate_optimal_bst_input(num_keys=size)
    elif clean_slug in ("multistage-graph-problem", "multistage-graph"):
        return generate_multistage_graph_input(stages=size)
    elif clean_slug in ("reliability-design-problem", "reliability-design"):
        return generate_reliability_design_input(num_stages=size)
    elif clean_slug in ("array-sorting", "sorting"):
        dist = kwargs.get("distribution", "random")
        return generate_sorting_input(size=size, distribution=dist)
    elif clean_slug in ("element-searching", "searching"):
        return generate_searching_input(size=size)
    else:
        # Fallback to sorting array
        return generate_sorting_input(size=size)
