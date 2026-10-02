"""
Memory Allocation and Peak Tracking using tracemalloc.
"""
import tracemalloc
from typing import Callable, Any, Tuple, Dict


class MemoryTracker:
    """
    Measures allocated and peak memory usage of a callable in kilobytes.
    """

    @staticmethod
    def measure(func: Callable, *args, **kwargs) -> Tuple[Any, Dict[str, float]]:
        """
        Executes a function under tracemalloc surveillance.

        Returns:
            (result, {"allocated_kb": float, "peak_kb": float})
        """
        tracemalloc.start()
        tracemalloc.reset_peak()

        try:
            result = func(*args, **kwargs)
            current, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()

        return result, {
            "allocated_kb": current / 1024.0,
            "peak_kb": peak / 1024.0
        }
