# Numerical methods

## Deterministic regression suite

Run:

```bash
python reproducibility/run_all.py
```

This executes exact-response checks, analytic theorem regressions, the calibrated input-output reconstruction tests, Green-tensor benchmark checks, noisy-support consistency tests, v0.6 proof-sensitive freeze tests, v0.7 operational-claim tests, and deterministic figure generation.

## Operational Green-tensor support calculation

Run separately:

```bash
python code/scripts/generate_v050_operational_support.py
```

For the permutation-symmetric equilateral trimer, the fixed-marginal quantum support is evaluated exactly by excitation-sector spectral optimization and a small linear program. The separable problem is reduced by convex duality to a product numerical range. Its remaining nonconvex product-state maximization is evaluated with differential evolution using the fixed seeds

```text
20260826, 20260827, 20260828
```

at each reported checkpoint. The JSON result records each multistart value and their spread.

The manuscript intentionally describes this separable component as a reproducible multistart numerical estimate, not as a formal continuous-time global-optimality certificate.

## Environment

The core suite uses NumPy, SciPy and Matplotlib. Exact package versions can be installed from `reproducibility/requirements.txt`; project metadata are in `pyproject.toml`.
