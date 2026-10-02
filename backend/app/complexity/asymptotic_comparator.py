"""
Asymptotic Comparator for DAA Complexity Classes.
Compares growth orders, provides asymptotic relations, and evaluates efficiency rankings.
"""
from typing import Dict, Any, List


class AsymptoticComparator:
    """
    Evaluates asymptotic dominance and hierarchy among complexity orders.
    """

    HIERARCHY = {
        "O(1)": 1,
        "O(log n)": 2,
        "O(sqrt(n))": 3,
        "O(n)": 4,
        "O(n log n)": 5,
        "O(n^2)": 6,
        "O(n^3)": 7,
        "O(2^n)": 8,
        "O(n!)": 9,
    }

    DESCRIPTIONS = {
        "O(1)": "Constant Time - Execution time is independent of input size.",
        "O(log n)": "Logarithmic Time - Problem size halves at each step (e.g. Binary Search, Balanced Trees).",
        "O(sqrt(n))": "Sublinear / Square Root Time - Block jumping / trial division.",
        "O(n)": "Linear Time - Single pass through the input elements.",
        "O(n log n)": "Linearithmic Time - Optimal comparison-based sorting divide-and-conquer lower bound.",
        "O(n^2)": "Quadratic Time - Nested iteration over input (e.g. standard Bubble/Selection sort).",
        "O(n^3)": "Cubic Time - Triple nested loops (e.g. standard Matrix Multiplication, Floyd-Warshall).",
        "O(2^n)": "Exponential Time - Exhaustive subset / recursive branching search.",
        "O(n!)": "Factorial Time - Permutation generation / Traveling Salesperson brute force.",
    }

    @classmethod
    def compare(cls, complexity_a: str, complexity_b: str) -> Dict[str, Any]:
        """
        Compares two complexity classes and determines which is asymptotically faster.
        """
        rank_a = cls.HIERARCHY.get(complexity_a, 5)
        rank_b = cls.HIERARCHY.get(complexity_b, 5)

        if rank_a < rank_b:
            relation = f"{complexity_a} is strictly asymptotically faster (dominates) than {complexity_b}"
            asymptotic_symbol = "<"
            winner = complexity_a
        elif rank_a > rank_b:
            relation = f"{complexity_b} is strictly asymptotically faster (dominates) than {complexity_a}"
            asymptotic_symbol = ">"
            winner = complexity_b
        else:
            relation = f"{complexity_a} and {complexity_b} have identical asymptotic growth rates: Theta({complexity_a})"
            asymptotic_symbol = "="
            winner = "Equivalent"

        return {
            "complexity_a": complexity_a,
            "complexity_b": complexity_b,
            "rank_a": rank_a,
            "rank_b": rank_b,
            "relation": relation,
            "asymptotic_symbol": asymptotic_symbol,
            "faster_complexity": winner,
            "description_a": cls.DESCRIPTIONS.get(complexity_a, "Custom Complexity"),
            "description_b": cls.DESCRIPTIONS.get(complexity_b, "Custom Complexity"),
        }

    @classmethod
    def get_full_hierarchy(cls) -> List[Dict[str, Any]]:
        """
        Returns the canonical DAA complexity hierarchy ordered from fastest to slowest.
        """
        sorted_hierarchy = sorted(cls.HIERARCHY.items(), key=lambda x: x[1])
        return [
            {
                "complexity": comp,
                "rank": rank,
                "description": cls.DESCRIPTIONS.get(comp, "")
            }
            for comp, rank in sorted_hierarchy
        ]
