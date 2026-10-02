"""
Benchmark Pydantic Schemas
"""
from typing import List, Optional, Any, Dict
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class BenchmarkRunRequest(BaseModel):
    problem_id: str
    algorithm_ids: List[str]
    dataset_id: Optional[str] = None
    custom_dataset: Optional[Dict[str, Any]] = None
    dataset_config: Optional[Dict[str, Any]] = None  # inline generation if dataset_id not provided
    repetitions: int = Field(default=5, ge=1, le=50)
    warmup_runs: int = Field(default=2, ge=0, le=10)
    name: Optional[str] = None


class BenchmarkResultResponse(BaseModel):
    id: Optional[str] = None
    algorithm_id: str
    algorithm_name: str
    category: Optional[str] = None
    paradigm: Optional[str] = None
    input_size: int

    # Timing metrics (ms)
    min_time_ms: float
    max_time_ms: float
    mean_time_ms: float
    median_time_ms: float
    std_dev_time_ms: float

    # Memory metrics
    memory_peak_kb: float
    memory_allocated_kb: float

    # Operation Counters
    comparisons_count: int = 0
    swaps_count: int = 0
    recursive_calls_count: int = 0
    operations_count: int = 0

    raw_execution_times: List[float] = []
    status: str = "success"
    error_message: Optional[str] = None

    # Theoretical complexities for direct side-by-side comparison
    theoretical_time: Optional[str] = None
    theoretical_space: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class BenchmarkRunResponse(BaseModel):
    id: str
    name: Optional[str] = None
    problem_id: str
    problem_name: Optional[str] = None
    dataset_id: Optional[str] = None
    dataset_summary: Optional[Dict[str, Any]] = None
    status: str
    repetitions: int
    warmup_runs: int
    hardware_info: Dict[str, Any] = {}
    total_duration_ms: float
    created_at: Optional[datetime] = None
    results: List[BenchmarkResultResponse] = []
    fastest_algorithm: Optional[str] = None
    least_memory_algorithm: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class BenchmarkComparisonResponse(BaseModel):
    benchmark_run_id: str
    problem_name: str
    input_size: int
    results: List[BenchmarkResultResponse]
    speedup_matrix: Dict[str, Dict[str, float]]  # relative speedup between algorithms
    summary_analysis: Dict[str, Any]
