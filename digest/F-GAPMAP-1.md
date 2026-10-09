# F-GAPMAP-1 — F-v1 merge vs F-v2 bar (2026-09-04)

Source: `diagnosis-library.md` (11 F-files, 9 models + m3 fragments + mimo
prose; self-labeled DRAFT SCAFFOLDING) graded against
`prompts/F-DIAGNOSIS-LIBRARY.md` (F-v2: 10 symptoms, ordered trees,
discriminating experiments, recalled-frequency + recall_confidence, era
notes). Judgment sorts and grades; every content line below is lifted
verbatim with model attribution — no engineering content added.

## 1. Crosswalk: 6 v1 classes → 10 v2 symptoms

| # | v2 symptom | v1 source | Verdict |
|---|---|---|---|
| 1 | congestion DRCs, clean placement density | FAIL_CONGESTION shapes 1–3 + causes 1–5 | PARTIAL |
| 2 | setup violations after CTS | FAIL_TIMING-setup shape 4 + causes 4–5 | PARTIAL |
| 3 | hold violations after CTS | FAIL_TIMING-hold shapes 3–5 + causes 1,4 | PARTIAL |
| 4 | IR-drop-induced timing failure | FAIL_IR_DROP shape 5 + cause 10; setup cause 7 | PARTIAL |
| 5 | clock skew / CTS divergence | FAIL_CTS shapes 1,3,6 + causes 1–3,11 | PARTIAL |
| 6 | LVS: missing/shorted/open nets | NONE (no LVS class in v1) | RE-ELICIT |
| 7 | LVS: wrong sizes/extra devices | NONE | RE-ELICIT |
| 8 | antenna violations at signoff | FAIL_DRC shape 4 + cause 3 | PARTIAL |
| 9 | DRT hotspots after clean GRT | FAIL_DRC shapes 3,6 + cause 1 | PARTIAL |
| 10 | unroutable placement | FAIL_CONGESTION shape 6 + causes 1,8 | PARTIAL |

## 2. Per-symptom field verdicts (present / absent vs the v2 bar)

Scoring key per field: ✅ present at bar · ◐ present but wrong shape ·
❌ absent. Systematic result: **shapes/checks/traps strong; ordered
trees, frequencies, and era notes absent everywhere → 8 PARTIAL, 2
RE-ELICIT, 0 PROMOTABLE.**

