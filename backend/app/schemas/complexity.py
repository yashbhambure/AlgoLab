"""
Complexity Analysis Pydantic Schemas
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class MasterTheoremRequest(BaseModel):
    a: float = Field(..., ge=1, description="Number of subproblems a >= 1")
    b: float = Field(..., gt=1, description="Subproblem size factor b > 1")
    k: float = Field(..., ge=0, description="Exponent k in f(n) = O(n^k)")
    p: float = Field(default=0.0, description="Exponent p in log^p(n)")


class MasterTheoremResponse(BaseModel):
    a: Optional[float] = None
    b: Optional[float] = None
    k: Optional[float] = None
    p: Optional[float] = 0.0
    critical_exponent: float
    case: Optional[str] = None
    case_number: int
    complexity: Optional[str] = None
    latex: Optional[str] = None
    regularity_satisfied: Optional[bool] = True
    explanation: Optional[str] = None
    steps: Optional[List[str]] = []
    recurrence_form: Optional[str] = None
    case_description: Optional[str] = None
    condition_check: Optional[str] = None
    asymptotic_solution: Optional[str] = None
    step_by_step_proof: Optional[List[str]] = None


class DataPointItem(BaseModel):
    n: float
    time_ms: float


class CurveFitRequest(BaseModel):
    data_points: Optional[List[DataPointItem]] = None
    input_sizes: Optional[List[int]] = None
    measured_times_ms: Optional[List[float]] = None


class ModelFitResult(BaseModel):
    complexity: Optional[str] = None
    name: Optional[str] = None
    model_name: Optional[str] = None
    coefficient: Optional[float] = None
    r_squared: float
    rmse: float
    aic: Optional[float] = None
    predicted_curve: Optional[List[Dict[str, Any]]] = None
    coefficients: Optional[Dict[str, float]] = None


class CurveFitResponse(BaseModel):
    best_fit_complexity: Optional[str] = None
    best_fit_name: Optional[str] = None
    best_fit_model: Optional[str] = None
    best_r_squared: float
    fits: Optional[List[ModelFitResult]] = None
    all_models: Optional[List[ModelFitResult]] = None
    interpretation: Optional[str] = None


class AlgorithmComplexityProfile(BaseModel):
    slug: str
    name: str
    category: str
    paradigm: str
    is_curriculum: bool
    module_id: Optional[int] = None
    best_case: str
    average_case: str
    worst_case: str
    space_complexity: str
    recurrence_relation: Optional[str] = None
    is_stable: Optional[bool] = False
    is_in_place: Optional[bool] = False
    description: Optional[str] = None
    theoretical_vs_empirical_note: str = (
        "Theoretical bounds represent mathematical asymptotic limits. "
        "Empirical benchmarks measure wall-clock nanoseconds on physical hardware, "
        "which include cache, OS scheduling, and branch prediction effects."
    )


class CompatibleComparisonGroup(BaseModel):
    problem_slug: str
    problem_name: str
    category: str
    is_curriculum: bool
    constraints: Optional[str] = None
    algorithms: List[AlgorithmComplexityProfile]

