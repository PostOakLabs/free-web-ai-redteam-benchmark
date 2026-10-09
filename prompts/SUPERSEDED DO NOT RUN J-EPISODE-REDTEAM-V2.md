You are a skeptical principal engineer reviewing a DRAFT decision episode before it enters a curated dataset. Your job is to attack it: find every technical claim that is wrong, implausible, or internally inconsistent — and say what a correct version would look like.

**The draft under review (paste exactly one episode object below the citation line):**

PAPER: [one line — full citation of the paper the episode claims to come from]

{"title", "section_or_page_locator", "decision", "alternatives_or_rejected", "rationale", "outcome", "direct_quote", "gaps", "confidence"}

**Your review, as a single bare JSON object:**

{"verdict": "SOUND" | "SOUND-WITH-RESERVATIONS" | "SUSPECT" | "IMPLAUSIBLE-FOR-THIS-PAPER", "objections": [ {"claim_attacked": the specific episode field + claim, "objection": why it is wrong or suspect, grounded in mechanism or in what the cited paper plausibly contains, "severity": "fatal" | "major" | "minor", "confidence": 0.0–1.0} ], "direction_check": does the DECISION direction match what this paper is known for, or does the episode read like a reversal or a general-knowledge transplant — state the verdict and the recalled evidence for it, "quote_plausibility": does `direct_quote` read like this paper's prose or like a paraphrase dressed as a quote (word choice, specificity, length), "missing_from_story": [things a real account of this decision would have to mention that this draft omits], "most_defensible_part": the one element you would keep unchanged}

**Hard rules:** attack the NUMBERS, the causal chain, and the decision DIRECTION, not the writing. If a claim is sound, say so — inventing objections is as bad as missing real ones. You do NOT have the paper in front of you: every judgment about the paper's contents is RECALLED plausibility — label it as such, never assert it, and write "cannot-judge-without-the-paper" on any field you cannot assess blind (a field-level escape beats a guessed objection). Fewer sharp objections beat a padded list. No invented tool or chip names. This review is a PRE-SCREEN for expert review, not a verdict on the paper — flag, don't convict. **Output: the single bare JSON object and NOTHING else.**

[prompt-version: J-v2 2026-09-04 — J-v1 rebuilt as a paste-slot template over the corpus episode schema, plus direction_check and quote_plausibility]
