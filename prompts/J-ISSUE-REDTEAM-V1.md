**OUTPUT FORMAT (binding, read first):** your entire response must be exactly one JSON object
matching the schema at the end of this brief. The first character of your reply must be `{` and the
last must be `}`. No markdown, no headings, no commentary before or after, no code fences, no
explanations — the JSON object only.

You are a skeptical principal engineer reviewing a DRAFT incident episode before it enters a curated dataset. The episode was mined from a public bug-tracker thread. Your job is to attack it: find every technical claim that is wrong, implausible, or internally inconsistent — and say what a correct version would look like.

Unlike a paper episode, you need no outside knowledge here. The record pasted below IS the evidence base. Judge it on its own contents.

**The draft under review:**

RECORD: OpenROAD issue #6066, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "title": "BoomTile/Megaboom: 20k routing congestion DRCs at only 0.24 placement density",
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6066",
  "prior_state": "BoomTile (Megaboom-derived) design in asap7, ORFS v3.0-1735-gdefc349e. Placement density was only 0.24 with a lot of open space, especially at the top of the die, yet the design failed GRT.",
  "observation": "20k routing congestion DRCs while placement density is only 0.24. Congestion heatmap shows a large region at the top of the die and around the macro. Reported via `run-me-BoomTile-asap7-base.sh gui`.",
  "hypothesis": "The GRT routing-layer adjustment of 0.45 (originally derived from other asap7 designs) is too aggressive for this design; the default 30 congestion iterations were also insufficient. A separate suspected cause named in the thread is a global-route path 'looping around the macro' many times (tracked separately in issue #5971).",
  "candidates_considered": "Increasing the number of overflow/congestion iterations (asked early on and swept, default 30); changing the routing layer adjustment from 0.45 to 0.2; increasing congestion iteration count to 35; macro-placement improvements (issue #5971).",
  "chosen_intervention": "Per eder-matheus (MEMBER): 'we could finish GRT by changing the routing layer adjustments from 0.45 to 0.2... We also changed the number of congestion iterations to 35 to complete BoomTile.'",
  "post_state": "GRT was reported to complete ('could finish GRT', 'complete BoomTile') after reducing the layer adjustment to 0.2 and setting congestion iterations to 35. No re-measured DRC count was given.",
  "gaps": [
    "No measured post-fix DRC count or runtime is reported.",
    "The issue was closed automatically as not_planned/Stale in 2026; whether the reported parameter change was actually merged as a code change is not stated.",
    "No PR link for the fix. The macro-loop root cause is deferred to #5971 and was not resolved here.",
    "We (eder-matheus) note the layer-adjustment is documented at set-global-routing-layer-adjustment; exact meaning of a high vs low value only explained in prose."
  ],
  "confidence": 0.8,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6066",
  "source_type": "github-issue",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6066",
  "direct_quote": {
    "text": "we could finish GRT by changing the routing layer adjustments from 0.45 to 0.2.",
    "by": "eder-matheus",
    "date": "2024-11-14",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6066"
  }
}
```

**Your review, as a single bare JSON object copying this template EXACTLY — every key, every
leading code word, in this order, no extra keys, no renamed keys:**

{"verdict": "<exactly one of: SOUND | SOUND-WITH-RESERVATIONS | SUSPECT | IMPLAUSIBLE-FOR-THIS-RECORD>",
 "objections": [{"claim_attacked": "<field>: <the claim you attack>",
                 "objection": "<why it is wrong or suspect, grounded in the record's mechanism>",
                 "severity": "<exactly one of: fatal | major | minor>",
                 "confidence": 0.0}],
 "mechanism_check": "HOLDS | BREAKS | N-D — <one sentence: does chosen_intervention plausibly produce post_state given observation and hypothesis?>",
 "evidence_check": "MEAS | ASSERT | N-D — <one sentence: is post_state measured or merely asserted?>",
 "attribution_check": "SUPPORTS | WEAK | ABSENT | N-D — <one sentence: does direct_quote carry a named participant, a date and a locator, and support the claim chosen_intervention attaches to it?>",
 "missing_from_story": ["<what a real account of this incident would have to mention>"],
 "most_defensible_part": "<the one element you would keep unchanged>"}

Field rules: **verdict** is exactly one of the four strings, with no other words in that field.
**mechanism_check** MUST begin with HOLDS, BREAKS or N-D; **evidence_check** MUST begin with MEAS,
ASSERT or N-D; **attribution_check** MUST begin with SUPPORTS, WEAK, ABSENT or N-D — each followed
by " — " and one sentence of reasoning. **severity** is exactly fatal, major or minor. N-D means
"not determinable from this record" and is a valid answer, not a gap.

**Hard rules:** attack the NUMBERS, the causal chain, and whether the intervention explains the outcome — not the writing. The pasted record is the WHOLE evidence base: do not browse the web or fetch any page — the review requires none, and any externally fetched material invalidates the review — and do not invent thread content, commits, PRs, participants, or tool behaviour that is not in it, and do not fault the episode for omitting something the thread itself never contained (that belongs in `missing_from_story`, not in an objection). If the record does not settle a question, write "not-determinable-from-this-record" for that field rather than guessing — a field-level escape beats a guessed objection. A claimed resolution with no measured post-state is an EVIDENCE defect, not a mechanism defect; classify it under `evidence_check` and do not double-count it as a fatal objection. If a claim is sound, say so — inventing objections is as bad as missing real ones. Fewer sharp objections beat a padded list. No invented tool or chip names. This review is a PRE-SCREEN for expert review, not a verdict on the underlying bug — flag, don't convict. **Output: the single bare JSON object and NOTHING else.**

[prompt-version: JI-v1.2 2026-09-10 — over JI-v1.1: the abstract one-line schema replaced by a literal copy-exact template with field-leading enums (HOLDS/BREAKS/N-D, MEAS/ASSERT/N-D, SUPPORTS/WEAK/ABSENT/N-D) after the v1.1 pilot returned 0/15 schema compliance — every model invented its own verdict vocabulary. Keys and enums match the tally codebook one-to-one.]  [JI-v1.1 2026-09-10 — over JI-v1: binding first-character output-format contract added after the block-01 wave returned prose reviews from most models despite the NOTHING-else rule; explicit no-browsing rule added after one model fetched the live GitHub page. Schema, fields and blocks unchanged.]  [JI-v1 2026-09-08 — issue-episode red-team; J-v1's no-external-source frame retained, J-v2's verdict enum and pre-screen discipline carried over, paper-recall fields (direction_check, quote_plausibility) replaced by mechanism_check / evidence_check / attribution_check]

---

**BUILD NOTE — not part of the paste. Everything above this rule is the prompt.**

- Exemplar: `extractions/issue-episodes.json`, the BoomTile object, rendered verbatim (byte-checked against the extraction file; identical to RUNSHEET-34 Block 01). No normalization applied, including the garbled "We (eder-matheus) note..." clause in `gaps`, which is preserved as stored.
- Why this prompt exists: `J-EPISODE-REDTEAM-V2.md` cannot review these objects. All 34 blocks in `redteam/RUNSHEET-34.md` lack `decision`, `alternatives_or_rejected`, `rationale` and `outcome` (3 also lack `section_or_page_locator` and `direct_quote`), and their `PAPER:` line is a GitHub issue URL. J-v2 asks the reviewer to attack the decision DIRECTION and to judge quote prose against a recalled paper — with no `decision` key and no recallable source, `direction_check` and `quote_plausibility` collapse to the prompt's own `cannot-judge-without-the-paper` escape on every block. J-v2's schema was verified against the five paper-episode files only; the issue-episode files were never checked against it.
- Field substitution rationale: a bug-tracker thread is short enough that the episode object substantially IS the record, so recall-dependent pre-screens are the wrong instrument. `mechanism_check` tests the causal chain the reviewer can see; `evidence_check` targets the dominant failure mode in this set (resolution asserted without measurement — Block 01 gives no post-fix DRC count, Block 02 resolves as "solved on the latest version" with no commit, PR or root cause); `attribution_check` is stronger here than paper quote-plausibility because these episodes carry `{text, by, date, locator}` and the claim is checkable in-paste.
- Known-imperfect exemplar. A competent reviewer should land on the unmeasured `post_state` under `evidence_check` and on the unresolved macro-loop cause deferred to #5971. A reviewer returning bare SOUND with no objections is miscalibrated.
- Sibling prompt for published-paper episodes: `J-EPISODE-REDTEAM-V3.md`.
