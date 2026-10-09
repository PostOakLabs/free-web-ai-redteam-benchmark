This task is about **Regulation Z, Appendix J to 12 CFR Part 1026** — the actuarial method for computing the Annual Percentage Rate for closed-end credit, including its published computational examples.

From your knowledge of APPENDIX J SPECIFICALLY (its unit-period rules, fractional-period treatment, and worked examples), produce up to 5 worked APR computations covering: a regular monthly transaction, an irregular first period (odd days), a single-advance single-payment transaction, and at least one case with an irregular payment schedule.

**Output: a single bare JSON array** of:

{"case_name", "appendix_basis": which Appendix J section/example it follows as best you recall else null, "inputs": {amount financed, payment schedule, finance charge or payment amounts — with values}, "unit_period_analysis": how unit-periods and fractions are determined for this case per Appendix J's rules, "computation": the iteration/equation setup STEP BY STEP (the actuarial equation with the values substituted; iterations may be summarized but the equation must be exact), "result_apr": the APR with the rounding Appendix J prescribes, "doc_vs_general": "confident-in-appendix-j" | "probably" | "constructed-from-general-APR-knowledge", "weakest_point"}

**Hard rules:** the actuarial equation setup will be recomputed mechanically — a case whose equation doesn't reproduce its APR is discarded; the unit-period/fraction rules are where Appendix J diverges from generic APR math and where your value lies — be precise there or say you can't be; constructed-but-labeled is acceptable. No prose outside the JSON.

[prompt-version: C1-APPJ-v1 2026-08-31]
