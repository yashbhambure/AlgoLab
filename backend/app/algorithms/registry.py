"""
Central Algorithm Registry
Maps all algorithm slugs to their active implementation instances.
Includes strictly the 23 Authoritative DAA Curriculum algorithms and their aliases.
"""
from typing import Dict, List, Optional, Type
from app.algorithms.base import BaseAlgorithm

# Module 1: Divide and Conquer
from app.algorithms.divide_and_conquer.defective_chessboard import DefectiveChessboard
from app.algorithms.divide_and_conquer.max_min import MaxMinDivideConquer
from app.algorithms.divide_and_conquer.strassen_matrix import StrassenMatrixMultiplication

# Module 2: Backtracking
from app.algorithms.backtracking.n_queens import NQueens
from app.algorithms.backtracking.subset_sum import SubsetSum
from app.algorithms.backtracking.hamiltonian_cycle import HamiltonianCycle

# Module 3: Dynamic Programming
from app.algorithms.dynamic_programming.multistage_graph import MultistageGraphDP
from app.algorithms.graph.floyd_warshall import FloydWarshall
from app.algorithms.dynamic_programming.optimal_bst import OptimalBST
from app.algorithms.dynamic_programming.knapsack_01 import Knapsack01
from app.algorithms.dynamic_programming.tsp_dp import TravelingSalesmanDP
from app.algorithms.dynamic_programming.reliability_design import ReliabilityDesignDP

# Module 4: Greedy Method
from app.algorithms.greedy.optimal_storage_tapes import OptimalStorageOnTapes
from app.algorithms.greedy.fractional_knapsack import FractionalKnapsack
from app.algorithms.greedy.job_sequencing import JobSequencing
from app.algorithms.greedy.optimal_merge_patterns import OptimalMergePatterns
from app.algorithms.greedy.kruskal_mst import KruskalMST
from app.algorithms.greedy.prim_mst import PrimMST
from app.algorithms.greedy.dijkstra_greedy import DijkstraGreedy
from app.algorithms.graph.bellman_ford import BellmanFord

# Module 5: Branch and Bound
from app.algorithms.branch_and_bound.knapsack_lc_bb import KnapsackLCBranchAndBound
from app.algorithms.branch_and_bound.knapsack_fifo_bb import KnapsackFIFOBRanchAndBound
from app.algorithms.branch_and_bound.tsp_bb import TravelingSalesmanBranchAndBound


