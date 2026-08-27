# Final Verification Report - v1.0.0

Date: 2026-08-27

## Freeze scope

`v1.0.0` promotes the v0.7 adversarial-referee scientific revision to the first frozen release. The promotion changed release/version metadata and archival documentation but did not add a new theorem, physical model, numerical claim, or figure result. Historical v0.6/v0.7 audit files remain labeled with their original versions.

## Reproducibility

The complete public-repository runner was executed from the frozen v1.0.0 tree and exited with status 0. Final line:

```text
ALL v1.0.0 REPRODUCIBILITY CHECKS PASSED
```

The suite covers exact two-emitter response bodies, v0.2 theorem regressions, v0.3 input-output reconstruction, v0.4 Green-tensor checks, v0.5 operational-support checks, v0.6 proof-sensitive scientific-freeze regressions, v0.7 operational-claim regressions, deterministic figures, Monte Carlo sanity checks, and analytic theorem summaries.

The heavier multistart operational Green-tensor calculation remains a separate reproducible script and its stored fixed-seed results are unchanged from the audited v0.7/RC2 revision.

## Manuscript build

The frozen REVTeX manuscript was compiled twice with `pdflatex -interaction=nonstopmode -halt-on-error`. Result:

- 9 pages;
- US Letter page size;
- successful compilation with no fatal TeX error.

The resulting PDF was rendered at 200 dpi and all nine pages were visually inspected as a contact sheet. No clipped text, overlapping blocks, black squares, missing equations, or broken glyphs were observed.

## Scientific claim boundary

The frozen package preserves the v0.7 claim hierarchy:

- the ideal fixed-marginal response-body results are analytic/exact within the stated model;
- the three-flux separable-compatibility criterion is exact;
- the noisy quantum support is exact within the permutation-symmetric benchmark;
- the noisy separable support uses an exact convex-dual reduction followed by reproducible multistart nonconvex product-numerical-range searches; it is not represented as a formal continuous-time global-optimality certificate.

## External metadata intentionally pending

The following are not fabricated in this release and must be supplied externally before journal submission:

1. corresponding-author public email;
2. Zenodo v1.0.0 version DOI and concept DOI;
3. final submission-date author/reference/policy sign-off.

The public code release can be archived at Zenodo exactly as v1.0.0. The manuscript should then cite the resulting **version DOI**.

## Verdict

**PASS - v1.0.0 scientific-content and reproducibility freeze.**
