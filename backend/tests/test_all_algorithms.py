"""
Automated Comprehensive Test Suite for the 23 Canonical DAA Curriculum Algorithms.
Validates correctness, edge cases, boundaries, and instrumented execution across 5 computational paradigms.
"""
import pytest
from app.algorithms.registry import registry
from app.algorithms.base import AlgorithmExecutionResult


class TestDivideAndConquerAlgorithms:
    """Test suite for Divide and Conquer algorithms (3 implementations)."""

    def test_defective_chessboard(self):
        algo = registry.get("defective-chessboard")
        assert algo is not None
        res = algo.run({"size": 4, "defect": [0, 0]})
        assert "grid" in res
        assert len(res["grid"]) == 4
        assert len(res["grid"][0]) == 4
        assert res["grid"][0][0] == -1  # Defect marker

        inst = algo.run_instrumented({"size": 4, "defect": [0, 0]})
        assert isinstance(inst, AlgorithmExecutionResult)
        assert len(inst.steps) > 0

    def test_max_min(self):
        algo = registry.get("max-min-divide-conquer")
        assert algo is not None
        arr = [22, 13, -5, 88, 41, 7, 95, 3]
        res = algo.run(arr)
        assert res["min"] == -5
        assert res["max"] == 95
        assert res["comparisons"] <= 3 * len(arr) // 2

        # Edge cases
        single = algo.run([42])
        assert single["min"] == 42 and single["max"] == 42

        pair = algo.run([10, 5])
        assert pair["min"] == 5 and pair["max"] == 10

        inst = algo.run_instrumented(arr)
        assert isinstance(inst, AlgorithmExecutionResult)

    def test_strassen_matrix(self):
        algo = registry.get("strassen-matrix-multiplication")
        assert algo is not None
        A = [[1, 2], [3, 4]]
        B = [[5, 6], [7, 8]]
        res = algo.run({"matrix_a": A, "matrix_b": B})
        assert res["result_matrix"] == [[19, 22], [43, 50]]

        inst = algo.run_instrumented({"matrix_a": A, "matrix_b": B})
        assert isinstance(inst, AlgorithmExecutionResult)


class TestBacktrackingAlgorithms:
    """Test suite for Backtracking algorithms (3 implementations)."""

    def test_n_queens(self):
        algo = registry.get("n-queens-backtracking")
        assert algo is not None
        res_4 = algo.run({"n": 4})
        assert res_4["total_solutions"] == 2
        assert len(res_4["solutions"]) == 2

        res_1 = algo.run({"n": 1})
        assert res_1["total_solutions"] == 1

        inst = algo.run_instrumented({"n": 4})
        assert isinstance(inst, AlgorithmExecutionResult)

    def test_subset_sum(self):
        algo = registry.get("subset-sum-backtracking")
        assert algo is not None
        res = algo.run({"numbers": [10, 7, 5, 18, 12, 20, 15], "target_sum": 35})
        assert res["solution_count"] > 0
        for sol in res["solutions"]:
            assert sum(sol) == 35

        inst = algo.run_instrumented({"numbers": [3, 4, 5, 2], "target_sum": 9})
        assert isinstance(inst, AlgorithmExecutionResult)

    def test_hamiltonian_cycle(self):
        algo = registry.get("hamiltonian-cycle-backtracking")
        assert algo is not None
        c4 = {
            "vertices": ["A", "B", "C", "D"],
            "edges": [
                {"source": "A", "target": "B"},
                {"source": "B", "target": "C"},
                {"source": "C", "target": "D"},
                {"source": "D", "target": "A"},
            ]
        }
        res = algo.run(c4)
        assert res["cycle_found"] is True
        assert len(res["cycle"]) == 5

        inst = algo.run_instrumented(c4)
        assert isinstance(inst, AlgorithmExecutionResult)


