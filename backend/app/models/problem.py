"""
Problem and Algorithm-Problem Mapping Models
"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, ForeignKey, JSON, DateTime, Float
from sqlalchemy.orm import relationship
from app.core.database import Base


class Problem(Base):
    __tablename__ = "problems"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    slug = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(150), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    paradigm = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    input_format = Column(Text, nullable=False)
    output_format = Column(Text, nullable=False)
    constraints = Column(Text, nullable=True)
    data_type = Column(String(50), default="array")  # array, graph, string, knapsack_items, matrix, board
    example_input = Column(JSON, nullable=True)
    example_output = Column(JSON, nullable=True)
    daa_topics = Column(JSON, default=list)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    algorithm_mappings = relationship("AlgorithmProblemMapping", back_populates="problem", cascade="all, delete-orphan")
    benchmark_runs = relationship("BenchmarkRun", back_populates="problem")
    experiments = relationship("Experiment", back_populates="problem")
    recommendations = relationship("RecommendationRecord", back_populates="problem")


class AlgorithmProblemMapping(Base):
    __tablename__ = "algorithm_problem_mappings"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    algorithm_id = Column(String(36), ForeignKey("algorithms.id", ondelete="CASCADE"), nullable=False)
    problem_id = Column(String(36), ForeignKey("problems.id", ondelete="CASCADE"), nullable=False)
    suitability_score = Column(Float, default=1.0)
    notes = Column(Text, nullable=True)

    algorithm = relationship("Algorithm", back_populates="problem_mappings")
    problem = relationship("Problem", back_populates="algorithm_mappings")
