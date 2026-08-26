"""Exact resource cost for the two-emitter fixed-marginal benchmark."""
from __future__ import annotations
import numpy as np


def partial_transpose_b(rho):
    a = np.asarray(rho, dtype=complex).reshape(2, 2, 2, 2)
    return a.transpose(0, 3, 2, 1).reshape(4, 4)


def negativity(rho, atol=1e-12):
    eig = np.linalg.eigvalsh(partial_transpose_b(rho))
    return float(np.sum(np.maximum(-eig.real, 0.0) * (np.abs(eig) > atol)))


def minimum_negativity_from_radius(r):
    """N_min(r)=max(0,r-1/2), 0<=r<=1."""
    r = float(r)
    if r < -1e-12 or r > 1 + 1e-12:
        raise ValueError("r must lie in [0,1]")
    return max(0.0, r - 0.5)


def optimal_x_state_for_radius(r, phase=0.0):
    """Fixed-I/2 state attaining the minimum negativity for r>=1/2.

    For r<1/2 this state is still physical but need not be separable-optimal;
    use the separable boundary mixtures from states.py for a zero-cost state.
    """
    r = float(r)
    if r < 0 or r > 1:
        raise ValueError("r must lie in [0,1]")
    a = (1.0 - r) / 2.0
    b = r / 2.0
    z = (r / 2.0) * np.exp(1j * phase)
    rho = np.array(
        [[a, 0, 0, 0], [0, b, z, 0], [0, z.conjugate(), b, 0], [0, 0, 0, a]],
        dtype=complex,
    )
    return rho
