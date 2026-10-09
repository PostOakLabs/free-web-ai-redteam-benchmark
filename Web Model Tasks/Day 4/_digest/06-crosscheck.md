# Corpus-recall cross-check — the paid-for defect detector, run

Commission `DIGEST-COMMISSION-DAY4-1.md` §2.3, §2.4 and the addendum. This is the deliverable the
commission says the estate most wants. Every number below is an output of
`digest/_verify/d4xcheck.py` (hashed in `MANIFEST-D4.sha256`), reproduced in
`digest/_verify/d4run/xcheck.txt`. **As-of 2026-09-09T01:41:45Z.**

---

## 1. Memorial-3's two corrections, checked against 15 independent recalls

`SESSION-MEMORIAL-2026-09-08-REDTEAM-3.md` corrected two `outcome` percentages in
`extractions/Alpha21264.episodes.json`. Day 4's `alpha` family recalls the same two sentences 15
more times, independently, from 2026-09-04. **Both corrections are corroborated. Neither is
contradicted.**

| sentence | paper says | corpus recalls paper-true | corpus recalls the pre-correction value | silent |
|---|---|---|---|---|
| branch-predictor success rate (ep00, fixed `5%`→`90%`) | `90% to 100%` — 1 hit | **1** — meta | **0** | 14 |
| line/way prediction accuracy (ep06, fixed `95%`→`85%`) | `85% to 100%` — 1 hit | **2** — chatgpt, meta | **0** | 13 |

The pre-correction values `5% to 100%` and `95% to 100%` appear **zero** times in the paper and
**zero** times anywhere in the 15-file corpus. The corrections stand on two independent legs now:
memorial-3's source check, and a panel that never held the wrong figure.

**The honest limit.** Only 1–2 of 15 models recall these sentences at all. Corroboration is real but
thin, and it comes from the two models that quote most (§3). Fourteen models being silent is not
fifteen models agreeing.

## 2. Convergence, then actually checked — §2.3

Day 3 could only report "9 of 13 assert it, retrieved by none". Here every convergent numeric claim
is checked against the paper. **Claims made by ≥3 models, all four paper families:**

| family | claim | models | verdict | matched via |
|---|---|---|---|---|
| alpha | 64 kb | 5/15 | IN-PAPER (4 hits) | numeral |
| alpha | 600 mhz | 5/15 | IN-PAPER (4) | numeral |
| alpha | 80 entries | 3/15 | IN-PAPER (1) | **singular `80-entry`** |
| niagara | 32 threads | 9/14 | IN-PAPER (5) | numeral |
| niagara | 4 threads | 3/14 | IN-PAPER (7) | **spelled-out `four threads`** |
| niagara | 16 kb · 8 kb · 3 mb | 3/14 each | IN-PAPER (1 each) | numeral |
| p4 | 1.5 ghz | 7/15 | IN-PAPER (6) | numeral |
| p4 | 20 stages | 6/15 | IN-PAPER (1) | **singular `20-stage`** |
| p4 | 3 ghz · 400 mhz · 3.2 gb · 1 ghz · 100 mhz · 8 kb | 3–4/15 | IN-PAPER | numeral |
| p4 | 256 kb | 3/15 | IN-PAPER (1) | numeral + dehyphen |
| pphysical | 1 ghz | 4/14 | IN-PAPER (4) | numeral |

**Zero convergent numeric claims are unsupported by their paper.** Not one "majority wrong".

**Three of these were false NOT-FOUND on the first pass** and are the reason the matcher now tries
singular/plural and numeral/spelled-out forms. Had the first pass been published, this digest would
have reported that 6 of 15 models invented a 20-stage pipeline the paper states plainly, and two
similar claims besides. The `matched via` column exists so a reader can see which widening rescued
each claim rather than trusting a bare verdict.

## 3. Per-model, per-paper verdicts — for TALLY-42 cross-grading

The addendum asks for per-model per-paper output so a later TALLY-42 run can grade
`direction_check` against each model's own prior recall without re-parsing. Machine-readable at
`digest/_verify/d4run/d4permodel.json`.

`ent` entries · `assert` quotes actually asserted · `verb` verbatim (incl. hyphen-variant) ·
`para` paraphrase-consistent · `T3` contradicts · `T4` not-found · `decl` declined ·
`pg±2` page guesses within 2 of the located page, journal→PDF offset applied.

