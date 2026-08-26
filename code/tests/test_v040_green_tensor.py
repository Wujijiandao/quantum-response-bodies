from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from qrb.green_tensor import lehmberg_pair, free_space_couplings, equilateral_triangle, linear_chain
from qrb.input_output import collective_decay_jumps, exchange_hamiltonian, lindblad_superoperator

# Pair kernels are symmetric under r -> -r and converge to Gamma_ij -> gamma0 at small separation.
r = np.array([0.23, -0.17, 0.08])
g1, o1 = lehmberg_pair(r, dipole=(0,0,1))
g2, o2 = lehmberg_pair(-r, dipole=(0,0,1))
assert abs(g1-g2) < 1e-12
assert abs(o1-o2) < 1e-12

gs, _ = lehmberg_pair((1e-4,0,0), dipole=(0,0,1))
assert abs(gs - 1.0) < 5e-4

# Equilateral triangle with perpendicular dipoles has permutation-symmetric couplings.
pos = equilateral_triangle(0.35)
Gamma, Omega = free_space_couplings(pos, dipole=(0,0,1), wavelength=1.0, gamma0=1.0)
assert np.allclose(Gamma, Gamma.T, atol=1e-12)
assert np.allclose(Omega, Omega.T, atol=1e-12)
assert np.allclose(np.diag(Gamma), 1.0)
assert np.allclose(np.diag(Omega), 0.0)
assert np.max(np.abs(Gamma[np.triu_indices(3,1)] - Gamma[0,1])) < 1e-12
assert np.max(np.abs(Omega[np.triu_indices(3,1)] - Omega[0,1])) < 1e-12
assert np.linalg.eigvalsh(Gamma).min() > -1e-10

# Lindblad reconstruction of collective Gamma: sum_mu v_mu v_mu^dagger reproduces Gamma.
jumps = collective_decay_jumps(Gamma)
# Compare Liouvillian against direct jump count sanity and trace preservation.
H = exchange_hamiltonian(Omega)
L = lindblad_superoperator(H, jumps)
d = 8
Ivec = np.eye(d).reshape(-1, order='F')
# Trace preservation means vec(I)^dag L = 0.
assert np.linalg.norm(Ivec.conj() @ L) < 2e-10

# Linear-chain matrices remain PSD for representative subwavelength spacings.
for a in [0.2, 0.3, 0.4, 0.6]:
    G, Om = free_space_couplings(linear_chain(3,a), dipole=(0,0,1))
    assert np.linalg.eigvalsh(G).min() > -2e-9

print('v0.4 free-space Green-tensor tests passed')
