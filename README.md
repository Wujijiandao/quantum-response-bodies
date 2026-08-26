# Quantum Response Bodies

Reproducibility software for **fixed-marginal response geometry in quantum metamaterial scattering**.

Author: **Yuzhan Zhang** (Independent Researcher)  
ORCID: https://orcid.org/0009-0000-3121-7972

## Release status

This package is **v1.0.0-rc1**, a GitHub-ready release candidate produced after the v0.6 scientific-freeze audit. It is not yet the final Zenodo archival release. Promote it to `v1.0.0` only after the author personally verifies the manuscript, references, sign conventions, and numerical claims.

## Scope

The repository implements analytic and numerical checks supporting a theoretical study of quantum and separable electromagnetic response bodies at fixed one-body marginals. It includes:

- exact two- and three-emitter response-body checks;
- XY support-function calculations;
- scaled-elliptope / polar-body constructions;
- three-setting photon-flux reconstruction;
- Lindblad and pure-dephasing robustness checks;
- free-space Lehmberg Green-tensor couplings;
- exact symmetric quantum support under noisy readout;
- reproducible product-numerical-range dual checks for the separable noisy support;
- proof-sensitive v0.6 scientific-freeze regressions;
- deterministic figure generation.

## Reproduce

```bash
python -m pip install -e .[plot]
python reproducibility/run_all.py
```

Expected final line in this release candidate:

```text
ALL v1.0.0-rc1 REPRODUCIBILITY CHECKS PASSED
```

The heavier global product-dual calculation behind the operational Green-tensor figure is run separately:

```bash
python code/scripts/generate_v050_operational_support.py
```

## Scientific-status note

The ideal response-body geometry and the permutation-symmetric quantum noisy support are analytic/exact within the stated model. The noisy separable support has an exact convex-dual reduction, but the remaining finite-dimensional product numerical range is evaluated by reproducible global differential-evolution searches. Independent fixed-seed freeze-time checks reproduce the reported points to approximately `1e-10` or better; this is not claimed to be a formal global-optimality proof for all continuous times.

See `SCIENTIFIC_FREEZE_NOTES.md` for the theorem-by-theorem audit and documented implementation caveats.

## Repository layout

- `code/qrb/` - theory, input-output, Green-tensor and optimization modules
- `code/tests/` - deterministic and proof-sensitive regression tests
- `code/scripts/` - figure and numerical-check scripts
- `reproducibility/` - one-command regression runner and requirements
- `results/` - deterministic JSON outputs
- `figures/` - generated research figures

## GitHub + Zenodo

The intended public repository name is `quantum-response-bodies`. After author scientific sign-off:

1. change `1.0.0-rc1` / `1.0.0rc1` metadata to `1.0.0`;
2. push the cleaned repository to GitHub;
3. enable the repository in Zenodo's GitHub integration;
4. create GitHub Release `v1.0.0`;
5. record the Zenodo **version DOI** and **concept DOI**;
6. cite the version DOI in the exact manuscript submitted to the journal.

See `GITHUB_ZENODO_RELEASE_PLAN.md` and `RELEASE_CHECKLIST.md`.

## Citation

See `CITATION.cff`. Do not cite the RC as the final archival object if a Zenodo-backed `v1.0.0` release is available.

## License

Source code is released under the MIT License.
