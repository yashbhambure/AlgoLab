"""
Base Algorithm Interface and Execution Context
Provides standard execution signatures, metric instrumentation, and step tracing.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
import copy


@dataclass
class ExecutionMetrics:
    """Holds counters collected during instrumented algorithm execution."""
    comparisons: int = 0
    swaps: int = 0
    recursive_calls: int = 0
    operations: int = 0
    peak_memory_kb: float = 0.0
    allocated_memory_kb: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "comparisons": self.comparisons,
            "swaps": self.swaps,
            "recursive_calls": self.recursive_calls,
            "operations": self.operations,
            "peak_memory_kb": self.peak_memory_kb,
            "allocated_memory_kb": self.allocated_memory_kb,
        }


@dataclass
class ExecutionStep:
    """Single step in an algorithm's execution for visualizer animation."""
    step_id: int
    action: str  # e.g., 'compare', 'swap', 'visit', 'set_dp', 'backtrack', 'select', 'split', 'merge'
    indices: List[Any] = field(default_factory=list)
    values: List[Any] = field(default_factory=list)
    state_snapshot: Any = None
    description: str = ""
    highlight_line: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step_id": self.step_id,
            "action": self.action,
            "indices": self.indices,
            "values": self.values,
            "state_snapshot": self.state_snapshot,
            "description": self.description,
            "highlight_line": self.highlight_line,
            "metadata": self.metadata,
        }


@dataclass
class AlgorithmExecutionResult:
    """Return structure for an algorithm execution."""
    algorithm_slug: str
    output: Any
    metrics: ExecutionMetrics
    steps: List[ExecutionStep] = field(default_factory=list)
    success: bool = True
    error_message: Optional[str] = None


class BaseAlgorithm(ABC):
    """Abstract base class for all DAA algorithms."""

    slug: str = "base-algorithm"
    name: str = "Base Algorithm"
    category: str = "General"
    paradigm: str = "General"

    time_complexity_best: str = "O(n)"
    time_complexity_average: str = "O(n log n)"
    time_complexity_worst: str = "O(n^2)"
    space_complexity: str = "O(1)"
    is_stable: bool = False
    is_in_place: bool = True

    @abstractmethod
    def run(self, input_data: Any) -> Any:
        """Pure uninstrumented execution for clean benchmarking."""
        pass

    @abstractmethod
    def run_instrumented(self, input_data: Any, max_steps: int = 500) -> AlgorithmExecutionResult:
        """Instrumented execution collecting operation counts and visualization steps."""
        pass

    def prepare_input(self, input_data: Any) -> Any:
        """Deep copy input to prevent in-place mutation side-effects."""
        return copy.deepcopy(input_data)
