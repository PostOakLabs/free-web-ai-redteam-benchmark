# Model Scorecard — recall (309 claims, 6 slices) + arithmetic (S/T) + Class-1 computation (Day 2: ~250 + ~470 computations)

**What this is.** All six paper-recall slices (D2 · L · M · N · O · **P**) adjudicated against the five
locator-cited extraction sets in `../extractions/` and against the full text of the five PDFs in
`../sources/`. This is the only place in the collection where model output is scored against
**ground truth** rather than against other models.

**The five papers**

| Slice | Paper | Entries | Extraction |
|---|---|---|---|
| **D2** | Tendler et al., *POWER4 system microarchitecture*, IBM JRD 46(1):5–25, 2002 | 37 | 8 episodes |
| **L** | Kessler, *The Alpha 21264 Microprocessor*, IEEE Micro 19(2):24–36, 1999 | 57 | 7 episodes |
| **M** | Hinton et al., *The Microarchitecture of the Pentium 4 Processor*, Intel Tech. Journal Q1 2001 | 52 | 7 episodes |
| **N** | Warnock et al., *The circuit and physical design of the POWER4 microprocessor*, IBM JRD 46(1):27–52, 2002 | 48 | 8 episodes |
| **O** | Kongetira, Aingaran & Olukotun, *Niagara: A 32-Way Multithreaded SPARC Processor*, IEEE Micro 25(2):21–29, 2005 | 59 | 6 episodes |
| **P** | *POWER4 system microarchitecture* again — **controlled rerun of D2 with the anti-reversal rule** | 56 | same 8 episodes |

**Grades.** CONFIRMED (paper states it, direction right) · PARTIAL (decision right, stated rationale
or detail absent) · NOT-IN-PAPER (paper silent — may be true of the chip, not from this source) ·
**CONTRADICTED** (paper states the opposite — *the failure mode all five prompts name as worst*).

**Two caveats, stated once.** (1) M and N were graded by keyword-anchored spot-check rather than
claim-by-claim, so their PARTIAL/NOT-IN-PAPER counts are lower bounds and their CONFIRMED counts are
sound. (2) The extractions are 6–8-episode *samples*, not indexes; grading is against the papers, with
the extractions as corroboration where topics overlap.

---

## 1. Per-slice results

| Slice | Entries | CONFIRMED | PARTIAL | NOT-IN-PAPER | CONTRADICTED | Inversions |
|---|---|---|---|---|---|---|
| **D2** POWER4 micro | 37 | 62% | 14% | 5% | **19%** | **3** |
| **L** Alpha 21264 | 57 | 72% | 16% | 7% | 5% | 0 |
| **M** Pentium 4 | 52 | 81% | 10% | 10% | 0% | 0 |
| **N** POWER4 phys | 48 | 75% | 8% | 17% | 0% | 0 |
| **O** Niagara | 59 | 80% | 3% | 17% | 0% | 0 |
| **P** POWER4 micro *(rerun)* | 56 | **73%** | 9% | 14% | **3.6%** | **0** |
| **All six** | **309** | **74%** | **10%** | **12%** | **4%** | **3** |

**Every inversion in the collection is on one slice, and P settled why.** D2 carried all three
central-decision reversals. **P re-ran the same paper with the same models under the anti-reversal
rule and produced zero**, cutting contradictions from 19% to 3.6%. The paper was held constant, so
the confound is resolved in favour of the prompt — full analysis in `anti-reversal-experiment.md`.

Qualification: P-v1 changed three things together (the anti-reversal sentence, mandatory
`weakest_point`, optional `provenance_note`), so what is established is that **the package works**,
not the sentence alone.

---

## 2. Per-model scorecard

Sorted by confirmed rate. "Inv." = central-decision inversions. Coverage varies because several
models skipped slices or produced fewer than five entries.

| Model | Entries | CONFIRMED | Conf. rate | PART | NIP | **CONTRA** | **Inv.** | Slices |
|---|---|---|---|---|---|---|---|---|
| **meta** | 25 | 25 | **100%** | 0 | 0 | 0 | **0** | all 5 |
| **qwen** | 14 | 14 | **100%** | 0 | 0 | 0 | **0** | L M N O |
| **sonnet** | 12 | 12 | **100%** | 0 | 0 | 0 | **0** | L M N O |
| **grok** | 25 | 23 | 92% | 1 | 1 | 0 | **0** | all 5 |
| **chatgpt** | 25 | 23 | 92% | 0 | 1 | 1 | **1** | all 5 |
| **yuanbao** | 24 | 22 | 92% | 1 | 0 | 1 | **1** | all 5 |
| **gemini** | 16 | 14 | 88% | 1 | 1 | 0 | **0** | L M N O |
| **kimi** | 19 | 15 | 79% | 2 | 1 | 1 | **1** | L M N O |
| **deepseek** | 25 | 20 | 80% | 2 | 2 | 1 | **1** | all 5 |
| **mimo** *(prose)* | 8 | 5 | 63% | 1 | 1 | 1 | **1** | D2 L only |
| **minimax m3** | 16 | 6 | 38% | 6 | 1 | 3 | **3** | D2 L M O |
| **minimax 2.7** | 24 | 9 | 38% | 8 | 5 | 2 | **2** | all 5 |
| **glm 5.3 flash** | 20 | 2 | **10%** | 2 | 16 | 0 | 0 | L M N O |

