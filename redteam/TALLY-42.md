# TALLY-42 — red-team verdicts against `prompts/J-EPISODE-REDTEAM-V3.md`

Companion to `RUNSHEET-42.md` (42 blocks). One copy of the block table per model run. Every column
maps to exactly one key in J-v3's returned JSON object.

## Column coding

| Column | From JSON key | Codes |
|---|---|---|
| `Verdict` | `verdict` | `SOUND` · `S-W-RES` (SOUND-WITH-RESERVATIONS) · `SUSPECT` · `IMPLAUS` (IMPLAUSIBLE-FOR-THIS-PAPER) |
| `Fatal` / `Major` | count of `objections[].severity` | integer |
| `Dir` | `direction_check` | `MATCHES` · `REVERSAL` · `TRANSPLANT` (reads as general knowledge, not this paper) · `N-J` (cannot-judge-without-the-paper) |
| `Quote` | `quote_plausibility` | `PAPER-LIKE` · `PARAPHRASE` (dressed as a quote) · `FRAGMENT` (mid-phrase, judgment withheld) · `N-J` |

`N-J` is a **pass**, not a gap: J-v3 instructs a field-level escape over a guessed objection, and
states plainly that the reviewer does not have the paper. Scoring `N-J` as a miss pushes models back
toward guessing, which is the behaviour the prompt suppresses.

**`REVERSAL` is the headline signal.** J-v3's parent prompt family calls a reversed decision
direction the single worst possible output. Any `Dir = REVERSAL` should be escalated to source
before anything else in the run is read.

**Expect `Quote = FRAGMENT` on blocks 01–07, 14–20, 35–42.** Those pools store 37–58-character
mid-phrase quotes. That is an extraction property, not a fabrication signal — a model reporting
`PARAPHRASE` across a whole pool is describing the extraction method, not a defect.

**Block 8 is a calibration check, not evidence** — it is J-v3's own exemplar, declared
known-sound. Bare `SOUND` there is expected; many fatal objections there means miscalibrated.

---

## Block table — model: ________________  date: __________

