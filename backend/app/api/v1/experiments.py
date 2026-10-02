"""
Experiment Session Management and Academic Reporting Endpoints.
Provides structured 10-section academic exports in Markdown and JSON formats.
"""
from typing import Any, List, Optional, Dict
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import PlainTextResponse, JSONResponse
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_optional_user, get_current_user
from app.models.experiment import Experiment
from app.models.user import User
from app.schemas.experiment import ExperimentCreate, ExperimentResponse, ExperimentDetail
from app.algorithms.registry import registry
from app.recommendation.engine import RecommendationEngine

router = APIRouter(prefix="/experiments", tags=["Experiments"])


def generate_10_section_academic_markdown(exp: Experiment) -> str:
    """
    Generates a formal 10-section academic markdown report adhering to laboratory standards.
    """
    title = exp.name or "Algorithmic Empirical Performance Evaluation"
    created_str = exp.created_at.strftime('%Y-%m-%d %H:%M:%S UTC') if exp.created_at else 'N/A'
    algos = exp.algorithm_ids or []
    input_sizes = exp.input_sizes or []
    dist = exp.dataset_distribution or "Uniform Random"
    reps = exp.repetitions or 3
    results_data = exp.results_summary if isinstance(exp.results_summary, dict) else {}
    mcda_data = exp.asymptotic_fit_summary if isinstance(exp.asymptotic_fit_summary, dict) else {}
    notes = exp.conclusion_notes or "Empirical benchmark evaluation under controlled CPU time isolation."

    # Resolve theoretical complexities
    algo_meta_list = []
    for slug in algos:
        meta = RecommendationEngine._resolve_algo_metadata(slug)
        algo_meta_list.append(meta)

    # 1. Title & Header
    md = f"# Academic Experiment Report: {title}\n\n"
    md += f"**Experiment ID:** `{exp.id}`  \n"
    md += f"**Execution Timestamp:** {created_str}  \n"
    md += f"**Laboratory System:** AlgoLab Intelligent Benchmark & MCDA Suite\n\n"
    md += "---\n\n"

    # Section 1: Problem Definition and Constraints
    md += "## 1. Problem Definition and Constraints\n\n"
    md += f"- **Target Problem / Domain:** `{exp.problem_id or 'General Benchmark'}`\n"
    md += f"- **Objective:** Empirical evaluation and MCDA decision ranking of algorithmic candidates under variable input scaling.\n"
    md += f"- **Experimental Constraints:** Standard deterministic CPU execution, non-preemptive timing loops, memory allocation profiling.\n\n"

    # Section 2: Algorithms Evaluated
    md += "## 2. Algorithms Evaluated\n\n"
    md += "| Algorithm Name | Identifier / Slug | Paradigm | Category |\n"
    md += "| :--- | :--- | :--- | :--- |\n"
    for m in algo_meta_list:
        md += f"| {m['name']} | `{m['slug']}` | {m['paradigm']} | {m['category']} |\n"
    md += "\n"

    # Section 3: Experimental Setup
    md += "## 3. Experimental Setup\n\n"
    md += f"- **Repetitions per data point:** {reps} trials (averaged)\n"
    md += f"- **Timing Measurement Method:** Monotonic microsecond clock (`time.perf_counter_ns`)\n"
    md += f"- **Memory Measurement Method:** `tracemalloc` peak heap allocation delta\n"
    md += f"- **Execution Environment:** Sandboxed isolated Python runtime worker\n\n"

    # Section 4: Input Sizes and Distributions
    md += "## 4. Input Sizes & Distribution Profiles\n\n"
    md += f"- **Input Sizes ($N$):** {', '.join(str(s) for s in input_sizes) if input_sizes else 'N/A'}\n"
    md += f"- **Dataset Generation Model:** {dist.title()}\n\n"

    # Section 5: Theoretical Complexity
    md += "## 5. Theoretical Asymptotic Complexity\n\n"
    md += "| Algorithm | Best Case $T(n)$ | Average Case $T(n)$ | Worst Case $T(n)$ | Auxiliary Space $S(n)$ | Stability | In-Place |\n"
    md += "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
    for m in algo_meta_list:
        stable_str = "Yes" if m['stable'] else "No"
        inplace_str = "Yes" if m['in_place'] else "No"
        md += f"| {m['name']} | ${m['best']}$ | ${m['avg']}$ | ${m['worst']}$ | ${m['space']}$ | {stable_str} | {inplace_str} |\n"
    md += "\n"

    # Section 6: Measured Benchmark Results
    md += "## 6. Measured Benchmark Results\n\n"
    md += "| Input Size ($N$) | Algorithm | Mean Time (ms) | Peak Memory (KB) |\n"
    md += "| :--- | :--- | :--- | :--- |\n"
    has_results = False
    for algo_slug, data in results_data.items():
        if isinstance(data, list):
            for pt in data:
                has_results = True
                n_val = pt.get('n', pt.get('size', 'N/A'))
                t_val = pt.get('mean_ms', pt.get('time_ms', pt.get('execution_time_ms', 0.0)))
                m_val = pt.get('mem_kb', pt.get('peak_memory_kb', 0.0))
                md += f"| {n_val} | `{algo_slug}` | {float(t_val):.4f} | {float(m_val):.2f} |\n"
    if not has_results:
        md += "| N/A | No empirical measurements tabulated | — | — |\n"
    md += "\n"

    # Section 7: Speedup Calculations
    md += "## 7. Relative Speedup Calculations\n\n"
    # Find common max input size or compare compatible measured runs
    baseline_time: Optional[float] = None
    baseline_slug: Optional[str] = None
    all_final_times: Dict[str, float] = {}

    for algo_slug, data in results_data.items():
        if isinstance(data, list) and data:
            last_pt = data[-1]
            t = float(last_pt.get('mean_ms', last_pt.get('time_ms', 0.0)))
            if t > 0:
                all_final_times[algo_slug] = t

    if len(all_final_times) > 1:
        md += "| Algorithm | Measured Time (ms) | Relative Speedup vs Slowest | Relative Ratio vs Fastest |\n"
        md += "| :--- | :--- | :--- | :--- |\n"
        slowest_time = max(all_final_times.values())
        fastest_time = min(all_final_times.values())
        for a_slug, a_time in sorted(all_final_times.items(), key=lambda x: x[1]):
            speedup_vs_slowest = f"{(slowest_time / a_time):.2f}x" if a_time > 0 else "N/A"
            ratio_vs_fastest = f"{(a_time / fastest_time):.2f}x" if fastest_time > 0 else "N/A"
            md += f"| `{a_slug}` | {a_time:.4f} | **{speedup_vs_slowest}** | {ratio_vs_fastest} |\n"
    else:
        md += "*Speedup calculations require at least two compatible empirical benchmark measurements across identical input sizes.*\n"
    md += "\n"

    # Section 8: MCDA Scoring Breakdown
    md += "## 8. MCDA Multi-Criteria Decision Breakdown\n\n"
    rankings = mcda_data.get('rankings', [])
    if rankings:
        md += "| Rank | Algorithm | Composite Score | Theoretical Score | Empirical Score | Space Score | Input Fitness |\n"
        md += "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
        for i, r in enumerate(rankings, 1):
            sc = r.get('score', 0)
            bd = r.get('breakdown', r.get('scores', {}))
            md += f"| #{i} | {r.get('algorithm_name', r.get('algorithm_slug'))} | **{sc}** | {bd.get('theoretical_score', 'N/A')} | {bd.get('empirical_score', 'N/A')} | {bd.get('space_score', 'N/A')} | {bd.get('input_suitability_score', 'N/A')} |\n"
    else:
        md += "*No MCDA decision matrix was attached to this experiment run.*\n"
    md += "\n"

    # Section 9: Recommendation & Decision Summary
    md += "## 9. Decision Support Recommendation\n\n"
    rec_algo = mcda_data.get('recommended_name', mcda_data.get('recommended_algorithm', 'N/A'))
    rec_score = mcda_data.get('winning_score', 'N/A')
    justification = mcda_data.get('explanation', {}).get('summary', mcda_data.get('justification', notes))
    md += f"- **Recommended Optimal Algorithm:** **{rec_algo}** (Score: {rec_score})\n"
    md += f"- **Academic Decision Justification:** {justification}\n\n"

    # Section 10: Limitations and Conclusions
    md += "## 10. Experimental Limitations & Academic Conclusion\n\n"
    md += "1. **Distinction of Proof:** Empirical timing measurements characterize hardware-level execution behavior and constant factors on current architectures, but do not constitute formal mathematical proofs of theoretical Big-O upper/lower bounds.\n"
    md += "2. **Hardware Sensitivity:** Cache hierarchy, branch prediction, and OS interrupt scheduling introduce variance into micro-benchmarks.\n"
    md += f"3. **Experimental Conclusion:** {notes}\n"

    return md


