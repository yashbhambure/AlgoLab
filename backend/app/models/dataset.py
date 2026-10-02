"""
Dataset Database Model
"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False)
    problem_type = Column(String(100), nullable=False)
    data_type = Column(String(50), nullable=False)  # array, graph, string, knapsack_items, matrix, etc.
    size = Column(Integer, nullable=False)
    distribution = Column(String(100), default="random")  # random, sorted, reverse_sorted, nearly_sorted, duplicate_heavy, uniform, normal
    random_seed = Column(Integer, nullable=True)

    characteristics = Column(JSON, default=dict)  # min_val, max_val, sortedness, density, duplicate_rate, etc.
    data_payload = Column(JSON, nullable=False)   # The actual input data (reproducible)
    preview_sample = Column(JSON, nullable=True)  # First 10-20 elements for quick preview

    created_by_user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    benchmark_runs = relationship("BenchmarkRun", back_populates="dataset")
