"""
Algorithm Registry and Educational Catalog Endpoints.
"""
from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.algorithm import Algorithm
from app.models.problem import Problem, AlgorithmProblemMapping
from app.schemas.algorithm import AlgorithmResponse, AlgorithmDetail
from app.algorithms.registry import registry
from app.algorithms.c_sources import get_c_source

router = APIRouter(prefix="/algorithms", tags=["Algorithms"])


@router.get("", response_model=List[AlgorithmResponse])
def list_algorithms(
    category: Optional[str] = Query(None, description="Filter by category (Sorting, Searching, etc.)"),
    paradigm: Optional[str] = Query(None, description="Filter by paradigm (Greedy, DP, etc.)"),
    problem_slug: Optional[str] = Query(None, description="Filter by compatible problem slug"),
    is_stable: Optional[bool] = Query(None, description="Filter by stability"),
    is_in_place: Optional[bool] = Query(None, description="Filter by in-place property"),
    db: Session = Depends(get_db)
) -> Any:
    """Retrieve all algorithms registered in the DAA Laboratory."""
    query = db.query(Algorithm)

    if category:
        category_clean = category.strip()
        category_alt = category_clean.replace("&", "and") if "&" in category_clean else category_clean.replace("and", "&")
        query = query.filter(
            or_(
                Algorithm.category.ilike(f"%{category_clean}%"),
                Algorithm.category.ilike(f"%{category_alt}%"),
                Algorithm.paradigm.ilike(f"%{category_clean}%"),
                Algorithm.paradigm.ilike(f"%{category_alt}%")
            )
        )
    if paradigm:
        paradigm_clean = paradigm.strip()
        paradigm_alt = paradigm_clean.replace("&", "and") if "&" in paradigm_clean else paradigm_clean.replace("and", "&")
        query = query.filter(
            or_(
                Algorithm.paradigm.ilike(f"%{paradigm_clean}%"),
                Algorithm.paradigm.ilike(f"%{paradigm_alt}%"),
                Algorithm.category.ilike(f"%{paradigm_clean}%"),
                Algorithm.category.ilike(f"%{paradigm_alt}%")
            )
        )
    if is_stable is not None:
        query = query.filter(Algorithm.is_stable == is_stable)
    if is_in_place is not None:
        query = query.filter(Algorithm.is_in_place == is_in_place)
    if problem_slug:
        problem = db.query(Problem).filter(Problem.slug == problem_slug).first()
        if problem:
            query = query.join(AlgorithmProblemMapping).filter(AlgorithmProblemMapping.problem_id == problem.id)

    algorithms = query.order_by(Algorithm.category, Algorithm.name).all()
    return algorithms


@router.get("/{slug}", response_model=AlgorithmDetail)
def get_algorithm_by_slug(slug: str, db: Session = Depends(get_db)) -> Any:
    """Retrieve in-depth theoretical and implementation details for an algorithm."""
    algo = db.query(Algorithm).filter(Algorithm.slug == slug).first()
    if not algo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Algorithm with slug '{slug}' not found."
        )
    algo.c_source_code = get_c_source(algo.slug)
    return algo


@router.get("/{slug}/code")
def get_algorithm_code(slug: str, db: Session = Depends(get_db)) -> Any:
    """Retrieve multi-language source code implementations for an algorithm."""
    algo = db.query(Algorithm).filter(Algorithm.slug == slug).first()
    if not algo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Algorithm with slug '{slug}' not found."
        )

    return {
        "slug": algo.slug,
        "name": algo.name,
        "pseudocode": algo.pseudocode,
        "c_source_code": get_c_source(algo.slug),
        "implementation_python": algo.implementation_python,
        "daa_concept_notes": algo.daa_concept_notes
    }
