import sys, json, csv
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from qrb.states import random_density_matrix, random_separable_state
from qrb.response import response_xy

ROOT = Path(__file__).resolve().parents[2]
RES = ROOT/'results'
RES.mkdir(exist_ok=True)
rng = np.random.default_rng(20260826)

# Unconstrained random sampling only sanity-checks the universal separable radius bound.
# Exact fixed-marginal boundary achievability is handled analytically and in unit tests.
q_radii=[]
s_radii=[]
for _ in range(20000):
    q_radii.append(float(np.linalg.norm(response_xy(random_density_matrix(rng=rng)))))
for _ in range(20000):
    s_radii.append(float(np.linalg.norm(response_xy(random_separable_state(rng=rng)))))

summary = {
    'seed': 20260826,
    'n_quantum': len(q_radii),
    'n_separable': len(s_radii),
    'max_sampled_quantum_radius_unconstrained': max(q_radii),
    'max_sampled_separable_radius_unconstrained': max(s_radii),
    'exact_fixed_marginal_quantum_radius': 1.0,
    'exact_fixed_marginal_separable_radius': 0.5,
    'exact_area_ratio_quantum_to_separable': 4.0,
    'exact_hausdorff_radial_gap': 0.5,
}
(RES/'monte_carlo_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
print(json.dumps(summary, indent=2))
