# TALLY-34 — red-team verdicts against `prompts/J-ISSUE-REDTEAM-V1.md`

Re-rendered 2026-09-08 alongside `RUNSHEET-34.md`. The previous version's columns were built for
`J-EPISODE-REDTEAM-V2.md`, whose `direction_check` / `quote_plausibility` fields do not exist in
JI-v1 output and were unanswerable on these records anyway (see
`SESSION-MEMORIAL-2026-09-08-REDTEAM.md` §1).

**One copy of the block table per model run.** Fill from the model's returned JSON object; every
column below maps to exactly one key in it. `Fatal` / `Major` are counts of `objections[].severity`.

## Column coding

JI-v1's three checks are free-text in the JSON. Code them here so the sheet is sortable, and keep
the model's own sentence in `Note` when it is doing real work.

| Column | From JSON key | Codes |
|---|---|---|
| `Verdict` | `verdict` | `SOUND` · `S-W-RES` (SOUND-WITH-RESERVATIONS) · `SUSPECT` · `IMPLAUS` (IMPLAUSIBLE-FOR-THIS-RECORD) |
| `Fatal` / `Major` | count of `objections[].severity` | integer |
| `Mech` | `mechanism_check` | `HOLDS` (causal chain closes) · `BREAKS` (states where it breaks) · `N-D` (not-determinable-from-this-record) |
| `Evid` | `evidence_check` | `MEAS` (post_state measured) · `ASSERT` (claimed, unmeasured) · `N-D` |
| `Attr` | `attribution_check` | `SUPPORTS` (named + dated + locator, and supports the claim) · `WEAK` (present but does not carry the claim) · `ABSENT` (no quote in the record) · `N-D` |

`N-D` is a **pass**, not a gap: JI-v1 instructs a field-level escape over a guessed objection.

**Expected on blocks 04, 05 and 06:** `Attr = ABSENT`. Those three records carry no `direct_quote`
and no `section_or_page_locator`. A model that reports `SUPPORTS` there has invented a quote — treat
that as a disqualifying result for the whole run, not as one bad row.

**Block 01 is a calibration check, not evidence.** It is the exemplar baked into JI-v1 itself, and
the prompt's BUILD NOTE states what a competent review finds: the unmeasured `post_state`
(`Evid = ASSERT`) and the macro-loop cause deferred to #5971. A model returning bare `SOUND` with
zero objections on Block 01 is miscalibrated; read its other 33 verdicts in that light and record it
in the per-model summary.

---

## Block table — model: ________________  date: __________

