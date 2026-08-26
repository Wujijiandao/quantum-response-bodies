"""N-qubit operators for quantum-response-body calculations.

Basis convention: |g>=(1,0), |e>=(0,1).  The exchange observable
O_ij = sigma_i^+ sigma_j^- + sigma_i^- sigma_j^+
is independent of the ladder-label convention and equals (X_i X_j+Y_i Y_j)/2.
"""
from __future__ import annotations
import numpy as np

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
NQ = np.array([[0, 0], [0, 1]], dtype=complex)
SP = np.array([[0, 0], [1, 0]], dtype=complex)  # |e><g|
SM = SP.conj().T


def kron_all(ops):
    out = np.array([[1.0]], dtype=complex)
    for op in ops:
        out = np.kron(out, op)
    return out


def site_op(op, i: int, n: int):
    ops = [I2 for _ in range(n)]
    ops[i] = op
    return kron_all(ops)


def exchange(i: int, j: int, n: int):
    """O_ij=(X_i X_j + Y_i Y_j)/2."""
    return 0.5 * (
        site_op(X, i, n) @ site_op(X, j, n)
        + site_op(Y, i, n) @ site_op(Y, j, n)
    )


def xy_hamiltonian(weight_matrix):
    """Sum_{i<j} c_ij O_ij for a real symmetric zero-diagonal matrix C."""
    c = np.asarray(weight_matrix, dtype=float)
    if c.ndim != 2 or c.shape[0] != c.shape[1]:
        raise ValueError("weight_matrix must be square")
    n = c.shape[0]
    h = np.zeros((2**n, 2**n), dtype=complex)
    for i in range(n):
        for j in range(i + 1, n):
            if c[i, j] != 0:
                h += c[i, j] * exchange(i, j, n)
    return h


def total_excitation(n: int):
    return sum(site_op(NQ, i, n) for i in range(n))


def global_bitflip(n: int):
    return kron_all([X] * n)


def global_phaseflip(n: int):
    return kron_all([Z] * n)


def collective_spin(axis, n: int):
    pauli = {"x": X, "y": Y, "z": Z}[axis.lower()]
    return 0.5 * sum(site_op(pauli, i, n) for i in range(n))