| # | Paper | Title | Verdict | Fatal | Major | Dir | Quote | Note |
|---|---|---|---|---|---|---|---|---|
| 01 | Alpha 21264 | Tournament branch predictor combining local and globa… |  |  |  |  |  |  |
| 02 | Alpha 21264 | Register file clustering (split integer register file… |  |  |  |  |  |  |
| 03 | Alpha 21264 | Double-pumped data cache to provide two memory ports |  |  |  |  |  |  |
| 04 | Alpha 21264 | Dynamic store/load ordering adaptation using a load-w… |  |  |  |  |  |  |
| 05 | Alpha 21264 | Minirestart instead of full pipeline restart for load… |  |  |  |  |  |  |
| 06 | Alpha 21264 | Splitting conditional-move instructions to fit the tw… |  |  |  |  |  |  |
| 07 | Alpha 21264 | Line-and-way prediction for fast set-associative inst… |  |  |  |  |  |  |
| 08 | Niagara | Adopt thread-rich (32-thread) throughput approach ins… |  |  |  |  |  |  |
| 09 | Niagara | Group threads into a shared SPARC pipe (4 threads per… |  |  |  |  |  |  |
| 10 | Niagara | Use a shared on-chip crossbar and shared L2 cache ins… |  |  |  |  |  |  |
| 11 | Niagara | Provide a 3-Mbyte, 4-way banked, pipelined, 12-way se… |  |  |  |  |  |  |
| 12 | Niagara | Integrate four on-chip memory controllers for high me… |  |  |  |  |  |  |
| 13 | Niagara | Target low power/area (~60 W) by exploiting TLP inste… |  |  |  |  |  |  |
| 14 | Pentium 4 | Execution Trace Cache as L1 instruction cache instead… |  |  |  |  |  |  |
| 15 | Pentium 4 | Choosing a deeper pipeline to chase a high target fre… |  |  |  |  |  |  |
| 16 | Pentium 4 | Double-pumped low-latency integer ALU while pushing r… |  |  |  |  |  |  |
| 17 | Pentium 4 | Small low-latency L1 data cache backed by a large med… |  |  |  |  |  |  |
| 18 | Pentium 4 | Second FP/SSE port chosen for cost/performance over a… |  |  |  |  |  |  |
| 19 | Pentium 4 | Separate ROB and register-file allocation instead of… |  |  |  |  |  |  |
| 20 | Pentium 4 | Quad-pumped 400MHz source-synchronous system bus for… |  |  |  |  |  |  |
| 21 | POWER4 circuit/physical | Predominantly static-circuit design with sparing use… |  |  |  |  |  |  |
| 22 | POWER4 circuit/physical | Single chip-wide global clock domain with no skew fee… |  |  |  |  |  |  |
| 23 | POWER4 circuit/physical | Transistor-level timing of custom macros rather than… |  |  |  |  |  |  |
| 24 | POWER4 circuit/physical | Fourteen-wiring-track power grid image with more powe… |  |  |  |  |  |  |
| 25 | POWER4 circuit/physical | Selective use of low-threshold-voltage (low-Vt) devic… |  |  |  |  |  |  |
| 26 | POWER4 circuit/physical | Split (transparent master/slave) latch scheme for cri… |  |  |  |  |  |  |
| 27 | POWER4 circuit/physical | Tunable sector trees driving a single full-chip clock… |  |  |  |  |  |  |
| 28 | POWER4 circuit/physical | Custom design for dataflow macros and logic synthesis… |  |  |  |  |  |  |
| 29 | POWER4 system (d2true pool) | Pervasive RAS: transform checkstops into synchronous… |  |  |  |  |  |  |
| 30 | POWER4 system (d2true pool) | Full-system co-design: design processor, memory, I/O… |  |  |  |  |  |  |
| 31 | POWER4 system (d2true pool) | SMP-throughput optimization as the organizing princip… |  |  |  |  |  |  |
| 32 | POWER4 system (d2true pool) | Absolute binary-compatibility requirement after task… |  |  |  |  |  |  |
| 33 | POWER4 system (d2true pool) | Distributed-switch interconnect for chip-to-system SM… |  |  |  |  |  |  |
| 34 | POWER4 system (d2true pool) | Large shared on-chip L2 (about 1.5 MB, eight-way) ser… |  |  |  |  |  |  |
| 35 | POWER4 system | Embrace the speed-demon (high-frequency) design path |  |  |  |  |  |  |
| 36 | POWER4 system | Maintain binary compatibility with prior PowerPC syst… |  |  |  |  |  |  |
| 37 | POWER4 system | Single-port I-cache to save area rather than multi-po… |  |  |  |  |  |  |
| 38 | POWER4 system | Track machine state at group boundaries, not per-inst… |  |  |  |  |  |  |
| 39 | POWER4 system | Limit each instruction to two read registers and one… |  |  |  |  |  |  |
| 40 | POWER4 system | L3 sources S-state data only to its own L2s to cut cr… |  |  |  |  |  |  |
| 41 | POWER4 system | Classify cached data as T vs. Trem to skip memory add… |  |  |  |  |  |  |
| 42 | POWER4 system | Prefetch the fifth cache line instead of the second i… |  |  |  |  |  |  |

## Per-model summary (one row per model run)

| Model | Date | SOUND | S-W-RES | SUSPECT | IMPLAUS | Blk 8 calibration | REVERSAL blocks | Survivors first |
|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  | pass / miscalibrated |  |  |

`Survivors first` = blocks left standing with no fatal objection, in the order you would send them
to expert review.

## Cross-model rollup

| # | Runs | Worst verdict | Fatal across models | Consensus defect | Ready for expert review? |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

Two consistency checks this pool supports for free:

1. **Blocks 32 and 36 are the same decision** (POWER4 binary compatibility) extracted into two
   files. Verdicts should be compatible; divergence is a finding.
2. **`direction_check` vs the model's own prior recall.** Every panel model answered PROMPT-L/M/N/O/P
   (Day 1) and the D2-* recall prompts (Day 4) on these same five papers. A model whose
   `direction_check` here contradicts its own earlier recall is the sharpest available signal.

<!-- D5-CALIBRATION-BEGIN -->

## Calibration wave - Block 08, all 16 Day-5 models (generated by `digest/_verify/d5tally.py`, do not hand-edit)

Source: `Web Model Tasks/Day 5/* red3.json`. RUNSHEET-42 Block 08 (Niagara) - J-v3's own exemplar, declared known-SOUND.

**This wave measures reviewer calibration, not corpus quality** - every model
reviewed the block that is baked into the prompt itself. `direction_check` is out
of scope on a single-block wave and is deliberately absent rather than blank.

| model | verdict | obj | fatal | major | minor | calibration | parse |
|---|---|---|---|---|---|---|---|
| chatgpt | S-W-RES | 7 | 0 | 1 | 5 | consistent | structural-quote-repair |
| deepseek | S-W-RES | 3 | 0 | 0 | 3 | consistent | clean |
| glm 5.3 flash | S-W-RES | 3 | 0 | 1 | 2 | consistent | clean |
| kimi | S-W-RES | 4 | 0 | 1 | 3 | consistent | clean |
| mimo | S-W-RES | 4 | 0 | 1 | 3 | consistent | clean+fence-close+fenced |
| minara | S-W-RES | 1 | 0 | 1 | 0 | consistent | clean |
| mistral | S-W-RES | 3 | 0 | 1 | 2 | consistent | clean+fence-close+fenced |
| sonnet | S-W-RES | 3 | 0 | 1 | 2 | consistent | clean |
| yuanbao | S-W-RES | 4 | 0 | 1 | 3 | consistent | clean |
| gemini | SOUND | 0 | 0 | 0 | 0 | **MISCALIBRATED (bare SOUND)** | clean+fence-close+fenced |
| grok | SOUND | 0 | 0 | 0 | 0 | **MISCALIBRATED (bare SOUND)** | clean |
| longcat | SOUND | 2 | 0 | 0 | 2 | SCHEMA-ANOMALY-SOUND-with-objections | clean+fence-close+fenced |
| meta | SOUND | 0 | 0 | 0 | 0 | **MISCALIBRATED (bare SOUND)** | clean |
| minimax 2.7 | SOUND | 0 | 0 | 0 | 0 | **MISCALIBRATED (bare SOUND)** | clean |
| qwen | SOUND | 0 | 0 | 0 | 0 | **MISCALIBRATED (bare SOUND)** | clean |
| solar | NOT GRADABLE | — | — | — | — | parse failure | elementwise-truncation |

- **bare-SOUND (5)**: gemini, grok, meta, minimax 2.7, qwen. The prompt's own BUILD NOTE declares this block known-sound-with-known-gaps, so a SOUND verdict carrying zero objections is miscalibrated by the prompt's definition, not by this digest's opinion.
- **schema anomalies (1)**: longcat (objections) — a verdict inconsistent with the model's own objection list.

<!-- D5-CALIBRATION-END -->
