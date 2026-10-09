You are authoring candidate test vectors for deterministic hardware-assurance calculators. Every vector will be verified by mechanical recomputation; arithmetic that does not close discards the vector.

**Target calculations (produce 3 vectors EACH):**
1. **ISO 26262 SPFM**: given a fault distribution (λ_SPF, λ_RF, λ_MPF_latent, λ_safe, totals), compute SPFM and state which ASIL targets it meets.
2. **JEDEC FIT from accelerated test**: given device-hours, failures, confidence level, and Arrhenius parameters (Ea, use/stress temperatures), compute the acceleration factor and the FIT point estimate at confidence.
3. **EAR TPP**: given a processor's specifications (TOPS at stated bit-widths), compute TPP and state which side of the 3A090 threshold it falls on.

**Each vector is one object in a bare JSON array:**

{"calculation", "vector_name": descriptive of what it exercises, "inputs": {every input with value and units}, "computation": the arithmetic shown STEP BY STEP with intermediate values, "expected_output": {final values with units}, "discriminates": what this vector tests that the others do not (a boundary crossing, a degenerate input, a realistic mid-range case — each calculation's 3 vectors must include at least one THRESHOLD-BOUNDARY case where the result lands exactly at or adjacent to a regulatory limit), "known_uncertainty": which input assumptions or formula details you are least sure of}

**Hard rules:** step-by-step arithmetic is mandatory and will be recomputed — a vector whose stated steps don't reproduce its expected_output is discarded and counts against you; realistic input magnitudes (a FIT test with 3 device-hours is not a vector); do not invent current regulatory threshold values — where a threshold is needed and you are unsure of the current number, parameterize it as a named constant and say so. No prose outside the JSON.

[prompt-version: T-v1 2026-08-31]
