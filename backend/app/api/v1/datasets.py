"""
Dataset Management and Synthetic Data Generator Endpoints.
"""
import random
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_optional_user
from app.models.dataset import Dataset
from app.models.problem import Problem
from app.models.user import User
from app.schemas.dataset import DatasetResponse, DatasetDetail, DatasetGenerateRequest, CustomDatasetRequest
from app.benchmark.input_generators import generate_problem_input

router = APIRouter(prefix="/datasets", tags=["Datasets"])


@router.get("", response_model=List[DatasetResponse])
def list_datasets(
    problem_type: Optional[str] = Query(None, description="Filter by problem type"),
    data_type: Optional[str] = Query(None, description="Filter by data type"),
    db: Session = Depends(get_db)
) -> Any:
    """List standard and generated benchmark datasets."""
    query = db.query(Dataset)
    if problem_type:
        query = query.filter(Dataset.problem_type.ilike(f"%{problem_type}%"))
    if data_type:
        query = query.filter(Dataset.data_type == data_type)
    return query.order_by(Dataset.created_at.desc()).all()


@router.get("/{dataset_id}", response_model=DatasetDetail)
def get_dataset(dataset_id: str, db: Session = Depends(get_db)) -> Any:
    """Retrieve full dataset payload."""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataset with ID {dataset_id} not found."
        )
    return dataset


@router.post("/generate", response_model=DatasetDetail)
def generate_synthetic_dataset(
    req: DatasetGenerateRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
) -> Any:
    """
    Generates synthetic academic datasets tailored to algorithmic stress-testing
    (e.g., nearly-sorted, adversarial, dense/sparse graphs, integer ranges).
    """
    n = req.size
    min_v = req.min_val if req.min_val is not None else 1
    max_v = req.max_val if req.max_val is not None else 1000
    dist = req.distribution.lower()
    data_type = req.data_type
    raw_data: Any = None

    prob_type_clean = req.problem_type.lower().strip()
    if prob_type_clean in (
        "0-1-knapsack-problem", "knapsack", "traveling-salesman-problem", "tsp",
        "minimum-spanning-tree", "mst", "single-source-shortest-path", "sssp",
        "all-pairs-shortest-path", "apsp", "n-queens-problem", "n-queens",
        "subset-sum-problem", "subset-sum", "hamiltonian-cycle-problem", "hamiltonian-cycle",
        "matrix-multiplication-problem", "strassen", "defective-chessboard-problem",
        "max-min-problem", "fractional-knapsack-problem", "job-sequencing-problem",
        "optimal-merge-patterns-problem", "optimal-storage-tapes-problem",
        "optimal-bst-problem", "multistage-graph-problem", "reliability-design-problem"
    ):
        raw_data = generate_problem_input(prob_type_clean, size=n, distribution=dist)
        if "graph" in prob_type_clean or "tree" in prob_type_clean:
            data_type = "graph"
        elif "knapsack" in prob_type_clean:
            data_type = "knapsack"
        elif "matrix" in prob_type_clean or "chessboard" in prob_type_clean:
            data_type = "matrix"
        elif "queens" in prob_type_clean or "subset" in prob_type_clean:
            data_type = "board" if "queens" in prob_type_clean else "array"
        else:
            data_type = "object"
    elif req.problem_type == "sorting" or data_type == "array":
        raw_data = generate_sorting_input(size=n, distribution=dist, min_val=min_v, max_val=max_v)
        data_type = "array"
    elif req.problem_type == "searching":
        raw_data = generate_searching_input(size=n)
        data_type = "array"
    elif req.problem_type == "graph" or data_type == "graph":
        raw_data = generate_mst_input(num_vertices=min(n, 100))
        data_type = "graph"
    elif req.problem_type == "knapsack" or data_type == "knapsack":
        raw_data = generate_knapsack_input(num_items=n)
        data_type = "knapsack"
    elif data_type == "matrix":
        dim = int(n ** 0.5)
        raw_data = generate_strassen_input(power_of_two_dim=dim)
        data_type = "matrix"
    elif data_type == "string":
        bases = ["A", "C", "G", "T"]
        s1 = "".join(random.choice(bases) for _ in range(n))
        s2 = "".join(random.choice(bases) for _ in range(n))
        raw_data = {"str1": s1, "str2": s2}
        data_type = "string"
    else:
        raw_data = generate_sorting_input(size=n, distribution=dist, min_val=min_v, max_val=max_v)
        data_type = "array"

    # Preview sample (first 10 elements)
    preview = raw_data[:10] if isinstance(raw_data, list) else None

    dataset = Dataset(
        name=f"Generated {req.problem_type.title()} ({dist.title()}, N={n})",
        problem_type=req.problem_type,
        data_type=data_type,
        size=n,
        distribution=dist,
        random_seed=req.random_seed,
        characteristics={
            "size": n,
            "min_val": min_v,
            "max_val": max_v,
            "distribution": dist
        },
        data_payload=raw_data,
        preview_sample=preview,
        created_by_user_id=current_user.id if current_user else None
    )

    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    return dataset


@router.post("/custom", response_model=DatasetDetail)
def create_custom_dataset(
    req: CustomDatasetRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
) -> Any:
    """Upload or provide custom dataset payload."""
    raw = req.raw_data
    size = len(raw) if isinstance(raw, list) else 100
    preview = raw[:10] if isinstance(raw, list) else None

    dataset = Dataset(
        name=req.name,
        problem_type=req.problem_type,
        data_type=req.data_type,
        size=size,
        distribution="custom",
        characteristics={"size": size, "custom": True},
        data_payload=raw,
        preview_sample=preview,
        created_by_user_id=current_user.id if current_user else None
    )
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    return dataset
