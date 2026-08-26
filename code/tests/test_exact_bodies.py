import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
from qrb.states import bell_single_excitation, separable_boundary_state, partial_trace_A, partial_trace_B
from qrb.response import response_xy, far_field_intensity

I2 = np.eye(2)/2

def assert_close(a,b,tol=1e-10):
    if not np.allclose(a,b,atol=tol,rtol=0):
        raise AssertionError(f"not close:\n{a}\n!=\n{b}")

# Quantum boundary: Bell family gives unit response radius and fixed marginals.
for theta in np.linspace(0, 2*np.pi, 17):
    rho = bell_single_excitation(theta)
    assert_close(partial_trace_A(rho), I2)
    assert_close(partial_trace_B(rho), I2)
    r = response_xy(rho)
    assert abs(np.linalg.norm(r)-1.0) < 1e-10

# Separable boundary construction gives radius 1/2 and fixed marginals.
for theta in np.linspace(0, 2*np.pi, 17):
    rho = separable_boundary_state(0.0, theta)
    assert_close(partial_trace_A(rho), I2)
    assert_close(partial_trace_B(rho), I2)
    r = response_xy(rho)
    assert abs(np.linalg.norm(r)-0.5) < 1e-10

# Operational far-field extrema for representative phases.
rho_q = bell_single_excitation(0.0)
rho_s = separable_boundary_state(0.0, 0.0)
assert abs(max(far_field_intensity(rho_q,p) for p in np.linspace(0,2*np.pi,2001)) - 2.0) < 2e-6
assert abs(min(far_field_intensity(rho_q,p) for p in np.linspace(0,2*np.pi,2001)) - 0.0) < 2e-6
assert abs(max(far_field_intensity(rho_s,p) for p in np.linspace(0,2*np.pi,2001)) - 1.5) < 2e-6
assert abs(min(far_field_intensity(rho_s,p) for p in np.linspace(0,2*np.pi,2001)) - 0.5) < 2e-6

print('PASS: exact two-emitter response-body checks')