### The three perfect scores are not equivalent

- **meta — 25 for 25 across all five papers.** The only model with full coverage and no error of any
  kind. It reproduces exact figure-caption numbers (duplicated 80-entry integer register files;
  16 KB I / 8 KB D caches; 3 MB 12-way L2) and quotes guiding-principle language accurately. **This is
  the strongest single result in the collection.**
- **qwen — 14 for 14, but it declines to answer.** It produced 3 entries where others produced 5, and
  it **under-claims**: its Niagara memory-hierarchy entry is marked
  `from-general-Niagara-knowledge-not-necessarily-this-paper` (0.5) and its POWER4 split-latch
  cycle-stealing entry `from-general-POWER4-knowledge` at **0.35** — both are squarely in their
  papers, the latter with a dedicated figure. High precision bought with low recall.
- **sonnet — 12 for 12, and it doubts itself.** Two entries where others gave five, confidence
  0.25–0.85, and it too under-claims (marking the Alpha tournament predictor
  `from-general-Alpha-knowledge` at 0.25 when the paper has a labelled block diagram of it). It also
  contributed two of the three most obscure correct recalls in the corpus — Niagara's random
  I-cache replacement *"for area savings"* and the working-set / architectural-set split register
  file, both verbatim, neither in the extractions.

### The failures

- **glm 5.3 flash answered the wrong paper for M, N and O** — the identical five Alpha 21264 entries
  submitted for Pentium 4, POWER4 circuit/physical and Niagara, four of five marked
  `confident-this-is-in-the-paper`. 15 of its 20 entries are answers to a question nobody asked.
  Its L entries (the paper it actually answered) are fine. **This is a delivery/collection failure
  that no schema, honesty field or JSON check can detect** — only content-vs-target comparison finds
  it. See `episode-draft-bank.md` §6.2.
- **minimax 2.7 and minimax m3 hold 5 of the 7 contradictions** and between them all five
  POWER4-topic inversions. minimax m3 additionally refused N outright and produced corrupted output
  in three earlier slices. Their PARTIAL counts are also the highest — decisions roughly right,
  rationales invented.
- **deepseek's errors are distinctive**: it supplies claims that are true of the *chip* but absent
  from the *paper* (POWER4 instruction retry, DVFS/clock gating) and one confident contradiction
  (directory-based coherence for a snoop-based design). Same shape as its systematic TNS arithmetic
  errors elsewhere — **coherent, plausible, and reliably wrong in one direction.**

---

## 2b. ARITHMETIC RELIABILITY — from the S and T slices

Recall accuracy and arithmetic reliability are **different competencies**, and the S (formulas) and T
(test vectors) slices measure the second directly: every worked example and every vector was
recomputed step by step (`hw-calc-formulas.md`, `hw-calc-vectors.md`).