class TestDynamicProgrammingAlgorithms:
    """Test suite for Dynamic Programming algorithms (6 implementations)."""

    def test_multistage_graph(self):
        algo = registry.get("multistage-graph-dp")
        assert algo is not None
        graph_input = {
            "num_vertices": 8,
            "stages": 4,
            "edges": [
                {"from": 1, "to": 2, "weight": 2}, {"from": 1, "to": 3, "weight": 1}, {"from": 1, "to": 4, "weight": 3},
                {"from": 2, "to": 5, "weight": 2}, {"from": 2, "to": 6, "weight": 3}, {"from": 3, "to": 5, "weight": 6},
                {"from": 3, "to": 6, "weight": 7}, {"from": 4, "to": 6, "weight": 6}, {"from": 4, "to": 7, "weight": 8},
                {"from": 5, "to": 8, "weight": 1}, {"from": 6, "to": 8, "weight": 4}, {"from": 7, "to": 8, "weight": 2}
            ]
        }
        res = algo.run(graph_input)
        assert res["min_cost"] == 5.0
        assert res["path"] == [1, 2, 5, 8]

    def test_floyd_warshall(self):
        algo = registry.get("floyd-warshall-apsp")
        assert algo is not None
        graph = {
            "vertices": ["A", "B", "C", "D"],
            "edges": [
                {"source": "A", "target": "B", "weight": 3},
                {"source": "A", "target": "D", "weight": 7},
                {"source": "B", "target": "A", "weight": 8},
                {"source": "B", "target": "C", "weight": 2},
                {"source": "C", "target": "A", "weight": 5},
                {"source": "C", "target": "D", "weight": 1},
                {"source": "D", "target": "A", "weight": 2},
            ]
        }
        res = algo.run(graph)
        assert "distance_matrix" in res
        matrix = res["distance_matrix"]
        assert matrix["A"]["A"] == 0
        assert matrix["A"]["C"] == 5

    def test_optimal_bst(self):
        algo = registry.get("optimal-bst-dp")
        assert algo is not None
        obst_input = {
            "keys": ["k1", "k2", "k3", "k4"],
            "p": [0.1, 0.2, 0.4, 0.3],
            "q": [0.05, 0.1, 0.05, 0.05, 0.05]
        }
        res = algo.run(obst_input)
        assert "min_cost" in res
        assert res["min_cost"] > 0

    def test_knapsack_01_dp(self):
        algo = registry.get("0-1-knapsack-dp")
        assert algo is not None
        items = [
            {"name": "I1", "weight": 2, "value": 12},
            {"name": "I2", "weight": 1, "value": 10},
            {"name": "I3", "weight": 3, "value": 20},
            {"name": "I4", "weight": 2, "value": 15},
        ]
        res = algo.run({"items": items, "capacity": 5})
        assert res["max_value"] == 37

    def test_traveling_salesman_dp(self):
        algo = registry.get("traveling-salesman-dp")
        assert algo is not None
        tsp_input = {
            "distance_matrix": [
                [0, 10, 15, 20],
                [10, 0, 35, 25],
                [15, 35, 0, 30],
                [20, 25, 30, 0]
            ],
            "cities": ["A", "B", "C", "D"]
        }
        res = algo.run(tsp_input)
        assert res["min_cost"] == 80
        assert len(res["tour"]) == 5

    def test_reliability_design_dp(self):
        algo = registry.get("reliability-design-dp")
        assert algo is not None
        rel_input = {
            "reliabilities": [0.9, 0.8, 0.5],
            "costs": [30, 15, 20],
            "budget": 105
        }
        res = algo.run(rel_input)
        assert "max_reliability" in res
        assert res["max_reliability"] >= 0.6


class TestGreedyAlgorithms:
    """Test suite for Greedy Method algorithms (8 implementations)."""

    def test_optimal_storage_tapes(self):
        algo = registry.get("optimal-storage-tapes-greedy")
        assert algo is not None
        res = algo.run({"lengths": [5, 10, 3, 20, 12, 7], "tapes": 1})
        assert "optimal_order" in res
        assert res["sorted_lengths"] == [3, 5, 7, 10, 12, 20]

    def test_fractional_knapsack(self):
        algo = registry.get("fractional-knapsack")
        assert algo is not None
        items = [
            {"name": "Item1", "weight": 10, "value": 60},
            {"name": "Item2", "weight": 20, "value": 100},
            {"name": "Item3", "weight": 30, "value": 120},
        ]
        res = algo.run({"items": items, "capacity": 50})
        assert res["total_value"] == 240.0

    def test_job_sequencing(self):
        algo = registry.get("job-sequencing-deadlines")
        assert algo is not None
        jobs = [
            {"id": "J1", "deadline": 2, "profit": 100},
            {"id": "J2", "deadline": 1, "profit": 19},
            {"id": "J3", "deadline": 2, "profit": 27},
            {"id": "J4", "deadline": 1, "profit": 25},
            {"id": "J5", "deadline": 3, "profit": 15},
        ]
        res = algo.run({"jobs": jobs})
        assert res["total_profit"] == 142

    def test_optimal_merge_patterns(self):
        algo = registry.get("optimal-merge-patterns-greedy")
        assert algo is not None
        res = algo.run({"files": [20, 30, 10, 5, 30]})
        assert res["total_merge_cost"] == 205

    def test_kruskal_mst(self):
        algo = registry.get("kruskal-mst")
        assert algo is not None
        graph = {
            "vertices": ["A", "B", "C", "D"],
            "edges": [
                {"source": "A", "target": "B", "weight": 1},
                {"source": "B", "target": "C", "weight": 4},
                {"source": "A", "target": "C", "weight": 3},
                {"source": "C", "target": "D", "weight": 2},
                {"source": "B", "target": "D", "weight": 5},
            ]
        }
        res = algo.run(graph)
        assert res["mst_weight"] == 6

    def test_prim_mst(self):
        algo = registry.get("prim-mst")
        assert algo is not None
        graph = {
            "vertices": ["A", "B", "C", "D"],
            "edges": [
                {"source": "A", "target": "B", "weight": 1},
                {"source": "B", "target": "C", "weight": 4},
                {"source": "A", "target": "C", "weight": 3},
                {"source": "C", "target": "D", "weight": 2},
                {"source": "B", "target": "D", "weight": 5},
            ]
        }
        res = algo.run(graph)
        assert res["mst_weight"] == 6

    def test_dijkstra_sssp(self):
        algo = registry.get("dijkstra-sssp")
        assert algo is not None
        graph = {
            "vertices": ["A", "B", "C", "D"],
            "edges": [
                {"source": "A", "target": "B", "weight": 4},
                {"source": "A", "target": "C", "weight": 2},
                {"source": "C", "target": "B", "weight": 1},
                {"source": "B", "target": "D", "weight": 5},
                {"source": "C", "target": "D", "weight": 8},
            ],
            "source": "A"
        }
        res = algo.run(graph)
        assert res["distances"]["A"] == 0
        assert res["distances"]["C"] == 2
        assert res["distances"]["B"] == 3
        assert res["distances"]["D"] == 8

    def test_bellman_ford_sssp(self):
        algo = registry.get("bellman-ford-sssp")
        assert algo is not None
        graph = {
            "vertices": ["A", "B", "C", "D"],
            "edges": [
                {"source": "A", "target": "B", "weight": 4},
                {"source": "A", "target": "C", "weight": 5},
                {"source": "B", "target": "C", "weight": -2},
                {"source": "C", "target": "D", "weight": 3},
            ],
            "source": "A"
        }
        res = algo.run(graph)
        assert res["has_negative_cycle"] is False
        assert res["distances"]["A"] == 0
        assert res["distances"]["B"] == 4
        assert res["distances"]["C"] == 2
        assert res["distances"]["D"] == 5


