This task is about **MiCA asset-referenced/e-money token reserve requirements** (Regulation (EU) 2023/1114 — reserve of assets, and the own-funds requirements of Articles 35/45 family).

Produce up to 4 worked cases: (1) a reserve-coverage test — token supply, reserve asset values, the coverage ratio, and the pass/fail against full-backing; (2) an own-funds computation (the percentage-of-reserve or fixed-minimum tests, whichever you know precisely — state the article and the current percentages ONLY if you actually know them, else parameterize as named constants); (3) a stressed-coverage case where reserve assets decline by given haircuts and coverage is retested; (4) a redemptions-at-par case showing the obligation math.

**Output: a single bare JSON array** of:

{"case_name", "inputs": with values and units, "computation": step by step, "result": including the regulatory verdict (adequate/inadequate and against WHICH test), "article_basis": the MiCA article as best known — null over a guess, "tail_convention": for any percentile/stress statistic, state explicitly WHICH tail is adverse for the metric (coverage: LOW tail is adverse — higher coverage is better) and that your test examines the adverse tail, "weakest_point"}

**Hard rules:** arithmetic recomputed mechanically; the `tail_convention` field is mandatory because testing the favorable tail of a higher-is-better metric is a real observed defect class — a case whose stress test examines the wrong tail is itself the failure; no invented percentage thresholds — UNKNOWN-CURRENT-VALUE with a named parameter beats a guessed number. No prose outside the JSON.

[prompt-version: C1-MICA-v1 2026-08-31]
