# Quantum Response Bodies

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22120243.svg)](https://doi.org/10.5281/zenodo.22120243)

Reproducibility software for **fixed-marginal response geometry in quantum-emitter arrays**.

Author: **Yuzhan Zhang** (Independent Researcher)  
ORCID: https://orcid.org/0009-0000-3121-7972

## Release status

**v1.0.0** is the first frozen archival software release corresponding to the scientific content of the manuscript *Fixed-Marginal Response Geometry for Quantum-Emitter Arrays*. It supersedes the RC1/RC2 review candidates.

The scientific content is frozen. The exact v1.0.0 release is archived on Zenodo with version DOI **10.5281/zenodo.22120243**.

## Scope

The repository implements analytic and numerical checks supporting a theoretical study of quantum and separable electromagnetic response bodies at fixed one-body marginals. It includes:

- exact two- and three-emitter response-body checks;
- XY support-function calculations;
- scaled-elliptope / polar-body constructions;
- three-setting photon-flux reconstruction and separable-compatibility tests;
- Lindblad and pure-dephasing robustness checks;
- free-space Lehmberg Green-tensor couplings;
- exact symmetric quantum support under noisy readout;
- reproducible multistart product-numerical-range dual checks for the separable noisy support;
- proof-sensitive scientific-freeze regressions;
- deterministic figure generation.

## Reproduce

```bash
python -m pip install -e .[plot]
python reproducibility/run_all.py
```

Expected final line:

```text
ALL v1.0.0 REPRODUCIBILITY CHECKS PASSED
```

The heavier operational Green-tensor calculation is run separately:

```bash
python code/scripts/generate_v050_operational_support.py
```

## Scientific-status note

The ideal response-body geometry and the permutation-symmetric quantum noisy support are analytic/exact within the stated model. The noisy separable support has an exact convex-dual reduction, but the remaining finite-dimensional product numerical range is evaluated by reproducible multistart differential-evolution searches. Independent fixed-seed checks reproduce the reported checkpoints to approximately `1e-10` or better. This is not claimed to be a formal global-optimality proof for all continuous times.

Historical scientific-freeze notes are retained in `SCIENTIFIC_FREEZE_NOTES.md`. They preserve the v0.6/v0.7 audit history and are not rewritten as though those checks were originally performed at v1.0.0.

## Repository layout

- `code/qrb/` - theory, input-output, Green-tensor and optimization modules
- `code/tests/` - deterministic and proof-sensitive regression tests
- `code/scripts/` - figure and numerical-check scripts
- `reproducibility/` - one-command regression runner and requirements
- `results/` - deterministic JSON outputs
- `figures/` - generated research figures

## Citation and archival DOI

Citation metadata are provided in `CITATION.cff`. The version-specific archival citation for this release is **10.5281/zenodo.22120243**. The manuscript cites this DOI in its Data Availability statement.

## License

Source code is released under the MIT License.
