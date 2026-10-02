"""
Experiment Pydantic Schemas
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class ExperimentCreate(BaseModel):
    title: Optional[str] = "Scaling Experiment"
    name: Optional[str] = "Scaling Experiment"
    description: Optional[str] = None
    problem_id: str
    algorithm_ids: List[str]
    dataset_id: Optional[str] = None
    input_sizes: Optional[List[int]] = [50, 100, 250, 500, 1000]
    dataset_distribution: Optional[str] = "random"
    repetitions: Optional[int] = 3
    config: Optional[Dict[str, Any]] = None
    results: Optional[Dict[str, Any]] = None
    recommendations: Optional[Dict[str, Any]] = None
    is_public: Optional[bool] = True


class ExperimentRunRequest(BaseModel):
    name: str = "Scaling Experiment"
    problem_id: str
    algorithm_ids: List[str]
    input_sizes: List[int] = Field(default=[50, 100, 250, 500, 1000, 2500, 5000])
    distribution: str = "random"
    repetitions: int = Field(default=3, ge=1, le=10)
    data_config: Optional[Dict[str, Any]] = None


class ExperimentResultItem(BaseModel):
    algorithm_id: str
    algorithm_name: str
    input_size: int
    mean_time_ms: float
    memory_kb: float
    std_dev_ms: float
    operations_count: int


class AsymptoticFitModel(BaseModel):
    algorithm_id: str
    algorithm_name: str
    theoretical_complexity: str
    best_fit_model: str
    r_squared: float
    scaling_exponent: Optional[float] = None
    empirical_analysis: str


class ExperimentResponse(BaseModel):
    id: str
    name: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    problem_id: str
    problem_name: Optional[str] = None
    algorithm_ids: List[str]
    input_sizes: Optional[List[int]] = None
    dataset_distribution: Optional[str] = "random"
    repetitions: Optional[int] = 3
    created_at: Optional[datetime] = None
    results_summary: Optional[Dict[str, Any]] = None
    results: Optional[Dict[str, Any]] = None
    asymptotic_fit_summary: Optional[Any] = None
    recommendations: Optional[Dict[str, Any]] = None
    conclusion_notes: Optional[str] = None
    is_public: Optional[bool] = True

    model_config = ConfigDict(from_attributes=True)


class ExperimentDetail(ExperimentResponse):
    detailed_points: Optional[List[ExperimentResultItem]] = None
    config: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)


ExperimentDetailResponse = ExperimentDetail
