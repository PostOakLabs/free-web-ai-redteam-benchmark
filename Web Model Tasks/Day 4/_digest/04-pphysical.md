# Digest — family `pphysical`

**Prompt:** `prompts/D2-POWER4-PHYSICAL-RECALL.md` — Warnock et al., *The circuit and physical design
of the POWER4 microprocessor*, IBM JRD 46(1):27–52, 2002.
**Ground truth:** `sources/POWER4-cpd-pagemarked.txt`. **14 files, 66 entries, 14 of 14 parse clean.**
As-of 2026-09-09T01:41:45Z.

## Model set — 14

deepseek · gemini · glm 5.3 flash · grok · kimi · longcat · meta · mimo · minimax 2.7 · mistral ·
qwen · **solar** · sonnet · yuanbao. **chatgpt is ABSENT** from this family — recorded, not absorbed.

This is the companion paper to Day 3's `power4` family. Day 3's `03-power4.md` flagged a
`minimax m3` entry as clock-distribution content "belonging to the companion paper" and could not
resolve it; the companion's own 14 files are here.

## Quote grading

| tier | count |
|---|---|
| T1 verbatim | **7** |
| T2 paraphrase-consistent | 1 |
| **T3 contradicts-paper** | **1 (hand-confirmed)** |
| **T4 not-found** | **5** |
| T0 declined | 51 |
| entries | 66 |

**The weakest family in Day 4**: 14 assertions, 7 verbatim, 6 defective. Also the lowest confidence
(mean 0.643) and the highest `probably-in-the-paper` share (38 of 66). The models are collectively
less certain here, and the grading says they are right to be.

| model | result |
|---|---|
| grok | 5/5 verbatim, 5/5 page guesses within ±2 |
| deepseek | 2 verbatim, 1 paraphrase, **1 T3** |
| **glm 5.3 flash** | **5/5 T4 — every quote fabricated** |
| 11 others | declined |

Page offset PDF = journal − 26, from the extraction file's `_locator_note`.

## The one contradiction in Day 4, hand-confirmed

**deepseek, entry 2, clock distribution.** Quote claims *"a single critical **1.5 GHz** clock from
one SOI-optimized PLL to 15,200 pins"*.

| element | paper |
|---|---|
| 15,200 pins | ✓ `low skew among any of the 15200 clock pins on the chip` |
| one PLL | ✓ `a single PLL was used, placed near the center of the chip` |
| SOI-optimized PLL | ≈ `an SOI-specific phase-locked-loop (PLL) design` |
| **1.5 GHz** | ✗ **the paper says 1.3 GHz throughout.** `1.5` occurs only as `1.5 V`, the supply voltage |

Three of four elements are correct. The frequency is wrong, and the wrong figure is present in the
paper as a voltage. **This digest records the contradiction and does not assert the mechanism.**

## glm 5.3 flash — five fabricated quotes, hand-confirmed

No fragment of any of the five appears in the source at 60, 40 or 25 characters, in either the
normalised or de-hyphenated text. Sample:

```
"static timing analysis was the cornerstone of our timing closure methodology."
"embedded decoupling capacitors were essential to manage power integrity."
```

Fluent, plausible, absent.

## Convergent numerics, checked against the paper

Only one claim reaches three or more models: `1 ghz`, 4/14, **IN-PAPER** (4 hits). Convergence is far
weaker here than in the other three families, consistent with the low assertion rate.

## The only `not_in_paper: true` in Day 4

Across 272 entries in four paper families the escape is used **exactly once**, and it is here. Day
3's `power4` family used it **zero times in 68 entries**. The field exists, is almost never taken,
and therefore carries close to no signal for filtering.
