# FPM Claim Status & Epistemic Boundaries

To maintain strict epistemic hygiene, the following boundaries apply to the current `v4.4` release of Finite Possibility Mechanics (FPM):

1. **Synthetic Demo $\neq$ Observational Confirmation:**
   The `reproduce_fpm_galaxy_rollover.py --demo-synthetic` mode mathematically validates that the FPM finite-ledger topology successfully produces flat-rotation middle branches with terminal $r^{-1/2}$ rollovers. **It does not constitute empirical proof** until the identical equations are evaluated against blind, far-field observational data.

2. **Baseline Hooks $\neq$ Completed Baseline Comparison:**
   The prediction harness contains reserved execution stubs for baryon-only Newtonian gravity, MOND, and NFW halos. These merely ensure architectural space for comparison; they do not represent a completed statistical victory over standard models.

3. **Real Prediction Requires Real Inputs:**
   The `--predict-real` mode generates mathematically locked prospective predictions. However, it requires an explicitly verified, non-fitted input structural dataset (e.g., SPARC) containing isolated baryonic profiles before these predictions can be tested.

4. **Prediction $\neq$ Evaluation:**
   To prevent "vibes" and implicit data fitting, the prediction pipeline (`reproduce_fpm_galaxy_rollover.py`) is structurally severed from the grading pipeline (`evaluate_fpm_galaxy_rollover.py`). Predictions must be generated and locked by commit hash **before** the evaluation script executes against observational data.
