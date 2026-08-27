from pathlib import Path
import json, sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse.linalg import expm_multiply

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'code'))
from qrb.green_tensor import equilateral_triangle, free_space_couplings
from qrb.input_output import collective_decay_jumps, exchange_hamiltonian, lindblad_superoperator, vec, unvec
from qrb.operators_n import exchange
from qrb.operational_support import (
    quantum_support_symmetric_three,
    aligned_equatorial_support_three,
    equatorial_stationary_dual_check_three,
)

figdir = ROOT / 'figures'; figdir.mkdir(exist_ok=True)
resdir = ROOT / 'results'; resdir.mkdir(exist_ok=True)

B = sum(exchange(i,j,3) for i,j in [(0,1),(0,2),(1,2)])
spacing = 0.35
Gamma, Omega = free_space_couplings(equilateral_triangle(spacing), dipole=(0,0,1))
H = exchange_hamiltonian(Omega)
jumps = collective_decay_jumps(Gamma)
L = lindblad_superoperator(H, jumps)
Ld = L.conj().T

# Dense operational curve.  The separable curve is the aligned-equatorial
# candidate; multistart product-dual checks below test it at representative times.
times = np.linspace(0.0, 4.0, 161)
traj = expm_multiply(Ld, vec(B), start=float(times[0]), stop=float(times[-1]), num=len(times), endpoint=True)
hq=[]; hsep=[]; gap=[]; cert=[]
for vv in traj:
    A = unvec(vv, 8)
    q,_,_ = quantum_support_symmetric_three(A)
    s = aligned_equatorial_support_three(A)
    hq.append(q); hsep.append(s); gap.append(q-s)
    cert.append(0.5 - 2*np.linalg.norm(A-B,2))
hq=np.asarray(hq); hsep=np.asarray(hsep); gap=np.asarray(gap); cert=np.asarray(cert)

check_times = [0.0, 0.08838, 0.25, 0.5, 1.0, 2.0, 3.0, 4.0]
checks=[]
for t in check_times:
    # direct dense exponential for exact requested time
    from qrb.input_output import effective_observable
    A = effective_observable(B, float(t), H=H, jumps=jumps)
    q,w,a = quantum_support_symmetric_three(A)
    seeds = [20260826, 20260827, 20260828]
    dual_runs = [equatorial_stationary_dual_check_three(A, seed=sd, maxiter=350) for sd in seeds]
    # The inner task is a maximization, so the largest value found across starts
    # is the most conservative numerical estimate of the dual branch. This is
    # still not a formal global-optimality certificate.
    dual = max(dual_runs, key=lambda d: d['support_upper_numerical'])
    vals = [float(d['support_upper_numerical']) for d in dual_runs]
    checks.append({
        'Gamma0_t': float(t),
        'h_quantum_exact': float(q),
        'sector_weights': [float(x) for x in w],
        'sector_maxima': [float(x) for x in a],
        'h_separable_product_dual_numerical': float(dual['support_upper_numerical']),
        'h_separable_aligned_equatorial': float(dual['aligned_equatorial']),
        'dual_minus_equatorial': float(dual['dual_minus_equatorial']),
        'gap_product_dual_numerical': float(q-dual['support_upper_numerical']),
        'conservative_norm_certificate': float(0.5-2*np.linalg.norm(A-B,2)),
        'dual_lambda': float(dual['lambda']),
        'dual_product_argmax': [float(x) for x in dual['product_argmax']],
        'multistart_seeds': seeds,
        'multistart_support_values': vals,
        'multistart_spread': float(max(vals)-min(vals)),
    })

summary={
    'model': 'equilateral free-space Lehmberg trimer, normal dipoles',
    'spacing_over_lambda': spacing,
    'Gamma12_over_Gamma0': float(Gamma[0,1]),
    'Omega12_over_Gamma0': float(Omega[0,1]),
    'scan_interval_Gamma0_t': [float(times[0]), float(times[-1])],
    'minimum_aligned_equatorial_gap_candidate_on_dense_scan': float(gap.min()),
    'aligned_equatorial_gap_candidate_at_conservative_root_0p08838': float(np.interp(0.08838,times,gap)),
    'checkpoints': checks,
    'interpretation': (
        'Quantum support is exact by excitation-sector LP. Separable support at the listed '
        'checkpoints is estimated by three independent differential-evolution starts of the '
        'product-numerical-range dual. The aligned-equatorial construction agrees with those '
        'searches to numerical tolerance at the listed checkpoints. The dense solid curve uses '
        'the aligned-equatorial construction between checkpoints and is not a formal global certificate.'
    ),
}
(resdir/'operational_gap_v050.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')

plt.figure(figsize=(5.35,3.65))
plt.plot(times, gap, label='aligned-equatorial gap candidate')
plt.plot(times, cert, linestyle='--', label='norm certificate')
plt.axhline(0.0, linewidth=0.8)
ct=np.array([x['Gamma0_t'] for x in checks]); cg=np.array([x['gap_product_dual_numerical'] for x in checks])
plt.scatter(ct,cg,s=18,label='multistart product-dual estimates')
plt.xlabel(r'$\Gamma_0 t$')
plt.ylabel('response-gap estimate')
plt.xlim(0,4)
plt.ylim(-0.08,0.55)
plt.legend(frameon=False,fontsize=8)
plt.tight_layout()
plt.savefig(figdir/'fig9_operational_gap.pdf',bbox_inches='tight')
plt.savefig(figdir/'fig9_operational_gap.png',dpi=240,bbox_inches='tight')
plt.close()

print(json.dumps(summary,indent=2))