@router.get("", response_model=List[ExperimentResponse])
def list_experiments(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
) -> Any:
    """List experiment benchmark sessions."""
    query = db.query(Experiment)
    if current_user:
        query = query.filter((Experiment.user_id == current_user.id) | (Experiment.user_id == None))
    return query.order_by(Experiment.created_at.desc()).all()


@router.get("/{exp_id}", response_model=ExperimentDetail)
def get_experiment(
    exp_id: str,
    db: Session = Depends(get_db)
) -> Any:
    """Retrieve full experiment report and benchmark results."""
    exp = db.query(Experiment).filter(Experiment.id == exp_id).first()
    if not exp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Experiment with ID {exp_id} not found."
        )
    return exp


@router.post("", response_model=ExperimentDetail, status_code=status.HTTP_201_CREATED)
def create_experiment(
    exp_in: ExperimentCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
) -> Any:
    """Save a laboratory benchmark experiment run."""
    experiment = Experiment(
        name=exp_in.name or exp_in.title or "Scaling Experiment",
        problem_id=exp_in.problem_id,
        user_id=current_user.id if current_user else None,
        algorithm_ids=exp_in.algorithm_ids,
        input_sizes=exp_in.input_sizes or [50, 100, 250, 500, 1000],
        dataset_distribution=exp_in.dataset_distribution or "random",
        repetitions=exp_in.repetitions or 3,
        results_summary=exp_in.results or {},
        asymptotic_fit_summary=exp_in.recommendations or {},
        conclusion_notes=exp_in.description
    )
    db.add(experiment)
    db.commit()
    db.refresh(experiment)
    return experiment


