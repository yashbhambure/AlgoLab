"""
Master Theorem Solver for Divide-and-Conquer Recurrence Relations.
Solves T(n) = a*T(n/b) + f(n) where f(n) = Theta(n^k * log^p(n)).
Supports standard and extended Master Theorem cases.
"""
import math
from typing import Dict, Any, List


class MasterTheoremSolver:
    """
    Solves recurrence relations of the form:
        T(n) = a * T(n/b) + f(n)
        where f(n) = Theta(n^k * log^p(n))
    """

    @classmethod
    def solve(cls, a: float, b: float, k: float, p: float = 0.0) -> Dict[str, Any]:
        """
        Solves T(n) = a * T(n/b) + Theta(n^k * log^p(n)).

        Parameters:
            a (float): Number of subproblems (a >= 1)
            b (float): Subproblem size reduction factor (b > 1)
            k (float): Exponent of n in work per level (k >= 0)
            p (float): Exponent of log(n) in work per level (default 0)

        Returns:
            Dictionary containing case name, solution complexity string, LaTeX representation,
            step-by-step derivation steps, and regularity check.
        """
        steps: List[str] = []

        if a < 1:
            raise ValueError("Parameter 'a' (subproblems) must be >= 1.")
        if b <= 1:
            raise ValueError("Parameter 'b' (factor) must be > 1.")
        if k < 0:
            raise ValueError("Parameter 'k' (polynomial exponent) must be >= 0.")

        # Step 1: Compute critical exponent c = log_b(a)
        c_crit = math.log(a, b)
        c_crit_round = round(c_crit, 4)

        steps.append(f"Given recurrence: T(n) = {a}*T(n/{b}) + Theta(n^{k} * log^{p}(n))")
        steps.append(f"Step 1: Compute the critical exponent c_crit = log_b(a) = log_{b}({a}) = {c_crit_round}")

        # Format f(n) description
        if p == 0:
            fn_str = f"n^{k}" if k != 1 and k != 0 else ("n" if k == 1 else "1")
        else:
            fn_str = f"n^{k} * log^{p}(n)" if k > 0 else f"log^{p}(n)"

        steps.append(f"Step 2: Compare f(n) = Theta({fn_str}) with n^(c_crit) = n^{c_crit_round}")

        eps = 1e-6
        diff = k - c_crit

        # Case 1: k < c_crit (i.e. f(n) = O(n^(log_b(a) - epsilon)))
        if diff < -eps:
            case = "Case 1: Leaf-heavy (Dominated by recursive subproblems)"
            explanation = (
                f"Since k = {k} < log_{b}({a}) = {c_crit_round}, the work done at leaves dominates. "
                f"Specifically, f(n) = O(n^(log_{b}({a}) - epsilon)) for epsilon = {round(-diff, 4)} > 0."
            )
            if abs(c_crit - round(c_crit)) < 1e-4:
                c_int = int(round(c_crit))
                theta_str = f"Theta(n^{c_int})" if c_int != 1 else "Theta(n)"
                latex_str = f"\\Theta(n^{{{c_int}}})" if c_int != 1 else "\\Theta(n)"
            else:
                theta_str = f"Theta(n^{c_crit_round})"
                latex_str = f"\\Theta(n^{{{c_crit_round}}})"

            steps.append(explanation)
            steps.append(f"Conclusion: T(n) = {theta_str}")

            return {
                "a": a,
                "b": b,
                "k": k,
                "p": p,
                "critical_exponent": c_crit_round,
                "case": case,
                "case_number": 1,
                "complexity": theta_str,
                "latex": latex_str,
                "regularity_satisfied": True,
                "explanation": explanation,
                "steps": steps
            }

        # Case 2: k == c_crit (i.e. f(n) = Theta(n^(log_b(a)) * log^p(n)))
        elif abs(diff) <= eps:
            case = "Case 2: Balanced (Work is evenly distributed across all tree levels)"
            if p > -1:
                p_next = p + 1
                p_next_str = f"log^{p_next}(n)" if p_next != 1 else "log(n)"
                c_val_str = f"n^{round(k, 2)}" if (k != 1 and k != 0) else ("n" if k == 1 else "")
                sep = " * " if c_val_str and p_next_str else ""
                theta_str = f"Theta({c_val_str}{sep}{p_next_str})"
                latex_c = f"n^{{{round(k, 2)}}}" if (k != 1 and k != 0) else ("n" if k == 1 else "")
                latex_p = f"\\log^{{{p_next}}}(n)" if p_next != 1 else "\\log(n)"
                latex_str = f"\\Theta({latex_c} {latex_p})"
                explanation = (
                    f"Since k = {k} == log_{b}({a}) = {c_crit_round} and p = {p} > -1, "
                    f"the work per level is identical. We multiply by a logarithmic depth factor log(n)."
                )
            elif abs(p + 1) <= 1e-6:
                # p = -1 -> Theta(n^k * log(log(n)))
                c_val_str = f"n^{round(k, 2)}" if (k != 1 and k != 0) else ("n" if k == 1 else "")
                theta_str = f"Theta({c_val_str} * log(log(n)))"
                latex_str = f"\\Theta({c_val_str} \\log(\\log(n)))"
                explanation = f"Extended Master Theorem: for p = -1, T(n) = Theta(n^(log_b(a)) * log(log(n)))."
            else:
                # p < -1 -> Theta(n^k)
                c_val_str = f"n^{round(k, 2)}" if (k != 1 and k != 0) else ("n" if k == 1 else "1")
                theta_str = f"Theta({c_val_str})"
                latex_str = f"\\Theta({c_val_str})"
                explanation = f"Extended Master Theorem: for p < -1, T(n) = Theta(n^(log_b(a)))."

            steps.append(explanation)
            steps.append(f"Conclusion: T(n) = {theta_str}")

            return {
                "a": a,
                "b": b,
                "k": k,
                "p": p,
                "critical_exponent": c_crit_round,
                "case": case,
                "case_number": 2,
                "complexity": theta_str,
                "latex": latex_str,
                "regularity_satisfied": True,
                "explanation": explanation,
                "steps": steps
            }

        # Case 3: k > c_crit (i.e. f(n) = Omega(n^(log_b(a) + epsilon)))
        else:
            case = "Case 3: Root-heavy (Dominated by root division work f(n))"
            # Regularity condition check: a * f(n/b) <= c * f(n) for c < 1
            # a * (n/b)^k <= c * n^k  =>  a / (b^k) < 1
            reg_ratio = a / (b ** k)
            regularity_ok = reg_ratio < 1.0

            explanation = (
                f"Since k = {k} > log_{b}({a}) = {c_crit_round}, the root work dominates. "
                f"Regularity condition: a / (b^k) = {a} / ({b}^{k}) = {round(reg_ratio, 4)} < 1. "
                f"Condition is {'SATISFIED' if regularity_ok else 'VIOLATED'}."
            )
            steps.append(explanation)

            if p == 0:
                fn_comp = f"n^{k}" if (k != 1 and k != 0) else ("n" if k == 1 else "1")
                latex_comp = f"n^{{{k}}}" if (k != 1 and k != 0) else ("n" if k == 1 else "1")
            else:
                fn_comp = f"n^{k} * log^{p}(n)" if k > 0 else f"log^{p}(n)"
                latex_comp = f"n^{{{k}}} \\log^{{{p}}}(n)" if k > 0 else f"\\log^{{{p}}}(n)"

            theta_str = f"Theta({fn_comp})"
            latex_str = f"\\Theta({latex_comp})"

            steps.append(f"Conclusion: T(n) = {theta_str}")

            return {
                "a": a,
                "b": b,
                "k": k,
                "p": p,
                "critical_exponent": c_crit_round,
                "case": case,
                "case_number": 3,
                "complexity": theta_str,
                "latex": latex_str,
                "regularity_satisfied": regularity_ok,
                "explanation": explanation,
                "steps": steps
            }
