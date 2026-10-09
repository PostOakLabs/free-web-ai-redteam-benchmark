## Skeptical Review of Draft Episode

### CRITICAL — Misattribution of the core technical finding

The `chosen_intervention` and `direct_quote` both attribute the layer-adjustment fix to **eder-matheus** dated **2024-11-14**. This is wrong on both counts. The text

> "We are investigating with this design and a few others related to megaboom, and we could finish GRT by changing the routing layer adjustments from 0.45 to 0.2. I guess the 0.45 value came from other designs in asap7 that uses it, but 0.2 for megaboom seems more reasonable. We also changed the number of congestion iterations to 35 to complete BoomTile."

appears in **jeffng-or's comment dated November 1, 2024**. eder-matheus's only comment in the thread is dated **November 15** and concerns documentation cross-linking between OR and ORFS — it says nothing about layer adjustment, iterations, or the fix. The `by` field should read `"jeffng-or"`, and the `date` should read `"2024-11-01"`.

This error propagates into the `gaps` list's final bullet ("We (eder-matheus) note..."), which is also garbled.

---

### CRITICAL — Hypothesis mischaracterises the iteration-count finding

The draft's hypothesis states: *"the default 30 congestion iterations were also insufficient."* The thread tells the opposite story. maliberty asked whether increasing iterations helped; **jeffng-or tested it and answered "No."** Thirty iterations at 0.45 layer adjustment did not fix the problem. The bump to 35 iterations was reported by jeffng-or only as part of the *combined* intervention (layer adjustment 0.2 + 35 iterations). The draft should state that iteration count alone was insufficient and that the 35-iteration setting only contributed when paired with the reduced layer adjustment. As written, the hypothesis falsely implies a standalone causal role for the iteration count.

---

### MODERATE — "Stale" ≠ "closed"

The `gaps` list says: *"The issue was closed automatically as not_planned/Stale in 2026."* The thread evidence shows only that GitHub Actions **marked it stale** on 2026-05-25, warning it would be closed in 21 days if no further activity occurred. The record does not show the issue actually being closed. The gap should say "marked stale" not "closed automatically as not_planned."

---

### MODERATE — Unsupported addition in observation

The observation says congestion appears *"around the macro."* The original report text says only *"a lot of space especially at the top of the design."* The placement-density screenshot alt text says "placement\_density" and the congestion screenshot says "routing\_congestion" — neither alt text or body text mentions macro-proximate congestion in the initial report. The later global-placement screenshot (maliberty's comment) may show macro-adjacent congestion but that is a different design stage. The observation should either drop "around the macro" or explicitly source it to the later comment.

---

### MODERATE — Title deviates from source

The issue title is **"Megaboom: 20k routing congestion DRCs with just 0.24 placement density."** The draft prepends "BoomTile/" and changes "just" to "only." While BoomTile is the design name used in the body, the title should match the source verbatim, with BoomTile disambiguation in `prior_state`.

---

### MINOR — "Megaboom-derived" is not stated

The `prior_state` calls BoomTile "Megaboom-derived." The thread says the issue is "related to megaboom" (jeffng-or, Nov 1) and the issue title names "Megaboom," but no explicit derivation relationship is stated. This is a plausible inference but should be flagged as one.

---

### MINOR — Reproduction contributor omitted

oharboe (Øyvind Harboe, @2798822) did substantial work: confirming the issue independently, creating `make global_place_issue` for reproduction, and providing a tarball. maliberty's initial question about iterations was directed at this contributor's confirmation. The episode silently absorbs all of this.

---

### MINOR — Layer-adjustment semantics not captured

The thread includes a technically important explanation from eder-matheus (quoted by jeffng-or on Nov 14): *"we reduce the resources that the global router have to route the design… Using higher values would produce less congested areas in DRT, but values too high can make GRT to not complete."* This is the mechanistic explanation of why 0.45 → 0.2 works. The draft's hypothesis says the 0.45 was "too aggressive" but never explains the mechanism (higher value = more resource reduction = stricter constraint). A reader unfamiliar with ORFS would not understand why lowering the number fixes congestion. This explanation exists in the thread and should be fronted in the hypothesis.

---

### MINOR — Confidence too high

Given the misattribution, the lack of post-fix DRC measurement, the uncertain closure status, and the absence of a PR, a confidence of **0.8** is generous. I would place it at **0.55–0.65** until the attribution is corrected and the fix is confirmed merged.

---

### Summary of required corrections

| Field | Current | Should be |
|---|---|---|
| `direct_quote.by` | `"eder-matheus"` | `"jeffng-or"` |
| `direct_quote.date` | `"2024-11-14"` | `"2024-11-01"` |
| `hypothesis` | "default 30 congestion iterations were also insufficient" | "default 30 iterations were tested and did not resolve the issue; they only contributed in combination with the layer-adjustment change" |
| `gaps[1]` | "closed automatically as not_planned/Stale" | "marked stale on 2026-05-25; actual closure not confirmed in the record" |
| `observation` | "around the macro" | remove or source to maliberty's later comment |
| `title` | "BoomTile/Megaboom: …only…" | match source: "Megaboom: …just…" |
| `chosen_intervention` | "Per eder-matheus (MEMBER)" | "Per jeffng-or" |
| `confidence` | 0.8 | 0.6 (after corrections, 0.75) |