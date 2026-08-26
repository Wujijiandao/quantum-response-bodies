"""Graph response bodies for real pair-coherence coordinates."""
from __future__ import annotations
import numpy as np
from scipy.optimize import differential_evolution
from .operators_n import xy_hamiltonian


def weighted_adjacency(weights):
    """Return a real symmetric zero-diagonal matrix from an array/dict."""
    if isinstance(weights, dict):
        n = 1 + max(max(i, j) for i, j in weights)
        c = np.zeros((n, n), dtype=float)
        for (i, j), v in weights.items():
            c[i, j] = c[j, i] = float(v)
        return c
    c = np.asarray(weights, dtype=float)
    if c.ndim != 2 or c.shape[0] != c.shape[1]:
        raise ValueError("weights must be square")
    return 0.5 * (c + c.T) - np.diag(np.diag(c))


def quantum_support_xy(weights):
    """Fixed-I/2 support for real exchange responses.

    For H_XY(C)=sum_{i<j} C_ij O_ij, particle-hole symmetry makes the
    fixed-marginal support equal to lambda_max(H_XY).  For N=3 this also
    equals lambda_max(C).
    """
    c = weighted_adjacency(weights)
    return float(np.linalg.eigvalsh(xy_hamiltonian(c))[-1].real)


def separable_support_xy(weights, seed=1234, tol=1e-11):
    """Classical XY support: 1/2 max_phi sum c_ij cos(phi_i-phi_j).

    Global phase is fixed by phi_0=0. differential_evolution is used only
    as a numerical check; exact formulas are supplied for key graph families.
    """
    c = weighted_adjacency(weights)
    n = c.shape[0]
    if n == 1:
        return 0.0

    def objective(x):
        phi = np.concatenate(([0.0], x))
        val = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                val += c[i, j] * np.cos(phi[i] - phi[j])
        return -0.5 * val

    result = differential_evolution(
        objective,
        bounds=[(-np.pi, np.pi)] * (n - 1),
        seed=seed,
        tol=tol,
        polish=True,
        updating="immediate",
    )
    return float(-result.fun)


def three_c_matrix(c12, c13, c23):
    return np.array(
        [[0.0, c12, c13], [c12, 0.0, c23], [c13, c23, 0.0]],
        dtype=float,
    )


def three_quantum_support(c12, c13, c23):
    """Exact N=3 support h_Q(c)=lambda_max(C(c))."""
    return float(np.linalg.eigvalsh(three_c_matrix(c12, c13, c23))[-1])


def three_separable_elliptope_matrix(r12, r13, r23):
    """G=I+2*r_off; S_3 iff G is PSD."""
    return np.array(
        [[1.0, 2*r12, 2*r13], [2*r12, 1.0, 2*r23], [2*r13, 2*r23, 1.0]],
        dtype=float,
    )


def in_three_separable_body(r, atol=1e-10):
    r12, r13, r23 = map(float, r)
    g = three_separable_elliptope_matrix(r12, r13, r23)
    return np.linalg.eigvalsh(g)[0] >= -atol


def three_separable_boundary_polynomial(r):
    r12, r13, r23 = map(float, r)
    return 1 + 16*r12*r13*r23 - 4*(r12*r12 + r13*r13 + r23*r23)


def in_three_quantum_body(r, grid=1201, atol=2e-5):
    """Feasibility check for Q3 via a 1D diagonal search.

    Q3={r: exists p>=0, sum p=1, P(p,r)>=0}, P_ij=r_ij/2.
    We scan p1 and solve a fine p2 grid. This is for regression/plot checks,
    not used as a proof engine.
    """
    r12, r13, r23 = map(float, r)
    off = np.array([[0, r12/2, r13/2], [r12/2, 0, r23/2], [r13/2, r23/2, 0]], float)
    vals = np.linspace(0.0, 1.0, grid)
    for p1 in vals:
        p2max = 1.0 - p1
        if p2max < 0:
            continue
        # modest adaptive grid on remaining interval
        for p2 in np.linspace(0.0, p2max, max(3, int(grid*p2max))):
            p3 = 1.0 - p1 - p2
            p = off + np.diag([p1, p2, p3])
            if np.linalg.eigvalsh(p)[0] >= -atol:
                return True
    return False


def q3_state_from_psd_p(p):
    """Construct an 8x8 fixed-marginal state from 3x3 real PSD P, Tr P=1.

    rho = 1/2 P in the one-excitation subspace + 1/2 bit-flipped P in the
    two-excitation subspace. Basis ordering is |000>,...,|111>.
    """
    p = np.asarray(p, dtype=complex)
    if p.shape != (3, 3):
        raise ValueError("p must be 3x3")
    if abs(np.trace(p) - 1) > 1e-8 or np.linalg.eigvalsh(p)[0] < -1e-9:
        raise ValueError("p must be PSD with trace 1")
    rho = np.zeros((8, 8), dtype=complex)
    # one-excitation basis: |100>, |010>, |001> -> indices 4,2,1
    one = [4, 2, 1]
    # global bit flips -> |011>, |101>, |110> -> indices 3,5,6
    two = [3, 5, 6]
    for a in range(3):
        for b in range(3):
            rho[one[a], one[b]] += 0.5 * p[a, b]
            rho[two[a], two[b]] += 0.5 * p[a, b]
    return rho


def q3_response_from_p(p):
    p = np.asarray(p, dtype=float)
    return np.array([2*p[0, 1], 2*p[0, 2], 2*p[1, 2]], dtype=float)


def complete_antiferro_supports(n: int):
    """Exact supports for c_ij=-1 on K_n.

    sep=N/4 for N>=3; quantum=N/2 (even) or (N-1)/2 (odd).
    """
    if n < 3:
        raise ValueError("formula stated for n>=3")
    h_sep = n / 4.0
    h_q = n / 2.0 if n % 2 == 0 else (n - 1) / 2.0
    return h_q, h_sep


def complete_antiferro_matrix(n: int):
    c = -np.ones((n, n), dtype=float)
    np.fill_diagonal(c, 0.0)
    return c
