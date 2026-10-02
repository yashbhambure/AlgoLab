"""
Pydantic v2 Request & Response Schemas
"""
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token, TokenPayload
from app.schemas.algorithm import (
    AlgorithmResponse,
    AlgorithmDetailResponse,
    AlgorithmCompareRequest,
    AlgorithmCompareResponse
)
from app.schemas.problem import ProblemResponse, ProblemDetailResponse
from app.schemas.dataset import DatasetGenerateRequest, DatasetResponse, DatasetDetailResponse, CustomDatasetRequest
from app.schemas.benchmark import (
    BenchmarkRunRequest,
    BenchmarkRunResponse,
    BenchmarkResultResponse,
    BenchmarkComparisonResponse
)
from app.schemas.experiment import (
    ExperimentRunRequest,
    ExperimentResponse,
    ExperimentDetailResponse,
    AsymptoticFitModel
)
from app.schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
    ScoreBreakdown,
    RunnerUp
)
from app.schemas.complexity import (
    MasterTheoremRequest,
    MasterTheoremResponse,
    CurveFitRequest,
    CurveFitResponse
)

__all__ = [
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "Token",
    "TokenPayload",
    "AlgorithmResponse",
    "AlgorithmDetailResponse",
    "AlgorithmCompareRequest",
    "AlgorithmCompareResponse",
    "ProblemResponse",
    "ProblemDetailResponse",
    "DatasetGenerateRequest",
    "DatasetResponse",
    "DatasetDetailResponse",
    "CustomDatasetRequest",
    "BenchmarkRunRequest",
    "BenchmarkRunResponse",
    "BenchmarkResultResponse",
    "BenchmarkComparisonResponse",
    "ExperimentRunRequest",
    "ExperimentResponse",
    "ExperimentDetailResponse",
    "AsymptoticFitModel",
    "RecommendationRequest",
    "RecommendationResponse",
    "ScoreBreakdown",
    "RunnerUp",
    "MasterTheoremRequest",
    "MasterTheoremResponse",
    "CurveFitRequest",
    "CurveFitResponse",
]
