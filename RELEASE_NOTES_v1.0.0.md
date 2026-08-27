# v1.0.0 - First Archival Release

This is the first frozen archival release of **Quantum Response Bodies**, corresponding to the scientific content of the manuscript *Fixed-Marginal Response Geometry for Quantum-Emitter Arrays*.

## Main contents

- Fixed-marginal quantum and separable response bodies for quantum-emitter arrays.
- One-body no-go result for correlation-dependent response at fixed local marginals.
- Quantum/classical XY support-function correspondence.
- Exact three-emitter separable body `R_sep^(3) = (1/2) E_3`.
- Exact signed-polar characterization of the three-emitter quantum body.
- Three-setting calibrated photon-flux reconstruction and exact separable-compatibility criterion.
- Exact two-emitter minimum-negativity resource law.
- Open-system affine closure and stability bounds.
- Free-space Lehmberg Green-tensor benchmark.
- Reproducible multistart noisy separable-support estimates with fixed seeds.
- Deterministic regression tests and figure-generation scripts.

## Reproducibility

```bash
python -m pip install -e .[plot]
python reproducibility/run_all.py
```

Expected final line:

```text
ALL v1.0.0 REPRODUCIBILITY CHECKS PASSED
```

The heavier operational-support calculation can be regenerated with:

```bash
python code/scripts/generate_v050_operational_support.py
```

## Scientific scope

The exact ideal response-body theorems do not depend on the nonconvex noisy separable numerical search. For the noisy benchmark, the convex-dual reduction is exact while the remaining product numerical range is evaluated with reproducible multistart global-search heuristics; the release does not claim a formal continuous-time global-optimality certificate.

## Author

Yuzhan Zhang  
Independent Researcher  
ORCID: 0009-0000-3121-7972

## License

MIT License