| model | alpha | niagara | p4 | pphysical |
|---|---|---|---|---|
| **grok** | 5 verb, 5/5 pg | 5 verb, 5/5 pg | 5 verb, 3/3 pg | 5 verb, 5/5 pg |
| **meta** | 5 verb, 5/5 pg | declined | 5 verb, 5/5 pg | declined |
| **kimi** | 4 verb +1 para, 5/5 pg | declined | 5 verb, 5/5 pg | declined |
| **chatgpt** | 3 verb +2 para, 5/5 pg | 5 verb, 5/5 pg | 3 verb +2 para, 5/5 pg | absent |
| **deepseek** | declined | 2 para, **2 T4** | 2 verb, **1 T4** | 2 verb, 1 para, **1 T3** |
| **glm 5.3 flash** | declined | 2 para, **3 T4** | **FAILED (unparseable)** | **5 T4** |
| **longcat** | declined | absent | **5 T4** | declined |
| gemini · mimo · minimax 2.7 · minimax m3 · mistral · qwen · sonnet · yuanbao · solar | declined | declined | declined | declined |

**The split is bimodal and total.** Four models (grok, meta, kimi, chatgpt) assert quotes and are
overwhelmingly verbatim; nine models decline on every entry of every paper; three (deepseek,
glm 5.3 flash, longcat) assert quotes that are not in the paper.

**grok is the standout:** 20 of 20 entries verbatim across all four papers, with 18 of 18 scored page
guesses within ±2.

## 4. Hand-confirmed findings

Reported only after checking the source directly, per commission §4.

### 4.1 One contradiction — deepseek, `pphysical`, entry 2

> quote: *"…supplies a single critical **1.5 GHz** clock from one SOI-optimized PLL to 15,200 pins…"*

| claim | paper |
|---|---|
| 15,200 pins | ✓ *"low skew among any of the 15200 clock pins on the chip"* |
| one PLL | ✓ *"a single PLL was used, placed near the center of the chip"* |
| SOI-optimized PLL | ≈ *"an SOI-specific phase-locked-loop (PLL) design"* |
| **1.5 GHz** | ✗ **the paper says 1.3 GHz throughout.** `1.5` appears only as `1.5 V`, the supply voltage |

**T3 CONTRADICTS-PAPER, confirmed.** Three of four elements are right; the frequency is wrong, and
`1.5` is present in the paper as a voltage. A voltage-for-frequency transplant is the most likely
reading, but this digest does not assert the mechanism.

### 4.2 Two whole-file fabrication sets — 10 quotes, hand-confirmed

`glm 5.3 flash pphysical.json` (5/5) and `longcat p4.json` (5/5) return T4 on every entry. Probed by
hand at 60-, 40- and 25-character leading fragments against both the normalised and de-hyphenated
source: **no fragment of any quote appears at any length.** Samples:

```
glm 5.3 flash : "static timing analysis was the cornerstone of our timing closure methodology."
longcat       : "the hyper-pipelined technology doubles the pipeline depth of the p6 microarchitecture."
```

These are fluent, plausible, generically-worded sentences of the kind a paper *could* contain.
That is what distinguishes them from extraction artifacts, which are fragmentary and misspelled.
`glm 5.3 flash niagara.json` adds 3 more; `deepseek` adds 3 across niagara and p4. **16 T4 total.**

## 5. What this says, and what it does not

**Says:** the corpus's convergent numerics are sound; memorial-3's corrections are independently
corroborated; four models quote this literature accurately and locate it to within two pages; three
models produce confident quotes that are not in the papers.

**Does not say:** anything about the nine declining models' *knowledge*. Declining to quote is the
prompt's own sanctioned escape and this digest scores it as a pass, not a gap. A model that declines
every quote has made no checkable claim — that is honest behaviour, and it is also no evidence.

**Does not say** anything about `lvs`, which has no paper (see `05-lvs.md`).

## 6. Feeding TALLY-42

`RUNSHEET-42.md`'s operator notes call for grading `direction_check` against each model's own prior
recall of these same papers. That cross-grade is now possible without re-parsing:

- `d4permodel.json` keys are `"<model>|<family>"` and carry per-model per-paper tier counts.
- The four papers overlap RUNSHEET-42's pools exactly: `alpha`→Alpha 21264, `niagara`→Niagara,
  `p4`→Pentium 4, `pphysical`→POWER4 circuit/physical. RUNSHEET-42's fifth pool
  (POWER4 system, blocks 29–42) has **no Day-4 family** — Day 3's `power4` covers that paper.
- **Suggested use:** a model returning `REVERSAL` on a TALLY-42 block for a paper where it scored
  5/5 verbatim here is a sharper signal than one from a model that declined every quote.
