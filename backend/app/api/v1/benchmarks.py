"""
Real-time Benchmarking and Execution Visualizer Endpoints.
Guaranteed non-mocked, nanosecond-precise execution on genuine hardware.
"""
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_optional_user
from app.benchmark.runner import benchmark_runner, BenchmarkExecutionError
from app.algorithms.registry import registry
from app.models.dataset import Dataset
from app.models.algorithm import Algorithm
from app.models.user import User

router = APIRouter(prefix="/benchmarks", tags=["Benchmarks"])


class BenchmarkSingleRequest(BaseModel):
    algorithm_slug: str = Field(..., description="Algorithm slug to execute")
    dataset_id: Optional[str] = Field(None, description="Database dataset ID")
    custom_input: Optional[Any] = Field(None, description="Direct custom input data")
    input_data: Optional[Any] = Field(None, description="Alias for custom input data")
    iterations: int = Field(5, ge=1, le=50, description="Repetition iterations for statistical sampling")
    repetitions: Optional[int] = Field(None, ge=1, le=50, description="Alias for iterations")
    warmup_runs: int = Field(2, ge=0, le=10)


class BenchmarkCompareRequest(BaseModel):
    algorithm_slugs: List[str] = Field(..., min_items=1, description="List of algorithm slugs to compare")
    dataset_id: Optional[str] = Field(None, description="Database dataset ID")
    custom_input: Optional[Any] = Field(None, description="Direct custom input data")
    input_data: Optional[Any] = Field(None, description="Alias for custom input data")
    iterations: int = Field(5, ge=1, le=50, description="Repetitions per algorithm")
    repetitions: Optional[int] = Field(None, ge=1, le=50, description="Alias for iterations")
    warmup_runs: int = Field(2, ge=0, le=10)


class VisualizerStepRequest(BaseModel):
    algorithm_slug: str = Field(..., description="Algorithm slug to visualize")
    input_data: Any = Field(..., description="Input data to execute and visualize")
    max_steps: int = Field(300, ge=1, le=1000, description="Maximum step snapshots to record")


def _resolve_input(dataset_id: Optional[str], custom_input: Optional[Any], input_data: Optional[Any], db: Session) -> Any:
    if custom_input is not None:
        return custom_input
    if input_data is not None:
        return input_data
    if dataset_id is not None:
        ds = db.query(Dataset).filter(Dataset.id == dataset_id).first()
        if not ds:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dataset with ID {dataset_id} not found."
            )
        return ds.data_payload
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Either 'dataset_id', 'custom_input', or 'input_data' must be provided."
    )


@router.post("/run")
def run_single_benchmark(
    req: BenchmarkSingleRequest,
    db: Session = Depends(get_db)
) -> Any:
    """
    Executes a single algorithm in isolated laboratory conditions.
    Measures duration (time.perf_counter_ns), memory (tracemalloc), and operations.
    """
    input_data = _resolve_input(req.dataset_id, req.custom_input, req.input_data, db)
    iters = req.repetitions if req.repetitions is not None else req.iterations

    try:
        result = benchmark_runner.benchmark_algorithm(
            algorithm_slug=req.algorithm_slug,
            input_data=input_data,
            iterations=iters,
            warmup_runs=req.warmup_runs,
            include_instrumentation=True
        )
        return result
    except BenchmarkExecutionError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Benchmark execution failed: {str(e)}"
        )


@router.post("/compare")
def compare_algorithms_benchmark(
    req: BenchmarkCompareRequest,
    db: Session = Depends(get_db)
) -> Any:
    """
    Executes multiple algorithms on identical dataset for empirical comparison.
    """
    input_data = _resolve_input(req.dataset_id, req.custom_input, req.input_data, db)
    iters = req.repetitions if req.repetitions is not None else req.iterations

    try:
        result = benchmark_runner.compare_algorithms(
            algorithm_slugs=req.algorithm_slugs,
            input_data=input_data,
            iterations=iters,
            warmup_runs=req.warmup_runs
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Comparison failed: {str(e)}"
        )


@router.post("/step")
def get_execution_steps(req: VisualizerStepRequest) -> Any:
    """
    Executes algorithm in instrumented mode to record step-by-step snapshots,
    indices compared/swapped, and variables for interactive UI visualizer.
    """
    algo = registry.get(req.algorithm_slug)
    if not algo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Algorithm '{req.algorithm_slug}' not found in registry."
        )

    try:
        exec_res = algo.run_instrumented(req.input_data, max_steps=req.max_steps)
        return {
            "algorithm_slug": algo.slug,
            "algorithm_name": algo.name,
            "category": algo.category,
            "total_steps": len(exec_res.steps),
            "metrics": {
                "comparisons": exec_res.metrics.comparisons,
                "swaps": exec_res.metrics.swaps,
                "recursive_calls": exec_res.metrics.recursive_calls,
                "operations": exec_res.metrics.operations or (
                    exec_res.metrics.comparisons + exec_res.metrics.swaps + exec_res.metrics.recursive_calls
                ),
                "peak_memory_kb": getattr(exec_res.metrics, "peak_memory_kb", 0.0) or 0.0,
            },
            "steps": [s.to_dict() for s in exec_res.steps],
            "output": exec_res.output
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Step instrumentation failed: {str(e)}"
        )
