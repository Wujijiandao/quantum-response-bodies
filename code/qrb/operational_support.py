"""Operational fixed-marginal supports for permutation-symmetric three-emitter readout.

The routines here separate two tasks.

1. ``quantum_support_symmetric_three`` is exact for an observable A that commutes
   with total excitation and all site permutations.  The fixed local marginals
   I/2 can then be enforced by mixing excitation-sector optimizers so that the
   mean excitation is 3/2.

2. ``separable_product_dual_three`` evaluates the exact convex dual of the
   permutation- and U(1)-twirled fully separable problem, but its inner product
   numerical range is solved numerically by global differential evolution.  It
   therefore returns a reproducible numerical upper estimate rather than a
   computer-assisted proof unless an independent certificate is supplied.
"""
from __future__ import annotations
import itertools
import numpy as np
from scipy.optimize import linprog, differential_evolution, minimize_scalar
from .operators_n import I2, X, Y, Z, kron_all

PAULI = (I2, X, Y, Z)
PAULI_STRINGS_3 = tuple(itertools.product(range(4), repeat=3))


def excitation_sector_indices_three():
    return [[s for s in range(8) if int(s).bit_count() == k] for k in range(4)]


def sector_maxima_three(A):
    """Maximum eigenvalue of A in each k=0,1,2,3 excitation sector."""
    A = np.asarray(A, dtype=complex)
    vals = []
    for idx in excitation_sector_indices_three():
        block = A[np.ix_(idx, idx)]
        vals.append(float(np.linalg.eigvalsh(block).max().real))
    return np.asarray(vals)


def quantum_support_symmetric_three(A):
    """Exact support at local marginals I/2 for symmetric U(1)-invariant A.

    A permutation average of each sector optimizer has identical local
    marginals k/3.  Hence the fixed-marginal support is the linear program over
    sector weights with mean excitation 3/2.
    """
    a = sector_maxima_three(A)
    res = linprog(
        -a,
        A_eq=np.array([[1., 1., 1., 1.], [0., 1., 2., 3.]]),
        b_eq=np.array([1., 1.5]),
        bounds=[(0., None)] * 4,
        method="highs",
    )
    if not res.success:
        raise RuntimeError(res.message)
    return float(-res.fun), np.asarray(res.x), a


def pauli_coefficients_three(A):
    """Real Pauli coefficients c_s=Tr(P_s A)/8 for a Hermitian three-qubit A."""
    A = np.asarray(A, dtype=complex)
    coeff = np.empty(64, dtype=float)
    for q, inds in enumerate(PAULI_STRINGS_3):
        P = kron_all([PAULI[i] for i in inds])
        coeff[q] = float(np.real(np.trace(P @ A)) / 8.0)
    return coeff


def pure_product_expectation_three(params, coeff):
    """Expectation of A on a pure product state.

    params=(z1,z2,z3,phi2,phi3); global U(1) invariance sets phi1=0.
    Each local Bloch vector is (sqrt(1-z^2)cos phi, sqrt(1-z^2)sin phi,z).
    """
    x = np.asarray(params, dtype=float)
    z = x[:3]
    ph = np.array([0.0, x[3], x[4]])
    r = np.sqrt(np.maximum(0.0, 1.0 - z*z))
    bloch = np.column_stack([r*np.cos(ph), r*np.sin(ph), z])
    v = np.ones((3, 4), dtype=float)
    v[:, 1:] = bloch
    out = 0.0
    for c, inds in zip(coeff, PAULI_STRINGS_3):
        if abs(c) > 1e-15:
            out += c * v[0, inds[0]] * v[1, inds[1]] * v[2, inds[2]]
    return float(out)


def aligned_equatorial_support_three(A):
    """Response of the globally phase-twirled |+>^3 separable preparation.

    Global U(1) phase twirling makes every one-body marginal I/2 and leaves any
    U(1)-invariant observable expectation unchanged.
    """
    coeff = pauli_coefficients_three(A)
    return pure_product_expectation_three((0., 0., 0., 0., 0.), coeff)


