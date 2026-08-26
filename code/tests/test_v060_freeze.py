"""Scientific-freeze regression checks for v0.6.

These tests target proof-sensitive points that are easy to implement incorrectly:
sector-resolved particle-hole symmetrization, the three-emitter polar identity,
the fixed-marginal minimum-negativity lower bound, and the Lehmberg benchmark.
"""
from __future__ import annotations
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import numpy as np
from qrb.operators_n import exchange, X, I2, kron_all
from qrb.green_tensor import equilateral_triangle, free_space_couplings

rng = np.random.default_rng(20260827)


def bitcount_sector(n, k):
    return [s for s in range(2**n) if int(s).bit_count() == k]


def partial_trace_one(rho, keep, n):
    # explicit index contraction, deliberately independent of package helpers
    out = np.zeros((2, 2), complex)
    for a in range(2**n):
        bits_a = [(a >> (n - 1 - q)) & 1 for q in range(n)]
        for b in range(2**n):
            bits_b = [(b >> (n - 1 - q)) & 1 for q in range(n)]
            if all(bits_a[q] == bits_b[q] for q in range(n) if q != keep):
                out[bits_a[keep], bits_b[keep]] += rho[a, b]
    return out


def partial_transpose_B(rho):
    return rho.reshape(2,2,2,2).transpose(0,3,2,1).reshape(4,4)


def negativity(rho):
    ev = np.linalg.eigvalsh(partial_transpose_B(rho))
    return float(-ev[ev < 0].sum())


def random_su2():
    z = rng.normal(size=(2,2)) + 1j*rng.normal(size=(2,2))
    q, r = np.linalg.qr(z)
    q = q @ np.diag(np.exp(-1j*np.angle(np.diag(r))))
    return q / np.sqrt(np.linalg.det(q))


def test_sector_resolved_symmetrization():
    n = 3
    Os = [exchange(0,1,n), exchange(0,2,n), exchange(1,2,n)]
    XG = kron_all([X]*n)
    for _ in range(25):
        c = rng.normal(size=3)
        H = sum(ci*Oi for ci, Oi in zip(c, Os))
        top = -np.inf; psi = None
        for k in range(n+1):
            idx = bitcount_sector(n,k)
            vals, vecs = np.linalg.eigh(H[np.ix_(idx,idx)])
            if vals[-1] > top:
                top = float(vals[-1])
                psi = np.zeros(2**n, complex)
                psi[idx] = vecs[:, -1]
        rho0 = np.outer(psi, psi.conj())
        rho = 0.5*(rho0 + XG @ rho0 @ XG)
        assert abs(np.trace(H @ rho).real - top) < 2e-12
        for i in range(n):
            assert np.linalg.norm(partial_trace_one(rho,i,n)-I2/2) < 2e-12


def test_three_polar_support_identity():
    n=3
    Os=[exchange(0,1,n),exchange(0,2,n),exchange(1,2,n)]
    for _ in range(100):
        c=rng.normal(size=3)
        H=sum(ci*Oi for ci,Oi in zip(c,Os))
        C=np.array([[0,c[0],c[1]],[c[0],0,c[2]],[c[1],c[2],0]],float)
        assert abs(np.linalg.eigvalsh(H).max()-np.linalg.eigvalsh(C).max()) < 2e-12
        # c is in the polar exactly when I-C is PSD, i.e. -c lies in E3.
        polar = np.linalg.eigvalsh(C).max() <= 1 + 1e-12
        ell = np.linalg.eigvalsh(np.eye(3)-C).min() >= -1e-12
        assert polar == ell


def test_minimum_negativity_random_lmm_lower_bound():
    bells=[]
    for v in [(1,0,0,1),(1,0,0,-1),(0,1,1,0),(0,1,-1,0)]:
        psi=np.asarray(v,complex)/np.sqrt(2)
        bells.append(np.outer(psi,psi.conj()))
    for _ in range(1000):
        p=rng.dirichlet(np.ones(4))
        rho=sum(pi*bi for pi,bi in zip(p,bells))
        U,V=random_su2(),random_su2(); W=np.kron(U,V)
        rho=W@rho@W.conj().T
        r=2*abs(rho[1,2])
        assert negativity(rho) + 2e-12 >= max(0.0,r-0.5)
    for r in np.linspace(0,1,41):
        if r<=0.5:
            a=b=0.25
        else:
            a=(1-r)/2; b=r/2
        z=r/2
        rho=np.array([[a,0,0,0],[0,b,z,0],[0,z,b,0],[0,0,0,a]],complex)
        assert abs(negativity(rho)-max(0.0,r-0.5)) < 2e-12


def test_lehmberg_primary_benchmark_numbers():
    pos=equilateral_triangle(0.35)
    G,O=free_space_couplings(pos,dipole=(0,0,1),wavelength=1,gamma0=1)
    assert abs(G[0,1]-0.25540786413473576)<1e-13
    assert abs(O[0,1]-0.28447601704249503)<1e-13
    ev=np.linalg.eigvalsh(G)
    assert np.allclose(ev,[0.7445921358652642,0.7445921358652643,1.5108157282694714],atol=2e-13)


if __name__ == '__main__':
    test_sector_resolved_symmetrization()
    test_three_polar_support_identity()
    test_minimum_negativity_random_lmm_lower_bound()
    test_lehmberg_primary_benchmark_numbers()
    print('v0.6 scientific-freeze tests passed')
