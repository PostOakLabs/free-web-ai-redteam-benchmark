This task is about the **OFAC 50 Percent Rule** (blocked persons owning 50% or more in the aggregate, directly or indirectly — OFAC guidance and FAQ 398/401 family).

Produce up to 5 worked ownership-graph cases with hand-computed aggregate ownership. **At least 2 MUST be convergent graphs** (the same blocked owner reaches a target through multiple paths whose contributions must be SUMMED) and **at least 1 must include a chain through a majority-owned intermediary** (the indirect-ownership treatment where a ≥50%-owned entity's holdings count).

**Output: a single bare JSON array** of:

{"case_name", "entities": [{"id", "blocked": true|false}], "edges": [{"from", "to", "pct"}], "computation": step by step — each path's contribution, how indirect ownership is treated per the guidance (state the rule you are applying: full attribution through ≥50%-owned intermediaries vs multiplicative — OFAC's actual treatment, be precise or say unsure), the aggregate per target entity, "blocked_verdicts": which entities are blocked under the 50% aggregate test, "guidance_basis": the FAQ/guidance your treatment follows, "weakest_point"}

**Hard rules:** arithmetic recomputed mechanically; the treatment of INDIRECT ownership (attribution vs multiplication through intermediaries) is the load-bearing rule and the place implementations err — state which treatment OFAC's guidance actually prescribes and flag your certainty honestly; edge-order must never matter to your results (aggregates are properties of the graph, not the serialization). No prose outside the JSON.

[prompt-version: C1-OFAC-v1 2026-08-31]