def separable_product_dual_three(A, seed=123, inner_tol=2e-9, maxiter=500):
    """Numerical product-dual support for the symmetric fixed-marginal problem.

    After permutation and global-U(1) twirling, only the mean local z component
    m=(z1+z2+z3)/3 remains to be constrained.  Convex duality gives

        h_sep = min_lambda max_product [ <A> - lambda m ].

    The inner product numerical range is globally searched by differential
    evolution.  Returned ``duality_gap_to_equatorial`` is a useful convergence
    diagnostic when the aligned-equatorial state is the optimizer.
    """
    coeff = pauli_coefficients_three(A)
    bounds = [(-1., 1.)] * 3 + [(0., 2*np.pi)] * 2

    cache = {}
    def inner(lam):
        key = float(np.round(lam, 12))
        if key in cache:
            return cache[key]
        def obj(x):
            f = pure_product_expectation_three(x, coeff)
            m = (x[0] + x[1] + x[2]) / 3.0
            return -(f - lam*m)
        res = differential_evolution(
            obj, bounds, seed=seed, popsize=18, maxiter=maxiter,
            tol=inner_tol, polish=True, workers=1, updating="immediate"
        )
        val = float(-res.fun)
        cache[key] = (val, np.asarray(res.x))
        return cache[key]

    # A conservative search interval from the operator norm.  A local field
    # larger than several ||A|| cannot improve the m=0 dual optimum in this
    # three-qubit benchmark; enlarge if the scalar optimum touches the boundary.
    scale = max(1.0, float(np.linalg.norm(A, 2)))
    L = 6.0 * scale
    def outer(lam):
        return inner(float(lam))[0]
    out = minimize_scalar(outer, bounds=(-L, L), method="bounded", options={"xatol": 2e-7})
    lam = float(out.x)
    val, arg = inner(lam)
    eq = aligned_equatorial_support_three(A)
    return {
        "support": float(val),
        "lambda": lam,
        "product_argmax": arg,
        "aligned_equatorial": float(eq),
        "duality_gap_to_equatorial": float(val - eq),
        "outer_success": bool(out.success),
    }


def equatorial_stationary_dual_check_three(A, seed=123, inner_tol=2e-9, maxiter=500):
    """Global product-range check at the symmetric equatorial dual multiplier.

    For a permutation-symmetric U(1)-invariant A, write its Pauli expansion.
    At the aligned equatorial product point z_i=0, phi_i equal, the derivative
    with respect to each z_i is gamma+d, where gamma is the coefficient of ZII
    and d the coefficient of XXZ (equal to YYZ and permutations by symmetry).
    Since the dual constraint uses m=(z1+z2+z3)/3, stationarity fixes
    lambda=3(gamma+d).  A global product-state maximization then tests whether
    the equatorial construction saturates the separable dual.
    """
    coeff = pauli_coefficients_three(A)
    idx = {s:i for i,s in enumerate(PAULI_STRINGS_3)}
    gamma = coeff[idx[(3,0,0)]]
    d = coeff[idx[(1,1,3)]]
    lam = 3.0 * (gamma + d)
    bounds = [(-1., 1.)] * 3 + [(0., 2*np.pi)] * 2
    def obj(x):
        f = pure_product_expectation_three(x, coeff)
        m = (x[0] + x[1] + x[2]) / 3.0
        return -(f - lam*m)
    res = differential_evolution(
        obj, bounds, seed=seed, popsize=18, maxiter=maxiter, tol=inner_tol,
        polish=True, workers=1, updating="immediate"
    )
    val = float(-res.fun)
    eq = aligned_equatorial_support_three(A)
    return {
        "support_upper_numerical": val,
        "lambda": float(lam),
        "product_argmax": np.asarray(res.x),
        "aligned_equatorial": float(eq),
        "dual_minus_equatorial": float(val-eq),
        "inner_success": bool(res.success),
    }
