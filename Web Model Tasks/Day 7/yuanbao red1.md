Verdict: REJECT as a recovery episode. Reclassify as "unresolved / mitigation-proposed-never-adopted," or rewrite.

The record has one genuinely good asset — the ORFS provenance string v3.0-1735-gdefc349e — and one fatal structural problem: the metric that defines the failure, the knob that was turned, and the stage that was "fixed" are three different things. Confidence 0.8 is not defensible against the record's own gaps array.

I've split findings into [I] = provable from the record's own contents (internal inconsistency), and [D] = requires domain knowledge about OpenROAD semantics.

BLOCKING defects

B1 [I+D] — Stage/metric conflation: "20k routing congestion DRCs" at "failed GRT" is a category error.
DRC violations are not a GRT output. Global routing reports congestion/overflow (total overflow, worst overflow, congested-GCell count). DRCs come from detailed_route / check_drc. And the two knobs in the intervention — layer adjustment and -congestion_iterations — are GRT-only parameters; they cannot move a DRC count produced downstream. So either prior_state is wrong (it wasn't a GRT failure, it was a DR/DRC failure) or observation is wrong (20k was overflow/GCells). As written, the "fix" is aimed at a different metric than the one that defined the incident. Pick a stage and rename the number.

B2 [I] — No recovery is demonstrated, yet confidence is 0.8.
post_state says GRT "complete"; gaps admits no re-measured count. A GRT run completing is not evidence that 20k congestion events went away — GRT completes by default and reports overflow on the way out. The gaps field and the confidence field directly contradict each other: the gaps listed here destroy the causal claim, so 0.8 cannot survive them.

B3 [I] — Nothing was actually chosen.
The issue was closed not_planned, there is no PR, and gaps concedes the merge status is unknown. A maintainer's in-thread suggestion that the project declined is not a chosen_intervention — it's a proposed_intervention. The field name launders a rejected suggestion into an adopted fix. That is the single most misleading thing in the record for a downstream consumer.

B4 [I] — The record's own evidence indicts the root cause it declined to fix.
prior_state: "a lot of open space, especially at the top of the die." observation: congestion is "at the top of the die and around the macro." These are not a paradox — they are one fact. A hot region sitting inside empty area is the signature of a detour corridor: nets blocked by the macro route around it through the open top region. That is precisely the "looping around the macro" hypothesis deferred to #5971. So the heatmap is confirmatory evidence for #5971, and the chosen fix (a global capacity knob) does not address it. The record never draws this line, and its hypothesis/chosen_intervention pairing is therefore internally incoherent.

MAJOR defects

M1 [D] — The layer adjustment change is close to tautological, and the record never says why.
set_global_routing_layer_adjustment <layer> <adj> blocks a fraction of a layer's tracks from GRT. 0.45 → 45% blocked (55% usable); 0.2 → 20% blocked (80% usable). Going 0.45→0.2 increases modeled routing capacity by ~45%. That does not route the design better — it loosens the constraint until the tool stops reporting overflow. Of course GRT "completes." The real cost is deferred to detail route, which the record never runs. The gaps field admits the semantics are "only explained in prose," but this isn't a documentation nit — the entire causal claim is unintelligible without it.

M2 [I] — Confounded, unattributed change.
Two knobs moved together (0.45→0.2 and 30→35). candidates_considered says iterations were "asked early on and swept" but reports no sweep outcome. There is no basis to attribute convergence to either change, or to rule out that the layer adjustment alone did it.

M3 [D] — "default 30" is one unreplicated assertion carrying half the intervention.
The record asserts it twice, which reads as authority but is a single unsourced claim. If the actual default is higher than 35, then "changed to 35" is a decrease and the "default was insufficient, so we raised it" narrative inverts completely. Cheap to check; load-bearing.

M4 [D] — The parameter is per-layer; the record treats it as a scalar.
set_global_routing_layer_adjustment takes a layer argument, and asap7/ORFS applies non-uniform adjustments across the stack. "0.45" and "0.2" as bare scalars are unreproducible — which layers? All of them? Uniformly relaxing every layer is a very different (and much more dangerous) act than relaxing the two or three layers the congested corridor actually uses.

M5 [I] — The headline "paradox" is self-undermining.
"20k congestion DRCs at only 0.24 placement density" invites the reader to be shocked that a sparse design is congested. But 0.24 is a global average, and the congestion is explicitly localized. Low global density plus a hard macro plus concentrated local congestion is expected, not anomalous. The framing manufactures a mystery instead of reporting the actual one (why does the detour exist — i.e., #5971).

MINOR / hygiene

• [I] not_planned/Stale conflates a close state with a label; "Stale" is not a GitHub close reason.

• [I] Quote dated 2024-11-14 but closure in 2026 — a ~14-month gap before a stale bot fires is implausible. Either the quote date, the closure year, or the "automatically" claim is wrong.

• [I] gaps is written in the issue author's voice ("We (eder-matheus) note…"). Second-person leak into a dataset field.

• [D] set-global-routing-layer-adjustment is hyphenated — that's a docs-anchor slug. The Tcl command is set_global_routing_layer_adjustment.

• [I] run-me-BoomTile-asap7-base.sh gui is a reproduction command, filed under observation.

• [I] #5971 appears under candidates_considered as if evaluated-and-rejected; it was deferred, never attempted. Schema misuse.

• [I] The direct_quote is ellipsis-truncated mid-sentence, while post_state reads the same sentence as full confirmation. Also "complete BoomTile" (whole flow) ≠ "complete GRT" (one stage) — the record silently downgrades the claim to the weaker, more defensible one.

• [I] No seed, no global_route invocation, no congestion report artifact, no heatmap preserved → non-reproducible.

• [D] asap7 is a predictive PDK; any retained "DRC" count is against an approximate deck. Worth a footnote.

What a correct version looks like

{
  "title": "BoomTile (asap7, ORFS): GRT overflow concentrated in a macro-adjacent detour corridor despite 0.24 global placement density; mitigated only by relaxing the GRT capacity model — macro root cause deferred (#5971), change never adopted",
  "stage": "global_route (GRT)",
  "metric": "GRT congestion: total overflow, worst overflow, congested-GCell count. NOT DRC (DRC is a detailed_route/check_drc artifact and is not produced by GRT).",
  "prior_state": "BoomTile (MegaBoom-derived) in asap7, ORFS v3.0-1735-gdefc349e. Standard-cell placement density 0.24, with open area concentrated at the top of the die. global_route did not reach acceptable overflow.",
  "observation": "20k <congested GCells | total-overflow units — RECORD MUST NAME THE METRIC> reported by GRT. Congestion heatmap is contiguous with the macro halo and extends into the empty top-of-die region. That spatial pattern is consistent with a detour corridor around the macro, not with global capacity shortage.",
  "hypothesis_primary": "Nets loop around the macro, funneling through the open top-of-die region (#5971). Supported by the heatmap: the hot region is in *empty* area, which is what a detour looks like.",
  "hypothesis_secondary": "Modeled per-layer capacity is over-conservative for this design (layer adjustment 0.45 = 45% of tracks blocked).",
  "candidates_considered": "2x2 sweep required, results currently unreported: {layer_adj 0.45, 0.2} x {congestion_iterations DEFAULT, 35}. Note: as reported, both changes were applied together, so attribution is impossible.",
  "intervention_proposed": "Reduce set_global_routing_layer_adjustment on layers {UNSPECIFIED — MUST BE NAMED} from 0.45 to 0.2 (55% -> 80% usable tracks, i.e. a capacity-model relaxation, not a routing improvement); raise -congestion_iterations to 35.",
  "intervention_status": "Proposed in-thread by eder-matheus (MEMBER), 2024-11-14. No PR. Issue closed not_planned (Stale label), i.e. NOT adopted upstream.",
  "post_state": "GRT reported to complete in a local run. No overflow re-measurement, no detail-route or check_drc validation, no runtime. Because the change relaxes the capacity model, 'GRT completes' is a weak result: the displaced cost would appear at detail route, which was never measured.",
  "why_mitigation_not_fix": "The knob increases modeled track supply rather than reducing wiring demand; the named root cause (macro looping, #5971) was explicitly deferred and remains open.",
  "confidence": {
    "issue_exists": 0.8,
    "congestion_observed_as_described": 0.6,
    "intervention_caused_recovery": 0.15,
    "root_cause_identified": 0.25
  }
}


Before this earns a place in the dataset, someone must run: baseline (0.45 / default iters) → 0.2 / default → 0.45 / 35 → 0.2 / 35, capturing total overflow, worst overflow and congested-GCell count at each corner, then take the winning corner through detailed_route + check_drc and report DRC count and runtime. Until a corner clears detail route without regressing DRCs, this is not a recovery story — it's a report of a number going down because the ruler got longer.