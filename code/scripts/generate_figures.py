import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import matplotlib.pyplot as plt
from qrb.states import bell_single_excitation, separable_boundary_state
from qrb.response import response_xy, far_field_intensity

ROOT = Path(__file__).resolve().parents[2]
FIG = ROOT/'figures'
FIG.mkdir(exist_ok=True)

t = np.linspace(0, 2*np.pi, 600)

# Figure 1: exact response bodies.
fig, ax = plt.subplots(figsize=(6.2,6.2))
ax.plot(np.cos(t), np.sin(t), label='Quantum boundary')
ax.plot(0.5*np.cos(t), 0.5*np.sin(t), '--', label='Separable boundary')
ax.fill(0.5*np.cos(t), 0.5*np.sin(t), alpha=0.15)
ax.set_aspect('equal', adjustable='box')
ax.set_xlabel(r'$r_x=2\,\mathrm{Re}\langle\sigma_1^+\sigma_2^-\rangle$')
ax.set_ylabel(r'$r_y=2\,\mathrm{Im}\langle\sigma_1^+\sigma_2^-\rangle$')
ax.set_title('Fixed-marginal quantum and separable response bodies')
ax.legend()
fig.tight_layout()
fig.savefig(FIG/'fig1_response_bodies.png', dpi=220)
fig.savefig(FIG/'fig1_response_bodies.pdf')
plt.close(fig)

# Figure 2: far-field operational slice.
rho_q = bell_single_excitation(0.0)
rho_s = separable_boundary_state(0.0,0.0)
phi = np.linspace(0, 2*np.pi, 700)
Iq = np.array([far_field_intensity(rho_q,p) for p in phi])
Is = np.array([far_field_intensity(rho_s,p) for p in phi])
fig, ax = plt.subplots(figsize=(7.0,4.5))
ax.plot(phi, Iq, label='Entangled boundary state')
ax.plot(phi, Is, '--', label='Separable boundary state')
ax.axhline(1.5, linestyle=':', linewidth=1)
ax.axhline(0.5, linestyle=':', linewidth=1)
ax.set_xlabel(r'phase $\phi$')
ax.set_ylabel(r'dimensionless intensity $I(\phi)$')
ax.set_title('Operational phase-resolved response')
ax.legend()
fig.tight_layout()
fig.savefig(FIG/'fig2_far_field_slice.png', dpi=220)
fig.savefig(FIG/'fig2_far_field_slice.pdf')
plt.close(fig)

print('generated figures in', FIG)
