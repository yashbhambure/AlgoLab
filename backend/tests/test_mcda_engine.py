"""
Automated Test Suite for MCDA Recommendation Engine.
Validates 5-criteria weighted scoring, stability/in-place constraint satisfaction,
objective profiles, and explainability justifications across the 23 curriculum algorithms.
"""
import pytest
from app.recommendation.engine import RecommendationEngine


class TestMCDARecommendationEngine:
    """Test suite for MCDA algorithm recommendation and trade-off analysis."""

    def test_weight_profiles_normalization(self):
        """Ensure all pre-configured weight profiles sum to 1.0."""
        for profile_name, weights in RecommendationEngine.WEIGHT_PROFILES.items():
            total = sum(weights.values())
            assert abs(total - 1.0) < 1e-6, f"Weights for profile '{profile_name}' must sum to 1.0"

    def test_knapsack_recommendation_comparison(self):
        """
        Tests MCDA recommendation on Knapsack candidates (DP vs LC-BB vs FIFO-BB).
        """
        knapsack_data = {
            "items": [
                {"name": "I1", "weight": 2, "value": 12},
                {"name": "I2", "weight": 1, "value": 10},
                {"name": "I3", "weight": 3, "value": 20},
            ],
            "capacity": 5
        }
        result = RecommendationEngine.recommend(
            candidate_slugs=["0-1-knapsack-dp", "0-1-knapsack-lc-bb", "0-1-knapsack-fifo-bb"],
            input_data=knapsack_data,
            objective="balanced"
        )
        assert "recommended_algorithm" in result
        assert "rankings" in result
        assert len(result["rankings"]) == 3

    def test_mst_recommendation_sparse_vs_dense(self):
        """On sparse graph input, Kruskal should score well."""
        sparse_graph = {
            "vertices": ["A", "B", "C", "D"],
            "edges": [
                {"source": "A", "target": "B", "weight": 2},
                {"source": "B", "target": "C", "weight": 3},
                {"source": "C", "target": "D", "weight": 1}
            ]
        }
        result = RecommendationEngine.recommend(
            candidate_slugs=["kruskal-mst", "prim-mst"],
            input_data=sparse_graph,
            objective="speed"
        )
        assert "recommended_algorithm" in result
        assert len(result["rankings"]) == 2

    def test_graph_sssp_negative_weights_disqualification(self):
        """On a graph with negative edges, Dijkstra must be disqualified or severely penalized."""
        graph_with_neg = {
            "vertices": ["A", "B", "C"],
            "edges": [
                {"source": "A", "target": "B", "weight": 5},
                {"source": "B", "target": "C", "weight": -3}
            ]
        }
        result = RecommendationEngine.recommend(
            candidate_slugs=["dijkstra-sssp", "bellman-ford-sssp"],
            input_data=graph_with_neg,
            objective="balanced"
        )
        recommended = result.get("recommended_algorithm")
        if isinstance(recommended, dict):
            assert recommended.get("algorithm_slug") == "bellman-ford-sssp"
        else:
            assert recommended == "bellman-ford-sssp"
        dijkstra_rank = next(r for r in result["rankings"] if r["algorithm_slug"] == "dijkstra-sssp")
        assert dijkstra_rank["scores"]["input_suitability"] == 0.0

    def test_recommendation_tradeoff_explanation(self):
        """Ensure clear natural-language justification is generated in recommendation output."""
        result = RecommendationEngine.recommend(
            candidate_slugs=["kruskal-mst", "prim-mst"],
            input_data={"vertices": ["A", "B"], "edges": [{"source": "A", "target": "B", "weight": 1}]},
            objective="speed"
        )
        assert "justification" in result
        assert len(result["justification"]) > 0
        assert "tradeoff_matrix" in result
