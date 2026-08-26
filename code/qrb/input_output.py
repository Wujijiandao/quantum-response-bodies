r"""Operational input-output maps for few-emitter quantum response bodies.

The central identity is the photon-flux observable for a phase-coded output mode

    b_s = N^{-1/2} sum_j s_j sigma_j^- ,    |s_j|=1,
    F_s = b_s^\dagger b_s.

For fixed local marginals I/2 and real signs s_j=+/-1,

    N(<F_s>-1/2) = sum_{i<j} s_i s_j r_ij,

where r_ij=<sigma_i^+ sigma_j^- + h.c.>.  Three settings reconstruct all
three pair responses for N=3.
"""
from __future__ import annotations
import numpy as np
from scipy.linalg import expm
from .operators_n import site_op, SM, SP, NQ, I2, kron_all


def output_mode(signs):
    """Normalized collective lowering operator b_s."""
    s = np.asarray(signs, dtype=complex)
    n = len(s)
    if n == 0:
        raise ValueError("signs must be nonempty")
    return sum(s[j] * site_op(SM, j, n) for j in range(n)) / np.sqrt(n)


def flux_observable(signs):
    r"""Photon-flux observable F_s=b_s^\dagger b_s."""
    b = output_mode(signs)
    return b.conj().T @ b


def pair_list(n: int):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def sign_measurement_matrix(settings):
    """Matrix M with M[a,(ij)]=Re(s_ai^* s_aj).

    For real +/-1 settings this maps real exchange responses to the normalized
    excess flux x_a=N(<F_a>-1/2).
    """
    settings = np.asarray(settings, dtype=complex)
    if settings.ndim != 2:
        raise ValueError("settings must be 2D")
    m, n = settings.shape
    pairs = pair_list(n)
    M = np.empty((m, len(pairs)), dtype=float)
    for a in range(m):
        for k, (i, j) in enumerate(pairs):
            M[a, k] = float(np.real(np.conj(settings[a, i]) * settings[a, j]))
    return M


THREE_SETTINGS = np.array(
    [
        [1.0, 1.0, 1.0],
        [1.0, -1.0, 1.0],
        [1.0, 1.0, -1.0],
    ],
    dtype=complex,
)


def three_reconstruction_matrix():
    """Return M and M^{-1} for the canonical three phase-coded settings."""
    M = sign_measurement_matrix(THREE_SETTINGS)
    return M, np.linalg.inv(M)


def normalized_excess_flux(rho, signs):
    """x_s=N(<F_s>-1/2), assuming the prepared local marginals are I/2."""
    rho = np.asarray(rho, dtype=complex)
    n = len(signs)
    F = flux_observable(signs)
    return float(np.real(n * (np.trace(rho @ F) - 0.5)))


def reconstruct_three_pair_response(rho):
    """Reconstruct (r12,r13,r23) from three phase-coded flux settings."""
    x = np.array([normalized_excess_flux(rho, s) for s in THREE_SETTINGS])
    _, Minv = three_reconstruction_matrix()
    return Minv @ x, x


def vec(a):
    """Column-major vectorization."""
    return np.asarray(a, dtype=complex).reshape(-1, order="F")


def unvec(v, d):
    return np.asarray(v, dtype=complex).reshape((d, d), order="F")


def lindblad_superoperator(H, jumps):
    """Liouvillian L acting on vec(rho) in column-major convention."""
    H = np.asarray(H, dtype=complex)
    d = H.shape[0]
    I = np.eye(d, dtype=complex)
    L = -1j * (np.kron(I, H) - np.kron(H.T, I))
    for J in jumps:
        J = np.asarray(J, dtype=complex)
        JJ = J.conj().T @ J
        L += np.kron(J.conj(), J)
        L -= 0.5 * np.kron(I, JJ)
        L -= 0.5 * np.kron(JJ.T, I)
    return L


