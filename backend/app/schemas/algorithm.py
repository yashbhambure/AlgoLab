"""
Algorithm Pydantic Schemas
"""
from typing import List, Optional, Any, Dict
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AlgorithmBase(BaseModel):
    slug: str
    name: str
    category: str
    paradigm: str
    description: str
    best_case: str
    average_case: str
    worst_case: str
    space_complexity: str
    recurrence_relation: Optional[str] = None
    is_stable: bool = False
    is_in_place: bool = False
    is_adaptive: bool = False
    is_deterministic: bool = True
    advantages: List[str] = []
    disadvantages: List[str] = []
    suitable_cases: List[str] = []
    unsuitable_cases: List[str] = []


class AlgorithmCreate(AlgorithmBase):
    pseudocode: Optional[str] = None
    implementation_python: Optional[str] = None
    daa_concept_notes: Optional[str] = None


class AlgorithmResponse(AlgorithmBase):
    id: str
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class AlgorithmDetail(AlgorithmResponse):
    pseudocode: Optional[str] = None
    c_source_code: Optional[str] = None
    implementation_python: Optional[str] = None
    daa_concept_notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# Alias
AlgorithmDetailResponse = AlgorithmDetail


class AlgorithmCompareRequest(BaseModel):
    algorithm_ids: List[str]
    problem_id: Optional[str] = None


class AlgorithmCompareResponse(BaseModel):
    algorithms: List[AlgorithmDetailResponse]
    complexity_matrix: List[Dict[str, Any]]
    property_matrix: List[Dict[str, Any]]
    tradeoff_summary: Dict[str, Any]