| # | Title | Verdict | Fatal | Major | Mech | Evid | Attr | Note |
|---|---|---|---|---|---|---|---|---|
| 01 | BoomTile/Megaboom: 20k routing congestion DRCs at only 0.24 p… |  |  |  |  |  |  |
| 02 | GPL-0314: getFillerGCell index out of bounds during global pl… |  |  |  |  |  |  |
| 03 | RUDY and global-route congestion maps disagree for ICCAD04 ri… |  |  |  |  |  |  |
| 04 | GRT DRC-error cap (10000) hides congestion hotspots and macro… |  |  |  |  |  |  |
| 05 | repair_timing ODB-1200 with Liberty flip-flops defining Q→QN… |  |  |  |  |  |  |
| 06 | TritonCTS segfault in getBufferFanoutLimit when Liberty has n… |  |  |  |  |  |  |
| 07 | CTS NDRs on heavily gated clocks cause routing congestion (le… |  |  |  |  |  |  |
| 08 | asap7 cva6 hierarchical-synth GRT congestion report reference… |  |  |  |  |  |  |
| 09 | STA: false hold/setup violations in floorplan from ideal top-… |  |  |  |  |  |  |
| 10 | GPL regression: too-early non-virtual timing-driven iteration… |  |  |  |  |  |  |
| 11 | GPL: RePlAce divergence (GPL-0307) on megaboom — snapshot-del… |  |  |  |  |  |  |
| 12 | Manual macro placement (R90, asap7 M2) leaves pins off routin… |  |  |  |  |  |  |
| 13 | DRT assert in patchMetalShape_minStep: violation on last meta… |  |  |  |  |  |  |
| 14 | GRT heap underflow (GRT-0183) after antenna repair — FastRout… |  |  |  |  |  |  |
| 15 | PDN: negative placement halo mis-applied to obstructions/pins… |  |  |  |  |  |  |
| 16 | CTS crash (stack overflow in computeSinkArrivalRecur) after c… |  |  |  |  |  |  |
| 17 | CTS design decision: balance macro insertion latency against… |  |  |  |  |  |  |
| 18 | PDN legality decision: rings outside the die area become an e… |  |  |  |  |  |  |
| 19 | repair_timing non-determinism with threads>1: stale driver-ve… |  |  |  |  |  |  |
| 20 | eqy formal check exposes silent netlist corruption: RSZ journ… |  |  |  |  |  |  |
| 21 | DRT runtime regression on ispd19_test6: misaligned GCELLGRID… |  |  |  |  |  |  |
| 22 | DRT 4-hour pause after '100%': one 235k-pin unclocked net thr… |  |  |  |  |  |  |
| 23 | DRT DRC decision: pin access 'not so close to the cell edge'… |  |  |  |  |  |  |
| 24 | MegaBoom repair_timing spends 40000s repairing 1 endpoint and… |  |  |  |  |  |  |
| 25 | GPL divergence with 0 HPWL: division-by-zero in gradient when… |  |  |  |  |  |  |
| 26 | DPL creates unroutable placement for centered (non-origin) fl… |  |  |  |  |  |  |
| 27 | GRT-attributed ODB non-determinism actually originates in pin… |  |  |  |  |  |  |
| 28 | FlexGC-vs-KLayout signoff disagreement near SRAM macro pins r… |  |  |  |  |  |  |
| 29 | GRT guides over a single-layer planar region: DRT abandons gu… |  |  |  |  |  |  |
| 30 | repairDesign core dump when buffering a net from an IO-pad co… |  |  |  |  |  |  |
| 31 | CTS signal-6 lockup "once in a blue moon" — closed unreproduc… |  |  |  |  |  |  |
| 32 | RSZ-2008 "wire step options empty" in timing-driven placement… |  |  |  |  |  |  |
| 33 | LibreLane PDN-0179 "Unable to repair all channels" with SRAM… |  |  |  |  |  |  |
| 34 | LVS fails on nets with >2 pins: magic extraction drops them a… |  |  |  |  |  |  |

## Per-model summary (one row per model run)

| Model | Date | SOUND | S-W-RES | SUSPECT | IMPLAUS | Blk01 calibration | Attr invented on 04/05/06 | Survivors first |
|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  | pass / miscalibrated | yes / no |  |

`Survivors first` = the block numbers this model left standing with no fatal objection, in the order
you would send them to expert review.

## Cross-model rollup (fill once several models are in)

| # | Runs | Worst verdict | Fatal count across models | Consensus defect | Ready for expert review? |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

A block only reaches expert review when no model returned a fatal objection on it. A block that
several models mark `Evid = ASSERT` is not thereby disqualified — under JI-v1 an unmeasured
resolution is an evidence defect and is explicitly **not** counted as a fatal objection.

<!-- D5-CALIBRATION-BEGIN -->

## Calibration wave - Block 01, all 16 Day-5 models (generated by `digest/_verify/d5tally.py`, do not hand-edit)

Source: `Web Model Tasks/Day 5/* red1.json`. RUNSHEET-34 Block 01 (BoomTile) - J-v1's own exemplar, declared known-IMPERFECT.

**This wave measures reviewer calibration, not corpus quality** - every model
reviewed the block that is baked into the prompt itself. `direction_check` is out
of scope on a single-block wave and is deliberately absent rather than blank.

| model | verdict | obj | fatal | major | minor | calibration | parse |
|---|---|---|---|---|---|---|---|
| chatgpt | S-W-RES | 4 | 0 | 2 | 2 | consistent | structural-quote-repair |
| deepseek | S-W-RES | 3 | 0 | 1 | 2 | consistent | clean |
| gemini | S-W-RES | 1 | 0 | 0 | 1 | consistent | clean+fence-close+fenced |
| glm 5.3 flash | S-W-RES | 3 | 0 | 1 | 2 | consistent | clean |
| grok | S-W-RES | 2 | 0 | 1 | 1 | consistent | clean |
| kimi | S-W-RES | 3 | 0 | 3 | 0 | consistent | clean |
| meta | S-W-RES | 1 | 0 | 0 | 1 | consistent | clean |
| mimo | S-W-RES | 4 | 0 | 1 | 3 | consistent | clean+fence-close+fenced |
| minara | S-W-RES | 1 | 0 | 0 | 1 | consistent | clean |
| minimax 2.7 | S-W-RES | 0 | 0 | 0 | 0 | SCHEMA-ANOMALY-reservations-without-objections | clean |
| mistral | S-W-RES | 2 | 0 | 1 | 1 | consistent | clean+fence-close+fenced |
| qwen | S-W-RES | 1 | 0 | 0 | 1 | consistent | clean |
| solar | S-W-RES | 3 | 0 | 1 | 2 | consistent | clean |
| sonnet | S-W-RES | 3 | 0 | 0 | 3 | consistent | clean |
| yuanbao | S-W-RES | 6 | 0 | 4 | 2 | consistent | clean |
| longcat | SUSPECT | 2 | 0 | 1 | 1 | consistent | clean |

- **bare-SOUND (0)**: none. The prompt's own BUILD NOTE declares this block known-imperfect, so a SOUND verdict carrying zero objections is miscalibrated by the prompt's definition, not by this digest's opinion.
- **schema anomalies (1)**: minimax 2.7 (objections) — a verdict inconsistent with the model's own objection list.

<!-- D5-CALIBRATION-END -->
