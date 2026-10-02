"""
Automated Test Suite for Interactive Algorithm Decision Tree.
Validates question traversal, leaf node recommendations, and slug alignment with the 23 curriculum algorithms.
"""
import pytest
from app.recommendation.decision_tree import AlgorithmDecisionTree
from app.algorithms.registry import registry


class TestAlgorithmDecisionTree:
    """Test suite for DAA Decision Tree engine."""

    def test_get_tree_structure(self):
        """Validates root node and top-level options."""
        tree = AlgorithmDecisionTree.get_tree()
        assert tree["id"] == "root"
        assert len(tree["options"]) >= 6
        assert "nodes" in tree

    def test_traversal_in_progress(self):
        """When partial answers are provided, returns next question."""
        res = AlgorithmDecisionTree.traverse({})
        assert res["status"] == "in_progress"
        assert res["current_node_id"] == "root"
        assert len(res["options"]) > 0

    def test_traversal_to_max_min_leaf(self):
        """Traverse: Divide and Conquer -> Max/Min."""
        answers = {
            "root": "Divide and Conquer Problems",
            "dc_problem_type": "Simultaneous Maximum and Minimum Finding",
            "dc_max_min": "Optimal comparison bound (3n/2 - 2 comparisons)"
        }
        res = AlgorithmDecisionTree.traverse(answers)
        assert res["status"] == "completed"
        assert "recommendation" in res
        slug = res["recommendation"]["algorithm_slug"]
        assert slug == "max-min-divide-conquer"
        assert registry.get(slug) is not None

    def test_traversal_to_knapsack_leaf(self):
        """Traverse: Knapsack -> 0/1 Knapsack -> DP Tabulation."""
        answers = {
            "root": "Knapsack / Resource Allocation",
            "knapsack_divisibility": "Discrete 0/1 choice per item",
            "knapsack_discrete_paradigm": "Dynamic Programming Tabulation"
        }
        res = AlgorithmDecisionTree.traverse(answers)
        assert res["status"] == "completed"
        assert "recommendation" in res
        slug = res["recommendation"]["algorithm_slug"]
        assert slug == "0-1-knapsack-dp"
        assert registry.get(slug) is not None

    def test_traversal_to_dijkstra_leaf(self):
        """Traverse: Shortest Path -> SSSP -> Non-negative -> Dijkstra."""
        answers = {
            "root": "Shortest Path in Graph",
            "shortest_path_type": "Single-Source Shortest Path (SSSP)",
            "sssp_weights": "No negative weights (Non-negative)"
        }
        res = AlgorithmDecisionTree.traverse(answers)
        assert res["status"] == "completed"
        slug = res["recommendation"]["algorithm_slug"]
        assert slug == "dijkstra-sssp"
        assert registry.get(slug) is not None

    def test_traversal_to_bellman_ford_leaf(self):
        """Traverse: Shortest Path -> SSSP -> Negative weights -> Bellman-Ford."""
        answers = {
            "root": "Shortest Path in Graph",
            "shortest_path_type": "Single-Source Shortest Path (SSSP)",
            "sssp_weights": "Negative edge weights exist (Potential negative cycles)"
        }
        res = AlgorithmDecisionTree.traverse(answers)
        assert res["status"] == "completed"
        slug = res["recommendation"]["algorithm_slug"]
        assert slug == "bellman-ford-sssp"
        assert registry.get(slug) is not None

    def test_traversal_to_floyd_warshall_leaf(self):
        """Traverse: Shortest Path -> APSP -> Floyd-Warshall."""
        answers = {
            "root": "Shortest Path in Graph",
            "shortest_path_type": "All-Pairs Shortest Path (APSP)"
        }
        res = AlgorithmDecisionTree.traverse(answers)
        assert res["status"] == "completed"
        slug = res["recommendation"]["algorithm_slug"]
        assert slug == "floyd-warshall-apsp"
        assert registry.get(slug) is not None

    def test_all_leaf_slugs_registered(self):
        """Verifies every leaf node in the entire tree points to an algorithm registered in registry."""
        tree = AlgorithmDecisionTree.get_tree()

        def collect_leaves(node_data):
            leaves = []
            for opt in node_data.get("options", []):
                if "leaf" in opt:
                    leaves.append(opt["leaf"]["algorithm_slug"])
            return leaves

        all_leaf_slugs = collect_leaves(tree)
        for node_id, node_data in tree.get("nodes", {}).items():
            all_leaf_slugs.extend(collect_leaves(node_data))

        assert len(all_leaf_slugs) > 0
        for slug in all_leaf_slugs:
            algo = registry.get(slug)
            assert algo is not None, f"Decision tree leaf slug '{slug}' is not registered in registry!"
