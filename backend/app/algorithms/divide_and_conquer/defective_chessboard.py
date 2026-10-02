"""
Defective Chessboard (Tromino Tiling) Implementation (Divide and Conquer O(n^2) / O(4^k))
Tiles a 2^k x 2^k board with a single missing/defective square using L-shaped trominos.
"""
from typing import Dict, Any, List, Tuple
from app.algorithms.base import BaseAlgorithm, ExecutionMetrics, ExecutionStep, AlgorithmExecutionResult


class DefectiveChessboard(BaseAlgorithm):
    slug = "defective-chessboard"
    name = "Defective Chessboard (Tromino Tiling)"
    category = "Divide and Conquer"
    paradigm = "Divide and Conquer"

    time_complexity_best = "O(n^2)"
    time_complexity_average = "O(n^2)"
    time_complexity_worst = "O(n^2)"
    space_complexity = "O(n^2)"
    is_stable = False
    is_in_place = False

    def _parse_input(self, input_data: Any) -> Tuple[int, int, int]:
        """Extract board dimension n (power of 2) and defect coordinates (dr, dc)."""
        if isinstance(input_data, dict):
            size = input_data.get("size", input_data.get("board_size", 4))
            defect = input_data.get("defect", input_data.get("defect_pos", [0, 0]))
            if isinstance(defect, list) or isinstance(defect, tuple):
                dr, dc = defect[0], defect[1]
            else:
                dr = input_data.get("defect_row", 0)
                dc = input_data.get("defect_col", 0)
        elif isinstance(input_data, (list, tuple)) and len(input_data) >= 3:
            size, dr, dc = input_data[0], input_data[1], input_data[2]
        else:
            size, dr, dc = 4, 0, 0

        # Ensure size is a power of 2, minimum 2
        n = 1
        while n < size:
            n *= 2
        if n < 2:
            n = 2
        dr = max(0, min(dr, n - 1))
        dc = max(0, min(dc, n - 1))
        return n, dr, dc

    def run(self, input_data: Any) -> Dict[str, Any]:
        n, dr, dc = self._parse_input(input_data)
        board = [[0] * n for _ in range(n)]
        board[dr][dc] = -1  # -1 represents the defect square

        tromino_id = [1]

        def tile(top_r: int, top_c: int, defect_r: int, defect_c: int, size: int):
            if size <= 1:
                return

            t_id = tromino_id[0]
            tromino_id[0] += 1
            half = size // 2
            mid_r = top_r + half
            mid_c = top_c + half

            # Check which quadrant contains the defect / sub-defect
            # Quadrant 1: Top-Left
            if defect_r < mid_r and defect_c < mid_c:
                tile(top_r, top_c, defect_r, defect_c, half)
            else:
                board[mid_r - 1][mid_c - 1] = t_id
                tile(top_r, top_c, mid_r - 1, mid_c - 1, half)

            # Quadrant 2: Top-Right
            if defect_r < mid_r and defect_c >= mid_c:
                tile(top_r, mid_c, defect_r, defect_c, half)
            else:
                board[mid_r - 1][mid_c] = t_id
                tile(top_r, mid_c, mid_r - 1, mid_c, half)

            # Quadrant 3: Bottom-Left
            if defect_r >= mid_r and defect_c < mid_c:
                tile(mid_r, top_c, defect_r, defect_c, half)
            else:
                board[mid_r][mid_c - 1] = t_id
                tile(mid_r, top_c, mid_r, mid_c - 1, half)

            # Quadrant 4: Bottom-Right
            if defect_r >= mid_r and defect_c >= mid_c:
                tile(mid_r, mid_c, defect_r, defect_c, half)
            else:
                board[mid_r][mid_c] = t_id
                tile(mid_r, mid_c, mid_r, mid_c, half)

        tile(0, 0, dr, dc, n)

        return {
            "board_size": n,
            "defect": [dr, dc],
            "total_trominos": tromino_id[0] - 1,
            "board": board,
            "grid": board,
            "is_fully_tiled": True
        }

    def run_instrumented(self, input_data: Any, max_steps: int = 500) -> AlgorithmExecutionResult:
        n, dr, dc = self._parse_input(input_data)
        metrics = ExecutionMetrics()
        steps: List[ExecutionStep] = []
        step_id = [0]

        board = [[0] * n for _ in range(n)]
        board[dr][dc] = -1

        steps.append(ExecutionStep(
            step_id=step_id[0],
            action="init",
            indices=[dr, dc],
            values=[-1],
            state_snapshot=[row[:] for row in board],
            description=f"Initialized {n}x{n} chessboard with defect at row {dr}, col {dc}."
        ))
        step_id[0] += 1

        tromino_id = [1]

        def tile_instrumented(top_r: int, top_c: int, defect_r: int, defect_c: int, size: int):
            metrics.recursive_calls += 1
            metrics.operations += 1

            if size <= 1:
                return

            t_id = tromino_id[0]
            tromino_id[0] += 1
            half = size // 2
            mid_r = top_r + half
            mid_c = top_c + half

            placed_coords = []

            # Center tromino fills 3 quadrants without defect
            # Top-Left
            if not (defect_r < mid_r and defect_c < mid_c):
                board[mid_r - 1][mid_c - 1] = t_id
                placed_coords.append((mid_r - 1, mid_c - 1))

            # Top-Right
            if not (defect_r < mid_r and defect_c >= mid_c):
                board[mid_r - 1][mid_c] = t_id
                placed_coords.append((mid_r - 1, mid_c))

            # Bottom-Left
            if not (defect_r >= mid_r and defect_c < mid_c):
                board[mid_r][mid_c - 1] = t_id
                placed_coords.append((mid_r, mid_c - 1))

            # Bottom-Right
            if not (defect_r >= mid_r and defect_c >= mid_c):
                board[mid_r][mid_c] = t_id
                placed_coords.append((mid_r, mid_c))

            if len(steps) < max_steps:
                steps.append(ExecutionStep(
                    step_id=step_id[0],
                    action="place_tromino",
                    indices=[list(c) for c in placed_coords],
                    values=[t_id],
                    state_snapshot=[row[:] for row in board],
                    description=f"Placed Tromino #{t_id} at center ({mid_r-1}:{mid_r}, {mid_c-1}:{mid_c}) to create sub-defects for recursion."
                ))
                step_id[0] += 1

            # Recurse on 4 quadrants
            # 1. Top-Left
            sub_dr, sub_dc = (defect_r, defect_c) if (defect_r < mid_r and defect_c < mid_c) else (mid_r - 1, mid_c - 1)
            tile_instrumented(top_r, top_c, sub_dr, sub_dc, half)

            # 2. Top-Right
            sub_dr, sub_dc = (defect_r, defect_c) if (defect_r < mid_r and defect_c >= mid_c) else (mid_r - 1, mid_c)
            tile_instrumented(top_r, mid_c, sub_dr, sub_dc, half)

            # 3. Bottom-Left
            sub_dr, sub_dc = (defect_r, defect_c) if (defect_r >= mid_r and defect_c < mid_c) else (mid_r, mid_c - 1)
            tile_instrumented(mid_r, top_c, sub_dr, sub_dc, half)

            # 4. Bottom-Right
            sub_dr, sub_dc = (defect_r, defect_c) if (defect_r >= mid_r and defect_c >= mid_c) else (mid_r, mid_c)
            tile_instrumented(mid_r, mid_c, sub_dr, sub_dc, half)

        tile_instrumented(0, 0, dr, dc, n)

        out = {
            "board_size": n,
            "defect": [dr, dc],
            "total_trominos": tromino_id[0] - 1,
            "board": board,
            "is_fully_tiled": True
        }
        return AlgorithmExecutionResult(
            algorithm_slug=self.slug,
            output=out,
            metrics=metrics,
            steps=steps
        )
