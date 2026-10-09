This task is about the **Basel IRB risk-weight function** (BCBS CRE31 — the capital requirement K for unexpected loss, using the asymptotic single risk factor model).

Produce up to 4 worked capital computations at benchmark parameters — PD ∈ {0.5%, 1%, 3%, 10%}, LGD 45%, corporate correlation formula — each computed STEP BY STEP: the correlation R from PD per the CRE31 formula, Φ⁻¹(PD), Φ⁻¹(0.999), the full K expression with the maturity adjustment (state M and b(PD) explicitly), and the risk weight (K × 12.5 × EAD basis).

**Output: a single bare JSON array** of:

{"case_name", "inputs": {pd, lgd, m, ead}, "computation": every intermediate — R, Φ⁻¹(PD), Φ⁻¹(0.999), the inner Φ argument, Φ(·), K before and after maturity adjustment, risk weight — with values, "result": {k_pct, risk_weight_pct}, "formula_basis": the exact CRE31 formula structure you used, stated symbolically, "known_benchmark": if you know a published benchmark value for this parameter set (e.g. the ≈92% risk weight at PD 1% from Basel calibration documents), state it and whether your computation matches, "weakest_point"}

**Hard rules:** every step recomputed mechanically — including your Φ⁻¹ values (Φ⁻¹(0.999)=3.0902, Φ⁻¹(0.01)=−2.3263: get these right or the whole case discards); the formula GROUPING (where √R and √(1−R) sit) is where implementations err — state it symbolically and exactly; if your computed risk weight disagrees with a known benchmark you cited, report the disagreement rather than adjusting numbers to match. No prose outside the JSON.

[prompt-version: C1-IRB-v1 2026-08-31]
