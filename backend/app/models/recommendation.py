"""
Recommendation Record Database Model
"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, JSON, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class RecommendationRecord(Base):
    __tablename__ = "recommendations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    problem_id = Column(String(36), ForeignKey("problems.id", ondelete="CASCADE"), nullable=False)
    dataset_id = Column(String(36), ForeignKey("datasets.id", ondelete="SET NULL"), nullable=True)

    input_size = Column(Integer, nullable=False)
    input_characteristics = Column(JSON, default=dict)
    optimization_objective = Column(String(100), default="speed")  # speed, memory, scalability, simplicity, balanced

    # Outcome
    recommended_algorithm_id = Column(String(36), nullable=False)
    recommended_algorithm_name = Column(String(150), nullable=False)
    confidence_score = Column(Float, nullable=False)  # 0.0 - 100.0 %

    # Explainability Data
    explanation_points = Column(JSON, default=list)
    scores_breakdown = Column(JSON, default=dict)
    runner_ups = Column(JSON, default=list)
    theoretical_analysis = Column(JSON, default=dict)
    benchmark_evidence = Column(JSON, default=dict)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="recommendations")
    problem = relationship("Problem", back_populates="recommendations")
