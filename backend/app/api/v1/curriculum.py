"""
Curriculum API Router
Exposes the 7 authoritative DAA Curriculum modules, topics, theoretical classes, and algorithm mappings.
"""
from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any, List
from app.curriculum.curriculum_data import (
    CURRICULUM_MODULES,
    get_curriculum_modules,
    get_curriculum_module,
    get_all_approved_algorithm_slugs
)

router = APIRouter(prefix="/curriculum", tags=["Curriculum"])


@router.get("/modules", response_model=List[Dict[str, Any]])
def list_curriculum_modules():
    """Retrieve all 7 Authoritative DAA Curriculum modules."""
    return get_curriculum_modules()


@router.get("/modules/{module_id}", response_model=Dict[str, Any])
def get_module_by_id(module_id: str):
    """Retrieve details for a specific curriculum module (1 to 7 or slug)."""
    module = get_curriculum_module(module_id)
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"DAA Curriculum Module '{module_id}' not found. Valid modules are 1 through 7 or their respective slugs."
        )
    return module


@router.get("/theoretical", response_model=List[Dict[str, Any]])
def get_theoretical_modules():
    """Retrieve Module 6 (P and NP) and Module 7 (NP-Hard and NP-Complete) with theoretical foundations."""
    return [m for m in CURRICULUM_MODULES if m["module_id"] in (6, 7)]


@router.get("/approved-algorithms", response_model=List[str])
def list_approved_algorithm_slugs():
    """Returns the whitelist of all algorithm slugs explicitly approved in the 7 DAA modules."""
    return get_all_approved_algorithm_slugs()
