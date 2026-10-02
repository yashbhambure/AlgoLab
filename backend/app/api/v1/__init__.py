"""
API v1 Router Aggregator
"""
from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.algorithms import router as algorithms_router
from app.api.v1.problems import router as problems_router
from app.api.v1.datasets import router as datasets_router
from app.api.v1.benchmarks import router as benchmarks_router
from app.api.v1.complexity import router as complexity_router
from app.api.v1.recommendations import router as recommendations_router
from app.api.v1.experiments import router as experiments_router
from app.api.v1.curriculum import router as curriculum_router

api_router = APIRouter(prefix="/api/v1")

@api_router.get("/health", tags=["System"])
def api_v1_health_check():
    """Health check endpoint under API v1 prefix."""
    from app.config import settings
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }

api_router.include_router(auth_router)
api_router.include_router(curriculum_router)
api_router.include_router(algorithms_router)
api_router.include_router(problems_router)
api_router.include_router(datasets_router)
api_router.include_router(benchmarks_router)
api_router.include_router(complexity_router)
api_router.include_router(recommendations_router)
api_router.include_router(experiments_router)
