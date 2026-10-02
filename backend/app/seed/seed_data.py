"""
Authoritative DAA Curriculum Seed Data Module
Populates the database strictly with the 23 executable algorithms across the 5 computational paradigms,
the 18 curriculum problem definitions, problem mappings, and default accounts.
"""
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.algorithm import Algorithm
from app.models.problem import Problem, AlgorithmProblemMapping
from app.core.security import hash_password

# ==========================================
# 1. COMPUTATIONAL PROBLEMS SEED DEFINITIONS
# ==========================================
PROBLEMS_DATA: List[Dict[str, Any]] = [
    {
        "slug": "defective-chessboard-problem",
        "name": "Defective Chessboard (Tromino Tiling)",
        "category": "Divide and Conquer",
        "paradigm": "Divide and Conquer",
        "description": "Tile a 2^k x 2^k board containing exactly one defective square using L-shaped trominoes via recursive quadrant decomposition.",
        "input_format": "Integer board size 2^k and defective cell coordinate (row, col)",
        "output_format": "2^k x 2^k grid with unique tromino tile numbers and defective cell marked",
        "constraints": "Size must be a power of 2 (2^k), 1 <= k <= 8.",
        "data_type": "board",
        "example_input": {"size": 4, "defect": [0, 0]},
        "example_output": {"grid": [[-1, 1, 2, 2], [1, 1, 3, 2], [4, 3, 3, 5], [4, 4, 5, 5]]},
        "daa_topics": ["Quadrant Decomposition", "Master Theorem Case 1", "Tromino Induction Proof"]
    },
    {
        "slug": "max-min-problem",
        "name": "Finding Maximum and Minimum",
        "category": "Divide and Conquer",
        "paradigm": "Divide and Conquer",
        "description": "Simultaneously find the minimum and maximum elements in an array using at most 3n/2 - 2 comparisons.",
        "input_format": "Array of N comparable numbers",
        "output_format": "Tuple containing (minimum_value, maximum_value) and comparison count",
        "constraints": "Array size N >= 1.",
        "data_type": "array",
        "example_input": [22, 13, -5, 88, 41, 7, 95, 3],
        "example_output": {"min": -5, "max": 95, "comparisons": 10},
        "daa_topics": ["Comparison Lower Bounds", "Divide & Conquer Recurrence T(n)=2T(n/2)+2", "Optimal Min-Max"]
    },
    {
        "slug": "matrix-multiplication-problem",
        "name": "Strassen's Matrix Multiplication",
        "category": "Divide and Conquer",
        "paradigm": "Divide and Conquer",
        "description": "Compute the product matrix C = A x B of two n x n square matrices with sub-cubic complexity using Strassen's 7-block recursive decomposition.",
        "input_format": "Two n x n matrices A and B",
        "output_format": "Product matrix C of dimension n x n",
        "constraints": "Dimension n is a power of 2, n <= 256.",
        "data_type": "matrix",
        "example_input": {
            "matrix_a": [[1, 2], [3, 4]],
            "matrix_b": [[5, 6], [7, 8]]
        },
        "example_output": [[19, 22], [43, 50]],
        "daa_topics": ["Strassen 7-Multiplication Decomposition", "Sub-cubic Asymptotic Bound O(n^2.8074)", "Master Theorem Case 1"]
    },
    {
        "slug": "n-queens-problem",
        "name": "N-Queens Problem",
        "category": "Backtracking",
        "paradigm": "Backtracking",
        "description": "Place N chess queens on an N x N chessboard so that no two queens attack each other (no two queens share the same row, column, or diagonal).",
        "input_format": "Integer N (board dimension and number of queens)",
        "output_format": "Board configurations or total number of valid solutions",
        "constraints": "N >= 1 (usually 4 <= N <= 14 for live backtracking exploration).",
        "data_type": "board",
        "example_input": {"n": 4},
        "example_output": {"total_solutions": 2, "sample_board": [1, 3, 0, 2]},
        "daa_topics": ["State Space Tree Exploration", "Constraint Pruning", "Depth-First Search with Backtracking"]
    },
    {
        "slug": "subset-sum-problem",
        "name": "Sum of Subsets Problem",
        "category": "Backtracking",
        "paradigm": "Backtracking",
        "description": "Determine if there is a subset of a given set of non-negative integers whose sum equals a given target sum S.",
        "input_format": "Array of integers and target sum S",
        "output_format": "Boolean indicating existence, and list of elements forming the subset",
        "constraints": "1 <= N <= 30 for exact backtracking, target sum S >= 0.",
        "data_type": "array",
        "example_input": {"array": [3, 34, 4, 12, 5, 2], "target": 9},
        "example_output": {"exists": True, "subset": [4, 5]},
        "daa_topics": ["NP-Complete Problem", "Branch and Bound / Pruning", "State Space Tree"]
    },
    {
        "slug": "hamiltonian-cycle-problem",
        "name": "Hamiltonian Cycle Problem",
        "category": "Backtracking",
        "paradigm": "Backtracking",
        "description": "Determine whether a given undirected graph contains a closed loop (Hamiltonian Cycle) visiting every vertex exactly once and returning to the start.",
        "input_format": "Graph G = (V, E)",
        "output_format": "Ordered sequence of vertices forming the cycle, or False if none exists",
        "constraints": "|V| <= 20 for exact backtracking.",
        "data_type": "graph",
        "example_input": {
            "vertices": ["A", "B", "C", "D"],
            "edges": [["A", "B"], ["B", "C"], ["C", "D"], ["D", "A"]]
        },
        "example_output": ["A", "B", "C", "D", "A"],
        "daa_topics": ["State-Space Adjacency Pruning", "NP-Complete Decision Problem", "Vertex Tour Verification"]
    },
    {
        "slug": "multistage-graph-problem",
        "name": "Multistage Graph Problem",
        "category": "Dynamic Programming",
        "paradigm": "Dynamic Programming",
        "description": "Find the minimum-cost path from source (stage 1) to sink (stage k) in a k-stage partitioned directed acyclic graph.",
        "input_format": "k-stage partitioned graph G = (V, E) with weighted edges",
        "output_format": "Minimum path cost and sequence of vertices from source to sink",
        "constraints": "k >= 2 stages, DAG structure.",
        "data_type": "graph",
        "example_input": {
            "num_vertices": 8,
            "stages": 4,
            "edges": [
                {"from": 1, "to": 2, "weight": 2}, {"from": 1, "to": 3, "weight": 1}, {"from": 1, "to": 4, "weight": 3},
                {"from": 2, "to": 5, "weight": 2}, {"from": 2, "to": 6, "weight": 3}, {"from": 3, "to": 5, "weight": 6},
                {"from": 3, "to": 6, "weight": 7}, {"from": 4, "to": 6, "weight": 6}, {"from": 4, "to": 7, "weight": 8},
                {"from": 5, "to": 8, "weight": 1}, {"from": 6, "to": 8, "weight": 4}, {"from": 7, "to": 8, "weight": 2}
            ]
        },
        "example_output": {"min_cost": 7, "path": [1, 2, 5, 8]},
        "daa_topics": ["Backward/Forward DP Formulations", "Principle of Optimality", "Linear Time O(V+E) DAG Path"]
    },
    {
        "slug": "all-pairs-shortest-path",
        "name": "All-Pairs Shortest Path (APSP)",
        "category": "Dynamic Programming",
        "paradigm": "Dynamic Programming",
        "description": "Compute the shortest path distance between every pair of vertices (u, v) in a directed or undirected weighted graph.",
        "input_format": "Weighted Adjacency Matrix D^0 or Graph G = (V, E)",
        "output_format": "Distance matrix D of size |V| x |V| where D[i][j] is shortest path from i to j",
        "constraints": "|V| <= 500 for practical O(V^3) computation. No negative weight cycles.",
        "data_type": "graph",
        "example_input": {
            "matrix": [
                [0, 3, float("inf"), 7],
                [8, 0, 2, float("inf")],
                [5, float("inf"), 0, 1],
                [2, float("inf"), float("inf"), 0]
            ]
        },
        "example_output": [
            [0, 3, 5, 6],
            [5, 0, 2, 3],
            [3, 6, 0, 1],
            [2, 5, 7, 0]
        ],
        "daa_topics": ["Floyd-Warshall Recurrence D_k[i,j] = min(D_k-1[i,j], D_k-1[i,k] + D_k-1[k,j])", "Transitive Closure"]
    },
    {
        "slug": "optimal-bst-problem",
        "name": "Optimal Binary Search Tree (OBST)",
        "category": "Dynamic Programming",
        "paradigm": "Dynamic Programming",
        "description": "Construct a binary search tree with minimal expected search cost given access probabilities for keys and dummy keys.",
        "input_format": "Sorted keys array and their associated search probabilities p and q",
        "output_format": "Minimum expected search cost and root table for tree reconstruction",
        "constraints": "Number of keys n <= 100.",
        "data_type": "obst",
        "example_input": {
            "keys": ["k1", "k2", "k3", "k4"],
            "p": [0.1, 0.2, 0.4, 0.3],
            "q": [0.05, 0.1, 0.05, 0.05, 0.05]
        },
        "example_output": {"min_expected_cost": 2.15, "root": "k3"},
        "daa_topics": ["Weighted Interval DP", "Knuth's O(n^2) Optimization", "Expected Search Depth Minimization"]
    },
    {
        "slug": "0-1-knapsack-problem",
        "name": "0/1 Knapsack Problem",
        "category": "Dynamic Programming",
        "paradigm": "Dynamic Programming / Branch and Bound",
        "description": "Given N items with weights and values, select a subset of items to maximize total value without exceeding a maximum weight capacity W. Each item can be chosen at most once (0 or 1).",
        "input_format": "Weights list, Values list, and Knapsack Capacity W",
        "output_format": "Maximum achievable value and selected item indices",
        "constraints": "Weights and capacity W are non-negative integers; 1 <= N <= 1000.",
        "data_type": "knapsack",
        "example_input": {"weights": [2, 3, 4, 5], "values": [3, 4, 5, 6], "capacity": 5},
        "example_output": {"max_value": 7, "selected_items": [0, 1]},
        "daa_topics": ["Overlapping Subproblems", "Optimal Substructure", "Pseudo-polynomial Time Complexity O(nW)", "LC & FIFO Branch and Bound"]
    },
    {
        "slug": "traveling-salesman-problem",
        "name": "Traveling Salesman Problem (TSP)",
        "category": "Dynamic Programming",
        "paradigm": "Dynamic Programming / Branch and Bound",
        "description": "Find the exact minimum-cost tour visiting every city in a distance matrix exactly once and returning to the starting city.",
        "input_format": "Distance matrix D of size n x n and list of city names",
        "output_format": "Minimum tour cost and optimal city permutation sequence",
        "constraints": "n <= 20 for Held-Karp Bitmask DP; n <= 25 for Branch and Bound.",
        "data_type": "matrix",
        "example_input": {
            "distance_matrix": [
                [0, 10, 15, 20],
                [10, 0, 35, 25],
                [15, 35, 0, 30],
                [20, 25, 30, 0]
            ],
            "cities": ["A", "B", "C", "D"]
        },
        "example_output": {"min_cost": 80, "tour": ["A", "B", "D", "C", "A"]},
        "daa_topics": ["Held-Karp Bitmask DP", "Reduced Cost Matrix Lower Bounds", "LC Branch and Bound Search"]
    },
    {
        "slug": "reliability-design-problem",
        "name": "Reliability Design Problem",
        "category": "Dynamic Programming",
        "paradigm": "Dynamic Programming",
        "description": "Determine duplicate device redundancy counts for n stages in series to maximize total system reliability under a given budget.",
        "input_format": "Stage device costs, individual reliabilities, and total budget C",
        "output_format": "Maximum system reliability and device duplication count per stage",
        "constraints": "Stages n <= 20, Budget C <= 1000.",
        "data_type": "reliability",
        "example_input": {
            "reliabilities": [0.9, 0.8, 0.5],
            "costs": [30, 15, 20],
            "budget": 105
        },
        "example_output": {"max_reliability": 0.729, "devices_per_stage": [2, 3, 2]},
        "daa_topics": ["Multi-Stage Resource Allocation", "Dominated Tuple Elimination", "Series-Parallel Reliability Function"]
    },
    {
        "slug": "optimal-storage-tapes-problem",
        "name": "Optimal Storage on Tapes",
        "category": "Greedy Method",
        "paradigm": "Greedy Method",
        "description": "Order n programs on magnetic tape(s) in non-decreasing order of length to minimize Mean Retrieval Time (MRT).",
        "input_format": "List of program lengths and number of available tapes",
        "output_format": "Optimal ordering of programs and minimum Mean Retrieval Time",
        "constraints": "n <= 10000 programs.",
        "data_type": "array",
        "example_input": {"lengths": [5, 10, 3, 20, 12, 7], "tapes": 1},
        "example_output": {"optimal_order": [3, 5, 7, 10, 12, 20], "mean_retrieval_time": 25.17},
        "daa_topics": ["Shortest Program First (SPF)", "Exchange Argument Greedy Proof", "Weighted Sequential Retrieval"]
    },
    {
        "slug": "fractional-knapsack-problem",
        "name": "Fractional Knapsack Problem",
        "category": "Greedy Method",
        "paradigm": "Greedy Method",
        "description": "Maximize total value in a knapsack of capacity W where fractional quantities (fractions of items) may be taken.",
        "input_format": "Weights list, Values list, and Capacity W",
        "output_format": "Maximum achievable value (float) and fraction taken per item",
        "constraints": "N items >= 1, W > 0.",
        "data_type": "knapsack",
        "example_input": {"weights": [10, 20, 30], "values": [60, 100, 120], "capacity": 50},
        "example_output": {"max_value": 240.0, "fractions": [1.0, 1.0, 0.6667]},
        "daa_topics": ["Greedy Choice by Density (Value/Weight)", "Matroid Theory Connection"]
    },
    {
        "slug": "job-sequencing-problem",
        "name": "Job Sequencing with Deadlines",
        "category": "Greedy Method",
        "paradigm": "Greedy Method",
        "description": "Schedule unit-time jobs with specified deadlines and profits to maximize total profit without missing deadlines.",
        "input_format": "List of jobs with IDs, deadlines, and profit values",
        "output_format": "Maximum total profit and scheduled job sequence",
        "constraints": "Number of jobs n <= 10000.",
        "data_type": "jobs",
        "example_input": {
            "jobs": [
                {"id": "J1", "deadline": 2, "profit": 100},
                {"id": "J2", "deadline": 1, "profit": 19},
                {"id": "J3", "deadline": 2, "profit": 27},
                {"id": "J4", "deadline": 1, "profit": 25},
                {"id": "J5", "deadline": 3, "profit": 15}
            ]
        },
        "example_output": {"scheduled_jobs": ["J1", "J3", "J5"], "total_profit": 142},
        "daa_topics": ["Profit-Sorted Slot Allocation", "Disjoint Set Fast Free Slot Finding", "Matroid Independence System"]
    },
    {
        "slug": "optimal-merge-patterns-problem",
        "name": "Optimal Merge Patterns",
        "category": "Greedy Method",
        "paradigm": "Greedy Method",
        "description": "Merge n sorted files of varying lengths pairwise into one sorted file with minimal total record movement.",
        "input_format": "List of file sizes (record counts)",
        "output_format": "Minimum total merge cost and merge sequence tree",
        "constraints": "Number of files n <= 10000.",
        "data_type": "array",
        "example_input": {"files": [20, 30, 10, 5, 30]},
        "example_output": {"total_merge_cost": 205, "merge_steps": 4},
        "daa_topics": ["Min-Heap 2-Way Merge Tree", "Huffman Tree Isomorphism", "External Merge Sort Optimization"]
    },
    {
        "slug": "minimum-spanning-tree",
        "name": "Minimum Spanning Tree (MST)",
        "category": "Greedy Method",
        "paradigm": "Greedy Method",
        "description": "Find a subset of edges in a connected, edge-weighted undirected graph that connects all vertices together without cycles and with the minimum total edge weight.",
        "input_format": "Connected undirected graph G = (V, E) with weights w(u, v)",
        "output_format": "List of |V|-1 edges forming the minimum spanning tree and total weight",
        "constraints": "Graph must be connected and undirected with |V| >= 1.",
        "data_type": "graph",
        "example_input": {
            "vertices": ["0", "1", "2", "3"],
            "edges": [["0", "1", 10], ["0", "2", 6], ["0", "3", 5], ["1", "3", 15], ["2", "3", 4]]
        },
        "example_output": {"mst_edges": [["2", "3", 4], ["0", "3", 5], ["0", "1", 10]], "total_weight": 19},
        "daa_topics": ["Cut Property", "Cycle Property", "Disjoint Set Union (DSU)", "Kruskal vs Prim Density Trade-off"]
    },
    {
        "slug": "single-source-shortest-path",
        "name": "Single Source Shortest Path (SSSP)",
        "category": "Greedy Method",
        "paradigm": "Greedy Method",
        "description": "Find the minimum total weight path from a designated source vertex to every other reachable vertex in a weighted graph.",
        "input_format": "Graph G = (V, E) with edge weights w(u, v) and source vertex s",
        "output_format": "Dictionary mapping each vertex v to dist[v] and predecessor tree",
        "constraints": "Vertices V >= 1, Edges E >= 0. Dijkstra requires non-negative weights; Bellman-Ford supports negative weights.",
        "data_type": "graph",
        "example_input": {
            "vertices": ["A", "B", "C", "D"],
            "edges": [["A", "B", 1], ["B", "C", 2], ["A", "C", 4], ["C", "D", 1]],
            "source": "A"
        },
        "example_output": {"A": 0, "B": 1, "C": 3, "D": 4},
        "daa_topics": ["Greedy Choice Property", "Optimal Substructure", "Relaxation", "Negative Cycle Detection"]
    }
]

