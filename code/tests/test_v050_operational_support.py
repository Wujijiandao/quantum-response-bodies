from pathlib import Path
import sys
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from qrb.operators_n import exchange
from qrb.operational_support import quantum_support_symmetric_three, aligned_equatorial_support_three
from qrb.green_tensor import equilateral_triangle, free_space_couplings
from qrb.input_output import collective_decay_jumps, exchange_hamiltonian, effective_observable

B = sum(exchange(i,j,3) for i,j in [(0,1),(0,2),(1,2)])
q,w,a = quantum_support_symmetric_three(B)
assert abs(q-2.0) < 1e-12
assert np.allclose(w, [0,0.5,0.5,0], atol=1e-12)
assert np.allclose(a, [0,2,2,0], atol=1e-12)
assert abs(aligned_equatorial_support_three(B)-1.5) < 1e-12

Gamma, Omega = free_space_couplings(equilateral_triangle(0.35), dipole=(0,0,1))
H = exchange_hamiltonian(Omega)
jumps = collective_decay_jumps(Gamma)
A = effective_observable(B, 0.08838, H=H, jumps=jumps)
q,_,_ = quantum_support_symmetric_three(A)
s = aligned_equatorial_support_three(A)
assert abs(q - 1.8060751903578147) < 5e-11
assert abs(s - 1.368864441570206) < 5e-11
assert q-s > 0.4371

print('v0.5 operational-support tests passed')
