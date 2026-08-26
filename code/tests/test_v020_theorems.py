import os, sys
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT)

from qrb.graph_response import (
    three_quantum_support,
    in_three_separable_body,
    three_separable_boundary_polynomial,
    q3_state_from_psd_p,
    q3_response_from_p,
    complete_antiferro_supports,
    complete_antiferro_matrix,
    quantum_support_xy,
)
from qrb.resource_cost import negativity, minimum_negativity_from_radius, optimal_x_state_for_radius
from qrb.states import partial_trace_A, partial_trace_B
from qrb.operators_n import exchange


def assert_close(a,b,tol=1e-9):
    assert abs(a-b) < tol, (a,b)


def test_three_support_special_directions():
    # ferromagnetic triangle: eigenvalues 2,-1,-1
    assert_close(three_quantum_support(1,1,1), 2.0)
    # frustrated all-negative triangle: eigenvalues 1,1,-2
    assert_close(three_quantum_support(-1,-1,-1), 1.0)


def test_three_separable_elliptope_points():
    # aligned equatorial product states -> scaled elliptope corner
    assert in_three_separable_body([0.5,0.5,0.5])
    assert_close(three_separable_boundary_polynomial([0.5,0.5,0.5]), 0.0)
    # Bell-pair response is quantum but outside separable body
    assert not in_three_separable_body([1.0,0.0,0.0])


def test_q3_psd_construction_fixed_marginals_and_response():
    v = np.array([1.0,1.0,1.0])/np.sqrt(3)
    p = np.outer(v,v)
    rho = q3_state_from_psd_p(p)
    # one-qubit marginals are I/2: compute explicitly by tensor trace
    a = rho.reshape(2,2,2,2,2,2)
    r0 = np.einsum('abcdbc->ad', a)
    r1 = np.einsum('abcaec->be', a)
    r2 = np.einsum('abcabf->cf', a)
    for red in [r0,r1,r2]:
        assert np.linalg.norm(red - np.eye(2)/2) < 1e-10
    # r=(2/3,2/3,2/3)
    np.testing.assert_allclose(q3_response_from_p(p), [2/3,2/3,2/3], atol=1e-10)
    # direct operator expectations agree
    direct = [np.trace(rho @ exchange(i,j,3)).real for i,j in [(0,1),(0,2),(1,2)]]
    np.testing.assert_allclose(direct, [2/3,2/3,2/3], atol=1e-10)


def test_complete_antiferromagnetic_formula_against_exact_diagonalization():
    for n in range(3,8):
        hq_formula, _ = complete_antiferro_supports(n)
        hq_num = quantum_support_xy(complete_antiferro_matrix(n))
        assert_close(hq_formula, hq_num, tol=2e-9)


def test_exact_minimum_negativity_achiever():
    for r in np.linspace(0.5,1.0,11):
        rho = optimal_x_state_for_radius(r)
        np.testing.assert_allclose(partial_trace_A(rho), np.eye(2)/2, atol=1e-10)
        np.testing.assert_allclose(partial_trace_B(rho), np.eye(2)/2, atol=1e-10)
        assert_close(negativity(rho), minimum_negativity_from_radius(r), tol=1e-9)

if __name__ == '__main__':
    tests=[v for k,v in sorted(globals().items()) if k.startswith('test_') and callable(v)]
    for t in tests:
        t()
        print('PASS', t.__name__)
    print(f'{len(tests)} tests passed')
