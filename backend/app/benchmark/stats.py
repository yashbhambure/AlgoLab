"""
Statistical Aggregation Utilities for Benchmark Runs.
"""
import math
import statistics
from typing import List, Dict, Any


class BenchmarkStats:
    """
    Computes rigorous descriptive statistics over a collection of execution samples.
    """

    @staticmethod
    def calculate_duration_stats(durations_ms: List[float]) -> Dict[str, float]:
        """
        Calculates descriptive statistics for a list of execution times in milliseconds.
        """
        if not durations_ms:
            return {
                "min_ms": 0.0,
                "max_ms": 0.0,
                "mean_ms": 0.0,
                "median_ms": 0.0,
                "std_dev_ms": 0.0,
                "variance_ms": 0.0,
                "p95_ms": 0.0,
                "p99_ms": 0.0,
                "iqr_ms": 0.0,
            }

        n = len(durations_ms)
        sorted_d = sorted(durations_ms)
        min_v = sorted_d[0]
        max_v = sorted_d[-1]
        mean_v = statistics.mean(sorted_d)
        median_v = statistics.median(sorted_d)
        std_dev_v = statistics.stdev(sorted_d) if n > 1 else 0.0
        variance_v = statistics.variance(sorted_d) if n > 1 else 0.0

        # Percentiles
        p95_idx = int(math.ceil(0.95 * n)) - 1
        p99_idx = int(math.ceil(0.99 * n)) - 1
        p95_v = sorted_d[min(p95_idx, n - 1)]
        p99_v = sorted_d[min(p99_idx, n - 1)]

        # IQR
        q1_idx = int(math.ceil(0.25 * n)) - 1
        q3_idx = int(math.ceil(0.75 * n)) - 1
        iqr_v = sorted_d[min(q3_idx, n - 1)] - sorted_d[min(q1_idx, n - 1)]

        return {
            "min_ms": round(min_v, 6),
            "max_ms": round(max_v, 6),
            "mean_ms": round(mean_v, 6),
            "median_ms": round(median_v, 6),
            "std_dev_ms": round(std_dev_v, 6),
            "variance_ms": round(variance_v, 8),
            "p95_ms": round(p95_v, 6),
            "p99_ms": round(p99_v, 6),
            "iqr_ms": round(iqr_v, 6),
        }

    @staticmethod
    def calculate_memory_stats(peak_memories_kb: List[float]) -> Dict[str, float]:
        """
        Calculates descriptive statistics for memory measurements in KB.
        """
        if not peak_memories_kb:
            return {
                "min_kb": 0.0,
                "max_kb": 0.0,
                "mean_kb": 0.0,
                "median_kb": 0.0,
                "std_dev_kb": 0.0,
            }

        n = len(peak_memories_kb)
        sorted_m = sorted(peak_memories_kb)
        return {
            "min_kb": round(sorted_m[0], 4),
            "max_kb": round(sorted_m[-1], 4),
            "mean_kb": round(statistics.mean(sorted_m), 4),
            "median_kb": round(statistics.median(sorted_m), 4),
            "std_dev_kb": round(statistics.stdev(sorted_m), 4) if n > 1 else 0.0,
        }
