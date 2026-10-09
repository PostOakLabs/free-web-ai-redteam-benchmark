## Technical Review: OpenROAD Issue #6066 Episode Draft

Running this as a principal-level red-team pass. The record has several claims that don't hold together on their own terms.

---

### Issue 1: "0.24 placement density with a lot of open space" is internally contradictory as framed

The prior-state description uses "open space" as if it explains the mystery. It doesn't. Placement density of 0.24 means 76% of die area is *not* occupied by standard-cell sites — but that's a global statistic. Congestion is a *local* phenomenon. The record even admits the heatmap shows a "large region at the top of the die and around the macro." These two statements are not in tension; they're describing different spatial scales.

**Correct framing**: The density statistic is irrelevant to the congestion diagnosis. The relevant fact is macro placement and layer assignment creating a local routing bottleneck, not overall die utilization. The episode shouldn't use 0.24 density as explanatory color — it should be flagged as a *distractor* that makes the hypothesis look plausible when it isn't.

---

### Issue 2: The hypothesis doesn't actually follow from the observation

The stated hypothesis is: "routing-layer adjustment of 0.45 is too aggressive." But nowhere in this record is there evidence that a lower adjustment value would route around a macro-induced bottleneck. Layer adjustment affects which metal layers GlobalRoute uses for routing — it doesn't change the *geometry* of macro blocking. If the actual root cause is a global-route path looping around the macro (issue #5971), then changing layer adjustment is treating a symptom, not the cause.

**Implausibility**: A layer adjustment change that lets GRT "finish" is more likely masking the congestion through a different routing topology, not fixing the macro placement problem. The episode frames this as a successful fix; it's more accurately a workaround that made GRT converge without reporting violations.

---

### Issue 3: "Complete BoomTile" is not a measurable outcome

The post-state says GRT "could finish" — but "finish" and "pass" are different things. GRT can complete routing and still produce DRC violations. The fact that no post-fix DRC count is reported is not a minor gap; it's the entire point. Without a measured DRC count, the intervention's actual effectiveness is unverified.

**What the record should say**: Either "post-fix DRC count: N" or "post-fix DRC count: not reported, GRT completed without explicit DRC pass/fail signal." The current phrasing implies success where only process completion is demonstrated.

---

### Issue 4: The 30→35 congestion iteration change is arbitrary and undocumented

Increasing from 30 to 35 iterations with no explanation of why 35 specifically is the right number — not 40, not 100, not any value — makes this look like guessing. In GlobalRoute, congestion iterations are a convergence parameter; the normal failure mode is that *more iterations* doesn't help if the congestion is structural. The record doesn't explain what the sweep results were or why this specific increment was sufficient.

**Correct framing**: If the sweep was run and 35 was the minimum value that converged, that should be stated. If it was picked arbitrarily, that should be noted as well.

---

### Issue 5: The fix was never merged

This is the most significant gap. The chosen intervention is described as a *parameter change recommendation*, not a code change. The issue was then closed as `not_planned/Stale`. There is no PR link, no commit, no downstream fix verified. Anyone running this design would need to know to manually set those parameters — which means the "fix" is not reproducible from this episode.

**What the record should say**: "The intervention was a configuration recommendation with no corresponding code change. The fix is not captured in the OpenROAD codebase."

---

### Issue 6: The macro-loop root cause is unresolved and improperly linked

The episode notes a suspected root cause in #5971 ("looping around the macro") and then concludes that the layer-adjustment workaround was the solution. These are contradictory. If the macro-loop is a separate unresolved issue, it can't also be the root cause that was fixed here. Including both without resolving which one actually explains the failure undermines the episode's logical coherence.

**What should happen**: Either #5971 is marked as the true root cause (making this episode a workaround, not a fix), or the link is removed and the layer-adjustment change is treated as the stated resolution — not both.

---

### Summary of Corrections Needed

| Claim in Record | Problem | Correct Version |
|---|---|---|
| "Open space explains low density" | Density is global, congestion is local | Density is irrelevant to local routing bottleneck |
| "Layer adjustment 0.45 too aggressive → fix" | Layer change doesn't address macro geometry | This was a convergence workaround, not a root-cause fix |
| "Post-state: completed GRT" | No DRC count means success is unverified | "GRT completed; DRC count not reported" |
| "Iterations 35 as chosen intervention" | Arbitrary increment with no justification | "35 iterations was the minimum value in the sweep that converged; no further analysis" |
| "Issue resolved" | Closed stale, no PR, no code change | "Parameter recommendation only; no merged fix" |
| "#5971 linked as root cause" | Unresolved issue contradicts "fix" framing | Either state this is deferred or remove the causal link |

---

**Confidence verdict**: 0.8 is too high. This episode has no post-fix DRC count, no merged fix, and the stated intervention may not actually address the root cause. I'd rate this 0.4–0.5 at best, and recommend either downgrading to a "workaround observed" note or rejecting it until post-fix measurements and a PR link are available.