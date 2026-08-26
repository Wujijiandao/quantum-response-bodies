from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from qrb.input_output import (
    THREE_SETTINGS,
    flux_observable,
    three_reconstruction_matrix,
    reconstruct_three_pair_response,
    local_dephasing_jumps,
    evolve_state,
    effective_observable,
    integrated_effective_observable,
)
from qrb.operators_n import exchange
from qrb.graph_response import q3_state_from_psd_p, q3_response_from_p
from qrb.robustness import dephasing_scale, perturbation_safe

# Canonical measurement map is invertible and has the announced inverse.
M, Minv = three_reconstruction_matrix()
assert abs(np.linalg.det(M)) > 1e-12
assert np.allclose(M @ Minv, np.eye(3), atol=1e-12)

# Test exact optical reconstruction on random PSD one-excitation representatives.
rng = np.random.default_rng(20260826)
for _ in range(50):
    A = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    P = A @ A.conj().T
    P /= np.trace(P)
    # Restrict to real symmetric P so the three real pair coordinates close.
    P = np.real(P)
    # real(P) remains PSD; renormalize tiny numerical drift
    P /= np.trace(P)
    rho = q3_state_from_psd_p(P)
    r_expected = q3_response_from_p(P)
    r_rec, x = reconstruct_three_pair_response(rho)
    assert np.allclose(r_rec, r_expected, atol=2e-11)

# Local dephasing scales every O_ij expectation by exp(-2 gamma_phi t).
P = np.ones((3, 3), dtype=float) / 3.0  # W / anti-W mixture -> r=(2/3,2/3,2/3)
rho0 = q3_state_from_psd_p(P)
gamma_phi = 0.37
t = 0.83
rho_t = evolve_state(rho0, t, jumps=local_dephasing_jumps(3, gamma_phi))
scale = dephasing_scale(gamma_phi, t)
for i, j in [(0,1),(0,2),(1,2)]:
    O = exchange(i, j, 3)
    r0 = np.real(np.trace(rho0 @ O))
    rt = np.real(np.trace(rho_t @ O))
    assert abs(rt - scale * r0) < 2e-10

# Heisenberg and Schrödinger pictures agree.
O = flux_observable(THREE_SETTINGS[0])
Aeff = effective_observable(O, t, jumps=local_dephasing_jumps(3, gamma_phi))
lhs = np.trace(O @ rho_t)
rhs = np.trace(Aeff @ rho0)
assert abs(lhs - rhs) < 2e-10

# Perturbation theorem sanity.
assert perturbation_safe(0.5, 0.20) > 0
assert perturbation_safe(0.5, 0.26) < 0

print("v0.3 input-output and robustness tests passed")


# Integrated finite-time readout remains a linear observable of rho(0).
tau = 0.41
Aint = integrated_effective_observable(O, tau, jumps=local_dephasing_jumps(3, gamma_phi))
# independent numerical quadrature of the Schrödinger expectation
from scipy.integrate import quad
f = lambda tt: float(np.real(np.trace(O @ evolve_state(rho0, tt, jumps=local_dephasing_jumps(3, gamma_phi)))))
num, _ = quad(f, 0.0, tau, epsabs=1e-10, epsrel=1e-10)
ana = float(np.real(np.trace(Aint @ rho0)))
assert abs(num - ana) < 2e-9
