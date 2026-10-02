"""
Recommendation Pydantic Schemas
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class RecommendationRequest(BaseModel):
    problem_id: str
    input_size: int = Field(default=1000, ge=1)
    dataset_id: Optional[str] = None
    input_characteristics: Dict[str, Any] = Field(default_factory=dict)
    optimization_objective: str = Field(
        default="speed",
        description="speed, memory, scalability, simplicity, balanced"
    )
    weights_override: Optional[Dict[str, float]] = None
    require_stability: Optional[bool] = False
    require_in_place: Optional[bool] = False
    include_benchmark_run: Optional[bool] = True


class ScoreBreakdown(BaseModel):
    theoretical_complexity_score: float
    empirical_performance_score: float
    space_efficiency_score: float
    input_suitability_score: float
    constraint_compatibility_score: float
    total_composite_score: float


class RunnerUp(BaseModel):
    algorithm_id: str
    algorithm_name: str
    total_score: float
    confidence_relative: float
    why_not_first: str
    trade_off_pros: List[str] = []
    trade_off_cons: List[str] = []


class RecommendationResponse(BaseModel):
    id: Optional[str] = None
    problem_id: str
    problem_name: str
    input_size: int
    optimization_objective: str
    input_characteristics_summary: Dict[str, Any]

    # Selected Algorithm
    recommended_algorithm_id: str
    recommended_algorithm_name: str
    recommended_algorithm_paradigm: str
    confidence_score: float  # Percentage (e.g. 92.4%)

    # Explainability Data
    why_recommended_points: List[str]
    scores_breakdown: Dict[str, ScoreBreakdown]
    runner_ups: List[RunnerUp]

    theoretical_analysis: Dict[str, Any]
    benchmark_evidence: Optional[Dict[str, Any]] = None

    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
