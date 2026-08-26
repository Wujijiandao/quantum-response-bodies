from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
CODE = ROOT / "code"
sys.path.insert(0, str(CODE))
from qrb.input_output import three_reconstruction_matrix
from qrb.robustness import symmetric_three_gap

FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

# Fig. 6: operational measurement map.
M, Minv = three_reconstruction_matrix()
fig, ax = plt.subplots(figsize=(6.2, 4.0))
ax.axis("off")
text = (
    "Three phase-coded output settings\n\n"
    "s0 = (+,+,+)    x0 =  r12 + r13 + r23\n"
    "s1 = (+,-,+)    x1 = -r12 + r13 - r23\n"
    "s2 = (+,+,-)    x2 =  r12 - r13 - r23\n\n"
    "Reconstruction:\n"
    "r12 = (x0+x2)/2\n"
    "r13 = (x0+x1)/2\n"
    "r23 = -(x1+x2)/2"
)
ax.text(0.04, 0.96, text, va="top", ha="left", fontsize=12, family="monospace")
fig.tight_layout()
fig.savefig(FIG / "fig6_operational_reconstruction.pdf", bbox_inches="tight")
fig.savefig(FIG / "fig6_operational_reconstruction.png", dpi=220, bbox_inches="tight")
plt.close(fig)

# Fig. 7: exact dephasing contraction of the symmetric support gap.
tau = np.linspace(0, 3.0, 300)  # gamma_phi t
# set gamma=1 so horizontal axis is gamma_phi t
Delta = symmetric_three_gap(1.0, tau)
hq = 2.0 * np.exp(-2.0 * tau)
hs = 1.5 * np.exp(-2.0 * tau)
fig, ax = plt.subplots(figsize=(6.2, 4.0))
ax.plot(tau, hq, label=r"$h_Q$")
ax.plot(tau, hs, label=r"$h_{sep}$")
ax.plot(tau, Delta, linestyle="--", label=r"$\Delta=h_Q-h_{sep}$")
ax.set_xlabel(r"dephasing time $\gamma_\phi t$")
ax.set_ylabel("support / normalized excess-flux units")
ax.set_title("Exact contraction under independent pure dephasing")
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(FIG / "fig7_dephasing_robustness.pdf")
fig.savefig(FIG / "fig7_dephasing_robustness.png", dpi=220)
plt.close(fig)

print("generated v0.3 figures")
