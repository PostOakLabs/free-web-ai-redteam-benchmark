# DIGEST COMMISSION — DAY 5 — 80 responses, 5 families, 16 models — Day-4 discipline plus its lessons

Commissioned by the Flash re-audit session on the operator's instruction, 2026-09-09, for the Opus digest
session. Day 4's digest passed independent verification end-to-end (its vet recipe §0–§4 all
green); this commission reruns that discipline on a structurally different day and fixes what the
Day-4 pass exposed. Every number below was verified from disk by the commissioning session at
2026-09-09 ~02:30 UTC. **Census is asserted, not assumed — G1 applies to you as it did to Day 3.**

## 0. Verified census (re-assert before anything else)

`Web Model Tasks/Day 5/` holds **81 files: 80 JSON responses + 1 stray**.

- **5 families × 16 models, no gaps**: `e` (PROMPT-E-CALCULATIONS, HW-safety wave) · `regz`
  (C1-REGZ-FACTOR) · `strings` (C2-JCS-STRINGS) · `red1` (J-ISSUE-REDTEAM-V1 verdicts) ·
  `red3` (J-EPISODE-REDTEAM-V3 verdicts). The 15 legacy models each filed all 5.
- **`minara` (3 files: e, red1, regz) and `minaria` (2 files: red3, strings) are ONE new model
  collected under two spellings** — the yuanbao-power class of collection defect. Do NOT rename.
  Digest as a single model provisionally keyed `minara` with dual-spelling provenance; the operator confirms
  the canonical name at checkoff.
- **Stray, not Day-5 content**: `draft 3 and 4 prompt.md` (Hy4 seal-retest dispatch drafts). Exclude
  from census, leave in place untouched, flag for the operator to relocate.
- **Known parse defects going in** (found by commissioning scan, confirm on load): `chatgpt red1`,
  `chatgpt red3`, `solar red3` fail plain JSON parse — unescaped inner quotes, the chatgpt-jcs class
  from Day 2. Use the salvage path, record parse classes, never skip a file (G1 halts instead).

## 1. Hard gates (identical to Day 4 — they all passed live inspection there)

**G1** census: assert loaded + halted = 80, skipped = 0; unknown family or unknown model ⇒ exit
nonzero with `G1 STOP`, never a skip. Include the adversarial check (plant a bad-family file,
expect the halt, remove it, expect 80 again).
**G2** no verdict through a pipe: full output → file, `grep` the file, true `$?` before any filter.
**G3** tooling first: `digest/_verify/d5*.py` + `MANIFEST-D5.sha256` generated before the digest
run; no post-hoc loaders.
**G4** determinism: full re-run regenerates every derived JSON byte-identically; hash before/after.
**G5** vet recipe written LAST, every expected value produced in-session and as-of-stamped, no
placeholder sections, unique document numbers (Day 4 shipped two files numbered 06 — do not repeat).

## 2. Four digest tracks — three have deterministic ground truth; exploit that

**Track A — `regz` (16 files): pure arithmetic, zero heuristics.** Read the tasks from
`prompts/C1-REGZ-FACTOR.md`, recompute every tier's exact values in a reference script, grade
said-vs-computed per task per model (the `irb.py` pattern: quote the model's figure beside the
reference figure). Output: exactness table, first-error-step per model. No overlap tunables exist
on this track — a model is right or wrong at 6 decimals.

**Track B — `strings` (16 files): JCS conformance against the estate canonicalizer.** Grade every
`case` by running the reference `jcs.py` (it already passes its 12 RFC 8785 self-asserts) and
comparing the model's `jcs` output and `rules_applied`. Score = cases correct; separately flag
right-answer-wrong-rule explanations — a lucky canonicalization with a false rule statement is a
finding, not a pass.

**Track C — `e` (16 files): HW-safety calculations.** Recompute against the consensus formulas in
`digest/hw-calc-formulas.md` and the worked vectors in `hw-calc-vectors.md`. Standards that are
paywalled keep their `NEEDS-RETRIEVAL` honesty — grade only what the free primary text supports
(JEDEC JESD85 is free; ISO 26262 clauses are not). Cross-reference
`HW-ASSURANCE-SCOPING-2026-08-31.md` and note contradictions (model vs retrieved text = model wrong
unless it cites better).

