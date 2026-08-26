"""Robustness identities for fixed-marginal response bodies."""
from __future__ import annotations
import numpy as np


def dephasing_scale(gamma_phi: float, t):
    """Scale q^2=exp(-2 gamma_phi t) of pair exchange coherences."""
    return np.exp(-2.0 * float(gamma_phi) * np.asarray(t, dtype=float))


def symmetric_three_gap(gamma_phi: float, t):
    """Exact support gap along c=(1,1,1) after local pure dephasing.

    Ideal h_Q=2, h_sep=3/2, so Delta=1/2. Both scale by exp(-2 gamma_phi t).
    """
    return 0.5 * dephasing_scale(gamma_phi, t)


def perturbation_safe(delta_ideal: float, operator_error_norm: float):
    """Sufficient gap-survival test Delta' >= Delta-2||dA|| > 0."""
    return float(delta_ideal) - 2.0 * float(operator_error_norm)
