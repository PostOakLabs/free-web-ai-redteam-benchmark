# The anti-reversal experiment — P vs D2 on the same paper

**The question P exists to answer.** Across 253 graded recall claims (`recall-scorecard.md`), *every*
central-decision inversion in the collection landed on one paper: POWER4 system microarchitecture,
graded as slice D2, which scored **19% contradicted with 3 inversions**. Four later slices carrying an
explicit anti-reversal warning (L, M, N, O) produced **zero inversions across 216 claims**. That was
confounded: the warning changed *and* the paper changed. POWER4's decisions are guiding-principle
prose that smooths into a generic "balanced design" narrative; Alpha's, Pentium 4's and Niagara's are
named mechanisms.

**P holds the paper constant and changes the prompt.** Same paper, same 13 models, prompt-version
`P-v1 2026-08-31 — controlled rerun of D2 with the anti-reversal rule`.

---

## 1. Result

| | **D2** (no warning) | **P** (warning) |
|---|---|---|
| Gradable entries | 37 | 56 |
| CONFIRMED | 62% | **73%** |
| PARTIAL | 14% | 9% |
| NOT-IN-PAPER | 5% | 14% |
| **CONTRADICTED** | **19%** (7) | **3.6%** (2) |
| **Central-decision inversions** | **3** | **0** |

**Verdict, plainly stated: the confound is settled in favour of the prompt.** With the paper held
constant, adding the anti-reversal package eliminated all three inversions and cut the contradiction
rate by a factor of five. POWER4's prose is not what caused the reversals.

**One honest qualification.** P-v1 changed three things at once, not one: it added the anti-reversal
sentence, made `weakest_point` a required field, and added an optional `provenance_note`. The
experiment therefore establishes that **the P-v1 package works**, not that the warning sentence alone
does. The three components are cheap and mutually reinforcing, so there is little reason to isolate
them — but the claim should be stated as the package.

### The inversions that disappeared

All three D2 inversions were on the same decision — POWER4's clock-frequency philosophy, where the
paper says *"IBM opted to also embrace the speed-demon approach"* and three models claimed the
opposite. In P:

| Model | D2 | P |
|---|---|---|
| chatgpt | *"balanced design rather than maximizing clock speed"* — **INVERTED** | *"Commit to very high processor frequency as a primary design objective"* — **CONFIRMED** |
| minimax m2.7 | *"moderate frequency rather than maximum"* — **INVERTED** | did not raise the topic |
| minimax m3 | *"modest clock-frequency target"* — **INVERTED** | did not raise the topic; and its D2 *per-core L2* inversion became **shared L2, CONFIRMED** in P |

