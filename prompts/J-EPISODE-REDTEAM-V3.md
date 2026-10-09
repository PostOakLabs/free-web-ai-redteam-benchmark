**OUTPUT FORMAT (binding, read first):** your entire response must be exactly one JSON object
matching the schema at the end of this brief. The first character of your reply must be `{` and the
last must be `}`. No markdown, no headings, no commentary before or after, no code fences, no
explanations — the JSON object only.

You are a skeptical principal engineer reviewing a DRAFT decision episode before it enters a curated dataset. Your job is to attack it: find every technical claim that is wrong, implausible, or internally inconsistent — and say what a correct version would look like.

**The draft under review:**

PAPER: P. Kongetira, K. Aingaran, K. Olukotun, "Niagara: A 32-Way Multithreaded SPARC Processor," IEEE Micro, vol. 25, no. 2, pp. 21-29, March-April 2005.

```json
{
  "title": "Adopt thread-rich (32-thread) throughput approach instead of single-thread ILP",
  "section_or_page_locator": "page 1 (introduction)",
  "decision": "Design Niagara to optimize for multithreaded throughput in a commercial server environment rather than for single- or dual-thread performance. Build a machine with many hardware threads that hide memory latency, exploiting thread-level parallelism (TLP).",
  "alternatives_or_rejected": "Single-thread/ILP optimization (multiple instruction issue, out-of-order issue, aggressive branch prediction) and machines optimized for single-thread performance. Also rejected: simply running ILP processors at lower clock frequencies to save power.",
  "rationale": "Diminishing returns from single-thread focus because of limits on latency to main memory and inherently low ILP of applications; the ILP approach brought complexity and power concerns. Commercial server workloads are dominated by TLP, so increasing throughput across many threads is effective.",
  "outcome": "Niagara supports 32 hardware threads in hardware; application performance is increased by improving throughput (total work across threads).",
  "direct_quote": "This approach increases application performance by improving throughput, the total amount of work done across multiple threads of execution.",
  "gaps": [
    "The paper does not quantify the measured power or performance difference versus a specific single-thread ILP processor.",
    "It does not state the target clock frequency for the thread-rich design.",
    "It does not give quantitative ILP-vs-TLP performance comparisons, only a qualitative figure and Table 1 (application ILP/TLP categories)."
  ],
  "confidence": 0.95
}
```

**Your review, as a single bare JSON object:**

**Your review, as a single bare JSON object copying this template EXACTLY — every key, every
leading code word, in this order, no extra keys, no renamed keys:**

{"verdict": "<exactly one of: SOUND | SOUND-WITH-RESERVATIONS | SUSPECT | IMPLAUSIBLE-FOR-THIS-PAPER>",
 "objections": [{"claim_attacked": "<field>: <the claim you attack>",
                 "objection": "<why it is wrong or suspect, grounded in mechanism or in what the cited paper plausibly contains>",
                 "severity": "<exactly one of: fatal | major | minor>",
                 "confidence": 0.0}],
 "direction_check": "MATCHES | REVERSAL | TRANSPLANT | N-J — <one sentence: does the decision direction match what this paper is known for, with the recalled evidence>",
 "quote_plausibility": "PAPER-LIKE | PARAPHRASE | FRAGMENT | N-J — <one sentence: does direct_quote read like this paper's prose or like a paraphrase dressed as a quote>",
 "missing_from_story": ["<what a real account of this decision would have to mention>"],
 "most_defensible_part": "<the one element you would keep unchanged>"}

Field rules: **verdict** is exactly one of the four strings, with no other words in that field.
**direction_check** MUST begin with MATCHES, REVERSAL, TRANSPLANT or N-J; **quote_plausibility**
MUST begin with PAPER-LIKE, PARAPHRASE, FRAGMENT or N-J — each followed by " — " and one sentence
of recalled evidence. **severity** is exactly fatal, major or minor. N-J means
"cannot-judge-without-the-paper" and is a valid answer, not a gap.

**Hard rules:** attack the NUMBERS, the causal chain, and the decision DIRECTION, not the writing. If a claim is sound, say so — inventing objections is as bad as missing real ones. You do NOT have the paper in front of you: do not browse the web — the review is blind by design — and every judgment about the paper's contents is RECALLED plausibility — label it as such, never assert it, and write "cannot-judge-without-the-paper" on any field you cannot assess blind (a field-level escape beats a guessed objection). Fewer sharp objections beat a padded list. No invented tool or chip names. This review is a PRE-SCREEN for expert review, not a verdict on the paper — flag, don't convict. **Output: the single bare JSON object and NOTHING else.**

[prompt-version: J-v3.2 2026-09-10 — over J-v3.1: the abstract one-line schema replaced by a literal copy-exact template with field-leading enums (MATCHES/REVERSAL/TRANSPLANT/N-J, PAPER-LIKE/PARAPHRASE/FRAGMENT/N-J) — the same schema-invention risk the J-v1.1 pilot demonstrated, applied pre-dispatch to the paper sheet. Keys and enums match the tally codebook one-to-one.]  [J-v3.1 2026-09-10 — over J-v3: binding first-character output-format contract and explicit no-browsing rule added; schema and fields unchanged.]  [J-v3 2026-09-08 — J-v2's paste slot replaced by a fixed baked-in exemplar so the prompt runs standalone; output schema, hard rules and escape discipline unchanged from J-v2]

---

**BUILD NOTE — not part of the paste. Everything above this rule is the prompt.**

- Exemplar: `extractions/Niagara.episodes.json`, episode index 0. All 9 corpus-schema keys present.
- Quote verified byte-verbatim against `sources/Niagara-pagemarked.txt:27-30`. One deviation from stored bytes: the stored value carries `\r\n` at the source's line-wrap points; these were collapsed to single spaces so `quote_plausibility` judges prose rather than line-wrap artifacts. No words changed.
- Citation authors from standard bibliographic record; the pagemarked text drops the byline. Journal, volume, pages and year match the `_locator_note` in the extraction file.
- Why this exemplar: Niagara is the only paper pool in the corpus whose stored quotes are complete sentences (Alpha 21264, Pentium 4 and POWER4-system quotes are 37-58 character mid-phrase fragments) while still having strong general-model recall (the POWER4 IBM JRD papers have complete quotes but weak recall, so both pre-screen fields would escape).
- Known-sound exemplar. A reviewer returning many fatal objections here is miscalibrated. All 13 panel models already hold PROMPT-O Niagara recall output from 2026-08-31, so each model's `direction_check` can be graded against its own prior recall rather than against an unaided judgment.
- Sibling prompt for GitHub-issue episodes: `J-ISSUE-REDTEAM-V1.md`. Do not paste issue-episode objects into this prompt — they carry a different schema and no recallable paper.
