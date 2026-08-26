from pathlib import Path
import json, sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
from scipy.sparse.linalg import expm_multiply

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'code'))
from qrb.green_tensor import equilateral_triangle, free_space_couplings
from qrb.input_output import collective_decay_jumps, exchange_hamiltonian, effective_observable, lindblad_superoperator, vec, unvec
from qrb.operators_n import exchange

figdir = ROOT / 'figures'; figdir.mkdir(exist_ok=True)
resdir = ROOT / 'results'; resdir.mkdir(exist_ok=True)

B = sum(exchange(i,j,3) for i,j in [(0,1),(0,2),(1,2)])
spacings = [0.25, 0.35, 0.50]
t = np.linspace(0.0, 0.14, 120)
summary = {}

plt.figure(figsize=(5.2,3.7))
for a in spacings:
    Gamma, Omega = free_space_couplings(equilateral_triangle(a), dipole=(0,0,1))
    H = exchange_hamiltonian(Omega)
    jumps = collective_decay_jumps(Gamma)
    L = lindblad_superoperator(H, jumps)
    Avec = L.conj().T
    traj = expm_multiply(Avec, vec(B), start=float(t[0]), stop=float(t[-1]), num=len(t), endpoint=True)
    bounds=[]
    for vv in traj:
        A = unvec(vv, B.shape[0])
        eps = np.linalg.norm(A-B, 2)
        bounds.append(0.5 - 2.0*eps)
    bounds=np.asarray(bounds)
    def f(tt):
        A=effective_observable(B,float(tt),H=H,jumps=jumps)
        return 0.5 - 2*np.linalg.norm(A-B,2)
    try:
        root=float(brentq(f,1e-10,0.4))
    except ValueError:
        root=None
    summary[str(a)] = {
        'Gamma12_over_Gamma0': float(Gamma[0,1]),
        'Omega12_over_Gamma0': float(Omega[0,1]),
        'Gamma_eigenvalues_over_Gamma0': [float(x) for x in np.linalg.eigvalsh(Gamma)],
        'certified_positive_gap_until_Gamma0_t': root,
    }
    plt.plot(t, bounds, label=fr'$d={a:.2f}\lambda$')

plt.axhline(0.0, linewidth=1)
plt.xlabel(r'$\Gamma_0 t$')
plt.ylabel(r'certified gap lower bound')
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig(figdir/'fig8_green_tensor_gap.pdf', bbox_inches='tight')
plt.savefig(figdir/'fig8_green_tensor_gap.png', dpi=220, bbox_inches='tight')
plt.close()

(resdir/'green_tensor_benchmark.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
print(json.dumps(summary, indent=2))
