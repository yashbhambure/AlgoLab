"""
Strassen's Matrix Multiplication Implementation (Divide and Conquer O(n^2.8074))
"""
from typing import Dict, Any, List
from app.algorithms.base import BaseAlgorithm, ExecutionMetrics, ExecutionStep, AlgorithmExecutionResult


class StrassenMatrixMultiplication(BaseAlgorithm):
    slug = "strassen-matrix-multiplication"
    name = "Strassen's Matrix Multiplication"
    category = "Divide and Conquer"
    paradigm = "Divide and Conquer"

    def run(self, input_data: Any) -> Dict[str, Any]:
        if isinstance(input_data, dict):
            A = input_data.get("matrix_a", [])
            B = input_data.get("matrix_b", [])
        else:
            A, B = input_data

        n = len(A)
        if n == 0:
            return {"result_matrix": [], "dimension": 0}

        C = self._strassen(A, B, threshold=32)
        return {
            "result_matrix": C,
            "dimension": n
        }

    def _add(self, A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
        return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

    def _sub(self, A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
        return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

    def _standard_multiply(self, A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
        n = len(A)
        C = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for k in range(n):
                for j in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def _strassen(self, A: List[List[float]], B: List[List[float]], threshold: int = 32) -> List[List[float]]:
        n = len(A)
        if n <= threshold or (n & (n - 1)) != 0:  # Base case or non-power-of-2
            return self._standard_multiply(A, B)

        mid = n // 2

        # Partition A and B into 4 quadrants
        A11 = [row[:mid] for row in A[:mid]]
        A12 = [row[mid:] for row in A[:mid]]
        A21 = [row[:mid] for row in A[mid:]]
        A22 = [row[mid:] for row in A[mid:]]

        B11 = [row[:mid] for row in B[:mid]]
        B12 = [row[mid:] for row in B[:mid]]
        B21 = [row[:mid] for row in B[mid:]]
        B22 = [row[mid:] for row in B[mid:]]

        # 7 Strassen Products
        M1 = self._strassen(self._add(A11, A22), self._add(B11, B22), threshold)
        M2 = self._strassen(self._add(A21, A22), B11, threshold)
        M3 = self._strassen(A11, self._sub(B12, B22), threshold)
        M4 = self._strassen(A22, self._sub(B21, B11), threshold)
        M5 = self._strassen(self._add(A11, A12), B22, threshold)
        M6 = self._strassen(self._sub(A21, A11), self._add(B11, B12), threshold)
        M7 = self._strassen(self._sub(A12, A22), self._add(B21, B22), threshold)

        # Compute output quadrants
        C11 = self._add(self._sub(self._add(M1, M4), M5), M7)
        C12 = self._add(M3, M5)
        C21 = self._add(M2, M4)
        C22 = self._add(self._add(self._sub(M1, M2), M3), M6)

        # Assemble result matrix
        C = []
        for i in range(mid):
            C.append(C11[i] + C12[i])
        for i in range(mid):
            C.append(C21[i] + C22[i])

        return C

    def run_instrumented(self, input_data: Any, max_steps: int = 500) -> AlgorithmExecutionResult:
        if isinstance(input_data, dict):
            A = input_data.get("matrix_a", [])
            B = input_data.get("matrix_b", [])
        elif isinstance(input_data, (list, tuple)) and len(input_data) >= 2:
            A, B = input_data[0], input_data[1]
        else:
            A, B = [], []

        metrics = ExecutionMetrics()
        steps: List[ExecutionStep] = []
        step_id = [0]
        n = len(A)

        if n == 0 or len(B) == 0:
            return AlgorithmExecutionResult(
                algorithm_slug=self.slug,
                output={"result_matrix": [], "dimension": 0},
                metrics=metrics,
                steps=steps
            )

        steps.append(ExecutionStep(
            step_id=step_id[0],
            action="init",
            state_snapshot={"matrix_a": A, "matrix_b": B, "dimension": n},
            description=f"Initialized Strassen's Matrix Multiplication on {n}x{n} matrices."
        ))
        step_id[0] += 1

        def _strassen_instrumented(mat_a: List[List[float]], mat_b: List[List[float]], depth: int = 0) -> List[List[float]]:
            metrics.recursive_calls += 1
            metrics.operations += 1
            sz = len(mat_a)

            # Base case: 1x1 or standard multiplication for small sizes
            if sz == 1:
                val = mat_a[0][0] * mat_b[0][0]
                metrics.operations += 1
                return [[val]]

            if (sz & (sz - 1)) != 0:
                # Non-power-of-2 fallback
                res = self._standard_multiply(mat_a, mat_b)
                metrics.operations += sz ** 3
                return res

            mid = sz // 2

            # Partition into 4 quadrants
            A11 = [row[:mid] for row in mat_a[:mid]]
            A12 = [row[mid:] for row in mat_a[:mid]]
            A21 = [row[:mid] for row in mat_a[mid:]]
            A22 = [row[mid:] for row in mat_a[mid:]]

            B11 = [row[:mid] for row in mat_b[:mid]]
            B12 = [row[mid:] for row in mat_b[:mid]]
            B21 = [row[:mid] for row in mat_b[mid:]]
            B22 = [row[mid:] for row in mat_b[mid:]]

            if len(steps) < max_steps:
                steps.append(ExecutionStep(
                    step_id=step_id[0],
                    action="partition",
                    state_snapshot={
                        "depth": depth,
                        "size": sz,
                        "quadrants": {
                            "A11": A11, "A12": A12, "A21": A21, "A22": A22,
                            "B11": B11, "B12": B12, "B21": B21, "B22": B22
                        }
                    },
                    description=f"Partitioned {sz}x{sz} matrices into four {mid}x{mid} sub-quadrants (A11..A22, B11..B22)."
                ))
                step_id[0] += 1

            # 7 Strassen Multiplications
            # M1 = (A11 + A22) * (B11 + B22)
            s_a1 = self._add(A11, A22)
            s_b1 = self._add(B11, B22)
            M1 = _strassen_instrumented(s_a1, s_b1, depth + 1)
            metrics.operations += 2 * (mid ** 2)
            if len(steps) < max_steps:
                steps.append(ExecutionStep(
                    step_id=step_id[0],
                    action="compute_m1",
                    state_snapshot={"M1": M1, "depth": depth},
                    description=f"Computed Strassen product M1 = (A11 + A22) * (B11 + B22)."
                ))
                step_id[0] += 1

            # M2 = (A21 + A22) * B11
            s_a2 = self._add(A21, A22)
            M2 = _strassen_instrumented(s_a2, B11, depth + 1)
            metrics.operations += (mid ** 2)
            if len(steps) < max_steps:
                steps.append(ExecutionStep(
                    step_id=step_id[0],
                    action="compute_m2",
                    state_snapshot={"M2": M2, "depth": depth},
                    description=f"Computed Strassen product M2 = (A21 + A22) * B11."
                ))
                step_id[0] += 1

            # M3 = A11 * (B12 - B22)
            s_b3 = self._sub(B12, B22)
            M3 = _strassen_instrumented(A11, s_b3, depth + 1)
            metrics.operations += (mid ** 2)
            if len(steps) < max_steps:
                steps.append(ExecutionStep(
                    step_id=step_id[0],
                    action="compute_m3",
                    state_snapshot={"M3": M3, "depth": depth},
                    description=f"Computed Strassen product M3 = A11 * (B12 - B22)."
                ))
                step_id[0] += 1

            # M4 = A22 * (B21 - B11)
            s_b4 = self._sub(B21, B11)
            M4 = _strassen_instrumented(A22, s_b4, depth + 1)
            metrics.operations += (mid ** 2)
            if len(steps) < max_steps:
                steps.append(ExecutionStep(
                    step_id=step_id[0],
                    action="compute_m4",
                    state_snapshot={"M4": M4, "depth": depth},
                    description=f"Computed Strassen product M4 = A22 * (B21 - B11)."
                ))
                step_id[0] += 1

            # M5 = (A11 + A12) * B22
            s_a5 = self._add(A11, A12)
            M5 = _strassen_instrumented(s_a5, B22, depth + 1)
            metrics.operations += (mid ** 2)
            if len(steps) < max_steps:
                steps.append(ExecutionStep(
                    step_id=step_id[0],
                    action="compute_m5",
                    state_snapshot={"M5": M5, "depth": depth},
                    description=f"Computed Strassen product M5 = (A11 + A12) * B22."
                ))
                step_id[0] += 1

            # M6 = (A21 - A11) * (B11 + B12)
            s_a6 = self._sub(A21, A11)
            s_b6 = self._add(B11, B12)
            M6 = _strassen_instrumented(s_a6, s_b6, depth + 1)
            metrics.operations += 2 * (mid ** 2)
            if len(steps) < max_steps:
                steps.append(ExecutionStep(
                    step_id=step_id[0],
                    action="compute_m6",
                    state_snapshot={"M6": M6, "depth": depth},
                    description=f"Computed Strassen product M6 = (A21 - A11) * (B11 + B12)."
                ))
                step_id[0] += 1

            # M7 = (A12 - A22) * (B21 + B22)
            s_a7 = self._sub(A12, A22)
            s_b7 = self._add(B21, B22)
            M7 = _strassen_instrumented(s_a7, s_b7, depth + 1)
            metrics.operations += 2 * (mid ** 2)
            if len(steps) < max_steps:
                steps.append(ExecutionStep(
                    step_id=step_id[0],
                    action="compute_m7",
                    state_snapshot={"M7": M7, "depth": depth},
                    description=f"Computed Strassen product M7 = (A12 - A22) * (B21 + B22)."
                ))
                step_id[0] += 1

            # Combine into C11, C12, C21, C22
            C11 = self._add(self._sub(self._add(M1, M4), M5), M7)
            C12 = self._add(M3, M5)
            C21 = self._add(M2, M4)
            C22 = self._add(self._add(self._sub(M1, M2), M3), M6)
            metrics.operations += 8 * (mid ** 2)

            # Assemble result matrix
            C_sub = []
            for i in range(mid):
                C_sub.append(C11[i] + C12[i])
            for i in range(mid):
                C_sub.append(C21[i] + C22[i])

            if len(steps) < max_steps:
                steps.append(ExecutionStep(
                    step_id=step_id[0],
                    action="combine_quadrants",
                    state_snapshot={
                        "depth": depth,
                        "C11": C11, "C12": C12, "C21": C21, "C22": C22,
                        "assembled": C_sub
                    },
                    description=f"Combined 7 Strassen products into {sz}x{sz} matrix quadrants C11..C22."
                ))
                step_id[0] += 1

            return C_sub

        C = _strassen_instrumented(A, B, depth=0)

        if len(steps) < max_steps:
            steps.append(ExecutionStep(
                step_id=step_id[0],
                action="complete",
                state_snapshot=C,
                description=f"Strassen multiplication completed successfully for {n}x{n} result matrix."
            ))

        out = {
            "result_matrix": C,
            "dimension": n
        }
        return AlgorithmExecutionResult(
            algorithm_slug=self.slug,
            output=out,
            metrics=metrics,
            steps=steps
        )
