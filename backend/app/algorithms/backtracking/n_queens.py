"""
N-Queens Problem Implementation (Backtracking with Pruning)
"""
from typing import Dict, Any, List
from app.algorithms.base import BaseAlgorithm, ExecutionMetrics, ExecutionStep, AlgorithmExecutionResult


class NQueens(BaseAlgorithm):
    slug = "n-queens-backtracking"
    name = "N-Queens (Backtracking)"
    category = "Backtracking"
    paradigm = "Backtracking"

    def run(self, input_data: Any) -> Dict[str, Any]:
        if isinstance(input_data, dict):
            n = int(input_data.get("n", 4))
        else:
            n = int(input_data)

        solutions: List[List[int]] = []
        board = [-1] * n

        cols = set()
        pos_diag = set()  # (r + c)
        neg_diag = set()  # (r - c)

        def _solve(row: int):
            if row == n:
                solutions.append(list(board))
                return

            for col in range(n):
                if col in cols or (row + col) in pos_diag or (row - col) in neg_diag:
                    continue

                board[row] = col
                cols.add(col)
                pos_diag.add(row + col)
                neg_diag.add(row - col)

                _solve(row + 1)

                # Backtrack
                board[row] = -1
                cols.remove(col)
                pos_diag.remove(row + col)
                neg_diag.remove(row - col)

        _solve(0)

        return {
            "n": n,
            "total_solutions": len(solutions),
            "solutions": solutions,
            "sample_solution": solutions[0] if solutions else []
        }

    def run_instrumented(self, input_data: Any, max_steps: int = 500) -> AlgorithmExecutionResult:
        if isinstance(input_data, dict):
            n = int(input_data.get("n", 4))
        else:
            n = int(input_data)

        metrics = ExecutionMetrics()
        steps: List[ExecutionStep] = []
        step_id = [0]

        solutions: List[List[int]] = []
        board = [-1] * n

        cols = set()
        pos_diag = set()
        neg_diag = set()

        steps.append(ExecutionStep(
            step_id=step_id[0],
            action="init",
            state_snapshot=list(board),
            description=f"Initialized N-Queens search on {n}x{n} chessboard."
        ))
        step_id[0] += 1

        def _solve_instrumented(row: int):
            metrics.recursive_calls += 1
            metrics.operations += 1

            if row == n:
                solutions.append(list(board))
                if len(steps) < max_steps:
                    steps.append(ExecutionStep(
                        step_id=step_id[0],
                        action="solution_found",
                        state_snapshot=list(board),
                        description=f"Solution #{len(solutions)} found: Queens placed at columns {list(board)}!",
                        highlight_line=4
                    ))
                    step_id[0] += 1
                return

            for col in range(n):
                metrics.comparisons += 1
                is_safe = (col not in cols) and ((row + col) not in pos_diag) and ((row - col) not in neg_diag)

                if is_safe:
                    board[row] = col
                    cols.add(col)
                    pos_diag.add(row + col)
                    neg_diag.add(row - col)

                    if len(steps) < max_steps:
                        steps.append(ExecutionStep(
                            step_id=step_id[0],
                            action="place_queen",
                            indices=[row, col],
                            values=[row, col],
                            state_snapshot=list(board),
                            description=f"Placed Queen at row {row}, col {col}.",
                            highlight_line=7
                        ))
                        step_id[0] += 1

                    _solve_instrumented(row + 1)

                    # Backtrack
                    board[row] = -1
                    cols.remove(col)
                    pos_diag.remove(row + col)
                    neg_diag.remove(row - col)

                    if len(steps) < max_steps:
                        steps.append(ExecutionStep(
                            step_id=step_id[0],
                            action="backtrack",
                            indices=[row, col],
                            state_snapshot=list(board),
                            description=f"Backtracked: Removed Queen from row {row}, col {col} to try next branch."
                        ))
                        step_id[0] += 1

        _solve_instrumented(0)

        out = {
            "n": n,
            "total_solutions": len(solutions),
            "sample_solution": solutions[0] if solutions else []
        }
        return AlgorithmExecutionResult(
            algorithm_slug=self.slug,
            output=out,
            metrics=metrics,
            steps=steps
        )
