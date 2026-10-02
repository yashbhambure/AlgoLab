"""
Multi-Criteria Decision Analysis (MCDA) Algorithm Recommendation Engine.
Evaluates candidates across theoretical complexity, empirical benchmarks, space efficiency,
input dataset characteristics, and user constraints with rigorous academic explainability.
"""
from typing import Dict, Any, List, Optional
from app.algorithms.registry import registry
from app.recommendation.input_analyzer import InputAnalyzer
from app.curriculum.curriculum_data import CURRICULUM_MODULES, get_algorithm_curriculum_info


class RecommendationEngine:
    """
    Intelligent DAA Recommendation Engine powered by Multi-Criteria Decision Analysis.
    """

    COMPLEXITY_SCORES = {
        "O(1)": 100.0,
        "O(log log n)": 98.0,
        "O(log n)": 95.0,
        "O(sqrt(n))": 90.0,
        "O(n)": 85.0,
        "O(n + k)": 82.0,
        "O(nk)": 80.0,
        "O(n log n)": 75.0,
        "O(E log V)": 72.0,
        "O(E log E)": 72.0,
        "O(V + E)": 80.0,
        "O((V + E) log V)": 72.0,
        "O(n^2.8074)": 40.0,
        "O(nW)": 50.0,
        "O(n*W)": 50.0,
        "O(n * W)": 50.0,
        "O(nu)": 50.0,
        "O(n C^2)": 45.0,
        "O(mn)": 50.0,
        "O(m*n)": 50.0,
        "O(VE)": 45.0,
        "O(V * E)": 45.0,
        "O(n log n + n * d_max)": 45.0,
        "O(n^2)": 40.0,
        "O(n^3)": 25.0,
        "O(V^3)": 25.0,
        "O(n^2 2^n)": 15.0,
        "O(n 2^n)": 18.0,
        "O(2^n)": 10.0,
        "O(m^n)": 8.0,
        "O(n!)": 5.0,
        "O(N!)": 5.0,
        "O(V!)": 5.0,
    }

    SPACE_SCORES = {
        "O(1)": 100.0,
        "O(log n)": 85.0,
        "O(n)": 65.0,
        "O(N)": 65.0,
        "O(V)": 65.0,
        "O(n + k)": 55.0,
        "O(k)": 60.0,
        "O(d_max)": 65.0,
        "O(V + E)": 60.0,
        "O(V^2)": 35.0,
        "O(n^2)": 35.0,
        "O(nW)": 40.0,
        "O(n*W)": 40.0,
        "O(n * W)": 40.0,
        "O(nu)": 40.0,
        "O(n C)": 40.0,
        "O(n 2^n)": 15.0,
        "O(2^n)": 10.0,
        "O(n!)": 5.0,
        "O(N!)": 5.0,
        "O(V!)": 5.0,
    }

    # Authoritative Complexity Specifications for Canonical 23 Curriculum Implementations
    CANONICAL_PROPERTIES = {
        # Module 1: Divide-and-Conquer Algorithm
        "defective-chessboard": {"best": "O(n^2)", "avg": "O(n^2)", "worst": "O(n^2)", "space": "O(n^2)", "stable": False, "in_place": False},
        "max-min-divide-conquer": {"best": "O(n)", "avg": "O(n)", "worst": "O(n)", "space": "O(log n)", "stable": False, "in_place": True},
        "strassen-matrix-multiplication": {"best": "O(n^2.8074)", "avg": "O(n^2.8074)", "worst": "O(n^2.8074)", "space": "O(n^2)", "stable": False, "in_place": False},
        # Module 2: Backtracking Algorithm
        "n-queens-backtracking": {"best": "O(N!)", "avg": "O(N!)", "worst": "O(N!)", "space": "O(N)", "stable": False, "in_place": True},
        "subset-sum-backtracking": {"best": "O(2^n)", "avg": "O(2^n)", "worst": "O(2^n)", "space": "O(n)", "stable": False, "in_place": True},
        "hamiltonian-cycle-backtracking": {"best": "O(N!)", "avg": "O(N!)", "worst": "O(N!)", "space": "O(N)", "stable": False, "in_place": True},
        # Module 3: Dynamic Programming Algorithm
        "multistage-graph-dp": {"best": "O(V + E)", "avg": "O(V + E)", "worst": "O(V + E)", "space": "O(V)", "stable": False, "in_place": False},
        "floyd-warshall-apsp": {"best": "O(V^3)", "avg": "O(V^3)", "worst": "O(V^3)", "space": "O(V^2)", "stable": False, "in_place": False},
        "optimal-bst-dp": {"best": "O(n^3)", "avg": "O(n^3)", "worst": "O(n^3)", "space": "O(n^2)", "stable": False, "in_place": False},
        "0-1-knapsack-dp": {"best": "O(nW)", "avg": "O(nW)", "worst": "O(nW)", "space": "O(nW)", "stable": False, "in_place": False},
        "traveling-salesman-dp": {"best": "O(n^2 2^n)", "avg": "O(n^2 2^n)", "worst": "O(n^2 2^n)", "space": "O(n 2^n)", "stable": False, "in_place": False},
        "reliability-design-dp": {"best": "O(nu)", "avg": "O(nu)", "worst": "O(nu)", "space": "O(nu)", "stable": False, "in_place": False},
        # Module 4: Greedy Method Algorithm
        "optimal-storage-tapes-greedy": {"best": "O(n log n)", "avg": "O(n log n)", "worst": "O(n log n)", "space": "O(n)", "stable": False, "in_place": False},
        "fractional-knapsack": {"best": "O(n log n)", "avg": "O(n log n)", "worst": "O(n log n)", "space": "O(1)", "stable": False, "in_place": True},
        "job-sequencing-deadlines": {"best": "O(n^2)", "avg": "O(n^2)", "worst": "O(n^2)", "space": "O(n)", "stable": False, "in_place": False},
        "optimal-merge-patterns-greedy": {"best": "O(n log n)", "avg": "O(n log n)", "worst": "O(n log n)", "space": "O(n)", "stable": False, "in_place": False},
        "kruskal-mst": {"best": "O(E log E)", "avg": "O(E log E)", "worst": "O(E log E)", "space": "O(V + E)", "stable": False, "in_place": False},
        "prim-mst": {"best": "O(E log V)", "avg": "O(E log V)", "worst": "O(E log V)", "space": "O(V)", "stable": False, "in_place": False},
        "dijkstra-sssp": {"best": "O((V + E) log V)", "avg": "O((V + E) log V)", "worst": "O((V + E) log V)", "space": "O(V)", "stable": False, "in_place": False},
        "bellman-ford-sssp": {"best": "O(V * E)", "avg": "O(V * E)", "worst": "O(V * E)", "space": "O(V)", "stable": False, "in_place": False},
        # Module 5: Branch and Bound Algorithm
        "0-1-knapsack-lc-bb": {"best": "O(n)", "avg": "O(2^n)", "worst": "O(2^n)", "space": "O(2^n)", "stable": False, "in_place": False},
        "0-1-knapsack-fifo-bb": {"best": "O(n)", "avg": "O(2^n)", "worst": "O(2^n)", "space": "O(2^n)", "stable": False, "in_place": False},
        "traveling-salesman-bb": {"best": "O(n^2 2^n)", "avg": "O(n^2 2^n)", "worst": "O(n^2 2^n)", "space": "O(n^2 2^n)", "stable": False, "in_place": False},
    }

    WEIGHT_PROFILES = {
        "speed": {"theo": 0.35, "emp": 0.35, "space": 0.10, "input": 0.15, "req": 0.05},
        "memory": {"theo": 0.15, "emp": 0.10, "space": 0.50, "input": 0.10, "req": 0.15},
        "stability": {"theo": 0.20, "emp": 0.15, "space": 0.15, "input": 0.10, "req": 0.40},
        "balanced": {"theo": 0.25, "emp": 0.25, "space": 0.20, "input": 0.20, "req": 0.10},
    }

    @classmethod
    def _resolve_algo_metadata(cls, slug: str) -> Dict[str, Any]:
        """
        Dynamically extracts authoritative metadata from registry, curriculum data,
        and canonical properties.
        """
        algo = registry.get(slug)
        canon = cls.CANONICAL_PROPERTIES.get(slug, {})
        curr_info = get_algorithm_curriculum_info(slug)
        is_curriculum = curr_info is not None

        if canon:
            name = getattr(algo, "name", slug.replace("-", " ").title())
            category = getattr(algo, "category", curr_info["module_name"] if curr_info else "General")
            paradigm = getattr(algo, "paradigm", curr_info["module_name"] if curr_info else "General")
            return {
                "slug": slug,
                "name": name,
                "category": category,
                "paradigm": paradigm,
                "best": canon["best"],
                "avg": canon["avg"],
                "worst": canon["worst"],
                "space": canon["space"],
                "stable": canon["stable"],
                "in_place": canon["in_place"],
                "is_curriculum": is_curriculum,
            }

        if algo:
            return {
                "slug": slug,
                "name": getattr(algo, "name", slug.replace("-", " ").title()),
                "category": getattr(algo, "category", "General"),
                "paradigm": getattr(algo, "paradigm", "General"),
                "best": getattr(algo, "time_complexity_best", "O(n)"),
                "avg": getattr(algo, "time_complexity_average", "O(n log n)"),
                "worst": getattr(algo, "time_complexity_worst", "O(n^2)"),
                "space": getattr(algo, "space_complexity", "O(1)"),
                "stable": getattr(algo, "is_stable", False),
                "in_place": getattr(algo, "is_in_place", True),
                "is_curriculum": is_curriculum,
            }

        # Check curriculum module topic fallback
        for mod in CURRICULUM_MODULES:
            for top in mod.get("topics", []):
                if top.get("slug") == slug or top.get("algorithm_slug") == slug:
                    t_comp = top.get("time_complexity", "O(n log n)")
                    s_comp = top.get("space_complexity", "O(1)")
                    return {
                        "slug": slug,
                        "name": top.get("name", slug.replace("-", " ").title()),
                        "category": mod.get("short_name", "Curriculum"),
                        "paradigm": mod.get("name", "Curriculum"),
                        "best": t_comp,
                        "avg": t_comp,
                        "worst": t_comp,
                        "space": s_comp,
                        "stable": False,
                        "in_place": "O(1)" in s_comp,
                        "is_curriculum": True,
                    }

        # Fallback for unknown / unmapped slugs
        return {
            "slug": slug,
            "name": slug.replace("-", " ").title(),
            "category": "General",
            "paradigm": "General",
            "best": "O(n)",
            "avg": "O(n log n)",
            "worst": "O(n^2)",
            "space": "O(1)",
            "stable": False,
            "in_place": True,
            "is_curriculum": False,
        }

    @classmethod
    def recommend(
        cls,
        candidate_slugs: List[str],
        input_data: Optional[Any] = None,
        empirical_results: Optional[List[Dict[str, Any]]] = None,
        objective: str = "balanced",
        require_stable: bool = False,
        require_in_place: bool = False,
        custom_weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Generates an MCDA ranked recommendation with complete academic reasoning and trade-off matrices.
        """
        weights = custom_weights or cls.WEIGHT_PROFILES.get(objective.lower(), cls.WEIGHT_PROFILES["balanced"])

        # 1. Analyze input characteristics
        input_props = InputAnalyzer.analyze(input_data) if input_data is not None else {}
        input_size = input_props.get("size", 0)

        # 2. Extract empirical benchmark timings if supplied
        empirical_times: Dict[str, float] = {}
        has_empirical_data = False
        if empirical_results:
            for item in empirical_results:
                slug = item.get("algorithm_slug")
                t_ms = item.get("execution_time_ms", item.get("time_stats", {}).get("mean_ms"))
                if slug and t_ms is not None:
                    empirical_times[slug] = max(1e-6, float(t_ms))
                    has_empirical_data = True

        min_empirical_time = min(empirical_times.values()) if empirical_times else None

        evaluations = []

        for slug in candidate_slugs:
            meta = cls._resolve_algo_metadata(slug)
            algo_name = meta["name"]
            algo_cat = meta["category"]
            algo_par = meta["paradigm"]
            worst_str = meta["worst"]
            avg_str = meta["avg"]
            best_str = meta["best"]
            space_str = meta["space"]
            is_stable = meta["stable"]
            is_in_place = meta["in_place"]

            # A. Theoretical Score (S_theo)
            theo_worst = cls.COMPLEXITY_SCORES.get(worst_str, 45.0)
            theo_avg = cls.COMPLEXITY_SCORES.get(avg_str, 50.0)
            s_theo = 0.4 * theo_worst + 0.6 * theo_avg

            # B. Empirical Score (S_emp)
            measured_time = empirical_times.get(slug)
            if min_empirical_time and measured_time is not None:
                s_emp = (min_empirical_time / measured_time) * 100.0
            else:
                s_emp = s_theo  # Theoretical proxy when unmeasured

            # C. Space Score (S_mem)
            s_mem = cls.SPACE_SCORES.get(space_str, 60.0)
            if is_in_place:
                s_mem = max(s_mem, 90.0)

            # D. Input Suitability Score (S_input)
            s_input = 70.0  # baseline
            reasons_input = []

            # Sorting/Searching heuristics
            if input_props.get("type") == "array":
                if input_size > 0 and input_size <= 30:
                    if slug in ["insertion-sort"]:
                        s_input += 25.0
                        reasons_input.append(f"Practical Heuristic: Small input size (N={input_size}) gives Insertion Sort low constant-factor overhead.")
                    elif slug in ["bubble-sort", "selection-sort"]:
                        s_input += 10.0
                    elif slug in ["merge-sort", "strassen-matrix-multiplication"]:
                        s_input -= 15.0
                        reasons_input.append("Practical Heuristic: Recursive divide-and-conquer overhead is comparatively heavy for small N.")

                if input_props.get("is_nearly_sorted"):
                    if slug in ["insertion-sort"]:
                        s_input += 30.0
                        reasons_input.append(f"Practical Heuristic: High sortedness ratio ({input_props.get('sortedness_ratio', 1.0)*100:.1f}%) triggers Insertion Sort's near-linear O(N) performance.")
                    elif slug in ["bubble-sort"]:
                        s_input += 15.0
                    elif slug in ["quick-sort"]:
                        s_input -= 10.0
                        reasons_input.append("Practical Heuristic: Nearly sorted data can risk unbalanced partitioning in naive Quick Sort.")

                if input_size > 1000:
                    if avg_str in ["O(n^2)", "O(n^3)", "O(2^n)", "O(N!)", "O(n!)"]:
                        s_input -= 40.0
                        reasons_input.append(f"Practical Heuristic: Input size N={input_size} makes {avg_str} quadratic/exponential runtime prohibitive.")
                    elif avg_str in ["O(n log n)", "O(n)", "O(n + k)"]:
                        s_input += 20.0
                        reasons_input.append(f"Practical Heuristic: Asymptotically efficient {avg_str} scaling is advantageous for large datasets (N={input_size}).")

                if input_props.get("is_integer_only") and input_props.get("value_range") is not None:
                    v_range = input_props["value_range"]
                    if v_range <= 5 * max(1, input_size) and slug in ["counting-sort", "radix-sort"]:
                        s_input += 25.0
                        reasons_input.append(f"Formal Property: Bounded integer range (K={v_range} <= 5N) enables non-comparison {algo_name} to run in O(N+K) time.")

            # Graph heuristics
            elif input_props.get("type") == "graph":
                if input_props.get("has_negative_weights"):
                    if slug in ["dijkstra-sssp", "dijkstra-greedy"]:
                        s_input = 0.0  # Disqualified
                        reasons_input.append("DISQUALIFICATION: Dijkstra's algorithm cannot handle negative edge weights (mathematically invalid greediness).")
                    elif slug in ["bellman-ford-sssp", "floyd-warshall-apsp"]:
                        s_input += 30.0
                        reasons_input.append("Formal Property: Bellman-Ford / Floyd-Warshall correctly relaxes negative edge weights and detects negative cycles.")
                else:
                    if slug in ["dijkstra-sssp"]:
                        s_input += 25.0
                        reasons_input.append("Formal Property: Non-negative graph weights guarantee greedy optimal expansion in O((V+E) log V).")

            s_input = max(0.0, min(100.0, s_input))

            # E. User Requirements Score (S_req)
            s_req = 100.0
            reasons_req = []
            if require_stable:
                if is_stable:
                    reasons_req.append("Constraint Satisfied: Algorithm is provably Stable.")
                else:
                    s_req -= 60.0
                    reasons_req.append("Constraint Penalty: Violates requested Stability constraint.")

            if require_in_place:
                if is_in_place:
                    reasons_req.append("Constraint Satisfied: Algorithm operates In-Place.")
                else:
                    s_req -= 50.0
                    reasons_req.append(f"Constraint Penalty: Violates In-Place constraint (allocates {space_str} auxiliary space).")

            s_req = max(0.0, min(100.0, s_req))

            # Total Composite Score
            s_total = (
                weights["theo"] * s_theo +
                weights["emp"] * s_emp +
                weights["space"] * s_mem +
                weights["input"] * s_input +
                weights["req"] * s_req
            )
            s_total = round(max(0.0, min(100.0, s_total)), 2)

            breakdown_dict = {
                "theoretical_score": round(s_theo, 2),
                "empirical_score": round(s_emp, 2),
                "space_score": round(s_mem, 2),
                "input_suitability_score": round(s_input, 2),
                "requirements_score": round(s_req, 2),
                # Aliases for backwards test compatibility
                "theoretical": round(s_theo, 2),
                "empirical": round(s_emp, 2),
                "space": round(s_mem, 2),
                "space_efficiency": round(s_mem, 2),
                "input_suitability": round(s_input, 2),
                "requirements": round(s_req, 2),
                "user_requirements": round(s_req, 2),
            }

            evaluations.append({
                "algorithm_slug": slug,
                "algorithm_name": algo_name,
                "paradigm": algo_par,
                "category": algo_cat,
                "score": s_total,
                "breakdown": breakdown_dict,
                "scores": breakdown_dict,
                "complexities": {
                    "best": best_str,
                    "average": avg_str,
                    "worst": worst_str,
                    "space": space_str,
                },
                "is_stable": is_stable,
                "is_in_place": is_in_place,
                "input_reasons": reasons_input,
                "requirement_reasons": reasons_req,
                "empirical_time_ms": measured_time,
            })

        # Sort by total score descending
        evaluations.sort(key=lambda x: x["score"], reverse=True)

        winner = evaluations[0] if evaluations else None

        # Build comprehensive academic explainability narrative
        explanation = cls._generate_explanation(winner, evaluations, input_props, objective, has_empirical_data)

        return {
            "objective": objective,
            "weights_used": weights,
            "input_properties": input_props,
            "has_empirical_data": has_empirical_data,
            "recommended_algorithm": winner["algorithm_slug"] if winner else None,
            "recommended_name": winner["algorithm_name"] if winner else None,
            "winning_score": winner["score"] if winner else 0.0,
            "explanation": explanation,
            "justification": explanation.get("summary", "") if explanation else "",
            "rankings": evaluations,
            "trade_offs": cls._generate_tradeoff_matrix(evaluations),
            "tradeoff_matrix": cls._generate_tradeoff_matrix(evaluations),
        }

    @classmethod
    def _generate_explanation(
        cls,
        winner: Optional[Dict[str, Any]],
        all_evals: List[Dict[str, Any]],
        input_props: Dict[str, Any],
        objective: str,
        has_empirical_data: bool
    ) -> Dict[str, Any]:
        if not winner:
            return {
                "summary": "No candidate algorithms evaluated.",
                "formal_theoretical_reasoning": "N/A",
                "practical_heuristic_reasoning": "N/A",
                "empirical_benchmark_evidence": "N/A",
                "key_advantages": [],
                "runner_up_comparison": None,
                "disqualified_or_penalized": [],
            }

        w_name = winner["algorithm_name"]
        w_avg = winner["complexities"]["average"]
        w_worst = winner["complexities"]["worst"]
        w_space = winner["complexities"]["space"]

        summary = (
            f"Algorithm '{w_name}' is recommended with an MCDA composite score of {winner['score']}/100 "
            f"under the '{objective}' optimization objective."
        )

        formal_reasoning = (
            f"Theoretical Bounds: '{w_name}' exhibits average-case time complexity {w_avg}, "
            f"worst-case time complexity {w_worst}, and auxiliary space complexity {w_space}. "
            f"Asymptotic scaling guarantees favorable execution bounds under strict theoretical analysis."
        )

        heuristic_reasons = winner.get("input_reasons", [])
        if heuristic_reasons:
            heuristic_reasoning = "Practical Heuristics: " + " ".join(heuristic_reasons)
        else:
            heuristic_reasoning = (
                f"Practical Heuristics: Input profile ({input_props.get('type', 'general')}) fits the "
                f"operational characteristics of {w_name} without invoking penalizing thresholds."
            )

        if winner.get("empirical_time_ms") is not None:
            empirical_reasoning = (
                f"Empirical Benchmark Evidence: Measured mean execution time of {winner['empirical_time_ms']:.4f} ms "
                f"on the current experimental dataset."
            )
        else:
            empirical_reasoning = (
                "Empirical Benchmark Evidence: No direct empirical benchmark measurement was supplied; "
                "theoretical asymptotic complexity was utilized as proxy score."
            )

        key_advantages = []
        if winner["is_in_place"]:
            key_advantages.append("Operates strictly in-place (O(1) auxiliary space overhead).")
        if winner["is_stable"]:
            key_advantages.append("Maintains relative ordering of equal keys (Stable).")
        if winner.get("empirical_time_ms") is not None:
            key_advantages.append(f"Measured execution time: {winner['empirical_time_ms']:.4f} ms.")

        key_advantages.extend(winner.get("input_reasons", []))
        key_advantages.extend(winner.get("requirement_reasons", []))

        # Runner-up comparison
        runner_up_comparison = None
        if len(all_evals) > 1:
            runner = all_evals[1]
            diff = round(winner["score"] - runner["score"], 2)
            runner_up_comparison = (
                f"Ranked #{runner['algorithm_name']} second with a score of {runner['score']}/100 (score delta: {diff} pts). "
                f"While {runner['algorithm_name']} provides {runner['complexities']['average']} complexity, "
                f"{w_name} attained superior composite ranking across the evaluated multi-criteria dimensions."
            )

        disqualified_or_penalized = [
            {
                "algorithm": item["algorithm_name"],
                "reasons": item["input_reasons"] + item["requirement_reasons"]
            }
            for item in all_evals if (item["input_reasons"] or item["requirement_reasons"]) and item != winner
        ]

        return {
            "summary": summary,
            "formal_theoretical_reasoning": formal_reasoning,
            "practical_heuristic_reasoning": heuristic_reasoning,
            "empirical_benchmark_evidence": empirical_reasoning,
            "key_advantages": key_advantages,
            "runner_up_comparison": runner_up_comparison,
            "disqualified_or_penalized": disqualified_or_penalized,
        }

    @classmethod
    def _generate_tradeoff_matrix(cls, evaluations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        matrix = []
        for item in evaluations:
            matrix.append({
                "algorithm": item["algorithm_name"],
                "time_efficiency": item["breakdown"]["theoretical_score"],
                "memory_efficiency": item["breakdown"]["space_score"],
                "dataset_fitness": item["breakdown"]["input_suitability_score"],
                "constraint_compliance": item["breakdown"]["requirements_score"],
                "overall_score": item["score"]
            })
        return matrix
