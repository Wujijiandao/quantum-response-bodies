"""Free-space cooperative couplings for identical two-level emitters.

The implementation uses the standard Lehmberg pair kernels for identical dipoles
in homogeneous free space. Distances are given in units of the resonant wavelength
by default, and rates are returned in units of the single-emitter decay rate gamma0.

For i != j, with xi = k0 r_ij and u = d_hat . r_hat,

Gamma_ij/gamma0 = (3/2)[(1-u^2) sin(xi)/xi
    + (1-3u^2)(cos(xi)/xi^2 - sin(xi)/xi^3)],

Omega_ij/gamma0 = -(3/4)[(1-u^2) cos(xi)/xi
    - (1-3u^2)(sin(xi)/xi^2 + cos(xi)/xi^3)].

Gamma_ii = gamma0. The single-emitter Lamb shift is absorbed into the transition
frequency, so Omega_ii = 0.
"""
from __future__ import annotations
import numpy as np


def _unit(v):
    v = np.asarray(v, dtype=float)
    n = np.linalg.norm(v)
    if n <= 0:
        raise ValueError("zero vector cannot be normalized")
    return v / n


def lehmberg_pair(r_vec, dipole=(0.0, 0.0, 1.0), wavelength=1.0, gamma0=1.0):
    """Return (Gamma_ij, Omega_ij) for one distinct emitter pair."""
    r_vec = np.asarray(r_vec, dtype=float)
    r = np.linalg.norm(r_vec)
    if r <= 0:
        raise ValueError("pair separation must be positive")
    if wavelength <= 0 or gamma0 < 0:
        raise ValueError("wavelength must be positive and gamma0 nonnegative")
    r_hat = r_vec / r
    d_hat = _unit(dipole)
    u = float(np.dot(d_hat, r_hat))
    x = 2.0 * np.pi * r / float(wavelength)
    a = 1.0 - u * u
    b = 1.0 - 3.0 * u * u
    sx, cx = np.sin(x), np.cos(x)
    gamma = 1.5 * gamma0 * (a * sx / x + b * (cx / x**2 - sx / x**3))
    omega = -0.75 * gamma0 * (a * cx / x - b * (sx / x**2 + cx / x**3))
    return float(gamma), float(omega)


def free_space_couplings(positions, dipole=(0.0, 0.0, 1.0), wavelength=1.0, gamma0=1.0):
    """Return collective decay Gamma and coherent exchange Omega matrices."""
    pos = np.asarray(positions, dtype=float)
    if pos.ndim != 2 or pos.shape[1] != 3:
        raise ValueError("positions must have shape (N,3)")
    n = len(pos)
    Gamma = np.eye(n, dtype=float) * gamma0
    Omega = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(i + 1, n):
            gij, oij = lehmberg_pair(pos[i] - pos[j], dipole, wavelength, gamma0)
            Gamma[i, j] = Gamma[j, i] = gij
            Omega[i, j] = Omega[j, i] = oij
    return Gamma, Omega


def equilateral_triangle(spacing=0.35):
    """Three coplanar emitter positions with side length `spacing`."""
    a = float(spacing)
    return np.array([[0.0, 0.0, 0.0], [a, 0.0, 0.0], [0.5*a, np.sqrt(3.0)*a/2.0, 0.0]])


def linear_chain(n=3, spacing=0.35):
    """N emitters on x axis, in wavelength units if wavelength=1."""
    x = np.arange(int(n), dtype=float) * float(spacing)
    return np.column_stack([x, np.zeros_like(x), np.zeros_like(x)])
