This task is about the **TRID fee-tolerance rules — 12 CFR §1026.19(e)(3)** — the zero-tolerance, 10%-aggregate-tolerance, and no-tolerance-limit buckets for comparing Loan Estimate to Closing Disclosure charges.

Produce up to 5 worked tolerance-test cases, each with a fee table (LE amount vs CD amount per fee, bucket assignment per the rule) — and **at least 2 cases MUST have mixed directions inside the 10% bucket** (some fees increased, some decreased), because the 10% test compares AGGREGATE to AGGREGATE and mixed-direction cases are where implementations get it wrong.

**Output: a single bare JSON array** of:

{"case_name", "fees": [{"name", "bucket": "zero_tolerance" | "ten_pct_aggregate" | "no_limit", "le_amount", "cd_amount"}], "computation": step by step — per-bucket sums, the 10% threshold (Σle × 0.10), the aggregate comparison (Σcd vs Σle, NOT the sum of increases), zero-tolerance per-fee checks, "violations": which buckets violate and the cure amount per §19(e)(3), "clause_basis": the exact provision each conclusion rests on as best you know, "weakest_point"}

**Hard rules:** arithmetic recomputed mechanically; the load-bearing rule is aggregate-vs-aggregate for the 10% bucket — a case that computes the sum-of-increases instead is itself the defect this suite exists to catch (state the distinction explicitly in at least one case); bucket assignments must follow the rule's actual criteria (whether the borrower can shop, etc.) — if unsure of an assignment, say so. No prose outside the JSON.

[prompt-version: C1-TRID-v1 2026-08-31]
