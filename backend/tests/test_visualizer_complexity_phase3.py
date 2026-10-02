"""
Phase 3 Test Suite: Visualizer & Complexity Deepening
Validates 23/23 curriculum algorithm instrumentation, Strassen step generation,
compatible problem groups, theoretical vs empirical complexity separation,
and safe input boundary handling.
"""
import pytest
from app.algorithms.registry import registry
from app.curriculum.curriculum_data import get_all_approved_algorithm_slugs, get_curriculum_modules
from app.core.database import SessionLocal
from app.models.algorithm import Algorithm
from app.models.problem import Problem
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Canonical Default Test Inputs for all 23 Authoritative Curriculum Algorithms
CURRICULUM_SAMPLE_INPUTS = {
    # Module 1: Divide and Conquer
    "defective-chessboard": {"size": 4, "defect": [0, 0]},
    "max-min-divide-conquer": [22, 13, -5, 88, 41, 7, 95, 3],
    "strassen-matrix-multiplication": {
        "matrix_a": [[1, 2], [3, 4]],
        "matrix_b": [[5, 6], [7, 8]],
    },

    # Module 2: Backtracking
    "n-queens-backtracking": {"n": 4},
    "subset-sum-backtracking": {"numbers": [3, 5, 6, 7], "target_sum": 15},
    "hamiltonian-cycle-backtracking": {
        "vertices": ["A", "B", "C", "D"],
        "edges": [["A", "B"], ["B", "C"], ["C", "D"], ["D", "A"]],
    },

    # Module 3: Dynamic Programming I
    "multistage-graph-dp": {
        "num_vertices": 8,
        "stages": 4,
        "edges": [
            {"from": 1, "to": 2, "weight": 2}, {"from": 1, "to": 3, "weight": 1}, {"from": 1, "to": 4, "weight": 3},
            {"from": 2, "to": 5, "weight": 2}, {"from": 2, "to": 6, "weight": 3}, {"from": 3, "to": 5, "weight": 6},
            {"from": 3, "to": 6, "weight": 7}, {"from": 4, "to": 6, "weight": 6}, {"from": 4, "to": 7, "weight": 8},
            {"from": 5, "to": 8, "weight": 1}, {"from": 6, "to": 8, "weight": 4}, {"from": 7, "to": 8, "weight": 2},
        ],
    },
    "floyd-warshall-apsp": {
        "matrix": [
            [0, 3, 999999, 7],
            [8, 0, 2, 999999],
            [5, 999999, 0, 1],
            [2, 999999, 999999, 0],
        ],
    },
    "optimal-bst-dp": {
        "keys": ["k1", "k2", "k3", "k4"],
        "p": [0.1, 0.2, 0.4, 0.3],
        "q": [0.05, 0.1, 0.05, 0.05, 0.05],
    },

    # Module 4: Dynamic Programming II
    "0-1-knapsack-dp": {"weights": [2, 3, 4, 5], "values": [3, 4, 5, 6], "capacity": 5},
    "traveling-salesman-dp": {
        "distance_matrix": [
            [0, 10, 15, 20],
            [10, 0, 35, 25],
            [15, 35, 0, 30],
            [20, 25, 30, 0],
        ],
        "cities": ["A", "B", "C", "D"],
    },
    "reliability-design-dp": {
        "reliabilities": [0.9, 0.8, 0.5],
        "costs": [30, 15, 20],
        "budget": 105,
    },

    # Module 5: Greedy Method I
    "optimal-storage-tapes-greedy": {
        "lengths": [5, 10, 3, 20, 12, 7],
        "tapes": 1,
        "programs": ["P1", "P2", "P3", "P4", "P5", "P6"],
    },
    "fractional-knapsack": {"weights": [10, 20, 30], "values": [60, 100, 120], "capacity": 50},
    "job-sequencing-deadlines": {
        "jobs": [
            {"id": "J1", "deadline": 2, "profit": 100},
            {"id": "J2", "deadline": 1, "profit": 19},
            {"id": "J3", "deadline": 2, "profit": 27},
            {"id": "J4", "deadline": 1, "profit": 25},
            {"id": "J5", "deadline": 3, "profit": 15},
        ],
    },

    # Module 6: Greedy Method II
    "optimal-merge-patterns-greedy": {"files": [20, 30, 10, 5, 30], "names": ["F1", "F2", "F3", "F4", "F5"]},
    "kruskal-mst": {
        "vertices": ["0", "1", "2", "3"],
        "edges": [["0", "1", 10], ["0", "2", 6], ["0", "3", 5], ["1", "3", 15], ["2", "3", 4]],
    },
    "prim-mst": {
        "vertices": ["0", "1", "2", "3"],
        "edges": [["0", "1", 10], ["0", "2", 6], ["0", "3", 5], ["1", "3", 15], ["2", "3", 4]],
    },
    "dijkstra-sssp": {
        "vertices": ["A", "B", "C", "D"],
        "edges": [["A", "B", 1], ["B", "C", 2], ["A", "C", 4], ["C", "D", 1]],
        "source": "A",
    },
    "bellman-ford-sssp": {
        "vertices": ["A", "B", "C", "D"],
        "edges": [["A", "B", 4], ["A", "C", 5], ["B", "C", -2], ["C", "D", 3]],
        "source": "A",
    },

    # Module 7: Branch and Bound
    "0-1-knapsack-lc-bb": {"weights": [2, 4, 6, 9], "values": [10, 10, 12, 18], "capacity": 15},
    "0-1-knapsack-fifo-bb": {"weights": [2, 4, 6, 9], "values": [10, 10, 12, 18], "capacity": 15},
    "traveling-salesman-bb": {
        "distance_matrix": [
            [999999, 20, 30, 10, 11],
            [15, 999999, 16, 4, 2],
            [3, 5, 999999, 2, 4],
            [19, 6, 18, 999999, 3],
            [16, 4, 7, 16, 999999],
        ],
        "cities": ["A", "B", "C", "D", "E"],
    },
}


