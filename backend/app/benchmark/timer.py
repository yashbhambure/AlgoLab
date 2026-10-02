"""
High-precision timer for algorithm benchmarking.
Uses time.perf_counter_ns for nanosecond resolution.
"""
import time
from typing import Callable, Any, Dict

class PrecisionTimer:
    """
    Provides nanosecond-precision timing for execution measurement.
    """

    @staticmethod
    def measure(func: Callable, *args, **kwargs) -> Dict[str, int]:
        """
        Measures the execution time of a function in nanoseconds.

        Args:
            func: The function to be measured.
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.

        Returns:
            A dictionary containing the start time, end time, and duration.
        """
        start = time.perf_counter_ns()
        func(*args, **kwargs)
        end = time.perf_counter_ns()

        return {
            "start_ns": start,
            "end_ns": end,
            "duration_ns": end - start
        }
