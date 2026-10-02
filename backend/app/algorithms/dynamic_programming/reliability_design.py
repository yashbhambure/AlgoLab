"""
Reliability Design Problem Implementation (Dynamic Programming / Dominated Set Pruning)
Maximizes multi-stage series-parallel system reliability under fixed cost budget.
"""
from typing import Dict, Any, List, Tuple
from app.algorithms.base import BaseAlgorithm, ExecutionMetrics, ExecutionStep, AlgorithmExecutionResult


class ReliabilityDesignDP(BaseAlgorithm):
    slug = "reliability-design-dp"
    name = "Reliability Design (Dynamic Programming)"
    category = "Dynamic Programming"
    paradigm = "Dynamic Programming"

    time_complexity_best = "O(n C)"
    time_complexity_average = "O(n C^2)"
    time_complexity_worst = "O(n C^2)"
    space_complexity = "O(n C)"
    is_stable = True
    is_in_place = False

    def _parse_input(self, input_data: Any):
        if isinstance(input_data, dict):
            reliabilities = input_data.get("reliabilities", input_data.get("r", [0.9, 0.8, 0.5]))
            costs = input_data.get("costs", input_data.get("c", [30, 15, 20]))
            budget = input_data.get("budget", input_data.get("total_cost", 105))
        elif isinstance(input_data, (list, tuple)) and len(input_data) >= 3:
            reliabilities, costs, budget = input_data[0], input_data[1], input_data[2]
        else:
            # Canonical textbook example: 3 stages, r=[0.9, 0.8, 0.5], c=[30, 15, 20], budget=105
            reliabilities = [0.9, 0.8, 0.5]
            costs = [30, 15, 20]
            budget = 105

        n = len(reliabilities)
        r = [float(x) for x in reliabilities[:n]]
        c = [int(x) for x in costs[:n]]
        total_budget = int(budget)
        return n, r, c, total_budget

    def _stage_reliability(self, r_i: float, m_i: int) -> float:
        """Reliability of stage i with m_i parallel copies: 1 - (1 - r_i)^m_i."""
        return 1.0 - ((1.0 - r_i) ** m_i)

    def _purge_dominated(self, tuples: List[Tuple[float, int, List[int]]]) -> List[Tuple[float, int, List[int]]]:
        """Purge dominated tuples: If R1 <= R2 and C1 >= C2, discard tuple 1."""
        # Sort by cost ascending, then reliability descending
        tuples.sort(key=lambda t: (t[1], -t[0]))
        purged = []
        max_rel = -1.0
        for rel, cost, alloc in tuples:
            if rel > max_rel:
                purged.append((rel, cost, alloc))
                max_rel = rel
        return purged

    def run(self, input_data: Any) -> Dict[str, Any]:
        n, r, c, budget = self._parse_input(input_data)

        # Minimum base cost to instantiate at least 1 copy per stage
        min_cost_remaining = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            min_cost_remaining[i] = min_cost_remaining[i + 1] + c[i]

        if min_cost_remaining[0] > budget:
            return {
                "success": False,
                "error": "Budget insufficient to instantiate minimal configuration (1 copy per stage).",
                "max_reliability": 0.0,
                "allocation": [0] * n,
                "total_cost": 0
            }

        # S holds tuples: (reliability, cost_used, allocation_list)
        S: List[Tuple[float, int, List[int]]] = [(1.0, 0, [])]

        for i in range(n):
            # Compute upper bound copies for stage i: u_i
            rem_after_i = min_cost_remaining[i + 1]
            u_i = (budget - rem_after_i - (sum(c[:i]))) // c[i]
            u_i = max(1, min(u_i, 10))  # practical bound

            next_S: List[Tuple[float, int, List[int]]] = []
            for prev_rel, prev_cost, prev_alloc in S:
                for m_i in range(1, u_i + 1):
                    cost_curr = prev_cost + m_i * c[i]
                    if cost_curr + rem_after_i <= budget:
                        rel_curr = prev_rel * self._stage_reliability(r[i], m_i)
                        next_S.append((rel_curr, cost_curr, prev_alloc + [m_i]))

            S = self._purge_dominated(next_S)

        # Pick tuple with maximum reliability
        best_tuple = max(S, key=lambda t: t[0]) if S else (0.0, 0, [0] * n)

        stage_breakdown = []
        for i, m_i in enumerate(best_tuple[2]):
            phi = round(self._stage_reliability(r[i], m_i), 4)
            stage_breakdown.append({
                "stage": i + 1,
                "copies": m_i,
                "unit_cost": c[i],
                "stage_cost": m_i * c[i],
                "single_reliability": r[i],
                "stage_reliability": phi
            })

        return {
            "num_stages": n,
            "budget": budget,
            "max_reliability": round(best_tuple[0], 6),
            "total_cost": best_tuple[1],
            "allocation": best_tuple[2],
            "stage_breakdown": stage_breakdown,
            "feasible_configurations_evaluated": len(S)
        }

    def run_instrumented(self, input_data: Any, max_steps: int = 500) -> AlgorithmExecutionResult:
        n, r, c, budget = self._parse_input(input_data)
        metrics = ExecutionMetrics()
        steps: List[ExecutionStep] = []
        step_id = [0]

        min_cost_remaining = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            min_cost_remaining[i] = min_cost_remaining[i + 1] + c[i]

        steps.append(ExecutionStep(
            step_id=step_id[0],
            action="init",
            state_snapshot={"stages": n, "costs": c, "reliabilities": r, "budget": budget},
            description=f"Initialized Reliability Design DP for {n} stages with budget ${budget}."
        ))
        step_id[0] += 1

        S: List[Tuple[float, int, List[int]]] = [(1.0, 0, [])]

        for i in range(n):
            metrics.operations += 1
            rem_after_i = min_cost_remaining[i + 1]
            u_i = (budget - rem_after_i - (sum(c[:i]))) // c[i]
            u_i = max(1, min(u_i, 10))

            next_S: List[Tuple[float, int, List[int]]] = []
            for prev_rel, prev_cost, prev_alloc in S:
                for m_i in range(1, u_i + 1):
                    cost_curr = prev_cost + m_i * c[i]
                    metrics.comparisons += 1
                    if cost_curr + rem_after_i <= budget:
                        rel_curr = prev_rel * self._stage_reliability(r[i], m_i)
                        next_S.append((rel_curr, cost_curr, prev_alloc + [m_i]))

            unpurged_len = len(next_S)
            S = self._purge_dominated(next_S)

            if len(steps) < max_steps:
                best_so_far = max(S, key=lambda t: t[0]) if S else (0, 0, [])
                steps.append(ExecutionStep(
                    step_id=step_id[0],
                    action="generate_stage_set",
                    indices=[i + 1],
                    values=[len(S)],
                    state_snapshot={"stage": i + 1, "tuples_count": len(S), "best_rel": round(best_so_far[0], 4)},
                    description=f"Stage {i+1}: Generated {unpurged_len} states -> Purged {unpurged_len - len(S)} dominated tuples -> {len(S)} non-dominated states retained.",
                    highlight_line=5
                ))
                step_id[0] += 1

        best_tuple = max(S, key=lambda t: t[0]) if S else (0.0, 0, [0] * n)

        stage_breakdown = []
        for i, m_i in enumerate(best_tuple[2]):
            phi = round(self._stage_reliability(r[i], m_i), 4)
            stage_breakdown.append({
                "stage": i + 1,
                "copies": m_i,
                "unit_cost": c[i],
                "stage_cost": m_i * c[i],
                "single_reliability": r[i],
                "stage_reliability": phi
            })

        steps.append(ExecutionStep(
            step_id=step_id[0],
            action="optimal_design_selected",
            state_snapshot={"max_reliability": round(best_tuple[0], 6), "allocation": best_tuple[2], "cost": best_tuple[1]},
            description=f"Optimal Reliability Design found: Allocation={best_tuple[2]}, Total Cost=${best_tuple[1]} / ${budget}, System Reliability={round(best_tuple[0], 6)}."
        ))
        step_id[0] += 1

        out = {
            "num_stages": n,
            "budget": budget,
            "max_reliability": round(best_tuple[0], 6),
            "total_cost": best_tuple[1],
            "allocation": best_tuple[2],
            "stage_breakdown": stage_breakdown,
            "feasible_configurations_evaluated": len(S)
        }
        return AlgorithmExecutionResult(
            algorithm_slug=self.slug,
            output=out,
            metrics=metrics,
            steps=steps
        )
