I am mapping published, citable, DETERMINISTIC calculations in semiconductor-related regulation and standards — formulas or threshold tests a calculator could implement exactly, with a citable clause behind every number.

**List up to 12 entries** across families like: ISO 26262-5 hardware architectural metrics (SPFM, LFM, PMHF and ASIL targets); DO-254 design-assurance-level objective mappings; CHIPS Act incentive percentages/thresholds; US export-control parameters for semiconductors (EAR ECCN 3A090/4A090-class thresholds such as total processing performance); JEDEC reliability math (FIT-rate calculation, acceleration models); or any other semiconductor standard/regulation with published deterministic math you can NAME.

**Output: a single bare JSON array** of:

{"calculation": what is computed, "formula_or_test": stated as precisely as you can, "inputs": [...], "authority": the standard/law by exact name and part, "clause_locator": section/clause number IF you truly know it else null, "publicly_retrievable": your belief whether the authoritative text is free or paywalled, "volatility": how often the numbers change, "confidence": 0.0–1.0 that formula AND authority are stated correctly}

**Hard rules:** never invent a clause number — null beats a guess; a formula you only half-remember gets low confidence and a note; fewer verified-quality entries beat twelve vague ones. Every entry will be checked against the primary text before any use. No prose outside the JSON.

[prompt-version: E-v2 2026-08-31]
