# Task: derive and verify inflation-indexed regulatory threshold tables

You are given verified official values. Every computation must be shown step by step; all arithmetic will be recomputed mechanically, and every honesty label is taken at face value.

**Given (official, verified):** US Regulation Z qualified-mortgage points-and-fees tiers.
- 2023: tier A $124,331 · tier B fixed $3,730 · tier C floor $24,866 · tier D fixed $1,243
- 2024: tier A $130,461 · tier B fixed $3,914 · tier C floor $26,092 · tier D fixed $1,305
- The 2025 adjustment reflects a 3.4 percent CPI-U increase; the 2024 adjustment reflected 4.9 percent.

**Tasks:**
1. Compute the implied 2023→2024 adjustment factor per tier (4 factors, each to 6 decimal places, arithmetic shown). State whether the four factors are mutually consistent with a single uniform factor, and with the stated 4.9 percent.
2. Project the 2025 values per tier by applying 3.4 percent to the 2024 values, with the rounding rule you infer from the 2023→2024 step (state the rule you inferred and why). Show every multiplication and rounding.
3. The actual official 2025 tier A value is $134,841. Compare your projection; if it differs, compute the exact factor that WOULD produce $134,841 from $130,461 and state the discrepancy in basis points.
4. `weakest_point`: the single strongest reason your projection could differ from the official figure (rounding convention? factor precision? index vintage?) — a concrete mechanism, not a hedge.

**Output:** bare JSON only: `[{"task": 1..4, "steps": "<all arithmetic>", "answer": "...", "evidence_level": "computed"}]` plus a final object `{"weakest_point": "..."}`.
