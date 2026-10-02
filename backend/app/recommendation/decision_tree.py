"""
Interactive DAA Algorithm Decision Tree Engine.
Enables guided algorithm selection via step-by-step query traversal across all
authoritative curriculum computational problem paradigms and problem domains.
"""
from typing import Dict, Any, List, Optional


class AlgorithmDecisionTree:
    """
    Hierarchical decision tree for deterministic algorithm selection across the 23 DAA curriculum algorithms.
    """

    TREE_DATA: Dict[str, Any] = {
        "id": "root",
        "question": "What primary algorithmic problem paradigm or problem domain are you addressing?",
        "options": [
            {"label": "Divide and Conquer Problems", "next_node": "dc_problem_type"},
            {"label": "Backtracking & Constraint Satisfaction", "next_node": "backtracking_problem_type"},
            {"label": "Dynamic Programming Problems", "next_node": "dp_problem_type"},
            {"label": "Greedy Optimization Problems", "next_node": "greedy_problem_type"},
            {"label": "Branch and Bound Search", "next_node": "bb_problem_type"},
            {"label": "Shortest Path in Graph", "next_node": "shortest_path_type"},
            {"label": "Minimum Spanning Tree (MST)", "next_node": "greedy_mst_type"},
            {"label": "Knapsack / Resource Allocation", "next_node": "knapsack_divisibility"},
            {"label": "Traveling Salesman Problem (TSP)", "next_node": "tsp_approach"},
        ],
        "nodes": {
            # =========================================================================
            # 1. DIVIDE AND CONQUER
            # =========================================================================
            "dc_problem_type": {
                "question": "Which Divide & Conquer computational problem are you solving?",
                "options": [
                    {"label": "Simultaneous Maximum and Minimum Finding", "next_node": "dc_max_min"},
                    {"label": "Matrix Multiplication (Sub-cubic)", "next_node": "dc_matrix_mult"},
                    {"label": "Defective Chessboard / Tromino Tiling", "next_node": "dc_defective_chessboard"},
                ]
            },
            "dc_max_min": {
                "question": "What is the optimization goal for element extraction?",
                "options": [
                    {
                        "label": "Optimal comparison bound (3n/2 - 2 comparisons)",
                        "leaf": {
                            "algorithm_slug": "max-min-divide-conquer",
                            "name": "Finding Maximum and Minimum (Divide & Conquer)",
                            "complexity": "O(n)",
                            "space": "O(log n)",
                            "reasoning": "Splits array into halves recursively to achieve exactly 3n/2 - 2 element comparisons, matching the information-theoretic lower bound."
                        }
                    }
                ]
            },
            "dc_matrix_mult": {
                "question": "What is the matrix dimension and performance requirement?",
                "options": [
                    {
                        "label": "Sub-cubic asymptotic scaling for large matrices (O(n^2.8074))",
                        "leaf": {
                            "algorithm_slug": "strassen-matrix-multiplication",
                            "name": "Strassen's Matrix Multiplication",
                            "complexity": "O(n^2.8074)",
                            "space": "O(n^2)",
                            "reasoning": "Computes 7 recursive subproducts instead of 8, lowering the asymptotic exponent from 3.0 to ~2.8074 via block matrix algebra."
                        }
                    }
                ]
            },
            "dc_defective_chessboard": {
                "question": "What is the grid dimension and defect configuration?",
                "options": [
                    {
                        "label": "2^k x 2^k board with 1 defective cell",
                        "leaf": {
                            "algorithm_slug": "defective-chessboard",
                            "name": "Defective Chessboard Tiling",
                            "complexity": "O(n^2)",
                            "space": "O(n^2)",
                            "reasoning": "Places an L-tromino at the center intersection to reduce the problem to 4 identical sub-boards of size 2^(k-1) x 2^(k-1)."
                        }
                    }
                ]
            },

            # =========================================================================
            # 2. BACKTRACKING
            # =========================================================================
            "backtracking_problem_type": {
                "question": "Which combinatorial constraint satisfaction problem are you solving?",
                "options": [
                    {"label": "N-Queens Non-Attacking Placement", "next_node": "bt_nqueens"},
                    {"label": "Sum of Subsets (Target Sum Finding)", "next_node": "bt_subset_sum"},
                    {"label": "Hamiltonian Cycle (Visiting Every Vertex Exactly Once)", "next_node": "bt_hamiltonian"},
                ]
            },
            "bt_nqueens": {
                "question": "What is the board dimension N?",
                "options": [
                    {
                        "label": "Placing N queens on N x N board without conflict",
                        "leaf": {
                            "algorithm_slug": "n-queens-backtracking",
                            "name": "N-Queens (Backtracking)",
                            "complexity": "O(N!)",
                            "space": "O(N)",
                            "reasoning": "Systematically places queens column by column, pruning rows and diagonals via explicit bounding functions."
                        }
                    }
                ]
            },
            "bt_subset_sum": {
                "question": "What is the subset search condition?",
                "options": [
                    {
                        "label": "Finding subsets whose element sum equals target W",
                        "leaf": {
                            "algorithm_slug": "subset-sum-backtracking",
                            "name": "Sum of Subsets (Backtracking)",
                            "complexity": "O(2^n)",
                            "space": "O(n)",
                            "reasoning": "Explores binary inclusion/exclusion state-space tree, pruning subtrees where current_sum + remaining < W or current_sum > W."
                        }
                    }
                ]
            },
            "bt_hamiltonian": {
                "question": "What graph cycle property is required?",
                "options": [
                    {
                        "label": "Closed tour visiting each vertex exactly once",
                        "leaf": {
                            "algorithm_slug": "hamiltonian-cycle-backtracking",
                            "name": "Hamiltonian Cycle (Backtracking)",
                            "complexity": "O(V!)",
                            "space": "O(V)",
                            "reasoning": "Generates vertex sequences incrementally, verifying adjacency and distinctness at each step with immediate backtracking."
                        }
                    }
                ]
            },

            # =========================================================================
            # 3. DYNAMIC PROGRAMMING
            # =========================================================================
            "dp_problem_type": {
                "question": "Which Dynamic Programming problem structure are you solving?",
                "options": [
                    {"label": "Multistage Graph Shortest Path", "next_node": "dp_multistage"},
                    {"label": "All-Pairs Shortest Path (APSP)", "next_node": "dp_apsp"},
                    {"label": "Optimal Binary Search Tree (OBST)", "next_node": "dp_obst"},
                    {"label": "0/1 Knapsack (Discrete Item Selection)", "next_node": "dp_01_knapsack"},
                    {"label": "Traveling Salesperson Problem (TSP Held-Karp)", "next_node": "dp_tsp"},
                    {"label": "Reliability Design (System Redundancy)", "next_node": "dp_reliability"},
                ]
            },
            "dp_multistage": {
                "question": "Is the graph structured into ordered stages V_1, V_2, ..., V_k?",
                "options": [
                    {
                        "label": "Directed k-stage acyclic graph",
                        "leaf": {
                            "algorithm_slug": "multistage-graph-dp",
                            "name": "Multistage Graph (Dynamic Programming)",
                            "complexity": "O(V + E)",
                            "space": "O(V)",
                            "reasoning": "Backward / forward recurrence COST(i, j) = min { c(j, l) + COST(i+1, l) } exploiting stage topology."
                        }
                    }
                ]
            },
            "dp_apsp": {
                "question": "What is the shortest path scope across vertices?",
                "options": [
                    {
                        "label": "All-Pairs Shortest Paths via intermediate vertex relaxation",
                        "leaf": {
                            "algorithm_slug": "floyd-warshall-apsp",
                            "name": "Floyd-Warshall APSP Algorithm",
                            "complexity": "O(V^3)",
                            "space": "O(V^2)",
                            "reasoning": "Computes A^k(i, j) = min(A^(k-1)(i, j), A^(k-1)(i, k) + A^(k-1)(k, j)) across all intermediate nodes."
                        }
                    }
                ]
            },
            "dp_obst": {
                "question": "What search tree optimization is required?",
                "options": [
                    {
                        "label": "Minimizing Expected Search Cost for known access frequencies",
                        "leaf": {
                            "algorithm_slug": "optimal-bst-dp",
                            "name": "Optimal Binary Search Tree (OBST)",
                            "complexity": "O(n^3)",
                            "space": "O(n^2)",
                            "reasoning": "DP tabulation over subtrees [i..j] choosing root r that minimizes total expected search cost."
                        }
                    }
                ]
            },
            "dp_01_knapsack": {
                "question": "Are item selections discrete 0/1 choices with integer capacity W?",
                "options": [
                    {
                        "label": "Discrete 0/1 items with pseudo-polynomial capacity W",
                        "leaf": {
                            "algorithm_slug": "0-1-knapsack-dp",
                            "name": "0/1 Knapsack (Dynamic Programming)",
                            "complexity": "O(n * W)",
                            "space": "O(n * W)",
                            "reasoning": "Tabulates DP[i][w] = max(DP[i-1][w], DP[i-1][w-w_i] + v_i) exploiting optimal substructure."
                        }
                    }
                ]
            },
            "dp_tsp": {
                "question": "What exact tour calculation is required for N <= 20 cities?",
                "options": [
                    {
                        "label": "Exact minimum TSP Hamiltonian tour using DP bitmask tabulation",
                        "leaf": {
                            "algorithm_slug": "traveling-salesman-dp",
                            "name": "Traveling Salesperson Problem (Held-Karp DP)",
                            "complexity": "O(n^2 * 2^n)",
                            "space": "O(n * 2^n)",
                            "reasoning": "Held-Karp dynamic programming formulation computing g(i, S) = min_{j in S} { c_ij + g(j, S - {j}) }."
                        }
                    }
                ]
            },
            "dp_reliability": {
                "question": "What system constraint is being optimized?",
                "options": [
                    {
                        "label": "Maximizing total system reliability under fixed cost budget",
                        "leaf": {
                            "algorithm_slug": "reliability-design-dp",
                            "name": "Reliability Design (Dynamic Programming)",
                            "complexity": "O(n * C^2)",
                            "space": "O(n * C)",
                            "reasoning": "Determines optimal parallel copy counts m_i per stage to maximize product of stage reliabilities within budget C."
                        }
                    }
                ]
            },

            # =========================================================================
            # 4. GREEDY METHODS
            # =========================================================================
            "greedy_problem_type": {
                "question": "Which greedy optimization domain are you addressing?",
                "options": [
                    {"label": "Fractional Knapsack / Continuous Resource Allocation", "next_node": "greedy_knapsack_type"},
                    {"label": "Job Sequencing with Deadlines", "next_node": "greedy_job_sequencing"},
                    {"label": "Optimal Storage on Tapes (MRT Minimization)", "next_node": "greedy_storage_tapes"},
                    {"label": "Optimal 2-Way Merge Patterns", "next_node": "greedy_merge_patterns"},
                    {"label": "Minimum Spanning Tree (MST)", "next_node": "greedy_mst_type"},
                    {"label": "Single-Source Shortest Path (Non-negative)", "next_node": "greedy_sssp_type"},
                ]
            },
            "greedy_knapsack_type": {
                "question": "Are items fractionally divisible?",
                "options": [
                    {
                        "label": "Items can be fractionally divided (Continuous knapsack)",
                        "leaf": {
                            "algorithm_slug": "fractional-knapsack",
                            "name": "Fractional Knapsack (Greedy)",
                            "complexity": "O(n log n)",
                            "space": "O(1)",
                            "reasoning": "Sorts items by value-to-weight ratio (v_i / w_i) in descending order to greedily maximize total profit."
                        }
                    }
                ]
            },
            "greedy_job_sequencing": {
                "question": "What is the job scheduling constraint?",
                "options": [
                    {
                        "label": "Unit-duration jobs with deadlines and profits",
                        "leaf": {
                            "algorithm_slug": "job-sequencing-deadlines",
                            "name": "Job Sequencing with Deadlines",
                            "complexity": "O(n log n + n * d_max)",
                            "space": "O(d_max)",
                            "reasoning": "Greedily schedules highest-profit jobs at their latest possible feasible time slot."
                        }
                    }
                ]
            },
            "greedy_storage_tapes": {
                "question": "What is the tape storage objective?",
                "options": [
                    {
                        "label": "Minimizing Mean Retrieval Time (MRT) across programs",
                        "leaf": {
                            "algorithm_slug": "optimal-storage-tapes-greedy",
                            "name": "Optimal Storage on Tapes",
                            "complexity": "O(n log n)",
                            "space": "O(n)",
                            "reasoning": "Orders programs in non-decreasing order of length so shorter programs reduce subsequent retrieval latency."
                        }
                    }
                ]
            },
            "greedy_merge_patterns": {
                "question": "What is the file merge tree configuration?",
                "options": [
                    {
                        "label": "Optimal 2-way merge tree minimizing total record movements",
                        "leaf": {
                            "algorithm_slug": "optimal-merge-patterns-greedy",
                            "name": "Optimal Merge Patterns (Greedy / Min-Heap)",
                            "complexity": "O(n log n)",
                            "space": "O(n)",
                            "reasoning": "Repeatedly combines the two smallest file sizes using a min-priority queue to minimize weighted external path length."
                        }
                    }
                ]
            },
            "greedy_mst_type": {
                "question": "What is the graph edge density?",
                "options": [
                    {
                        "label": "Sparse Graph (E << V^2) - Edge-centric sorting (Kruskal)",
                        "leaf": {
                            "algorithm_slug": "kruskal-mst",
                            "name": "Kruskal's MST Algorithm",
                            "complexity": "O(E log E)",
                            "space": "O(V + E)",
                            "reasoning": "Sorts edges globally and applies Disjoint Set Union (Union-Find) with path compression to prevent cycles."
                        }
                    },
                    {
                        "label": "Dense Graph (E ~ V^2) - Vertex-centric relaxation (Prim)",
                        "leaf": {
                            "algorithm_slug": "prim-mst",
                            "name": "Prim's MST Algorithm",
                            "complexity": "O((V + E) log V)",
                            "space": "O(V)",
                            "reasoning": "Grows a single MST cut monotonically from a start vertex using priority queue cut relaxation."
                        }
                    }
                ]
            },
            "greedy_sssp_type": {
                "question": "Are all edge weights strictly non-negative?",
                "options": [
                    {
                        "label": "Yes, all edge weights are non-negative (>= 0)",
                        "leaf": {
                            "algorithm_slug": "dijkstra-sssp",
                            "name": "Dijkstra's SSSP Algorithm",
                            "complexity": "O((V + E) log V)",
                            "space": "O(V)",
                            "reasoning": "Greedily extracts the minimum tentative distance vertex from a priority queue."
                        }
                    }
                ]
            },

            # =========================================================================
            # 5. BRANCH AND BOUND
            # =========================================================================
            "bb_problem_type": {
                "question": "Which Branch & Bound optimization problem are you exploring?",
                "options": [
                    {"label": "0/1 Knapsack Branch & Bound Search Strategies", "next_node": "bb_knapsack_strategy"},
                    {"label": "Traveling Salesperson Problem (TSP) with Reduced Cost Matrices", "next_node": "bb_tsp"},
                ]
            },
            "bb_knapsack_strategy": {
                "question": "Which live node selection strategy do you prefer?",
                "options": [
                    {
                        "label": "Least-Cost (LC) Branch & Bound using upper bounding heuristic",
                        "leaf": {
                            "algorithm_slug": "0-1-knapsack-lc-bb",
                            "name": "0/1 Knapsack (LC Branch & Bound)",
                            "complexity": "O(2^n) worst / pruned in practice",
                            "space": "O(2^n)",
                            "reasoning": "Maintains a max-heap priority queue of live state nodes ordered by upper bound (fractional knapsack estimate) to prune unpromising subtrees."
                        }
                    },
                    {
                        "label": "FIFO Branch & Bound (Breadth-First Queue exploration)",
                        "leaf": {
                            "algorithm_slug": "0-1-knapsack-fifo-bb",
                            "name": "0/1 Knapsack (FIFO Branch & Bound)",
                            "complexity": "O(2^n) worst",
                            "space": "O(2^n)",
                            "reasoning": "Explores live state nodes in standard breadth-first order using a FIFO queue with fractional upper bound pruning."
                        }
                    }
                ]
            },
            "bb_tsp": {
                "question": "What bounding technique is applied for the TSP tour?",
                "options": [
                    {
                        "label": "Reduced Cost Matrix Lower Bounding with LC Search",
                        "leaf": {
                            "algorithm_slug": "traveling-salesman-bb",
                            "name": "Traveling Salesperson Problem (LC Branch & Bound)",
                            "complexity": "O(n^2 * 2^n)",
                            "space": "O(n^2 * 2^n)",
                            "reasoning": "Uses matrix row and column reduction to establish rigorous lower bounds, expanding lowest-cost tours first."
                        }
                    }
                ]
            },

            # =========================================================================
            # 6. SHORTEST PATH IN GRAPH
            # =========================================================================
            "shortest_path_type": {
                "question": "What is the query scope and edge weight nature?",
                "options": [
                    {"label": "Single-Source Shortest Path (SSSP)", "next_node": "sssp_weights"},
                    {
                        "label": "All-Pairs Shortest Path (APSP)",
                        "leaf": {
                            "algorithm_slug": "floyd-warshall-apsp",
                            "name": "Floyd-Warshall Algorithm",
                            "complexity": "O(V^3)",
                            "space": "O(V^2)",
                            "reasoning": "Dynamic programming matrix relaxation computing shortest paths between all pairs of vertices."
                        }
                    }
                ]
            },
            "sssp_weights": {
                "question": "Do edges contain negative weights?",
                "options": [
                    {
                        "label": "No negative weights (Non-negative) - Dijkstra",
                        "leaf": {
                            "algorithm_slug": "dijkstra-sssp",
                            "name": "Dijkstra's SSSP Algorithm",
                            "complexity": "O((V + E) log V)",
                            "space": "O(V)",
                            "reasoning": "Greedy priority queue expansion yields optimal single-source shortest paths on non-negative graphs."
                        }
                    },
                    {
                        "label": "Negative edge weights exist (Potential negative cycles) - Bellman-Ford",
                        "leaf": {
                            "algorithm_slug": "bellman-ford-sssp",
                            "name": "Bellman-Ford SSSP Algorithm",
                            "complexity": "O(V * E)",
                            "space": "O(V)",
                            "reasoning": "Relaxes all edges V-1 times to correctly handle negative weights and detect negative cycles."
                        }
                    }
                ]
            },

            # =========================================================================
            # 7. KNAPSACK DIVISIBILITY
            # =========================================================================
            "knapsack_divisibility": {
                "question": "Can item quantities be fractionally divided, or must items be taken discretely (0/1)?",
                "options": [
                    {
                        "label": "Items can be taken fractionally (Divisible) - Greedy",
                        "leaf": {
                            "algorithm_slug": "fractional-knapsack",
                            "name": "Fractional Knapsack (Greedy)",
                            "complexity": "O(n log n)",
                            "space": "O(1)",
                            "reasoning": "Greedy choice by value-to-weight ratio yields provably optimal solution."
                        }
                    },
                    {"label": "Discrete 0/1 choice per item", "next_node": "knapsack_discrete_paradigm"}
                ]
            },
            "knapsack_discrete_paradigm": {
                "question": "Which algorithmic paradigm do you want to apply for 0/1 Knapsack?",
                "options": [
                    {
                        "label": "Dynamic Programming Tabulation",
                        "leaf": {
                            "algorithm_slug": "0-1-knapsack-dp",
                            "name": "0/1 Knapsack (Dynamic Programming)",
                            "complexity": "O(n * W)",
                            "space": "O(n * W)",
                            "reasoning": "Pseudo-polynomial 2D DP tabulation considering optimal sub-structure."
                        }
                    },
                    {
                        "label": "Least-Cost (LC) Branch and Bound",
                        "leaf": {
                            "algorithm_slug": "0-1-knapsack-lc-bb",
                            "name": "0/1 Knapsack (LC Branch & Bound)",
                            "complexity": "O(2^n) worst",
                            "space": "O(2^n)",
                            "reasoning": "Max-priority queue search with fractional knapsack upper bound pruning."
                        }
                    },
                    {
                        "label": "FIFO Breadth-First Branch and Bound",
                        "leaf": {
                            "algorithm_slug": "0-1-knapsack-fifo-bb",
                            "name": "0/1 Knapsack (FIFO Branch & Bound)",
                            "complexity": "O(2^n) worst",
                            "space": "O(2^n)",
                            "reasoning": "Queue-based breadth-first state expansion with bound pruning."
                        }
                    }
                ]
            },

            # =========================================================================
            # 8. TRAVELING SALESMAN APPROACH
            # =========================================================================
            "tsp_approach": {
                "question": "Which algorithmic paradigm do you want to apply for the Traveling Salesman Problem?",
                "options": [
                    {
                        "label": "Held-Karp Dynamic Programming (Bitmask Subsets)",
                        "leaf": {
                            "algorithm_slug": "traveling-salesman-dp",
                            "name": "Traveling Salesperson Problem (Held-Karp DP)",
                            "complexity": "O(n^2 * 2^n)",
                            "space": "O(n * 2^n)",
                            "reasoning": "Sub-exponential dynamic programming formulation computing optimal paths over subset bitmasks."
                        }
                    },
                    {
                        "label": "Least-Cost (LC) Branch and Bound (Reduced Cost Matrix)",
                        "leaf": {
                            "algorithm_slug": "traveling-salesman-bb",
                            "name": "Traveling Salesperson Problem (LC Branch & Bound)",
                            "complexity": "O(n^2 * 2^n)",
                            "space": "O(n^2 * 2^n)",
                            "reasoning": "Priority queue best-first search utilizing matrix reduction to compute admissible lower bounds."
                        }
                    }
                ]
            }
        }
    }

    @classmethod
    def get_tree(cls) -> Dict[str, Any]:
        """Returns the full decision tree structure."""
        return cls.TREE_DATA

    @classmethod
    def traverse(cls, answers: Dict[str, str]) -> Dict[str, Any]:
        """
        Traverses tree given user answers: {'root': 'Divide and Conquer Problems', ...}
        """
        current_id = "root"
        path = []

        while True:
            node_data = cls.TREE_DATA["nodes"].get(current_id) if current_id != "root" else cls.TREE_DATA
            if not node_data:
                break

            question = node_data.get("question")
            options = node_data.get("options", [])

            # Check if user provided an answer for this node
            user_choice = answers.get(current_id)
            if not user_choice:
                # Need user input for this question
                return {
                    "status": "in_progress",
                    "current_node_id": current_id,
                    "question": question,
                    "options": [opt["label"] for opt in options],
                    "path_traversed": path
                }

            # Find matching option (case-insensitive with partial prefix/containment fallback)
            matched_option = next((opt for opt in options if opt["label"].strip().lower() == user_choice.strip().lower()), None)
            if not matched_option:
                matched_option = next((opt for opt in options if user_choice.strip().lower() in opt["label"].strip().lower() or opt["label"].strip().lower() in user_choice.strip().lower()), None)
            if not matched_option:
                return {
                    "status": "error",
                    "error": f"Invalid option '{user_choice}' for node '{current_id}'.",
                    "options": [opt["label"] for opt in options]
                }

            path.append({
                "node_id": current_id,
                "question": question,
                "selected": user_choice
            })

            # Check if option leads to leaf
            if "leaf" in matched_option:
                return {
                    "status": "completed",
                    "path_traversed": path,
                    "recommendation": matched_option["leaf"]
                }

            current_id = matched_option.get("next_node")
            if not current_id:
                break

        return {"status": "error", "error": "Decision path terminated without resolution."}

