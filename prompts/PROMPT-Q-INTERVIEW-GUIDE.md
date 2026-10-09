You are designing an expert-interview elicitation guide: the exact questions that extract a complete engineering-decision case study from a senior ASIC physical-design engineer's memory in a 30-minute conversation. The target record has this shape: prior state → observation (with metrics) → hypothesis → candidates considered WITH why each rejected one was rejected → chosen intervention → measured outcome → lessons. Veterans compress stories and skip the rejected paths; the guide's job is to decompress honestly without leading the witness.

**Output: a single bare JSON object:**

{"opening": [2-3 questions that surface a GOOD candidate story from memory — ones selecting for failure-and-recovery with real stakes, not success theater],
"decompression": [6-10 entries of {"question", "extracts": which record field it fills, "follow_up_if_vague": the probe when the first answer is compressed, "leading_risk": how this question could contaminate the answer and the neutral phrasing that avoids it}],
"rejected_paths": [3-4 questions specifically for recovering alternatives-considered and why-rejected — the hardest material to elicit because experts forget the roads not taken; include at least one memory-jogging technique],
"numbers": [2-3 questions that recover approximate metrics honestly — including how to record "order of magnitude only" without pressuring false precision],
"verification": [2-3 questions the interviewer asks to test the story's internal consistency in real time — the polite versions of "that number seems too good"],
"closing": [1-2 questions that surface the NEXT story before the session ends],
"anti_patterns": [3-5 interviewer mistakes that corrupt episodes, each with the observable symptom in the resulting record]}

**Hard rules:** questions must be usable verbatim by a non-expert interviewer; every decompression question maps to a named record field; the leading_risk field is mandatory — a guide that doesn't know how it contaminates is not a guide; ground techniques in real elicitation practice where you know it (cognitive interviewing, critical decision method) and name the technique when you use it. No prose outside the JSON.

[prompt-version: Q-v1 2026-08-31]