# ==========================================
# 2. ALGORITHMS SEED DEFINITIONS (23 CURRICULUM ALGORITHMS)
# ==========================================
ALGORITHMS_DATA: List[Dict[str, Any]] = [
    # ------------------------------------
    # MODULE 1: DIVIDE AND CONQUER (3 Algorithms)
    # ------------------------------------
    {
        "slug": "defective-chessboard",
        "name": "Defective Chessboard",
        "category": "Divide and Conquer",
        "paradigm": "Divide and Conquer",
        "description": "Tiles a 2^k x 2^k board with exactly one missing cell using L-shaped trominoes via recursive quadrant decomposition.",
        "best_case": "O(4^k)",
        "average_case": "O(4^k)",
        "worst_case": "O(4^k)",
        "space_complexity": "O(k)",
        "recurrence_relation": "T(n) = 4T(n/2) + O(1), where n = 2^k",
        "is_stable": True,
        "is_in_place": False,
        "is_adaptive": False,
        "is_deterministic": True,
        "pseudocode": """procedure tileBoard(n, top, left, defectR, defectC)
    if n == 1 then return
    place tromino at center facing away from quadrant with defect
    recursively tile all 4 sub-quadrants
end procedure""",
        "advantages": ["Elegant divide-and-conquer application", "Deterministic linear-time in board area O(4^k)", "Visually demonstrates recursive problem reduction"],
        "disadvantages": ["Requires board size to be exact power of 2", "Limited to single missing cell variant"],
        "suitable_cases": ["Defective VLSI grid fabrication", "Geometric floor tiling optimization", "Educational D&C demonstration"],
        "unsuitable_cases": ["Arbitrary non-power-of-2 grid dimensions", "Multiple distributed defective cells"],
        "daa_concept_notes": "Canonical divide-and-conquer geometric problem. Master Theorem Case 1 applies: a=4, b=2, d=0 -> O(n^2) = O(4^k)."
    },
    {
        "slug": "max-min-divide-conquer",
        "name": "Finding the Maximum and Minimum",
        "category": "Divide and Conquer",
        "paradigm": "Divide and Conquer",
        "description": "Simultaneously finds maximum and minimum in an array using divide-and-conquer with at most 3n/2 - 2 comparisons.",
        "best_case": "O(n)",
        "average_case": "O(n)",
        "worst_case": "O(n)",
        "space_complexity": "O(log n)",
        "recurrence_relation": "T(n) = 2T(n/2) + 2, with T(2)=1, T(1)=0 -> 3n/2 - 2 comparisons",
        "is_stable": True,
        "is_in_place": True,
        "is_adaptive": False,
        "is_deterministic": True,
        "pseudocode": """procedure maxMin(A, i, j)
    if i == j then return (A[i], A[i])
    if i == j - 1 then return (min(A[i], A[j]), max(A[i], A[j]))
    mid = (i + j) / 2
    (min1, max1) = maxMin(A, i, mid)
    (min2, max2) = maxMin(A, mid + 1, j)
    return (min(min1, min2), max(max1, max2))
end procedure""",
        "advantages": ["Reduces comparisons from 2n-2 to 3n/2-2 (25% reduction)", "Optimal comparison complexity for simultaneous extrema", "Easily parallelizable subproblems"],
        "disadvantages": ["Recursive stack overhead O(log n)", "Slightly more complex than standard linear scan"],
        "suitable_cases": ["Statistical range queries", "Signal envelope detection", "Array bounds computation"],
        "unsuitable_cases": ["Streaming data where elements arrive sequentially", "Extremely small arrays where scan has lower overhead"],
        "daa_concept_notes": "Optimal comparison lower bound proof for simultaneous max-min: ceiling(3n/2) - 2."
    },
    {
        "slug": "strassen-matrix-multiplication",
        "name": "Strassen's Matrix Multiplication",
        "category": "Divide and Conquer",
        "paradigm": "Divide and Conquer",
        "description": "Multiplies two n x n square matrices using 7 recursive sub-multiplications instead of 8, achieving sub-cubic O(n^2.8074) complexity.",
        "best_case": "O(n^2.807)",
        "average_case": "O(n^2.807)",
        "worst_case": "O(n^2.807)",
        "space_complexity": "O(n^2)",
        "recurrence_relation": "T(n) = 7T(n/2) + O(n^2) -> O(n^log2(7)) = O(n^2.8074)",
        "is_stable": True,
        "is_in_place": False,
        "is_adaptive": False,
        "is_deterministic": True,
        "pseudocode": """procedure strassen(A, B, n)
    if n <= threshold then return standardMultiply(A, B)
    split A, B into 4 submatrices each
    M1 = (A11 + A22)(B11 + B22); M2 = (A21 + A22)B11; M3 = A11(B12 - B22)
    M4 = A22(B21 - B11); M5 = (A11 + A12)B22; M6 = (A21 - A11)(B11 + B12)
    M7 = (A12 - A22)(B21 + B22)
    C11 = M1 + M4 - M5 + M7; C12 = M3 + M5
    C21 = M2 + M4; C22 = M1 - M2 + M3 + M6
    return combine(C11, C12, C21, C22)
end procedure""",
        "advantages": ["Sub-cubic asymptotic complexity O(n^2.8074)", "Faster than standard O(n^3) for large matrices (n > 128)", "Foundation of modern fast linear algebra algorithms"],
        "disadvantages": ["Large constant factor due to 18 matrix additions", "Numerical instability with floating-point arithmetic", "High memory allocation overhead"],
        "suitable_cases": ["Large dense matrix multiplication in scientific computing", "Graph transitive closure computation", "Big data numerical transformations"],
        "unsuitable_cases": ["Small matrices (n < 64) where O(n^3) is faster due to low constants", "Sparse matrices where specialized sparse solvers excel"],
        "daa_concept_notes": "First algorithm to beat O(n^3) matrix multiplication. Master Theorem Case 1: log2(7) ≈ 2.8074 > 2."
    },

    # ------------------------------------
    # MODULE 2: BACKTRACKING (3 Algorithms)
    # ------------------------------------
    {
        "slug": "n-queens-backtracking",
        "name": "N-Queens Problem",
        "category": "Backtracking",
        "paradigm": "Backtracking",
        "description": "Places N non-attacking queens on an N x N chessboard using systematic depth-first search with column and diagonal pruning.",
        "best_case": "O(N)",
        "average_case": "O(N!)",
        "worst_case": "O(N!)",
        "space_complexity": "O(N)",
        "recurrence_relation": "T(n) = n * T(n-1) with state-space diagonal and column pruning",
        "is_stable": True,
        "is_in_place": False,
        "is_adaptive": True,
        "is_deterministic": True,
        "pseudocode": """procedure solveNQueens(board, col, N)
    if col >= N then recordSolution(board); return true
    for row = 0 to N-1 do
        if isSafe(board, row, col) then
            placeQueen(board, row, col)
            solveNQueens(board, col + 1, N)
            removeQueen(board, row, col)
    end for
end procedure""",
        "advantages": ["Exact solution with minimal O(N) memory", "State space tree pruning eliminates vast non-viable branches", "Can find all solutions or stop at first valid solution"],
        "disadvantages": ["Factorial worst-case time complexity O(N!)", "Impractical for very large boards (N > 30) without heuristics"],
        "suitable_cases": ["Constraint satisfaction benchmarks", "VLSI circuit crossbar routing", "Deadlock prevention in distributed systems"],
        "unsuitable_cases": ["Large-scale real-time configuration where heuristic approximation is needed"],
        "daa_concept_notes": "Classic state space tree traversal with bounding functions (row, column, and diagonal constraints)."
    },
    {
        "slug": "subset-sum-backtracking",
        "name": "Sum of Subsets Problem",
        "category": "Backtracking",
        "paradigm": "Backtracking",
        "description": "Finds all subsets of a given set of positive integers that sum to a target value using sorted state-space bounding.",
        "best_case": "O(n)",
        "average_case": "O(2^n)",
        "worst_case": "O(2^n)",
        "space_complexity": "O(n)",
        "recurrence_relation": "T(n) = 2T(n-1) bounded by current_sum + remaining_sum >= target",
        "is_stable": True,
        "is_in_place": False,
        "is_adaptive": True,
        "is_deterministic": True,
        "pseudocode": """procedure sumOfSubsets(s, k, r, target, w, x)
    // s: current sum, k: index, r: remaining sum
    x[k] = 1
    if s + w[k] == target then outputSolution(x)
    else if s + w[k] + w[k+1] <= target then
        sumOfSubsets(s + w[k], k + 1, r - w[k], target, w, x)
    if s + r - w[k] >= target and s + w[k+1] <= target then
        x[k] = 0
        sumOfSubsets(s, k + 1, r - w[k], target, w, x)
end procedure""",
        "advantages": ["Prunes exponential search space using remaining sum bounds", "O(n) auxiliary memory on call stack", "Finds all exact solution subsets"],
        "disadvantages": ["Exponential worst-case O(2^n)", "Requires pre-sorting for effective pruning"],
        "suitable_cases": ["Financial portfolio budget matching", "Knapsack exact capacity subset finding", "Cargo weight balancing"],
        "unsuitable_cases": ["Dense integer ranges with very large N (use DP if target is small)"],
        "daa_concept_notes": "Demonstrates left-child (include) and right-child (exclude) state space tree exploration with 2-way pruning."
    },
    {
        "slug": "hamiltonian-cycle-backtracking",
        "name": "Hamiltonian Cycles",
        "category": "Backtracking",
        "paradigm": "Backtracking",
        "description": "Finds closed tours visiting every vertex in an undirected graph exactly once using vertex adjacency constraint pruning.",
        "best_case": "O(V)",
        "average_case": "O(V!)",
        "worst_case": "O(V!)",
        "space_complexity": "O(V)",
        "recurrence_relation": "T(V) = V * T(V-1) bounded by edge existence and unvisited constraints",
        "is_stable": True,
        "is_in_place": False,
        "is_adaptive": True,
        "is_deterministic": True,
        "pseudocode": """procedure hamiltonianCycle(k, x, G, n)
    repeat
        nextVertex(k, x, G, n)
        if x[k] == 0 then return
        if k == n then outputTour(x)
        else hamiltonianCycle(k + 1, x, G, n)
    until false
end procedure""",
        "advantages": ["Exact solution for NP-complete decision and enumeration problem", "Memory efficient O(V) call stack", "Prunes non-adjacent vertices immediately"],
        "disadvantages": ["Factorial worst-case complexity O(V!)", "Inefficient on dense graphs without cycle existence tests"],
        "suitable_cases": ["Printed circuit board (PCB) drill path routing", "Robotic inspection trajectory planning", "Network topology ring validation"],
        "unsuitable_cases": ["Large graphs (V > 25) in real-time environments"],
        "daa_concept_notes": "NP-complete problem formulation. Connects directly to TSP (Hamiltonian cycle of minimum weight)."
    },

    # ------------------------------------
    # MODULE 3: DYNAMIC PROGRAMMING (6 Algorithms)
    # ------------------------------------
    {
        "slug": "multistage-graph-dp",
        "name": "Multistage Graphs",
        "category": "Dynamic Programming",
        "paradigm": "Dynamic Programming",
        "description": "Finds minimum-cost path from source to sink in a k-stage partitioned directed graph using backward/forward DP recurrence.",
        "best_case": "O(V + E)",
        "average_case": "O(V + E)",
        "worst_case": "O(V + E)",
        "space_complexity": "O(V)",
        "recurrence_relation": "cost(i, j) = min_{l in V_{i+1}} { c(j, l) + cost(i+1, l) }",
        "is_stable": True,
        "is_in_place": False,
        "is_adaptive": False,
        "is_deterministic": True,
        "pseudocode": """procedure multistageGraphBackward(G, k, n)
    cost[n] = 0
    for j = n-1 down to 1 do
        cost[j] = min_{(j, r) in E} { c(j, r) + cost[r] }
        d[j] = argmin_{(j, r) in E} { c(j, r) + cost[r] }
    end for
    return reconstructPath(d, k)
end procedure""",
        "advantages": ["Linear time O(V + E) for staged DAGs", "Exemplifies backward and forward DP formulations", "Guaranteed global optimal path"],
        "disadvantages": ["Strict requirement: graph must be partitioned into sequential stages", "Cannot handle cyclic graphs"],
        "suitable_cases": ["Multi-stage production line optimization", "Supply chain pipeline routing", "Sequential decision processes"],
        "unsuitable_cases": ["General cyclic graphs", "Arbitrary un-staged networks"],
        "daa_concept_notes": "Classic illustration of Bellman's Principle of Optimality applied to staged decision problems."
    },
    {
        "slug": "floyd-warshall-apsp",
        "name": "All-Pairs Shortest Path (Floyd-Warshall)",
        "category": "Dynamic Programming",
        "paradigm": "Dynamic Programming",
        "description": "Computes shortest paths between all pairs of vertices in O(V^3) time using intermediate vertex DP relaxation.",
        "best_case": "O(V³)",
        "average_case": "O(V³)",
        "worst_case": "O(V³)",
        "space_complexity": "O(V²)",
        "recurrence_relation": "D^k[i, j] = min(D^{k-1}[i, j], D^{k-1}[i, k] + D^{k-1}[k, j])",
        "is_stable": True,
        "is_in_place": True,
        "is_adaptive": False,
        "is_deterministic": True,
        "pseudocode": """procedure floydWarshall(W, V)
    D = copy(W)
    for k = 1 to V do
        for i = 1 to V do
            for j = 1 to V do
                D[i][j] = min(D[i][j], D[i][k] + D[k][j])
    return D
end procedure""",
        "advantages": ["Simplicity of implementation: triple nested loop", "Handles negative edge weights (detects negative cycles via diagonal)", "Computes all pairs simultaneously in O(V^3)"],
        "disadvantages": ["O(V^3) time regardless of edge density", "O(V^2) memory required"],
        "suitable_cases": ["Dense graphs (E ~ V^2)", "Transitive closure computation (Warshall's variant)", "Network routing tables"],
        "unsuitable_cases": ["Sparse graphs where running Dijkstra |V| times gives O(V*E log V)"],
        "daa_concept_notes": "Dynamic programming formulation over the set of allowed intermediate vertices {1, 2, ..., k}."
    },
    {
        "slug": "optimal-bst-dp",
        "name": "Optimal Binary Search Trees",
        "category": "Dynamic Programming",
        "paradigm": "Dynamic Programming",
        "description": "Constructs a binary search tree with minimum expected search cost using interval DP over key and dummy key access probabilities.",
        "best_case": "O(n³)",
        "average_case": "O(n³)",
        "worst_case": "O(n³)",
        "space_complexity": "O(n²)",
        "recurrence_relation": "e[i, j] = min_{i <= r <= j} { e[i, r-1] + e[r+1, j] + w(i, j) }",
        "is_stable": True,
        "is_in_place": False,
        "is_adaptive": False,
        "is_deterministic": True,
        "pseudocode": """procedure optimalBST(p, q, n)
    for i = 1 to n+1 do e[i, i-1] = q[i-1]; w[i, i-1] = q[i-1]
    for l = 1 to n do
        for i = 1 to n-l+1 do
            j = i + l - 1
            e[i, j] = infinity; w[i, j] = w[i, j-1] + p[j] + q[j]
            for r = i to j do
                t = e[i, r-1] + e[r+1, j] + w[i, j]
                if t < e[i, j] then e[i, j] = t; root[i, j] = r
    return (e[1, n], root)
end procedure""",
        "advantages": ["Minimizes average search time given non-uniform access frequencies", "Guaranteed optimal static search structure", "Can be optimized to O(n^2) using Knuth's quadrangle inequality"],
        "disadvantages": ["O(n^3) standard time complexity (O(n^2) optimized)", "Requires static key probability distributions known upfront"],
        "suitable_cases": ["Compilers symbol table construction", "Dictionary lookups with known word frequencies", "Static routing lookup tables"],
        "unsuitable_cases": ["Dynamic datasets with frequent insertions and deletions"],
        "daa_concept_notes": "Weighted interval DP. Demonstrates how probability weight w(i,j) accumulates across tree levels."
    },
    {
        "slug": "0-1-knapsack-dp",
        "name": "0/1 Knapsack (Dynamic Programming)",
        "category": "Dynamic Programming",
        "paradigm": "Dynamic Programming",
        "description": "Solves the discrete 0/1 knapsack problem using pseudo-polynomial DP tabulation over items and capacity.",
        "best_case": "O(n * W)",
        "average_case": "O(n * W)",
        "worst_case": "O(n * W)",
        "space_complexity": "O(n * W)",
        "recurrence_relation": "V[i, w] = max(V[i-1, w], V[i-1, w - w_i] + v_i)",
        "is_stable": True,
        "is_in_place": False,
        "is_adaptive": False,
        "is_deterministic": True,
        "pseudocode": """procedure knapsackDP(values, weights, W, n)
    for w = 0 to W do K[0, w] = 0
    for i = 1 to n do
        for w = 0 to W do
            if weights[i-1] <= w then
                K[i, w] = max(values[i-1] + K[i-1, w - weights[i-1]], K[i-1, w])
            else
                K[i, w] = K[i-1, w]
    return K[n, W]
end procedure""",
        "advantages": ["Guaranteed exact optimal subset selection", "Pseudo-polynomial O(nW) time is very fast when capacity W is moderate", "Backtracking reconstructs the exact chosen items"],
        "disadvantages": ["Space and time scale with capacity W (fails if W is exponential)", "Not applicable to continuous fractional items"],
        "suitable_cases": ["Budget allocation", "Cargo packing with integer weight constraints", "Resource scheduling"],
        "unsuitable_cases": ["Fractional items (use Greedy)", "Very large capacities W >> 10^7"],
        "daa_concept_notes": "Canonical dynamic programming problem demonstrating optimal substructure and overlapping subproblems."
    },
    {
        "slug": "traveling-salesman-dp",
        "name": "Traveling Salesman Problem (Held-Karp DP)",
        "category": "Dynamic Programming",
        "paradigm": "Dynamic Programming",
        "description": "Exact solver for TSP using Held-Karp bitmask dynamic programming in O(n^2 * 2^n) time.",
        "best_case": "O(n² 2^n)",
        "average_case": "O(n² 2^n)",
        "worst_case": "O(n² 2^n)",
        "space_complexity": "O(n 2^n)",
        "recurrence_relation": "C(S, j) = min_{i in S, i != j} { C(S - {j}, i) + d(i, j) }",
        "is_stable": True,
        "is_in_place": False,
        "is_adaptive": False,
        "is_deterministic": True,
        "pseudocode": """procedure heldKarpTSP(dist, n)
    for i = 1 to n-1 do memo[1 << i, i] = dist[0][i]
    for subsetSize = 2 to n-1 do
        for each subset S of size subsetSize containing 0 do
            for each j in S, j != 0 do
                memo[S, j] = min_{i in S, i != j, i != 0} (memo[S - {j}, i] + dist[i][j])
    return min_{j != 0} (memo[fullMask, j] + dist[j][0])
end procedure""",
        "advantages": ["Reduces TSP complexity from O(n!) brute-force to O(n^2 2^n)", "Guaranteed exact global optimal tour", "Standard benchmark for subset bitmask DP"],
        "disadvantages": ["Exponential time and memory O(n 2^n)", "Limited to n <= 23 cities in practical memory"],
        "suitable_cases": ["Exact small-scale vehicle routing", "CNC machine path planning", "Robotic circuit board inspection"],
        "unsuitable_cases": ["Large-scale logistics (n > 25, use Branch & Bound or heuristics)"],
        "daa_concept_notes": "Bitmask dynamic programming. Demonstrates subproblem compression using binary state masks."
    },
    {
        "slug": "reliability-design-dp",
        "name": "Reliability Design",
        "category": "Dynamic Programming",
        "paradigm": "Dynamic Programming",
        "description": "Determines optimal device duplication counts per stage in a series system to maximize total reliability under budget.",
        "best_case": "O(n * C)",
        "average_case": "O(n * C)",
        "worst_case": "O(n * C)",
        "space_complexity": "O(n * C)",
        "recurrence_relation": "f_i(x) = max_{1 <= u_i <= u_max} { phi_i(u_i) * f_{i-1}(x - u_i * c_i) }",
        "is_stable": True,
        "is_in_place": False,
        "is_adaptive": False,
        "is_deterministic": True,
        "pseudocode": """procedure reliabilityDesign(costs, reliabilities, budget, n)
    initialize S_0 = {(1.0, 0)} // (reliability, cost)
    for i = 1 to n do
        S_i = generateTuples(S_{i-1}, costs[i], reliabilities[i], budget)
        S_i = eliminateDominatedTuples(S_i)
    return maxReliability(S_n)
end procedure""",
        "advantages": ["Maximized system availability under strict budget constraints", "Dominated tuple elimination drastically prunes search space", "Exact non-linear optimization solver"],
        "disadvantages": ["Complexity depends on device duplication limits and budget C", "Requires discrete cost and reliability parameters"],
        "suitable_cases": ["Mission-critical aerospace system design", "Fault-tolerant data center architecture", "Telecommunications repeater redundancy"],
        "unsuitable_cases": ["Continuous resource allocation models"],
        "daa_concept_notes": "Non-linear multi-stage DP with tuple-based state representation and Pareto-frontier pruning."
    },

    # ------------------------------------
    # MODULE 4: GREEDY METHOD (8 Algorithms)
    # ------------------------------------
    {
        "slug": "optimal-storage-tapes-greedy",
        "name": "Optimal Storage on Tapes",
        "category": "Greedy Method",
        "paradigm": "Greedy Method",
        "description": "Orders programs on sequential storage tape(s) in non-decreasing length order to minimize Mean Retrieval Time (MRT).",
        "best_case": "O(n log n)",
        "average_case": "O(n log n)",
        "worst_case": "O(n log n)",
        "space_complexity": "O(1)",
        "recurrence_relation": "MRT = (1/n) * sum_{j=1}^n sum_{k=1}^j L_{i_k} -> minimized by L_{i_1} <= L_{i_2} <= ... <= L_{i_n}",
        "is_stable": True,
        "is_in_place": True,
        "is_adaptive": False,
        "is_deterministic": True,
        "pseudocode": """procedure optimalTapeStorage(lengths, n, m_tapes)
    sort lengths in non-decreasing order
    distribute programs round-robin across m tapes
    compute total retrieval time and MRT
    return (programOrder, MRT)
end procedure""",
        "advantages": ["Provably optimal MRT via greedy Shortest Program First rule", "Fast O(n log n) sorting time", "Easily extends to multi-tape systems"],
        "disadvantages": ["Assumes uniform retrieval frequency for all programs", "Sequential access model only"],
        "suitable_cases": ["Magnetic tape backup ordering", "Batch job sequential execution ordering", "Single-threaded queue latency reduction"],
        "unsuitable_cases": ["Random access media (SSDs/RAM) where seek time is uniform"],
        "daa_concept_notes": "Exchange argument proof showing any out-of-order pair increases total retrieval time."
    },
    {
        "slug": "fractional-knapsack",
        "name": "Fractional Knapsack Problem",
        "category": "Greedy Method",
        "paradigm": "Greedy Method",
        "description": "Maximizes value in a capacity-constrained knapsack where divisible items can be taken fractionally by sorting value/weight ratio.",
        "best_case": "O(n log n)",
        "average_case": "O(n log n)",
        "worst_case": "O(n log n)",
        "space_complexity": "O(1)",
        "recurrence_relation": "Greedy choice: take maximum available weight of item with highest v_i / w_i",
        "is_stable": True,
        "is_in_place": True,
        "is_adaptive": False,
        "is_deterministic": True,
        "pseudocode": """procedure fractionalKnapsack(items, capacity)
    sort items by value/weight ratio descending
    totalValue = 0.0, remainingCap = capacity
    for item in items do
        if item.weight <= remainingCap then
            take 100% of item
            totalValue += item.value; remainingCap -= item.weight
        else
            take (remainingCap / item.weight) fraction of item
            totalValue += item.value * (remainingCap / item.weight)
            break
    return totalValue
end procedure""",
        "advantages": ["Optimal solution in O(n log n) time", "True greedy choice property holds unconditionally", "Can be solved in O(n) using median-of-medians linear selection"],
        "disadvantages": ["Requires items to be continuously divisible", "Does not solve discrete 0/1 integer items"],
        "suitable_cases": ["Liquid/grain bulk commodity transport", "Bandwidth bandwidth allocation", "Continuous asset trading"],
        "unsuitable_cases": ["Indivisible discrete goods (cars, laptops) -> use 0/1 DP"],
        "daa_concept_notes": "Classic comparison between Greedy (Fractional) and DP (0/1). Matroid theoretical greedy optimality."
    },
    {
        "slug": "job-sequencing-deadlines",
        "name": "Job Sequencing with Deadlines",
        "category": "Greedy Method",
        "paradigm": "Greedy Method",
        "description": "Schedules unit-time jobs with profits and deadlines into the latest available time slots to maximize total profit.",
        "best_case": "O(n²)",
        "average_case": "O(n²)",
        "worst_case": "O(n²)",
        "space_complexity": "O(min(n, max_deadline))",
        "recurrence_relation": "Sort by profit descending; assign to latest free slot t <= deadline",
        "is_stable": True,
        "is_in_place": False,
        "is_adaptive": False,
        "is_deterministic": True,
        "pseudocode": """procedure jobSequencing(jobs, maxDeadline)
    sort jobs in descending order of profit
    slots = array of size maxDeadline initialized to empty
    totalProfit = 0
    for job in jobs do
        for t = min(maxDeadline, job.deadline) down to 1 do
            if slots[t] is empty then
                slots[t] = job.id; totalProfit += job.profit; break
    return (slots, totalProfit)
end procedure""",
        "advantages": ["Guaranteed maximum profit schedule", "Intuitive latest-feasible-slot greedy strategy", "Can be accelerated to O(n alpha(n)) using Disjoint Set Union (DSU)"],
        "disadvantages": ["O(n^2) time with linear slot scan", "Assumes unit execution time per job"],
        "suitable_cases": ["Server task dispatch with penalty deadlines", "Manufacturing slot reservation", "Cloud batch worker scheduling"],
        "unsuitable_cases": ["Jobs with variable processing durations (preemptive scheduling needed)"],
        "daa_concept_notes": "Matroid independence system formulation: the set of feasible job subsets forms a matroid."
    },
    {
        "slug": "optimal-merge-patterns-greedy",
        "name": "Optimal Merge Patterns",
        "category": "Greedy Method",
        "paradigm": "Greedy Method",
        "description": "Merges n sorted files of various sizes pairwise with minimal total record moves using a min-heap.",
        "best_case": "O(n log n)",
        "average_case": "O(n log n)",
        "worst_case": "O(n log n)",
        "space_complexity": "O(n)",
        "recurrence_relation": "Extract 2 smallest files (a, b), merge cost = a + b, re-insert (a + b) into min-heap",
        "is_stable": True,
        "is_in_place": False,
        "is_adaptive": False,
        "is_deterministic": True,
        "pseudocode": """procedure optimalMerge(files)
    heap = MinHeap(files)
    totalCost = 0
    while heap.size() > 1 do
        f1 = heap.extractMin(); f2 = heap.extractMin()
        merged = f1 + f2
        totalCost += merged
        heap.insert(merged)
    return totalCost
end procedure""",
        "advantages": ["Provably optimal O(n log n) merge tree", "Isomorphic to Huffman coding tree construction", "Minimizes disk I/O in external sorting"],
        "disadvantages": ["Requires min-heap priority queue data structure", "Static file sizes must be known in advance"],
        "suitable_cases": ["External merge sort optimization", "Distributed log aggregation", "Big data chunk consolidation"],
        "unsuitable_cases": ["Dynamic streaming files with unknown future sizes"],
        "daa_concept_notes": "Optimal prefix code / merge tree duality. Proof of greedy choice by induction on tree depth."
    },
    {
        "slug": "kruskal-mst",
        "name": "Kruskal's Algorithm (MST)",
        "category": "Greedy Method",
        "paradigm": "Greedy Method",
        "description": "Constructs a Minimum Spanning Tree by sorting all edges and greedily adding the cheapest non-cycle edge using Disjoint Set Union (DSU).",
        "best_case": "O(E log E)",
        "average_case": "O(E log E)",
        "worst_case": "O(E log E)",
        "space_complexity": "O(V)",
        "recurrence_relation": "T(E, V) = O(E log E) sorting + O(E * alpha(V)) DSU operations",
        "is_stable": True,
        "is_in_place": False,
        "is_adaptive": False,
        "is_deterministic": True,
        "pseudocode": """procedure kruskalMST(G=(V, E))
    sort E in non-decreasing order of weight
    dsu = DisjointSet(V)
    mst = []
    for (u, v, w) in E do
        if dsu.find(u) != dsu.find(v) then
            dsu.union(u, v)
            mst.append((u, v, w))
            if mst.length == V - 1 then break
    return mst
end procedure""",
        "advantages": ["Highly efficient on sparse graphs (E << V^2)", "Naturally handles disconnected components (produces Minimum Spanning Forest)", "Simple and robust edge-centric processing"],
        "disadvantages": ["Requires sorting all edges upfront O(E log E)", "Slower than Prim on dense graphs (E ~ V^2)"],
        "suitable_cases": ["Telecommunications cable layout", "Sparse electrical grid construction", "Road network cost minimization"],
        "unsuitable_cases": ["Extremely dense graphs where Prim with adjacency matrix is O(V^2)"],
        "daa_concept_notes": "Cycle property of spanning trees. DSU path compression and union-by-rank achieve nearly linear alpha(V) time."
    },
    {
        "slug": "prim-mst",
        "name": "Prim's Algorithm (MST)",
        "category": "Greedy Method",
        "paradigm": "Greedy Method",
        "description": "Grows a single Minimum Spanning Tree vertex by vertex from an arbitrary start, always adding the cheapest cut edge.",
        "best_case": "O(E + V log V)",
        "average_case": "O(E + V log V)",
        "worst_case": "O(E + V log V)",
        "space_complexity": "O(V)",
        "recurrence_relation": "T(V, E) = O(V log V + E log V) with binary heap, O(V^2) with adjacency matrix",
        "is_stable": True,
        "is_in_place": False,
        "is_adaptive": False,
        "is_deterministic": True,
        "pseudocode": """procedure primMST(G=(V, E), start)
    pq = MinPriorityQueue()
    pq.insert(start, 0)
    visited = set()
    while not pq.isEmpty() do
        (u, w) = pq.extractMin()
        if u in visited then continue
        visited.add(u)
        for neighbor v of u do
            if v not in visited then pq.insertOrDecrease(v, weight(u, v))
end procedure""",
        "advantages": ["Faster than Kruskal on dense graphs O(V^2) or O(E + V log V)", "Always maintains a single connected tree", "Does not require edge pre-sorting"],
        "disadvantages": ["Requires priority queue with decrease-key operation", "Cannot process disconnected components without outer restart"],
        "suitable_cases": ["Dense communication networks", "Integrated circuit layout", "Fiber optic backbone design"],
        "unsuitable_cases": ["Sparse graphs with E << V^2 (Kruskal is faster)"],
        "daa_concept_notes": "Cut property of spanning trees. Vertex-growing greedy cut relaxation."
    },
    {
        "slug": "dijkstra-sssp",
        "name": "Dijkstra's Algorithm (SSSP)",
        "category": "Greedy Method",
        "paradigm": "Greedy Method",
        "description": "Finds shortest paths from a single source vertex to all other vertices in non-negative edge weighted graphs using priority queue relaxation.",
        "best_case": "O(E + V log V)",
        "average_case": "O(E + V log V)",
        "worst_case": "O(E + V log V)",
        "space_complexity": "O(V)",
        "recurrence_relation": "dist[v] = min(dist[v], dist[u] + w(u, v)) via extract-min greedy frontier",
        "is_stable": True,
        "is_in_place": False,
        "is_adaptive": False,
        "is_deterministic": True,
        "pseudocode": """procedure dijkstraSSSP(G, source)
    dist = [infinity] * V; dist[source] = 0
    pq = MinPriorityQueue(); pq.insert(source, 0)
    while not pq.isEmpty() do
        u = pq.extractMin()
        for each (u, v, w) in G.adj[u] do
            if dist[u] + w < dist[v] then
                dist[v] = dist[u] + w
                pq.insertOrDecrease(v, dist[v])
    return dist
end procedure""",
        "advantages": ["Optimal O(E + V log V) time with Fibonacci heap", "Greedy choice guarantees shortest distance when extracted", "Standard industry routing algorithm (OSPF, GPS navigation)"],
        "disadvantages": ["Fails completely on graphs with negative edge weights (infinite loop or incorrect distances)"],
        "suitable_cases": ["GPS map route calculation", "Internet packet routing (OSPF, IS-IS)", "Social network shortest connection degree"],
        "unsuitable_cases": ["Graphs with negative edge weights -> use Bellman-Ford"],
        "daa_concept_notes": "Greedy triangle relaxation invariant: once a vertex is finalized, its shortest distance cannot be improved."
    },
    {
        "slug": "bellman-ford-sssp",
        "name": "Bellman-Ford Algorithm (SSSP)",
        "category": "Greedy Method",
        "paradigm": "Greedy Method",
        "description": "Computes single-source shortest paths in graphs with negative weights and detects reachable negative weight cycles via |V|-1 edge relaxations.",
        "best_case": "O(E)",
        "average_case": "O(V * E)",
        "worst_case": "O(V * E)",
        "space_complexity": "O(V)",
        "recurrence_relation": "dist^k[v] = min(dist^{k-1}[v], min_{(u,v) in E} { dist^{k-1}[u] + w(u, v) })",
        "is_stable": True,
        "is_in_place": True,
        "is_adaptive": True,
        "is_deterministic": True,
        "pseudocode": """procedure bellmanFord(G=(V, E), source)
    dist = [infinity] * V; dist[source] = 0
    for i = 1 to V-1 do
        for each (u, v, w) in E do
            if dist[u] + w < dist[v] then dist[v] = dist[u] + w
    // Negative cycle detection pass
    for each (u, v, w) in E do
        if dist[u] + w < dist[v] then return "Negative Weight Cycle Detected"
    return dist
end procedure""",
        "advantages": ["Handles negative edge weights correctly", "Detects reachable negative cycles", "Simple edge relaxation structure easily distributed (Distance Vector Routing / RIP)"],
        "disadvantages": ["O(V * E) time is significantly slower than Dijkstra on non-negative graphs"],
        "suitable_cases": ["Financial arbitrage detection in currency exchange networks", "Distance-Vector routing protocols (RIP)", "Graphs with negative cost edges"],
        "unsuitable_cases": ["Large positive-weight road networks where Dijkstra is hundreds of times faster"],
        "daa_concept_notes": "After |V|-1 iterations, all simple shortest paths must be converged. An extra relaxation indicates a negative cycle."
    },

    # ------------------------------------
    # MODULE 5: BRANCH AND BOUND (3 Algorithms)
    # ------------------------------------
    {
        "slug": "0-1-knapsack-lc-bb",
        "name": "0/1 Knapsack (LC Branch & Bound)",
        "category": "Branch and Bound",
        "paradigm": "Branch and Bound",
        "description": "Solves 0/1 Knapsack using Least-Cost (Best-First) Branch & Bound with fractional knapsack upper bound pruning.",
        "best_case": "O(n)",
        "average_case": "O(2^n)",
        "worst_case": "O(2^n)",
        "space_complexity": "O(2^n)",
        "recurrence_relation": "Upper Bound = current_value + fractional_knapsack(remaining_items, remaining_capacity)",
        "is_stable": True,
        "is_in_place": False,
        "is_adaptive": True,
        "is_deterministic": True,
        "pseudocode": """procedure knapsackLCBB(items, capacity)
    queue = MaxPriorityQueue()
    queue.insert((0, 0, 0, []))  // (level, value, weight, items)
    maxValue = 0
    while not queue.isEmpty() do
        node = queue.extractMax()  // highest upper bound
        if node.bound <= maxValue then continue
        if node.weight <= capacity then
            maxValue = max(maxValue, node.value)
        // Branch: include next item
        if feasible then queue.insert(include_node)
        // Branch: exclude next item
        if feasible then queue.insert(exclude_node)
    return maxValue
end procedure""",
        "advantages": ["Aggressively prunes search space with best-first exploration", "Optimal solution guaranteed", "Often faster than DP for sparse solution spaces"],
        "disadvantages": ["Worst-case O(2^n) exponential complexity", "Exponential memory for priority queue"],
        "suitable_cases": ["High-value investment portfolio optimization", "Critical cargo space allocation", "When optimal solution is sparse"],
        "unsuitable_cases": ["Dense solution spaces (use DP)", "Real-time systems", "Very large n (> 30)"],
        "daa_concept_notes": "LC search explores most promising nodes first via priority queue. Fractional knapsack bound is admissible upper bound."
    },
    {
        "slug": "0-1-knapsack-fifo-bb",
        "name": "0/1 Knapsack (FIFO Branch & Bound)",
        "category": "Branch and Bound",
        "paradigm": "Branch and Bound",
        "description": "Solves 0/1 Knapsack using FIFO queue breadth-first Branch & Bound with bound-based pruning.",
        "best_case": "O(n)",
        "average_case": "O(2^n)",
        "worst_case": "O(2^n)",
        "space_complexity": "O(2^n)",
        "recurrence_relation": "Breadth-first level-by-level exploration with bound pruning",
        "is_stable": True,
        "is_in_place": False,
        "is_adaptive": True,
        "is_deterministic": True,
        "pseudocode": """procedure knapsackFIFOBB(items, capacity)
    queue = FIFOQueue()
    queue.enqueue((0, 0, 0))  // (level, value, weight)
    maxValue = 0
    while not queue.isEmpty() do
        node = queue.dequeue()
        if node.bound <= maxValue then continue
        if node.weight <= capacity then
            maxValue = max(maxValue, node.value)
        // Enqueue include and exclude branches
        if feasible then queue.enqueue(include_node)
        if feasible then queue.enqueue(exclude_node)
    return maxValue
end procedure""",
        "advantages": ["Systematic breadth-first exploration", "Simpler FIFO queue implementation", "Memory-bound pruning opportunities"],
        "disadvantages": ["Slower than LC B&B (explores less promising nodes)", "Exponential queue size without aggressive pruning"],
        "suitable_cases": ["Educational B&B demonstration", "Memory-constrained systems (FIFO simpler than heap)", "When level-wise exploration is desired"],
        "unsuitable_cases": ["Large problem instances", "When best-first exploration significantly reduces search space"],
        "daa_concept_notes": "FIFO B&B contrasts with LC B&B: systematic level-order vs. best-first heuristic-guided search."
    },
    {
        "slug": "traveling-salesman-bb",
        "name": "Traveling Salesman (Branch & Bound)",
        "category": "Branch and Bound",
        "paradigm": "Branch and Bound",
        "description": "Solves TSP to optimality using LC Branch & Bound with reduced cost matrix lower bound calculation.",
        "best_case": "O(n²)",
        "average_case": "O(n² 2^n)",
        "worst_case": "O(n² 2^n)",
        "space_complexity": "O(n² 2^n)",
        "recurrence_relation": "Lower Bound = parent_bound + edge_cost + row_reduction + col_reduction",
        "is_stable": True,
        "is_in_place": False,
        "is_adaptive": True,
        "is_deterministic": True,
        "pseudocode": """procedure tspBranchBound(distMatrix)
    initialBound = reduceMatrix(distMatrix)
    queue = PriorityQueue()
    queue.insert((initialBound, [0], reducedMatrix))
    minCost = infinity
    while not queue.isEmpty() do
        node = queue.extractMin()
        if node.bound >= minCost then continue
        if node.path.length == n then
            cost = pathCost(node.path) + dist[node.path[-1]][0]
            minCost = min(minCost, cost)
        else
            for each unvisited city c do
                newBound = calculateBound(node, c)
                if newBound < minCost then
                    queue.insert((newBound, node.path + [c], newMatrix))
    return minCost
end procedure""",
        "advantages": ["Exact optimal TSP solution", "Sharp lower bounds via matrix reduction", "Best-first search prunes aggressively"],
        "disadvantages": ["Exponential worst-case complexity", "Expensive bound calculations (O(n²) per node)", "Large memory requirements"],
        "suitable_cases": ["Small to medium TSP instances (n <= 25)", "Aviation crew scheduling", "CNC milling trajectory optimization"],
        "unsuitable_cases": ["Large TSP instances (n > 30)", "Real-time routing applications"],
        "daa_concept_notes": "Reduced cost matrix provides tight admissible lower bound. LC search minimizes nodes expanded to find optimum."
    }
]

