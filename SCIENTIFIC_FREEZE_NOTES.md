# Scientific Freeze Audit — v0.6.0

Date: 2026-08-27
Status: **scientific-freeze candidate; not yet author-signed for submission**

## Scope

This audit re-checks the manuscript's principal analytic claims, the microscopic free-space benchmark, the numerical optimization layer, and the novelty boundary. It intentionally distinguishes exact mathematics, reproducible numerical evidence, literature-positioning judgments, and items that still require the author's personal verification before submission.

## Audit summary

| Item | Status | Freeze conclusion |
|---|---|---|
| Fixed-marginal symmetrization theorem | PASS | Exact, with an important sector-degeneracy implementation caveat documented below. |
| Quantum XY support identity | PASS | Follows from the symmetrization theorem for the stated number-conserving, global-bit-flip-invariant operators. |
| Separable planar-XY support | PASS | Product-state reduction and global twirling preserve the fixed marginals; equatorial extremality is now stated explicitly. |
| Three-emitter separable body | PASS | Exact scaled elliptope: `R_sep^(3)=(1/2)E_3`. |
| Three-emitter quantum body | PASS | Spectrahedral-shadow representation independently reconstructed; signed-polar identity retained. |
| Complete-graph scaling | PASS | Closed forms rechecked against direct diagonalization through the regression suite. |
| Two-emitter minimum-negativity law | PASS, scoped | Exact for the stated fixed-marginal response coordinate. The manuscript now cites prior interference/entanglement work and claims only the inverse minimum-resource result. |
| Open-system affine response | PASS | Exact for state-independent CPTP readout; fixed marginals constrain the prepared input class, not necessarily the evolved marginals. |
| Operator-norm stability bound | PASS | Sufficient certificate only; not a necessary closing time. |
| Lehmberg couplings/sign convention | PASS against stated convention | Formula and benchmark values rechecked; author must still perform final primary-source sign audit before submission. |
| Symmetric noisy quantum support | PASS | Exact sector-weight linear program under the stated permutation symmetry. |
| Noisy separable support | PASS as a convex-dual formulation; numerical inner maximization remains numerical | Independent fixed-seed global searches reproduce the reported checkpoints to ~1e-10 or better, but this is not a formal global-optimality proof for every time. |
| Novelty boundary | PASS with restrained language | No direct prior was located for the full fixed-marginal scattering-response-body + exact trimer geometry + inverse resource cost + microscopic noisy-support framework. Individual mathematical and diagnostic ingredients have clear antecedents and are cited. |

## 1. Fixed-marginal symmetrization: proof-sensitive check

The theorem assumes a Hermitian operator `A` that conserves excitation number and is invariant under the global bit flip `X^{\otimes N}`. A top eigenvector can therefore be chosen inside a definite excitation-number sector. Mixing that sector-resolved eigenstate with its global-bit-flipped partner produces locally maximally mixed marginals without changing the expectation value of `A`.

### Implementation pitfall found during the independent audit

A generic eigensolver returned an arbitrary superposition across degenerate one- and two-excitation top eigenspaces in the three-emitter test. Symmetrizing that arbitrary vector did **not** automatically give the required local marginals. This was an implementation issue, not a theorem counterexample: selecting the top eigenvector *within a definite excitation sector*, exactly as the theorem states, reduced the maximum marginal error to approximately `4.4e-16` and the expectation mismatch to approximately `1.8e-15`.

This check is now represented by a dedicated v0.6 regression test so future refactors cannot silently drop the sector condition.

## 2. Three-emitter separable body

For `r=(r12,r13,r23)`, the separable fixed-marginal body is

`R_sep^(3) = (1/2) E_3`,

where `E_3` is the 3x3 correlation elliptope. The proof is now explicit in both directions:

1. Product-state transverse Bloch vectors can be completed with mutually orthogonal auxiliary components to unit Gram vectors, giving the positive-semidefinite correlation matrix.
2. Extreme points of `E_3` have rank at most two; planar Gram representations are realized by equatorial product states, and a global `Z` twirl restores the locally maximally mixed one-body marginals without changing pair responses.

The volume normalization was independently checked: `Vol(E_3)=pi^2/2`, hence `Vol(R_sep^(3))=pi^2/16`.

## 3. Three-emitter quantum body and polar identity

The quantum body is represented by

`R_Q^(3) = {r : exists p in Delta_2, P(p,r) >= 0}`,

with the manuscript's `3x3` matrix `P`.

The necessity proof was strengthened at freeze time. After global `U(1)` twirling, the one-excitation block and the bit-flipped two-excitation block can be combined into a positive-semidefinite matrix `S`. For real response coordinates, `Re(S)` remains positive semidefinite because `x^T Re(S) x = x^dagger S x >= 0` for every real vector `x`. Missing trace weight can be added diagonally without changing the response coordinates.

Independent constructive tests recover randomly sampled feasible response points to machine precision (representative error ~`1.6e-16`). The polar convention is now stated explicitly in the manuscript before using

`(R_Q^(3))^circ = -E_3`.

## 4. Two-emitter inverse resource law

For the stated locally maximally mixed two-qubit response

`r = 2 |<sigma_1^+ sigma_2^->|`,

the minimum negativity is

`N_min(r) = max(0, r-1/2)`.

