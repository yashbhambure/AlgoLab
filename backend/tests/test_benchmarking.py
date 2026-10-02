"""
Automated Test Suite for Benchmark Runner & Hardware Telemetry.
Validates GC isolation, copy isolation, multi-iteration statistics, and memory profiling across curriculum algorithms.
"""
import pytest
from app.benchmark.runner import BenchmarkRunner, BenchmarkExecutionError
from app.algorithms.divide_and_conquer.max_min import MaxMinDivideConquer
from app.algorithms.greedy.optimal_storage_tapes import OptimalStorageOnTapes


class TestBenchmarkRunner:
    """Test suite for controlled laboratory benchmarking runner."""

    def test_single_run_execution(self):
        """Validates nanosecond timing and input isolation in a single run."""
        runner = BenchmarkRunner(warmup_runs=1, default_iterations=3)
        algo = MaxMinDivideConquer()
        input_data = [5, 2, 8, 1, 9, 3]
        input_copy = list(input_data)

        result = runner.execute_single_run(algo, input_data)
        assert "duration_ns" in result
        assert "duration_ms" in result
        assert result["duration_ns"] > 0
        assert result["output"]["min"] == 1
        assert result["output"]["max"] == 9
        # Ensure original input_data was not mutated externally
        assert input_data == input_copy

    def test_multi_iteration_benchmark(self):
        """Validates multi-iteration benchmark statistics generation."""
        runner = BenchmarkRunner(warmup_runs=1, default_iterations=5)
        input_data = [64, 34, 25, 12, 22, 11, 90]

        bench = runner.benchmark_algorithm("max-min-divide-conquer", input_data, iterations=5)
        assert bench["algorithm_slug"] == "max-min-divide-conquer"
        assert bench["iterations_run"] == 5
        assert "time_stats" in bench
        assert "mean_ms" in bench["time_stats"]
        assert "median_ms" in bench["time_stats"]
        assert "std_dev_ms" in bench["time_stats"]
        assert "p95_ms" in bench["time_stats"]
        assert "p99_ms" in bench["time_stats"]
        assert "memory_stats" in bench

    def test_memory_measurement(self):
        """Validates memory profiling with tracemalloc."""
        runner = BenchmarkRunner()
        algo = OptimalStorageOnTapes()
        input_data = {"lengths": list(range(100, 0, -1)), "tapes": 2}
        mem = runner.measure_memory(algo, input_data)
        assert "peak_kb" in mem or "peak_bytes" in mem or "current_kb" in mem or "peak_memory_kb" in mem

    def test_unknown_algorithm_error(self):
        """Validates that nonexistent algorithms raise BenchmarkExecutionError."""
        runner = BenchmarkRunner()
        with pytest.raises(BenchmarkExecutionError, match="not found in registry"):
            runner.benchmark_algorithm("non-existent-algo-xyz", [1, 2, 3])

    def test_compare_two_algorithms(self):
        """Validates head-to-head comparison between 2 algorithms."""
        from app.benchmark.input_generators import generate_mst_input
        runner = BenchmarkRunner(warmup_runs=1, default_iterations=2)
        payload = generate_mst_input(num_vertices=8)
        res = runner.compare_algorithms(["kruskal-mst", "prim-mst"], payload, iterations=2, warmup_runs=1)

        assert res["total_candidates"] == 2
        assert res["successful_runs"] == 2
        assert res["fastest_algorithm"] in ["kruskal-mst", "prim-mst"]
        assert res["most_memory_efficient"] in ["kruskal-mst", "prim-mst"]
        assert len(res["results"]) == 2
        assert len(res["ranking_by_speed"]) == 2
        assert len(res["ranking_by_memory"]) == 2
        assert "kruskal-mst" in res["speedup_ratios"]
        assert "prim-mst" in res["speedup_ratios"]

    def test_compare_multiple_algorithms(self):
        """Validates comparison across multiple algorithms (3 Knapsack variants)."""
        from app.benchmark.input_generators import generate_knapsack_input
        runner = BenchmarkRunner(warmup_runs=1, default_iterations=2)
        slugs = ["0-1-knapsack-dp", "0-1-knapsack-lc-bb", "0-1-knapsack-fifo-bb"]
        input_data = generate_knapsack_input(num_items=5)
        res = runner.compare_algorithms(slugs, input_data, iterations=2, warmup_runs=1)

        assert res["total_candidates"] == 3
        assert res["successful_runs"] == 3
        assert len(res["results"]) == 3
        assert len(res["ranking_by_speed"]) == 3
        assert len(res["ranking_by_memory"]) == 3
        assert res["fastest_algorithm"] is not None
        assert res["most_memory_efficient"] is not None
        for r in res["results"]:
            assert "time_stats" in r
            assert "mean_ms" in r["time_stats"]
            assert "memory_stats" in r
            assert "peak_kb" in r["memory_stats"]

    @pytest.mark.parametrize("edge_input", [
        [42],
        [1, 2, 3, 4, 5],
        [5, 5, 5, 5, 5],
        [100, -50, 0, 999, -1],
    ])
    def test_compare_edge_case_inputs(self, edge_input):
        """Validates comparative benchmarking against edge-case datasets."""
        runner = BenchmarkRunner(warmup_runs=1, default_iterations=2)
        res = runner.compare_algorithms(["max-min-divide-conquer"], edge_input, iterations=2, warmup_runs=1)
        assert res["total_candidates"] == 1
        assert res["successful_runs"] == 1
        assert len(res["results"]) == 1

    def test_compare_with_failed_and_incompatible_algorithm(self):
        """
        Validates error tolerance during comparative benchmark.
        A nonexistent or incompatible algorithm must be isolated in errors dict
        without crashing the entire comparison or other successful algorithms.
        """
        runner = BenchmarkRunner(warmup_runs=1, default_iterations=2)
        slugs = ["max-min-divide-conquer", "non-existent-algo"]
        input_data = [5, 3, 8, 1, 2]
        res = runner.compare_algorithms(slugs, input_data, iterations=2, warmup_runs=1)

        assert res["total_candidates"] == 2
        assert res["successful_runs"] == 1
        assert len(res["results"]) == 1
        assert res["results"][0]["algorithm_slug"] == "max-min-divide-conquer"
        assert res["fastest_algorithm"] == "max-min-divide-conquer"
        assert res["most_memory_efficient"] == "max-min-divide-conquer"
        assert "non-existent-algo" in res["errors"]

    def test_compare_repeated_executions(self):
        """Validates that repeated benchmark comparisons maintain idempotency and isolation."""
        from app.benchmark.input_generators import generate_mst_input
        runner = BenchmarkRunner(warmup_runs=1, default_iterations=2)
        input_data = generate_mst_input(num_vertices=6)
        res1 = runner.compare_algorithms(["kruskal-mst", "prim-mst"], input_data, iterations=2, warmup_runs=1)
        res2 = runner.compare_algorithms(["kruskal-mst", "prim-mst"], input_data, iterations=2, warmup_runs=1)

        assert res1["successful_runs"] == 2
        assert res2["successful_runs"] == 2
        assert len(res1["results"]) == 2
        assert len(res2["results"]) == 2

    def test_canonical_knapsack_benchmark(self):
        """Validates head-to-head benchmarking across 3 Knapsack implementations (DP, LC-BB, FIFO-BB)."""
        from app.benchmark.input_generators import generate_knapsack_input
        runner = BenchmarkRunner(warmup_runs=1, default_iterations=2)
        payload = generate_knapsack_input(num_items=6)
        slugs = ["0-1-knapsack-dp", "0-1-knapsack-lc-bb", "0-1-knapsack-fifo-bb"]
        res = runner.compare_algorithms(slugs, payload, iterations=2, warmup_runs=1)

        assert res["total_candidates"] == 3
        assert res["successful_runs"] == 3
        assert len(res["results"]) == 3
        assert res["fastest_algorithm"] in slugs
        assert res["most_memory_efficient"] in slugs

    def test_canonical_tsp_benchmark(self):
        """Validates head-to-head benchmarking between Held-Karp DP and Branch & Bound TSP."""
        from app.benchmark.input_generators import generate_tsp_input
        runner = BenchmarkRunner(warmup_runs=1, default_iterations=2)
        payload = generate_tsp_input(num_cities=5)
        slugs = ["traveling-salesman-dp", "traveling-salesman-bb"]
        res = runner.compare_algorithms(slugs, payload, iterations=2, warmup_runs=1)

        assert res["total_candidates"] == 2
        assert res["successful_runs"] == 2
        assert len(res["results"]) == 2

    def test_canonical_mst_benchmark(self):
        """Validates head-to-head benchmarking between Kruskal and Prim MST."""
        from app.benchmark.input_generators import generate_mst_input
        runner = BenchmarkRunner(warmup_runs=1, default_iterations=2)
        payload = generate_mst_input(num_vertices=10)
        slugs = ["kruskal-mst", "prim-mst"]
        res = runner.compare_algorithms(slugs, payload, iterations=2, warmup_runs=1)

        assert res["total_candidates"] == 2
        assert res["successful_runs"] == 2
        assert len(res["results"]) == 2

    def test_canonical_sssp_benchmark(self):
        """Validates head-to-head benchmarking between Dijkstra and Bellman-Ford SSSP."""
        from app.benchmark.input_generators import generate_sssp_input
        runner = BenchmarkRunner(warmup_runs=1, default_iterations=2)
        payload = generate_sssp_input(num_vertices=8)
        slugs = ["dijkstra-sssp", "bellman-ford-sssp"]
        res = runner.compare_algorithms(slugs, payload, iterations=2, warmup_runs=1)

        assert res["total_candidates"] == 2
        assert res["successful_runs"] == 2
        assert len(res["results"]) == 2

    def test_backtracking_benchmarks(self):
        """Validates isolated benchmarking on N-Queens and Subset Sum."""
        from app.benchmark.input_generators import generate_n_queens_input, generate_subset_sum_input
        runner = BenchmarkRunner(warmup_runs=1, default_iterations=2)

        # N-Queens
        q_res = runner.benchmark_algorithm("n-queens-backtracking", generate_n_queens_input(6), iterations=2)
        assert q_res["algorithm_slug"] == "n-queens-backtracking"
        assert q_res["execution_time_ms"] > 0

        # Subset Sum
        ss_res = runner.benchmark_algorithm("subset-sum-backtracking", generate_subset_sum_input(8), iterations=2)
        assert ss_res["algorithm_slug"] == "subset-sum-backtracking"
        assert ss_res["execution_time_ms"] > 0

    def test_canonical_apsp_benchmark_and_formats(self):
        """
        Regression test for Floyd-Warshall APSP:
        Validates generated payload, run(), run_instrumented(), and benchmark execution.
        """
        from app.benchmark.input_generators import generate_apsp_input, generate_problem_input
        from app.algorithms.registry import registry

        algo = registry.get("floyd-warshall-apsp")
        assert algo is not None

        # 1. Test with generator payload (contains vertices, edges, and matrix)
        gen_payload = generate_problem_input("all-pairs-shortest-path", size=4)
        assert "matrix" in gen_payload
        assert "vertices" in gen_payload

        run_res = algo.run(gen_payload)
        assert "distance_matrix" in run_res
        assert run_res["matrix_size"] == 4

        inst_res = algo.run_instrumented(gen_payload, max_steps=50)
        assert inst_res.output["matrix_size"] == 4
        assert len(inst_res.steps) > 0
        assert inst_res.metrics.operations > 0

        # 2. Test benchmark runner execution
        runner = BenchmarkRunner(warmup_runs=1, default_iterations=2)
        bench_res = runner.benchmark_algorithm("floyd-warshall-apsp", gen_payload, iterations=2)
        assert bench_res["algorithm_slug"] == "floyd-warshall-apsp"
        assert bench_res["execution_time_ms"] > 0
        assert bench_res["time_stats"]["mean_ms"] > 0

        # 3. Test with pure 2D matrix list format
        raw_matrix = [
            [0.0, 5.0, float("inf")],
            [float("inf"), 0.0, 2.0],
            [1.0, float("inf"), 0.0]
        ]
        raw_res = algo.run(raw_matrix)
        assert raw_res["matrix_size"] == 3
        raw_inst = algo.run_instrumented(raw_matrix, max_steps=20)
        assert raw_inst.output["matrix_size"] == 3

        # 4. Test with standard graph vertices/edges dict format
        graph_dict = {
            "vertices": ["A", "B", "C"],
            "edges": [{"source": "A", "target": "B", "weight": 4}, {"source": "B", "target": "C", "weight": 1}]
        }
        graph_res = algo.run(graph_dict)
        assert graph_res["matrix_size"] == 3
        assert graph_res["distance_matrix"]["A"]["C"] == 5.0
