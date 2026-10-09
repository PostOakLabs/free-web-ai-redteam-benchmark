# Track D — the calibration wave

**`red1`** = all 16 models reviewing **RUNSHEET-34 Block 01** (BoomTile), the exemplar baked into
`J-ISSUE-REDTEAM-V1` and declared **known-imperfect**.
**`red3`** = all 16 models reviewing **RUNSHEET-42 Block 08** (Niagara), the exemplar baked into
`J-EPISODE-REDTEAM-V3` and declared **known-sound-with-known-gaps**.

**32 reviews of 2 blocks. This is the first inter-model consistency instrument the estate owns.**
As-of 2026-09-09T14:11:04Z.

---

## ⛔ Scope, stated before any number

- **These waves measure reviewer calibration, not corpus quality.** Every model reviewed the block
  that is baked into the prompt it was given. Nothing here is evidence about the episodes.
- **`direction_check` is OUT OF SCOPE.** One block gives no direction spread to compare against.
  The column is absent, not blank-and-unexplained.
- **The topic-anchor fabrication probe does not apply** — these families carry no recalled quotes.
- **Contradiction detection elsewhere in this digest is numeric-only: a direction reversal would
  pass silently.**

## A verdict-parsing defect that inverted the first table

`"SOUND-WITH-RESERVATIONS".startswith("SOUND")` is true. A shortest-enum-first scan collapsed every
reserved verdict into `SOUND`, and the first Track-D table reported **15 of 16 bare SOUND on red1**
— a corpus-wide miscalibration that does not exist. Longest-enum-first matching gives the real
figure: **15 of 16 SOUND-WITH-RESERVATIONS**. The commission's own predictions then matched exactly,
which is how the fix was confirmed rather than assumed.

## red1 — BoomTile, known-imperfect

| verdict | models |
|---|---|
| SOUND-WITH-RESERVATIONS | 15 |
| SUSPECT | 1 (longcat) |
| bare SOUND | **0** |

**No model returned bare SOUND on a block the prompt declares imperfect.** Objection counts run
0–6; yuanbao leads with 6 (4 major), kimi has 3 all-major.

**Schema anomaly, 1 — `minimax 2.7`:** verdict `SOUND-WITH-RESERVATIONS` with **zero objections**.
A reserved verdict whose reservation list is empty is inconsistent with its own output. Predicted by
the commission and confirmed here.

Most-attacked claim tokens: `layer`, `hypothesis`, `adjustment`, `chosen_intervention`, `routing`,
`post_state`, `complete`, `reported` — the convergence lands on `post_state` and the layer-adjustment
hypothesis, which are the two weaknesses `J-v1`'s BUILD NOTE names.

## red3 — Niagara, known-sound

| verdict | models |
|---|---|
| SOUND-WITH-RESERVATIONS | 9 |
| SOUND | 6 |
| NOT GRADABLE | 1 (solar) |

**Bare SOUND — 5 models: `gemini`, `grok`, `meta`, `minimax 2.7`, `qwen`.**

J-v3's BUILD NOTE declares Block 08 known-sound **with known gaps** and states that a reviewer
returning bare SOUND with no objections is miscalibrated. Applying the prompt's own definition,
those five are **MISCALIBRATED** — by the prompt's standard, not this digest's opinion. The
commission flagged exactly these five as "look bare, verify before asserting"; verified.

**Schema anomaly, 1 — `longcat`:** verdict `SOUND` while listing 2 objections. Also predicted.

Most-attacked claim tokens: `thread`, `clock`, `rationale`, `performance`, `target`, `state`,
`frequency`, `hardware`.

## What the two waves say together

| | red1 (imperfect block) | red3 (sound block) |
|---|---|---|
| bare SOUND | 0 of 16 | **5 of 15** |
| reserved or worse | 16 of 16 | 10 of 15 |

**The panel discriminates.** Given a block with real defects, nobody waved it through; given a sound
block, a third stopped looking. That is the correct direction — a reviewer that flags everything is
as useless as one that flags nothing — but bare SOUND on a block whose own prompt names its gaps is
still a miss.

`minimax 2.7` is the only model anomalous on **both** waves: empty reservations on red1, bare SOUND
on red3. It is the one model whose verdicts do not track its own objection lists in either
direction.

## Calibration columns filled

`redteam/TALLY-34.md` and `redteam/TALLY-42.md` now carry a generated calibration block between
`<!-- D5-CALIBRATION-BEGIN -->` / `<!-- D5-CALIBRATION-END -->`, written by
`digest/_verify/d5tally.py` — tooling, not hand-edited prose, and idempotent on re-run so G4 holds.
