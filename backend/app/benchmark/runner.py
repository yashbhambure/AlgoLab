"""
Isolated Benchmark Runner with GC suspension, warmup runs, and high-precision telemetry.
"""
import copy
import gc
import sys
import time
import concurrent.futures
from typing import Dict, Any, List, Optional
from app.algorithms.registry import registry
from app.algorithms.base import BaseAlgorithm, AlgorithmExecutionResult
from app.benchmark.timer import PrecisionTimer
from app.benchmark.memory_tracker import MemoryTracker
from app.benchmark.stats import BenchmarkStats


class BenchmarkExecutionError(Exception):
    pass


class BenchmarkRunner:
    """
    Executes algorithms under controlled laboratory conditions to produce verified,
    non-simulated empirical metrics.
    """

    def __init__(self, warmup_runs: int = 2, default_iterations: int = 5, timeout_seconds: float = 30.0):
        self.warmup_runs = warmup_runs
        self.default_iterations = default_iterations
        self.timeout_seconds = timeout_seconds

    def execute_single_run(self, algo: BaseAlgorithm, input_data: Any) -> Dict[str, Any]:
        """
        Executes a single isolated run of the algorithm with GC control.
        """
        # Deep copy input data so in-place operations don't leak across runs
        data_copy = copy.deepcopy(input_data)

        # Force garbage collection before timing
        gc.collect()
        gc.disable()

        start_time = time.perf_counter_ns()
        try:
            output = algo.run(data_copy)
        finally:
            end_time = time.perf_counter_ns()
            gc.enable()

        duration_ns = end_time - start_time
        duration_ms = duration_ns / 1_000_000.0

        return {
            "duration_ns": duration_ns,
            "duration_ms": duration_ms,
            "output": output
        }

    def measure_memory(self, algo: BaseAlgorithm, input_data: Any) -> Dict[str, float]:
        """
        Executes a run under tracemalloc to determine peak and allocated memory.
        """
        data_copy = copy.deepcopy(input_data)
        gc.collect()

        _, mem_info = MemoryTracker.measure(algo.run, data_copy)
        return mem_info

    def benchmark_algorithm(
        self,
        algorithm_slug: str,
        input_data: Any,
        iterations: Optional[int] = None,
        warmup_runs: Optional[int] = None,
        include_instrumentation: bool = True
    ) -> Dict[str, Any]:
        """
        Conducts a multi-iteration benchmark suite on a specific algorithm.
        """
        algo = registry.get(algorithm_slug)
        if not algo:
            raise BenchmarkExecutionError(f"Algorithm '{algorithm_slug}' not found in registry.")

        num_iterations = iterations if iterations is not None else self.default_iterations
        if num_iterations < 1:
            num_iterations = 1

        actual_warmup = warmup_runs if warmup_runs is not None else self.warmup_runs

        # 1. Warmup runs
        for _ in range(actual_warmup):
            data_copy = copy.deepcopy(input_data)
            try:
                algo.run(data_copy)
            except Exception as e:
                raise BenchmarkExecutionError(f"Warmup execution failed for {algorithm_slug}: {str(e)}")

        # 2. Timed Iterations
        durations_ms: List[float] = []
        last_output = None

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            for i in range(num_iterations):
                future = executor.submit(self.execute_single_run, algo, input_data)
                try:
                    res = future.result(timeout=self.timeout_seconds)
                    durations_ms.append(res["duration_ms"])
                    last_output = res["output"]
                except concurrent.futures.TimeoutError:
                    raise BenchmarkExecutionError(
                        f"Algorithm '{algorithm_slug}' timed out after {self.timeout_seconds}s on iteration {i+1}."
                    )
                except Exception as e:
                    raise BenchmarkExecutionError(f"Execution error on {algorithm_slug}: {str(e)}")

        # 3. Memory Measurement
        mem_info = self.measure_memory(algo, input_data)

        # 4. Statistical Metrics Aggregation
        time_stats = BenchmarkStats.calculate_duration_stats(durations_ms)

        # 5. Instrumentation for Operation Counting (Comparisons, Swaps, Recursive Calls)
        operations_count = 0
        comparisons_count = 0
        swaps_count = 0
        recursive_calls_count = 0
        steps_summary = []

        if include_instrumentation:
            try:
                data_copy = copy.deepcopy(input_data)
                instrumented_res: AlgorithmExecutionResult = algo.run_instrumented(data_copy, max_steps=100)
                comparisons_count = instrumented_res.metrics.comparisons
                swaps_count = instrumented_res.metrics.swaps
                recursive_calls_count = instrumented_res.metrics.recursive_calls
                operations_count = (
                    instrumented_res.metrics.operations or
                    (comparisons_count + swaps_count + recursive_calls_count)
                )
                steps_summary = [s.to_dict() for s in instrumented_res.steps[:20]]
            except Exception:
                pass

        # Infer input size
        input_size = 0
        if isinstance(input_data, list):
            input_size = len(input_data)
        elif isinstance(input_data, dict):
            if "array" in input_data:
                input_size = len(input_data["array"])
            elif "matrix_a" in input_data:
                input_size = len(input_data["matrix_a"])
            elif "weights" in input_data:
                input_size = len(input_data["weights"])
            elif "vertices" in input_data:
                input_size = len(input_data["vertices"])
            elif "n" in input_data:
                input_size = int(input_data["n"])
            elif "str1" in input_data:
                input_size = max(len(input_data.get("str1", "")), len(input_data.get("str2", "")))

        return {
            "algorithm_slug": algorithm_slug,
            "algorithm_name": algo.name,
            "category": algo.category,
            "input_size": input_size,
            "iterations": num_iterations,
            "iterations_run": num_iterations,
            "raw_durations_ms": durations_ms,
            "time_stats": time_stats,
            "execution_time_ms": time_stats["mean_ms"],
            "memory_stats": {
                "allocated_kb": round(mem_info["allocated_kb"], 4),
                "peak_kb": round(mem_info["peak_kb"], 4)
            },
            "metrics": {
                "comparisons": comparisons_count,
                "swaps": swaps_count,
                "recursive_calls": recursive_calls_count,
                "operations": operations_count
            },
            "steps_sample": steps_summary,
            "output_preview": str(last_output)[:200] if last_output is not None else None
        }

    def compare_algorithms(
        self,
        algorithm_slugs: List[str],
        input_data: Any,
        iterations: Optional[int] = None,
        warmup_runs: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Executes multiple algorithms sequentially on the exact same dataset to produce
        a head-to-head empirical comparison.
        """
        results = []
        errors = {}

        for slug in algorithm_slugs:
            try:
                res = self.benchmark_algorithm(slug, input_data, iterations=iterations, warmup_runs=warmup_runs)
                results.append(res)
            except Exception as e:
                errors[slug] = str(e)

        # Sort results by execution time (fastest first)
        sorted_results = sorted(results, key=lambda x: x["execution_time_ms"])

        # Determine winner
        winner_slug = sorted_results[0]["algorithm_slug"] if sorted_results else None
        speedup_ratios = {}
        if sorted_results:
            base_time = sorted_results[0]["execution_time_ms"]
            for r in sorted_results:
                slug = r["algorithm_slug"]
                if r["execution_time_ms"] > 0 and base_time > 0:
                    speedup_ratios[slug] = round(r["execution_time_ms"] / base_time, 2)
                else:
                    speedup_ratios[slug] = 1.0

        # Memory ranking & winner
        sorted_by_memory = sorted(results, key=lambda x: x.get("memory_stats", {}).get("peak_kb", 0.0)) if results else []
        most_memory_efficient_slug = sorted_by_memory[0]["algorithm_slug"] if sorted_by_memory else None

        ranking_by_speed = [r["algorithm_slug"] for r in sorted_results]
        ranking_by_memory = [r["algorithm_slug"] for r in sorted_by_memory]

        return {
            "total_candidates": len(algorithm_slugs),
            "successful_runs": len(results),
            "fastest_algorithm": winner_slug,
            "most_memory_efficient": most_memory_efficient_slug,
            "ranking_by_speed": ranking_by_speed,
            "ranking_by_memory": ranking_by_memory,
            "speedup_ratios": speedup_ratios,
            "results": sorted_results,
            "errors": errors
        }


# Global benchmark runner instance
benchmark_runner = BenchmarkRunner()
