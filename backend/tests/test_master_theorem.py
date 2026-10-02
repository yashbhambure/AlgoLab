"""
Automated Test Suite for Master Theorem Solver.
Validates Cases 1, 2, 3, extended logarithmic cases, regularity condition, and input validations.
"""
import pytest
from app.complexity.master_theorem import MasterTheoremSolver


class TestMasterTheoremSolver:
    """Test suite for Master Theorem analytical recurrence solver."""

    def test_case_1_leaf_dominated(self):
        """
        Strassen-like recurrence: T(n) = 7T(n/2) + Theta(n^2)
        c_crit = log2(7) ≈ 2.8074 > k = 2 -> Case 1 -> Theta(n^2.8074)
        """
        res = MasterTheoremSolver.solve(a=7, b=2, k=2)
        assert res["case_number"] == 1
        assert "Case 1" in res["case"]
        assert "n^2.8074" in res["complexity"] or "n^{2.8074}" in res["latex"]
        assert res["critical_exponent"] == 2.8074

    def test_case_2_balanced_standard(self):
        """
        Merge Sort: T(n) = 2T(n/2) + Theta(n)
        c_crit = log2(2) = 1 == k = 1, p = 0 -> Case 2 -> Theta(n log n)
        """
        res = MasterTheoremSolver.solve(a=2, b=2, k=1, p=0)
        assert res["case_number"] == 2
        assert "Case 2" in res["case"]
        assert "Theta(n * log(n))" in res["complexity"] or "Theta(n log(n))" in res["complexity"]

    def test_case_2_binary_search(self):
        """
        Binary Search: T(n) = T(n/2) + Theta(1)
        c_crit = log2(1) = 0 == k = 0, p = 0 -> Case 2 -> Theta(log n)
        """
        res = MasterTheoremSolver.solve(a=1, b=2, k=0, p=0)
        assert res["case_number"] == 2
        assert "log(n)" in res["complexity"]

    def test_case_2_extended_logarithmic_neg_1(self):
        """
        Extended Case 2: T(n) = 2T(n/2) + Theta(n / log n) -> p = -1
        c_crit = 1 == k = 1, p = -1 -> Case 2 -> Theta(n * log(log(n)))
        """
        res = MasterTheoremSolver.solve(a=2, b=2, k=1, p=-1)
        assert res["case_number"] == 2
        assert "log(log(n))" in res["complexity"]

    def test_case_2_extended_logarithmic_less_than_neg_1(self):
        """
        Extended Case 2: T(n) = 2T(n/2) + Theta(n / log^2 n) -> p = -2
        c_crit = 1 == k = 1, p = -2 -> Case 2 -> Theta(n)
        """
        res = MasterTheoremSolver.solve(a=2, b=2, k=1, p=-2)
        assert res["case_number"] == 2
        assert "Theta(n)" in res["complexity"]

    def test_case_3_root_dominated(self):
        """
        Root heavy: T(n) = 3T(n/4) + Theta(n^2)
        c_crit = log4(3) ≈ 0.7925 < k = 2 -> Case 3 -> Theta(n^2)
        Regularity: a / (b^k) = 3 / (4^2) = 3/16 = 0.1875 < 1 -> SATISFIED
        """
        res = MasterTheoremSolver.solve(a=3, b=4, k=2, p=0)
        assert res["case_number"] == 3
        assert "Case 3" in res["case"]
        assert "Theta(n^2)" in res["complexity"]
        assert res["regularity_satisfied"] is True

    def test_parameter_validation_errors(self):
        """Validates error throwing on illegal Master Theorem parameters."""
        with pytest.raises(ValueError, match="subproblems.*must be >= 1"):
            MasterTheoremSolver.solve(a=0.5, b=2, k=1)

        with pytest.raises(ValueError, match="factor.*must be > 1"):
            MasterTheoremSolver.solve(a=2, b=1.0, k=1)

        with pytest.raises(ValueError, match="polynomial exponent.*must be >= 0"):
            MasterTheoremSolver.solve(a=2, b=2, k=-1)
