"""
Problem Pydantic Schemas
"""
from typing import List, Optional, Any, Dict
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ProblemBase(BaseModel):
    slug: str
    name: str
    category: str
    paradigm: str
    description: str
    input_format: str
    output_format: str
    constraints: Optional[str] = None
    data_type: str = "array"
    daa_topics: List[str] = []


class ProblemCreate(ProblemBase):
    example_input: Optional[Any] = None
    example_output: Optional[Any] = None


class ProblemResponse(ProblemBase):
    id: str
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ProblemDetail(ProblemResponse):
    example_input: Optional[Any] = None
    example_output: Optional[Any] = None
    applicable_algorithms: List[Dict[str, Any]] = []

    model_config = ConfigDict(from_attributes=True)


ProblemDetailResponse = ProblemDetail
