# TALLYCODES-VET-1 — VERDICT (Flash station) — G6.6(c) vet of `digest/_verify/tallycodes.py`

Vet performed 2026-09-09 against `TALLYCODES-VET-1.md` §4–§8, under G6.6(c) as settled: this was a
rule-reimplementation vet, divergences adjudicated against the primary (the TALLY prose tables and
the prompts' own enums), and the tool's own path exercised rather than reimplemented wherever
possible.

## 1. What passed

- **§4:** manifest `tallycodes.py: OK`, sha256 prefix **`7f6c5033`** ✓; exit 0 ✓; **G6.1 fixtures
  22/22 pass** ✓; **exactly 1 DIVERGE** — `SOUND-WITH-RESERVATIONS` pinned `S-W-RES` vs naive
  `SOUND`, i.e. the Day-5 prefix collision reproduced on demand ✓ (zero DIVERGE lines would have
  meant a broken differential, per the recipe).
- **§5 back-test, independently re-derived from `d5corpus.json`** (raw model responses, not the old
  grader's output): red1 = **15 `S-W-RES` + 1 `SUSPECT`**, calibration **15 consistent + 1
  reservations-without-objections**; red3 = **9 `S-W-RES` + 6 `SOUND` + 1 `NOT-GRADABLE`**,
  calibration **9 consistent + 5 `MISCALIBRATED-bare-SOUND` + 1 `SOUND-with-objections`**. Zero
  `UNCODED` across 32. Matches the settled Day-5 values and the recipe's table exactly.
- **Sheet separation** holds (a paper-side IMPLAUS cannot code on the record sheet, and vice versa).
- **No-substring credit** holds: `unsound`, `soundness`, `measurements`, `assertion failed` all
  return UNCODED (boundary regex rejects token-internal matches).
- **`UNCODED` propagates** through `calibration()` (fixture and probe agree).
- **W5 audited:** exactly one cross-code prefix pair exists in any table — the `SOUND`/
  `SOUND-WITH-RESERVATIONS` pair the longest-first rule was built for. The precondition holds today.
- **W2 confirmed as documented limitation, not a defect:** a fatal objection labelled `minor` is
  counted as labelled; the module cannot do otherwise without a rubric that does not exist.
- **`block_class = "unknown"` guard is real:** bare `SOUND` on an unknown block returns
  `consistent` — the DO-254-DAL circularity does not recur.

## 2. The named list — codes it gets wrong (run stays gated on these)

Each was probed with an input the 22 fixtures do not cover, and adjudicated against the primary.
The primary is silent on all four, and the codebook's own rule 2 (`UNCODED` is a value) therefore
demands UNCODED — not the confident wrong code it returns.

| # | probe | returns | should be | fix |
|---|---|---|---|---|
| 1 | `code_verdict("not sound", "34")` | **`SOUND`** | UNCODED (or negation-aliased) | negator guard: no code when a negator (`not`, `never`, `n't`) precedes the alias in the cell |
| 2 | `code_field("evid", "not measured")` | **`MEAS`** | `ASSERT` | add the negated alias — the module already proves the pattern (`"does not hold"` → BREAKS for mech) and currently assigns synonyms of one concept to opposite codes (`"unmeasured"` → ASSERT, `"not measured"` → MEAS) |
| 3 | `code_field("dir", "does not match the paper")` | **`MATCHES`** | UNCODED or REVERSAL-aliased | same negation class as 2; note the inconsistency: `"does not match — reads like a transplant"` → TRANSPLANT (longest-alias luck), so the same semantic codes two ways |
| 4 | `calibration("SOUND", 0, "Known-Sound")` (also `"KNOWN-SOUND"`, `" known-sound "`, `None`) | **`consistent`** | `MISCALIBRATED-bare-SOUND` or a loud error | normalize `block_class` (casefold/strip) and raise on values outside the three-value contract — silent `consistent` masks the calibration finding entirely |

1–3 are one class: the positive token matched inside a negated phrase — the no-substring-credit
defect's negation variant, which the fixture list does not yet cover. 4 is a normalization gap in
the one function whose misfire masks a finding rather than producing one.

**Required to lift the gate:** the four fixes, each with a G6.1 fixture carrying the exact probe
above as a known-wrong input, re-run of §4 and §5, and unchanged back-test values.

## 3. §7 weaknesses — adjudicated

W1 confirmed by construction (22 self-chosen fixtures; the negation class above is the proof). W2
confirmed as designed. W3 confirmed and escalated into named defect 4. W4 confirmed live: bare
`IMPLAUSIBLE`, bare `implausible`, and `n/a` all return UNCODED today — in the 76-block run each
such row is a codebook-gap finding to fix by alias addition, not noise to tune away. W5 precondition
holds; re-audit the prefix property whenever an enum gains a member.

## 4. Verdict

**Named list of codes it gets wrong — the run stays gated** per §8's own rule. The gate is cheap to
lift: four one-line-scale fixes plus four fixtures, then a §4/§5 re-run. Everything else — enums,
sheet split, longest-first, no-substring, UNCODED discipline, differential, back-test — verified
and, once the four land, the codebook is the specification and the prose tables in `TALLY-34`/
`TALLY-42` become its documentation.