# ==========================================
# 3. ALGORITHM-PROBLEM MAPPINGS (23 Algorithms -> 18 Curriculum Problems)
# ==========================================
MAPPINGS_DATA = [
    # Module 1: Divide and Conquer
    ("defective-chessboard", "defective-chessboard-problem", 1.0, "Canonical tromino tiling quadrant decomposition solver"),
    ("max-min-divide-conquer", "max-min-problem", 1.0, "Optimal 3n/2 - 2 comparisons simultaneous min-max finder"),
    ("strassen-matrix-multiplication", "matrix-multiplication-problem", 0.95, "Sub-cubic O(n^2.8074) Strassen matrix multiplication decomposition"),

    # Module 2: Backtracking
    ("n-queens-backtracking", "n-queens-problem", 0.95, "Standard state-space diagonal/column pruning solver"),
    ("subset-sum-backtracking", "subset-sum-problem", 0.9, "Exact combinatorial backtracking search with partial sum bounds"),
    ("hamiltonian-cycle-backtracking", "hamiltonian-cycle-problem", 0.9, "Exact Hamiltonian cycle finder with vertex adjacency pruning"),

    # Module 3: Dynamic Programming
    ("multistage-graph-dp", "multistage-graph-problem", 1.0, "Backward/forward DP path optimizer for k-stage partitioned graphs"),
    ("floyd-warshall-apsp", "all-pairs-shortest-path", 0.95, "Standard DP algorithm for dense all-pairs shortest paths"),
    ("optimal-bst-dp", "optimal-bst-problem", 1.0, "Optimal BST interval DP given key and dummy key access probabilities"),
    ("0-1-knapsack-dp", "0-1-knapsack-problem", 0.99, "Standard optimal DP tabulation solution for discrete knapsack items"),
    ("traveling-salesman-dp", "traveling-salesman-problem", 0.95, "Held-Karp Bitmask DP exact solver for small TSP instances"),
    ("reliability-design-dp", "reliability-design-problem", 1.0, "Multi-stage reliability maximization with dominated tuple elimination"),

    # Module 4: Greedy Method
    ("optimal-storage-tapes-greedy", "optimal-storage-tapes-problem", 1.0, "Shortest Program First greedy ordering minimizing Mean Retrieval Time"),
    ("fractional-knapsack", "fractional-knapsack-problem", 0.99, "Greedy optimal value/weight density selection for divisible items"),
    ("job-sequencing-deadlines", "job-sequencing-problem", 1.0, "Profit-sorted latest slot greedy task scheduling with deadlines"),
    ("optimal-merge-patterns-greedy", "optimal-merge-patterns-problem", 1.0, "2-way min-heap optimal merge tree construction minimizing record moves"),
    ("kruskal-mst", "minimum-spanning-tree", 0.95, "Optimal for sparse graphs (E << V^2) and disconnected forests via DSU"),
    ("prim-mst", "minimum-spanning-tree", 0.95, "Optimal for dense graphs (E ~ V^2) with priority queue cut relaxation"),
    ("dijkstra-sssp", "single-source-shortest-path", 0.98, "Optimal for non-negative edge weight graphs via greedy relaxation"),
    ("bellman-ford-sssp", "single-source-shortest-path", 0.85, "Mandatory when negative edge weights are present; detects cycles"),

    # Module 5: Branch and Bound (Shared Problem Domains: 0/1 Knapsack & TSP)
    ("0-1-knapsack-lc-bb", "0-1-knapsack-problem", 0.95, "Least-Cost Branch & Bound with fractional knapsack upper bound pruning"),
    ("0-1-knapsack-fifo-bb", "0-1-knapsack-problem", 0.90, "FIFO Breadth-First Branch & Bound with lower bound pruning"),
    ("traveling-salesman-bb", "traveling-salesman-problem", 0.92, "LC Branch & Bound with reduced cost matrix lower bounds and pruning"),
]


