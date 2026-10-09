This task is about one specific published paper: **"POWER4 system microarchitecture" — J. M. Tendler, J. S. Dodson, J. S. Fields, Jr., H. Le, B. Sinharoy — IBM Journal of Research and Development, Vol. 46, No. 1, January 2002, pp. 5–26.**

From your knowledge of THIS SPECIFIC PAPER (not your general knowledge of the POWER4 processor), reconstruct up to 5 engineering-decision episodes that the paper itself describes — design objectives weighed, alternatives considered or rejected, trade-offs made (its guiding-principles section and discussions like the clock-frequency philosophy, RAS approach, and interconnect choices are examples of the kind of material meant).

**Output: a single bare JSON array** of:

{"title", "where_in_paper" (section name or topic area, as best you recall), "decision": what was decided, "alternatives_or_rejected": what the paper says was considered or argued against, "rationale": the paper's stated reasoning, "outcome": what the paper reports resulted, "paper_vs_general" — exactly one of "confident-this-is-in-the-paper" | "probably-in-the-paper" | "from-general-POWER4-knowledge-not-necessarily-this-paper", "confidence": 0.0–1.0}

**Hard rules:** the `paper_vs_general` field is the most important one — be brutally honest about whether you are recalling THIS paper or general knowledge; mislabeling general knowledge as paper content is the worst possible output. If you do not know this paper at all, output `[]`. Fewer honest entries beat five vague ones. No prose outside the JSON.

[prompt-version: D2-v4 2026-08-31]
