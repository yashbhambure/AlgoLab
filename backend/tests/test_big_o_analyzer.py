"""
Automated Test Suite for Big-O Empirical Curve Fitting Analyzer.
Validates regression modeling, R^2, RMSE, AIC, and edge cases across complexity classes.
"""
import pytest
from app.complexity.big_o_analyzer import BigOAnalyzer


class TestBigOAnalyzer:
    """Test suite for empirical Big-O curve fitting."""

    def test_linear_curve_fitting(self):
        """Synthetic linear data should fit O(n) with R^2 near 1.0."""
        data = [(10, 10.2), (20, 20.1), (50, 49.8), (100, 100.5), (200, 199.9), (500, 501.2)]
        result = BigOAnalyzer.fit_curve(data)
        assert result["best_fit_complexity"] == "O(n)"
        assert result["best_r_squared"] > 0.99
        assert result["sample_count"] == 6

    def test_quadratic_curve_fitting(self):
        """Synthetic quadratic data should fit O(n^2) with high R^2."""
        data = [(10, 105), (20, 395), (30, 910), (40, 1620), (50, 2480)]
        result = BigOAnalyzer.fit_curve(data)
        assert result["best_fit_complexity"] == "O(n^2)"
        assert result["best_r_squared"] > 0.98

    def test_logarithmic_curve_fitting(self):
        """Synthetic logarithmic data should fit O(log n)."""
        import math
        data = [(10, 3.32), (50, 5.64), (100, 6.64), (500, 8.96), (1000, 9.96)]
        result = BigOAnalyzer.fit_curve(data)
        assert result["best_fit_complexity"] in ["O(log n)", "O(1)"]
        assert result["best_r_squared"] > 0.95

    def test_insufficient_data_points(self):
        """Should gracefully handle < 2 points without throwing unhandled exceptions."""
        result_empty = BigOAnalyzer.fit_curve([])
        assert "Insufficient" in result_empty["best_fit"]
        assert result_empty["r_squared"] == 0.0

        result_single = BigOAnalyzer.fit_curve([(10, 5.0)])
        assert "Insufficient" in result_single["best_fit"]
        assert result_single["r_squared"] == 0.0

    def test_fits_structure_and_metrics(self):
        """Ensure every fit entry contains required statistical metrics."""
        data = [(10, 15), (20, 32), (30, 48), (40, 63)]
        result = BigOAnalyzer.fit_curve(data)
        assert len(result["fits"]) > 0
        for fit in result["fits"]:
            assert "complexity" in fit
            assert "name" in fit
            assert "coefficient" in fit
            assert "r_squared" in fit
            assert "rmse" in fit
            assert "aic" in fit
            assert "predicted_curve" in fit
