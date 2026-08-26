# v1.0.0 release checklist

Current package: **v1.0.0-rc1**.

- [x] v0.6 theorem-by-theorem scientific-freeze audit completed internally.
- [x] Proof-sensitive regression suite added.
- [x] Public repository excludes submission strategy, cover letter, and private novelty notes.
- [x] Clean-package reproducibility test to be run before delivery.
- [ ] Author personally verifies every theorem, proof, sign convention, reference, and numerical claim.
- [ ] Author supplies corresponding email in the manuscript/submission metadata.
- [ ] Change `pyproject.toml` version from `1.0.0rc1` to `1.0.0`.
- [ ] Change `CITATION.cff` version from `1.0.0-rc1` to `1.0.0` and confirm final release date.
- [ ] Add final GitHub repository URL to metadata/readme after repository creation.
- [ ] Validate `CITATION.cff`.
- [ ] Run `python reproducibility/run_all.py` in a fresh environment and update expected final line to `ALL v1.0.0 REPRODUCIBILITY CHECKS PASSED`.
- [ ] Confirm GitHub Actions pass on Python 3.10 and 3.12.
- [ ] Enable the public repository in Zenodo GitHub integration.
- [ ] Create GitHub Release `v1.0.0`.
- [ ] Verify Zenodo creator spelling and ORCID.
- [ ] Record version DOI and concept DOI in `RELEASE_DOI_RECORD.md`.
- [ ] Insert version DOI into the manuscript Data Availability statement.
- [ ] Recompile and inspect the exact DOI-bearing submission PDF.
