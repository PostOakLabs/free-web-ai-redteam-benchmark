You are reconstructing the signoff review checklists senior ASIC physical-design leads actually use — the ordered questions a reviewer asks before approving a milestone, which rarely get written down publicly.

**Cover exactly these 4 review gates:** floorplan review (before placement starts), pre-CTS review (placement done, clocks next), pre-tapeout timing signoff review, and physical verification signoff review (DRC/LVS/antenna/ERC).

**For each gate, output one object:**

{"review_gate", "purpose": what this review exists to catch that later gates cannot cheaply fix, "checks": [6-10 entries of {"question": the actual question the reviewer asks, "evidence_demanded": what artifact/report answers it, "red_flag": the answer that stops the review, "why_it_matters": what escapes downstream if this is waved through}], "kill_questions": [1-2 questions that most often actually stop a review in practice], "waiver_culture": one honest sentence on what gets waived at this gate in real projects and what the waiver later costs, "confidence": 0.0–1.0}

**Hard rules:** the value is in reviewer-grade specificity — "is timing clean?" is worthless; "show me the histogram of setup slack by clock group; a healthy pre-CTS review has the wall at zero, not a tail at −300 ps" is the level wanted. Order checks the way a real reviewer sequences them. No invented tool, chip, or company names. Where the checklist differs by node era (28nm vs 7nm), say so inside the relevant check. Fewer sharp checks beat ten vague ones. **Output: a single bare JSON array of the 4 objects and NOTHING else.**

[prompt-version: I-v1 2026-08-31]
