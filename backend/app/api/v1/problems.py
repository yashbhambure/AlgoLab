"""
Canonical DAA Problem Definition Endpoints.
"""
from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.problem import Problem
from app.schemas.problem import ProblemResponse, ProblemDetail

router = APIRouter(prefix="/problems", tags=["Problems"])


@router.get("", response_model=List[ProblemResponse])
def list_problems(
    category: Optional[str] = Query(None, description="Filter by problem category"),
    db: Session = Depends(get_db)
) -> Any:
    """List all canonical computational problems in the DAA Laboratory."""
    query = db.query(Problem)
    if category:
        query = query.filter(Problem.category.ilike(f"%{category}%"))
    problems = query.order_by(Problem.category, Problem.name).all()
    return problems


@router.get("/{slug}", response_model=ProblemDetail)
def get_problem_by_slug(slug: str, db: Session = Depends(get_db)) -> Any:
    """Retrieve detailed problem specification, compatible algorithms, and sample datasets."""
    problem = db.query(Problem).filter(Problem.slug == slug).first()
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Problem with slug '{slug}' not found."
        )

    # Format applicable algorithms
    applicable = []
    for mapping in problem.algorithm_mappings:
        algo = mapping.algorithm
        if algo:
            applicable.append({
                "id": algo.id,
                "slug": algo.slug,
                "name": algo.name,
                "category": algo.category,
                "paradigm": algo.paradigm,
                "time_complexity_average": algo.average_case,
                "space_complexity": algo.space_complexity,
                "suitability_score": mapping.suitability_score,
                "notes": mapping.notes
            })

    res = ProblemDetail.model_validate(problem)
    res.applicable_algorithms = applicable
    return res
