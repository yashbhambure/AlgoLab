"""
Custom Exception Classes for the Application
"""
from fastapi import HTTPException, status


class AlgorithmNotFoundError(HTTPException):
    def __init__(self, algorithm_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Algorithm '{algorithm_id}' not found in registry"
        )


class ProblemNotFoundError(HTTPException):
    def __init__(self, problem_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Problem '{problem_id}' not found in registry"
        )


class BenchmarkExecutionError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Benchmark execution failed: {detail}"
        )


class BenchmarkTimeoutError(HTTPException):
    def __init__(self, algorithm_name: str, timeout: float):
        super().__init__(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail=f"Algorithm '{algorithm_name}' timed out after exceeding {timeout}s safety limit"
        )


class InvalidInputDatasetError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid input dataset: {detail}"
        )