Two of the three inverters **stopped making the claim** rather than correcting it — which is what the
prompt asked for (*"if you are not certain of a decision's DIRECTION, either omit the entry or state
the uncertainty"*). minimax m3 dropped from 5 entries to 3. **The warning appears to work partly by
suppressing low-confidence direction claims, not only by fixing them** — a real effect, and one that
costs coverage.

### What the warning did *not* fix

**deepseek reproduced its D2 error set exactly**: directory-based coherence (CONTRADICTED — the paper
is snoop-based, 39 hits for "snoop"), instruction retry (NOT-IN-PAPER, zero hits, deferred to the
Bossen companion), and DVFS/clock gating (NOT-IN-PAPER — *voltage*, *clock gating* and *power
management* have zero hits). Same three claims, same confidence, both runs.

**The one new contradiction is minimax m2.7's**: *"Simultaneous Multithreading: SMT with 2 threads per
core vs. chip-level multiprocessing only."* POWER4 has no SMT — that is POWER5 — and the paper states
the opposite organisation: *"The two processors on the chip are identical and provide a two-way SMP
model to software."* Every *multithread* hit in the paper is in the reference list or an author
biography.

**Conclusion: the anti-reversal rule governs direction errors, not content errors.** Claims that are
true-of-the-chip-but-absent-from-the-paper, and claims imported from a later generation, pass straight
through it. Those need the separate `paper_vs_general` discipline, which remains weak.

---

## 2. `weakest_point` adoption

P made `weakest_point` mandatory for the first time.

| | Count |
|---|---|
| Entries with a populated `weakest_point` | **51 / 56 (91%)** |
| Entries without | 5 — **all five are glm 5.3 flash** |
| Entries with the optional `provenance_note` | 24 (43%) |

**Adoption is essentially total among models that engaged with the prompt**, and the field is
substantive rather than perfunctory. yuanbao's are the best calibrated: it flags that the 174 M
transistor count *"is from the companion circuit-design paper (Warnock et al.), not exclusively from
this system microarchitecture paper"* — which is exactly right and which this digest independently
established two passes ago; and it hedges the *"speed-demon vs brainiac"* framing as possibly IBM's
later summary language rather than the paper's, when in fact the paper does use it.

Given `weakest_point` is the one honesty field that has repeatedly predicted what independent review
attacks (`episode-draft-bank.md` §4), 91% adoption on first request is a strong result and argues for
making it mandatory in every prompt that asks for a factual claim.

---

## 3. glm 5.3 flash ran despite suspension — and it is the same file again

`recall-scorecard.md` suspended glm 5.3 flash after it submitted the identical five **Alpha 21264**
entries for M (Pentium 4), N (POWER4 circuit/physical) and O (Niagara). It ran again for P, and
**submitted the same five Alpha entries a fourth time** — "departure from the 21164", two integer
clusters, 80 integer / 72 FP registers, off-chip L2, local+global+chooser predictor. Counting its S
and T files (below), the same content has now been submitted **seven times across seven different
prompts**, including two that ask for formulas and test vectors rather than paper recall.

**On the flagged "L2-topology inversion candidate."** Entry P19 reads *"Large on-chip L1 caches with
the second-level cache moved off-chip."* Read as a POWER4 claim that is an inversion — POWER4's L2 is
**on-chip** (unified, three autonomous controllers, via the CIU crossbar) and it is the **L3** whose
data arrays are off-chip with an on-chip controller and directory.

**But the wrong-paper check comes first, and it changes the grade.** The statement is not a POWER4
claim at all: it is an accurate Alpha 21264 statement, and the 21264 genuinely has large on-chip L1s
with an off-chip L2. **Graded NOT-IN-PAPER (wrong paper), not CONTRADICTED.** Scoring it as an
inversion would misattribute a delivery failure to a reasoning failure — and would have corrupted the
headline result of this experiment, since one spurious inversion in P would have muddied the 3 → 0
finding.

**All five glm entries are graded NOT-IN-PAPER on the same basis**, and its 0/5 on `weakest_point` is
consistent with the file predating the P prompt entirely.

**Recommendation unchanged and now urgent:** suspend glm 5.3 flash from all slices until the cause is
identified, and add the target-paper keyword pre-check before grading. Its P file scores near zero
against POWER4 vocabulary and near maximum against Alpha.

---

## 4. Per-model P results

| Model | Entries | CONF | PART | NIP | CONTRA | Inversions | Note |
|---|---|---|---|---|---|---|---|
| chatgpt | 5 | 5 | — | — | — | **0** | corrected its D2 inversion |
| gemini | 4 | 4 | — | — | — | 0 | |
| grok | 5 | 5 | — | — | — | 0 | |
| meta | 5 | 5 | — | — | — | 0 | *three autonomous L2 controllers* and the branch-prediction rationale, both verbatim |
| sonnet | 5 | 5 | — | — | — | 0 | **all five map onto extraction episodes** — binary compat, group tracking, 2-read/1-write, single-ported I-cache, T/Trem |
| yuanbao | 5 | 5 | — | — | — | 0 | best-calibrated `weakest_point` fields in the slice |
| kimi | 5 | 4 | 1 | — | — | 0 | retry again (PARTIAL) |
| qwen | 4 | 3 | 1 | — | — | 0 | "thermal control" — zero hits |
| minimax m3 | 3 | 1 | 1 | 1 | — | **0** | reduced coverage; corrected its L2 inversion |
| minimax m2.7 | 5 | 3 | 1 | — | **1** | 0 | SMT — a *fabricated* decision, not a reversed one |
| deepseek | 5 | 1 | 1 | 2 | **1** | 0 | identical error set to D2 |
| glm 5.3 flash | 5 | — | — | **5** | — | n/a | wrong paper, 4th time |
| mimo | prose | — | — | — | — | — | 12th refusal |

---

## 5. What to do with this

1. **Back-port the P-v1 package to every prompt that asks for a factual claim** — anti-reversal
   sentence, mandatory `weakest_point`, optional `provenance_note`. Evidence: 3 → 0 inversions on the
   same paper, 91% adoption of the new field on first request, and a schema that now accommodates the
   nuanced provenance yuanbao was already straining to express.
2. **Do not expect it to fix content errors.** deepseek's three wrong claims survived unchanged. A
   separate mechanism is needed for true-of-the-chip-but-not-in-this-paper, and the only one that has
   worked so far is grading against the extracted text.
3. **Add the target-paper keyword pre-check.** It is the only thing that catches the glm class, it
   costs a few lines, and without it a delivery failure gets scored as a reasoning failure.
4. **Note the coverage cost.** Two of three inverters answered less rather than better. If breadth
   matters more than direction-safety for some future slice, that trade should be made knowingly.
