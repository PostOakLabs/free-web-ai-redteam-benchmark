**Review of draft episode (OpenROAD #6066)**

The draft is mostly a faithful paraphrase of the issue thread, but several technical claims are imprecise, over-interpreted, or internally inconsistent with the evidence presented. Below are the concrete problems, ordered by severity.

### 1. Over-claim on root-cause certainty
**Draft claim**  
“The GRT routing-layer adjustment of 0.45 … is too aggressive for this design; the default 30 congestion iterations were also insufficient.”

**Problem**  
The thread never establishes that 0.45 is *inherently* too aggressive, only that lowering it to 0.2 (together with raising iterations to 35) allowed GRT to finish. No ablation is shown that isolates the layer-adjustment effect from the iteration-count effect, nor is any quantitative comparison of overflow/congestion metrics before vs. after provided. The macro-looping issue (#5971) is simultaneously listed as a suspected cause; the draft treats the layer-adjustment change as the decisive fix while leaving the macro problem unresolved. This creates an internal inconsistency: two independent root causes are named, yet only one parameter change is presented as the chosen intervention that “completed” BoomTile.

**Correct version**  
“Lowering the routing-layer adjustment from 0.45 to 0.2 *and* raising the congestion-iteration limit from 30 to 35 allowed GRT to complete on this instance. Whether either change alone would have been sufficient, or whether the macro-looping behaviour (#5971) was the deeper cause, is not resolved by the thread.”

### 2. Post-state is reported without quantitative evidence
**Draft claim**  
“GRT was reported to complete … after reducing the layer adjustment to 0.2 and setting congestion iterations to 35. No re-measured DRC count was given.”

**Problem**  
The draft correctly notes the absence of a post-fix DRC count, yet still states “GRT was reported to complete” and “complete BoomTile” as if those statements constitute a verified post-state. The only evidence is a single developer sentence (“we could finish GRT”). No log snippet, congestion heatmap after the change, or even a statement that the final GRT overflow was zero appears in the record. Closing the issue as “not_planned/Stale” further weakens any claim that a durable fix was achieved.

**Correct version**  
“Developer eder-matheus stated that GRT finished after the two parameter changes. No post-change congestion/DRC numbers, runtime, or confirmation that the design subsequently passed detailed routing are present in the thread. The issue was later auto-closed as stale.”

### 3. “Chosen intervention” is presented as a committed fix
**Draft claim**  
“chosen_intervention: Per eder-matheus (MEMBER): ‘we could finish GRT by changing …’”

**Problem**  
The quoted statement is an observation about a local experiment, not a description of a merged code or flow change. The draft’s own gaps section already admits there is no PR link and that it is unknown whether the parameter values were ever committed. Elevating the quote to “chosen_intervention” therefore over-states the status of the change.

**Correct version**  
“Experimental parameter change that allowed GRT to finish on the reporter’s machine: layer-adjustment 0.2 + congestion iterations 35. No evidence that these values were upstreamed.”

### 4. Density vs. congestion causal language is slightly misleading
**Draft claim**  
“20k routing congestion DRCs while placement density is only 0.24 … a lot of open space, especially at the top of the die”

**Problem**  
The observation is factually present, but the draft’s framing implies that low density *should* have prevented congestion, making the 20 k DRC figure surprising. Global routing congestion can easily concentrate in narrow channels around macros even when average density is low; the heatmap description already points to the macro and the top region. The draft does not need to invent a paradox.

**Correct version**  
“Placement density 0.24 left substantial open area, yet GRT still reported ~20 k congestion DRCs, concentrated at the top of the die and around the macro.”

### 5. Minor internal inconsistencies / missing precision
- The prior-state and observation both mention “0.24 placement density” and “top of the die,” but never clarify whether that density figure is the *target* density used by the placer or the *final* density after placement. The difference matters for diagnosing why open space remained.
- The hypothesis mixes two orthogonal levers (layer adjustment and iteration count) with a third, unresolved issue (#5971). The draft never ranks their relative contribution.
- The gaps list correctly flags the missing PR and the stale closure, yet the confidence score remains 0.8. That score is inconsistent with the admitted evidentiary gaps.

**Correct confidence adjustment**  
Given the absence of post-fix metrics, the lack of a merged change, and the open macro-loop ticket, a confidence closer to 0.5–0.6 is more appropriate for any claim that “the design was fixed.”

### Summary of required corrections for dataset inclusion
1. Demote the layer-adjustment / iteration change from “chosen intervention that completed BoomTile” to “local experimental parameters that allowed GRT to finish.”
2. Explicitly state that no quantitative post-change congestion or DRC data exist.
3. Keep the macro-loop (#5971) as an unresolved parallel hypothesis rather than a secondary note.
4. Soften causal language that presents low average density as inherently protective against routing congestion.
5. Lower confidence to reflect the evidentiary gaps already listed by the draft itself.

With those edits the episode becomes a clean, modestly-scoped parameter-tuning anecdote rather than an overstated root-cause resolution.