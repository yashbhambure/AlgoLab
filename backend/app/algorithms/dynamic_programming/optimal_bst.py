"""
Optimal Binary Search Tree (OBST) Implementation (Dynamic Programming O(n^3))
Constructs a binary search tree with minimum expected search cost given key probabilities.
"""
from typing import Dict, Any, List, Optional
from app.algorithms.base import BaseAlgorithm, ExecutionMetrics, ExecutionStep, AlgorithmExecutionResult


class OptimalBST(BaseAlgorithm):
    slug = "optimal-bst-dp"
    name = "Optimal Binary Search Tree (OBST DP)"
    category = "Dynamic Programming"
    paradigm = "Dynamic Programming"

    time_complexity_best = "O(n^3)"
    time_complexity_average = "O(n^3)"
    time_complexity_worst = "O(n^3)"
    space_complexity = "O(n^2)"
    is_stable = True
    is_in_place = False

    def _parse_input(self, input_data: Any):
        if isinstance(input_data, dict):
            keys = input_data.get("keys", ["k1", "k2", "k3", "k4"])
            p = input_data.get("probabilities", input_data.get("p", [0.1, 0.2, 0.4, 0.3]))
            q = input_data.get("dummy_probabilities", input_data.get("q", [0.05, 0.1, 0.05, 0.05, 0.05]))
        else:
            keys = ["k1", "k2", "k3", "k4"]
            p = [0.1, 0.2, 0.4, 0.3]
            q = [0.05, 0.1, 0.05, 0.05, 0.05]

        n = len(keys)
        # Pad p to 1-indexed (p[0] = 0)
        p_padded = [0.0] + [float(x) for x in p[:n]]
        q_padded = [float(x) for x in q[:n + 1]]
        while len(q_padded) < n + 1:
            q_padded.append(0.0)

        return keys, p_padded, q_padded, n

    def run(self, input_data: Any) -> Dict[str, Any]:
        keys, p, q, n = self._parse_input(input_data)

        # e[i][j] = expected search cost of optimal subtree with keys k_{i+1} .. k_j
        # w[i][j] = sum of probabilities in subtree
        # root[i][j] = optimal root index for keys k_{i+1} .. k_j
        e = [[0.0] * (n + 1) for _ in range(n + 1)]
        w = [[0.0] * (n + 1) for _ in range(n + 1)]
        root = [[0] * (n + 1) for _ in range(n + 1)]

        for i in range(n + 1):
            e[i][i] = q[i]
            w[i][i] = q[i]

        for length in range(1, n + 1):
            for i in range(n - length + 1):
                j = i + length
                e[i][j] = float('inf')
                w[i][j] = round(w[i][j - 1] + p[j] + q[j], 4)

                for r in range(i + 1, j + 1):
                    cost = round(e[i][r - 1] + e[r][j] + w[i][j], 4)
                    if cost < e[i][j]:
                        e[i][j] = cost
                        root[i][j] = r

        def build_tree(i: int, j: int) -> Optional[Dict[str, Any]]:
            if i >= j:
                return None
            r = root[i][j]
            if r == 0:
                return None
            key_label = keys[r - 1] if r - 1 < len(keys) else f"k{r}"
            return {
                "key": key_label,
                "key_index": r,
                "left": build_tree(i, r - 1),
                "right": build_tree(r, j)
            }

        tree = build_tree(0, n)

        return {
            "num_keys": n,
            "optimal_cost": round(e[0][n], 4),
            "min_cost": round(e[0][n], 4),
            "root_table": root,
            "cost_table": [[round(x, 4) for x in row] for row in e],
            "weight_table": [[round(x, 4) for x in row] for row in w],
            "tree_structure": tree
        }

    def run_instrumented(self, input_data: Any, max_steps: int = 500) -> AlgorithmExecutionResult:
        keys, p, q, n = self._parse_input(input_data)
        metrics = ExecutionMetrics()
        steps: List[ExecutionStep] = []
        step_id = [0]

        e = [[0.0] * (n + 1) for _ in range(n + 1)]
        w = [[0.0] * (n + 1) for _ in range(n + 1)]
        root = [[0] * (n + 1) for _ in range(n + 1)]

        for i in range(n + 1):
            e[i][i] = q[i]
            w[i][i] = q[i]

        steps.append(ExecutionStep(
            step_id=step_id[0],
            action="init",
            state_snapshot={"e": [[round(x, 4) for x in row] for row in e], "w": [[round(x, 4) for x in row] for row in w]},
            description=f"Initialized OBST DP tables for {n} keys and {n+1} dummy keys with base costs."
        ))
        step_id[0] += 1

        for length in range(1, n + 1):
            for i in range(n - length + 1):
                j = i + length
                e[i][j] = float('inf')
                w[i][j] = round(w[i][j - 1] + p[j] + q[j], 4)
                metrics.operations += 1

                for r in range(i + 1, j + 1):
                    metrics.comparisons += 1
                    cost = round(e[i][r - 1] + e[r][j] + w[i][j], 4)

                    if cost < e[i][j]:
                        e[i][j] = cost
                        root[i][j] = r

                        if len(steps) < max_steps:
                            steps.append(ExecutionStep(
                                step_id=step_id[0],
                                action="set_root",
                                indices=[i, j, r],
                                values=[cost, r],
                                state_snapshot={"current_len": length, "subproblem": [i, j], "best_root": r, "cost": cost},
                                description=f"Subtree ({i}..{j}) optimal root set to key k{r} ({keys[r-1] if r-1 < len(keys) else r}) with expected cost {cost}.",
                                highlight_line=5
                            ))
                            step_id[0] += 1

        def build_tree(i: int, j: int) -> Optional[Dict[str, Any]]:
            if i >= j:
                return None
            r = root[i][j]
            if r == 0:
                return None
            key_label = keys[r - 1] if r - 1 < len(keys) else f"k{r}"
            return {
                "key": key_label,
                "key_index": r,
                "left": build_tree(i, r - 1),
                "right": build_tree(r, j)
            }

        tree = build_tree(0, n)

        out = {
            "num_keys": n,
            "optimal_cost": round(e[0][n], 4),
            "root_table": root,
            "cost_table": [[round(x, 4) for x in row] for row in e],
            "weight_table": [[round(x, 4) for x in row] for row in w],
            "tree_structure": tree
        }
        return AlgorithmExecutionResult(
            algorithm_slug=self.slug,
            output=out,
            metrics=metrics,
            steps=steps
        )
