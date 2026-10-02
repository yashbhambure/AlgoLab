"""
Empirical Big-O Curve Fitting and Asymptotic Complexity Analyzer.
Fits experimental data points (n, time) to theoretical complexity functions
via linear and non-linear regression, computing R^2, RMSE, and AIC.
"""
import math
from typing import List, Dict, Any, Tuple


class BigOAnalyzer:
    """
    Fits empirical benchmark series (n vs. execution time / operations)
    against standard asymptotic complexity classes.
    """

    COMPLEXITY_CLASSES = [
        ("O(1)", "Constant", lambda n: 1.0),
        ("O(log n)", "Logarithmic", lambda n: math.log2(n) if n > 1 else 0.1),
        ("O(n)", "Linear", lambda n: float(n)),
        ("O(n log n)", "Linearithmic", lambda n: float(n) * math.log2(n) if n > 1 else 0.1),
        ("O(n^2)", "Quadratic", lambda n: float(n) ** 2),
        ("O(n^3)", "Cubic", lambda n: float(n) ** 3),
        ("O(2^n)", "Exponential", lambda n: 2.0 ** min(float(n), 30)),
    ]

    @classmethod
    def fit_curve(cls, data_points: List[Tuple[float, float]]) -> Dict[str, Any]:
        """
        Fits data points [(n_1, t_1), (n_2, t_2), ...] to theoretical complexity models.

        Parameters:
            data_points: List of (input_size_n, execution_time_ms_or_ops)

        Returns:
            Dictionary with best_fit_class, all_fits list, and analysis summary.
        """
        if len(data_points) < 2:
            return {
                "best_fit": "Insufficient data (need >= 2 points)",
                "r_squared": 0.0,
                "fits": [],
                "data_points": data_points
            }

        # Filter valid points
        valid_points = [(float(n), max(1e-9, float(t))) for n, t in data_points if n > 0]
        if len(valid_points) < 2:
            return {
                "best_fit": "Insufficient valid data",
                "r_squared": 0.0,
                "fits": [],
                "data_points": data_points
            }

        n_samples = len(valid_points)
        y_values = [p[1] for p in valid_points]
        y_mean = sum(y_values) / n_samples
        ss_tot = sum((y - y_mean) ** 2 for y in y_values)

        fit_results = []

        for o_label, name, func in cls.COMPLEXITY_CLASSES:
            try:
                x_trans = [func(p[0]) for p in valid_points]
                # Linear regression y = c * x_trans through origin or with offset
                # For complexity: y = c * f(n)
                # c = sum(x_i * y_i) / sum(x_i^2)
                denom = sum(x ** 2 for x in x_trans)
                if denom == 0:
                    continue
                c = sum(x * y for x, y in zip(x_trans, y_values)) / denom
                if c < 0:
                    c = 1e-9

                # Predicted y
                y_pred = [c * x for x in x_trans]

                # Residual Sum of Squares
                ss_res = sum((y - yp) ** 2 for y, yp in zip(y_values, y_pred))

                # R^2 calculation
                r_squared = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
                r_squared = max(0.0, min(1.0, r_squared))

                # RMSE
                rmse = math.sqrt(ss_res / n_samples)

                # AIC (Akaike Information Criterion)
                # AIC = n * ln(ss_res/n) + 2*k
                if ss_res > 0:
                    aic = n_samples * math.log(ss_res / n_samples) + 2.0 * 1  # 1 parameter: c
                else:
                    aic = -9999.0

                fit_results.append({
                    "complexity": o_label,
                    "name": name,
                    "coefficient": round(c, 8),
                    "r_squared": round(r_squared, 5),
                    "rmse": round(rmse, 6),
                    "aic": round(aic, 4),
                    "predicted_curve": [{"n": p[0], "pred": round(yp, 6)} for p, yp in zip(valid_points, y_pred)]
                })
            except Exception:
                continue

        # Sort fits by R^2 descending (and lowest AIC / RMSE)
        fit_results.sort(key=lambda item: (-item["r_squared"], item["rmse"]))

        best_fit = fit_results[0] if fit_results else None

        return {
            "best_fit_complexity": best_fit["complexity"] if best_fit else "Unknown",
            "best_fit_name": best_fit["name"] if best_fit else "Unknown",
            "best_r_squared": best_fit["r_squared"] if best_fit else 0.0,
            "fits": fit_results,
            "sample_count": n_samples,
            "data_points": [{"n": p[0], "measured": round(p[1], 6)} for p in valid_points]
        }