def seed_database(db: Session) -> None:
    """Seed the database strictly with the 23 curriculum algorithms and 18 problems, purging any stale items."""
    print("-> Seeding database...")

    # 1. Seed Admin & Student User
    existing_user = db.query(User).filter(User.email == "admin@daa-benchmark.edu").first()
    if not existing_user:
        admin = User(
            email="admin@daa-benchmark.edu",
            hashed_password=hash_password("admin123456"),
            full_name="DAA Laboratory Administrator",
            role="admin"
        )
        db.add(admin)

        student = User(
            email="student@daa-benchmark.edu",
            hashed_password=hash_password("student123456"),
            full_name="DAA Student Researcher",
            role="student"
        )
        db.add(student)
        db.commit()
        print("  [OK] Seeded default users (admin & student)")

    # 2. Seed Problems & Prune Stale Problems
    valid_prob_slugs = {p["slug"] for p in PROBLEMS_DATA}
    problem_map = {}
    for p_data in PROBLEMS_DATA:
        problem = db.query(Problem).filter(Problem.slug == p_data["slug"]).first()
        if not problem:
            problem = Problem(**p_data)
            db.add(problem)
            db.flush()
        else:
            for k, v in p_data.items():
                setattr(problem, k, v)
        problem_map[p_data["slug"]] = problem

    # 3. Seed Algorithms & Prune Stale Algorithms
    valid_algo_slugs = {a["slug"] for a in ALGORITHMS_DATA}
    algo_map = {}
    for a_data in ALGORITHMS_DATA:
        algo = db.query(Algorithm).filter(Algorithm.slug == a_data["slug"]).first()
        if not algo:
            algo = Algorithm(**a_data)
            db.add(algo)
            db.flush()
        else:
            for k, v in a_data.items():
                setattr(algo, k, v)
        algo_map[a_data["slug"]] = algo
    db.commit()

    # 4. Seed Algorithm-Problem Mappings
    valid_pair_ids = set()
    mapped_count = 0
    for algo_slug, prob_slug, score, notes in MAPPINGS_DATA:
        if algo_slug in algo_map and prob_slug in problem_map:
            algo_obj = algo_map[algo_slug]
            prob_obj = problem_map[prob_slug]
            valid_pair_ids.add((algo_obj.id, prob_obj.id))
            existing_mapping = db.query(AlgorithmProblemMapping).filter(
                AlgorithmProblemMapping.algorithm_id == algo_obj.id,
                AlgorithmProblemMapping.problem_id == prob_obj.id
            ).first()
            if not existing_mapping:
                mapping = AlgorithmProblemMapping(
                    algorithm_id=algo_obj.id,
                    problem_id=prob_obj.id,
                    suitability_score=score,
                    notes=notes
                )
                db.add(mapping)
                mapped_count += 1
            else:
                existing_mapping.suitability_score = score
                existing_mapping.notes = notes

    # Remove stale mappings not in MAPPINGS_DATA
    all_mappings = db.query(AlgorithmProblemMapping).all()
    stale_mappings_removed = 0
    for m in all_mappings:
        if (m.algorithm_id, m.problem_id) not in valid_pair_ids:
            db.delete(m)
            stale_mappings_removed += 1
    db.commit()

    # Remove stale algorithms from DB
    stale_algos = db.query(Algorithm).filter(~Algorithm.slug.in_(valid_algo_slugs)).all()
    stale_algos_removed = len(stale_algos)
    for sa in stale_algos:
        db.delete(sa)

    # Remove stale problems from DB
    stale_probs = db.query(Problem).filter(~Problem.slug.in_(valid_prob_slugs)).all()
    stale_probs_removed = len(stale_probs)
    for sp in stale_probs:
        db.delete(sp)
    db.commit()

    print(f"  [OK] Seeded {len(PROBLEMS_DATA)} curriculum problems (Removed stale: {stale_probs_removed})")
    print(f"  [OK] Seeded {len(ALGORITHMS_DATA)} curriculum algorithms (Removed stale: {stale_algos_removed})")
    print(f"  [OK] Seeded {len(valid_pair_ids)} algorithm-problem mappings (Removed stale: {stale_mappings_removed})")
    print("[OK] Database seeding completed successfully!")
