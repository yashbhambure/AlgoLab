"""
Benchmark Run and Benchmark Result Database Models
"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, JSON, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class BenchmarkRun(Base):
    __tablename__ = "benchmark_runs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    problem_id = Column(String(36), ForeignKey("problems.id", ondelete="CASCADE"), nullable=False)
    dataset_id = Column(String(36), ForeignKey("datasets.id", ondelete="SET NULL"), nullable=True)

    status = Column(String(50), default="completed")  # running, completed, failed, cancelled
    repetitions = Column(Integer, default=5)
    warmup_runs = Column(Integer, default=2)
    hardware_info = Column(JSON, default=dict)
    total_duration_ms = Column(Float, default=0.0)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="benchmark_runs")
    problem = relationship("Problem", back_populates="benchmark_runs")
    dataset = relationship("Dataset", back_populates="benchmark_runs")
    results = relationship("BenchmarkResult", back_populates="benchmark_run", cascade="all, delete-orphan")


class BenchmarkResult(Base):
    __tablename__ = "benchmark_results"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    benchmark_run_id = Column(String(36), ForeignKey("benchmark_runs.id", ondelete="CASCADE"), nullable=False)
    algorithm_id = Column(String(36), ForeignKey("algorithms.id", ondelete="CASCADE"), nullable=False)
    algorithm_name = Column(String(150), nullable=False)

    input_size = Column(Integer, nullable=False)

    # Measured Timings (in milliseconds)
    min_time_ms = Column(Float, nullable=False)
    max_time_ms = Column(Float, nullable=False)
    mean_time_ms = Column(Float, nullable=False)
    median_time_ms = Column(Float, nullable=False)
    std_dev_time_ms = Column(Float, default=0.0)

    # Memory Tracking
    memory_peak_kb = Column(Float, default=0.0)
    memory_allocated_kb = Column(Float, default=0.0)

    # Operation Counters
    comparisons_count = Column(Integer, default=0)
    swaps_count = Column(Integer, default=0)
    recursive_calls_count = Column(Integer, default=0)
    operations_count = Column(Integer, default=0)

    raw_execution_times = Column(JSON, default=list)  # individual run times in ms
    status = Column(String(50), default="success")    # success, timeout, error
    error_message = Column(Text, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    benchmark_run = relationship("BenchmarkRun", back_populates="results")
    algorithm = relationship("Algorithm", back_populates="benchmark_results")