class AlgorithmRegistry:
    """Singleton registry for querying and executing the 23 Authoritative DAA algorithms."""

    def __init__(self):
        self._algorithms: Dict[str, BaseAlgorithm] = {}
        self._aliases: Dict[str, str] = {}
        self._register_all()

    def _register_all(self):
        classes: List[Type[BaseAlgorithm]] = [
            # Module 1: Divide and Conquer (3)
            DefectiveChessboard,
            MaxMinDivideConquer,
            StrassenMatrixMultiplication,

            # Module 2: Backtracking (3)
            NQueens,
            SubsetSum,
            HamiltonianCycle,

            # Module 3: Dynamic Programming (6)
            MultistageGraphDP,
            FloydWarshall,
            OptimalBST,
            Knapsack01,
            TravelingSalesmanDP,
            ReliabilityDesignDP,

            # Module 4: Greedy Method (7 across 5 problem areas)
            OptimalStorageOnTapes,
            FractionalKnapsack,
            JobSequencing,
            OptimalMergePatterns,
            KruskalMST,
            PrimMST,
            DijkstraGreedy,
            BellmanFord,

            # Module 5: Branch and Bound (3)
            KnapsackLCBranchAndBound,
            KnapsackFIFOBRanchAndBound,
            TravelingSalesmanBranchAndBound,
        ]

        for cls in classes:
            instance = cls()
            self._algorithms[instance.slug] = instance

        # Canonical Slug aliases
        self._aliases = {
            # Module 1: Divide and Conquer
            "defective-chessboard-dc": "defective-chessboard",
            "tromino-tiling": "defective-chessboard",
            "max-min": "max-min-divide-conquer",
            "max-min-dc": "max-min-divide-conquer",
            "finding-max-min": "max-min-divide-conquer",
            "strassen-matrix": "strassen-matrix-multiplication",
            "strassen": "strassen-matrix-multiplication",

            # Module 2: Backtracking
            "n-queens": "n-queens-backtracking",
            "subset-sum": "subset-sum-backtracking",
            "sum-of-subsets": "subset-sum-backtracking",
            "hamiltonian-cycle": "hamiltonian-cycle-backtracking",
            "hamiltonian-cycles": "hamiltonian-cycle-backtracking",

            # Module 3: Dynamic Programming
            "multistage-graph": "multistage-graph-dp",
            "multistage-graphs": "multistage-graph-dp",
            "floyd-warshall": "floyd-warshall-apsp",
            "all-pairs-shortest-path": "floyd-warshall-apsp",
            "all-pairs-shortest-path-dp": "floyd-warshall-apsp",
            "optimal-bst": "optimal-bst-dp",
            "optimal-binary-search-tree": "optimal-bst-dp",
            "optimal-binary-search-trees": "optimal-bst-dp",
            "0-1-knapsack": "0-1-knapsack-dp",
            "0-1-knapsack-problem": "0-1-knapsack-dp",
            "knapsack-0-1": "0-1-knapsack-dp",
            "knapsack-01": "0-1-knapsack-dp",
            "traveling-salesman": "traveling-salesman-dp",
            "traveling-salesperson": "traveling-salesman-dp",
            "tsp": "traveling-salesman-dp",
            "tsp-dp": "traveling-salesman-dp",
            "reliability-design": "reliability-design-dp",

            # Module 4: Greedy Method
            "optimal-storage-on-tapes": "optimal-storage-tapes-greedy",
            "optimal-storage-tapes": "optimal-storage-tapes-greedy",
            "storage-on-tapes": "optimal-storage-tapes-greedy",
            "fractional-knapsack-greedy": "fractional-knapsack",
            "job-sequencing": "job-sequencing-deadlines",
            "job-sequencing-with-deadlines": "job-sequencing-deadlines",
            "optimal-merge-patterns": "optimal-merge-patterns-greedy",
            "optimal-merge": "optimal-merge-patterns-greedy",
            "kruskal": "kruskal-mst",
            "prim": "prim-mst",
            "dijkstra": "dijkstra-sssp",
            "dijkstra-greedy": "dijkstra-sssp",
            "bellman-ford": "bellman-ford-sssp",
            "single-source-shortest-path": "dijkstra-sssp",

            # Module 5: Branch and Bound
            "knapsack-lc-bb": "0-1-knapsack-lc-bb",
            "knapsack-lc-branch-and-bound": "0-1-knapsack-lc-bb",
            "0-1-knapsack-lc-branch-and-bound": "0-1-knapsack-lc-bb",
            "knapsack-fifo-bb": "0-1-knapsack-fifo-bb",
            "knapsack-fifo-branch-and-bound": "0-1-knapsack-fifo-bb",
            "0-1-knapsack-fifo-branch-and-bound": "0-1-knapsack-fifo-bb",
            "tsp-bb": "traveling-salesman-bb",
            "tsp-branch-and-bound": "traveling-salesman-bb",
            "traveling-salesman-branch-and-bound": "traveling-salesman-bb",
        }

    def get(self, slug: str) -> Optional[BaseAlgorithm]:
        """Retrieve algorithm instance by slug or alias."""
        target_slug = self._aliases.get(slug, slug)
        return self._algorithms.get(target_slug)

    def list_all(self) -> List[BaseAlgorithm]:
        """List all registered algorithms."""
        return list(self._algorithms.values())

    def list_by_category(self, category: str) -> List[BaseAlgorithm]:
        """List algorithms belonging to a specific DAA category."""
        return [algo for algo in self._algorithms.values() if algo.category.lower() == category.lower()]


# Global registry instance
registry = AlgorithmRegistry()

