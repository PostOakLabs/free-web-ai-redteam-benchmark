You are building a differential-diagnosis reference for ASIC physical-design failure triage — the kind a senior engineer carries in their head: given a symptom, what are the candidate causes, in what order do you check them, and what does each check cost?

**Cover exactly these 6 failure classes:** FAIL\_CONGESTION, FAIL\_TIMING (setup), FAIL\_TIMING (hold), FAIL\_IR\_DROP, FAIL\_CTS (clock tree), FAIL\_DRC (routing DRCs).

**For each class, output one object:**

{"failure\_class", "symptoms": \[2-4 distinct observable signatures, each with the metric shape that distinguishes it — e.g. how a report LOOKS different when the cause differs], "candidate\_causes": \[4-6 entries of {"cause", "distinguishing\_check": the specific report/experiment that confirms or rules it out, "check\_cost": minutes|hours|days, "typical\_fix", "fix\_cost"}], "ordering\_rationale": one sentence on why a veteran checks in that order (cheapest-first? highest-prior-probability-first?), "classic\_trap": the misdiagnosis engineers most commonly make in this class, "confidence": 0.0–1.0}

**Hard rules:** the value is in the DISTINGUISHING checks — "look at the timing report" is worthless; "if all failing paths share one common clock-gating cell, it's X; if they spread across unrelated hierarchies, it's Y" is the level wanted. Numbers only where they are genuinely typical (say "order of" if approximate). No invented tool names or chip names. Where practice differs by node era (28nm vs 7nm), say so briefly inside the relevant entry. **Output: a single bare JSON array of the 6 objects and NOTHING else.**

\[prompt-version: F-v1 2026-08-31]

