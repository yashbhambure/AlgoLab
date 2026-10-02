"""
Optimal Storage on Tapes Implementation (Greedy O(n log n))
Minimizes Mean Retrieval Time (MRT) by ordering programs by length on magnetic tapes.
"""
from typing import Dict, Any, List
from app.algorithms.base import BaseAlgorithm, ExecutionMetrics, ExecutionStep, AlgorithmExecutionResult


class OptimalStorageOnTapes(BaseAlgorithm):
    slug = "optimal-storage-tapes-greedy"
    name = "Optimal Storage on Tapes (Greedy)"
    category = "Greedy"
    paradigm = "Greedy"

    time_complexity_best = "O(n log n)"
    time_complexity_average = "O(n log n)"
    time_complexity_worst = "O(n log n)"
    space_complexity = "O(n)"
    is_stable = True
    is_in_place = False

    def _parse_input(self, input_data: Any):
        if isinstance(input_data, dict):
            lengths = input_data.get("lengths", input_data.get("program_lengths", [5, 10, 3, 20, 12, 7]))
            tapes = input_data.get("tapes", input_data.get("num_tapes", 1))
            program_names = input_data.get("programs", [])
        elif isinstance(input_data, list):
            lengths = input_data
            tapes = 1
            program_names = []
        else:
            lengths = [5, 10, 3, 20, 12, 7]
            tapes = 1
            program_names = []

        n = len(lengths)
        if not program_names or len(program_names) < n:
            program_names = [f"P{i+1}" for i in range(n)]

        return [float(x) for x in lengths], int(max(1, tapes)), program_names

    def run(self, input_data: Any) -> Dict[str, Any]:
        lengths, num_tapes, names = self._parse_input(input_data)
        n = len(lengths)

        # Pair program index, name, and length
        programs = [{"id": i, "name": names[i], "length": lengths[i]} for i in range(n)]
        # Greedy strategy: Sort by length ascending
        programs.sort(key=lambda p: p["length"])

        tape_assignments: List[List[Dict[str, Any]]] = [[] for _ in range(num_tapes)]
        tape_retrieval_times: List[List[float]] = [[] for _ in range(num_tapes)]

        for idx, prog in enumerate(programs):
            tape_idx = idx % num_tapes
            tape_assignments[tape_idx].append(prog)

        # Calculate MRT per tape and overall
        total_system_time = 0.0
        tape_summaries = []

        for t_idx, tape in enumerate(tape_assignments):
            cum_time = 0.0
            total_tape_time = 0.0
            r_times = []
            for p in tape:
                cum_time += p["length"]
                r_times.append(cum_time)
                total_tape_time += cum_time

            total_system_time += total_tape_time
            tape_mrt = total_tape_time / len(tape) if tape else 0.0
            tape_summaries.append({
                "tape_id": t_idx + 1,
                "programs": [p["name"] for p in tape],
                "lengths": [p["length"] for p in tape],
                "retrieval_times": r_times,
                "total_retrieval_time": round(total_tape_time, 2),
                "mrt": round(tape_mrt, 2)
            })

        overall_mrt = total_system_time / n if n > 0 else 0.0

        return {
            "num_programs": n,
            "num_tapes": num_tapes,
            "optimal_order": [p["name"] for p in programs],
            "sorted_lengths": [p["length"] for p in programs],
            "tape_distribution": tape_summaries,
            "total_retrieval_time": round(total_system_time, 2),
            "mean_retrieval_time": round(overall_mrt, 4)
        }

    def run_instrumented(self, input_data: Any, max_steps: int = 500) -> AlgorithmExecutionResult:
        lengths, num_tapes, names = self._parse_input(input_data)
        metrics = ExecutionMetrics()
        steps: List[ExecutionStep] = []
        step_id = [0]
        n = len(lengths)

        steps.append(ExecutionStep(
            step_id=step_id[0],
            action="init",
            state_snapshot={"lengths": lengths, "tapes": num_tapes},
            description=f"Initialized Optimal Storage on Tapes for {n} programs across {num_tapes} magnetic tape(s)."
        ))
        step_id[0] += 1

        programs = [{"id": i, "name": names[i], "length": lengths[i]} for i in range(n)]
        programs.sort(key=lambda p: p["length"])
        metrics.operations += n

        prog_list = [f"{p['name']}({p['length']})" for p in programs]
        steps.append(ExecutionStep(
            step_id=step_id[0],
            action="greedy_sort",
            state_snapshot=[p["length"] for p in programs],
            description=f"Greedy Ordering: Sorted all programs in ascending length order: {prog_list}."
        ))
        step_id[0] += 1

        tape_assignments: List[List[Dict[str, Any]]] = [[] for _ in range(num_tapes)]

        for idx, prog in enumerate(programs):
            tape_idx = idx % num_tapes
            tape_assignments[tape_idx].append(prog)
            metrics.operations += 1

            if len(steps) < max_steps:
                steps.append(ExecutionStep(
                    step_id=step_id[0],
                    action="assign_to_tape",
                    indices=[prog["id"], tape_idx],
                    values=[prog["length"]],
                    state_snapshot={"program": prog["name"], "tape": tape_idx + 1, "length": prog["length"]},
                    description=f"Assigned {prog['name']} (length {prog['length']}) to Tape {tape_idx + 1}.",
                    highlight_line=4
                ))
                step_id[0] += 1

        # Summary
        total_system_time = 0.0
        tape_summaries = []
        for t_idx, tape in enumerate(tape_assignments):
            cum_time = 0.0
            total_tape_time = 0.0
            r_times = []
            for p in tape:
                cum_time += p["length"]
                r_times.append(cum_time)
                total_tape_time += cum_time

            total_system_time += total_tape_time
            tape_mrt = total_tape_time / len(tape) if tape else 0.0
            tape_summaries.append({
                "tape_id": t_idx + 1,
                "programs": [p["name"] for p in tape],
                "lengths": [p["length"] for p in tape],
                "retrieval_times": r_times,
                "total_retrieval_time": round(total_tape_time, 2),
                "mrt": round(tape_mrt, 2)
            })

        overall_mrt = total_system_time / n if n > 0 else 0.0

        steps.append(ExecutionStep(
            step_id=step_id[0],
            action="optimal_mrt_computed",
            state_snapshot={"mean_retrieval_time": round(overall_mrt, 4), "total_time": round(total_system_time, 2)},
            description=f"Storage schedule complete. Overall Mean Retrieval Time (MRT) = {round(overall_mrt, 4)} units."
        ))
        step_id[0] += 1

        out = {
            "num_programs": n,
            "num_tapes": num_tapes,
            "optimal_order": [p["name"] for p in programs],
            "sorted_lengths": [p["length"] for p in programs],
            "tape_distribution": tape_summaries,
            "total_retrieval_time": round(total_system_time, 2),
            "mean_retrieval_time": round(overall_mrt, 4)
        }
        return AlgorithmExecutionResult(
            algorithm_slug=self.slug,
            output=out,
            metrics=metrics,
            steps=steps
        )