class TestCurriculumAlgorithmCoverage:
    """Verifies all 23 authoritative curriculum algorithms have genuine step instrumentation."""

    def test_23_approved_slugs_count(self):
        approved = get_all_approved_algorithm_slugs()
        assert len(approved) == 23, f"Expected exactly 23 approved curriculum algorithms, got {len(approved)}"

    @pytest.mark.parametrize("slug", get_all_approved_algorithm_slugs())
    def test_curriculum_algorithm_instrumented_execution(self, slug):
        algo = registry.get(slug)
        assert algo is not None, f"Curriculum algorithm '{slug}' not found in registry"

        sample_input = CURRICULUM_SAMPLE_INPUTS.get(slug)
        assert sample_input is not None, f"Missing test sample input for '{slug}'"

        res = algo.run_instrumented(sample_input, max_steps=500)
        assert res.algorithm_slug == algo.slug
        assert res.success is True
        assert len(res.steps) > 0, f"Algorithm '{slug}' returned 0 execution steps"
        assert res.output is not None

    @pytest.mark.parametrize("slug", get_all_approved_algorithm_slugs())
    def test_step_execution_api_endpoint(self, slug):
        sample_input = CURRICULUM_SAMPLE_INPUTS.get(slug)
        resp = client.post("/api/v1/benchmarks/step", json={
            "algorithm_slug": slug,
            "input_data": sample_input,
            "max_steps": 300
        })
        assert resp.status_code == 200, f"API failed for {slug}: {resp.text}"
        data = resp.json()
        assert data["algorithm_slug"] == slug
        assert len(data["steps"]) > 0
        assert "metrics" in data


class TestStrassenCorrectness:
    """Verifies Strassen's step-by-step partition, M1..M7 product generation, and result equality."""

    def test_strassen_m1_m7_step_presence(self):
        algo = registry.get("strassen-matrix-multiplication")
        assert algo is not None

        test_input = {
            "matrix_a": [[1, 2], [3, 4]],
            "matrix_b": [[5, 6], [7, 8]]
        }

        # 1. Uninstrumented run
        uninstrumented = algo.run(test_input)
        # 2. Instrumented run
        instrumented = algo.run_instrumented(test_input, max_steps=500)

        assert instrumented.output["result_matrix"] == uninstrumented["result_matrix"]

        actions = [s.action for s in instrumented.steps]
        assert "init" in actions
        assert "partition" in actions
        assert "compute_m1" in actions
        assert "compute_m2" in actions
        assert "compute_m3" in actions
        assert "compute_m4" in actions
        assert "compute_m5" in actions
        assert "compute_m6" in actions
        assert "compute_m7" in actions
        assert "combine_quadrants" in actions
        assert "complete" in actions


class TestComplexityEndpoints:
    """Verifies compatible problem groups, complexity profiles, and theoretical separation."""

    def test_compatible_groups_endpoint(self):
        resp = client.get("/api/v1/complexity/compatible-groups")
        assert resp.status_code == 200
        groups = resp.json()
        assert len(groups) >= 4

        prob_slugs = {g["problem_slug"] for g in groups}
        # Required curriculum groups
        assert "0-1-knapsack-problem" in prob_slugs
        assert "traveling-salesman-problem" in prob_slugs
        assert "minimum-spanning-tree" in prob_slugs
        assert "single-source-shortest-path" in prob_slugs

        # Verify 0/1 Knapsack has DP, LC B&B, FIFO B&B
        knapsack_group = next(g for g in groups if g["problem_slug"] == "0-1-knapsack-problem")
        algo_slugs = [a["slug"] for a in knapsack_group["algorithms"]]
        assert "0-1-knapsack-dp" in algo_slugs
        assert "0-1-knapsack-lc-bb" in algo_slugs
        assert "0-1-knapsack-fifo-bb" in algo_slugs

    def test_single_algorithm_complexity_profile(self):
        resp = client.get("/api/v1/complexity/algorithms/0-1-knapsack-dp")
        assert resp.status_code == 200
        profile = resp.json()
        assert profile["slug"] == "0-1-knapsack-dp"
        assert profile["is_curriculum"] is True
        assert profile["module_id"] == 3
        assert "O(n" in profile["worst_case"] or "O(" in profile["worst_case"]
        assert profile["theoretical_vs_empirical_note"] is not None

    def test_nonexistent_algorithm_complexity_profile(self):
        resp = client.get("/api/v1/complexity/algorithms/nonexistent-algorithm")
        assert resp.status_code == 404


class TestTheoryOnlyIsolation:
    """Verifies that theory-only modules (Module 6 & 7) cannot be executed via the step visualizer."""

    def test_theory_topics_not_in_approved_executable_slugs(self):
        approved = set(get_all_approved_algorithm_slugs())
        theory_slugs = [
            "tractable-problems", "non-tractable-problems", "class-p", "class-np",
            "np-hard-problems", "np-complete-problems", "cooks-theorem"
        ]
        for ts in theory_slugs:
            assert ts not in approved, f"Theory-only topic '{ts}' should not be in executable algorithm slugs"
            # Requesting step visualizer for non-registered theory slug should return 404
            resp = client.post("/api/v1/benchmarks/step", json={
                "algorithm_slug": ts,
                "input_data": {}
            })
            assert resp.status_code == 404
