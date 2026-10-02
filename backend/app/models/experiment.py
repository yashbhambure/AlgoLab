"""
Scaling Experiment Database Models
"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, JSON, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    problem_id = Column(String(36), ForeignKey("problems.id", ondelete="CASCADE"), nullable=False)

    algorithm_ids = Column(JSON, nullable=False)  # list of algorithm slugs or ids
    input_sizes = Column(JSON, nullable=False)    # e.g., [100, 500, 1000, 5000, 10000]
    dataset_distribution = Column(String(100), default="random")
    repetitions = Column(Integer, default=3)

    results_summary = Column(JSON, default=dict)
    asymptotic_fit_summary = Column(JSON, default=dict)
    conclusion_notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="experiments")
    problem = relationship("Problem", back_populates="experiments")
    results = relationship("ExperimentResult", back_populates="experiment", cascade="all, delete-orphan")


class ExperimentResult(Base):
    __tablename__ = "experiment_results"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    experiment_id = Column(String(36), ForeignKey("experiments.id", ondelete="CASCADE"), nullable=False)
    algorithm_id = Column(String(36), nullable=False)
    algorithm_name = Column(String(150), nullable=False)

    input_size = Column(Integer, nullable=False)
    mean_time_ms = Column(Float, nullable=False)
    memory_kb = Column(Float, default=0.0)
    std_dev_ms = Column(Float, default=0.0)
    operations_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    experiment = relationship("Experiment", back_populates="results")
