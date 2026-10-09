# Cross-model calibration — the per-model feed

`digest/_verify/d5run/d5permodel.json` — **16 models × 5 mechanically gradable instruments**, the
richest onboarding wave the estate has collected. Usable as a research row without re-parsing prose.
As-of 2026-09-09T14:11:04Z.

---

## Shape

```json
"<model>": {
  "regz":    {"t1": 4, "t2": 4, "t3_factor": true, "score": 9, "max": 9, "parse": "clean"},
  "strings": {"correct": 4, "cases_seen": 4, "right_answer_wrong_rule": [], "parse": "…"},
  "e":       {"entries": 12, "classified": 10, "shape_ok": 9, "needs_retrieval": 5, "families": […]},
  "red1":    {"verdict": "SOUND-WITH-RESERVATIONS", "objections": 3, "fatal": 0, "major": 1,
              "calibration": "consistent", "claims_attacked": […]},
  "red3":    {"…"},
  "dual_spelled": false,
  "spellings_as_collected": ["yuanbao"]
}
```

Every track carries its own `gradable` flag, so a consumer can tell a NOT-GRADABLE cell from a zero.
**Three cells are NOT GRADABLE and none is a decline** (`05-decline-and-coverage.md` §3).

## What the feed shows across tracks

**Track A separates almost nobody.** 13 of 15 exact at 9/9. As a discriminator between models, the
regz task is nearly saturated — useful as a floor test, not as a ranking instrument.

**Track B separates sharply.** 1 to 4 of 4, driven almost entirely by case 3 (ES6 number
serialization), which halves the field. If one instrument were kept for model selection, this is it.

**Track A and Track B rank differently.** `gemini` and `qwen` are 9/9 on arithmetic and 2/4 on
canonicalization; `mistral` is weak on both. **Exact arithmetic does not predict specification
conformance**, which is the single most useful thing this wave says about model selection.

**Track D is orthogonal to both.** `grok` and `meta` are strong on A and B and are two of the five
bare-SOUND misses on red3. Reviewing well and computing well are separate capabilities, and this
wave is the first time the estate can show that rather than assert it.

## Consuming it for TALLY-42

`RUNSHEET-42`'s operator notes ask that `direction_check` be graded against each model's own prior
recall. **This wave cannot serve that** — red3 is a single-block calibration run, so there is no
direction spread. The Day-4 feed (`d4permodel.json`) is the right source for that cross-grade;
this one supplies calibration class instead.

**Suggested join:** a model's `red3.calibration` here against its Day-4 per-paper verbatim rate. A
model that scored high verbatim recall on Niagara in Day 4 and returned bare SOUND on the Niagara
block here is not failing to know the paper — it is failing to review.

## Provenance carried in the feed

`minara` holds `dual_spelled: true` and `spellings_as_collected: ["minara", "minaria"]`. Any
consumer that keys on the as-collected filename will see two models; the feed is the record that
says otherwise. **The files were not renamed** and the operator confirms the canonical name at checkoff.

## Limits

- `e.shape_ok` is token-based. It does not certify a formula is correct, and an inverted metric
  passes (`02-e.md`).
- `regz.score` counts reference values present in the model's text, not the quality of its stated
  reasoning.
- `strings.correct` is out of 4; case 5 is ungradable by transport (`03-strings.md`).
- `red1`/`red3` are single-block calibration, not survey coverage.
