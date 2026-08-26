import numpy as np


def ket_g():
    return np.array([1.0, 0.0], dtype=complex)


def ket_e():
    return np.array([0.0, 1.0], dtype=complex)


def projector(psi):
    psi = np.asarray(psi, dtype=complex)
    return np.outer(psi, psi.conj())


def bell_single_excitation(theta=0.0):
    """(|e,g> + exp(i theta)|g,e>)/sqrt(2)."""
    eg = np.kron(ket_e(), ket_g())
    ge = np.kron(ket_g(), ket_e())
    psi = (eg + np.exp(1j * theta) * ge) / np.sqrt(2.0)
    return projector(psi)


def equatorial(alpha=0.0, sign=1):
    """(|g> + sign*exp(i alpha)|e>)/sqrt(2), sign = +/-1."""
    return (ket_g() + sign * np.exp(1j * alpha) * ket_e()) / np.sqrt(2.0)


def separable_boundary_state(alpha=0.0, beta=0.0):
    """Separable state with both local marginals I/2 and |<sp1 sm2>|=1/4.

    rho = 1/2 |+a,+b><+a,+b| + 1/2 |-a,-b><-a,-b|.
    """
    pp = np.kron(equatorial(alpha, +1), equatorial(beta, +1))
    mm = np.kron(equatorial(alpha, -1), equatorial(beta, -1))
    return 0.5 * projector(pp) + 0.5 * projector(mm)


def maximally_mixed_two_qubits():
    return np.eye(4, dtype=complex) / 4.0


def random_density_matrix(dim=4, rng=None):
    rng = np.random.default_rng() if rng is None else rng
    x = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
    rho = x @ x.conj().T
    return rho / np.trace(rho)


def random_pure_qubit(rng=None):
    rng = np.random.default_rng() if rng is None else rng
    v = rng.normal(size=2) + 1j * rng.normal(size=2)
    v = v / np.linalg.norm(v)
    return v


def random_separable_state(num_terms=8, rng=None):
    rng = np.random.default_rng() if rng is None else rng
    weights = rng.random(num_terms)
    weights /= weights.sum()
    rho = np.zeros((4,4), dtype=complex)
    for w in weights:
        a = random_pure_qubit(rng)
        b = random_pure_qubit(rng)
        psi = np.kron(a,b)
        rho += w * projector(psi)
    return rho


def partial_trace_B(rho):
    rho = np.asarray(rho).reshape(2,2,2,2)
    # indices a,b,a',b'; trace b=b'
    return np.einsum('abcb->ac', rho)


def partial_trace_A(rho):
    rho = np.asarray(rho).reshape(2,2,2,2)
    # trace a=a'
    return np.einsum('abad->bd', rho)
