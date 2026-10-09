This record fails curation as written. It is internally inconsistent and technically sloppy. Judged only on what is in the record:

**1. Terminology: "20k routing congestion DRCs" is wrong.**
GRT does not produce DRCs. It produces overflow / congestion violations. The GUI may visualize them as markers, but they are not DRCs. The observation should say: ~20k overflow violations at GRT stage. Calling them DRCs implies detailed routing ran and failed.

**2. Layer adjustment directionality is inverted / undefined.**
Hypothesis: "0.45 is too aggressive, 0.2 fixes it."

The record itself flags in `gaps`: meaning of high vs low value is only explained in prose. If `set-global-routing-layer-adjustment` is *fraction kept* [0=block all, 1=keep all], then 0.45 -> 0.2 is MORE aggressive [20% capacity kept vs 45%], and would make congestion worse, not better. If it is *fraction reduced*, then 0.45 -> 0.2 is less aggressive. You cannot claim a fix without stating the definition. Correct version:

> `adjustment` is defined as [keep|reduce]. Under that definition, moving from 0.45 to 0.2 means [increasing|decreasing] available capacity from X% to Y%. The thread claims this allowed GRT to converge.

As written it asserts a causal fix while admitting it does not know what the parameter means.

**3. Prior_state vs Observation contradicts on location.**
Prior: "a lot of open space, especially at the top of the die"
Observation: "Congestion heatmap shows a large region at the top of the die"

You cannot have both: top is empty AND top is highly congested due to placement, unless the congestion is *not* from cell placement but from macro-induced routing detour. That is exactly the competing hypothesis in #5971 that you bury.

**4. Two competing root causes are conflated.**
Record lists simultaneously:
- a) layer adjustment 0.45 tuned for other asap7 designs is too aggressive for BoomTile
- b) global-route path "looping around the macro many times" [#5971]

If b) is true, a) is a workaround that hides the bug by adding routing resources, not a fix. If a) is true, b) is irrelevant. You cannot claim both without disambiguation. Correct version must keep them separate: suspected workaround = relax layer adjustment, suspected bug = macro-loop in GRT.

**5. Intervention magnitude does not match claimed effect.**
20k violations fixed by 30 -> 35 congestion iterations [+16%] is implausible on its own. The thread asks about increasing iterations early and sweeps it. The final quote bundles two changes: adjustment 0.45->0.2 AND 30->35. The record has no ablation: was it adjustment, iterations, or both? No data.

**6. Post_state claims completion with zero measurement.**
`post_state`: "GRT was reported to complete ('could finish GRT', 'complete BoomTile')"

But `gaps` itself admits: "No measured post-fix DRC count or runtime is reported." You cannot claim 20k -> 0. You must claim: anecdotal report by MEMBER that GRT finished, no log, no final overflow count, no runtime, no reproduction.

**7. Lifecycle vs fix claim is inconsistent.**
If this parameter change actually fixed BoomTile, why was #6066 closed automatically as `not_planned/Stale` in 2026 with "No PR link for the fix" and "whether the reported parameter change was actually merged as a code change is not stated"?

A real fix would have a PR, a config change in ORFS, or a closed-as-completed. Auto-stale + not_planned means it was *not* accepted as a fix. The correct post_state is: fix unmerged, workaround reported locally, issue timed out.

**8. Confidence 0.8 is unjustified.**
Given: no post-fix numbers, no PR, ambiguous parameter semantics, competing hypothesis deferred to #5971, auto-closed stale. Confidence should be 0.3-0.4 and marked as `workaround_reported_not_verified`.

What a correct version would look like:

> BoomTile in asap7, reported placement density 0.24 [definition unspecified]. GRT reports ~20k congestion/overflow violations, visualized in top-of-die and around macro. Thread proposes two hypotheses: (1) layer adjustment value 0.45, carried from other asap7 designs, over-constrains GRT; (2) GRT routes looping around macro repeatedly [#5971]. Local workaround reported by eder-matheus to allow GRT to finish: relax adjustment to 0.2 [pending definition of keep vs reduce] and raise congestion iterations 30->35. No final overflow count, no runtime, no config PR. Issue closed as stale/not_planned in 2026, fix status unknown.