@router.delete("/{exp_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_experiment(
    exp_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> None:
    """Delete an experiment (owner or admin only)."""
    exp = db.query(Experiment).filter(Experiment.id == exp_id).first()
    if not exp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiment not found.")
    if exp.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this experiment.")

    db.delete(exp)
    db.commit()


@router.get("/{exp_id}/export")
def export_experiment(
    exp_id: str,
    format: str = Query("json", description="Export format: json or markdown"),
    db: Session = Depends(get_db)
) -> Any:
    """Export structured 10-section academic experiment benchmark report."""
    exp = db.query(Experiment).filter(Experiment.id == exp_id).first()
    if not exp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiment not found.")

    if format.lower() == "markdown":
        md = generate_10_section_academic_markdown(exp)
        return PlainTextResponse(content=md, media_type="text/markdown")

    # Structured 10-section academic JSON
    algos = exp.algorithm_ids or []
    algo_meta_list = [RecommendationEngine._resolve_algo_metadata(slug) for slug in algos]
    results_data = exp.results_summary if isinstance(exp.results_summary, dict) else {}
    mcda_data = exp.asymptotic_fit_summary if isinstance(exp.asymptotic_fit_summary, dict) else {}

    # Calculate valid speedups
    all_final_times: Dict[str, float] = {}
    for algo_slug, data in results_data.items():
        if isinstance(data, list) and data:
            last_pt = data[-1]
            t = float(last_pt.get('mean_ms', last_pt.get('time_ms', 0.0)))
            if t > 0:
                all_final_times[algo_slug] = t

    speedups = {}
    if len(all_final_times) > 1:
        slowest = max(all_final_times.values())
        for s, t in all_final_times.items():
            speedups[s] = {
                "measured_ms": t,
                "speedup_vs_slowest": round(slowest / t, 2) if t > 0 else 1.0,
            }

    return JSONResponse(content={
        "academic_report": {
            "section_1_problem_definition": {
                "experiment_id": exp.id,
                "experiment_name": exp.name,
                "problem_id": exp.problem_id,
                "created_at": exp.created_at.isoformat() if exp.created_at else None,
            },
            "section_2_algorithms_evaluated": algo_meta_list,
            "section_3_experimental_setup": {
                "repetitions": exp.repetitions,
                "timer": "monotonic_perf_counter_ns",
                "memory_profiler": "tracemalloc_peak_kb",
            },
            "section_4_input_characteristics": {
                "input_sizes": exp.input_sizes,
                "distribution": exp.dataset_distribution,
            },
            "section_5_theoretical_complexity": [
                {
                    "slug": m["slug"],
                    "best": m["best"],
                    "average": m["avg"],
                    "worst": m["worst"],
                    "space": m["space"],
                    "is_stable": m["stable"],
                    "is_in_place": m["in_place"],
                }
                for m in algo_meta_list
            ],
            "section_6_measured_benchmark_results": results_data,
            "section_7_speedup_calculations": speedups,
            "section_8_mcda_scoring_breakdown": mcda_data.get("rankings", []),
            "section_9_recommendation": {
                "recommended_algorithm": mcda_data.get("recommended_algorithm"),
                "recommended_name": mcda_data.get("recommended_name"),
                "winning_score": mcda_data.get("winning_score"),
                "justification": mcda_data.get("justification") or exp.conclusion_notes,
                "explanation": mcda_data.get("explanation"),
            },
            "section_10_limitations_and_conclusions": {
                "empirical_claim_boundary": "Empirical benchmarks evaluate concrete runtime characteristics but do not replace asymptotic proofs.",
                "conclusion_notes": exp.conclusion_notes or "Benchmarking completed successfully.",
            },
        },
        "raw": {
            "id": exp.id,
            "name": exp.name,
            "problem_id": exp.problem_id,
            "created_at": exp.created_at.isoformat() if exp.created_at else None,
            "algorithm_ids": exp.algorithm_ids,
            "input_sizes": exp.input_sizes,
            "dataset_distribution": exp.dataset_distribution,
            "results_summary": exp.results_summary,
            "asymptotic_fit_summary": exp.asymptotic_fit_summary,
            "conclusion_notes": exp.conclusion_notes,
        }
    })