- **S1 congestion-clean-density:** shapes ✅ ("modest placement
  utilization can carry severe routing demand" — chatgpt/gemini/meta/qwen);
  checks ✅◐ (10 causes with costs, but union-ordered not tree-ordered);
  experiments ◐ (sharpest: grok "route only non-clock nets first — if
  congestion collapses…" — decision-grade but not rules_in/out form);
  frequencies ❌ (only model-count consensus); trap ✅ (9/9 headline trap);
  era ❌. Worst line: none — thinnest claim is grok's single-model
  wirelength-tail shape. Dispute to keep: floorplan-first (6 models) vs
  cheapest-experiment-first (chatgpt, gemini).
- **S2 setup-after-CTS:** shapes ✅ (4 axes incl. "tight unimodal cluster
  → go straight to SDC" — minimax 2.7); checks ✅◐ (10 causes);
  experiments ◐ (grok idealization test; chatgpt skew-signature read);
  frequencies ❌; trap ✅ (5 traps, chatgpt sizing-everything best);
  era ◐ (one threshold with 28nm/7nm split — meta PBA/derate). Content
  hole (merge's own finding): wall-means-constraint vs wall-means-derate
  discriminator missing — Alice question.
- **S3 hold-after-CTS:** shapes ✅ (6 shapes, all short-path/clock-signature
  reads); checks ✅◐ (10 causes); experiments ◐ (what-if delay insertion;
  CRPR re-run); frequencies ❌; trap ✅ (yuanbao "Hold fix belongs on the
  DATA path only" — most operational line in v1); era ◐ (meta hold
  uncertainty 50–100ps@28nm/30–60ps@7nm only). Dispute to keep: hold
  uncertainty sign convention (deepseek outlier, flagged).
- **S4 IR-timing:** shapes ✅ (5, incl. mobility discriminator);
  checks ✅◐ (10 causes); experiments ✅◐ closest to bar (chatgpt
  move-with-switching-group + recover-at-nominal-voltage — nearest to
  rules_in/out form in the corpus); frequencies ❌; trap ✅; era ◐
  (yuanbao ≤7nm ≤3% budget caveat only). Lowest-confidence class
  (0.82–0.94) — stated in merge, keep the caveat.
- **S5 CTS-divergence:** shapes ✅ (7); checks ✅◐ (12 causes, richest
  table); experiments ◐; frequencies ❌; trap ✅ (yuanbao "80% of CTS
  failures are placement or constraint issues" — keep verbatim);
  era ❌. Framing dispute (roll-back-first vs tune-knobs) is Alice's
  ruling, not re-elicitation material.
- **S8 antenna:** shapes ◐ (one DRC shape + cause 3 with chatgpt's
  layer-break test); checks ◐; experiments ❌ as standalone tree;
  frequencies ❌; trap ✅ (deepseek single-diode cheap win);
  era ❌. PARTIAL-lean (thinnest of the 8 — one shape, one cause).
- **S9 DRT-after-clean-GRT:** shapes ✅ (grok >70%-in-top-10-gcells test);
  checks ✅ (cause 1 + congestion overlay); experiments ◐; frequencies ❌;
  trap ✅ (marker-by-marker repair); era ❌.
- **S10 unroutable:** shapes ◐ (asymptote/"unroutable" report + cause 8
  aspect ratio); checks ◐; experiments ❌ (no decisive unroutability test
  stated); frequencies ❌; trap ✅ (router-effort trap); era ❌.
  PARTIAL-lean with S8.

## 3. Promotable subset (v2-shaped objects, verbatim + attributed)

Provenance on every object: `free-model-harvest/F/2026-08-31` (per the
merge's integrity header). Absent v2 fields marked `ABSENT — re-elicit`,
never filled. (Full objects with all lifted lines: S1–S5, S8–S10 as
specified below — first_checks drawn from each class's cheapest-check
rows in listed order with why_first QUOTING the merge's ordering
disputes where they exist; discriminating_experiments quoting the
sharpest checks above; recalled_frequency/recall_confidence/node_era_note
marked ABSENT except the three scattered era fragments, each quoted with
its model; classic_trap quoting the best phrasing per class with model.)

- **S1:** first_checks ← congestion causes 1 (macro overlay, min–hrs),
  2 (density screen, minutes), 7 (layer overflow, minutes) — order
  DISPUTED in merge (floorplan-first vs cheapest-first), both orders
  preserved with attribution; experiments ← grok non-clock-nets-first,
  meta PG-visibility toggle; trap ← chatgpt headline + yuanbao
  router-effort; era ABSENT.
- **S2:** first_checks ← cause 1 (constraint audit, minutes), cause 4
  skew decomposition (minutes), yuanbao logic/net split report
  (minutes); experiments ← grok idealization, meta ideal-clock recovery;
  trap ← chatgpt sizing-everything + minimax-2.7 wrong-layer-cost;
  era ← meta PBA/derate 28-vs-7nm fragment only.
- **S3:** first_checks ← cause 1 skew decomposition, cause 6 min-delay
  audit (minutes), cause 5 CRPR re-run (minutes); experiments ←
  controlled delay-insertion what-if, gated/ungated delta (deepseek);
  trap ← yuanbao DATA-path-only + meta sequencing; era ← meta hold
  uncertainty fragment only.
- **S4:** first_checks ← hotspot-mobility test (chatgpt), static-vs-
  dynamic scenario compare, decap-proximity map; experiments ← move-
  with-switching-group, recover-at-nominal-voltage; trap ← yuanbao
  static-remedy + grok blanket-decap; era ← yuanbao ≤7nm budget fragment
  only; confidence caveat kept.
- **S5:** first_checks ← minimax-2.7 stale-CTS check (minutes), sink
  topology inspect, ICG-boundary grouping; experiments ← grok
  move-the-ICG, derate-reduction re-run; trap ← yuanbao placement-first
  + qwen tighten-target; era ABSENT; framing dispute preserved.
- **S8:** first_checks ← antenna-marker filter + layer-break test
  (chatgpt, minutes); experiments ← diode-protection clear-test;
  trap ← deepseek single-diode; all else ABSENT (thinnest object).
- **S9:** first_checks ← grok >70% overlay test (minutes), layer map;
  experiments ← congestion-overlay collapse check; trap ←
  marker-by-marker; era ABSENT.
- **S10:** first_checks ← asymptote-across-iterations read, aspect-ratio
  + corridor check; experiments ABSENT (no decisive test in merge);
  trap ← router-effort; era ABSENT.

## 4. RE-ELICIT list (paste-ready for the operator's loop)

- **S6 LVS missing/shorted/open:** no v1 source. Paste `prompts/F-DIAGNOSIS-LIBRARY.md`
  with this symptom line first: "Symptom 6 only: LVS mismatch — missing,
  shorted, or open nets. Full ordered tree per the file's object spec."
- **S7 LVS wrong sizes/extra devices:** no v1 source. Same file:
  "Symptom 7 only: LVS mismatch — wrong device sizes or extra devices…"
- Optional targeted reruns (PARTIAL-lean fields, not new symptoms):
  S8 full tree, S10 decisive unroutability experiment, S2 wall-meaning
  discriminator, S3 uncertainty sign convention — one symptom per paste
  per the file's spec.

## 5. Honest closer (what a merge cannot establish, however sharp)

Frequencies (no model was asked; counts are consensus, not recall);
node-era deltas (three fragments do not make a practice map); ordering
disputes (floorplan-first vs cheapest-first, antenna-vs-congestion
precondition, CTS framing — practitioner rulings for Alice, and the most
valuable holes to re-elicit around); single-model thin claims (grok
wirelength tail, gemini clock-power bloat, deepseek 200µm rule);
porous-boundary material (yuanbao FPGA SLR — already excluded in merge,
do not promote). Nothing above graduates without Alice's rewriting or a
reproduced run — per the merge header, promotion-ready content would
enter as `synthetic-fixture`, never as data.
