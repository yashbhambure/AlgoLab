"""
Authoritative DAA Curriculum Data Structure (7 Strict Modules)
Defines the canonical academic structure, topics, theoretical context,
computational implementations, and educational metadata.
"""
from typing import Dict, Any, List, Optional

CURRICULUM_MODULES: List[Dict[str, Any]] = [
    # =========================================================================
    # MODULE 1: DIVIDE-AND-CONQUER ALGORITHM
    # =========================================================================
    {
        "module_id": 1,
        "slug": "module-1-divide-and-conquer",
        "name": "Divide-and-Conquer Algorithm",
        "short_name": "Divide & Conquer",
        "description": "Decomposes a problem instance into smaller, non-overlapping subproblems of the same type, solves them recursively, and combines their solutions to form the global solution.",
        "general_method": {
            "title": "General Method — Divide, Conquer, Combine",
            "recurrence_template": "T(n) = a T(n/b) + f(n)",
            "principles": [
                "Divide: Partition the input problem into 'a' independent subproblems each of size n/b.",
                "Conquer: Solve subproblems recursively if size > threshold; else apply direct base case.",
                "Combine: Merge subproblem solutions into the global solution in f(n) time.",
                "Analysis: Asymptotic growth governed by Master Theorem and recursion tree bounds."
            ],
            "master_theorem_cases": [
                "Case 1 (Leaf Heavy): f(n) = O(n^(log_b(a) - eps)) => T(n) = Theta(n^(log_b(a)))",
                "Case 2 (Balanced): f(n) = Theta(n^(log_b(a)) * log^k(n)) => T(n) = Theta(n^(log_b(a)) * log^(k+1)(n))",
                "Case 3 (Root Heavy): f(n) = Omega(n^(log_b(a) + eps)) and regularity condition => T(n) = Theta(f(n))"
            ]
        },
        "topics": [
            {
                "topic_id": "1.1",
                "name": "General Method",
                "type": "theoretical_foundation",
                "slug": "divide-and-conquer-general-method",
                "description": "Mathematical framework of divide and conquer recurrences, Master Theorem, and recursion trees.",
                "time_complexity": "Varies by recurrence T(n) = aT(n/b) + f(n)",
                "space_complexity": "O(log n) call stack",
                "invariance": "Subproblems must be strictly disjoint and independent."
            },
            {
                "topic_id": "1.2",
                "name": "Defective Chessboard",
                "type": "computational",
                "slug": "defective-chessboard",
                "algorithm_slug": "defective-chessboard",
                "problem_slug": "defective-chessboard-problem",
                "method_name": "Tromino Tiling Divide & Conquer",
                "time_complexity": "O(n^2)",
                "space_complexity": "O(n^2)",
                "recurrence": "T(n) = 4T(n/2) + O(1)",
                "description": "Tiles a 2^k x 2^k board containing exactly one defective square using (4^k - 1)/3 L-shaped trominoes.",
                "real_world_applications": ["VLSI defect-tolerant chip layout", "Quadtree spatial partitioning", "Surface mesh tessellation"],
                "default_input": {"size": 4, "defect": [0, 0]}
            },
            {
                "topic_id": "1.3",
                "name": "Finding the Maximum and Minimum",
                "type": "computational",
                "slug": "max-min-divide-conquer",
                "algorithm_slug": "max-min-divide-conquer",
                "problem_slug": "max-min-problem",
                "method_name": "Min-Max Divide and Conquer",
                "time_complexity": "O(n)",
                "space_complexity": "O(log n)",
                "recurrence": "T(n) = 2T(n/2) + 2 with T(2)=1, T(1)=0 => 3n/2 - 2 comparisons",
                "description": "Simultaneously extracts minimum and maximum elements in an array using only 3n/2 - 2 comparisons (optimal comparison bound).",
                "real_world_applications": ["Sensor telemetry range normalization", "Graphics rendering bounding-box calculation", "Statistical outlier bounding"],
                "default_input": [22, 13, -5, 88, 41, 7, 95, 3]
            },
            {
                "topic_id": "1.4",
                "name": "Strassen's Matrix Multiplication",
                "type": "computational",
                "slug": "strassen-matrix-multiplication",
                "algorithm_slug": "strassen-matrix-multiplication",
                "problem_slug": "matrix-multiplication-problem",
                "method_name": "Strassen's 7-Product Sub-Cubic Decomposition",
                "time_complexity": "O(n^2.8074)",
                "space_complexity": "O(n^2)",
                "recurrence": "T(n) = 7T(n/2) + O(n^2)",
                "description": "Multiplies two n x n matrices using 7 recursive block multiplications rather than 8, breaking the O(n^3) cubic barrier.",
                "real_world_applications": ["Large-scale linear algebra systems", "Scientific computing & finite element simulations", "Deep learning kernel acceleration"],
                "default_input": {
                    "matrix_a": [[1, 2, 3, 4], [5, 6, 7, 8], [9, 1, 2, 3], [4, 5, 6, 7]],
                    "matrix_b": [[7, 6, 5, 4], [3, 2, 1, 9], [8, 7, 6, 5], [4, 3, 2, 1]]
                }
            }
        ]
    },

    # =========================================================================
    # MODULE 2: BACKTRACKING ALGORITHM
    # =========================================================================
    {
        "module_id": 2,
        "slug": "module-2-backtracking",
        "name": "Backtracking Algorithm",
        "short_name": "Backtracking",
        "description": "Constructs candidate solutions incrementally and abandons (backtracks from) a candidate branch as soon as it is determined that it cannot lead to a valid global solution.",
        "general_method": {
            "title": "General Method — State-Space Tree Exploration & Bounding Functions",
            "recurrence_template": "T(n) <= b^d (pruned depth-first search)",
            "principles": [
                "State-Space Tree: Systematically represents all potential solution states from root to leaf.",
                "Explicit Constraints: Rules defining valid values for individual decision variables.",
                "Implicit Constraints: Relational criteria determining which variable tuples satisfy the problem.",
                "Bounding & Pruning: Tests intermediate nodes to prune non-viable subtrees without exhaustive enumeration."
            ]
        },
        "topics": [
            {
                "topic_id": "2.1",
                "name": "General Method",
                "type": "theoretical_foundation",
                "slug": "backtracking-general-method",
                "description": "Systematic state-space tree traversal, bounding functions, and dead-end pruning mechanics.",
                "time_complexity": "O(b^d) worst-case combinatorial search",
                "space_complexity": "O(d) stack depth",
                "invariance": "Pruning must never discard an active branch containing a valid solution."
            },
            {
                "topic_id": "2.2",
                "name": "N-Queens Problem",
                "type": "computational",
                "slug": "n-queens-backtracking",
                "algorithm_slug": "n-queens-backtracking",
                "problem_slug": "n-queens-problem",
                "method_name": "Backtracking with Diagonal & Column Pruning",
                "time_complexity": "O(N!)",
                "space_complexity": "O(N)",
                "recurrence": "T(N) = N * T(N-1) + O(N)",
                "description": "Places N non-attacking queens on an N x N chessboard such that no two queens share a row, column, or diagonal.",
                "real_world_applications": ["VLSI routing collision avoidance", "Parallel process dead-lock free scheduling", "Constraint Satisfaction Problems (CSP)"],
                "default_input": {"n": 4}
            },
            {
                "topic_id": "2.3",
                "name": "Sum of Subsets Problem",
                "type": "computational",
                "slug": "subset-sum-backtracking",
                "algorithm_slug": "subset-sum-backtracking",
                "problem_slug": "subset-sum-problem",
                "method_name": "Binary Inclusion/Exclusion State-Space Pruning",
                "time_complexity": "O(2^n)",
                "space_complexity": "O(n)",
                "recurrence": "T(n) = 2T(n-1) + O(1)",
                "description": "Finds all subsets of a given set of positive integers whose sum equals target sum S using partial sum bounds.",
                "real_world_applications": ["Budget parcel allocation", "Cryptographic knapsack cryptosystems", "Financial audit transaction matching"],
                "default_input": {"array": [3, 5, 6, 7], "target": 15}
            },
            {
                "topic_id": "2.4",
                "name": "Hamiltonian Cycles",
                "type": "computational",
                "slug": "hamiltonian-cycle-backtracking",
                "algorithm_slug": "hamiltonian-cycle-backtracking",
                "problem_slug": "hamiltonian-cycle-problem",
                "method_name": "Vertex Adjacency Backtracking Search",
                "time_complexity": "O(V!)",
                "space_complexity": "O(V)",
                "recurrence": "T(V) = V * T(V-1) + O(V)",
                "description": "Determines whether a graph contains a closed loop visiting every vertex exactly once and returning to the start.",
                "real_world_applications": ["Circuit board drilling tool paths", "DNA physical genome mapping", "Courier delivery round-trip verification"],
                "default_input": {
                    "num_vertices": 5,
                    "edges": [[0, 1], [1, 2], [2, 3], [3, 4], [4, 0], [0, 2], [1, 3], [2, 4]]
                }
            }
        ]
    },

    # =========================================================================
    # MODULE 3: DYNAMIC PROGRAMMING ALGORITHM
    # =========================================================================
    {
        "module_id": 3,
        "slug": "module-3-dynamic-programming",
        "name": "Dynamic Programming Algorithm",
        "short_name": "Dynamic Programming",
        "description": "Solves multi-stage optimization problems by breaking them down into overlapping subproblems, guaranteeing global optimality through Bellman's Principle of Optimality.",
        "general_method": {
            "title": "General Method — Principle of Optimality & Memoization/Tabulation",
            "recurrence_template": "Opt(S) = min/max_{decision} { cost(decision) + Opt(subproblem) }",
            "principles": [
                "Principle of Optimality: An optimal policy has the property that whatever the initial state and decision are, the remaining decisions must constitute an optimal policy with regard to the state resulting from the first decision.",
                "Overlapping Subproblems: The problem space contains polynomial distinct subproblems recomputed exponentially in naive recursion.",
                "Tabulation (Bottom-Up): Evaluates base cases first and populates lookup table in topological subproblem order.",
                "Memoization (Top-Down): Caches recursive function outputs to ensure each subproblem is evaluated at most once."
            ]
        },
        "topics": [
            {
                "topic_id": "3.1",
                "name": "General Method",
                "type": "theoretical_foundation",
                "slug": "dp-general-method",
                "description": "Bellman's Principle of Optimality, optimal substructure, and state transition table construction.",
                "time_complexity": "O(states * transitions_per_state)",
                "space_complexity": "O(states)",
                "invariance": "Subproblem optimal solutions must compose strictly into global optimal solutions."
            },
            {
                "topic_id": "3.2",
                "name": "Multistage Graphs",
                "type": "computational",
                "slug": "multistage-graph-dp",
                "algorithm_slug": "multistage-graph-dp",
                "problem_slug": "multistage-graph-problem",
                "method_name": "Backward/Forward Dynamic Programming",
                "time_complexity": "O(V + E)",
                "space_complexity": "O(V)",
                "recurrence": "cost(i, j) = min_{l in V_{i+1}} { c(j, l) + cost(i+1, l) }",
                "description": "Finds minimum cost path from source (stage 1) to sink (stage k) in a k-stage partitioned directed graph.",
                "real_world_applications": ["Supply chain manufacturing logistics", "Pipeline stage resource scheduling", "Network routing across transit tiers"],
                "default_input": {
                    "num_vertices": 8,
                    "stages": 4,
                    "edges": [
                        {"from": 1, "to": 2, "weight": 2}, {"from": 1, "to": 3, "weight": 1}, {"from": 1, "to": 4, "weight": 3},
                        {"from": 2, "to": 5, "weight": 2}, {"from": 2, "to": 6, "weight": 3}, {"from": 3, "to": 5, "weight": 6},
                        {"from": 3, "to": 6, "weight": 7}, {"from": 4, "to": 6, "weight": 6}, {"from": 4, "to": 7, "weight": 8},
                        {"from": 5, "to": 8, "weight": 1}, {"from": 6, "to": 8, "weight": 4}, {"from": 7, "to": 8, "weight": 2}
                    ]
                }
            },
            {
                "topic_id": "3.3",
                "name": "All-Pairs Shortest Path Problem",
                "type": "computational",
                "slug": "all-pairs-shortest-path-dp",
                "algorithm_slug": "floyd-warshall-apsp",
                "problem_slug": "all-pairs-shortest-path",
                "method_name": "Floyd-Warshall Dynamic Programming Matrix Relaxation",
                "time_complexity": "O(V^3)",
                "space_complexity": "O(V^2)",
                "recurrence": "D^(k)[i, j] = min(D^(k-1)[i, j], D^(k-1)[i, k] + D^(k-1)[k, j])",
                "description": "Computes shortest path distances between all pairs of vertices in a weighted graph with possible negative weights.",
                "real_world_applications": ["Global telecommunication latency tables", "Transitive closure in database query compilers", "Urban transit travel time matrix"],
                "default_input": {
                    "matrix": [
                        [0, 3, float("inf"), 7],
                        [8, 0, 2, float("inf")],
                        [5, float("inf"), 0, 1],
                        [2, float("inf"), float("inf"), 0]
                    ]
                }
            },
            {
                "topic_id": "3.4",
                "name": "Optimal Binary Search Trees",
                "type": "computational",
                "slug": "optimal-bst-dp",
                "algorithm_slug": "optimal-bst-dp",
                "problem_slug": "optimal-bst-problem",
                "method_name": "OBST Dynamic Programming / Knuth Optimization",
                "time_complexity": "O(n^3)",
                "space_complexity": "O(n^2)",
                "recurrence": "e[i, j] = min_{i < r <= j} { e[i, r-1] + e[r, j] } + w(i, j)",
                "description": "Constructs a binary search tree with minimum expected search cost given access probabilities of keys and dummy keys.",
                "real_world_applications": ["Compiler symbol table lookups", "Dictionary / auto-complete search indexing", "Network packet header inspection filters"],
                "default_input": {
                    "keys": ["k1", "k2", "k3", "k4"],
                    "p": [0.1, 0.2, 0.4, 0.3],
                    "q": [0.05, 0.1, 0.05, 0.05, 0.05]
                }
            },
            {
                "topic_id": "3.5",
                "name": "0/1 Knapsack Problem",
                "type": "computational",
                "slug": "0-1-knapsack-dp",
                "algorithm_slug": "0-1-knapsack-dp",
                "problem_slug": "0-1-knapsack-problem",
                "method_name": "2D Tabulation 0/1 Knapsack DP",
                "time_complexity": "O(n * W)",
                "space_complexity": "O(n * W)",
                "recurrence": "V[i, w] = max(V[i-1, w], V[i-1, w - wt[i]] + val[i])",
                "description": "Selects subset of indivisible items to maximize total profit without exceeding weight capacity W.",
                "real_world_applications": ["Capital expenditure portfolio budgeting", "Cargo container payload loading", "Server VM resource packing"],
                "default_input": {"weights": [2, 3, 4, 5], "values": [3, 4, 5, 6], "capacity": 5}
            },
            {
                "topic_id": "3.6",
                "name": "Traveling Salesman Problem",
                "type": "computational",
                "slug": "traveling-salesman-dp",
                "algorithm_slug": "traveling-salesman-dp",
                "problem_slug": "traveling-salesman-problem",
                "method_name": "Held-Karp Bitmask Dynamic Programming",
                "time_complexity": "O(n^2 2^n)",
                "space_complexity": "O(n 2^n)",
                "recurrence": "C(S, j) = min_{i in S, i != j} { C(S \\ {j}, i) + dist(i, j) }",
                "description": "Finds exact minimum cost Hamiltonian cycle visiting every city once and returning to the origin.",
                "real_world_applications": ["Logistics vehicle route optimization", "Robotic laser PCB drilling", "Microchip wire length minimization"],
                "default_input": {
                    "distance_matrix": [
                        [0, 10, 15, 20],
                        [10, 0, 35, 25],
                        [15, 35, 0, 30],
                        [20, 25, 30, 0]
                    ],
                    "cities": ["A", "B", "C", "D"]
                }
            },
            {
                "topic_id": "3.7",
                "name": "Reliability Design",
                "type": "computational",
                "slug": "reliability-design-dp",
                "algorithm_slug": "reliability-design-dp",
                "problem_slug": "reliability-design-problem",
                "method_name": "Multi-Stage Reliability Optimization with Dominated Set Pruning",
                "time_complexity": "O(n C^2)",
                "space_complexity": "O(n C)",
                "recurrence": "S^i = purge_dominated( { (R * phi_i(m_i), C + m_i * c_i) } )",
                "description": "Determines parallel duplicate device counts for n series stages to maximize total system reliability subject to a budget constraint C.",
                "real_world_applications": ["Aerospace avionics fault-tolerant redundancy", "Nuclear plant safety telemetry systems", "Mission-critical datacenter power grid design"],
                "default_input": {
                    "reliabilities": [0.9, 0.8, 0.5],
                    "costs": [30, 15, 20],
                    "budget": 105
                }
            }
        ]
    },

    # =========================================================================
    # MODULE 4: GREEDY METHOD ALGORITHM
    # =========================================================================
    {
        "module_id": 4,
        "slug": "module-4-greedy-method",
        "name": "Greedy Method Algorithm",
        "short_name": "Greedy Method",
        "description": "Constructs a solution through a sequence of locally optimal choices, relying on the greedy choice property and optimal substructure to achieve global optimality.",
        "general_method": {
            "title": "General Method — Greedy Choice Property & Matroid Theory",
            "recurrence_template": "Solution = Union(Solution, { argmax_{candidate} LocalGain(candidate) })",
            "principles": [
                "Greedy Choice Property: A globally optimal solution can be arrived at by making a locally optimal (greedy) choice without looking ahead.",
                "Optimal Substructure: An optimal solution to the problem contains within it optimal solutions to subproblems.",
                "Proof Techniques: Exchange arguments and mathematical induction to prove that greedy choices never preclude global optimum."
            ]
        },
        "topics": [
            {
                "topic_id": "4.1",
                "name": "General Method",
                "type": "theoretical_foundation",
                "slug": "greedy-general-method",
                "description": "Greedy choice property, optimal substructure, and matroid exchange theorems.",
                "time_complexity": "O(n log n) sorting + O(n) greedy selection",
                "space_complexity": "O(1) to O(n)",
                "invariance": "Locally optimal choice must never be retracted."
            },
            {
                "topic_id": "4.2",
                "name": "Optimal Storage on Tapes",
                "type": "computational",
                "slug": "optimal-storage-tapes-greedy",
                "algorithm_slug": "optimal-storage-tapes-greedy",
                "problem_slug": "optimal-storage-tapes-problem",
                "method_name": "Shortest Program First (SPF) Greedy Ordering",
                "time_complexity": "O(n log n)",
                "space_complexity": "O(n)",
                "recurrence": "MRT = (1/n) * sum_{i=1}^n (n - i + 1) * l_i",
                "description": "Orders programs on magnetic tape(s) in non-decreasing order of lengths to minimize Mean Retrieval Time (MRT).",
                "real_world_applications": ["Tape library backup sequential storage", "Database sequential scan log compaction", "Audio track sequential streaming queue"],
                "default_input": {
                    "lengths": [5, 10, 3, 20, 12, 7],
                    "tapes": 1,
                    "programs": ["P1", "P2", "P3", "P4", "P5", "P6"]
                }
            },
            {
                "topic_id": "4.3",
                "name": "Fractional Knapsack Problem",
                "type": "computational",
                "slug": "fractional-knapsack-greedy",
                "algorithm_slug": "fractional-knapsack",
                "problem_slug": "fractional-knapsack-problem",
                "method_name": "Value/Weight Density Greedy Selection",
                "time_complexity": "O(n log n)",
                "space_complexity": "O(1)",
                "recurrence": "T(n) = O(n log n) sorting + O(n) scan",
                "description": "Maximizes total profit in knapsack of capacity W where fractional quantities of items can be taken.",
                "real_world_applications": ["Commodity liquid chemical blending", "Continuous bandwidth allocation", "Mineral ore smelting load optimization"],
                "default_input": {"weights": [10, 20, 30], "values": [60, 100, 120], "capacity": 50}
            },
            {
                "topic_id": "4.4",
                "name": "Job Sequencing with Deadlines",
                "type": "computational",
                "slug": "job-sequencing-deadlines",
                "algorithm_slug": "job-sequencing-deadlines",
                "problem_slug": "job-sequencing-problem",
                "method_name": "Profit-Sorted Latest Slot Greedy Scheduling",
                "time_complexity": "O(n log n + n * d_max)",
                "space_complexity": "O(d_max)",
                "recurrence": "T(n) = O(n log n) + O(n * d_max)",
                "description": "Schedules unit-time jobs with deadlines and profits to maximize total profit by placing each job in the latest available free time slot.",
                "real_world_applications": ["Real-time embedded task execution", "Financial trade execution before settlement windows", "Manufacturing queue job sequencing"],
                "default_input": {
                    "jobs": [
                        {"id": "J1", "deadline": 2, "profit": 100},
                        {"id": "J2", "deadline": 1, "profit": 19},
                        {"id": "J3", "deadline": 2, "profit": 27},
                        {"id": "J4", "deadline": 1, "profit": 25},
                        {"id": "J5", "deadline": 3, "profit": 15}
                    ]
                }
            },
            {
                "topic_id": "4.5",
                "name": "Optimal Merge Patterns",
                "type": "computational",
                "slug": "optimal-merge-patterns-greedy",
                "algorithm_slug": "optimal-merge-patterns-greedy",
                "problem_slug": "optimal-merge-patterns-problem",
                "method_name": "2-Way Merge Tree Min-Heap Algorithm",
                "time_complexity": "O(n log n)",
                "space_complexity": "O(n)",
                "recurrence": "T(n) = sum of n-1 pairwise merge costs",
                "description": "Merges n sorted files of varying lengths into one sorted file with minimum total record movement using a min-heap.",
                "real_world_applications": ["External merge sort file runs", "Distributed log stream consolidation", "Data stream aggregation in big data frameworks"],
                "default_input": {"files": [20, 30, 10, 5, 30], "names": ["F1", "F2", "F3", "F4", "F5"]}
            },
            {
                "topic_id": "4.6",
                "name": "Minimum Spanning Trees",
                "type": "computational",
                "slug": "minimum-spanning-trees-greedy",
                "algorithm_slug": "kruskal-mst",
                "algorithm_slugs": ["kruskal-mst", "prim-mst"],
                "problem_slug": "minimum-spanning-tree",
                "method_name": "Kruskal's (DSU) & Prim's (Cut-Relaxation) Algorithms",
                "time_complexity": "O(E log E) / O((V + E) log V)",
                "space_complexity": "O(V + E)",
                "recurrence": "T(V, E) = O(E log E) or O(E + V log V)",
                "description": "Finds a tree spanning all vertices with minimal total edge weight in connected undirected graphs.",
                "real_world_applications": ["Electrical power grid distribution design", "Telecommunication fiber optic backbones", "Cluster analysis / single-linkage clustering"],
                "default_input": {
                    "vertices": ["0", "1", "2", "3"],
                    "edges": [["0", "1", 10], ["0", "2", 6], ["0", "3", 5], ["1", "3", 15], ["2", "3", 4]]
                }
            },
            {
                "topic_id": "4.7",
                "name": "Single-Source Shortest Path Problem",
                "type": "computational",
                "slug": "single-source-shortest-path-greedy",
                "algorithm_slug": "dijkstra-sssp",
                "algorithm_slugs": ["dijkstra-sssp", "bellman-ford-sssp"],
                "problem_slug": "single-source-shortest-path",
                "method_name": "Dijkstra's Greedy Relaxation & Bellman-Ford DP",
                "time_complexity": "O((V + E) log V) / O(V * E)",
                "space_complexity": "O(V)",
                "recurrence": "T(V, E) = O((V + E) log V)",
                "description": "Computes shortest paths from a single origin vertex to all other reachable vertices in weighted graphs.",
                "real_world_applications": ["GPS vehicular route navigation", "Internet IP packet routing protocols (OSPF, IS-IS)", "Social network shortest connection degree"],
                "default_input": {
                    "vertices": ["A", "B", "C", "D"],
                    "edges": [["A", "B", 1], ["B", "C", 2], ["A", "C", 4], ["C", "D", 1]],
                    "source": "A"
                }
            }
        ]
    },

    # =========================================================================
    # MODULE 5: BRANCH AND BOUND ALGORITHM
    # =========================================================================
    {
        "module_id": 5,
        "slug": "module-5-branch-and-bound",
        "name": "Branch and Bound Algorithm",
        "short_name": "Branch & Bound",
        "description": "Solves combinatorial optimization problems by systematically partitioning the solution space (branching) and computing upper/lower bounds to prune suboptimal branches (bounding).",
        "general_method": {
            "title": "General Method — LC Search, FIFO Search & Bounding Functions",
            "recurrence_template": "State-Space Tree with Priority Queue or FIFO Queue Pruning",
            "principles": [
                "Branching: Dividing the feasible region into smaller subregions forming a search tree.",
                "Bounding: Computing upper/lower bounds on the optimal objective value achievable in a subregion.",
                "Pruning: Discarding nodes whose bound is worse than the best known feasible solution.",
                "LC (Least Cost / Best First): Uses a priority queue to always expand the live node with the most promising bound.",
                "FIFO (First In First Out): Uses a standard queue for breadth-first level-by-level search tree exploration."
            ]
        },
        "topics": [
            {
                "topic_id": "5.1",
                "name": "General Method",
                "type": "theoretical_foundation",
                "slug": "branch-and-bound-general-method",
                "description": "Mathematical framework of state-space tree branching, LC search vs FIFO search, and bounding functions.",
                "time_complexity": "O(2^n) worst-case with high empirical pruning",
                "space_complexity": "O(2^n) queue/heap storage",
                "invariance": "Bounding function must be admissible (never overestimate maximum profit or underestimate minimum cost)."
            },
            {
                "topic_id": "5.2",
                "name": "0/1 Knapsack Problem — LC Branch and Bound Solution",
                "type": "computational",
                "slug": "0-1-knapsack-lc-bb",
                "algorithm_slug": "0-1-knapsack-lc-bb",
                "algorithm_slugs": ["0-1-knapsack-lc-bb"],
                "problem_slug": "0-1-knapsack-problem",
                "method_name": "Least-Cost (LC) Branch and Bound with Fractional Knapsack Upper Bound",
                "time_complexity": "O(2^n) worst case, O(n) best case",
                "space_complexity": "O(2^n)",
                "recurrence": "u(N) = Fractional Knapsack Bound for remaining items",
                "description": "Explores the 0/1 Knapsack state-space tree using a max-priority queue ordered by upper bound, aggressively pruning subtrees.",
                "real_world_applications": ["High-value investment portfolio optimization", "Satellite payload space allocation", "Critical cargo dispatch with tight tolerances"],
                "default_input": {"weights": [2, 4, 6, 9], "values": [10, 10, 12, 18], "capacity": 15}
            },
            {
                "topic_id": "5.3",
                "name": "0/1 Knapsack Problem — FIFO Branch and Bound Solution",
                "type": "computational",
                "slug": "0-1-knapsack-fifo-bb",
                "algorithm_slug": "0-1-knapsack-fifo-bb",
                "algorithm_slugs": ["0-1-knapsack-fifo-bb"],
                "problem_slug": "0-1-knapsack-problem",
                "method_name": "FIFO Queue Breadth-First Branch and Bound with Pruning",
                "time_complexity": "O(2^n) worst case, O(n) best case",
                "space_complexity": "O(2^n)",
                "recurrence": "Breadth-first state expansion with bound pruning",
                "description": "Explores the 0/1 Knapsack state-space tree level-by-level using a FIFO queue, discarding branches whose bound falls below best known profit.",
                "real_world_applications": ["Real-time memory-bound scheduling", "Discrete manufacturing batch production planning", "Hardware constraint synthesis"],
                "default_input": {"weights": [2, 4, 6, 9], "values": [10, 10, 12, 18], "capacity": 15}
            },
            {
                "topic_id": "5.4",
                "name": "Traveling Salesman Problem",
                "type": "computational",
                "slug": "traveling-salesman-bb",
                "algorithm_slug": "traveling-salesman-bb",
                "algorithm_slugs": ["traveling-salesman-bb"],
                "problem_slug": "traveling-salesman-problem",
                "method_name": "LC Branch and Bound with Reduced Cost Matrix",
                "time_complexity": "O(n^2 2^n)",
                "space_complexity": "O(n^2 2^n)",
                "recurrence": "Lower Bound = parent_bound + edge_cost + matrix_reduction_cost",
                "description": "Solves TSP to optimality by reducing row/column costs to compute sharp lower bounds and exploring branches with best-first priority.",
                "real_world_applications": ["Aviation flight crew scheduling", "CNC milling cutter trajectory optimization", "Semiconductor wafer inspection routing"],
                "default_input": {
                    "distance_matrix": [
                        [float('inf'), 20, 30, 10, 11],
                        [15, float('inf'), 16, 4, 2],
                        [3, 5, float('inf'), 2, 4],
                        [19, 6, 18, float('inf'), 3],
                        [16, 4, 7, 16, float('inf')]
                    ],
                    "cities": ["A", "B", "C", "D", "E"]
                }
            }
        ]
    },

    # =========================================================================
    # MODULE 6: P AND NP PROBLEMS (THEORY ONLY)
    # =========================================================================
    {
        "module_id": 6,
        "slug": "module-6-p-and-np-problems",
        "name": "P and NP Problems",
        "short_name": "P and NP",
        "description": "Foundational computational complexity theory classifying decision problems by tractability, deterministic polynomial time (P), and nondeterministic polynomial verification (NP).",
        "general_method": {
            "title": "Theoretical Complexity Foundations — Tractability & Nondeterminism",
            "recurrence_template": "Complexity Classes P, NP, and the P vs NP Millennium Problem",
            "principles": [
                "Decision Problem: A computational problem with a binary yes/no answer for any given instance.",
                "Language Recognition: A language L subset of {0, 1}* is decided by an algorithm A if A accepts all x in L and rejects all x not in L.",
                "Tractability: Problems solvable in polynomial time O(n^k) for constant k are tractable; exponential lower bounds Omega(2^n) are intractable.",
                "P (Polynomial Time): Class of languages decidable by a Deterministic Turing Machine (DTM) in polynomial time.",
                "NP (Nondeterministic Polynomial Time): Class of languages verifiable by a DTM in polynomial time given a polynomial-size certificate, or decidable by a Nondeterministic Turing Machine (NDTM) in polynomial time."
            ]
        },
        "topics": [
            {
                "topic_id": "6.1",
                "name": "Tractable Problems",
                "type": "theoretical",
                "slug": "tractable-problems",
                "description": "Problems with polynomial-time upper bounds O(n^k) (e.g. SSSP, MST, 2-way merge) that scale efficiently on modern hardware.",
                "asymptotic_characterization": "Upper bounded by O(n^k) for fixed constant k",
                "canonical_examples": ["Single-Source Shortest Path (Dijkstra)", "Minimum Spanning Tree (Kruskal/Prim)", "Optimal Merge Patterns"],
                "key_takeaway": "Polynomial growth ensures that doubling input size increases runtime by a constant factor 2^k."
            },
            {
                "topic_id": "6.2",
                "name": "Non-Tractable Problems",
                "type": "theoretical",
                "slug": "non-tractable-problems",
                "description": "Intractable or super-polynomial problems (e.g., exact TSP, general Hamiltonian Cycle, Subset Sum) whose worst-case complexity requires Omega(c^n) operations.",
                "asymptotic_characterization": "Lower bounded by Omega(2^(n^c)) or Omega(n!)",
                "canonical_examples": ["Traveling Salesman Problem (Exact)", "Hamiltonian Cycle", "N-Queens (All Solutions)"],
                "key_takeaway": "Even modest increases in N (e.g. N=50 to N=100) render exact exhaustive solutions computationally unreachable in the lifetime of the universe."
            },
            {
                "topic_id": "6.3",
                "name": "P (Deterministic Polynomial Time)",
                "type": "theoretical",
                "slug": "class-p",
                "description": "Formal definition of complexity class P: { L | L is decided by a Deterministic Turing Machine in time O(n^k) for some k > 0 }.",
                "formal_definition": "P = Union_{k >= 0} TIME(n^k)",
                "properties": [
                    "Closed under union, intersection, complementation, and concatenation.",
                    "Invariant across all standard computational models (RAM model, Turing Machine, Lambda Calculus) by the Extended Church-Turing Thesis."
                ]
            },
            {
                "topic_id": "6.4",
                "name": "NP (Nondeterministic Polynomial Time)",
                "type": "theoretical",
                "slug": "class-np",
                "description": "Formal definition of complexity class NP: problems where a candidate solution (certificate) can be verified in deterministic polynomial time.",
                "formal_definition": "NP = Union_{k >= 0} NTIME(n^k) = { L | exists poly-time verifier V and constant c s.t. x in L iff exists certificate y (|y| <= |x|^c) with V(x, y) = 1 }",
                "properties": [
                    "P is a subset of NP (every problem solvable in polynomial time can be verified in polynomial time).",
                    "The P = NP question asks whether every problem with easily verifiable solutions also possesses an easily discoverable solution."
                ]
            }
        ]
    },

    # =========================================================================
    # MODULE 7: NP-HARD AND NP-COMPLETE PROBLEMS (THEORY ONLY)
    # =========================================================================
    {
        "module_id": 7,
        "slug": "module-7-np-hard-and-np-complete",
        "name": "NP-Hard and NP-Complete Problems",
        "short_name": "NP-Hard & NP-Complete",
        "description": "Advanced computational complexity theory covering polynomial-time reductions, NP-Hard lower bounds, the NP-Complete equivalence class, and Cook's Theorem.",
        "general_method": {
            "title": "Theoretical Complexity Foundations — Reductions & Cook's Theorem",
            "recurrence_template": "Polynomial-Time Many-One Reductions L_1 <=_p L_2",
            "principles": [
                "Polynomial-Time Reduction (L_1 <=_p L_2): A polynomial-time computable function f: {0,1}* -> {0,1}* such that for all x, x in L_1 iff f(x) in L_2.",
                "NP-Hardness: A problem H is NP-Hard if for every L in NP, L <=_p H. (H is at least as hard as any problem in NP).",
                "NP-Completeness: A problem C is NP-Complete if: (1) C in NP, and (2) C is NP-Hard.",
                "Cook's Theorem (Cook-Levin 1971): Proved that the Boolean Satisfiability problem (SAT) is NP-Complete, anchoring the reduction hierarchy."
            ]
        },
        "topics": [
            {
                "topic_id": "7.1",
                "name": "NP-Hard Problems",
                "type": "theoretical",
                "slug": "np-hard-problems",
                "description": "Problems to which every problem in NP can be reduced in polynomial time. NP-Hard problems need not be decision problems and need not belong to NP (e.g. Halting Problem, TSP Optimization).",
                "formal_definition": "H is NP-Hard iff for all L in NP, L <=_p H",
                "properties": [
                    "If any NP-Hard problem is solvable in polynomial time, then P = NP.",
                    "Includes both decision and optimization variants (e.g. TSP Optimization: finding the exact minimum cost tour)."
                ]
            },
            {
                "topic_id": "7.2",
                "name": "NP-Complete Problems",
                "type": "theoretical",
                "slug": "np-complete-problems",
                "description": "The hardest decision problems in NP. If any single NP-Complete problem has a polynomial-time algorithm, then every problem in NP can be solved in polynomial time.",
                "formal_definition": "C is NP-Complete iff C in NP and C is NP-Hard",
                "canonical_reductions": [
                    "Circuit-SAT <=_p SAT (Cook-Levin Theorem)",
                    "SAT <=_p 3-SAT",
                    "3-SAT <=_p Vertex Cover <=_p Independent Set <=_p Clique",
                    "3-SAT <=_p Subset Sum <=_p 0/1 Knapsack (Decision Variant)",
                    "3-SAT <=_p Directed Hamiltonian Cycle <=_p Undirected Hamiltonian Cycle <=_p TSP Decision"
                ]
            },
            {
                "topic_id": "7.3",
                "name": "Cook's Theorem (Cook-Levin Theorem)",
                "type": "theoretical",
                "slug": "cooks-theorem",
                "description": "Landmark 1971 theorem proving that the Boolean Satisfiability problem (SAT) is NP-Complete by directly encoding the polynomial-time execution of any Nondeterministic Turing Machine as a boolean formula.",
                "theorem_statement": "SAT = { phi | phi is a satisfiable Boolean CNF formula } is NP-Complete.",
                "proof_architecture": [
                    "1. SAT in NP: A truth assignment to variables can be evaluated in deterministic polynomial time.",
                    "2. SAT is NP-Hard: Given any language L in NP decided by NDTM M in time n^k, encode M's computation tableau into a Boolean CNF formula phi_w of size O(n^(2k)) such that w in L iff phi_w is satisfiable."
                ],
                "impact": "Provided the foundational first NP-Complete problem, enabling Karp's 21 NP-Complete problems through pairwise polynomial-time reductions."
            }
        ]
    }
]