class TestBranchAndBoundAlgorithms:
    """Test suite for Branch and Bound algorithms (3 implementations)."""

    def test_knapsack_lc_bb(self):
        algo = registry.get("0-1-knapsack-lc-bb")
        assert algo is not None
        items = [
            {"name": "I1", "weight": 2, "value": 12},
            {"name": "I2", "weight": 1, "value": 10},
            {"name": "I3", "weight": 3, "value": 20},
            {"name": "I4", "weight": 2, "value": 15},
        ]
        res = algo.run({"items": items, "capacity": 5})
        assert res["max_value"] == 37

    def test_knapsack_fifo_bb(self):
        algo = registry.get("0-1-knapsack-fifo-bb")
        assert algo is not None
        items = [
            {"name": "I1", "weight": 2, "value": 12},
            {"name": "I2", "weight": 1, "value": 10},
            {"name": "I3", "weight": 3, "value": 20},
            {"name": "I4", "weight": 2, "value": 15},
        ]
        res = algo.run({"items": items, "capacity": 5})
        assert res["max_value"] == 37

    def test_traveling_salesman_bb(self):
        algo = registry.get("traveling-salesman-bb")
        assert algo is not None
        tsp_input = {
            "distance_matrix": [
                [0, 10, 15, 20],
                [10, 0, 35, 25],
                [15, 35, 0, 30],
                [20, 25, 30, 0]
            ],
            "cities": ["A", "B", "C", "D"]
        }
        res = algo.run(tsp_input)
        assert res["min_cost"] == 80
        assert len(res["tour"]) == 5


class TestCurriculumRegistryIntegrity:
    """Test suite validating exact 23 curriculum algorithms and API endpoint filtering."""

    def test_exact_23_curriculum_algorithms(self):
        """Validates that exactly 23 executable curriculum algorithms are registered."""
        all_algos = registry.list_all()
        assert len(all_algos) == 23

    def test_paradigm_filter_api_endpoints(self):
        """Validates that API correctly filters across the 5 computational paradigms."""
        from fastapi.testclient import TestClient
        from app.main import app

        client = TestClient(app)

        # 1. Test All (no query param)
        res_all = client.get("/api/v1/algorithms")
        assert res_all.status_code == 200
        data_all = res_all.json()
        assert len(data_all) == 23

        # 2. Test Divide & Conquer (3 algorithms)
        res_dc = client.get("/api/v1/algorithms?paradigm=Divide%20and%20Conquer")
        assert res_dc.status_code == 200
        assert len(res_dc.json()) == 3

        # 3. Test Backtracking (3 algorithms)
        res_bt = client.get("/api/v1/algorithms?paradigm=Backtracking")
        assert res_bt.status_code == 200
        assert len(res_bt.json()) == 3

        # 4. Test Dynamic Programming (6 algorithms)
        res_dp = client.get("/api/v1/algorithms?paradigm=Dynamic%20Programming")
        assert res_dp.status_code == 200
        assert len(res_dp.json()) == 6

        # 5. Test Greedy Method (8 algorithms)
        res_greedy = client.get("/api/v1/algorithms?paradigm=Greedy%20Method")
        assert res_greedy.status_code == 200
        assert len(res_greedy.json()) == 8

        # 6. Test Branch & Bound (3 algorithms)
        res_bb = client.get("/api/v1/algorithms?paradigm=Branch%20and%20Bound")
        assert res_bb.status_code == 200
        assert len(res_bb.json()) == 3
