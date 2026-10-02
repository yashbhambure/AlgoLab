"""
FastAPI Main Application Entrypoint for Algorithm Benchmark & Recommendation System.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.core.database import engine, Base, SessionLocal
from app.seed.seed_data import seed_database
from app.api.v1 import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for startup and shutdown procedures."""
    # 1. Initialize tables
    Base.metadata.create_all(bind=engine)

    # 2. Seed database with DAA problems, algorithms, and test users if empty
    db = SessionLocal()
    try:
        seed_database(db)
    except Exception as e:
        print(f"[Warning] Seeding encountered exception: {e}")
    finally:
        db.close()

    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Academic DAA Laboratory, Empirical Benchmark Engine, and Intelligent MCDA Recommendation Platform",
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS for Vite React Frontend and API consumers
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"An unexpected server error occurred: {str(exc)}"}
    )

# Include API Router
app.include_router(api_router)


@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint for container orchestration and uptime monitoring."""
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }


@app.get("/", tags=["System"])
def root():
    """Root metadata endpoint."""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "description": "Welcome to the Intelligent Algorithm Benchmark & Recommendation System API.",
        "docs": "/docs",
        "api_v1": "/api/v1"
    }