| Model | S formulas | T vectors | **ARITHMETIC RELIABILITY** |
|---|---|---|---|
| **chatgpt** | 9/9 close | 9/9 close | **EXCELLENT** — no arithmetic defect anywhere; its 4792-vs-4800 near-miss vector is the best single discriminator in the suite |
| **yuanbao** | 9/9 close | 9/9 internally consistent | **EXCELLENT with a caveat** — the only multi-element SPFM example in the corpus, and the only EAR classification that matches the regulation's banded structure; **but its SPFM denominator excludes safe faults**, a convention divergence that changes every expected value |
| **meta** | closes | 9/9 close | **EXCELLENT** — clean throughout, no classification error |
| **minimax 2.7** | closes | 9/9 close | **GOOD** — arithmetic is sound; uses the stale 25% CHIPS rate |
| **sonnet** | closes | 3/3 SPFM close, realistic magnitudes | **GOOD** — and the most honest PMHF answer in the slice ("no single closed form; requires fault-tree or Markov") |
| **kimi** | closes | 9/9 close | **GOOD** — contributes the 0.05 pp near-miss and the PD = 3.2 boundary |
| **deepseek** | ⚠ PMHF example self-destructs mid-calculation ("Wait:", "Actually") | vectors close | **MIXED** — a dimensionally wrong PMHF form (`λ×(1−DC)×t` is not a rate) with a visibly broken example, alongside sound FIT and TPP work |
| **gemini** | closes | closes | **MIXED — arithmetic excellent, rules wrong.** Contributes the best single idea in S (the closed form `χ²(2,CL) = −2·ln(1−CL)`, removing a table lookup) **and** states 3A090.a as `(TPP≥4800) OR (TPP≥1600 AND PD≥5.92)`, conflating .a with .b. Computes flawlessly, then classifies against a misremembered regulation |
| **grok** | ❌ FIT example off by 10³ (1.442e-10 stated where 1.4424e-7 is correct → 0.144 FIT vs 144 FIT) | vectors close | **MIXED** — also asserts "TPP = 1600 and PD = 5.92 meets the a.2 threshold exactly", wrong on both the band name and the boundary semantics |
| **minimax m3** | flattened shape, recovered | vectors close internally | **CONVENTION-DIVERGENT** — excludes detected multiple-point faults from the SPFM denominator; arithmetic is fine against its own definition |
| **qwen** | *no `s.json` submitted* | ❌ **2 of 3 SPFM vectors use a fabricated formula** — `SPFM = 1 − (λ_RF / λ_SPF)`, which ignores λ_total and lands on 0.90/0.99 by coincidence of inputs | **POOR on formula, GOOD on honesty** — and it carries **three explicit UNKNOWN / parameterize-the-threshold flags**, more than any other model, doing exactly what the prompt asked where it did not know a current regulatory value. **Credit that: its defect is a wrong formula confidently applied, not an invented threshold** |
| **mistral** | ❌ **SPFM stated inverted**: `λ_SP / (λ_SP + λ_MP + λ_SF)` | ❌ **all 3 SPFM vectors carry the same inversion** — one reports 95% where the correct value is 3% | **DISQUALIFYING, and stable across both slices.** Not a slip: the same structural error in the formula and in every vector derived from it. Plausible-looking ASIL percentages that are wrong by an order of magnitude |
| **glm 5.3 flash** | ❌ **wrong content — the Alpha 21264 recall again** | ❌ **same wrong content** | **NOT ASSESSABLE.** Submitted the identical paper-recall text for a formulas prompt and a test-vector prompt. Counting P, S, T and Q, the same five entries have now been submitted for **eight different prompts** |
| **mimo** | prose refusal | prose refusal | not assessable |

**Correction to the brief's premise.** The task described mistral as *"empty both, connection-suspect
not graded"*. **Both files are present and full** — `mistral s.json` is 8.8 KB with 9 recovered formula
objects, `mistral t.json` is 10.0 KB with 9 vectors. They were graded, and they contain the corpus's
most consequential arithmetic defect. Had they been skipped as empty, an inverted SPFM would have gone
into the merge unchallenged.

### What the arithmetic column adds that recall did not

**The two competencies do not correlate.** meta and chatgpt are strong at both. **qwen and sonnet are
100% on recall and split on arithmetic** — sonnet sound, qwen fabricating a formula. **grok and gemini
are 88–92% on recall and both carry arithmetic-or-rule defects.** A model trusted for one task cannot
be assumed for the other.

**Two failure shapes that a recomputation gate does not catch:**
1. **Rule errors** (gemini, grok) — arithmetic closes perfectly and the regulatory classification is
   wrong. A calculator built from these returns the right number and the wrong answer.
2. **Convention divergence** (yuanbao, minimax m3) — arithmetic closes against a *different* stated
   denominator. Not an error, but silently incompatible with the other models' fixtures.

