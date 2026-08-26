# Operational-support numerical method (v1.0.0-rc1)

For the equilateral three-emitter Lehmberg benchmark, the Heisenberg effective observable is

`B(t) = exp(L^dagger t)[B]`, with `B = O12 + O13 + O23`.

## Quantum support

Because the benchmark is permutation symmetric and U(1)-covariant, `B(t)` is block diagonal in total excitation number. For each sector `k=0,1,2,3`, the code computes its largest eigenvalue `a_k(t)`. The fixed local marginals `I/2` are then enforced exactly by a four-variable linear program over excitation-sector weights with mean excitation `3/2`.

## Separable support

Permutation averaging and global U(1) twirling reduce the fixed-marginal separable problem to a convex dual over the mean longitudinal Bloch component. The remaining inner optimization is the product numerical range of a three-qubit Hermitian operator. It is solved by SciPy differential evolution over three Bloch `z` coordinates and two independent relative phases.

For the reported `d=0.35 lambda` benchmark, the aligned-equatorial phase-twirled separable construction saturates the product dual at all eight reported checkpoints on `0 <= Gamma0 t <= 4`, with the largest absolute numerical residual below `1.1e-10`.

The code therefore distinguishes exact analytic/model reductions from the numerical global search used to evaluate the product numerical range. The latter is reproducible but should not be described as a formal computer-assisted proof.


## v0.6 freeze-time independent rechecks

At `Gamma0 t = 0.08838, 1, 2, 4`, the product-dual inner optimization was repeated with two distinct fixed seeds. Both searches reproduced the aligned-equatorial dual value to approximately `1e-10` or better. These checks are included as a robustness audit of the reported numerical branch, not as a formal certificate for all continuous times.
