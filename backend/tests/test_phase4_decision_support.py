"""
Phase 4 Decision Support and Academic Polish Test Suite.
Validates 23/23 curriculum algorithm MCDA coverage, dynamic metadata resolution,
decision tree traversal, constraint disqualification, benchmark -> MCDA data flow,
10-section academic export formatting, and theory-only isolation.
"""
import pytest
from app.algorithms.registry import registry
from app.curriculum.curriculum_data import CURRICULUM_MODULES
from app.recommendation.engine import RecommendationEngine
from app.recommendation.decision_tree import AlgorithmDecisionTree
from app.api.v1.experiments import generate_10_section_academic_markdown
from app.models.experiment import Experiment
from datetime import datetime


APPROVED_23_CURRICULUM_SLUGS = [
    # Module 1: Divide and Conquer (3)
    "defective-chessboard",
    "max-min-divide-conquer",
    "strassen-matrix-multiplication",
    # Module 2: Backtracking (3)
    "n-queens-backtracking",
    "subset-sum-backtracking",
    "hamiltonian-cycle-backtracking",
    # Module 3: Dynamic Programming (6)
    "multistage-graph-dp",
    "floyd-warshall-apsp",
    "optimal-bst-dp",
    "0-1-knapsack-dp",
    "traveling-salesman-dp",
    "reliability-design-dp",
    # Module 4: Greedy Method (8)
    "optimal-storage-tapes-greedy",
    "fractional-knapsack",
    "job-sequencing-deadlines",
    "optimal-merge-patterns-greedy",
    "kruskal-mst",
    "prim-mst",
    "dijkstra-sssp",
    "bellman-ford-sssp",
    # Module 5: Branch and Bound (3)
    "0-1-knapsack-lc-bb",
    "0-1-knapsack-fifo-bb",
    "traveling-salesman-bb",
]


class TestPhase4MCDACoverage:
    """Verifies all 23 authoritative curriculum algorithms are accounted for in MCDA."""

    def test_23_curriculum_coverage_count(self):
        assert len(APPROVED_23_CURRICULUM_SLUGS) == 23

    @pytest.mark.parametrize("slug", APPROVED_23_CURRICULUM_SLUGS)
    def test_mcda_evaluation_on_every_curriculum_algo(self, slug):
        res = RecommendationEngine.recommend(
            candidate_slugs=[slug],
            objective="balanced"
        )
        assert res["recommended_algorithm"] == slug
        assert res["winning_score"] > 0
        assert len(res["rankings"]) == 1
        ranking = res["rankings"][0]

        # Verify dynamic metadata fields
        assert "algorithm_name" in ranking
        assert "complexities" in ranking
        assert "breakdown" in ranking
        assert ranking["breakdown"]["theoretical_score"] > 0
        assert ranking["breakdown"]["space_score"] > 0

        # Verify explanation structure
        explanation = res["explanation"]
        assert "summary" in explanation
        assert "formal_theoretical_reasoning" in explanation
        assert "practical_heuristic_reasoning" in explanation
        assert "empirical_benchmark_evidence" in explanation

    def test_multi_candidate_ranking(self):
        candidates = ["0-1-knapsack-dp", "0-1-knapsack-lc-bb", "0-1-knapsack-fifo-bb"]
        res = RecommendationEngine.recommend(
            candidate_slugs=candidates,
            objective="speed"
        )
        assert len(res["rankings"]) == 3
        assert res["winning_score"] >= res["rankings"][1]["score"]
        assert res["explanation"]["runner_up_comparison"] is not None


class TestPhase4DynamicMetadataResolution:
    """Verifies dynamic resolution from registry/curriculum without hardcoded duplicate dicts."""

    def test_no_static_algo_metadata_dict(self):
        assert not hasattr(RecommendationEngine, "ALGO_METADATA")

    def test_resolve_metadata_registered(self):
        meta = RecommendationEngine._resolve_algo_metadata("strassen-matrix-multiplication")
        assert meta["name"] == "Strassen's Matrix Multiplication"
        assert meta["worst"] == "O(n^2.8074)"
        assert meta["is_curriculum"] is True

    def test_resolve_metadata_fallback_unknown(self):
        meta = RecommendationEngine._resolve_algo_metadata("custom-nonexistent-algo")
        assert meta["slug"] == "custom-nonexistent-algo"
        assert meta["is_curriculum"] is False


class TestPhase4ConstraintDisqualification:
    """Verifies technically defensible disqualification and constraint compliance."""

    def test_dijkstra_negative_weight_disqualification(self):
        graph_with_negatives = {
            "type": "graph",
            "has_negative_weights": True,
            "vertices": ["A", "B", "C"],
            "edges": [["A", "B", -5], ["B", "C", 2]],
        }
        res = RecommendationEngine.recommend(
            candidate_slugs=["dijkstra-sssp", "bellman-ford-sssp"],
            input_data=graph_with_negatives,
            objective="balanced"
        )
        assert res["recommended_algorithm"] == "bellman-ford-sssp"
        dijkstra_eval = next(r for r in res["rankings"] if r["algorithm_slug"] == "dijkstra-sssp")
        assert dijkstra_eval["breakdown"]["input_suitability_score"] == 0.0
        assert any("DISQUALIFICATION" in r for r in dijkstra_eval["input_reasons"])