Only the third shape — **stated steps that do not reproduce the stated output** (mistral, qwen, grok's
FIT, deepseek's PMHF) — is mechanically detectable, and it accounts for 12 of 113 vectors.

---

## 2c. CLASS-1 ARITHMETIC RELIABILITY — Day 2 (GLOBE · APPJ · TRID · OFAC)

Day 2's four prompts required step-by-step arithmetic, making adjudication mechanical: **55 files,
~250 computations, every one re-executed independently** (`day2-c1-adjudication.md`). This is a
different and better measurement than the S/T column above, because the prompts were designed for it.

| Model | VERIFIED | SELF-INCONSISTENT | WRONG-INPUT | WRONG-RULE | Anti-reversal | **CLASS-1 VERDICT** |
|---|---|---|---|---|---|---|
| **chatgpt** | 15/15 assessable | 0 | 0 | 0 | 0 | **EXEMPLARY** — APPJ rates match independent bisection to **1e-10** across four Appendix J code paths; 5/5 published GLOBE examples close. *One file wrong-content (OFAC = its TRID), not assessable* |
| **kimi** | 20/20 | 0 | 0 | 0 | 0 | **EXEMPLARY** — clean on all four prompts; reproduces both published APPJ anchors |
| **grok** | 20/20 | 0 | 0 | 0 | 0 | **EXEMPLARY** — both APPJ anchors, full-attribution OFAC |
| **meta** | 18/18 | 0 | 0 | 0 | 0 | **EXCELLENT** — honestly labels all APPJ cases as constructed |
| **qwen** | 19/19 | 0 | 0 | 0 | 0 | **EXCELLENT** — contributes the sharpest TRID discriminator (+400/−400, aggregate zero) |
| **sonnet** | 18/18 | 0 | 0 | 0 | 0 | **EXCELLENT** — the only 47% near-miss OFAC vector |
| **minimax 2.7** | 19/19 | 0 | 0 | 0 | 0 | **EXCELLENT** — see reinstatement below |
| **yuanbao** | 19/20 | 0 | 0 | 0 | **1** | **STRONG** — Form 1 and Form 3 closed forms verify exactly; one TRID case titled "aggregate passes" while its own verdict is a violation |
| **glm 5.3 flash** | 14/14 | 0 | 1 (GLOBE rate year) | 0 | 0 | **STRONG** — best OFAC gate case in the batch; *trid file absent* |
| **mimo** | 19/20 | 1 (OFAC) | 0 | 0 | 0 | **GOOD** — and it produced parseable JSON for the first time in the collection |
| **gemini** | 15/16 | 0 | 0 | **1** (OFAC multiplicative) | 0 | **GOOD-with-rule-defect** — arithmetic exact, legal treatment wrong on the one case the prompt was built to expose |
| **deepseek** | 18/20 | 1 (TRID) | 1 (GLOBE rate pair) | 0 | 0 | **MIXED** — substituted its own inputs mid-computation to manufacture a violation |
| **mistral** | 17/20 | 3 (OFAC) | 0 | 0 | 0 | **MIXED** — correct attribution arithmetic, blocked-entity verdicts omit the intermediaries |
| **minimax m3** | 3/3 recovered | 0 | 0 | 0 | 0 | **NOT ASSESSABLE** — token dropout in 3 of 4 files |

### What this column changes

1. **Class-1 framing beats model selection.** Twelve of fourteen models produced defect-free
   arithmetic on at least three of four prompts. **All 13 responding models avoided the
   sum-of-increases trap** in 31 mixed-direction TRID cases. Requiring shown steps did more for
   reliability than any rotation decision in this scorecard.
2. **`weakest_point` hit 100% adoption** (55/55 files, every item) — up from 91% in Prompt P. But it
   missed the one SELF-INCONSISTENT entry in the batch: deepseek's TRID case flagged its GLOBE rate
   risk and not its own substituted fee table. The field surfaces *perceived* uncertainty, not
   mechanical self-contradiction.
3. **Three defect classes, only one machine-detectable.** Broken artefact (deepseek) — caught by
   recomputation. Misapplied rule with exact arithmetic (gemini) — invisible to recomputation.
   Incomplete answer field over correct work (mistral) — also invisible. Same three-way split found
   in the S/T slices, now confirmed on a purpose-built prompt set.

### Status changes

- **glm 5.3 flash — SUSPENSION LIFTED for deterministic-computation work.** The wrong-content failure
  that suspended it did not reproduce across three files; its OFAC set is among the batch's best.
  Paper-recall reinstatement is **not** decided here — no recall prompt was run.
- **minimax 2.7 — DROP OVERTURNED for Class-1 work.** 5/5 on TRID and OFAC, no corruption in any of
  four files. The drop rested on recall inversions and integrity failures; neither recurred.
- **mimo — DROP OVERTURNED on delivery.** First parseable JSON in the collection after thirteen prose
  refusals, and 19/20 verified.
- **minimax m3 — DROP STANDS.** Token-level dropout in three of four files, the same serialization
  defect now seen across five collection days.
- **chatgpt — a wrong-content instance, and it changes the diagnosis.** Its `ofac.json` contains its
  TRID content. The wrong-content failure was previously attributed to glm alone across eight slices;
  its appearance in the collection's most reliable model **moves the diagnosis from "one bad model"
  to "a defect in the collection or paste step."** No quality inference is drawn against chatgpt,
  whose other three files are the strongest in the batch. **The target-content pre-check is now
  unambiguously required before any grading pass.**

### Rotation, revised

**Class-1 deterministic computation:** chatgpt, kimi, grok, meta, qwen, sonnet, minimax 2.7 — all
defect-free. **Add a rule-check step for gemini** (arithmetic trustworthy, legal classification not)
and **a completeness check for mistral** (computations trustworthy, answer fields not). **Recall and
extraction:** unchanged — meta, grok, yuanbao, verified by sonnet and qwen. **Still suspended from
recall:** glm 5.3 flash, pending a recall re-trial. **Still dropped:** minimax m3, on delivery alone.

*(Superseded in part by §2d — the second Day-2 batch reverses three of these placements.)*

---

## 2d. CLASS-1, SECOND BATCH — Day 2 (IRB · FRTB · MICA · CCD2 · RECEIPT · JCS)

**86 files, 15 models × 6 prompts, ~470 recomputations** (`day2-c1b-c2-adjudication.md`). Four
regulatory-math prompts re-executed in scratch Python; 208 JCS vectors graded against a scratch
RFC 8785 canonicalizer self-tested on the RFC's own published vectors; the receipt slice has **no
ground truth** and is excluded from scoring.

**Denominators.** Six files never arrived — glm 5.3 flash × {irb, frtb, mica, ccd2}, kimi/ccd2,
mimo/irb. **These are no-data, not failures**, and no verdict is recorded against a model for a file
that did not arrive. glm 5.3 flash's Class-1 reinstatement from batch 1 stands untouched.

| Model | IRB | FRTB | MICA | CCD2 | JCS | **BATCH-2 VERDICT** |
|---|---|---|---|---|---|---|
| **chatgpt** | 4/4 ✓ | ✓ | ✓ | 4/4 ✓ | **10/11** | **EXEMPLARY** — IRB to 15 s.f.; JCS recovered only by salvage (its file's inner quotes were unescaped) |
| **kimi** | 4/4 ✓ | ✓ | ✓ | *absent* | **12/12** | **EXEMPLARY** — the only model that *derives* its Basel benchmark (CRE99.2 at LGD 40%, scaled) rather than asserting one; flawless canonicalizer |
| **sonnet** | 4/4 ✓ | ✓ | ✓ | 4/4 + **1 honest UNKNOWN** | **12/12** | **EXEMPLARY** — declines to assert an APRC it cannot close; joint-best JCS |
| **meta** | 4/4 ✓ | ✓ | ✓ | ✓ | **10/10** | **EXEMPLARY** — and the only receipt file with source-level detail (domain-separator tags, 4-byte selector, 128-bit claim-digest split) |
| **grok** | 4/4 ✓ | ✓ | ✓ | 5/5 ✓ | 10/11 | **EXCELLENT** — one escaping-form miss only |
| **qwen** | 4/4 ✓ | ✓ | ✓ (4 UNKNOWN flags) | 5/5 ✓ | 9/10 | **EXCELLENT** — its MiCA flags sit on the one figure now marked NEEDS-RETRIEVAL |
| **mimo** | *absent* | ✓ | ✓ | 5/5 ✓ | 9/11 | **STRONG** — second consecutive batch of parseable, correct output |
| **glm 5.3 flash** | – | – | – | – | 9/11 | **INSUFFICIENT DATA** — 2 of 6 files. One anti-reversal instance (below) |
| **yuanbao** | **WRONG-RULE 4/4** | ✓ | ✓ | 5/5 ✓ | 9/11 | **SPLIT** — exact on APRC, wrong grouping on CRE31 |
| **deepseek** | 4/4 ✓ | ✓ | ✓ | **SELF-INCONSISTENT 3** | 13/15, **1 WRONG-RULE** | **MIXED** — the batch's only UTF-16 key-order failure, and APRCs disconnected from its own schedules |
| **gemini** | 3/4, **1 SELF-INCONSISTENT** | ✓ | ✓ | **SELF-INCONSISTENT 3** | 6/8 | **MIXED** — nominal rate reported as APRC; fabricated a benchmark that confirms its own error |
| **solar** | **WRONG-RULE 4/4** | ✓ | ✓ | 1/1 ✓ | 17/19 | **SPLIT** — best JCS volume in the batch, worst IRB formula |
| **minimax 2.7** | **WRONG-RULE 4/4 + WRONG-INPUT** | ✓ | ✓ | **WRONG-RULE 2** | 5/10 | **WEAK — but self-flagged.** Four independent IRB defects, each correctly reported as not matching benchmark |
| **minimax m3** | **SELF-INCONSISTENT** | ✓ | ✓ | **SELF-INCONSISTENT 3** | 6/9 | **WEAK** — fabricated a BCBS table citation to explain away its own arithmetic |
| **mistral** | **WRONG-RULE 4/4** | ✓ | ✓ | **WRONG-RULE + SELF-INCONSISTENT 3** | **3/11** | **BOTTOM** — weakest on arithmetic, rules and output integrity simultaneously |

**Solar cross-add to batch 1:** `trid` **VERIFIED 5/5** (its case 3 is a clean aggregate-vs-sum-of-
increases discriminator); `ofac` **2/5 VERIFIED, 3/5 WRONG-RULE** under the batch-1 standard — it
declares a *hybrid* rule (full attribution through blocked intermediaries **plus** multiplicative
through non-blocked ones) that is a third live reading in the corpus, and on one case it moves the
target from 40% to exactly 50.0% and flips the legal outcome.

### What the second batch changes

1. **Two of six purpose-built traps caught nobody.** FRTB's ES-vs-VaR conflation: **zero instances in
   14 files** — every model has the ES multipliers 2.3378 / 2.6652 right. MiCA's wrong-tail trap:
   **zero in 13 files** — `tail_convention` present on every case, all testing the adverse tail. The
   JCS UTF-16 ordering trap caught **one model of eight** that built it. **Defects appear where the
   prompt was not looking:** mistral's simple-interest APRC, minimax 2.7's nominal-monthly
   discounting, solar's OFAC hybrid.
2. **The honesty fields are independent of correctness in both directions, at 100% adoption.**
   gemini invented a 50.6% Basel benchmark to ratify a 19-point error. minimax m3 cited "BCBS 128,
   Table 1" to explain away a slip. minimax 2.7 was wrong four ways and said so
   (*"COMPUTED DOES NOT MATCH KNOWN BENCHMARK"*). **The only signal in the audit is the absence of a
   label:** mistral's honesty text runs 4–45 characters, including the batch's only
   `weakest_point: "None"`, and mistral is the weakest model in the batch. A short label predicts a
   weak answer; a long one predicts nothing.
3. **Salvage decides scores.** Three techniques new to this pass — unescaped inner quotes, a
   `"key":"value"` pair inside an array, raw newlines inside strings — turned `chatgpt jcs` from 0/33
   fragments into 10/11, and `sonnet receipt` and `yuanbao receipt` from zero sections into 7/7.
   **Emission bugs are not quality signals**; the ladder is now eight techniques deep.
4. **The 15-significant-figure agreement is a new capability signal.** chatgpt, grok and meta produce
   *bit-identical* CRE31 outputs (`5.568938909768941`). That is not "agreement" — it is three models
   running the same closed form at full double precision, and it makes a three-way golden vector
   available for free.

### Status changes — second batch

- **kimi, sonnet, meta — promoted to first-rank Class-1.** All three were already strong; this batch
  adds the behaviours that matter under audit: kimi derives its benchmark instead of asserting one,
  sonnet returns an explicit UNKNOWN rather than a manufactured number, meta carries the only
  source-level structural detail in the receipt slice.
- **gemini — rule-check step is now mandatory, not advisory.** Batch 1 found one WRONG-RULE (OFAC
  multiplicative). Batch 2 adds a self-inconsistent IRB case *and a fabricated benchmark that
  confirms it*, plus three APRCs reported at the nominal rate. Its arithmetic is still usually exact;
  **its self-verification is actively misleading and must not be trusted as a check.**
- **mistral — DOWNGRADE. Remove from all computational work.** Three batches, three instances of the
  same signature: writes a formula missing a term, computes it correctly, reports a third number
  (inverted SPFM in S/T; dropped `/(1−1.5b)` in IRB; simple-interest APRC reported as 500/10500). Add
  six substantive RFC 8785 failures and the batch's only malformed JSON output. It remains useful
  where its honest `null`s are the answer — its MiCA `article_basis: null` is more valuable than nine
  confident unretrieved constants.
- **deepseek — narrower than batch 1 suggested.** IRB exact 4/4; CCD2 answers disconnected from its
  own schedules; the only UTF-16 key-order failure in 208 vectors, at `certainty: rfc-exact`.
  **Trust its closed-form work, verify anything it solves iteratively or sorts.**
- **minimax 2.7 — the reinstatement holds, with a caveat that is nearly a compliment.** Its IRB work
  is wrong four independent ways and it flagged that it was wrong. Usable **only** where a checker
  reads the flag; unusable where the number is consumed directly.
- **minimax m3 — DROP STANDS, and the reason has changed.** Batch 1 dropped it on delivery (token
  dropout). This batch it delivered cleanly and **fabricated authority twice** — a BCBS table
  citation and a Directive annex example, both attached to numbers its own data contradicts. That is
  a worse defect than dropout, because dropout is visible.
- **glm 5.3 flash — no new evidence.** Two of six files. Its one JCS anti-reversal instance
  (a vector titled *"No Unicode normalization"* whose own output normalizes U+2126 → U+03A9) is
  recorded but is too thin to move its standing either way.

### Rotation, second revision

**Regulatory closed-form math (IRB/FRTB/ES-class):** chatgpt, kimi, grok, meta, qwen, sonnet —
six models, defect-free, three of them bit-identical. **Iterative solves (APRC/IRR-class):** chatgpt,
grok, qwen, yuanbao, mimo, sonnet, meta — **never** deepseek, gemini, minimax m3 or mistral, all of
which report a number that is not the solution to their own equation. **Canonicalization / byte-exact
specification work:** kimi, sonnet, meta, chatgpt (post-salvage) — **never** mistral. **Structural
recall of undocumented formats:** meta first, grok second, everything else single-source and
unverified.

---

## 3. Honesty-field calibration — did the labels predict correctness?

The question the scorecard exists to answer: **can `confidence` or `paper_vs_general` be used to
filter?**

### 3.1 `confidence` — no

| Grade | Median self-confidence |
|---|---|
| CONFIRMED | 0.90 |
| PARTIAL | 0.75 |
| NOT-IN-PAPER | 0.85 |
| **CONTRADICTED** | **0.82** |

Contradicted claims are rated **as confidently as** partial ones and nearly as confidently as correct
ones. Specific cases: minimax m2.7's frequency inversion at `confident` / 0.82; gemini's
not-in-the-paper shared FPU at `confident` / **0.95**; glm's wrong-paper entries at 0.75–0.90. Against
that, sonnet's *correct* obscure recalls sit at 0.25–0.75.

**`confidence` is uninformative for recall, exactly as it was for episodes, SDC patterns, node deltas
and review checklists. Five slices, same result. Stop reading it.**

### 3.2 `paper_vs_general` — informative but weak, and it fails in both directions

| Self-label | Entries | CONFIRMED | NOT-IN-PAPER or CONTRADICTED |
|---|---|---|---|
| `confident-this-is-in-the-paper` | ~170 | 78% | 13% |
| `probably-in-the-paper` | ~65 | 66% | 22% |
| `from-general-…-knowledge` | ~10 | **70%** | 20% |

The gradient between `confident` and `probably` is real but shallow — a 12-point difference in
confirmed rate. The third row is the interesting one: **entries the models flagged as *general
knowledge* were confirmed 70% of the time**, i.e. roughly as often as `probably-in-the-paper`. Every
one of those under-claims came from qwen or sonnet.

So the field fails both ways:
- **Over-claiming:** the worst error in the corpus (gemini's shared FPU, glm's wrong paper, minimax
  m2.7's inversion) is labelled `confident`.
- **Under-claiming:** correct, verbatim recalls are labelled general knowledge and would be discarded
  by a filter that trusted the label.

**Usable as a weak negative signal — a `probably` entry deserves checking first — and not as a
filter.** The one genuinely excellent use of the field is yuanbao's out-of-schema entry, which scoped
*two different labels to two clauses of the same claim* (`episode-draft-bank.md` §6.5). That is more
honesty than the schema can express, and the schema should be widened to accept it.

### 3.3 What does predict correctness

Nothing in the output. **Model identity does**: 4 models are ≥92% across ≥16 entries; 3 are ≤38%.
And **paper identity does**: 62% confirmed on POWER4-microarchitecture against 80% on Niagara, with
the same models. Grade a model on one paper and you have measured almost nothing — chatgpt inverted
POWER4's central decision and then scored 15/15 across Alpha, Pentium 4 and Niagara.

---

## 4. Rotation recommendation

Combining recall accuracy here with generative performance in F (diagnosis), G (SDC), H (proving
pitfalls), I (review checklists) and K (node deltas).

### Trusted for recall — give these the paper work

| Model | Why |
|---|---|
| **meta** | 25/25 across all five papers. Exact numbers, accurate quotation, full coverage. First call for any extraction or recall task. |
| **grok** | 23/25, zero inversions, and the single best recall in the collection — POWER4's *"global slew rate limit equal to one third of the cycle time"* and the late-binding low-Vt swap, both verbatim, on the paper closest to Alice's domain. |
| **yuanbao** | 22/24, quotes distinctive phrasing, reproduces exact cache and coherence configurations. One inversion (Alpha register counts) which its own honesty field isolated as its only non-confident entry. |
| **sonnet, qwen** | Perfect precision, low volume, systematic under-claiming. Use them as **verifiers**, not as primary recall — ask them to check another model's entries rather than to generate. |

### Generative scaffolding only — do not trust their recall

| Model | Why |
|---|---|
| **chatgpt** | 92% recall but owns one inversion, and its citation record is poor (a "jackpot" C-slice paper title that does not exist). Meanwhile it is the **best structural contributor in the collection**: the sharpest F library, the best-reasoned SDC mode-analysis pattern, the only literature-grounded red-team objection. Use for structure and merged prose; verify every fact. |
| **gemini** | 88% recall but the shared-FPU error at 0.95 confidence, plus two arithmetically impossible episodes and a swapped-port SDC derivation elsewhere. Excellent at structure and staged derivations; **never trust its numbers or its confident negatives.** |
| **kimi** | 79% recall, strong H-slice and B-cell work, honest B-cell sourcing. Solid mid-tier for generative slices. |
| **deepseek** | 80% recall but the errors are systematic and confident in a single direction — plausible content the source does not contain. Its F-slice thresholds and G-slice provenance-naming are genuinely useful. **Generative only, and spot-check.** |

### Drop, or fix the pipeline around them

| Model | Why |
|---|---|
| **glm 5.3 flash** | Answered the wrong paper three times out of four, confidently. Until the cause is identified — model, session or paste step — nothing it produces can be trusted without a target-paper keyword check. **Suspend from recall; re-test once with a content guard in place.** |
| **minimax 2.7** | 38% recall, 2 inversions, plus token-level output corruption, a chat summary submitted instead of JSON, and two quota failures. Four distinct integrity failure modes across the collection. **Drop.** |
| **minimax m3** | 38% recall, 3 inversions — the most of any model — plus truncation in F, corruption in I and J, a UI capture artefact, and a prose refusal in N. **Drop.** |
| **mimo** | Refused 8 of 11 prompts as injection attempts while answering substantively in prose every time — and its POWER4 prose got the clock-philosophy direction *right* where three JSON-compliant models inverted it. **Not a bad model; an undeliverable one.** Test the paste-as-user-message workaround once; if the refusals persist, drop. |

### The rotation, in one line — updated for arithmetic

**Recall and extraction: meta, grok, yuanbao. Deterministic-math work: chatgpt, meta, yuanbao (with
its denominator convention pinned first) — never mistral or qwen. Verification passes: sonnet and
qwen for recall, sonnet for math. Generative slices: chatgpt and gemini for structure, kimi and
deepseek for breadth, all spot-checked. Suspended: glm 5.3 flash. Dropped: minimax 2.7, minimax m3.
Pending a delivery fix: mimo.**

**The one change the arithmetic column forces:** qwen moves from unqualified verifier to
*recall-verifier only*. It is 14/14 on paper recall and it fabricated an SPFM formula. Its honesty is
intact — it flagged unknown thresholds more often than anyone — but honesty about what it does not
know does not make it right about what it thinks it does.

### The rotation, in one line — updated for the second Day-2 batch

**Regulatory closed-form math: chatgpt, kimi, grok, meta, qwen, sonnet. Iterative solves: the same
six minus kimi, plus yuanbao and mimo — never deepseek, gemini, minimax m3 or mistral. Byte-exact
specification work: kimi, sonnet, meta, chatgpt — never mistral. Recall and extraction: unchanged —
meta, grok, yuanbao. Verification passes: sonnet, and kimi where a benchmark must be derived rather
than recalled — and never gemini, whose self-verification now demonstrably confirms its own errors.
Removed from computational work: mistral. Dropped: minimax m3, now for fabricated citations rather
than for delivery. Still suspended from recall: glm 5.3 flash. Reinstated on delivery: mimo,
minimax 2.7 (the latter only where a checker reads its self-flags).**

**The one change the second batch forces:** **qwen's caveat partially lifts and gemini's tightens.**
qwen is 4/4 IRB, 5/5 CCD2, 9/10 JCS, and its MiCA `UNKNOWN` flags landed on the exact constant this
digest now marks NEEDS-RETRIEVAL — restored as a math verifier, with the S/T formula-fabrication note
still standing for *unprompted* formula recall. gemini goes the other way: it is the one model
observed to **manufacture a corroborating benchmark for its own wrong answer**, which makes it the
one model that must never be used to check anything, including itself.

**Three retrievals now gate the harvest, not the grading:** the MiCA own-funds floor (asserted by 9
of 13 models, retrieved by none), the OFAC indirect-attribution rule (three live readings, one
threshold case that flips between them), and the risc0 Groth16 receipt layout (17 single-source field
names).

`TODO(alice): the recall tier above is graded against paper text by an agent, not by a domain expert.
The claim being made is "this model said what the paper says", not "this model said something true".`
