# GitHub + Zenodo release plan

## Recommended public object

Repository name: **`quantum-response-bodies`**

Purpose: public source code and reproducibility archive supporting the manuscript. The journal manuscript itself does not need to be deposited in the software record; this avoids confusing the software DOI with the eventual article DOI.

Recommended visibility sequence:

1. Keep the working project private/local while the theorem set is still changing.
2. Freeze a submission artifact as `v1.0.0`.
3. Create a **public** GitHub repository containing the cleaned reproducibility repository.
4. Connect that public repository to Zenodo.
5. Create GitHub Release `v1.0.0`.
6. Let Zenodo archive the release and mint a version DOI plus a concept DOI.
7. Put the **version DOI** into the manuscript Data Availability statement before PRA submission.
8. Put the **concept DOI** in the GitHub README badge after the first release, because it resolves to the latest archived version.

## Why this workflow

Zenodo's GitHub integration automatically ingests enabled GitHub releases. The integration works with public repositories and does not provide access to private repositories. A DOI cannot be pre-reserved through the GitHub integration. If a DOI must be reserved before a public GitHub release, use a manual Zenodo draft instead; do not create both a manual record and an automatic GitHub record for the same release.


## Two DOI workflows

### Recommended: GitHub release -> automatic Zenodo archive

Use this for the normal submission release. Make the cleaned repository public, enable it in the Zenodo GitHub integration, and publish GitHub Release `v1.0.0`. Zenodo then ingests the release and creates the archival software record. Insert the resulting version-specific DOI into the manuscript.

### Alternative: manual Zenodo draft when the DOI must be known first

If the DOI must appear inside files before the public GitHub release exists, create a manual Zenodo software draft and use Zenodo's DOI-reservation function before publication. Do **not** then auto-archive the identical GitHub release into a second Zenodo record; choose one archival record for the same software object to avoid duplicate DOIs.

The project currently recommends the automatic GitHub-release route because the manuscript only needs the DOI before journal submission, not before the code release itself.

## DOI policy

- Cite the **version DOI** in the submitted paper and reproducibility statements. This identifies the exact code used for the submitted results.
- Use the **concept DOI** for an evolving project badge or general project citation.
- If the software changes after referee revisions, release `v1.1.0` (or an appropriate semantic version) and update the paper to cite the new version DOI.

## Metadata source

Use a single root-level `CITATION.cff` as the primary GitHub/Zenodo metadata file. Do not also add `.zenodo.json` unless Zenodo-specific fields are actually required; when both are present, Zenodo ignores `CITATION.cff` for GitHub archiving.

Initial metadata:

- Creator: Yuzhan Zhang
- ORCID: 0009-0000-3121-7972
- Affiliation: Independent Researcher
- Resource type: software
- Code license: MIT
- Keywords: quantum metamaterials; quantum optics; entanglement; convex geometry; atomic arrays; reproducibility

After the article obtains a DOI, update `CITATION.cff` with a `preferred-citation` entry pointing to the journal article while retaining the software DOI for the repository itself.

## Release tags

Internal development tags may remain `v0.x.y` locally. Public archival releases should start at:

- `v1.0.0` - exact artifact submitted to PRA.
- `v1.1.0` - scientifically changed revision after referee reports.
- `v1.0.1` - packaging/documentation correction that does not alter scientific output (use sparingly; if files in the reproducibility object change, Zenodo creates a new version DOI).

## GitHub release contents

The public repository should contain:

- `code/qrb/`
- `code/tests/`
- `code/scripts/`
- `reproducibility/`
- deterministic `results/` used in the paper
- figure-generation code; optionally generated figures
- `README.md`
- `CITATION.cff`
- `LICENSE`
- `pyproject.toml`
- `.github/workflows/tests.yml`
- `SHA256SUMS.txt` in tagged release assets if a separate reproducibility ZIP is attached

Keep `submission/`, private review notes, referee strategy, and draft cover letters out of the public repository.

## PRA Data Availability template after DOI minting

`No experimental data were generated or analyzed. The code, deterministic regression tests, and figure-generation scripts supporting this work are archived in Zenodo at [VERSION DOI] and are also available from the associated GitHub repository.`

## Final release checklist

1. Run `python reproducibility/run_all.py` from a fresh environment.
2. Confirm the final line is `ALL v1.0.0 REPRODUCIBILITY CHECKS PASSED` (update runner version text before release).
3. Verify `CITATION.cff` with a CFF validator.
4. Confirm ORCID and creator spelling.
5. Confirm the code license.
6. Remove transient build files and private notes.
7. Create Git tag and GitHub Release `v1.0.0`.
8. Confirm Zenodo ingestion succeeded and record metadata are correct.
9. Record both version DOI and concept DOI in `RELEASE_DOI_RECORD.md`.
10. Insert the version DOI into the manuscript and regenerate the submission PDF.
