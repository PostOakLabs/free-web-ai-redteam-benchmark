You are documenting how ASIC physical-design closure practice CHANGED between the 28nm era and the 7nm/5nm era — the deltas a veteran who did both would name, which rarely get written down because each era's practitioners assume their normal.

**List up to 10 deltas** across areas like: what dominates timing closure (wire vs cell delay, variation); congestion character (pin access vs channel routing); the rise of via/pin-access-driven DRC; power-grid vs routing-resource tension; multi-patterning/coloring constraints entering placement; library/Vt-mixing strategy; clock distribution style shifts; signoff corner explosion; IR/EM moving from afterthought to first-class; hold closure difficulty; utilization targets and why they moved.

**Each delta is one object:**

{"delta_name", "at_28nm": how it worked / what mattered then, "at_7nm_5nm": how it works now and what changed, "why_it_changed": the physical/process mechanism driving the shift, "what_breaks": the mistake a 28nm-trained engineer makes on a 7nm block (or vice versa) and its observable symptom, "workflow_impact": what step/tool-stage absorbed the new work, "confidence": 0.0–1.0}

**Hard rules:** the `what_breaks` field carries the value — a delta without a concrete cross-era mistake is trivia. Mechanisms must be physical (resistance scaling, EUV vs multi-patterning, Vt granularity), not hand-waving. Only include shifts you genuinely know; numbers only where genuinely typical ("order of"). No invented tool, chip, or company names. Fewer sharp deltas beat ten vague ones. **Output: a single bare JSON array and NOTHING else.**

[prompt-version: K-v1 2026-08-31]
