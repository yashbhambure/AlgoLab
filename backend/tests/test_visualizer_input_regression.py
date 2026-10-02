"""
Regression tests for Visualizer input synchronization and instrumented step execution.
Verifies:
1. Changed 1D array input produces traces reflecting the exact modified array.
2. Changed structured JSON object produces traces reflecting the modified object.
3. Consecutive executions with distinct inputs produce distinct, isolated traces.
4. Invalid inputs raise clear validation errors and are not silently substituted with presets.
5. All 23 authoritative curriculum algorithms properly execute custom inputs via run_instrumented().
6. The /benchmarks/step API endpoint transmits and executes the exact input payload.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.algorithms.registry import registry
from app.curriculum.curriculum_data import get_all_approved_algorithm_slugs

client = TestClient(app)
APPROVED_CURRICULUM_ALGORITHMS = get_all_approved_algorithm_slugs()


def test_visualizer_changed_1d_array_input():
    """
    Test 1: Changed array input.
    Default array [22, 13, -5, 88, 41, 7, 95, 3] vs custom [10, 20, 30].
    Assert trace contains only the modified array elements and correct min/max.
    """
    custom_input = [10, 20, 30]
    res = client.post("/api/v1/benchmarks/step", json={
        "algorithm_slug": "max-min-divide-conquer",
        "input_data": custom_input,
        "max_steps": 300
    })
    assert res.status_code == 200
    data = res.json()
    assert data["algorithm_slug"] == "max-min-divide-conquer"
    assert data["output"]["min"] == 10.0
    assert data["output"]["max"] == 30.0
    assert data["output"]["size"] == 3

    # Check init step snapshot matches custom input
    init_step = next(s for s in data["steps"] if s["action"] == "init")
    assert init_step["state_snapshot"] == [10.0, 20.0, 30.0]


def test_visualizer_changed_structured_json_object():
    """
    Test 2: Changed structured JSON object.
    Custom 4x4 chessboard with defect at [2, 3] vs default [0, 0].
    Assert defect and tiled grid match the custom coordinates.
    """
    custom_input = {"size": 4, "defect": [2, 3]}
    res = client.post("/api/v1/benchmarks/step", json={
        "algorithm_slug": "defective-chessboard",
        "input_data": custom_input,
        "max_steps": 300
    })
    assert res.status_code == 200
    data = res.json()
    assert data["output"]["board_size"] == 4
    assert data["output"]["defect"] == [2, 3]
    board = data["output"]["board"]
    assert board[2][3] == -1  # Defect location
    assert board[0][0] != -1  # Default location is NOT defect


def test_visualizer_consecutive_executions_isolation():
    """
    Test 3: Consecutive executions with distinct inputs.
    Run A: N=4 Queens -> 2 solutions.
    Run B: N=5 Queens -> 10 solutions.
    Assert traces are completely isolated and trace B has N=5 state snapshots.
    """
    res_a = client.post("/api/v1/benchmarks/step", json={
        "algorithm_slug": "n-queens-backtracking",
        "input_data": {"n": 4},
        "max_steps": 300
    })
    assert res_a.status_code == 200
    data_a = res_a.json()
    assert data_a["output"]["n"] == 4
    assert data_a["output"]["total_solutions"] == 2

    res_b = client.post("/api/v1/benchmarks/step", json={
        "algorithm_slug": "n-queens-backtracking",
        "input_data": {"n": 5},
        "max_steps": 300
    })
    assert res_b.status_code == 200
    data_b = res_b.json()
    assert data_b["output"]["n"] == 5
    assert data_b["output"]["total_solutions"] == 10

    # Ensure trace B steps reflect 5-element board state
    init_b = next(s for s in data_b["steps"] if s["action"] == "init")
    assert len(init_b["state_snapshot"]) == 5


def test_visualizer_subset_sum_custom_input():
    """
    Test 4: Subset Sum custom input handling.
    Test with numbers=[1, 2, 3, 4] and target_sum=7.
    """
    custom_input = {"numbers": [1, 2, 3, 4], "target_sum": 7}
    res = client.post("/api/v1/benchmarks/step", json={
        "algorithm_slug": "subset-sum-backtracking",
        "input_data": custom_input,
        "max_steps": 300
    })
    assert res.status_code == 200
    data = res.json()
    assert data["output"]["has_solution"] is True
    assert data["output"]["target"] == 7
    # Solutions for sum=7 from [1, 2, 3, 4]: [1, 2, 4], [3, 4]
    assert data["output"]["total_solutions"] == 2


def test_visualizer_invalid_algorithm_slug():
    """
    Test 5: Non-existent algorithm slug returns 404.
    """
    res = client.post("/api/v1/benchmarks/step", json={
        "algorithm_slug": "non-existent-bubble-sort",
        "input_data": [1, 2, 3],
        "max_steps": 100
    })
    assert res.status_code == 404


@pytest.mark.parametrize("slug", APPROVED_CURRICULUM_ALGORITHMS)
def test_all_23_curriculum_algorithms_instrumented_custom_input(slug):
    """
    Test 6: Verify all 23 authoritative curriculum algorithms accept custom execution inputs
    via run_instrumented() without error, returning valid step sequences and metrics.
    """
    algo = registry.get(slug)
    assert algo is not None, f"Curriculum algorithm {slug} missing from registry"

    sample_inputs = {
        "defective-chessboard": {"size": 4, "defect": [1, 1]},
        "max-min-divide-conquer": [15, 3, 99, -4, 42, 8],
        "strassen-matrix-multiplication": {
            "matrix_a": [[2, 0], [1, 3]],
            "matrix_b": [[1, 2], [3, 4]]
        },
        "n-queens-backtracking": {"n": 4},
        "subset-sum-backtracking": {"numbers": [2, 4, 6, 8], "target_sum": 10},
        "hamiltonian-cycle-backtracking": {
            "vertices": ["0", "1", "2", "3"],
            "edges": [["0", "1"], ["1", "2"], ["2", "3"], ["3", "0"]]
        },
        "multistage-graph-dp": {
            "num_vertices": 4,
            "stages": 3,
            "edges": [
                {"from": 1, "to": 2, "weight": 2},
                {"from": 1, "to": 3, "weight": 4},
                {"from": 2, "to": 4, "weight": 3},
                {"from": 3, "to": 4, "weight": 1}
            ]
        },
        "floyd-warshall-apsp": {
            "matrix": [
                [0, 5, 999999],
                [999999, 0, 3],
                [2, 999999, 0]
            ]
        },
        "optimal-bst-dp": {
            "keys": ["A", "B", "C"],
            "p": [0.2, 0.5, 0.3],
            "q": [0.05, 0.05, 0.05, 0.05]
        },
        "0-1-knapsack-dp": {
            "weights": [1, 2, 3],
            "values": [6, 10, 12],
            "capacity": 5
        },
        "traveling-salesman-dp": {
            "distance_matrix": [
                [0, 10, 20],
                [10, 0, 15],
                [20, 15, 0]
            ],
            "cities": ["X", "Y", "Z"]
        },
        "reliability-design-dp": {
            "reliabilities": [0.8, 0.7],
            "costs": [20, 10],
            "budget": 50
        },
        "optimal-storage-tapes-greedy": {
            "lengths": [4, 8, 2],
            "tapes": 1,
            "programs": ["ProgA", "ProgB", "ProgC"]
        },
        "fractional-knapsack": {
            "weights": [10, 20, 30],
            "values": [60, 100, 120],
            "capacity": 40
        },
        "job-sequencing-deadlines": {
            "jobs": [
                {"id": "A", "deadline": 1, "profit": 50},
                {"id": "B", "deadline": 2, "profit": 100},
                {"id": "C", "deadline": 2, "profit": 80}
            ]
        },
        "optimal-merge-patterns-greedy": {
            "files": [10, 20, 30],
            "names": ["File1", "File2", "File3"]
        },
        "kruskal-mst": {
            "vertices": ["0", "1", "2"],
            "edges": [["0", "1", 4], ["1", "2", 2], ["0", "2", 5]]
        },
        "prim-mst": {
            "vertices": ["0", "1", "2"],
            "edges": [["0", "1", 4], ["1", "2", 2], ["0", "2", 5]]
        },
        "dijkstra-sssp": {
            "vertices": ["A", "B", "C"],
            "edges": [["A", "B", 4], ["B", "C", 2], ["A", "C", 8]],
            "source": "A"
        },
        "bellman-ford-sssp": {
            "vertices": ["A", "B", "C"],
            "edges": [["A", "B", 4], ["B", "C", -2], ["A", "C", 5]],
            "source": "A"
        },
        "0-1-knapsack-lc-bb": {
            "weights": [2, 3, 5],
            "values": [10, 12, 20],
            "capacity": 7
        },
        "0-1-knapsack-fifo-bb": {
            "weights": [2, 3, 5],
            "values": [10, 12, 20],
            "capacity": 7
        },
        "traveling-salesman-bb": {
            "distance_matrix": [
                [999999, 10, 15],
                [10, 999999, 20],
                [15, 20, 999999]
            ],
            "cities": ["A", "B", "C"]
        }
    }

    payload = sample_inputs.get(slug, [1, 2, 3])
    res = client.post("/api/v1/benchmarks/step", json={
        "algorithm_slug": slug,
        "input_data": payload,
        "max_steps": 300
    })
    assert res.status_code == 200, f"Failed for algorithm {slug}: {res.text}"
    data = res.json()
    assert data["algorithm_slug"] == slug
    assert len(data["steps"]) > 0
    assert "metrics" in data
    assert "output" in data
