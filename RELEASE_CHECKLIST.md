# v1.0.0 release checklist

## Completed in the frozen package

- [x] Scientific content frozen from the v0.7 adversarial-referee revision.
- [x] Software version updated to `1.0.0`.
- [x] `CITATION.cff` updated to `1.0.0`.
- [x] Reproducibility runner updated to report `v1.0.0`.
- [x] Hidden `.gitignore` and `.github/workflows/tests.yml` included in the ZIP.
- [x] Release notes and Zenodo metadata prepared.
- [x] SHA-256 manifest regenerated after final verification.

## External publication steps

- [ ] Update the GitHub working tree to exactly this package.
- [ ] Ensure `.github/workflows/tests.yml` exists in GitHub (use Git CLI or GitHub “Create new file” if drag-and-drop omits dot paths).
- [ ] Ensure `.gitignore` exists in GitHub.
- [ ] Confirm GitHub Actions passes on Python 3.10 and 3.12.
- [ ] Enable the repository in Zenodo GitHub integration.
- [ ] Create Git tag/release `v1.0.0` (not a pre-release).
- [ ] Record the Zenodo version DOI and concept DOI.
- [ ] Cite the version DOI in the exact journal manuscript submitted.
