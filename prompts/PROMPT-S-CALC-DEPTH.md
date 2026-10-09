You are specifying deterministic calculators for semiconductor hardware-assurance mathematics — depth, not breadth. Every output will be verified against the authoritative text and by recomputation; anything unverifiable is discarded.

**Cover exactly these 4 calculation families:**
1. **ISO 26262-5 hardware architectural metrics**: SPFM and LFM formulas (exact expressions over λ terms — single-point, residual, latent, multiple-point, safe faults) and the ASIL B/C/D target values for each; plus PMHF and its ASIL targets.
2. **JEDEC FIT-rate math**: the FIT calculation from accelerated-test data (JESD85-class): χ²-based point estimate with confidence level, and the Arrhenius acceleration factor formula with typical activation-energy values and their applicability caveats.
3. **EAR advanced-computing parameters**: the Total Processing Performance (TPP) formula and the performance-density formula as defined for ECCN 3A090, with the current threshold values and their units, stated exactly as the regulation defines them.
4. **CHIPS Act incentives math**: the investment tax credit percentage (48D) and any statutory eligibility thresholds that are pure calculations, with the exact statutory locators.

**Each family is one object in a bare JSON array:**

{"family", "formulas": [{"name", "expression": stated precisely with every variable defined, "variables": [{"symbol", "meaning", "units"}], "worked_example": one fully-worked numeric example with self-consistent arithmetic shown step by step, "authority", "clause_locator": exact section IF truly known else null, "known_uncertainty": what part of your statement you are least sure of}], "edge_cases": [1-3 boundary conditions a calculator must handle (division by zero, undefined regions, threshold-exactly-equal semantics)]}

**Hard rules:** the worked examples are the core deliverable — their arithmetic will be recomputed mechanically, and an example that doesn't recompute discredits the whole family entry; null beats a guessed clause number; a formula you only half-remember gets stated with its `known_uncertainty` filled honestly; no invented threshold values — if you do not know the current number, say UNKNOWN-CURRENT-VALUE. No prose outside the JSON.

[prompt-version: S-v1 2026-08-31]
