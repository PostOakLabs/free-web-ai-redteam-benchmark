This task is about **FRTB expected shortfall** (BCBS MAR33 — the 97.5% ES standard) and parametric ES/VaR under normality.

Produce up to 4 worked cases: (1) parametric ES at 97.5% for a normal P&L (the φ(z)/α factor — with z_{0.975}=1.9600, φ(1.9600), and the ES multiplier vs the VaR multiplier stated separately); (2) the same at 99% (z=2.3263); (3) a liquidity-horizon-scaled ES per MAR33's √(LH/10) structure for one risk factor category; (4) a historical-simulation ES from a supplied small sample (give 20 P&L values, take the tail average per the 97.5% definition — show which observations enter the tail).

**Output: a single bare JSON array** of:

{"case_name", "inputs": with values and units, "computation": step by step with every intermediate (quantiles, densities, scale factors, which sample points average), "result": with units, "formula_basis": symbolic statement of the formula used and its MAR33 anchor as best known, "weakest_point"}

**Hard rules:** all arithmetic recomputed mechanically — quantile and density values must be correct to 4 decimals (φ(1.96)=0.05844, φ(2.3263)=0.02665); the ES-vs-VaR distinction (tail mean vs quantile) must be exact — conflating them is the defect class this suite exists to catch; the historical case must show the tail-selection rule explicitly (how many of 20 observations at 97.5%, and the fractional-observation treatment you chose, named honestly as a convention where the text is silent). No prose outside the JSON.

[prompt-version: C1-FRTB-v1 2026-08-31]
