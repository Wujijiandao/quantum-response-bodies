import numpy as np
from .operators import SP1SM2, N1, N2


def coherence(rho):
    """z = <sigma_1^+ sigma_2^->."""
    return np.trace(rho @ SP1SM2)


def response_xy(rho):
    """Normalized 2D response vector r=(2 Re z, 2 Im z)."""
    z = coherence(rho)
    return np.array([2.0*z.real, 2.0*z.imag], dtype=float)


def local_excitation_sum(rho):
    return float(np.real(np.trace(rho @ (N1 + N2))))


def far_field_intensity(rho, phi):
    """Dimensionless two-emitter first-order intensity.

    I(phi) = n1+n2 + 2 Re[exp(i phi) <sigma_1^+ sigma_2^->].
    For fixed local marginals I/2, n1+n2=1.
    """
    z = coherence(rho)
    return local_excitation_sum(rho) + 2.0*np.real(np.exp(1j*phi)*z)


def quantum_support(unit_direction):
    u = np.asarray(unit_direction, dtype=float)
    return np.linalg.norm(u)


def separable_support(unit_direction):
    u = np.asarray(unit_direction, dtype=float)
    return 0.5*np.linalg.norm(u)


def fixed_marginal_quantum_radius():
    return 1.0


def fixed_marginal_separable_radius():
    return 0.5