def local_dephasing_jumps(n: int, gamma_phi: float):
    """Pure-dephasing jumps sqrt(gamma_phi/2) Z_i.

    This convention makes single-qubit transverse coherence decay as
    exp(-gamma_phi t), hence pair exchange coherence as exp(-2 gamma_phi t).
    """
    from .operators_n import Z
    if gamma_phi < 0:
        raise ValueError("gamma_phi must be nonnegative")
    return [np.sqrt(gamma_phi / 2.0) * site_op(Z, i, n) for i in range(n)]


def independent_decay_jumps(n: int, gamma: float):
    if gamma < 0:
        raise ValueError("gamma must be nonnegative")
    return [np.sqrt(gamma) * site_op(SM, i, n) for i in range(n)]


def evolve_state(rho0, t: float, H=None, jumps=()):
    """Exact dense Lindblad evolution for small N."""
    rho0 = np.asarray(rho0, dtype=complex)
    d = rho0.shape[0]
    if H is None:
        H = np.zeros((d, d), dtype=complex)
    L = lindblad_superoperator(H, jumps)
    return unvec(expm(L * t) @ vec(rho0), d)


def effective_observable(O, t: float, H=None, jumps=()):
    """Heisenberg-picture observable satisfying Tr[O rho(t)]=Tr[A_t rho(0)]."""
    O = np.asarray(O, dtype=complex)
    d = O.shape[0]
    if H is None:
        H = np.zeros((d, d), dtype=complex)
    L = lindblad_superoperator(H, jumps)
    # Hilbert-Schmidt dual in vec convention: vec(A_t)=exp(L^\dagger t) vec(O)
    return unvec(expm(L.conj().T * t) @ vec(O), d)



def integrated_effective_observable(O, tau: float, H=None, jumps=()):
    """A_tau=int_0^tau exp(L^dagger t)[O] dt for finite-time photon counts."""
    O = np.asarray(O, dtype=complex)
    d = O.shape[0]
    if H is None:
        H = np.zeros((d, d), dtype=complex)
    L = lindblad_superoperator(H, jumps)
    A = L.conj().T
    n = A.shape[0]
    block = np.zeros((2*n, 2*n), dtype=complex)
    block[:n, :n] = A
    block[:n, n:] = np.eye(n, dtype=complex)
    E = expm(block * float(tau))
    integ = E[:n, n:]
    return unvec(integ @ vec(O), d)


def collective_decay_jumps(Gamma, tol=1e-12):
    """Diagonalize a positive semidefinite collective-decay matrix.

    Returns jump operators J_mu = sqrt(lambda_mu) sum_i v_{i,mu} sigma_i^-.
    """
    Gamma = np.asarray(Gamma, dtype=complex)
    if Gamma.ndim != 2 or Gamma.shape[0] != Gamma.shape[1]:
        raise ValueError("Gamma must be square")
    if not np.allclose(Gamma, Gamma.conj().T, atol=1e-10):
        raise ValueError("Gamma must be Hermitian")
    vals, vecs = np.linalg.eigh(Gamma)
    if vals.min(initial=0.0) < -1e-9:
        raise ValueError("Gamma is not positive semidefinite")
    n = Gamma.shape[0]
    jumps = []
    for k, lam in enumerate(vals):
        if lam > tol:
            v = vecs[:, k]
            J = sum(v[i] * site_op(SM, i, n) for i in range(n)) * np.sqrt(lam)
            jumps.append(J)
    return jumps


def exchange_hamiltonian(Omega, detunings=None):
    """Construct H=sum_i Delta_i n_i + sum_{i<j} Omega_ij O_ij."""
    Omega = np.asarray(Omega, dtype=float)
    if Omega.ndim != 2 or Omega.shape[0] != Omega.shape[1]:
        raise ValueError("Omega must be square")
    n = Omega.shape[0]
    H = np.zeros((2**n, 2**n), dtype=complex)
    if detunings is not None:
        d = np.asarray(detunings, dtype=float)
        if d.shape != (n,):
            raise ValueError("detunings must have length N")
        for i in range(n):
            H += d[i] * site_op(NQ, i, n)
    from .operators_n import exchange
    for i in range(n):
        for j in range(i + 1, n):
            H += Omega[i, j] * exchange(i, j, n)
    return H
