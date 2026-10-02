"""
Dataset Pydantic Schemas
"""
from typing import Optional, Any, Dict, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class DatasetGenerateRequest(BaseModel):
    problem_type: str = "sorting"
    data_type: str = "array"
    size: int = Field(default=100, ge=2, le=1000000)
    distribution: str = "random"
    min_val: Optional[int] = 1
    max_val: Optional[int] = 1000
    random_seed: Optional[int] = None
    target_value: Optional[Any] = None

    num_vertices: Optional[int] = 10
    num_edges: Optional[int] = 20
    is_directed: Optional[bool] = False
    is_weighted: Optional[bool] = True
    graph_density: Optional[str] = "medium"
    allow_negative_weights: Optional[bool] = False

    knapsack_capacity: Optional[int] = 50
    string_pattern_type: Optional[str] = "random_dna"
    matrix_dims: Optional[List[int]] = None


class CustomDatasetRequest(BaseModel):
    name: str
    problem_type: str = "sorting"
    data_type: str = "array"
    raw_data: Any


class DatasetCreate(BaseModel):
    name: str
    problem_type: str = "sorting"
    data_type: str = "array"
    size: int = 100
    distribution: str = "random"
    random_seed: Optional[int] = None
    characteristics: Dict[str, Any] = {}
    data_payload: Any
    preview_sample: Optional[Any] = None


class DatasetResponse(BaseModel):
    id: str
    name: str
    problem_type: str
    data_type: str
    size: int
    distribution: str
    random_seed: Optional[int] = None
    characteristics: Dict[str, Any] = {}
    preview_sample: Optional[Any] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class DatasetDetail(DatasetResponse):
    data_payload: Any

    model_config = ConfigDict(from_attributes=True)


DatasetDetailResponse = DatasetDetail