def get_curriculum_modules() -> List[Dict[str, Any]]:
    """Returns all 7 authoritative DAA curriculum modules."""
    return CURRICULUM_MODULES


def get_curriculum_module(module_id: Any) -> Optional[Dict[str, Any]]:
    """Returns a specific curriculum module by module number (1-7) or slug."""
    for m in CURRICULUM_MODULES:
        if str(m["module_id"]) == str(module_id) or m["slug"] == str(module_id):
            return m
    return None


def get_all_approved_algorithm_slugs() -> List[str]:
    """
    Returns the list of all 23 authoritative executable algorithm slugs
    explicitly approved across the 7 curriculum modules.
    """
    slugs: List[str] = []
    for m in CURRICULUM_MODULES:
        for t in m.get("topics", []):
            if t.get("algorithm_slugs"):
                for s in t["algorithm_slugs"]:
                    if s not in slugs:
                        slugs.append(s)
            elif t.get("algorithm_slug"):
                s = t["algorithm_slug"]
                if s not in slugs:
                    slugs.append(s)
    return slugs


def get_algorithm_curriculum_info(slug: str) -> Optional[Dict[str, Any]]:
    """
    Returns curriculum metadata (module_id, module_name, topic) for an approved algorithm.
    """
    for m in CURRICULUM_MODULES:
        for t in m.get("topics", []):
            if (t.get("algorithm_slug") == slug) or (slug in t.get("algorithm_slugs", [])):
                return {
                    "is_curriculum": True,
                    "module_id": m["module_id"],
                    "module_name": m["name"],
                    "module_slug": m["slug"],
                    "topic_id": t.get("topic_id"),
                    "topic_name": t.get("name"),
                    "recurrence": t.get("recurrence")
                }
    return None
