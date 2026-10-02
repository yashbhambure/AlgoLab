"""
Job Sequencing with Deadlines Implementation (Greedy)
"""
from typing import Dict, Any, List
from app.algorithms.base import BaseAlgorithm, ExecutionMetrics, ExecutionStep, AlgorithmExecutionResult


class JobSequencing(BaseAlgorithm):
    slug = "job-sequencing-deadlines"
    name = "Job Sequencing with Deadlines"
    category = "Greedy"
    paradigm = "Greedy"

    def _parse_input(self, input_data: Any):
        if isinstance(input_data, dict):
            if "jobs" in input_data:
                jobs_raw = input_data["jobs"]
                deadlines = [j.get("deadline", 1) if isinstance(j, dict) else j[1] for j in jobs_raw]
                profits = [j.get("profit", 0) if isinstance(j, dict) else j[2] for j in jobs_raw]
            else:
                deadlines = input_data.get("deadlines", [])
                profits = input_data.get("profits", [])
        elif isinstance(input_data, list) and input_data and isinstance(input_data[0], dict):
            deadlines = [j.get("deadline", 1) for j in input_data]
            profits = [j.get("profit", 0) for j in input_data]
        elif isinstance(input_data, (list, tuple)) and len(input_data) == 2 and isinstance(input_data[0], list):
            deadlines, profits = input_data
        else:
            deadlines, profits = [], []
        return deadlines, profits

    def run(self, input_data: Any) -> Dict[str, Any]:
        deadlines, profits = self._parse_input(input_data)

        n = len(deadlines)
        if n == 0:
            return {"total_profit": 0, "schedule": []}

        jobs = sorted(
            [{"id": i, "deadline": deadlines[i], "profit": profits[i]} for i in range(n)],
            key=lambda x: x["profit"],
            reverse=True
        )

        max_deadline = max(deadlines) if deadlines else 0
        slots = [-1] * max_deadline
        total_profit = 0
        scheduled_jobs = []

        for job in jobs:
            # Find the latest available free time slot before deadline
            for t in range(min(max_deadline, job["deadline"]) - 1, -1, -1):
                if slots[t] == -1:
                    slots[t] = job["id"]
                    total_profit += job["profit"]
                    scheduled_jobs.append(job["id"])
                    break

        return {
            "total_profit": total_profit,
            "scheduled_count": len(scheduled_jobs),
            "slots": slots,
            "scheduled_jobs": scheduled_jobs
        }

    def run_instrumented(self, input_data: Any, max_steps: int = 500) -> AlgorithmExecutionResult:
        deadlines, profits = self._parse_input(input_data)

        metrics = ExecutionMetrics()
        steps: List[ExecutionStep] = []
        step_id = 0
        n = len(deadlines)

        if n == 0:
            return AlgorithmExecutionResult(algorithm_slug=self.slug, output={}, metrics=metrics, steps=[])

        jobs = sorted(
            [{"id": i, "deadline": deadlines[i], "profit": profits[i]} for i in range(n)],
            key=lambda x: x["profit"],
            reverse=True
        )
        metrics.operations += n

        max_deadline = max(deadlines) if deadlines else 0
        slots = [-1] * max_deadline

        steps.append(ExecutionStep(
            step_id=step_id,
            action="init_sort",
            state_snapshot=jobs,
            description=f"Sorted {n} jobs descending by profit for Greedy processing. Timeline slots 0..{max_deadline-1} initialized."
        ))
        step_id += 1

        total_profit = 0
        scheduled_jobs = []

        for job in jobs:
            allocated = False
            for t in range(min(max_deadline, job["deadline"]) - 1, -1, -1):
                metrics.comparisons += 1
                metrics.operations += 1
                if slots[t] == -1:
                    slots[t] = job["id"]
                    total_profit += job["profit"]
                    scheduled_jobs.append(job["id"])
                    allocated = True

                    if len(steps) < max_steps:
                        steps.append(ExecutionStep(
                            step_id=step_id,
                            action="slot_assigned",
                            indices=[t],
                            values=[job["id"], job["profit"], job["deadline"]],
                            state_snapshot=list(slots),
                            description=f"Scheduled Job #{job['id']} (profit={job['profit']}, deadline={job['deadline']}) in slot {t}.",
                            highlight_line=5
                        ))
                        step_id += 1
                    break

            if not allocated and len(steps) < max_steps:
                steps.append(ExecutionStep(
                    step_id=step_id,
                    action="job_dropped",
                    indices=[job["id"]],
                    values=[job["profit"]],
                    state_snapshot=list(slots),
                    description=f"Dropped Job #{job['id']} (deadline={job['deadline']}) - no available earlier time slot."
                ))
                step_id += 1

        out = {
            "total_profit": total_profit,
            "scheduled_count": len(scheduled_jobs),
            "slots": slots,
            "scheduled_jobs": scheduled_jobs
        }
        return AlgorithmExecutionResult(
            algorithm_slug=self.slug,
            output=out,
            metrics=metrics,
            steps=steps
        )
