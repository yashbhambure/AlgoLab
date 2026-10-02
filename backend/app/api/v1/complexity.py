"""
Asymptotic Complexity Analysis, Problem Compatibility Groups, and Master Theorem Solver Endpoints.
"""
from typing import Any, List, Optional, Tuple
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.algorithm import Algorithm
from app.models.problem import Problem, AlgorithmProblemMapping
from app.complexity.master_theorem import MasterTheoremSolver
from app.complexity.big_o_analyzer import BigOAnalyzer
from app.complexity.asymptotic_comparator import AsymptoticComparator
from app.curriculum.curriculum_data import get_all_approved_algorithm_slugs, get_algorithm_curriculum_info
from app.schemas.complexity import (
    MasterTheoremRequest,
    MasterTheoremResponse,
    CurveFitRequest,
    CurveFitResponse,
    AlgorithmComplexityProfile,
    CompatibleComparisonGroup,
)

router = APIRouter(prefix="/complexity", tags=["Complexity Analysis"])


class AsymptoticCompareRequest(BaseModel):
    complexity_a: str = Field(..., example="O(n log n)")
    complexity_b: str = Field(..., example="O(n^2)")


@router.get("/compatible-groups", response_model=List[CompatibleComparisonGroup])
def get_compatible_algorithm_groups(
    curriculum_only: bool = Query(False, description="Filter only authoritative curriculum problem groups"),
    db: Session = Depends(get_db)
) -> Any:
    """
    Returns grouped compatible algorithms mapped to the same underlying problem.
    Only allows comparison between compatible algorithms (e.g., 0/1 Knapsack DP vs B&B,
    TSP DP vs B&B, Prim vs Kruskal, Dijkstra vs Bellman-Ford, Sort, Search).
    """
    approved_slugs = set(get_all_approved_algorithm_slugs())
    problems = db.query(Problem).order_by(Problem.category, Problem.name).all()

    groups: List[CompatibleComparisonGroup] = []

    for prob in problems:
        algos_in_problem = [m.algorithm for m in prob.algorithm_mappings if m.algorithm]
        if not algos_in_problem:
            continue

        # Check if this group belongs to the authoritative curriculum
        has_curriculum_algo = any(a.slug in approved_slugs for a in algos_in_problem)

        if curriculum_only and not has_curriculum_algo:
            continue

        profiles: List[AlgorithmComplexityProfile] = []
        for algo in algos_in_problem:
            curr_info = get_algorithm_curriculum_info(algo.slug)
            is_curr = curr_info is not None
            module_id = curr_info["module_id"] if curr_info else None
            recurrence = (curr_info.get("recurrence") if curr_info else None) or algo.recurrence_relation

            profiles.append(
                AlgorithmComplexityProfile(
                    slug=algo.slug,
                    name=algo.name,
                    category=algo.category,
                    paradigm=algo.paradigm,
                    is_curriculum=is_curr,
                    module_id=module_id,
                    best_case=algo.best_case,
                    average_case=algo.average_case,
                    worst_case=algo.worst_case,
                    space_complexity=algo.space_complexity,
                    recurrence_relation=recurrence,
                    is_stable=algo.is_stable,
                    is_in_place=algo.is_in_place,
                    description=algo.description,
                )
            )

        groups.append(
            CompatibleComparisonGroup(
                problem_slug=prob.slug,
                problem_name=prob.name,
                category=prob.category,
                is_curriculum=has_curriculum_algo,
                constraints=prob.constraints,
                algorithms=profiles,
            )
        )

    return groups


@router.get("/algorithms/{slug}", response_model=AlgorithmComplexityProfile)
def get_algorithm_complexity_profile(slug: str, db: Session = Depends(get_db)) -> Any:
    """
    Retrieve authoritative theoretical complexity metadata for a single algorithm.
    """
    algo = db.query(Algorithm).filter(Algorithm.slug == slug).first()
    if not algo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Algorithm with slug '{slug}' not found."
        )

    curr_info = get_algorithm_curriculum_info(algo.slug)
    is_curr = curr_info is not None
    module_id = curr_info["module_id"] if curr_info else None
    recurrence = (curr_info.get("recurrence") if curr_info else None) or algo.recurrence_relation

    return AlgorithmComplexityProfile(
        slug=algo.slug,
        name=algo.name,
        category=algo.category,
        paradigm=algo.paradigm,
        is_curriculum=is_curr,
        module_id=module_id,
        best_case=algo.best_case,
        average_case=algo.average_case,
        worst_case=algo.worst_case,
        space_complexity=algo.space_complexity,
        recurrence_relation=recurrence,
        is_stable=algo.is_stable,
        is_in_place=algo.is_in_place,
        description=algo.description,
    )


@router.post("/master-theorem", response_model=MasterTheoremResponse)
def solve_master_theorem(req: MasterTheoremRequest) -> Any:
    """
    Solves recurrence relation T(n) = a*T(n/b) + Theta(n^k * log^p(n))
    with step-by-step mathematical derivation.
    """
    try:
        res = MasterTheoremSolver.solve(
            a=req.a,
            b=req.b,
            k=req.k,
            p=req.p
        )
        return res
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/fit-big-o", response_model=CurveFitResponse)
def fit_empirical_big_o(req: CurveFitRequest) -> Any:
    """
    Fits empirical scaling data points (n, time) to theoretical complexity classes,
    calculating R^2, RMSE, and AIC.
    """
    try:
        points = [(p.n, p.time_ms) for p in req.data_points]
        res = BigOAnalyzer.fit_curve(points)
        return res
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Curve fitting failed: {str(e)}"
        )


@router.get("/hierarchy")
def get_complexity_hierarchy() -> Any:
    """Returns the canonical DAA asymptotic complexity growth order."""
    return AsymptoticComparator.get_full_hierarchy()


@router.post("/compare")
def compare_complexities(req: AsymptoticCompareRequest) -> Any:
    """Compares two asymptotic complexity classes."""
    return AsymptoticComparator.compare(req.complexity_a, req.complexity_b)

