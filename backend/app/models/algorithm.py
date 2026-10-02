"""
Algorithm Database Model
"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Boolean, JSON, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base


class Algorithm(Base):
    __tablename__ = "algorithms"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    slug = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(150), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)  # Sorting, Searching, Graph, Greedy, Dynamic Programming, Divide and Conquer, Backtracking
    paradigm = Column(String(100), nullable=False, index=True)  # Divide and Conquer, Greedy, Dynamic Programming, Backtracking, Brute Force, Transform and Conquer, Decrease and Conquer
    description = Column(Text, nullable=False)
    pseudocode = Column(Text, nullable=True)
    implementation_python = Column(Text, nullable=True)

    # Asymptotic Complexities
    best_case = Column(String(50), nullable=False)  # e.g., O(n)
    average_case = Column(String(50), nullable=False)  # e.g., O(n log n)
    worst_case = Column(String(50), nullable=False)  # e.g., O(n^2)
    space_complexity = Column(String(50), nullable=False)  # e.g., O(1)
    recurrence_relation = Column(String(200), nullable=True)  # e.g., T(n) = 2T(n/2) + O(n)

    # Properties
    is_stable = Column(Boolean, default=False)
    is_in_place = Column(Boolean, default=False)
    is_adaptive = Column(Boolean, default=False)
    is_deterministic = Column(Boolean, default=True)

    # Detailed pedagogical attributes
    advantages = Column(JSON, default=list)
    disadvantages = Column(JSON, default=list)
    suitable_cases = Column(JSON, default=list)
    unsuitable_cases = Column(JSON, default=list)
    daa_concept_notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    problem_mappings = relationship("AlgorithmProblemMapping", back_populates="algorithm", cascade="all, delete-orphan")
    benchmark_results = relationship("BenchmarkResult", back_populates="algorithm")
