"""
Intelligent Algorithm Recommendation and Decision Tree Endpoints.
"""
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.recommendation.engine import RecommendationEngine
from app.recommendation.decision_tree import AlgorithmDecisionTree
from app.models.dataset import Dataset
from app.models.problem import Problem
from app.models.algorithm import Algorithm

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


class RecommendationEvaluateRequest(BaseModel):
    problem_slug: Optional[str] = Field(None, description="Problem slug to fetch candidate algorithms")
    candidate_slugs: Optional[List[str]] = Field(None, description="Explicit list of algorithm slugs")
    dataset_id: Optional[str] = Field(None, description="Dataset ID to inspect data characteristics")
    custom_input: Optional[Any] = Field(None, description="Direct custom input dataset")
    empirical_results: Optional[List[Dict[str, Any]]] = Field(None, description="Prior benchmark run results")
    objective: str = Field("balanced", description="Optimization objective: speed, memory, stability, balanced")
    require_stable: bool = Field(False, description="Strict stability constraint")
    require_in_place: bool = Field(False, description="Strict in-place constraint")
    custom_weights: Optional[Dict[str, float]] = Field(None, description="Custom MCDA criteria weights")


class DecisionTreeTraverseRequest(BaseModel):
    answers: Dict[str, str] = Field(..., description="Mapping of question node IDs to selected choices")


@router.post("/evaluate")
def evaluate_recommendations(
    req: RecommendationEvaluateRequest,
    db: Session = Depends(get_db)
) -> Any:
    """
    Evaluates candidate algorithms using Multi-Criteria Decision Analysis (MCDA),
    incorporating theoretical complexities, empirical benchmark metrics, input dataset
    characteristics, and user constraints.
    """
    candidate_slugs = req.candidate_slugs or []

    # If problem_slug provided and candidate_slugs empty, resolve from database
    if not candidate_slugs and req.problem_slug:
        problem = db.query(Problem).filter(Problem.slug == req.problem_slug).first()
        if problem and problem.algorithm_mappings:
            candidate_slugs = [mapping.algorithm.slug for mapping in problem.algorithm_mappings if mapping.algorithm]

    if not candidate_slugs:
        # Default to sorting algorithms if none provided
        candidate_slugs = [
            "bubble-sort", "selection-sort", "insertion-sort",
            "merge-sort", "quick-sort", "heap-sort", "counting-sort", "radix-sort"
        ]

    # Resolve input data
    input_data = req.custom_input
    if input_data is None and req.dataset_id is not None:
        ds = db.query(Dataset).filter(Dataset.id == req.dataset_id).first()
        if ds:
            input_data = ds.data_payload

    result = RecommendationEngine.recommend(
        candidate_slugs=candidate_slugs,
        input_data=input_data,
        empirical_results=req.empirical_results,
        objective=req.objective,
        require_stable=req.require_stable,
        require_in_place=req.require_in_place,
        custom_weights=req.custom_weights
    )

    return result


@router.get("/decision-tree")
def get_decision_tree() -> Any:
    """Returns the full DAA interactive decision tree structure."""
    return AlgorithmDecisionTree.get_tree()


@router.post("/decision-tree/traverse")
def traverse_decision_tree(req: DecisionTreeTraverseRequest) -> Any:
    """Traverses decision tree given user responses and returns next step or recommended algorithm."""
    return AlgorithmDecisionTree.traverse(req.answers)