The lower bound was rechecked through the principal subblock of the **partial transpose**, with the manuscript now explicitly invoking the relevant principal-submatrix/interlacing step. Random locally maximally mixed states in the independent audit produced no violations of the bound, and the analytic achieving family reproduced the law to machine precision.

Novelty is deliberately narrow here. Relations between atomic interference visibility/coherence and concurrence or negativity predate this work, notably J. Suzuki, C. Miniatura, and K. Nemoto, Phys. Rev. A 81, 062307 (2010), DOI 10.1103/PhysRevA.81.062307. The present claim is the minimum entanglement **required to synthesize a prescribed fixed-marginal response**, embedded in the response-body inverse-design framework.

## 5. Open-system and microscopic checks

The affine Heisenberg-picture reduction

`Tr[M Lambda(rho)] = Tr[Lambda^dagger(M) rho]`

was checked independently against direct Schrödinger-picture evolution in the regression suite.

The free-space benchmark uses the standard Lehmberg cooperative-decay/coherent-exchange convention. For an equilateral trimer of side `0.35 lambda` with dipoles normal to the plane, the implementation reproduces

- `Gamma_ij/Gamma_0 = 0.25540786413473576`,
- `Omega_ij/Gamma_0 = 0.28447601704249503`,
- collective decay eigenvalues approximately `(0.7445921359, 0.7445921359, 1.5108157283) Gamma_0`.

Primary source: R. H. Lehmberg, Phys. Rev. A 2, 883 (1970), DOI 10.1103/PhysRevA.2.883.

The manuscript now states explicitly that the fixed-marginal constraint applies to the **prepared initial state classes**. Under amplitude damping or collective radiative decay, the evolved one-body marginals generally do not remain `I/2`; this does not invalidate the Heisenberg-picture comparison because the optimization is over the initial admissible classes.

## 6. Noisy operational support

For the permutation-symmetric trimer, the quantum support of the evolved effective observable is exact after decomposing into excitation-number sectors and optimizing sector weights subject to normalization and mean excitation `3/2`.

The separable problem has an exact convex-dual reduction to a product numerical-range optimization. The remaining finite-dimensional nonconvex inner maximum is evaluated numerically. Freeze-time independent searches used two distinct fixed seeds at `Gamma_0 t = 0.08838, 1, 2, 4`; they agreed with the aligned-equatorial construction within roughly `1e-10` or better at all four checkpoints.

This is strong reproducible evidence, not a symbolic proof that the same ansatz is globally optimal for every continuous time. The paper therefore says **globally optimized numerical product dual** rather than **analytic separable optimum** in the noisy section.

## 7. Novelty boundary after adversarial search

The following adjacent results must remain visible in the manuscript:

- fixed-marginal composite state geometry: O. Rudolph, J. Math. Phys. 45, 4035 (2004);
- energy/observable quantum–separable gaps: M. R. Dowling, A. C. Doherty, and S. D. Bartlett, Phys. Rev. A 70, 062113 (2004);
- product/separable numerical ranges: Z. Puchala et al., Linear Algebra Appl. 434, 327 (2011); L. Simnacher et al., Phys. Rev. A 104, 042420 (2021);
- atom-photon interference as an entanglement diagnostic: J. Suzuki et al., Phys. Rev. A 81, 062307 (2010), plus later radiation-witness work;
- recent three-qubit correlation geometry using different invariant coordinates: S. Shravan et al., Phys. Rev. A 110, 062419 (2024);
- separable descriptions of ideal Dicke superradiance: P. Rosario et al., Phys. Rev. Lett. 135, 133602 (2025); N. S. Bassler, Phys. Rev. A 112, 053713 (2025).

The defensible contribution is therefore **not** the invention of restricted numerical ranges, fixed marginals, entanglement witnesses, or correlation geometry. It is the combination of a physically reconstructible electromagnetic scattering map with fixed local states, the exact three-emitter quantum/separable response geometry, and an inverse resource-cost interpretation, extended into a microscopic open-system benchmark.

Use language such as “to our knowledge” or “we did not locate a prior formulation that combines …”. Do not state “first ever” or “no one has studied this”.

## 8. Remaining pre-submission risks

1. **Author verification:** every proof, sign convention, citation, and numerical claim must be personally checked by the author before submission.
2. **Noisy separable optimization:** the inner product numerical-range calculation is reproducible global numerical optimization, not a formal certificate. If a higher-impact target is pursued, an analytic proof or certified branch-and-bound/SOS bound would materially strengthen the paper.
3. **Scope/title:** “quantum metamaterial scattering” is defensible through the state-programmed-response framing, but “quantum-emitter arrays” is a narrower alternative if an editor views “metamaterial” as requiring stronger homogenization language.
4. **Corresponding email:** still absent from the submission metadata.
5. **Archival DOI:** the submission PDF should cite the exact Zenodo version DOI after the public repository is frozen.
6. **AI disclosure:** APS currently requires substantive AI use in scientific reasoning, derivations, code, simulations/numerical analysis, or scientific-claim drafting to be disclosed; the draft disclosure is retained, but the author remains accountable for the final verification.

## Freeze decision

**PASS AS v0.6 SCIENTIFIC-FREEZE CANDIDATE.** No core theorem was invalidated by the adversarial audit. The main remaining scientific limitation is the non-formal global certification of the noisy separable product optimization; this is explicitly disclosed in the manuscript/method notes rather than hidden.
