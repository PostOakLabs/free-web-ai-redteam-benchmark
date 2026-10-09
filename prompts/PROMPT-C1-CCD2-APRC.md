This task is about the **Consumer Credit Directive APRC** — the annual percentage rate of charge formula and the officially published calculation examples in the directive's annex (Directive 2008/48/EC Annex I and its successor Directive (EU) 2023/2225 Annex III).

From your knowledge of THOSE ANNEXES SPECIFICALLY, produce up to 5 worked APRC computations: the basic single-drawdown case, a case with charges paid at conclusion, a case with irregular intervals, and any annex example you can reproduce with its own numbers.

**Output: a single bare JSON array** of:

{"case_name", "annex_basis": which directive + annex example number as best you recall else null, "inputs": {credit amount, drawdown/payment schedule with dates or intervals, charges — with values}, "equation_setup": the APRC equation with the case's values substituted (the Σ drawdowns = Σ repayments discounted form, exact), "computation": the solution steps (iteration summarized, equation exact), "result_aprc": with the rounding the annex prescribes, "assumptions_applied": which of the annex's calculation assumptions (about drawdown timing, one-year intervals, etc.) this case invokes, "doc_vs_general": "confident-this-example-is-in-an-annex" | "probably" | "constructed-from-formula-knowledge", "weakest_point"}

**Hard rules:** equation setups recomputed mechanically; the annex ASSUMPTIONS (immediate full drawdown, interval conventions, day-count) are where implementations diverge from the formula — name every assumption you apply; REVERSING a convention (e.g. which date convention the annex prescribes) flagged-if-unsure beats asserted-wrong; constructed-but-labeled acceptable. No prose outside the JSON.

[prompt-version: C1-CCD2-v1 2026-08-31]