class TestPhase4BenchmarkMCDADataFlow:
    """Verifies that measured empirical benchmark metrics are strictly preserved and not fabricated."""

    def test_empirical_measurements_preserved(self):
        empirical_data = [
            {"algorithm_slug": "kruskal-mst", "execution_time_ms": 2.5},
            {"algorithm_slug": "prim-mst", "execution_time_ms": 1.25},
        ]
        res = RecommendationEngine.recommend(
            candidate_slugs=["kruskal-mst", "prim-mst"],
            empirical_results=empirical_data,
            objective="speed"
        )
        assert res["has_empirical_data"] is True
        prim_eval = next(r for r in res["rankings"] if r["algorithm_slug"] == "prim-mst")
        kruskal_eval = next(r for r in res["rankings"] if r["algorithm_slug"] == "kruskal-mst")
        assert prim_eval["empirical_time_ms"] == 1.25
        assert kruskal_eval["empirical_time_ms"] == 2.5
        assert prim_eval["breakdown"]["empirical_score"] == 100.0
        assert kruskal_eval["breakdown"]["empirical_score"] == 50.0

    def test_unmeasured_algorithms_do_not_fabricate_empirical_time(self):
        res = RecommendationEngine.recommend(
            candidate_slugs=["strassen-matrix-multiplication"],
            empirical_results=None,
            objective="balanced"
        )
        assert res["has_empirical_data"] is False
        eval_item = res["rankings"][0]
        assert eval_item["empirical_time_ms"] is None
        assert "No direct empirical benchmark measurement was supplied" in res["explanation"]["empirical_benchmark_evidence"]


class TestPhase4DecisionTree:
    """Verifies interactive decision tree traversal and theory-only isolation."""

    def test_traverse_extrema_max_min(self):
        answers = {
            "root": "Divide and Conquer Problems",
            "dc_problem_type": "Simultaneous Maximum and Minimum Finding",
            "dc_max_min": "Optimal comparison bound (3n/2 - 2 comparisons)"
        }
        res = AlgorithmDecisionTree.traverse(answers)
        assert res["status"] == "completed"
        assert res["recommendation"]["algorithm_slug"] == "max-min-divide-conquer"

    def test_traverse_backtracking_nqueens(self):
        answers = {
            "root": "Backtracking & Constraint Satisfaction",
            "backtracking_problem_type": "N-Queens Non-Attacking Placement",
            "bt_nqueens": "Placing N queens on N x N board without conflict"
        }
        res = AlgorithmDecisionTree.traverse(answers)
        assert res["status"] == "completed"
        assert res["recommendation"]["algorithm_slug"] == "n-queens-backtracking"

    def test_traverse_branch_and_bound_knapsack(self):
        answers = {
            "root": "Branch and Bound Search",
            "bb_problem_type": "0/1 Knapsack Branch & Bound Search Strategies",
            "bb_knapsack_strategy": "Least-Cost (LC) Branch & Bound using upper bounding heuristic"
        }
        res = AlgorithmDecisionTree.traverse(answers)
        assert res["status"] == "completed"
        assert res["recommendation"]["algorithm_slug"] == "0-1-knapsack-lc-bb"

    def test_theory_modules_6_and_7_isolated(self):
        """Modules 6-7 (P, NP, NP-Hard, NP-Complete) remain conceptual and are not in tree."""
        tree = AlgorithmDecisionTree.get_tree()
        root_options = [opt["label"] for opt in tree["options"]]
        assert "P and NP Problems" not in root_options
        assert "NP-Hard and NP-Complete" not in root_options


class TestPhase4AcademicExport:
    """Verifies structured 10-section academic export format and speedup calculation."""

    def test_10_section_markdown_generation(self):
        exp = Experiment(
            id="exp-test-101",
            name="MST Asymptotic Empirical Study",
            problem_id="minimum-spanning-tree",
            algorithm_ids=["kruskal-mst", "prim-mst"],
            input_sizes=[10, 50, 100],
            dataset_distribution="random",
            repetitions=3,
            results_summary={
                "kruskal-mst": [{"n": 10, "mean_ms": 0.1}, {"n": 50, "mean_ms": 0.6}, {"n": 100, "mean_ms": 1.4}],
                "prim-mst": [{"n": 10, "mean_ms": 0.05}, {"n": 50, "mean_ms": 0.3}, {"n": 100, "mean_ms": 0.7}],
            },
            asymptotic_fit_summary={
                "recommended_algorithm": "prim-mst",
                "recommended_name": "Prim's MST",
                "winning_score": 92.5,
                "rankings": [
                    {"algorithm_slug": "prim-mst", "algorithm_name": "Prim's MST", "score": 92.5, "breakdown": {"theoretical_score": 75, "empirical_score": 100, "space_score": 85, "input_suitability_score": 90}},
                    {"algorithm_slug": "kruskal-mst", "algorithm_name": "Kruskal's MST", "score": 84.0, "breakdown": {"theoretical_score": 75, "empirical_score": 50, "space_score": 65, "input_suitability_score": 90}},
                ]
            },
            conclusion_notes="Prim's algorithm demonstrates ~2x empirical throughput over Kruskal on dense graph instances.",
            created_at=datetime.utcnow()
        )

        md = generate_10_section_academic_markdown(exp)

        # Check all 10 required sections
        assert "## 1. Problem Definition and Constraints" in md
        assert "## 2. Algorithms Evaluated" in md
        assert "## 3. Experimental Setup" in md
        assert "## 4. Input Sizes & Distribution Profiles" in md
        assert "## 5. Theoretical Asymptotic Complexity" in md
        assert "## 6. Measured Benchmark Results" in md
        assert "## 7. Relative Speedup Calculations" in md
        assert "## 8. MCDA Multi-Criteria Decision Breakdown" in md
        assert "## 9. Decision Support Recommendation" in md
        assert "## 10. Experimental Limitations & Academic Conclusion" in md

        # Verify speedup calculation presence
        assert "2.00x" in md
        # Verify theoretical vs empirical claim boundary statement
        assert "do not constitute formal mathematical proofs" in md
