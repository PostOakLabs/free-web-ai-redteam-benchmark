## Principal Engineer Review: Incident Episode #6066

### Executive Summary
This draft conflates global routing congestion with detailed routing DRCs, misattributes causality between low density and congestion, and reports a confounded workaround as a validated fix while deferring the actual root cause. The 0.8 confidence score is unjustified given the complete absence of post-intervention metrics. The episode reads as a preliminary debugging log, not a curated incident record.

---

### 1. Factual Errors

**Error: "20k routing congestion DRCs"**
- **Location**: Title, Observation
- **Problem**: Global Routing (GRT) does not produce DRCs. DRC violations are a detailed-routing concept checked by the geometry router, not the global router. GRT produces congestion maps and overflow metrics.
- **Correction**: Replace with "20k global routing congestion violations" or "20k global routing overflow hotspots." If the 20k figure refers to post-detailed-route DRCs, the record must explicitly state that detailed routing was attempted and failed, which contradicts "failed GRT."

**Error: "BoomTile (Megaboom-derived) design in asap7"**
- **Location**: Prior_state
- **Problem**: ASAP7 is a predictive 7nm PDK, not a foundry node. Designs cannot be "in asap7" in a tapeout sense; they are *targeted to* or *implemented using* the ASAP7 PDK. This is imprecise language for a technical record.
- **Correction**: "BoomTile design targeted to the ASAP7 7nm PDK" or "implemented using ASAP7 standard cells."

---

### 2. Internal Inconsistencies

**Inconsistency: Low Density vs. Congestion Causality**
- **Location**: Prior_state, Hypothesis
- **Problem**: The record treats 0.24 placement density as a surprising factor for congestion ("only 0.24... yet the design failed GRT"). However, low density *reduces* congestion risk; high density causes it. The observation that congestion exists *despite* low density should immediately invalidate density as a root cause and point to algorithmic or macro-placement issues (which the record later mentions but defers).
- **Correction**: The narrative should state: "Congestion at low density indicates a non-density-related root cause, such as the suspected macro-routing loop (issue #5971)."

**Inconsistency: Success Criteria**
- **Location**: Post_state, Gaps
- **Problem**: The original problem is quantified as "20k routing congestion DRCs," but success is defined as "GRT was reported to complete." GRT completion is a binary status, not a metric. The record admits no post-fix DRC/congestion count was taken, yet claims the design "complete BoomTile."
- **Correction**: Success must be measured by reduction in the original violation metric. If GRT completion was the goal, the problem statement should be "GRT failed to converge," not "20k DRCs."

**Inconsistency: Closure Status vs. Claimed Fix**
- **Location**: Gaps
- **Problem**: The record claims the fix "could finish GRT" but also notes the issue was "closed automatically as not_planned/Stale in 2026." If the fix was effective, why was it closed as stale? This suggests the fix was never merged, validated, or accepted.
- **Correction**: Clarify disposition: "The parameter change was proposed but never merged; the issue was closed due to inactivity."

---

### 3. Technical Implausibilities

**Implausibility: Confounded Intervention**
- **Location**: Chosen_intervention
- **Problem**: Two parameters are changed simultaneously (layer adjustment 0.45→0.2 AND iterations 30→35). This makes it impossible to determine which change was effective, whether both were necessary, or if either was irrelevant. This is not a controlled experiment.
- **Correction**: Report results for each parameter change independently, or use a factorial design. At minimum, state: "The individual contribution of each parameter change is unknown."

**Implausibility: Marginal Iteration Increase**
- **Location**: Candidates_considered, Chosen_intervention
- **Problem**: Increasing iterations from 30 to 35 is a 16% change. If 30 iterations were insufficient to resolve 20k violations, why would 35 be sufficient? This suggests either random tuning or that the iteration count was never the bottleneck.
- **Correction**: Provide convergence data: "At 30 iterations, congestion was X; at 35, congestion was Y." Or explain why 35 is a theoretical minimum (e.g., "35 iterations correspond to the diameter of the routing graph").

**Implausibility: Undefined Parameter Semantics**
- **Location**: Gaps
- **Problem**: The record admits the "exact meaning of a high vs low value [of routing-layer adjustment] only explained in prose." For a critical tuning parameter, this is unacceptable. Is 0.45 a multiplier on wire cost? A layer probability? An additive offset? Without a precise definition, the fix is not reproducible.
- **Correction**: Include the exact API documentation or code comment defining `set-global-routing-layer-adjustment`. Example: "Layer adjustment is a multiplicative factor on the cost of routing on lower metal layers; higher values discourage lower-layer usage."

**Implausibility: Root Cause Evasion**
- **Location**: Hypothesis, Gaps
- **Problem**: The record identifies a "global-route path 'looping around the macro' many times" as a suspected cause but explicitly defers it to issue #5971. If this is the true root cause, the parameter changes are merely workarounds that mask the symptom without fixing the disease.
- **Correction**: The title and hypothesis should be reframed: "Workaround: Parameter tuning masks macro-routing loop congestion (root cause deferred to #5971)."

---

### 4. Missing Information

The record lacks essential context for a curated incident:

1. **Design Metrics**: Cell count, die area, macro dimensions/count, target utilization. A 0.24 density on a 0.1 mm² design is trivial; on a 10 mm² design, it indicates a massive floorplanning issue.
2. **Congestion Map Data**: Exact coordinates, layer distribution, and severity histogram of the 20k violations. "Top of the die and around the macro" is insufficient.
3. **Sweep Results**: The record mentions parameters were "swept" but provides no data. What values were tested? What was the response surface?
4. **Runtime Data**: No before/after runtime for GRT. If the fix increased runtime 10×, that's a critical tradeoff.
5. **Reproducibility**: Was the fix scripted or manually applied? Is there a TCL snippet? The record mentions a GUI command (`run-me-BoomTile-asap7-base.sh gui`), suggesting manual intervention.
6. **Version Control**: The ORFS version is pinned, but the fix is a parameter change, not a code commit. Is this a tool bug or a user configuration error? The record doesn't clarify.

---

### 5. Corrected Version (What This Record Should Look Like)

**Title**: *BoomTile: Global routing congestion workaround via layer-adjustment tuning (root cause: macro-routing loop deferred to #5971)*

**Problem Statement**: BoomTile design (ASAP7 PDK, ~500k cells, 0.24 placement density) exhibited ~20k global routing congestion violations concentrated near the macro and die top. GRT failed to converge after 30 iterations.

**Root Cause**: Suspected global-route path looping around the macro (deferred to issue #5971). Low density rules out cell-level congestion; the issue is algorithmic.

**Intervention**: As a workaround, `set-global-routing-layer-adjustment` was reduced from 0.45 to 0.2 (a multiplicative cost factor on lower metal layers) and congestion iterations increased from 30 to 35. **Note: These changes were applied simultaneously; individual contributions are unvalidated.**

**Result**: GRT completed. Post-fix congestion count was **not measured**. Runtime increased from X to Y seconds.

**Disposition**: **Not merged.** Issue closed as stale. The workaround is design-specific and does not address the macro-routing loop root cause.

**Confidence**: 0.3 (low) — no post-fix metrics, confounded variables, root cause unresolved.

---

### 6. Verdict

**Reject for dataset inclusion.** This draft is a raw debugging log, not a validated incident. It contains a fundamental terminology error (DRCs vs. congestion), misattributes causality, reports a confounded workaround without metrics, and defers the actual root cause. The 0.8 confidence score is dangerously misleading. If included, it must be reclassified as an "unvalidated workaround" with confidence ≤0.4 and explicit warnings about the missing post-fix data.