**Track D — `red1`/`red3` (16+16): verdict harvest into the TALLYs, calibration wave.** Verified
block identities: **red1 reviewed RUNSHEET-34 Block 01** (BoomTile 20k congestion DRCs — the
exemplar baked into J-v1 itself) and **red3 reviewed RUNSHEET-42 Block 08** (Niagara thread-rich —
the exemplar baked into J-v3, ⚠-marked). These are calibration waves, and the digest should say so
on every page. Deliverables:
- Fill the calibration column of `TALLY-34.md` and `TALLY-42.md` (verdict, fatal/major counts,
  note), one row per model — via `mktally.py`-style tooling, not by hand-editing prose.
- Salvage the 3 parse-fail files with recorded parse classes; hand-confirm anything you report as a
  model defect (estate rule: no failure is reported unless hand-confirmed).
- Flag schema anomalies as findings: SOUND-with-objections (longcat red3), SOUND-WITH-RESERVATIONS
  with zero objections (minimax 2.7 red1) — verdicts inconsistent with their own objection lists.
- **Cross-model agreement matrix**: on identical inputs, which fields did models attack, where do
  objections converge, and who returned bare `SOUND` on a block the prompt itself declares
  known-sound-with-known-gaps (J-v3's BUILD NOTE calls bare-SOUND miscalibration — apply it; grok,
  gemini, meta, minimax 2.7, qwen look bare on red3, verify before asserting). This matrix is the
  first inter-model consistency instrument the estate owns — RUNSHEET-42's operator notes
  anticipated exactly this use.
- `direction_check` is out of scope on single-block waves — say so rather than leaving a blank
  column unexplained.

## 3. Required improvements over Day 4 (not optional — each traces to a verified Day-4 finding)

1. **Retire the T-collision.** Day 4's quote tiers (T0–T4) collide with the harvest rubric's
   T1/T2/T3 (keeper/salvage/discard, `FREE-MODEL-HARVEST-2026-08-31.md` §log) and with survey triage
   items. Any tiered output in Day 5 tooling uses **Q-names** (`Q1-verbatim`, `Q2-paraphrase`, …).
2. **Floor-band shipped in the summary.** Any overlap-graded output publishes its 0.5/0.6/0.7 tier
   tally inline in `grade-summary.txt`, not only in the vet recipe's self-criticism. (Day 4: 13 of
   272 entries moved; its only contradiction lived 0.015 above the floor.)
3. **Numeric-only detection disclosed on every page that uses it.** Any summary whose contradiction
   detection is numeric says "a direction reversal would pass silently" in the summary itself.
4. **Topic-anchor fabrication probe as a standard column**: for every not-found quote, whether its
   distinctive content words exist in the source (Day 4's fabricators scored high — "trace cache"
   ×35 — with invented sentences).
5. **Decline table first-class per family** — which models declined all/some, stated so "no
   findings against them" is never readable as "clean" (Day 4: 9 of 16 models declined everything
   including the strongest Day-2 performer).
6. **Per-model machine-readable calibration file** (`d5run/d5permodel.json`): per-model × per-track
   results (regz exactness, strings conformance, e accuracy, redteam verdicts + calibration class).
   This is the AINumbers feed — the richest onboarding wave yet (16 models on 5 mechanically
   gradable instruments), and it should be usable as a research row without re-parsing prose.
7. **Manifest backfill while you are in the ledger**: append RUN-MANIFEST rows for Day 4 (73) and
   Day 5 (80), dated honestly, including the minara/minaria dual spelling. Survey triage T2 closes
   with this digest.
8. **Vet recipe includes its own floor-sweep and adversarial-census results as sections**, with
   expected values run in-session (Day 4's recipe caught its own from-memory defect — keep that bar).

## 4. Deliverables

`Web Model Tasks/Day 5/_digest/00-corpus-and-harness.md` + one digest per track + a cross-model
calibration note + the vet recipe; `digest/_verify/d5{load,grade_*,xcheck}.py` + `MANIFEST-D5.sha256`
+ `d5run/` derived JSONs; TALLY-34/42 calibration columns filled; RUN-MANIFEST Day-4/Day-5 rows.
**Read-only on the corpus**: no renames (minara/minaria stay as collected), no deletions (the stray
md stays), no commits to either estate unless the operator asks.

## 5. Note from the commissioning session

`PROMPT-B-BROWSER` and `PROMPT-C-SOURCES` re-runs with the new AIs are **deferred** by separate
recommendation (queue discipline; B is web-access-gated and operator-gated; C's existing outputs are not
yet digested). Do not fold them into this digest.
