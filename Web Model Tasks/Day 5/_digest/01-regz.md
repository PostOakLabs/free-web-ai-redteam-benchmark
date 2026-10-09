# Track A — `regz`, exact recomputation

**Prompt:** `prompts/C1-REGZ-FACTOR.md` — Regulation Z qualified-mortgage points-and-fees tiers.
**16 files, 15 gradable.** As-of 2026-09-09T14:11:04Z.

**No tunable exists on this track.** No overlap floor, no paraphrase tier, no window. A value is
present at 6 decimal places or it is not. This is the one track in the corpus where a wrong answer
cannot be argued into a right one.

---

## Reference — computed by `d5grade_regz.py`, never transcribed

| tier | 2023 | 2024 | factor (6dp) | 2025 projection ×1.034 |
|---|---|---|---|---|
| A | 124,331 | 130,461 | **1.049304** | **134,897** |
| B | 3,730 | 3,914 | **1.049330** | **4,047** |
| C | 24,866 | 26,092 | **1.049304** | **26,979** |
| D | 1,243 | 1,305 | **1.049879** | **1,349** |

Official 2025 tier A is **134,841**, so the implied factor is **1.033573**, which sits **4.27 bp**
below the stated 3.4 %, and the projection overshoots by **56**.

The four factors are *not* mutually uniform (A and C agree at 1.049304; B and D do not), and none
equals the stated 4.9 %. That non-uniformity is the substance of task 1.

## Results — 9 checked values per model

| model | task 1 /4 | task 2 /4 | task 3 factor | score /9 |
|---|---|---|---|---|
| chatgpt · gemini · glm 5.3 flash · grok · kimi · longcat · meta · mimo · minara · qwen · sonnet · yuanbao | 4 | 4 | ✓ | **9** |
| deepseek | 4 | 4 | ✗ | 8 |
| minimax 2.7 | 1 | 4 | ✗ | 5 |
| mistral | 1 | 1 | ✗ | 2 |
| solar | — | — | — | **NOT GRADABLE** |

**12 of 15 gradable models are exact on all nine values.**

> **CORRECTED 2026-09-09 after the Flash vet.** This read **13** until an audit pass found that
> the matcher compared SUBSTRINGS, not values: `1.033573` occurs inside deepseek's working figure
> `1.0335735`, and deepseek's *stated* 6dp answer is **1.033574**, which is wrong (the true value is
> 1.03357325…). deepseek was credited for task 3 and is now 8 of 9. Six other models wrote the
> full-precision `1.033573251776393` and legitimately keep the credit. The matcher now compares
> numbers at the reference's own precision. `mistral`'s task-3 basis-point credit fell away in the
> same fix. **The Flash vet reproduced the 13 and signed it off — reproducing a number does not test
> the rule that produced it.**

## The two failures — hand-confirmed against the models' own text

Reported only after reading their task-1 steps directly, per the estate rule.

**minimax 2.7** — 1 of 4 factors right. Its own steps read:

```
Tier A: 130461 / 124331 = 1.04936534… → 1.049365      (reference 1.049304)
Tier B: 3914 / 3730     = 1.04933029… → 1.049330      ✓
Tier C: 26092 / 24866   = 1.04929409… → 1.049294      (reference 1.049304)
Tier D: 1305 / 1243     = 1.04995881… → 1.049959      (reference 1.049879)
```

Three of four divisions are wrong in the *mantissa*, not the rounding — the model printed 8-digit
intermediates that are themselves incorrect. Its task 2 is nonetheless 4 of 4, because the ×1.034
step does not depend on task 1.

**mistral** — 1 of 4. Two distinct causes, and they should not be conflated:

```
Tier A: 1.049465   wrong division      (reference 1.049304)
Tier B: 1.049329   TRUNCATION not rounding: 3914/3730 = 1.0493297…
                   → rounds to 1.049330, truncates to 1.049329
Tier C: 1.049299   wrong division      (reference 1.049304)
Tier D: 1.049879   ✓
```

**Tier B is a convention difference, not an arithmetic error.** The prompt says "to 6 decimal
places" without naming round-vs-truncate. A grader that scores it simply wrong is over-claiming; it
is recorded here as a miss against the round-half-up reference with the convention stated.

## `solar` — prose, not JSON

`solar regz.json` opens *"Here is the answer in English, with each task shown step by step."* and
answers in markdown tables. There is no JSON. Recorded `PROSE-NOT-JSON`, excluded from denominators,
**content not transcribed into a score**. Whether its arithmetic is right is unknown and this digest
does not guess.

## What this track cannot tell you

It checks whether the reference values appear in the model's text. A model that printed the right
figures alongside wrong reasoning would score 9. Task 1 also asks for a *consistency judgment* about
the four factors and the stated 4.9 %, which is prose and is not scored here.
