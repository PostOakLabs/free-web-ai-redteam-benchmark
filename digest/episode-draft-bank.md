# Episode Draft Bank — all episode drafts, runs 1–2, plus D2 paper recalls

**Status: DRAFT SCAFFOLDING, NOT EXPERT DATA.** Nothing in this bank is an episode in the corpus and
nothing counts toward any corpus number. Everything enters downstream use as
`provenance: synthetic-fixture` with run marker `free-model-harvest/A/2026-08-31`. The one
exception the integrity rule allows — locator-cited extraction from a verified public source
becoming a `retrospective`-candidate — applies to a **small named subset of the D2 recalls in §3**,
and only pending Alice's technical review.

**Contents.** §1 the 78 episode drafts with honesty labels, log tier and a KEEP/SALVAGE/DISCARD
recommendation. §2 the cross-run findings that only appear when both runs are read together.
§3 the D2 POWER4 recalls, now checkable against the actual paper. §3.4 re-grades every D2 claim against the
now-available extraction and paper text. §4 the Prompt J red-team adjudications. §5 the Prompt L Alpha 21264 recalls,
§5b the M and N slices, §6 the Prompt O Niagara adjudication. §7 appendix: all 266
`candidates_considered` / `rejected_because` pairs grouped by failure class.

---

## 1. The 78 drafts

**Count correction.** The logs record 39 drafts (run 1) and a partial run-2 count. The recovered
total across both runs is **78 episodes from 26 model-runs**, and the rejection-pair count is
**266**, not the "~120" recorded in LOG-RUN1. The extra pairs come from run 2, from models that
over-delivered 4–5 candidates instead of 3, and from `solar pro`/`glm 5.3`/`sonnet`/`opus` files
that carry more than three episodes each.

**Recommendation key.**
- **KEEP** (26) / **KEEP-WITH-CORRECTIONS** (2, E28/E64 — the two red-teamed drafts) — numerically self-consistent on spot-check, honest `weakest_point`, from a model
  the logs graded T1 or an episode whose specific arithmetic survives recomputation. Worth Alice's
  reading time.
- **SALVAGE** (41) — structure sound, content generic or unverified. The `candidates_considered`
  pairs remain useful (§4) even where the episode body is bland.
- **DISCARD** (9) — contains an arithmetically impossible or self-contradicting state transition.
  These are *not* deleted; they are the calibration data. Every one of them carries a model
  confidence of 0.78–0.98, which is the point.


| # | model/run | class | conf | basis | log tier | rec | one-line summary | digest note |
|---|---|---|---|---|---|---|---|---|
| E1 | chatgpt/R1 | FAIL_CONGESTION | 0.84 | composite | T2 | SALVAGE | Late-route congestion from localized pin density |  |
| E2 | chatgpt/R1 | FAIL_TIMING | 0.9 | composite | T2 | SALVAGE | Hundreds of setup violations that were really one constraint problem |  |
| E3 | chatgpt/R1 | SDC_BUDGET | 0.78 | constructed | T2 | SALVAGE | Deriving an interface budget from the receiving block's real slack margin |  |
| E4 | deepseek instant/R1 | FAIL_CONGESTION | 0.78 | composite | T2–T3 | SALVAGE | Late routing congestion resolved by pin-swap and density-guide tweaks instead of floorplan respin |  |
| E5 | deepseek instant/R1 | FAIL_TIMING | 0.82 | composite | T2–T3 | **DISCARD** | Timing closure failure diagnosed by path-shape signature as a systematic clock-uncertainty issue | 312 paths failing 50–150 ps cannot sum to TNS −2500 ps (floor ≈ −15,600 ps) |
| E6 | deepseek instant/R1 | SDC_BUDGET | 0.85 | composite | T2–T3 | SALVAGE | SDC budget derivation at block boundary: switching to multicycle constraints instead of tightening c |  |
| E7 | gemini/R1 | FAIL_CONGESTION | 0.95 | composite | T2–T3 | **DISCARD** | Post-CTS Global Routing Hotspot Resolution via Local Cell-Density Soft Keepouts and Clock Tree Re-ro | DRC 14,200→42 plus WNS −0.12→−0.015 from local keepouts alone; effect size not credible |
| E8 | gemini/R1 | FAIL_TIMING | 0.98 | composite | T2–T3 | **DISCARD** | Identifying Missing False Path Constraints via Massive Uniform WNS Violations Across Unrelated Clock | TNS/endpoint mean (8.57 ns) exceeds |WNS| (8.45 ns) — arithmetically impossible |
| E9 | gemini/R1 | SDC_BUDGET | 0.92 | composite | T2–T3 | SALVAGE | Inter-Block Timing Budget Allocation for High-Speed Memory Controller to PHY Interface |  |
| E10 | glm 5.3/R1 | FAIL_CONGESTION | 0.72 | composite | T2 | SALVAGE | Post-CTS congestion hotspot in macro channel fixed with routing-direction restriction instead of flo |  |
| E11 | glm 5.3/R1 | FAIL_TIMING | 0.78 | composite | T2 | **KEEP** | Thousands of small hold violations sharing one launch clock finger diagnosed as CTS skew signature,  | hold TNS −118 ns over 3,900 endpoints vs WNS −38 ps ✅ consistent |
| E12 | glm 5.3/R1 | SDC_BUDGET | 0.68 | constructed | T2 | SALVAGE | Block-boundary IO budget derived from real interface timing rather than a 50/50 split, avoiding over |  |
| E13 | kimi/R1 | FAIL_CONGESTION | 0.75 | composite | T1 | **KEEP** | Late-stage macro pin-access congestion resolved by selective macro spreading without full re-placeme | congestion fix COSTS timing (−0.05→−0.06 ns) — the realistic direction, pre-hint |
| E14 | kimi/R1 | FAIL_TIMING | 0.8 | composite | T1 | **KEEP** | Uniform cross-clock violation signature reveals incorrect clock period constraint, avoiding physical |  |
| E15 | kimi/R1 | SDC_BUDGET | 0.7 | constructed | T1 | **KEEP** | Interface timing budget reallocation from measured delays prevents congestion collapse in high-utili |  |
| E16 | meta/R1 | FAIL_CONGESTION | 0.72 | composite | T2 | SALVAGE | Late routing congestion at top-level pin field after CTS |  |
| E17 | meta/R1 | FAIL_TIMING | 0.81 | composite | T2 | SALVAGE | Input-delay overconstraint masquerading as logic depth failure |  |
| E18 | meta/R1 | SDC_BUDGET | 0.76 | constructed | T2 | SALVAGE | Cross-block output budget allocation between encryption core and fabric |  |
| E19 | mimo/R1 | FAIL_CONGESTION | 0.72 | composite | T2 | SALVAGE | Macro Pin-Swap Resolves Post-CTS Congestion Hotspot Without Floorplan Rework |  |
| E20 | mimo/R1 | FAIL_TIMING | 0.81 | composite | T2 | SALVAGE | Clustered Launch-Point Signature Exposes Missing False Path Before Any Physical Work |  |
| E21 | mimo/R1 | SDC_BUDGET | 0.68 | composite | T2 | SALVAGE | Asymmetric Slack-Aware Budget Re-Derivation Replaces Naive Split-the-Difference SDC |  |
| E22 | minimax m3/R1 | FAIL_CONGESTION | 0.62 | composite | T2 | SALVAGE | Late-stage routing congestion rescued by macro channel widening after cell spreading was rejected |  |
| E23 | minimax m3/R1 | FAIL_TIMING | 0.58 | composite | T2 | **KEEP** | Distinguishing constraint problem from physical problem by violation report shape on a 7nm block | tight-cluster numbers self-consistent (312 paths, TNS −64 ns, WNS −210 ps) and honest conf 0.58 |
| E24 | minimax m3/R1 | SDC_BUDGET | 0.65 | composite | T2 | SALVAGE | Block boundary timing budget: false-path vs multicycle derivation that avoided a 3-week schedule sli |  |
| E25 | mistral/R1 | FAIL_CONGESTION | 0.88 | composite | T2–T3 | SALVAGE | Late-stage congestion hotspot resolved via localized pin optimization |  |
| E26 | mistral/R1 | FAIL_TIMING | 0.92 | composite | T2–T3 | SALVAGE | Clock skew signature distinguishes physical problem from constraint issue |  |
| E27 | mistral/R1 | SDC_BUDGET | 0.85 | composite | T2–T3 | SALVAGE | Async block boundary budget derived from measured clock uncertainty |  |
| E28 | opus 5/R1 | FAIL_CONGESTION | 0.62 | composite | T1 | **KEEP-WITH-CORRECTIONS** | Late detonation of routing congestion in a macro-dense DSP block; floorplan rework rejected, hotspot | self-flags its own 214k→340 DRC drop as the weakest number | — red-teamed, see §4
| E29 | opus 5/R1 | FAIL_TIMING | 0.68 | composite | T1 | **KEEP** | 4,200 failing endpoints that were one SDC defect: reading the violation histogram before touching th |  |
| E30 | opus 5/R1 | SDC_BUDGET | 0.6 | composite | T1 | **KEEP** | Deriving an asymmetric interface budget at a block boundary, and why the multicycle - not the false  |  |
| E31 | qwen/R1 | FAIL_CONGESTION | 0.85 | constructed | T2–T3 | SALVAGE | Post-CTS Routing Congestion Resolved via Macro Shifting and Localized NDR |  |
| E32 | qwen/R1 | FAIL_TIMING | 0.95 | composite | T2–T3 | SALVAGE | Timing Cliff Identified as SDC Multicycle Path Error Rather Than Logic Delay |  |
| E33 | qwen/R1 | SDC_BUDGET | 0.9 | constructed | T2–T3 | SALVAGE | Block Boundary Timing Budget Reallocation from Receiving Block Margin |  |
| E34 | sonnet/R1 | FAIL_CONGESTION | 0.55 | composite | T1 | **KEEP** | Late-detected congestion pocket near a macro cluster resolved by targeted cell spreading, not re-pla |  |
| E35 | sonnet/R1 | FAIL_TIMING | 0.5 | constructed | T1 | **KEEP** | Reading a bimodal failing-path distribution to separate a constraint problem from a physical problem |  |
| E36 | sonnet/R1 | SDC_BUDGET | 0.5 | composite | T1 | **KEEP** | Deriving a block-boundary timing budget by logic-depth ratio instead of an even split |  |
| E37 | tencent yunbao/R1 | FAIL_CONGESTION | 0.78 | constructed | T2 | SALVAGE | Macro-channel congestion resolved via pin-swap and selective promotion at 7nm, avoiding floorplan re |  |
| E38 | tencent yunbao/R1 | FAIL_TIMING | 0.85 | constructed | T2 | **DISCARD** | Signature-based diagnosis: 1415 correlated timing failures traced to incorrect SDC constraint, not p | post-state has WNS +120 ps, 0 failing paths, and TNS −850 ps simultaneously |
| E39 | tencent yunbao/R1 | SDC_BUDGET | 0.75 | constructed | T2 | SALVAGE | Asymmetric inter-block timing budget derived bottom-up from internal WNS margins at 16nm |  |
| E40 | chatgpt/R2 | FAIL_CONGESTION | 0.86 | composite | T1 | **KEEP** | Late detailed-route overflow concentrated around SRAM channels |  |
| E41 | chatgpt/R2 | FAIL_TIMING | 0.91 | composite | T1 | **KEEP** | Violation-count and depth pattern exposed a clock-constraint problem |  |
| E42 | chatgpt/R2 | SDC_BUDGET | 0.82 | constructed | T1 | **KEEP** | Interface budget derived from end-to-end timing rather than a symmetric split |  |
| E43 | deepseek/R2 | FAIL_CONGESTION | 0.8 | composite | T3 | **DISCARD** | Late congestion in macro channels resolved by local pin-swap and route-guide, not by floorplan revis | post_state text says 'slight timing degradation' while WNS improves −45→−30 ps |
| E44 | deepseek/R2 | FAIL_TIMING | 0.84 | composite | T3 | **DISCARD** | Timing violation shape reveals clock skew mis-modeling rather than logic depth | 410 paths failing 80–150 ps cannot sum to TNS −1800 ps (floor ≈ −32,800 ps) |
| E45 | deepseek/R2 | SDC_BUDGET | 0.87 | composite | T3 | SALVAGE | SDC multicycle exception chosen over clock period tightening for cross-domain control signals |  |
| E46 | gemini/R2 | FAIL_CONGESTION | 0.94 | composite | T2 | **DISCARD** | Post-CTS Macro Channel Routing Congestion Resolution via Soft Placement Blockages and Clock Buffer R | DRC 24,150→118 from soft blockages and buffer relocation alone; effect size not credible |
| E47 | gemini/R2 | FAIL_TIMING | 0.96 | composite | T2 | **DISCARD** | Diagnosis of Missing Asynchronous Clock Group Constraints from Uniform Violation Magnitude Signature | TNS/endpoint mean equals |WNS| exactly — requires perfectly uniform slack; not credible |
| E48 | gemini/R2 | SDC_BUDGET | 0.93 | composite | T2 | SALVAGE | Hierarchical Block-Boundary Budget Realignment Based on Asymmetric Logic Depth |  |
| E49 | glm 5.3/R2 | FAIL_CONGESTION | 0.74 | composite | T1 | **KEEP** | Detailed-route congestion in SRAM channels fixed with channel-local routing blockages and incrementa |  |
| E50 | glm 5.3/R2 | FAIL_TIMING | 0.76 | composite | T1 | **KEEP** | 1,900 setup paths failing 150-250 ps from one launch bank read as a logic-depth problem — fixed by r |  |
| E51 | glm 5.3/R2 | SDC_BUDGET | 0.7 | constructed | T1 | **KEEP** | Slow config-register bus given an evidence-backed 2-cycle multicycle instead of a single-cycle budge |  |
| E52 | kimi/R2 | FAIL_CONGESTION | 0.72 | composite | T1 | **KEEP** | Post-CTS macro-channel congestion resolved by selective repeater relocation without invalidating clo |  |
| E53 | kimi/R2 | FAIL_TIMING | 0.78 | composite | T1 | **KEEP** | Uniform fanout-violation signature reveals source-side logic-depth problem, avoiding fruitless place |  |
| E54 | kimi/R2 | SDC_BUDGET | 0.75 | constructed | T1 | **KEEP** | Interface budget reallocation from measured parasitics prevents congestion collapse in high-utilizat |  |
| E55 | meta/R2 | FAIL_CONGESTION | 0.74 | composite | T2 | SALVAGE | 28nm macro-channel congestion at first detailed route after clean post-CTS |  |
| E56 | meta/R2 | FAIL_TIMING | 0.79 | composite | T2 | SALVAGE | Many small shared-startpoint failures vs few large distributed failures |  |
| E57 | meta/R2 | SDC_BUDGET | 0.77 | constructed | T2 | SALVAGE | Output budget split between crypto core and interconnect fabric |  |
| E58 | mimo/R2 | FAIL_CONGESTION | 0.74 | composite | T2 | SALVAGE | Macro-Channel Overflow Resolved by Selective Macro Rotation and Pin-Row Rebalancing |  |
| E59 | mimo/R2 | FAIL_TIMING | 0.83 | composite | T2 | **KEEP** | Clustered Single-Launch Signature Reveals Missing Clock-Group Exclusion Before Any Physical Optimiza | self-critical: flags its own scenario as assuming an unrealistic SDC-review gap |
| E60 | mimo/R2 | SDC_BUDGET | 0.71 | composite | T2 | **KEEP** | Slack-Asymmetric Budget Re-Derivation Avoids Floorplan Change at Block Boundary | self-critical: flags its own premise as one a mature team would have caught |
| E61 | mistral/R2 | FAIL_CONGESTION | 0.9 | composite | T3 | SALVAGE | Post-CTS congestion in SRAM channels on 28nm block |  |
| E62 | mistral/R2 | FAIL_TIMING | 0.88 | composite | T3 | SALVAGE | Spatial clustering of 12k failing paths reveals physical congestion, not constraint issue |  |
| E63 | mistral/R2 | SDC_BUDGET | 0.85 | composite | T3 | SALVAGE | Async boundary budget derived from measured clock skew and uncertainty |  |
| E64 | opus/R2 | FAIL_CONGESTION | 0.62 | composite | T1 | **KEEP-WITH-CORRECTIONS** | 28nm SRAM-channel congestion found at first detailed route; frozen floorplan forced a density-screen | self-flags its own 175k→2,400 DRC drop as the weakest number | — red-teamed, see §4
| E65 | opus/R2 | FAIL_TIMING | 0.66 | composite | T1 | **KEEP** | A 4,200-endpoint failure that was one generated-clock definition: diagnosing from the slack histogra |  |
| E66 | opus/R2 | SDC_BUDGET | 0.6 | composite | T1 | **KEEP** | Asymmetric interface budget derived from logic depth, and why the configuration path got a multicycl |  |
| E67 | qwen/R2 | FAIL_CONGESTION | 0.88 | constructed | T2 | SALVAGE | Post-CTS Routing Congestion Resolved via Macro Shifting and Localized NDR |  |
| E68 | qwen/R2 | FAIL_TIMING | 0.95 | composite | T2 | SALVAGE | Timing Cliff Identified as SDC Multicycle Path Error Rather Than Logic Delay |  |
| E69 | qwen/R2 | SDC_BUDGET | 0.9 | constructed | T2 | SALVAGE | Block Boundary Timing Budget Reallocation from Receiving Block Margin |  |
| E70 | solar pro/R2 | FAIL_CONGESTION | 0.72 | composite | T2 | SALVAGE | Post-CTS routing congestion in macro channels resolved by macro halo adjustment, not router effort |  |
| E71 | solar pro/R2 | FAIL_TIMING | 0.78 | composite | T2 | **DISCARD** | Timing violation report shape distinguished a clock-domain constraint error from a logic-depth probl | WNS −0.62 ns while its own distribution puts 87 paths worse than −2 ns |
| E72 | solar pro/R2 | SDC_BUDGET | 0.75 | composite | T2 | SALVAGE | Inter-block SDC budget between 28nm CPU core and 28nm L2 cache: false-path rejection and multicycle  |  |
| E73 | sonnet/R2 | FAIL_CONGESTION | 0.5 | composite | T1 | **KEEP** | Macro-channel congestion caught at first detailed-route, fixed by SRAM channel re-guiding instead of |  |
| E74 | sonnet/R2 | FAIL_TIMING | 0.45 | constructed | T1 | **KEEP** | Reading violation-report shape to tell constraint problem from logic-depth problem from physical/pla |  |
| E75 | sonnet/R2 | SDC_BUDGET | 0.45 | composite | T1 | **KEEP** | Deriving a cross-clock-domain boundary budget from CDC synchronizer latency instead of a flat guess |  |
| E76 | yuanbao/R2 | FAIL_CONGESTION | 0.78 | constructed | T2 | SALVAGE | Macro-channel congestion resolved via pin-swap and selective layer promotion at 28nm, avoiding floor |  |
| E77 | yuanbao/R2 | FAIL_TIMING | 0.85 | constructed | T2 | SALVAGE | Signature-based diagnosis: 980 correlated timing failures traced to incorrect SDC constraint, not ph |  |
| E78 | yuanbao/R2 | SDC_BUDGET | 0.75 | constructed | T2 | SALVAGE | Asymmetric inter-block timing budget derived bottom-up from internal WNS margins at 7nm |  |


---

## 2. Cross-run findings

### Finding 1 — the "congestion fix costs timing" hint propagated to almost every model

Prompt A-v2 added the parenthetical *"a congestion fix often COSTS a little timing"*. Counting the
15 congestion episodes per run by whether the post-state WNS is worse than the prior:

| | fix costs timing (realistic) | fix improves timing (optimistic) |
|---|---|---|
| Run 1 (A-v1, no hint) | 7 | 8 |
| Run 2 (A-v2, hint present) | 14 | 1 |

Thirteen of fifteen models flipped direction. LOG-RUN1 singled out kimi as "the only model whose
congestion fix COSTS timing — the realistic direction"; after the hint, that behaviour is near
universal and therefore no longer evidence of anything about the model.

**Why this matters more than it looks.** It establishes that `post_state` numbers in this corpus are
**prompt-shaped, not knowledge-shaped**. Any future use of these numbers as a distribution — "what
does a real congestion fix cost?" — would be measuring the prompt. It also means the honesty
machinery cannot detect this class of contamination: the models were being obedient, not dishonest,
and their `weakest_point` fields correctly flag other things.

### Finding 2 — a mechanical consistency check nobody has been running

For any setup-timing episode, `TNS`, `WNS` and the failing-endpoint count are not independent:
`|TNS| / endpoints` is the mean negative slack, and it **cannot exceed `|WNS|`**. Applying that
single inequality plus two related sanity rules (a positive WNS forces TNS = 0; a stated slack
distribution must sum to at least the count times its own floor) catches **6 of the 26 timing
episodes**, across four different models, including the two highest-confidence episodes in the whole
corpus (gemini at 0.98 and 0.96).

| Episode | Model | The impossibility |
|---|---|---|
| E8 | gemini/R1 (conf 0.98) | 2,150 endpoints, TNS −18,420 ns → mean −8.57 ns, but WNS is −8.45 ns |
| E47 | gemini/R2 (conf 0.96) | 2,000 endpoints, TNS −9,700 ns → mean −4.85 ns = exactly WNS |
| E5 | deepseek/R1 | 312 paths "failing 50–150 ps" but TNS only −2,500 ps |
| E44 | deepseek/R2 | 410 paths "failing 80–150 ps" but TNS only −1,800 ps |
| E38 | tencent yunbao/R1 | post: WNS +120 ps, 0 failing paths, TNS −850 ps |
| E71 | solar pro/R2 | WNS −0.62 ns while its own histogram has 87 paths worse than −2 ns |

deepseek produces the same error class in both runs, which makes it a per-model trait rather than a
slip. Recommendation in `MISSED.md` §5.1: implement this as a validator; it is four lines of
arithmetic and it would have graded these six mechanically.

### Finding 3 — the scenario pinning worked, and produced near-duplicate episodes

Run 2 pinned scenario 1 to 28nm / ~1M instances / ~80 SRAM macros / discovered at first detailed
route after a clean post-CTS. Fifteen models produced fifteen episodes that are recognizably the
same episode: macro-channel overflow invisible in the block average, obvious fix (re-floorplan)
rejected on schedule, subtle fix (density screens, pin swaps, macro nudges, NDR re-scoping,
repeater relocation) succeeds. That is the prompt working as designed — but it also means run 2's
congestion episodes carry roughly one episode's worth of independent information, not fifteen.
The *interventions* differ usefully (see §4); the diagnoses do not.

### Finding 4 — `source_basis` stayed honest across 78 drafts

Zero `recalled-public-case` claims in either run. 58 `composite-of-common-practice`, 20
`constructed-example`. No model invented a named chip, company or person in an episode. The honesty
ladder is doing exactly what it was built for — and it confirms LOG-RUN1's read that the episode
prompt will not produce a named-source jackpot. That path runs through Prompt C/D and the source
PDFs, not through Prompt A.

### Finding 5 — confidence does not predict correctness

Of the 9 DISCARD episodes, self-rated confidence runs 0.78–0.98 (median 0.88). Of the 28 KEEP
episodes, confidence runs 0.45–0.90 (median 0.70). **The relationship is inverted.** sonnet and
opus, the two models that consistently rate themselves lowest (0.45–0.68), produce the episodes that
survive arithmetic checking; gemini, which rates itself 0.94–0.98, produces two of the impossible
ones. Use `weakest_point` — which is consistently useful — and ignore `confidence` as a ranking
signal for this task.



---

## 3. D2 — POWER4 paper recalls, checked against the actual paper

**This section is different from the rest of the bank, because the source is now on disk.**
`../sources/POWER4-system-microarchitecture-IBMJRD-46-1-2002.pdf` (21 pp., text-extractable) was
available to this digest session, so the D2 recall claims could be checked against primary text
rather than graded on plausibility. Four further consensus-five PDFs are also present (see
`source-candidates.md` §1) — the master's local queue entry saying only POWER4-microarch is held is
**stale**.

**Corpus:** 9 D2 files, 8 models producing extraction-shaped objects (34 decision records), one
producing a genre map instead (gemini — wrong task, 10 entries, folded into
`source-candidates.md`), one prose refusal (mimo).

### 3.1 Verified TRUE against primary text → `retrospective`-candidates pending Alice

These recalls match the paper closely enough to quote. Under the integrity rule's exception they may
enter as `retrospective`-candidates **only after Alice's technical review**; the locator is given so
that review is cheap.

| Claim | Models | Primary text (POWER4 microarch paper) |
|---|---|---|
| **RAS philosophy: explicitly rejects "reliable parts + ECC on major arrays"; transforms checkstops into synchronous machine interrupts** | grok (0.95), meta (0.92), yuanbao (0.95) | Guiding principles: *"we accepted the principle that one does not achieve high levels of reliability only by choosing reliable parts and incorporating error-correction-code (ECC) logic into major arrays. Instead, we required an approach that eliminated outages and provided redundancy in cases where errors could not be eliminated… transform hard machine stops (checkstops) into synchronous machine interrupts to software"* |
| **Full-system design approach — the system was designed together, not the chip alone** | grok (0.95), meta (0.92), yuanbao (0.95) | Guiding principles: *"To optimize the system, we began with the full design in mind up front. This marriage of process technology, packaging, and microarchitecture was designed to allow software to exploit them."* |
| **SMP optimization as the organizing principle, transistors spent on total system throughput** | meta (0.95), yuanbao (0.95) | Guiding principles: *"The system must be optimized for SMP operation, in which a large number of transistors can be used to improve total system performance. By their very nature, servers process disparate information, often with multiple processes active concurrently."* |
| **Binary compatibility accepted as an absolute requirement after task forces found no technical impediment to scaling PowerPC** | meta (0.93) | *"…had concluded that the PowerPC Architecture had no technical impediments to prevent it from scaling up to significantly higher frequencies with excellent performance. With no technical reason to change, in order to keep our customers' software investment intact, we accepted the absolute requirement of maintaining binary compatibility…"* |
| **Distributed switch interconnect described as new to the industry; 4 chips/MCM → 8-way, 4 MCMs → 32-way** | grok (0.9), yuanbao (0.9) | *"The interconnect topology, referred to as a distributed switch, is new to the industry."* Plus the chip-organization section. |
| **174 M transistors; companion RAS paper by Bossen et al.** | yuanbao, grok | *"The chip contains 174 million transistors interconnected across seven layers of copper metallurgy."* / *"A more complete discussion of the POWER4 RAS features may be found in a companion paper by Bossen et al."* (yuanbao attributes the transistor count to the companion circuit paper; it is in this one — content right, attribution slightly off.) |
| **~1.5 MB shared L2** | deepseek (0.95) | Storage-hierarchy table: L2 *"≈1.5 MB"*, eight-way, 128-byte line. |

**yuanbao is the standout D2 model.** It quotes distinctive phrasing (*"an architecture within which
a set of chips are designed together to realize a system"*), names the CIU crossbar and its
32 bytes/cycle, names the companion paper's authors, and every one of its five entries checks out.
grok and meta are close behind and reproduce the guiding-principles section almost verbatim.

### 3.2 Verified FALSE against primary text — the inversion hunt

LOG-RUN5-era grading found **2 models inverting the clock-frequency philosophy**. Reading all nine
D2 files against the paper finds **3**, plus three further factual inversions on other axes.

**The clock-philosophy inversion (3 models, not 2).** The paper states the opposite of what they
claim, in the Introduction: *"In the ongoing debate between the 'speed demons' (high clock rate) and
the 'braniacs' (more complex design but a higher instructions-per-cycle rate), IBM UNIX-based
systems have traditionally been in the braniac camp. **With the POWER4, IBM opted to also embrace
the speed-demon approach.** The POWER4 design was initially introduced at processor frequencies of
1.1 GHz and 1.3 GHz, surpassing all other 64-bit microprocessors in some key performance
benchmarks."*

| Model | What it claimed | conf |
|---|---|---|
| chatgpt | "Optimize frequency with a balanced overall design **rather than maximizing clock speed**" | 0.72, hedged `probably-in-the-paper` |
| minimax m2.7 | "**moderate frequency rather than maximum frequency**… targeted 1.3–1.5 GHz rather than pushing to the maximum achievable" | 0.82, `confident-this-is-in-the-paper` ← the worst case: high confidence, wrong direction |
| minimax m3 | "**Modest clock-frequency target** chosen over highest possible frequency… robust frequency preferred over a headline number" | 0.45, hedged — the honesty field caught it |
| *(correct)* grok | "Opted to **also embrace the speed-demon** approach while retaining complex high-IPC design elements" — near-verbatim | 0.95 |

**Three further inversions on other axes, all newly found here:**

1. **minimax m2.7:** "POWER4 integrated a large on-chip L2 **rather than relying on an off-chip L3**
   as in earlier POWER processors." The paper: *"The directory for a third-level cache, L3, and its
   controller are also located on the POWER4 chip. **The actual L3 is on a separate chip.**"* POWER4
   has both — the contrast is fabricated.
2. **minimax m3:** "Use a **distributed on-chip L2 (per-core L2** with shared controller)". The
   paper's Figure 1 and text describe a *unified* L2 shared by both cores through the CIU crossbar,
   with three L2 controllers. Per-core L2 is the opposite of the design.
3. **deepseek and minimax m3 both:** "**directory-based** cache coherence protocol; snoopy protocols
   were considered but not scalable." The paper uses snoop-based coherence over the distributed
   switch — "snoop" appears 39 times, including *"no cache is sourcing data and no snooper retried
   the request"* — and the "L3 directory" it describes is a **cache tag directory**, not a
   directory-coherence protocol. **Two models agree on a wrong fact.** This is the most important
   single item in this section: consensus across models is not evidence of truth, and the run-3
   grading heuristic ("82 singletons are the risk pool") assumes it is.
4. **deepseek:** "DVFS support as well as clock gating for idle units… the paper mentions that
   without such measures power would exceed the thermal envelope." The strings *voltage*,
   *clock gating*, *power management* appear **zero times** in the paper. Fabricated — though
   deepseek gave it its own lowest confidence (0.70, `probably-in-the-paper`), so the honesty field
   worked even where the content did not.

**Minor:** grok, meta and yuanbao all use the phrase *"best-of-breed"* for the frequency goal. The
phrase does not appear in this paper. Content correct, quotation not — a reminder that these are
recalls, not extractions, and that a `direct_quote` field would have caught it.

### 3.3 What this changes about the pipeline

- The D2-v4 recall format **works**: with the PDF on disk, 7 claims verified true, 6 verified false,
  in one session. That ratio (roughly 50/50 by claim, but concentrated by model) is exactly what
  makes the format useful — it is separable.
- **`paper_vs_general` is the field that earns its place.** Of the six falsified claims, three were
  self-marked `probably-in-the-paper` and one `confident`. Of the seven verified claims, six were
  self-marked `confident-this-is-in-the-paper`. The field is not perfect but it is informative,
  unlike `confidence`.
- **The single most valuable next action** is running the retired D2-v3 *extraction* schema (with
  `where_in_paper` locators and non-empty `gaps`) against the POWER4 circuit/physical-design paper
  now on disk — it is the richer target and it is the one Alice's domain actually is.



### 3.4 Re-grade against the ground truth — every D2 claim marked CONFIRMED / NOT-IN-PAPER / CONTRADICTED

**What changed.** `../extractions/POWER4-system-microarchitecture.episodes.json` now exists: 8
locator-cited episodes with `direct_quote` and non-empty `gaps`, produced by a parallel session from
the actual PDF. `../VERIFIED-SOURCES.md` confirms the citation (Tendler et al., IBM J. Res. & Dev.
46(1):**5–25**, 2002 — note the page range the models gave as 5–26 is corrected there to 5–25).

**Method, and its one important limit.** The extraction is a **sample of 8 episodes chosen by an
extractor, not an index of the paper.** Its topic coverage barely overlaps the D2 recalls: it covers
speed-demon, binary compatibility, I-cache porting, group-boundary state tracking, the two-read /
one-write register limit, two L3 coherency-state decisions, and prefetch distance — while the D2
recalls concentrate on guiding principles and chip organization. **"Not in the extraction" therefore
means nothing.** Grading is done against the **full paper text** (extracted from the PDF in this
digest), with the extraction used as corroboration where the topics do overlap.

| Grade | Meaning |
|---|---|
| **CONFIRMED** | The paper states this, and the claim's direction is right |
| **PARTIAL** | Decision correct, but the stated rationale or a specific detail is not in the paper |
| **NOT-IN-PAPER** | The paper is silent — the claim may be true of POWER4, but not from this source |
| **CONTRADICTED** | The paper states the opposite |

#### The full grading

| Model | Claim | Grade | Evidence |
|---|---|---|---|
| **grok** | Embrace speed-demon alongside braniac | **CONFIRMED** | *"With the POWER4, IBM opted to also embrace the speed-demon approach"*; extraction episode [0] |
| grok | RAS beyond "reliable parts + ECC"; checkstops → machine interrupts | **CONFIRMED** | verbatim, Guiding principles |
| grok | Full-system co-design from the outset | **CONFIRMED** | *"we began with the full design in mind up front"* |
| grok | Single design for technical **and** commercial workloads | **CONFIRMED** | *"● Balanced technical and commercial performance"* |
| grok | Dual-core + distributed switch, 8-way module → 32-way | **CONFIRMED** | *"five primary interfaces"*; *"Four POWER4 chips… eight-way SMP. Four such modules… 32-way"* |
| **meta** | SMP optimization as primary target | **CONFIRMED** | verbatim guiding principle |
| meta | Full-system design vs chip-only | **CONFIRMED** | verbatim |
| meta | Very-high-frequency via **logic regularization** | **CONFIRMED** | *"revamped our chip design with new transistor-level tools, and have transformed complex control logic into regular data flow constructs"* |
| meta | Pervasive RAS eliminating checkstops | **CONFIRMED** | verbatim |
| meta | Binary compatibility as an absolute requirement | **CONFIRMED** | verbatim; extraction episode [1] |
| **yuanbao** | Very-high-frequency + regular dataflow | **CONFIRMED** | as above |
| yuanbao | Two cores sharing unified L2 via CIU crossbar | **CONFIRMED** | chip organization + Figure 1 |
| yuanbao | Full-system design approach | **CONFIRMED** | verbatim |
| yuanbao | Distributed switch, MCM hierarchy | **CONFIRMED** | verbatim |
| yuanbao | Pervasive RAS philosophy | **CONFIRMED** | verbatim |
| **chatgpt** | Distributed RAS, not a narrow centralized mechanism | **CONFIRMED** | Guiding principles |
| chatgpt | Distributed interconnect rather than a centralized bus | **CONFIRMED** (one detail unsupported) | *"distributed switch, is new to the industry"* ✓. But **"packet-based"** appears nowhere — "packet" has zero hits |
| chatgpt | Two cores on one chip sharing major resources | **CONFIRMED** | chip organization |
| chatgpt | Large shared L2 serving both cores | **CONFIRMED** | *"L2 Eight-way, 128-byte line ≈1.5 MB"* |
| chatgpt | **"Optimize frequency with a balanced design rather than maximizing clock speed"** | **CONTRADICTED** | The paper embraces the speed-demon approach and cites 1.1/1.3 GHz "surpassing all other 64-bit microprocessors" |
| **deepseek** | Dual-core with shared 1.5 MB L2 | **CONFIRMED** | storage-hierarchy table |
| deepseek | Deep pipeline, **"seven stages for integer"**, for 1 GHz+ | **PARTIAL** | Frequency goal confirmed; **the paper never states a pipeline-stage count.** Note: seven stages is the *Alpha 21264's* number (see §5) — possible cross-paper contamination |
| deepseek | Processor recovery incl. check-stop and **instruction retry** | **NOT-IN-PAPER** | "retry" has **zero hits**. RAS detail is explicitly deferred: *"a companion paper by Bossen et al."* |
| deepseek | **Directory-based** coherence; snoopy rejected as unscalable | **CONTRADICTED** | Snoop-based: "snoop" appears 39×, incl. *"no snooper retried the request"*. The "L3 directory" is a cache **tag** directory |
| deepseek | **DVFS and clock gating** for idle units | **NOT-IN-PAPER** | *voltage*, *clock gating*, *power management*: **zero hits each** |
| **minimax m2.7** | Dual-core rather than single-core | **PARTIAL** | Decision right; its rationale (*"frequency alone would not meet performance-per-chip goals at acceptable power"*) is absent — the paper argues from SMP throughput, not power |
| minimax m2.7 | **On-chip L2 rather than relying on an off-chip L3** | **CONTRADICTED** | *"The directory for a third-level cache, L3… located on the POWER4 chip. The actual L3 is on a separate chip."* POWER4 has both |
| minimax m2.7 | **"Moderate frequency rather than maximum frequency"** | **CONTRADICTED** | as chatgpt above; self-rated `confident-this-is-in-the-paper` |
| minimax m2.7 | L2 redundancy + ECC rather than retry-based recovery | **PARTIAL** | Redundancy confirmed (*"Both wordline and bitline redundancy… two redundant eight-way set-associative parity-protected arrays"*); the "rather than retry" contrast is not in the paper |
| **minimax m3** | Dual-core on a single die | **PARTIAL** | Decision right; its rationale (*"area, frequency, and **yield** trade-offs"*) is absent — "yield" has zero hits |
| minimax m3 | **"Modest clock-frequency target"** | **CONTRADICTED** | third inversion; self-flagged at 0.45 |
| minimax m3 | **Distributed per-core L2** | **CONTRADICTED** | L2 is unified and shared via the CIU; three L2 controllers serve both cores |
| minimax m3 | RAS-first with hardware **retry** and isolation | **PARTIAL** | RAS-first confirmed; retry not in this paper |
| minimax m3 | **Directory-based** coherence for chip-to-chip | **CONTRADICTED** | as deepseek above |
| **mimo** *(prose refusal, graded from its text)* | High-frequency design target as a deliberate architectural choice | **CONFIRMED** | **mimo got the clock-philosophy direction right** where three JSON-compliant models inverted it |
| mimo | RAS as a core design objective, not an afterthought | **CONFIRMED** | verbatim |
| mimo | Interconnect / SMP fabric as a distinguishing feature | **CONFIRMED** | distributed switch |
| **gemini** | *(produced a genre map, not an extraction — 0 gradable claims)* | — | wrong task; its 10 titles are folded into `source-candidates.md` |

#### Tally

| Grade | Count | Share |
|---|---|---|
| CONFIRMED | 23 | 62% |
| PARTIAL | 5 | 14% |
| NOT-IN-PAPER | 2 | 5% |
| CONTRADICTED | **7** | **19%** |
| **Total gradable claims** | **37** | (34 JSON + 3 recovered from mimo's prose) |

#### What the re-grade establishes

1. **Four models are clean: grok, meta, yuanbao and mimo — 18 claims, zero errors.** All four quote or
   closely paraphrase the guiding-principles section. yuanbao and grok additionally reproduce
   distinctive phrasing. These are the models to give paper-recall work.
2. **The errors concentrate in two models.** minimax m2.7 and minimax m3 account for **5 of the 7
   contradictions** between them. deepseek supplies the sixth and both NOT-IN-PAPER items; chatgpt the
   seventh. **Recall accuracy is a per-model property here, not a random error rate** — the same
   conclusion the arithmetic checks reached about deepseek in §2.
3. **`paper_vs_general` is worth more than `confidence`, but it is not reliable.** Of the 7
   contradicted claims, minimax m2.7 marked one `confident-this-is-in-the-paper` (the frequency
   inversion) and minimax m3 marked its inversion `probably-in-the-paper` at 0.45 — the honesty field
   caught one and missed the other. Of the 23 confirmed claims, 19 were self-marked `confident`.
   **Directionally useful, not a filter.**
4. **The consensus-is-evidence heuristic fails again.** Two models independently assert
   directory-based coherence for a snoop-based design. Two independently assert instruction retry that
   this paper defers to a companion. Agreement between models is agreement about a shared prior, not
   about the paper.
5. **Nothing in the extraction contradicted a claim that the full text confirmed**, and the extraction's
   episode [0] independently corroborates the clock-philosophy finding. Where the two sources overlap,
   they agree — which is a small positive signal about the extraction's fidelity.

#### ⚠ Correction to §3.2 of this file

§3.2 stated: *"grok, meta and yuanbao all use the phrase 'best-of-breed'… The phrase does not appear
in this paper."* **That was wrong.** The phrase is in the paper, in the very-high-frequency guiding
principle — *"we planned from the outset to deliver best-of-breed operating frequencies"* — and my
earlier search missed it because the PDF text breaks it across a line as `best-of- breed`. All three
models were quoting accurately.

**The methodological lesson is worth more than the correction:** naive substring search over
PDF-extracted text produces **false negatives at every line break**, and a false negative here reads
as "the model made it up". Any future grading pass must de-hyphenate and collapse whitespace before
searching. The same de-hyphenated search is what confirmed *"regular data flow constructs"*, which had
also returned zero hits in raw form.

---

## 4. Adjudications — Prompt J red-team review of the flagship congestion draft

**Status: model output reviewing model output.** These are adjudications of a draft, not expert
review. Run marker `free-model-harvest/J/2026-08-31`. They do not promote or demote anything in the
corpus by themselves; they produce a **correction list** for one draft, and a calibration result
about the honesty machinery.

### 5.1 What was reviewed

Prompt J (`prompts/PROMPT-J-EPISODE-REDTEAM.md`, J-v1) put a single draft in front of 13 models and
told them to attack the numbers and the causal chain, with the explicit instruction that *"inventing
objections is as bad as missing real ones."*

The draft is a lightly edited composite of **E28 / E64** — opus's 28nm SRAM-channel congestion
episode, the highest-graded episode of run 1 and run 2. The version under review: 71.5% utilization,
3.8% overflow in six west-edge channels 2–4 gcell columns wide, **~214,000 first-pass DRC
violations**, floorplan frozen by top-level feedthroughs and PG stripes, three actions (65% density
screens, NDR relaxation on two mid-layer metals, pin-swap on two macros), result **340 violations on
the next pass → 0 after two repair iterations**, overflow 3.8% → 0.6%, utilization unchanged at
71.5%, WNS −12 ps.

### 5.2 Parse and salvage

All 13 files contain a usable review. **Only 9 parse on first load.** The recovery ladder:

| Model | Parse status | Salvage needed |
|---|---|---|
| deepseek, gemini, kimi, meta, minimax 2.7, mistral, qwen, sonnet, yuanbao | ✅ clean | none |
| **grok** | ❌ → ✅ | **A single invalid escape sequence broke the entire object.** The string `"…dropped to 340 \ldots with unchanged utilization…"` contains a LaTeX `\ldots`; `\l` is not a legal JSON escape, so `json.loads` rejects the whole file. Stripping stray backslashes before invalid escapes recovers the complete 5-objection review, verdict, `missing_from_story`, `most_defensible_part` and `overall_note` — **nothing was actually missing from grok's output; one character made all of it unreadable.** A naive element-wise fallback recovers only 4 of 5 objections and loses every top-level field, which is why this needed a targeted repair rather than the generic salvage path. |
| **chatgpt** | ❌ → ✅ | Valid object **followed by appended reference links** (`Extra data: line 65`). `raw_decode` from the first `{` recovers it intact. The trailing material is a real citation — a ResearchGate 28nm physical-design case study — meaning chatgpt's review is partly literature-grounded. New source candidate, logged in `source-candidates.md`. |
| **minimax m3** | ⚠ partial | Mid-string corruption at char 606 (`"…without changing71.5%)", "object density screens…"` — a key fused into a truncated value), same class as the `毛片` corruption in its 2.7 sibling. 5 objections recovered element-wise; verdict readable from the raw head. |
| **mimo** | ⚠ prose | Fifth consecutive refusal-then-answer. Its prose review is complete and structured (verdict, 5 objections, missing-from-story, most-defensible-part, overall note) and is folded into the tallies below. |

**Note on the count.** The task brief describes "all 10 responding models". The measured figure is
**13 of 13 models produced a review**, of which 10 were reachable with routine parsing (9 clean +
grok after escape repair). The three additional reviews — chatgpt, minimax m3, mimo — required the
salvage ladder above and all three confirm the headline objection.

### 5.3 Verdicts

| Verdict | Count | Models |
|---|---|---|
| PLAUSIBLE-AS-IS | **0** | — |
| PLAUSIBLE-WITH-CORRECTIONS | **12** | chatgpt, gemini, grok, kimi, meta, mimo, minimax 2.7, minimax m3, mistral, qwen, sonnet, yuanbao |
| IMPLAUSIBLE | **1** | deepseek |

**72 objections total** (62 from the 11 structured reviews, plus 5 from minimax m3 and 5 from mimo).
Severity across the structured set: 8 fatal, 28 major, 25 minor, 1 "moderate" (yuanbao, off-schema).

### 5.4 The headline: unanimous confirmation of the DRC-drop objection

**All 13 models independently attacked the DRC numbers.** No model let the 214,000 → 340 transition
pass, and no model was asked to look at it specifically.

The attack splits into two related claims, and most models make both:

- **The 214,000 magnitude is too large for 3.8% overflow.** grok: *"Typical first-detail-route DRC
  counts for a 1M-instance block with modest overflow are in the low tens of thousands; 214k implies
  either massive shorts/spacing failures from near-zero free tracks or an unstated technology/rule-deck
  factor."* mimo, independently: *"A more realistic number for 3.8% overflow concentrated in six
  channels might be 20,000–60,000 DRCs."* sonnet rates this **fatal**.
- **The 214,000 → 340 drop in one pass is not achievable from three soft actions.** minimax m3
  (**fatal**): *"a 99.8% reduction without any placement spreading and without rerunning CTS or power.
  Three soft measures cannot plausibly explain that magnitude."* deepseek (**fatal**) proposes the
  realistic figure: *"a reduction from 214k to perhaps 150k–180k after rule relaxation, with the
  majority of violations remaining due to insufficient routing tracks."* minimax 2.7: *"a realistic
  outcome after one repair iteration would be 40–60% violation reduction (214K → 85K–120K)."*

chatgpt alone proposes a **reconciling** correction rather than a numeric one — that the figure may
be *rule-marker instances rather than unique violations*, and that the draft's real defect is failing
to define what it is counting. That is the most useful single correction in the whole set, because it
is the only one that would make both numbers defensible if true.

**The calibration result, and it is the important part.** opus's own `weakest_point` on this episode
reads: *"The claimed DRC drop from 214k to 340 in a single route after these three actions is the
least defensible number — a real recovery of that magnitude usually takes more than one route
iteration."* **The author flagged exactly the claim that 13 independent reviewers then attacked, and
nothing else in the draft drew unanimous fire.** The honesty field predicted the red team. That is
the strongest evidence in the entire collection that `weakest_point` is a real signal — and it is
consistent with `episode-draft-bank.md` §2 Finding 5, where `weakest_point` is useful and
`confidence` is not.

### 5.5 The correction list — convergent objections that survive as required edits

Four objections were raised by 9+ of the 11 structured reviews. Together they are the draft's
correction list.

**C1 — The DRC numbers (13/13).** As above. **Required edit:** define what is being counted (unique
violations vs rule-marker instances), and either reduce the first-pass figure to the tens of
thousands or report the intermediate state after the repair iterations rather than a single-pass
drop. Severity: fatal (3 models), major (6), minor (4).

**C2 — "NDR relaxation" is the wrong lever, or the wrong word (10/11 structured, plus mimo).** The
strongest technical objection in the set, and the models converge on the mechanism: relaxing a
non-default rule that specifies *wider* spacing or width **consumes more track resource, not less**,
so it should worsen a track-starved channel. grok: *"The useful lever in a pin-access/macro-channel
bottleneck is usually the opposite: tighter rules, double-cut vias, or preferential use of higher
layers that still have free tracks."* minimax 2.7 and deepseek both rate it **fatal**.

Three distinct corrected versions are offered, and they are not equivalent:
- *It was a reversion, not a relaxation* — gemini: *"reverted non-critical signal nets from 2S/2W NDRs
  to default rules inside the channel while re-assigning high-speed NDR nets to upper metal layers."*
  chatgpt says the same in schema terms: *"reverting an unnecessarily restrictive NDR toward the legal
  default."* **This is almost certainly what the original episode meant** — and it matches the
  `diagnosis-library.md` FAIL_CONGESTION cause #7, where a blanket NDR is a self-inflicted supply
  reduction.
- *It was layer promotion, not rule change* — grok, mistral.
- *It was a genuine spacing reduction and needs an SI check* — kimi: *"track-optimized NDRs with
  reduced spacing… pre-validated against the foundry signoff DRC deck, and SI analysis confirmed that
  increased coupling did not degrade timing on adjacent critical paths by more than 5 ps."*

**Required edit:** say which of the three it was. The draft's current wording is ambiguous in a way
that makes a correct action look like an incorrect one.

**C3 — The overflow arithmetic and the unchanged-utilization claim (11/11 structured, plus mimo).**
Two coupled problems. First, 3.8% → 0.6% attributed entirely to three local actions: meta proposes
the staged version — *"3.8% → ~1.8% after screens + NDR, then to 0.6% after also thinning PG straps
in channels or adding layer promotion and placement halo, requiring two incremental global route
passes."* Second, a 65% density screen displaces cells by construction, so **utilization cannot be
unchanged at 71.5% unless the displaced cells went somewhere the draft does not mention.** grok:
*"it is implausible that the displaced cells produce zero measurable increase in global utilization
or new secondary congestion."* mimo: *"If cells were moved out of the channels, they went somewhere —
that destination region's density increased."*

**Required edit:** report local density before/after (not just chip-level utilization), and either
show the small global rise (~72–73% per grok) or state explicitly that cells were absorbed into
existing legal whitespace. chatgpt's softer version — describe 71.5% as *"the rounded global
utilization rather than evidence that the placement was otherwise unchanged"* — is the minimum
honest fix.

**C4 — Pin-swap legality on hard macros (10/11 structured, plus mimo).** kimi rates this **fatal**.
The objection is uniform: hard-macro pins are fixed by the IP vendor's internal floorplan; "pin-swap"
is only legal where the macro exposes logically equivalent pin groups, and on an SRAM the
high-fanout pins are usually clocks, resets or wide data buses whose positions cannot move. minimax
m3 adds a magnitude argument: *"Two macros out of 100 with maybe 30–50 high-fanout pins each moves
tens of nets, not the hundreds-to-thousands needed."*

**Required edit:** state what kind of swap (logically equivalent pin group / orientation flip / net
re-assignment on a soft block), and quantify how many nets left the congested channel.

**Secondary convergence (10/11): the −12 ps WNS claim.** Not attacked as impossible — attacked as
under-specified. The models want the corner and mode named, setup vs hold distinguished, and
"recovered later during incremental optimization" replaced with something falsifiable. minimax m3:
*"Do not say 'recovered later during incremental optimization' without naming the mechanism."*

### 5.6 What the red team defends

**9 of 13 name the same element as most defensible: the frozen-floorplan rejection.** meta —
*"exactly the schedule-risk reason a veteran would give"*; minimax 2.7 — *"a genuine organizational
reality, not a plot device"*; qwen, kimi, gemini, grok, yuanbao all agree; grok extends the defence
to the choice of localized density screens as the consequent primary lever.

This is the useful asymmetry: **the decision reasoning survives the red team intact while nearly every
number in the draft is corrected.** Which is precisely the shape the project wants — the episodes are
being collected for their reasoning, and the reasoning is the part that held up.

### 5.7 What the red team says is missing

Convergent `missing_from_story` items, in order of how many models raised them:

1. **Hold timing** — density screens and repair-iteration buffering both move minimum-delay paths, and
   the draft reports setup only.
2. **The power grid's contribution to the channel starvation** — several models note that a frozen
   macro placement usually implies a frozen PG stripe pattern *inside* those channels, which is very
   likely part of the original defect and goes unmentioned.
3. **Layer-by-layer utilization inside the channels, before and after** — without it the NDR-vs-layer
   promotion question (C2) cannot be settled.
4. **SI / crosstalk consequences** of any spacing change on the two mid-layer metals.
5. **Wall-clock time and iteration count** for the recovery.
6. **TNS, not just WNS**; and the corner at which the −12 ps applies.

### 5.8 Adjudication outcome for the episode bank

- **E28 / E64 (opus): recommendation changed from KEEP to KEEP-WITH-CORRECTIONS.** The reasoning and
  the constraint narrative stand; C1–C4 must be applied before the draft is put in front of Alice, so
  that her review time is spent on judgment rather than on catching what 13 models already caught.
- **No other episode was red-teamed.** The J run covers exactly one draft. The other 12 congestion
  episodes in the bank make structurally similar claims — several assert larger DRC collapses than
  the one just unanimously rejected (E7 gemini 14,200 → 42; E46 gemini 24,150 → 118; E19 mimo
  2,417 → 183; E58 mimo 3,842 → 287). **They inherit C1 by analogy** and are already marked DISCARD
  or SALVAGE in §1 on independent grounds.
- **The J prompt should be run against the other DISCARD candidates**, particularly E8 and E47
  (gemini's arithmetically impossible timing episodes). If a 13-model red team reliably converges on
  the same defect a three-line arithmetic check finds, the cheap check can be trusted to triage and
  the expensive review reserved for drafts that survive it.

---

## 5. The L slice — Alpha 21264 recalls, graded against the extraction and the paper

**The `* l.json` set has arrived: 13 files, 52 entries.** Prompt L
(`prompts/PROMPT-L-ALPHA21264-RECALL.md`, L-v1) is D2's format re-pointed at Kessler, *"The Alpha
21264 Microprocessor,"* IEEE Micro 19(2):24–36, 1999 — with a hardened honesty rule: *"REVERSING a
decision the paper actually made … is even worse"* than mislabeling general knowledge.

Graded against `../extractions/Alpha21264.episodes.json` (7 locator-cited episodes) **and** the full
paper text, extracted from the held PDF in this digest. 12 models produced JSON; `mimo l.json` is a
seventh prose refusal, graded from its text.

### 5.1 A caveat about the ground truth itself

**The Alpha PDF has a broken font encoding, and it has silently damaged the extraction.** The
`direct_quote` field of every episode in `Alpha21264.episodes.json` is unusable — e.g.
`"accuracyYthanYlargerYtablesYofYeitherYindividual"`. The PDF's embedded Type-3 subset maps space→`Y`,
hyphen→`r`, period→`s`, comma→`q`, and every digit to a symbol (`w x y z – — “ ’ ﬁ` = 0 1 2 3 4 5 6 7 9).
Letters survive, so the prose is readable and the extraction's *content* fields are sound — but its
quotes are not quotes, and **any digit in that PDF is unrecoverable by text search.**

Two consequences, both important:
1. **The extraction's `direct_quote` field silently failed its purpose** and nobody would notice
   without opening the file. `VERIFIED-SOURCES.md` records this PDF as having *"clean text
   (`pdftotext`/`pypdf` confirmed) for locator-cited extraction"* — **that assessment is wrong for
   this file.**
2. **Numeric claims in this section are graded against the paper's figure captions** (which survived
   as literal text: *"Data cache (64 Kbytes, two-way)… Integer issue queue (20 entries)… Integer
   register file (80)… Floating-point register file (72)"*), not against body text.

### 5.2 The grading

| Model | Entries | CONFIRMED | PARTIAL | NOT-IN-PAPER | CONTRADICTED |
|---|---|---|---|---|---|
| chatgpt | 5 | **5** | — | — | — |
| meta | 5 | **5** | — | — | — |
| gemini | 4 | **4** | — | — | — |
| deepseek | 5 | **5** | — | — | — |
| grok | 5 | 4 | 1 | — | — |
| qwen | 3 | **3** | — | — | — |
| sonnet | 2 | **2** | — | — | — |
| glm 5.3 Flash | 5 | 2 | 2 | 1 | — |
| yuanbao | 5 | 3 | 1 | — | 1 |
| kimi | 5 | 3 | 1 | — | 1 |
| minimax 2.7 | 5 | 1 | 2 | 2 | — |
| minimax m3 | 3 | 2 | 1 | — | — |
| mimo *(prose)* | 5 | 2 | 1 | 1 | 1 |
| **Total** | **57** | **41 (72%)** | **9 (16%)** | **4 (7%)** | **3 (5%)** |

### 5.3 What checks out — and one genuinely impressive recall

**Unanimously correct core.** Tournament branch predictor (10 models), clustered integer execution
with duplicated register files (9), line-and-way prediction (5), double-pumped data cache (3) — all
CONFIRMED against both the extraction and the paper. meta reproduces the exact figure-caption numbers
(duplicated 80-entry integer register files, 64 KB two-way data cache) and names both the load-wait
table and load hit/miss prediction correctly.

**The standout: chatgpt's "skew cache-fill writes by a cycle" (conf 0.98).** The paper says: *"The
data that crosses the data buses in cycle 0 gets skewed to cycle 2 and written into the cache. This
skew is for performance reasons only — the fill data could have been written in cycle 1 instead, but
pipeline conflicts would allow fewer load and store issues."* That is a paragraph-level implementation
detail with a stated rejected alternative, recalled accurately — and it is **not among the
extraction's 7 episodes**, which is the clearest possible demonstration that the extraction is a
sample rather than an index. chatgpt went 5-for-5 on this paper after inverting POWER4's central
decision, which is a useful reminder that recall accuracy is per-paper, not just per-model.

**A naming nuance the corpus got right.** meta and the extraction both say *"load-wait table"*; the
paper uses **both** *"load wait table"* and *"store wait table"* for the same structure, in adjacent
sentences. Not an error by either.

### 5.4 The errors

**CONTRADICTED (3):**
- **yuanbao L51** — *"80 physical registers (40 integer + 40 floating point)"*. Figure 2 gives **80
  integer** (per cluster, duplicated) **and 72 floating-point**. The same entry adds an 8-bit "inum",
  a reorder buffer and "collapsible" issue queues — *inum*, *reorder buffer* and *collapsible* all
  have **zero hits** in the paper. **This is yuanbao's only non-`confident` entry of the five
  (`probably-in-the-paper`, 0.7) and its only wrong one — the honesty field isolated the bad entry
  exactly.**
- **kimi L27** — *"deep pipeline optimized for clock frequency."* The paper states the pipeline *"has
  seven stages, similar to the earlier in-order 21164,"* with the map stage as the one notable
  addition. The 21264 is not presented as a pipeline-deepening-for-frequency design; that framing is
  imported from the Pentium 4 era.
- **mimo** — *"large instruction window (up to 80 instructions in-flight)."* 80 is the integer
  register file depth, not an in-flight instruction count. A number correctly recalled and attached to
  the wrong quantity.

**NOT-IN-PAPER (4):** minimax 2.7's *"GAg vs GAs"* predictor taxonomy (zero hits — imported academic
nomenclature) and its *"unified reservation stations"* alternative (the paper never discusses
reservation stations); glm's *"non-blocking caches with a large write buffer"* as stated (the
mechanism is an eight-entry miss address file, described differently); mimo's *"streaming buffers."*

**PARTIAL (9)** are mostly right-substance / imported-vocabulary: glm's *"age-based selection"* is
the paper's *"issues the oldest two queued instructions each cycle"*; glm's *"physical register file
rather than a ROB"* has the right numbers but an alternative the paper never weighs; yuanbao's
*"32 outstanding loads and 32 outstanding stores"* is unverifiable (digits destroyed) against a paper
that specifies an **eight-entry** miss address file; grok's *"large in-flight window"* against a
20-entry integer queue.

### 5.5 The finding that matters: L inverted D2's failure mode

| | D2 (POWER4) | L (Alpha 21264) |
|---|---|---|
| Gradable claims | 37 | 57 |
| CONFIRMED | 62% | **72%** |
| CONTRADICTED | **19%** | **5%** |
| Direction reversals of a central decision | **3** (clock philosophy) + 3 others | **0** |

**Zero models reversed a central decision on the Alpha paper**, against three who reversed POWER4's
clock philosophy. Two candidate explanations, and they are separable by experiment:

1. **The prompt.** L-v1 added the explicit anti-reversal warning that D2-v4 lacked. If that is the
   cause, the warning is nearly free and should be back-ported to D2 immediately.
2. **The paper.** The Alpha 21264's decisions (tournament predictor, clustering, double-pumping) are
   famous, distinctive and named; POWER4's are guiding-principle prose that is easy to smooth into a
   generic "balanced design" narrative — which is precisely the shape all three inversions took.

**The tie-breaker is cheap:** re-run D2 with L's anti-reversal warning added and nothing else changed.
If the inversions vanish, it was the prompt.

**A second, softer finding: the honesty field over-corrected here.** qwen and sonnet both marked the
tournament predictor `from-general-Alpha-knowledge-not-necessarily-this-paper` (conf 0.6 and 0.25) —
it is unambiguously in the paper, with a labelled block diagram. sonnet also marked the clustering
entry `probably-in-the-paper` at 0.4; it is verbatim in the extraction and the paper. **Under-claiming
is the safe direction and both were being appropriately careful — but it means `paper_vs_general`
cannot be used as a positive filter, only as a negative one.** Combined with §3.4's finding that one
inversion was self-marked `confident`, the honest summary is: *the field flags roughly the right
entries when it fires, and it fires inconsistently.*

### 5.6 Consequence for the extraction pipeline

The five held PDFs have now produced two independent grading passes (D2/POWER4 and L/Alpha) with
consistent results: **models recall the famous, distinctive decisions well and confabulate the
surrounding rationale** — yield arguments, power arguments, rejected alternatives that were never
weighed. That pattern argues for a specific division of labour:

- **Locator-cited extraction from the PDF** (the parallel session's `extractions/`) for anything that
  will carry a claim.
- **Model recall** used only as a *retrieval hint* — a cheap way to find which parts of a paper are
  worth extracting — never as content.

And one concrete repair: **re-extract the Alpha episodes with a font-aware text pipeline** so the
`direct_quote` field carries real quotes, and correct `VERIFIED-SOURCES.md`'s "clean text" assessment
for that file.

---

## 5b. The M and N slices — Pentium 4 and POWER4 circuit/physical recalls

Graded the same way for the cross-paper scorecard (`recall-scorecard.md`). Both target papers passed
the space-ratio encoding check.

| | M — Pentium 4 (ITJ 2001) | N — POWER4 circuit/physical (IBM JRD 2002) |
|---|---|---|
| Files / entries | 13 / 52 | 13 / 48 |
| CONFIRMED | 42 (81%) | 36 (75%) |
| PARTIAL | 5 | 4 |
| NOT-IN-PAPER | 5 | 8 |
| **CONTRADICTED** | **0** | **0** |

**Grading note:** M and N were graded by keyword-anchored spot-check against the full text rather than
claim-by-claim as D2 and L were. Confirmations are sound; the PARTIAL/NOT-IN-PAPER counts are lower
bounds.

**M highlights.** chatgpt's *"keep the high-speed integer ALU loop deliberately small"* is the
paper's staggered-add design (*"only a 16-bit adder and its input muxes need to be completed in a fast
clock cycle"*) — CONFIRMED. minimax 2.7's *"126 instructions in flight"* is exact. Two era-marketing
terms are absent from the source: **"hyper-pipelined" appears zero times** in the ITJ paper (the paper
says *"20-stage misprediction pipeline"*), and **no 10 GHz target is stated** — minimax 2.7's
*"targeting 10GHz at 0.18µm"* is NOT-IN-PAPER.

**N highlights — the best single recall in the whole collection.** grok's
*"global slew-rate limit of one-third cycle time"* is verbatim: *"A global slew rate limit equal to one
third of the cycle time was set and enforced for all signals (local and global) across the whole
chip."* Its *"selective, late-binding use of low-Vt devices"* is equally exact: *"desirable to use
these low-Vt devices selectively… ground rules allowed swapping from normal Vt to low Vt at the last
moment."* This is the paper closest to Alice's own domain, and grok recalled it at circuit-designer
resolution.

**N errors.** gemini's *"selective dynamic compound domino logic in execution datapaths"* — dynamic
circuits are real in the paper but confined to *"some of the register files, array circuitry, and some
circuitry in the load/store unit"*, not the execution datapaths (PARTIAL). chatgpt's
*"silicon full-frequency testing as a final timing-validation mechanism"* has no support
(NOT-IN-PAPER). minimax's *"differential domino clock distribution"* and *"distributed voltage
regulation"* are both NOT-IN-PAPER. `minimax m3 n.json` is a prose refusal — its **first**, joining
mimo's eight.

**Another under-claim.** qwen's *"latch-based timing methodology with cycle stealing"* is marked
`from-general-POWER4-knowledge-not-necessarily-this-paper` at **0.35** — and the paper devotes a
figure to it (*"Split-latch clocking diagram. c1 and c2 latches are transparent on alternate
half-cycles, allowing logic to propagate through successive cycles"*). Third instance of qwen or
sonnet under-claiming a correct recall.

---

## 6. The O slice — Niagara recalls, adjudicated

**13 files, 59 entries.** Prompt O (`prompts/PROMPT-O-NIAGARA-RECALL.md`, O-v1) against Kongetira,
Aingaran & Olukotun, *"Niagara: A 32-Way Multithreaded SPARC Processor,"* IEEE Micro 25(2):21–29,
2005. Graded against `../extractions/Niagara.episodes.json` (6 locator-cited episodes) **and** the
full paper text, extracted here with the space-ratio sanity check recommended in `MISSED.md` §1f —
**this PDF passes (0.131), unlike the Alpha one.**

### 6.1 Result

| Grade | Count | Share |
|---|---|---|
| CONFIRMED | 47 | 80% |
| PARTIAL | 2 | 3% |
| NOT-IN-PAPER | 10 | 17% |
| **CONTRADICTED** | **0** | **0%** |

**Zero inversions — the second paper in a row with none**, and the best confirmed rate of the five
recall slices. But the NOT-IN-PAPER share is the highest of any slice, and it is not evenly spread:
**10 of 10 come from just six entries' worth of real error plus one catastrophic file.**

### 6.2 The finding: one model answered the wrong paper — three times

**`glm 5.3 flash o.json` contains Alpha 21264 content.** Its five entries are *"Departure from the
21164: out-of-order execution combined with high clock frequency"*, *"two integer clusters with
duplicated register files"*, *"register renaming into enlarged physical register files (80 integer /
72 FP)"*, *"large on-chip L1 caches with the second-level cache moved off-chip"*, and a
local+global+chooser branch predictor. That is the L-slice paper, verbatim in substance, submitted
as an answer about a 32-thread SPARC chip.

**It did the same thing for M and N.** `glm 5.3 flash m.json` (Pentium 4) and
`glm 5.3 flash n.json` (POWER4 circuit/physical) contain **the identical five Alpha entries** —
byte-for-byte the same titles and decisions as its O file. One answer, submitted four times, for four
different papers, three of them wrong.

Four of the five entries are marked `confident-this-is-in-the-paper`, at 0.75–0.90.

**This is a failure mode nothing else in the collection exhibits**, and it is invisible to every check
the pipeline has: the JSON is well-formed, the schema is satisfied, the honesty fields are populated,
the entries are internally coherent and — for the L paper — *substantively correct*. Only comparing
the content against the requested paper catches it. Whether the cause is the model, the session, or
the human paste step cannot be determined from the artefacts; what is determinable is that **15 of
glm 5.3 flash's 20 recall entries are answers to a question nobody asked.**

**Mechanical guard, cheap:** score each recall file for paper-specific keyword overlap with its target
paper before grading (Niagara: *thread group, crossbar, Sparc pipe*; Pentium 4: *trace cache, µop,
NetBurst*). glm's O file would score near zero against Niagara and near maximum against Alpha.

### 6.3 The other NOT-IN-PAPER entries — a single shared error

Excluding glm, five entries are NOT-IN-PAPER and **three of them are the same claim**: a *single
shared floating-point unit across all eight cores* (gemini O12 at `confident`/0.95; grok O24 at
`probably`/0.75; kimi O28 at `probably`/0.75).

**The words *floating point*, *FPU* and *floating-point unit* appear zero times in this paper.** The
single shared FPU is a famous and true fact about UltraSPARC T1 — it is simply not in this article.
This is the exact failure the prompt names as its primary target: general-processor knowledge
labelled as paper content. **Two of the three models marked it `probably-in-the-paper`; gemini marked
it `confident` at 0.95.**

The remaining two: minimax m2.7's *"minimal branch prediction hardware vs sophisticated predictor"*
(the paper mentions branch prediction only once, in the introduction's critique of ILP designs, and
states no Niagara branch-prediction decision) and minimax m3's *"eliminating an external
northbridge"* (zero hits).

**PARTIAL (2):** kimi's *"in-order execution pipeline"* — true, but the paper says *"single-issue
pipeline with six stages"* and never uses the phrase; and minimax m3's *"round-robin"* thread
scheduling — the paper describes a priority scheme that deprioritizes speculative threads, not
round-robin.

### 6.4 What checks out — including three obscure details

The throughput-over-ILP philosophy, four-threads-per-pipe grouping, the crossbar to a shared banked
L2, and the memory-bandwidth motivation are unanimous and all CONFIRMED against both the extraction
and the paper. Three deeper recalls stand out because they are the kind of detail that separates
reading a paper from knowing a chip:

- **sonnet O54** — *"random L1 instruction-cache replacement instead of LRU, for area savings."*
  Paper: *"We implement a random replacement scheme for area savings, without incurring significant
  performance cost."* Verbatim, and not in the extraction's 6 episodes.
- **sonnet O53** — *"split working-set / architectural-set register file instead of a single large
  multiported SRAM."* Paper: *"The set of registers visible to a thread is the working set, and we
  implement it using fast register file cells. The complete set of registers is the architectural
  set; we implement it using compact six-transistor SRAM cells. A transfer port links the two."*
- **yuanbao O59** — the coherence protocol at full precision: *"L1 caches are write-through with
  allocate-on-load and no-allocate-on-store; the L2 maintains a directory that shadows the L1 tags."*
  Every clause matches the paper.

meta and yuanbao both reproduce the exact cache configuration (16 KB I / 8 KB D, 4-way; 3 MB L2,
4-banked, 12-way; four DDR2 controllers, >20 GB/s).

### 6.5 Salvage: yuanbao's out-of-schema enum value

`yuanbao o.json` entry O57 carries, in the `paper_vs_general` field:

> `"confident-this-is-in-the-paper for the simple-pipeline decision; power/area numbers are from-general-Niagara-knowledge-not-necessarily-this-paper"`

The schema demands exactly one of three enum values; this is free text containing two of them, scoped
to different clauses of the same entry. Strict enum validation would reject the entry.

**Salvaged by splitting it into its two scoped labels**, and both check out: the simple-pipeline
decision is CONFIRMED, and the power/area figures were correctly withheld from the confident claim
(≈60 W *is* in the paper, so this is a conservative self-label, not an error).

**Worth noting rather than penalizing.** The model produced a **more informative** honesty label than
the schema permits — per-clause provenance instead of per-entry — and the only thing wrong with it is
that the field is typed as an enum. That is a schema limitation, not a model failure, and the obvious
fix is to allow an optional free-text `provenance_note` alongside the enum. It is the one instance in
the whole collection of a model straining *against* a schema in the direction of more honesty.

---

## 7. Appendix — all 266 rejected alternatives, grouped by failure class

The `candidates_considered` / `rejected_because` pairs are the highest-yield artefact of the episode
runs: even where an episode's numbers are junk, a rejection that cites a concrete cost (schedule,
area, risk, IR, downstream churn) is reusable as differential-diagnosis and annotation scaffolding.
All 266 are reproduced below with their originating model and run, deduplicated only by exact
repetition. Bland entries are retained deliberately — the density of *cost types* is part of what
Alice would be judging.

Counts by class: FAIL_CONGESTION 91, FAIL_TIMING 89, SDC_BUDGET 86.


### FAIL_CONGESTION — 91 rejected alternatives

- **Reduce target utilization across the affected region by about 8 percentage points and rerun placement through route.**  
  ↳ rejected: The estimated placement-to-route restart would cost roughly 1.5 to 2 days, and moving the surrounding logic was expected to invalidate already-closed clock and timing relationships.  
  ↳ `chatgpt/R1`
- **Move one of the three memory macros by roughly 20um to widen the central channel.**  
  ↳ rejected: The macro was already tied closely to a power-grid strap and clock-tree topology; moving it would require PG and CTS ECO work and carried a realistic risk of several hundred additional downstream changes.  
  ↳ `chatgpt/R1`
- **Add routing resources by relaxing selected noncritical upper-metal constraints and reserve extra tracks globally for the affected layer range.**  
  ↳ rejected: A broader routing-rule change could increase coupling and antenna/DRC risk elsewhere and would require another detailed-route signoff pass, with little guarantee that the narrow corridor itself would improve enough.  
  ↳ `chatgpt/R1`
- **Respin floorplan to spread macros and widen channels**  
  ↳ rejected: schedule risk: would add 2 weeks of physical re-implementation and re-verification, missing tapeout deadline.  
  ↳ `deepseek instant/R1`
- **Increase placement utilization target to 75% to force cells out of congested areas**  
  ↳ rejected: would worsen congestion by increasing cell density in already crowded bins, likely increasing DRCs.  
  ↳ `deepseek instant/R1`
- **Add an extra metal layer for routing**  
  ↳ rejected: mask cost and fab schedule change unacceptable at this stage; would also require new PDK validation.  
  ↳ `deepseek instant/R1`
- **Move macro floorplan to widen memory channels by 15um**  
  ↳ rejected: Requires full floorplan re-spins, invalidates top-level power grid, and causes a 3-week schedule delay.  
  ↳ `gemini/R1`
- **Apply a global placement density limit reduction from 75% to 65%**  
  ↳ rejected: Pushes logic into peripheral blocks, causing WNS degradation of over 300ps on long critical paths and severe area bloat.  
  ↳ `gemini/R1`
- **Rip up clock tree and re-run global placement from scratch**  
  ↳ rejected: High risk of unresolvable timing closure churn across all clock domains two weeks before target tapeout.  
  ↳ `gemini/R1`
- **Full floorplan rework: move SRAMs apart by 30µm to widen the channel**  
  ↳ rejected: Re-floorplan at post-CTS means redoing placement and CTS (~1.5-2 weeks) and invalidates already-signed-off macro pin alignment with the top level; schedule slip past tape-in milestone.  
  ↳ `glm 5.3/R1`
- **Drop placement utilization globally from 74% to 65% to give the router breathing room**  
  ↳ rejected: Block area is fixed by the top-level budget; reducing utilization means growing the block, which breaks the chip-level floorplan and reopens top-level routing.  
  ↳ `glm 5.3/R1`
- **Congestion-driven cell padding / NDR on the whole bus**  
  ↳ rejected: Applying keep-out/padding broadly adds area and can worsen timing on already-critical paths; NDRs on a wide bus inside a dense channel typically make overflow worse, not better.  
  ↳ `glm 5.3/R1`
- **Rip up entire placement and re-floorplan with 20-micron macro spacing across the block**  
  ↳ rejected: 3-week schedule impact; would invalidate completed CTS, all clock tree optimization, and require re-running placement through route closure, pushing tape-out past the hard deadline.  
  ↳ `kimi/R1`
- **Add full placement blockages in the congested channel to force cells out**  
  ↳ rejected: Would raise utilization in remaining regions to >90%, triggering new congestion hotspots in the standard-cell core and degrading timing from high-density placement.  
  ↳ `kimi/R1`
- **Swap macro orientations to open pins away from the channel**  
  ↳ rejected: SRAM macros have fixed pin locations on all four edges per the memory compiler; rotation does not change which edge faces the channel, and flipping would misalign power straps, risking IR drop violations.  
  ↳ `kimi/R1`
- **Increase die area 3% to drop utilization to 72%**  
  ↳ rejected: Requires top-level floorplan re-signoff and bump map invalidation, 2-week schedule hit, impacts all blocks.  
  ↳ `meta/R1`
- **Flip every other SRAM macro 180deg to stagger pins**  
  ↳ rejected: Risk of timing regression on 87 macros, requires full CTS rerun, estimated IR increase +8mV on flipped orientation.  
  ↳ `meta/R1`
- **Lower utilization 5% via placement blockage in channel**  
  ↳ rejected: Pushes cells into already congested periphery, adds 5% area penalty and does not solve pin-access root cause.  
  ↳ `meta/R1`
- **Apply non-default routing rule widening M2 pitch in channel**  
  ↳ rejected: Widening pitch reduces available tracks further and worsens pin access, increases overflow to 3.1% in trial run.  
  ↳ `meta/R1`
- **Rip up and re-place the two SRAM macros with 60 um wider spacing, then re-run CTS and routing from scratch**  
  ↳ rejected: Would push effective utilization above 78% in the surrounding region, require full CTS re-run (~18 hours), and add an estimated 5 calendar days to the schedule. The placement team had already iterated the floorplan twice and the macro positions were locked by the top-level abutment plan.  
  ↳ `mimo/R1`
- **Add M2/M3 routing blockages in the congested channel and force all signals to upper metals (M4–M6)**  
  ↳ rejected: Upper metal sheet resistance is 2.3x higher than M2/M3 at this node. Forcing ~1,800 nets to upper metals would degrade path delay by an estimated 50–80 ps on critical paths routed through that region, pushing WNS past the -0.25 ns budget threshold.  
  ↳ `mimo/R1`
- **Reduce local cell density in the hotspot by 8% using cell inflation, then re-optimize timing**  
  ↳ rejected: Would require re-optimization of the entire block's timing (estimated 3 days), and the inflated cells would push neighboring regions toward their own congestion thresholds. The timing team judged the risk of cascading congestion as unacceptable this late in the flow.  
  ↳ `mimo/R1`
- **Swap pin access on both SRAM macros to redistribute ~40% of signal traffic from the narrow north-side channel to the wider south-side access corridor, combined with targeted ECO re-placement of ~200 cells in the hotspot**  
  ↳ rejected: None  
  ↳ `mimo/R1`
- **Global cell spreading + utilization target drop to 65%**  
  ↳ rejected: Re-routing iteration: 4 days + risks hold degradation on near-critical paths already passing; does not address macro pin escape which is the actual source.  
  ↳ `minimax m3/R1`
- **Switch M3/M4 layer assignment to double-patterning-friendly directions**  
  ↳ rejected: Library/preferred direction constraints make this infeasible without re-placing macros; macro placement is frozen by upstream signoff dependency.  
  ↳ `minimax m3/R1`
- **Widen the macro channel by 15um and shove macros outward symmetrically**  
  ↳ rejected: Risks IR/SSN degradation on the 6 analog macros (layout-dependent effects); would require analog re-simulation, ~2 week slip.  
  ↳ `minimax m3/R1`
- **Asymmetric channel widening: 10um into the non-analog row only + targeted pin-spreading on the bounding macros**  
  ↳ rejected: None  
  ↳ `minimax m3/R1`
- **Re-run global placement with congestion-aware cost weight increased from 0.3 to 0.8**  
  ↳ rejected: Adds 2 days to schedule with no guarantee the hotspot will resolve given macro positions are fixed  
  ↳ `mistral/R1`
- **Insert congestion-guided buffers in hotspot region**  
  ↳ rejected: Increases area by 0.4% and degrades IR drop by 3mV, risking hold violations on 12 identified paths  
  ↳ `mistral/R1`
- **Swap macros M17 and M23 to open routing channel**  
  ↳ rejected: Requires re-running timing for both macro domains (estimated 1.2 days CPU) and risks breaking existing timing closure  
  ↳ `mistral/R1`
- **Rework the floorplan: widen the six west-edge macro channels and re-place macros to open routing corridors.**  
  ↳ rejected: Macro placement was frozen because top-level feedthrough and power-grid stripe locations were derived from it and already integrated at the top level; changing it would force a top-level re-integration and a fresh power/IR sign-off, estimated 2.5-3 weeks against 9 days of schedule.  
  ↳ `opus 5/R1`
- **Reduce overall placement utilization from 71.5% to ~64% by growing the block outline.**  
  ↳ rejected: Block outline was fixed by the top-level partition; growth would take area from the neighbouring block and, in any case, treats a local defect with a global remedy - the channel supply does not increase when the whole block gets sparser.  
  ↳ `opus 5/R1`
- **Re-run placement with a global congestion-driven effort setting bumped to high and let the tool spread everything.**  
  ↳ rejected: Discards a placement that CTS was already built on; the clock tree would have to be rebuilt and all post-CTS timing work redone, costing 3-4 full flow days with no guarantee the tool would treat the channels differently, since its own cost function had already chosen them.  
  ↳ `opus 5/R1`
- **Push the block to route with DRC waivers and fix violations manually in the last days.**  
  ↳ rejected: 214k violations is far beyond manual-repair scale, and shipping unrouted shorts creates downstream churn - every ECO after that point would be against a database that cannot be signed off.  
  ↳ `opus 5/R1`
- **Increase block utilization to 88% and shrink the floorplan.**  
  ↳ rejected: It would exacerbate the existing 14% congestion and likely push overflow >25%, causing unrouteable hotspots and massive DRC violations.  
  ↳ `qwen/R1`
- **Rip up and re-run CTS with higher clock tree latency targets (skew relaxation).**  
  ↳ rejected: It would degrade WNS by at least 100ps, pushing timing into critical failure, and require a full re-optimization cycle costing 3 days of schedule.  
  ↳ `qwen/R1`
- **Add routing blockages on M5/M6 in the congested channels to force CTS to route clocks on M7/M8.**  
  ↳ rejected: M7/M8 are reserved for power straps in this 16nm kit; using them for signal routing violates the power grid methodology and causes severe IR drop issues.  
  ↳ `qwen/R1`
- **Full re-placement with lower global target utilization**  
  ↳ rejected: would require re-running placement through CTS, costing ~2 weeks of schedule with re-validation of clock structure; risk of introducing new hold violations elsewhere  
  ↳ `sonnet/R1`
- **Reposition the macro cluster**  
  ↳ rejected: macros were locked by an upstream floorplan partition agreement with the packaging team; moving them would break pin alignment on an adjacent hard-macro bus and required a floorplan sign-off re-cycle  
  ↳ `sonnet/R1`
- **Add a routing layer / change layer assignment in that region**  
  ↳ rejected: reticle/stack was fixed for this tapeout; adding a layer was a mask-cost and schedule non-starter this late  
  ↳ `sonnet/R1`
- **Targeted ECO placement blockage + local cell spreading with incremental route**  
  ↳ rejected: None  
  ↳ `sonnet/R1`
- **Re-floorplan: move 4 macros to create wider routing channels**  
  ↳ rejected: Would invalidate CTS (8 days to rebuild) and re-place 1.2M cells (5 days); tapeout in 11 days; aggregate re-spin risk >60%  
  ↳ `tencent yunbao/R1`
- **Add M8-M9 routing layers via metal option**  
  ↳ rejected: Requires metal stack change: new mask set (+$120K, 2-week foundry lead time); misses tapeout window by 3 days  
  ↳ `tencent yunbao/R1`
- **Partial pin-swap on macros + targeted cell padding in hotspots + selective net promotion to upper layers**  
  ↳ rejected: NOT rejected - chosen as best schedule-risk tradeoff  
  ↳ `tencent yunbao/R1`
- **Reduce cell util target from 81% to 72% via placement blockages**  
  ↳ rejected: Requires re-placing entire block (4 days) + re-CTS (2 days); similar schedule risk to re-floorplan with lower efficacy for macro-channel congestion  
  ↳ `tencent yunbao/R1`
- **Reduce overall placement density by approximately 5 percentage points and repeat placement, CTS, and route.**  
  ↳ rejected: This would consume at least one full closure iteration and risk perturbing clock-tree and timing results that were already substantially converged; it also addressed block-wide density rather than the localized channels.  
  ↳ `chatgpt/R2`
- **Move several SRAM macros to widen the congested channels.**  
  ↳ rejected: The SRAMs were already aligned with power-grid and floorplan constraints, so macro movement would require floorplan, power-grid, CTS, and timing revalidation with a high risk of several days of downstream churn.  
  ↳ `chatgpt/R2`
- **Globally relax selected routing constraints and increase routing resources on the affected layers.**  
  ↳ rejected: A global routing-rule change could trade the local problem for coupling, antenna, or DRC problems elsewhere and would require another detailed-route signoff pass.  
  ↳ `chatgpt/R2`
- **Redo floorplan to widen macro channels by 2 µm each**  
  ↳ rejected: schedule: would require re-initializing placement and clock-tree synthesis, adding 5 days to the tapeout timeline, which is not acceptable.  
  ↳ `deepseek/R2`
- **Increase cell density target to 78% to push logic away from channels**  
  ↳ rejected: would increase global congestion elsewhere and likely worsen overall DRC count, with negligible effect on channel-specific overflow.  
  ↳ `deepseek/R2`
- **Add a dedicated metal-layer route guide to restrict the channels to use only M2–M4**  
  ↳ rejected: would reduce routing resources in those areas and could increase via count, leading to IR-drop issues; not a net gain.  
  ↳ `deepseek/R2`
- **Move SRAM clusters 25um apart to widen routing channels**  
  ↳ rejected: Invalidates top-level power grid rail alignment, requiring full top-level floorplan ECO and adding 2 weeks to schedule.  
  ↳ `gemini/R2`
- **Apply 100% hard placement blockages in inter-macro channels**  
  ↳ rejected: Pushes all channel logic to core periphery, increasing path lengths and degrading setup WNS by an estimated 280ps into failing territory.  
  ↳ `gemini/R2`
- **Lower global block target placement utilization from 78% to 70%**  
  ↳ rejected: Expands overall block footprint beyond die boundary constraints, causing physical overlap with adjacent partition blocks.  
  ↳ `gemini/R2`
- **Shift two SRAM rows to widen the worst channels**  
  ↳ rejected: Macro positions were signed off against the top-level pin assignment and power grid; moving them reopens the top-level integration review and forces a full re-place/re-CTS — estimated 10-12 working days against a tape-in checkpoint in 4 weeks.  
  ↳ `glm 5.3/R2`
- **Drop block utilization from 72% to ~62% and re-place everything**  
  ↳ rejected: Block boundary is frozen by the chip floorplan; lower utilization means a larger block area, which the top level cannot absorb, and a full re-place invalidates the clean post-CTS timing anyway.  
  ↳ `glm 5.3/R2`
- **Turn up routing effort/layer-tapering globally and iterate detailed route**  
  ↳ rejected: Two overnight attempts already showed shorts moving around rather than clearing (3,900 → 3,100 → 3,350); pure effort escalation burns 2 days of machine time while the track-supply problem stays.  
  ↳ `glm 5.3/R2`
- **Rip up entire placement, increase all macro spacing by 15 microns, and re-run placement through CTS**  
  ↳ rejected: 4-week schedule impact; invalidates completed CTS, all clock tree optimization, and extracted parasitics; risks new timing convergence issues and would push tape-out past the hard deadline.  
  ↳ `kimi/R2`
- **Remove all clock buffers from the macro channels via manual ECO and relocate them to the core**  
  ↳ rejected: Would degrade clock skew by approximately 80ps, violating the 50ps skew budget and creating hold violations across more than 200 paths; hold closure would require buffer insertion, re-creating the congestion.  
  ↳ `kimi/R2`
- **Add full placement blockages in all three macro channels to prevent any cell insertion**  
  ↳ rejected: Would push approximately 15,000 cells into already-dense standard-cell regions, raising core utilization above 90% and triggering new congestion hotspots with cascading timing degradation.  
  ↳ `kimi/R2`
- **Expand floorplan 4% to reduce utilization to 68%**  
  ↳ rejected: Requires top-level re-integration and bump re-spin, 10-day schedule hit and area cost ~0.8mm2, invalidates pinout.  
  ↳ `meta/R2`
- **Rotate 50% of SRAMs 90deg to spread pins**  
  ↳ rejected: Requires full CTS rebuild, risk of timing regression >100ps on 400MHz domain and IR drop +12mV, needs Liberty re-char.  
  ↳ `meta/R2`
- **Insert hard placement blockage 8um in channels to force spreading**  
  ↳ rejected: Pushes cells to already dense periphery, worsens WNS by 60ps and still leaves pin access issue, area penalty.  
  ↳ `meta/R2`
- **Apply non-default rule doubling M2 pitch in channel**  
  ↳ rejected: Reduces available tracks further, trial run increased overflow to 3.1% and added 15% runtime.  
  ↳ `meta/R2`
- **Widen the four macro channels by 15 um each, re-running placement and CTS from scratch**  
  ↳ rejected: The floorplan was locked by the top-level integration team. Moving macros would shift port locations on the block boundary, requiring top-level re-integration. Estimated schedule impact: 8–10 days. The tape-out date was 5 weeks away.  
  ↳ `mimo/R2`
- **Add M2 routing blockages in the congested channels and force all traffic to M3–M5**  
  ↳ rejected: M2 blockages would push ~2,400 nets to upper metals. M3 sheet resistance at 28nm is 1.8x M2; forcing critical-path nets to detour through M3–M5 would degrade setup timing by an estimated 40–70 ps. The post-CTS WNS margin was only 12 ps — no timing budget to spend.  
  ↳ `mimo/R2`
- **Reduce standard-cell density by 5% in the congested quadrants using cell inflation, then re-route**  
  ↳ rejected: Cell inflation in two quadrants would require re-optimization of the entire block's timing (estimated 2 days runtime plus 1 day of engineer review). The timing team judged the risk of creating new violations in adjacent regions as unacceptable given the schedule.  
  ↳ `mimo/R2`
- **Rotate 14 of the 82 macros 90 degrees to reorient their pin rows from channel-parallel to channel-perpendicular, redistributing pin access from M2 to M3/M4, combined with adding soft M2 keep-out zones (not hard blockages) along the four congested channels**  
  ↳ rejected: None  
  ↳ `mimo/R2`
- **Re-run global placement with congestion-aware cost weight increased from 0.4 to 0.9**  
  ↳ rejected: Adds 1.5 days to schedule with no guarantee of fixing channel-specific hotspots given fixed macro positions  
  ↳ `mistral/R2`
- **Swap SRAM macros M42 and M65 to open channel between M42-M45 cluster**  
  ↳ rejected: Requires re-running timing for both macro domains (estimated 1.0 day CPU) and risks breaking existing timing closure in both domains  
  ↳ `mistral/R2`
- **Manually add routing guides around congested channels**  
  ↳ rejected: Requires manual creation of 50+ guides, error-prone and not scalable; estimated 0.8 days of engineer time  
  ↳ `mistral/R2`
- **Re-place the SRAM stacks to widen the 7 channels and open proper routing corridors.**  
  ↳ rejected: Macro placement had already been exported upward: top-level feedthrough locations and the power-grid stripe pattern were derived from it and integrated. Moving macros forces top-level re-integration plus a fresh IR/EM sign-off on the rebuilt grid, estimated 2.5-3 weeks against 8 days of schedule.  
  ↳ `opus/R2`
- **Drop overall placement utilization from 70% to ~62% by growing the block outline.**  
  ↳ rejected: The outline is fixed by the top-level partition, so the area would have to come out of the neighbouring block, and the remedy does not address the defect anyway - thinning the whole block does not add a single M3 track between two abutting SRAMs.  
  ↳ `opus/R2`
- **Re-run placement from scratch with global congestion effort raised to high.**  
  ↳ rejected: Throws away the placement the clock tree was built on, so CTS and all post-CTS timing work is redone: 3-4 full flow days, and no reason to expect a different outcome, since the tool's own cost function had already chosen those channels once at high effort.  
  ↳ `opus/R2`
- **Route with DRC waivers and clean up the residue by hand in the final days.**  
  ↳ rejected: 175k violations is three orders of magnitude beyond manual-repair scale, and every subsequent ECO would be made against a database that cannot be signed off - the downstream churn swamps the days it appears to save.  
  ↳ `opus/R2`
- **Add routing blockages over the channels to keep signal routing out of them entirely.**  
  ↳ rejected: The channels are the only path from the logic core to the SRAM pins on the far side; blocking them converts a congestion problem into an unroutable-by-construction one, and it also strands the CTS trunks already built through them.  
  ↳ `opus/R2`
- **Increase block utilization to 85% and shrink floorplan.**  
  ↳ rejected: It would compress the macro channels further, pushing vertical overflow >30% and guaranteeing unrouteable hotspots, requiring a full floorplan re-spin that costs 2 weeks.  
  ↳ `qwen/R2`
- **Rip up CTS and re-run with higher latency/skew targets to force clock routing to M6/M7.**  
  ↳ rejected: M6/M7 are reserved for power straps in this 28nm kit; using them for clock routing violates the power grid methodology and causes >15% IR drop violations.  
  ↳ `qwen/R2`
- **Add routing blockages on M4/M5 in the congested channels to force standard cell routing to M3.**  
  ↳ rejected: M3 is already 90% utilized for local logic; forcing more M3 routing would cause massive via congestion and increase detailed route DRCs by an estimated 500+, blowing the schedule.  
  ↳ `qwen/R2`
- **Increase detailed router effort: higher rip-up count, more iterations, aggressive congestion-driven re-route**  
  ↳ rejected: The overflow is structural (physical channel capacity exceeded by macro packing), not a search deficiency. Additional router effort had already been tried at global route stage (3 iterations with increasing effort, overflow only dropped from 22% to 19%). Each detailed-routing iteration with high effort consumes ~6 hours on the shared farm and the schedule allows only 2 more routing attempts before the integration deadline. Effort would not resolve a physical capacity issue.  
  ↳ `solar pro/R2`
- **Apply layer directives to force more routing onto lower-priority metals (M5/M6) in congested channels**  
  ↳ rejected: The 28nm process has only 6 routing layers; M5/M6 already carry 60% of the routing in those channels per the global route report. Forcing more traffic onto layers already near capacity would create new DRC violations (min-width and spacing on tighter-pitch lower layers) and likely increase antenna violations. The foundry PDK restricts M5/M6 antenna current limits below what additional routing would draw.  
  ↳ `solar pro/R2`
- **Re-run placement with more aggressive spreading to open macro channels, then re-CTS and re-opt**  
  ↳ rejected: A full placement refresh plus re-CTS and post-CTS optimization would consume 3-4 days of engineer time plus 2 days of compute on the farm — blowing past the integration milestone by 5 days. The block is already at 76% utilization; spreading risks pushing utilization above 80% in adjacent regions, creating new congestion. The post-CTS WNS of +0.24ns is acceptable; re-CTS could degrade it.  
  ↳ `solar pro/R2`
- **Reduce macro halo sizes on the 78 SRAM macros from 12um to 8um, freeing channel width for routing while accepting a slight DRC risk that can be waived post-tapeout**  
  ↳ rejected: None  
  ↳ `solar pro/R2`
- **Re-floorplan to widen all macro channels chip-wide**  
  ↳ rejected: would require re-running placement and CTS from scratch, costing an estimated 3 weeks and reopening already-signed-off clock tree QoR, unacceptable this late in the schedule  
  ↳ `sonnet/R2`
- **Globally lower target utilization to open up routing headroom everywhere**  
  ↳ rejected: utilization was already fine outside the channels — a global relaxation would burn area budget chip-wide to fix a problem that was localized to <10% of the block  
  ↳ `sonnet/R2`
- **Route through the power straps by relaxing keepout rules in the affected channels**  
  ↳ rejected: IR-drop and electromigration sign-off had already been closed against the existing keepout spec; relaxing it risked a full power-integrity re-verification pass with uncertain outcome  
  ↳ `sonnet/R2`
- **Locally widen only the three affected channels via targeted macro nudging (legal micro-placement move within existing floorplan bounds) plus manual routing guides**  
  ↳ rejected: None  
  ↳ `sonnet/R2`
- **Re-floorplan: move 12 SRAM macros to create wider routing channels**  
  ↳ rejected: Would invalidate CTS (5 days to rebuild) and re-place 1M cells (3 days); tapeout in 9 days; aggregate re-spin risk >50%  
  ↳ `yuanbao/R2`
- **Add M7-M8 routing layers via metal option**  
  ↳ rejected: 28nm process does not offer additional layers; would require migrate to 16nm, impossible within schedule  
  ↳ `yuanbao/R2`
- **Partial pin-swap on macros + targeted cell padding in hotspots + selective net promotion to upper layers**  
  ↳ rejected: NOT rejected - chosen as best schedule-risk tradeoff  
  ↳ `yuanbao/R2`
- **Reduce cell util target from 75% to 65% via placement blockages**  
  ↳ rejected: Requires re-placing entire block (3 days) + re-CTS (2 days); similar schedule risk to re-floorplan with lower efficacy for macro-channel congestion  
  ↳ `yuanbao/R2`

### FAIL_TIMING — 89 rejected alternatives

- **Upsize the top violating combinational cells and insert additional buffers on the worst paths.**  
  ↳ rejected: The affected path count was too large for a local ECO strategy, and widespread upsizing was projected to increase dynamic and leakage power while potentially worsening congestion in an already moderately utilized region.  
  ↳ `chatgpt/R1`
- **Run a broad placement/timing optimization pass to re-place the 428 violating endpoints.**  
  ↳ rejected: A global optimization would consume a full closure iteration and risk perturbing paths that were already positive, with no evidence yet that the required-time calculation itself was correct.  
  ↳ `chatgpt/R1`
- **Add a multicycle exception across the clock-domain boundary to remove most of the reported setup failures.**  
  ↳ rejected: The design intent had not established a multi-cycle transfer; adding the exception merely to improve the report would create a functional signoff risk and could mask a real interface requirement.  
  ↳ `chatgpt/R1`
- **Upsize 100 cells along the data paths to gain 80 ps**  
  ↳ rejected: area +2% and power +3% with only marginal gain; would also require re-placement of surrounding cells.  
  ↳ `deepseek instant/R1`
- **Swap to lower-Vt libraries for all failing paths**  
  ↳ rejected: leakage power would increase ~15%, exceeding the chip's standby budget; thermal risk.  
  ↳ `deepseek instant/R1`
- **Respin clock tree to rebalance skew**  
  ↳ rejected: schedule: would require 3 days of clock-tree re-synthesis and full STA re-run, pushing other signoff activities.  
  ↳ `deepseek instant/R1`
- **Upsize registers and insert pipeline stages along failing paths**  
  ↳ rejected: Inserts unnecessary latency and logic overhead without fixing the fundamental 1-cycle setup check across asynchronous domains.  
  ↳ `gemini/R1`
- **Increase clock drive strength and apply extreme path weighting during optimization**  
  ↳ rejected: Distorts local placement, exacerbates local power/area, and fails to close timing because the physical path delay exceeds single-cycle targeting.  
  ↳ `gemini/R1`
- **Set a multicycle path constraint of 2 cycles without checking CDC synchronization logic**  
  ↳ rejected: Risks masking structural CDC bugs if hardware handshaking or synchronizer flops are absent.  
  ↳ `gemini/R1`
- **Fix hold per-path with buffers on 3,900 endpoints**  
  ↳ rejected: 3,900 hold buffers add area and setup degradation on paths already at +0.011 ns slack, plus 1-2 days of ECO/route iterations and DRC risk in already route-critical areas.  
  ↳ `glm 5.3/R1`
- **Relax the hold constraint (loosen uncertainty / remove on-chip-variation derating on hold)**  
  ↳ rejected: That masks the signature instead of fixing it; hold analysis credibility is lost and the bug reappears at silicon with real skew.  
  ↳ `glm 5.3/R1`
- **Claim the paths are false paths / multicycle and waive them**  
  ↳ rejected: The endpoints are real launch-capture pairs in the same domain at the same edge; waiving thousands of same-shift transfers is exactly how hold escapes reach silicon.  
  ↳ `glm 5.3/R1`
- **Insert buffers on all 4,200 failing paths**  
  ↳ rejected: Would add approximately 120,000 buffer instances (8% area increase, significant power cost), and would not fix a systematic 0.22ns gap that is identical across all paths regardless of load.  
  ↳ `kimi/R1`
- **Reduce clock skew between clk_core and clk_io via clock tree rework**  
  ↳ rejected: Current skew is already <50ps; a 0.22ns gap cannot be closed by skew tuning alone. Rework would require 2 weeks and risk hold violations across the design.  
  ↳ `kimi/R1`
- **Rip up placement and spread logic to reduce wire delay**  
  ↳ rejected: Paths are already distributed across the die with no clustering; spreading would increase wire length and worsen timing, while invalidating CTS and route closure.  
  ↳ `kimi/R1`
- **Upsize drivers on failing paths and add useful skew**  
  ↳ rejected: Would add 12% area and 18mW leakage for no benefit since root is input arrival, and increases IR drop in dense input cluster.  
  ↳ `meta/R1`
- **Re-place input flops closer to pads**  
  ↳ rejected: Requires IO movement risking DRC, 3-day schedule cost, does not fix 0.7*clock input delay which remains unrealistic.  
  ↳ `meta/R1`
- **Insert pipeline stage after inputs**  
  ↳ rejected: Changes latency visible to system, requires RTL change and re-verification, not allowed in ECO window.  
  ↳ `meta/R1`
- **Run incremental placement and routing focused on the 23 failing paths with aggressive cell sizing**  
  ↳ rejected: The paths were already physically short and well-routed (no detours, clean layers). Physical optimization would not address the root cause. The runtime cost was estimated at 6–8 hours with low probability of closing 312 ps on paths that were already near-optimal physically.  
  ↳ `mimo/R1`
- **Add buffer trees on the 3 launch nets to improve drive strength**  
  ↳ rejected: The launch nets were already buffered (2–3 stages). Adding more buffers would increase insertion delay on the non-violating paths sharing those nets, potentially creating new violations. The estimated gain was 30–50 ps, insufficient to close 312 ps.  
  ↳ `mimo/R1`
- **Upsize cells on the 23 critical paths to next-higher drive strength**  
  ↳ rejected: Cells were already at X4 or X8 drive. Upsizing to X16 would add approximately 15% area in the local region and gain only ~30 ps per stage (90–150 ps total across 3–5 levels), still insufficient. Power increase was judged unacceptable for the gain.  
  ↳ `mimo/R1`
- **Review SDC constraints for the clock domain crossing between async_rst and core_clk; add set_false_path or set_clock_groups as appropriate**  
  ↳ rejected: None  
  ↳ `mimo/R1`
- **Run buffer/eco-placement on the failing cones**  
  ↳ rejected: Would buy at most 30-50ps per hop; failing slacks are 180ps+, so 3-4 buffer hops needed per path = ~12K cells of churn, high risk of new hold/DRC, addresses symptom not cause.  
  ↳ `minimax m3/R1`
- **Re-synthesize the fanin logic with different area/delay**  
  ↳ rejected: Logic is locked by architecture team; downstream ECO only is the agreed scope.  
  ↳ `minimax m3/R1`
- **Modify SDC: re-derive the output port's output delay to match realistic loading/capture, or correct the input arrival that was set conservatively upstream**  
  ↳ rejected: Risks regressing other passes; requires signoff re-validation. But this addresses the reported cluster signature directly.  
  ↳ `minimax m3/R1`
- **Reduce the clock skew pessimism on the failing clock domain by ~30ps via CTS-only adjustment**  
  ↳ rejected: Skew was already within spec; only buys 30ps of the 210ps gap.  
  ↳ `minimax m3/R1`
- **Relax setup constraint on CLK_A by 50ps**  
  ↳ rejected: Would mask real timing issues in paths not affected by skew, risking silicon failure in other domains  
  ↳ `mistral/R1`
- **Upsize all drivers on failing paths**  
  ↳ rejected: Increases area by 0.6% and power by 2.1%, plus creates new congestion in already-tight regions  
  ↳ `mistral/R1`
- **Re-synthesize entire CLK_A domain logic**  
  ↳ rejected: Requires 3 days of runtime and could introduce new timing violations while not addressing root cause  
  ↳ `mistral/R1`
- **Start incremental timing optimization on the 4,200 endpoints immediately, since the schedule was tight and the tool could be running overnight.**  
  ↳ rejected: Optimizing against a wrong constraint burns real area and power buying margin that does not exist, and the resulting upsized, buffer-heavy netlist has to be reverted once the constraint is fixed - a full day of tool time plus an untangling cost on top of it.  
  ↳ `opus 5/R1`
- **Assume a placement regression and re-run placement with tighter timing effort.**  
  ↳ rejected: The netlist and floorplan were byte-identical to the previous run; spending a 6-hour placement cycle to test a hypothesis already falsified by the inputs is unaffordable in a daily-turn schedule.  
  ↳ `opus 5/R1`
- **Declare the core-to-peripheral crossings asynchronous and set_false_path them, which would have made all 3,900 failures disappear immediately.**  
  ↳ rejected: The two clocks are synchronous and phase-related by construction; a false path there hides real single-cycle transfers and would defer a genuine functional hold/setup failure to silicon, which is the most expensive place to find it.  
  ↳ `opus 5/R1`
- **Relax the clock uncertainty on the peripheral domain to absorb the shortfall.**  
  ↳ rejected: 1.35 ns is roughly a full half-period of margin - far outside any defensible uncertainty budget - so this would be disguising a constraint error as pessimism removal and would silently corrupt every later margin decision on that domain.  
  ↳ `opus 5/R1`
- **Upsize the drivers on the 3 shared sink pins to reduce cell delay.**  
  ↳ rejected: It would add ~40% capacitance load to the preceding stage, shifting the bottleneck and likely degrading the overall WNS by another 50ps without fixing the root constraint mismatch.  
  ↳ `qwen/R1`
- **Re-run synthesis with higher effort and boundary optimization.**  
  ↳ rejected: The identical slack across 4,000+ paths is a mathematical signature of a constraint boundary issue, not a logic optimization plateau; re-running would just waste 12 hours of compute and yield the same cliff.  
  ↳ `qwen/R1`
- **Add a 50ps timing margin to the clock latency in the SDC.**  
  ↳ rejected: It masks the symptom without fixing the underlying path grouping, and would artificially tighten timing on the rest of the block, causing false failures in subsequent P&R.  
  ↳ `qwen/R1`
- **Globally increase drive strength / re-buffer across the whole failing set**  
  ↳ rejected: would blow the switching-power/ODC budget already near its cap, and does nothing to fix a constraint-modeling problem — treats symptom for one group and wastes the schedule window  
  ↳ `sonnet/R1`
- **Re-characterize clock uncertainty for all domains**  
  ↳ rejected: would mask the real physical issue in the tail group and risks silently under-constraining paths that are legitimately tight  
  ↳ `sonnet/R1`
- **Blanket ECO re-route of all 850 failing paths**  
  ↳ rejected: unnecessary churn on the 600 paths that were a constraint artifact, with real risk of new DRC and schedule cost disproportionate to the actual physical problem  
  ↳ `sonnet/R1`
- **Split fix: refine SDC clock latency/uncertainty modeling for the bulk group; targeted ECO buffer insertion and local re-route for the tail group**  
  ↳ rejected: None  
  ↳ `sonnet/R1`
- **Full timing-driven P&R optimization (useful skew, layer opt, cell sizing) on 1,415 paths**  
  ↳ rejected: Would consume 3+ days of ECO iterations to recover 150-190ps across 1,415 paths; low probability of full closure; massive downstream DRC churn; likely to degrade other paths  
  ↳ `tencent yunbao/R1`
- **Insert multicycle 2 constraint on register-file write paths**  
  ↳ rejected: NOT rejected - chosen after RTL verification  
  ↳ `tencent yunbao/R1`
- **Reduce CPU clock from 1.5GHz to 1.0GHz**  
  ↳ rejected: Unacceptable performance regression (-33%); product spec mandates 1.5GHz minimum; would lose customer commitment  
  ↳ `tencent yunbao/R1`
- **Pipeline register file interface (add 1 stage)**  
  ↳ rejected: Requires RTL change: 2-week re-verification cycle; misses tapeout by 10 days  
  ↳ `tencent yunbao/R1`
- **Upsize cells and insert buffers on the worst violating cones.**  
  ↳ rejected: The violations were distributed across hundreds of endpoints, so broad upsizing would add area and power while increasing congestion before establishing that the required arrival times were correct.  
  ↳ `chatgpt/R2`
- **Run a global placement/timing optimization pass focused on the violating endpoints.**  
  ↳ rejected: The optimization would risk moving already-clean logic and consume a closure iteration, while the common-clock signature provided stronger evidence for a constraint issue than a placement issue.  
  ↳ `chatgpt/R2`
- **Add a broad multicycle exception between the two clock domains.**  
  ↳ rejected: No architectural evidence established that the transfers were intentionally multi-cycle; suppressing the violations would create a functional signoff risk and could mask a real timing requirement.  
  ↳ `chatgpt/R2`
- **Upsize 150 cells along the data paths to gain 90 ps**  
  ↳ rejected: area +3% and power +4%, with marginal improvement and risk of new hold violations.  
  ↳ `deepseek/R2`
- **Swap to lower-Vt libraries for all failing paths**  
  ↳ rejected: leakage power would exceed the standby budget by 12%, causing thermal issues.  
  ↳ `deepseek/R2`
- **Re-synthesize the clock tree to balance the skew**  
  ↳ rejected: would require 2 days of clock tree re-build and full STA re-run, delaying other signoff tasks.  
  ↳ `deepseek/R2`
- **Insert 3 pipeline register stages across all 2,000 cross-domain data paths**  
  ↳ rejected: Consumes unnecessary area, alters pipeline latency, requires extensive RTL churn, and adds 10 days to schedule.  
  ↳ `gemini/R2`
- **Apply high-effort physical optimization and buffer upsizing during P&R post-CTS**  
  ↳ rejected: Wastes tool runtime, inflates power and cell count, and cannot close timing because physical delay cannot cover an invalid single-cycle setup check.  
  ↳ `gemini/R2`
- **Set multicycle path constraint of 2 cycles across the boundary without RTL audit**  
  ↳ rejected: Risks masking true single-cycle timing requirements if any path lacks dual-flop synchronization logic.  
  ↳ `gemini/R2`
- **More placement/timing optimization effort: bind the cone tighter, upscale gates, push the router**  
  ↳ rejected: On logic-limited paths the physical engine typically recovers 30-50 ps; the deficit is ~200 ps, so this burns 2-3 days of iterations and leaves the block fundamentally unclosable.  
  ↳ `glm 5.3/R2`
- **Treat it as a constraint problem and relax the clock or claim the paths false**  
  ↳ rejected: The paths are real same-edge transfers on the operating frequency promised in the spec; relaxing SDC hides the deficit and moves the failure to silicon or to the SoC integration schedule.  
  ↳ `glm 5.3/R2`
- **Pipeline the cone with a new register stage at the cone output**  
  ↳ rejected: A visible pipeline register changes the block's cycle-accurate interface contract (one-cycle latency on the bank's outputs), rippling into the block-level verification environment and the receiving block — a 4-6 week churn, too late for this revision.  
  ↳ `glm 5.3/R2`
- **Add a pipeline register to break the 12,000 fanout paths**  
  ↳ rejected: The source register output feeds a protocol state-machine enable signal that must remain single-cycle relative to the data path; adding latency would break functional correctness and require RTL redesign with 3-week verification impact including formal property checking.  
  ↳ `kimi/R2`
- **Rip up placement and spread the 12,000 destinations away from the source to reduce wire delay**  
  ↳ rejected: The violation is identical to both near and far destinations, proving wire delay is not the dominant term. Spreading would increase average wire length, potentially worsening timing, and would require full re-placement (2-week schedule hit) with no expected benefit.  
  ↳ `kimi/R2`
- **Upsize the source register to the largest available drive strength**  
  ↳ rejected: The source is already the largest drive strength (X8) in the standard cell library. Further upsizing is impossible without buffer insertion, which would add gate delay and increase area without resolving the logic-depth deficit.  
  ↳ `kimi/R2`
- **Upsize entire failing logic cone and add 120ps useful skew**  
  ↳ rejected: Adds 11% area and 15mW leakage for 10k paths that are constraint-driven, increases IR 9mV in input cluster with no benefit.  
  ↳ `meta/R2`
- **Re-place input flops 2um closer to pads**  
  ↳ rejected: Requires IO re-spin, 2-day schedule cost, does not fix 1.2ns input delay that is still 0.6x period and unrealistic.  
  ↳ `meta/R2`
- **Pipeline after inputs adding flop stage**  
  ↳ rejected: Changes latency 1 cycle, requires RTL change and full re-verification, not allowed in ECO window.  
  ↳ `meta/R2`
- **Relax clock uncertainty from 120ps to 250ps**  
  ↳ rejected: Hides real margin, risks hold and top-level failures, violates signoff methodology.  
  ↳ `meta/R2`
- **Run incremental placement and routing on the 31 failing paths with aggressive cell sizing and Vt swap**  
  ↳ rejected: The paths were already physically short and well-routed. Physical optimization on 2–4 logic levels would gain at most 30–50 ps per path, insufficient to close 287 ps. Runtime: 4–6 hours with near-zero probability of success.  
  ↳ `mimo/R2`
- **Add buffer trees on the 2 launch nets to improve drive strength and reduce delay**  
  ↳ rejected: The launch nets were already buffered (2 stages). Adding buffers would increase insertion delay on the non-violating paths sharing those nets. Estimated gain: 20–40 ps, still insufficient for 287 ps.  
  ↳ `mimo/R2`
- **Upsize all cells on the 31 critical paths to maximum drive strength**  
  ↳ rejected: Cells were already at X4 or X8. Upsizing to X16 would gain ~25 ps per stage (50–100 ps total across 2–4 levels), still insufficient. Area increase of ~12% in the local region was judged unacceptable for the marginal gain.  
  ↳ `mimo/R2`
- **Add set_clock_groups -asynchronous between aon_clk and core_clk in the SDC, or add set_false_path -from [get_clocks aon_clk] -to [get_clocks core_clk]**  
  ↳ rejected: None  
  ↳ `mimo/R2`
- **Relax setup constraint by 10% across the block**  
  ↳ rejected: Would mask real timing issues in other quadrants, risking silicon failure in non-congested regions  
  ↳ `mistral/R2`
- **Upsize all drivers on failing paths**  
  ↳ rejected: Increases area by 0.8% and power by 3.0%, plus creates new congestion in an already-tight top-right quadrant  
  ↳ `mistral/R2`
- **Re-synthesize logic in top-right quadrant only**  
  ↳ rejected: Requires 2 days of runtime and could introduce new timing violations while not addressing the physical routing cause  
  ↳ `mistral/R2`
- **Launch incremental timing optimization on the 4,200 endpoints overnight, since schedule was tight and the tool was otherwise idle.**  
  ↳ rejected: Optimizing against a wrong constraint spends real area and leakage buying margin that does not exist, and the upsized, buffer-heavy result has to be reverted once the constraint is corrected - a day of tool time plus a non-trivial untangling cost, on a netlist that was correct to begin with.  
  ↳ `opus/R2`
- **Suspect a placement or flow regression and re-run placement with higher timing effort.**  
  ↳ rejected: Inputs were byte-identical to the passing run, so the hypothesis was already falsified before the run started; a 6-hour placement cycle to test it is unaffordable on a daily-turn schedule.  
  ↳ `opus/R2`
- **Declare the core-to-peripheral crossings asynchronous and set_false_path them - which would have cleared 3,900 violations in one line.**  
  ↳ rejected: The two clocks are synchronous and phase-related by construction. A false path removes setup and hold checking on genuine single-cycle transfers, deferring a real functional failure to silicon, which is the most expensive place to find one.  
  ↳ `opus/R2`
- **Absorb the shortfall by relaxing clock uncertainty on the peripheral domain.**  
  ↳ rejected: 1.35 ns is roughly a full half-period - far outside any defensible uncertainty budget - so this disguises a constraint error as pessimism removal and corrupts every subsequent margin judgement on that domain.  
  ↳ `opus/R2`
- **Upsize the drivers on the 2 shared sink pins to reduce cell delay.**  
  ↳ rejected: It would add ~35% capacitance load to the preceding stage, shifting the bottleneck and likely degrading the overall WNS by another 40ps without fixing the root constraint mismatch.  
  ↳ `qwen/R2`
- **Re-run synthesis with higher effort and boundary optimization.**  
  ↳ rejected: The identical slack across 3,000+ paths is a mathematical signature of a constraint boundary issue, not a logic optimization plateau; re-running would waste 10 hours of compute and yield the same cliff.  
  ↳ `qwen/R2`
- **Add a 30ps timing margin to the clock latency in the SDC.**  
  ↳ rejected: It masks the symptom without fixing the underlying path grouping, and would artificially tighten timing on the rest of the block, causing false failures in subsequent P&R.  
  ↳ `qwen/R2`
- **Run aggressive retiming and logic duplication to break the 3-cycle sequential chain and reduce logic depth**  
  ↳ rejected: The chain is a functional pipeline (write-back through 4 pipeline stages with inter-stage registers already in place); further logic duplication would violate the pipeline protocol and could break the design functionally. The 14 cells are already pipeline registers — duplicating them destroys the pipeline structure. Also, retiming on 3,412 paths would consume 2-3 days of engineer time and the farm compute, with no guarantee of resolving the root cause if the problem is a constraint error.  
  ↳ `solar pro/R2`
- **Apply a global setup optimization pass with higher effort on all 3,847 paths**  
  ↳ rejected: The violation shape (concentrated on 14 cells, clean hold) indicates the optimizer is correctly optimizing to the wrong constraints. More optimization effort on unconstrained paths will not fix incorrectly constrained paths — it will just burn schedule (1-2 days of compute on the farm for a full-chip high-effort setup pass) and potentially degrade hold timing by inserting unnecessary buffers. The clean hold timing is a strong signal that the problem is constraint-specific, not a general logic-depth issue.  
  ↳ `solar pro/R2`
- **Re-place the 14 hot cells to improve their routing and reduce wireload**  
  ↳ rejected: The violation shape does not correlate with physical location — the 14 cells are spread across the physical design in different congestion regions, and their violating paths terminate in different physical areas. A placement fix would not address a constraint problem. Re-placement of 14 cells would also risk disrupting the carefully balanced pipeline placement that was tuned for the 800 MHz domain, potentially creating new violations.  
  ↳ `solar pro/R2`
- **Audit the clock specification for the 800 MHz cache domain: verify clock uncertainty, check for missing multicycle pathExceptions on the 3-cycle sequential chain (which legitimately has a 3-cycle latency requirement per the microarchitecture spec), verify that the 14 pipeline registers are correctly grouped in the SDC**  
  ↳ rejected: None  
  ↳ `solar pro/R2`
- **Apply one global fix (e.g. across-the-board re-buffering) to all 640 failing paths**  
  ↳ rejected: would burn power/area budget re-buffering the constraint-artifact group unnecessarily and still not fix the logic-depth group, which needs re-pipelining, not buffering  
  ↳ `sonnet/R2`
- **Re-run synthesis with tighter global constraints to force the tool to close everything**  
  ↳ rejected: risks over-constraining the majority group that was actually fine, and doesn't address the physical clustering in the smallest group at all — high risk of new violations elsewhere with no guarantee of fixing the real outliers  
  ↳ `sonnet/R2`
- **Treat the whole failing set as a single congestion-driven issue and re-place the block**  
  ↳ rejected: only ~80 of 640 failing paths were physically clustered; re-placing the whole block to fix 12% of the failures would be schedule-disproportionate and would perturb the other two groups' timing unpredictably  
  ↳ `sonnet/R2`
- **Split fix by group: refine clock uncertainty for the affected domain; insert a pipeline register on the high-fanout structure; targeted route/ECO in the clustered macro channel**  
  ↳ rejected: None  
  ↳ `sonnet/R2`
- **Full timing-driven P&R optimization (useful skew, layer opt, cell sizing) on 980 paths**  
  ↳ rejected: Would consume 3+ days of ECO iterations to recover 140-160ps across 980 paths; low probability of full closure; massive downstream DRC churn; likely to degrade other paths  
  ↳ `yuanbao/R2`
- **Insert multicycle 2 constraint on ALU output paths**  
  ↳ rejected: NOT rejected - chosen after RTL verification  
  ↳ `yuanbao/R2`
- **Reduce CPU clock from 1.2GHz to 800MHz**  
  ↳ rejected: Unacceptable performance regression (-33%); product spec mandates 1.2GHz minimum; would lose customer commitment  
  ↳ `yuanbao/R2`
- **Pipeline ALU interface (add 1 stage)**  
  ↳ rejected: Requires RTL change: 2-week re-verification cycle; misses tapeout by 12 days  
  ↳ `yuanbao/R2`

### SDC_BUDGET — 86 rejected alternatives

- **Keep the original 0.60ns output requirement for Block A and solve it with additional buffering and cell upsizing.**  
  ↳ rejected: Meeting the tighter budget was estimated to require roughly 4-6% additional cell area in the interface cone and would likely increase local congestion and leakage for only an interface-level accounting decision.  
  ↳ `chatgpt/R1`
- **Make the budgets symmetric at 1.0ns per block and rely on the end-to-end path to determine whether either side needed tightening later.**  
  ↳ rejected: This would remove useful block-level guardrails and could allow Block B to consume far more than its demonstrated need, creating substantial integration churn when the final top-level path budget was re-established.  
  ↳ `chatgpt/R1`
- **Declare the interface false-path because the transfer was architecturally associated with a decoupled control mechanism.**  
  ↳ rejected: The interface still carried data consumed synchronously in the active mode; removing the timing requirement would create a real functional signoff hole rather than solve a budget-allocation problem.  
  ↳ `chatgpt/R1`
- **Tighten the inter-block budget from 2.0 ns to 1.8 ns to force faster logic**  
  ↳ rejected: would require resizing ~50 cells in both blocks, adding 3% area and 4% power, and delay the integration schedule by 1 week for re-synthesis.  
  ↳ `deepseek instant/R1`
- **Increase the clock period of the 1.5 GHz domain to 1.2 GHz to create margin**  
  ↳ rejected: would reduce overall CPU performance by ~20%, failing the performance target.  
  ↳ `deepseek instant/R1`
- **Insert a manual pipeline register at the boundary**  
  ↳ rejected: would add a full cycle of latency that breaks the handshake protocol; not functional.  
  ↳ `deepseek instant/R1`
- **Apply a 70/30 budget shift favoring Block B (875ps for Block A, 375ps for Block B)**  
  ↳ rejected: Over-constrains Block A internal logic, creating 120ps of setup violations inside Block A where pipeline stages cannot be added.  
  ↳ `gemini/R1`
- **Flatten Block A and Block B into a single sub-system for top-level P&R**  
  ↳ rejected: Exceeds runtime memory limits causing tool instability, breaks modular floorplanning, and disrupts concurrent multi-team block layout workflows.  
  ↳ `gemini/R1`
- **Relax input/output delay constraints on both blocks without top-level budgeting validation**  
  ↳ rejected: Passes block-level STA but guarantees massive top-level setup violations during chip-level timing signoff.  
  ↳ `gemini/R1`
- **Keep the 50/50 split and push the inner block harder (more pipelining)**  
  ↳ rejected: Adding a pipeline stage changes the bus protocol, ripples into verification and the neighbor's latency assumptions, and costs 3+ weeks of rework — to satisfy a budget that was arbitrary in the first place.  
  ↳ `glm 5.3/R1`
- **Declare the crossing multicycle (2-cycle) to relieve pressure**  
  ↳ rejected: The bus is a same-cycle request path in the protocol; a multicycle would be a false claim on real transfers and would hide genuine silicon risk at frequency.  
  ↳ `glm 5.3/R1`
- **Tighten the budget on the neighbor and take margin there without rebalancing formally**  
  ↳ rejected: Informal margin theft disappears from SDC, so the next owner re-derives 50/50 and the whole negotiation repeats; constraint provenance is lost.  
  ↳ `glm 5.3/R1`
- **Tighten Block A internal timing target by 0.25ns to force the tool to optimize interface paths harder**  
  ↳ rejected: Block A is already at 85% utilization with congestion overflow 8% near macro boundaries; further tightening would force larger cells into congested regions, likely causing placement legalization failures and routing DRCs, requiring a 2-week iteration cycle.  
  ↳ `kimi/R1`
- **Relax Block B internal target by 0.20ns and absorb the slack into the interface budget**  
  ↳ rejected: Block B has 40 macros with tight pin-access requirements; relaxing timing would force larger drive-strength cells near macro boundaries, exacerbating existing pin-access congestion and risking DRC violations from insufficient routing tracks.  
  ↳ `kimi/R1`
- **Add a pipeline register at the A-to-B interface**  
  ↳ rejected: The interface protocol is single-cycle handshaking with no latency tolerance; adding a register would break functional correctness and require an RTL change with 4-week schedule impact, including re-verification of the protocol state machine.  
  ↳ `kimi/R1`
- **Keep 50/50 and upsize Block A output logic**  
  ↳ rejected: Costs 4% area in A and +22mW dynamic power for marginal benefit, creates IR hotspot near output pins.  
  ↳ `meta/R1`
- **Move to 40/60 giving more to B (0.4ns A, 0.6ns B)**  
  ↳ rejected: Makes A WNS worse to -210ps requiring floorplan change, no benefit as B already has slack.  
  ↳ `meta/R1`
- **Add false path between blocks and rely on top-level closure**  
  ↳ rejected: Hides real timing, risk of silicon failure at 1GHz, violates methodology and would be caught in top-level STA.  
  ↳ `meta/R1`
- **Re-derive budget allocating 70% of top-level margin to block A and 30% to block B**  
  ↳ rejected: Block A's physical-design team stated they could not meet the tighter output-delay budget without a floorplan change to bring the blocks closer. The top-level floorplan was already committed for the next shuttle run, and a floorplan change would slip the tape-out by 3 weeks.  
  ↳ `mimo/R1`
- **Add set_max_delay on the inter-block paths at top level to relax them by 0.2 ns**  
  ↳ rejected: The SoC integrator rejected this because the inter-block paths were part of a system-level timing requirement verified at chip-level simulation. Relaxing them would violate the system spec and require re-validation with the firmware team, adding 2 weeks.  
  ↳ `mimo/R1`
- **Insert a pipeline register between block A and block B**  
  ↳ rejected: The inter-block data path carried a real-time control signal for a feedback loop with single-cycle latency requirement. Adding a pipeline stage would break the control protocol and require a micro-architecture change to the feedback algorithm.  
  ↳ `mimo/R1`
- **Shift 0.12 ns of budget from block B's input-delay constraint to block A's output-delay constraint, then re-optimize each block independently**  
  ↳ rejected: None  
  ↳ `mimo/R1`
- **Add buffers on the failing inter-block paths to close the 50-150ps setup**  
  ↳ rejected: Buffers must be added in both blocks (interface spans both), requires coordination across two P&R teams; risks hold issues on the return path; schedule cost ~1 week, plus churn.  
  ↳ `minimax m3/R1`
- **Reject the budget split and renegotiate 50/50 between blocks via formal margin**  
  ↳ rejected: Would require both teams to re-time their; ~3 week slip, high risk of regressing closed paths elsewhere.  
  ↳ `minimax m3/R1`
- **Declare the interface paths as false-path (functionally not timing-critical)**  
  ↳ rejected: Interface IS timing-critical for the handshake acknowledgment within the protocol window; false-path would create a silicon bug. Wrong category.  
  ↳ `minimax m3/R1`
- **Declare as multicycle-path with N=2, derive per-block budgets as output_delay=0.4ns on sender side, input_delay=0.4ns on receiver side (50/50)**  
  ↳ rejected: None  
  ↳ `minimax m3/R1`
- **Set fixed budget of 10% of Beta clock period (500ps) for all boundary paths**  
  ↳ rejected: Overly conservative for most paths, would cause unnecessary optimization effort and area increase estimated at 1.2%  
  ↳ `mistral/R1`
- **Mark all boundary paths as false paths**  
  ↳ rejected: Would break functional timing for real synchronous paths and cause silicon failure on boundary registers  
  ↳ `mistral/R1`
- **Use clock latency difference only as budget**  
  ↳ rejected: Ignores clock uncertainty and jitter, which account for ~60ps of the observed failures  
  ↳ `mistral/R1`
- **Keep the 50/50 split and let block B absorb the shortfall through optimization and, if needed, a pipeline stage in the decode.**  
  ↳ rejected: The pipeline stage changes the block's cycle-level interface behaviour, which requires an RTL change, a verification re-run, and agreement from the architecture owner - weeks of downstream churn to solve a constraint-arithmetic problem.  
  ↳ `opus 5/R1`
- **Give block A only 250 ps of output delay budget and hand B 720 ps, matching depth proportionally with margin to spare.**  
  ↳ rejected: It leaves A with essentially no room for the top-level buffering that had not yet been placed; when top-level routing came in worse than the 220 ps estimate, A would have had no absorbing capacity and the shortfall would land on the block that had already been signed off.  
  ↳ `opus 5/R1`
- **Declare the configuration-write subset of the interface a false path, since software writes those registers once at boot and never during traffic.**  
  ↳ rejected: The configuration writes are synchronous transfers in the same clock domain; a false path removes both setup AND hold checking, and the hold check on that short, lightly-loaded path is the one that actually protects it. A boot-time-only path can still be sampled wrong on the cycle after the write if hold is unconstrained, and that failure would be silicon-visible and intermittent.  
  ↳ `opus 5/R1`
- **Widen the assumed top-level interconnect estimate from 220 ps to 400 ps to be safe, shrinking both sides' budgets.**  
  ↳ rejected: Unearned pessimism at the boundary propagates into both blocks' optimization and buys area on both sides; it also destroys the ability to tell later whether a real top-level route regression has occurred, because the estimate no longer tracks anything measured.  
  ↳ `opus 5/R1`
- **Increase the internal block routing budget for Block A from 200ps to 300ps by reducing the off-chip budget to 400ps.**  
  ↳ rejected: The board-level signal integrity team confirmed that 400ps is the absolute minimum required to meet the eye-diagram specs for the PCB traces; reducing it would cause system-level bit errors.  
  ↳ `qwen/R1`
- **Insert a synchronous FIFO (async boundary) between Block A and Block B to break the timing path.**  
  ↳ rejected: It would add 2 cycles of latency to the memory access path, violating the strict performance requirement for the processor's L2 cache miss penalty, and would require 3 weeks of RTL redesign and verification.  
  ↳ `qwen/R1`
- **Relax the clock skew constraint between the two blocks from 50ps to 150ps in the SDC.**  
  ↳ rejected: The two blocks share the same PLL, and the physical distance of the clock tree makes a 150ps skew physically unachievable without adding massive, area-prohibitive clock buffers that would violate the power budget.  
  ↳ `qwen/R1`
- **Keep the even 200ps/200ps split**  
  ↳ rejected: directly caused block A to miss timing by ~60ps in the baseline run — demonstrated failure, not hypothetical  
  ↳ `sonnet/R1`
- **Give nearly all margin to A (e.g. 380/20)**  
  ↳ rejected: starves block B of any headroom for its own future ECOs and doesn't account for B's own margin needs — unrealistic once B's own internal changes are considered, and OCV/derate reserve has to come from somewhere  
  ↳ `sonnet/R1`
- **False-path or multicycle the boundary entirely**  
  ↳ rejected: the interface is a genuine single-cycle timing path in normal operation; false-pathing it would mask real silicon timing risk rather than resolve it — considered dangerous for tapeout  
  ↳ `sonnet/R1`
- **Proportional split based on standard-cell stage-count ratio between A and B (plus a reserved OCV margin)**  
  ↳ rejected: None  
  ↳ `sonnet/R1`
- **Equal split: 250ps A-side, 250ps B-side**  
  ↳ rejected: Block B at -280ps internal WNS leaves only -30ps margin for 250ps boundary budget; insufficient given B's existing struggle; would force massive B-side ECOs with schedule risk  
  ↳ `tencent yunbao/R1`
- **Asymmetric: 350ps A-side, 150ps B-side**  
  ↳ rejected: NOT rejected - chosen as optimal balance  
  ↳ `tencent yunbao/R1`
- **Asymmetric: 400ps A-side, 100ps B-side**  
  ↳ rejected: Too aggressive against A; A needs significant optimization for 320 signals in 350ps when A's internal paths already consume ~200ps of phase; risk of creating A-side violations  
  ↳ `tencent yunbao/R1`
- **No budget - flat top-level implementation**  
  ↳ rejected: Top-level is 3.2M instances; flat STA takes 40+ hours per run; hierarchical budgeting mandatory for schedule  
  ↳ `tencent yunbao/R1`
- **Keep the existing 0.46ns Block A budget and close the remainder with cell upsizing and buffering.**  
  ↳ rejected: The affected interface cones would require additional buffering and upsizing, with likely area and leakage cost and some risk of worsening local congestion, even though the top-level timing budget did not require that severity.  
  ↳ `chatgpt/R2`
- **Split the 2.0ns period symmetrically between the two blocks.**  
  ↳ rejected: A symmetric allocation would discard measured information about the actual receiving-side delay and could allow either block to consume more budget than its implementation needs, causing later integration churn.  
  ↳ `chatgpt/R2`
- **Declare the boundary false-path because the interface is associated with a control protocol rather than ordinary dataflow.**  
  ↳ rejected: The transfer is still synchronously consumed in the active operating mode, so removing the timing requirement would create a functional signoff hole rather than a valid budget derivation.  
  ↳ `chatgpt/R2`
- **Reduce the inter-block budget from 2.5 ns to 2.2 ns to force faster logic**  
  ↳ rejected: would require resizing ~80 cells in both blocks, adding 5% area and 6% power, and delaying integration by 1 week for re-synthesis.  
  ↳ `deepseek/R2`
- **Increase the fast clock period to 1.0 GHz (from 1.5 GHz) to create margin**  
  ↳ rejected: would reduce CPU performance by 33%, failing the performance target.  
  ↳ `deepseek/R2`
- **Insert a pipelined register at the boundary**  
  ↳ rejected: would add a full cycle of latency that breaks the handshake protocol; not functional.  
  ↳ `deepseek/R2`
- **Shift interface budget to 70/30 (1.4ns output delay for A, 0.6ns input delay for B)**  
  ↳ rejected: Over-constrains Block B, forcing B's input registers directly against port boundaries and causing internal setup violations (-180ps WNS) inside Block B.  
  ↳ `gemini/R2`
- **Merge Block A and Block B into a single top-level P&R execution partition**  
  ↳ rejected: Exceeds tool memory capacity, increases P&R turnaround time from 6 hours to 26 hours, and breaks parallel multi-engineer work streams.  
  ↳ `gemini/R2`
- **Relax top-level interface setup checks using set_max_delay 2.4ns across boundary**  
  ↳ rejected: Violates 2.0ns top-level clock period requirement, triggering signoff STA failures during full-chip integration.  
  ↳ `gemini/R2`
- **Keep single-cycle and pipeline the bus at the boundary to meet 900 MHz**  
  ↳ rejected: Two pipeline stages on a 512-bit bus cost real area (~6k cells), push the inner block over its power budget, and — decisive — change the write latency the configuration protocol documents, forcing re-verification of every register access sequence on both blocks (weeks of churn) to satisfy a constraint for a transfer that does not exist.  
  ↳ `glm 5.3/R2`
- **Fix it physically: harder optimization, cell upsizing on the 512 paths**  
  ↳ rejected: A 240 ps deficit at the boundary is far beyond ECO-scale recovery (tens of ps); it would leave the interface red at signoff while consuming days of iterations.  
  ↳ `glm 5.3/R2`
- **Waive the paths as false paths with no documentation**  
  ↳ rejected: An undocumented exception is indistinguishable from a mistake at the next re-derivation; the SDC loses provenance and the waiver silently breaks if the write protocol ever changes.  
  ↳ `glm 5.3/R2`
- **Tighten Block A internal timing target by 0.20ns to force harder optimization on interface paths**  
  ↳ rejected: Block A is already at 82% utilization with 7% congestion near macro boundaries; tightening would force larger drive-strength cells and more aggressive buffering into congested regions, likely pushing congestion above 12% and causing placement legalization failures or routing DRCs, requiring a 2-week iteration cycle.  
  ↳ `kimi/R2`
- **Relax Block B input budget to 0.55ns and absorb the slack into the interface**  
  ↳ rejected: Block B has 30 macros with tight pin access on the interface-facing side; relaxing timing would allow larger cells near those macros, blocking pin-access tracks and creating localized congestion that does not currently exist, risking DRC violations from insufficient routing tracks.  
  ↳ `kimi/R2`
- **Increase the top-level wire budget to 0.35ns by relaxing both block budgets equally**  
  ↳ rejected: The physical distance between Block A and Block B is only 150 microns with ample upper-metal routing layers; 0.20ns is already conservative for the wire. Increasing the wire budget would mask the real problem (Block A's internal congestion) and leave no margin for unexpected detours caused by macro blockages.  
  ↳ `kimi/R2`
- **Keep 50/50 and upsize A output logic**  
  ↳ rejected: Costs 3.5% area and 20mW power, creates IR hotspot near pins, marginal timing benefit only.  
  ↳ `meta/R2`
- **Move to 35/65 giving more to B (0.35ns A, 0.65ns B)**  
  ↳ rejected: Makes A WNS -180ps requiring floorplan change, no benefit as B already has slack, wastes power.  
  ↳ `meta/R2`
- **False path interface and close at top level**  
  ↳ rejected: Hides real timing, risk silicon failure at 800MHz, violates signoff methodology and would be caught in top STA.  
  ↳ `meta/R2`
- **Move block A and block B 800 um closer in the top-level floorplan to match the WLM assumption**  
  ↳ rejected: The top-level floorplan was committed. Moving blocks would shift port locations on the chip boundary, requiring re-validation of the package substrate design (already in fabrication). Schedule impact: 4 weeks minimum. Cost of substrate re-spin: ~$180K.  
  ↳ `mimo/R2`
- **Insert a pipeline register between block A and block B at the top level**  
  ↳ rejected: The inter-block data path carried a single-cycle-latency memory-write acknowledgment signal. Adding a pipeline stage would break the memory controller protocol and require micro-architecture changes to the ECC encoder's write-handshake logic. The RTL team estimated 3 weeks for the change plus re-verification.  
  ↳ `mimo/R2`
- **Allocate 0.7 ns of the inter-block delay as block A output delay and 0.3 ns as block B input delay, then re-optimize block A to meet the tighter budget**  
  ↳ rejected: Block A had only 3 ps of internal slack. Tightening its output-delay budget by 0.2 ns (from 0.5 ns to 0.3 ns effective) was physically impossible without a floorplan change or major re-architecture. The block A team confirmed this was infeasible.  
  ↳ `mimo/R2`
- **Allocate 0.35 ns of inter-block delay as block A output delay and 0.65 ns as block B input delay, then re-optimize block B (which has 110 ps of slack) to absorb the tighter input-delay budget**  
  ↳ rejected: None  
  ↳ `mimo/R2`
- **Set fixed budget of 200ps for all A-to-B boundary paths**  
  ↳ rejected: Overly conservative for 60% of paths, would cause unnecessary optimization effort and area increase estimated at 1.5%  
  ↳ `mistral/R2`
- **Mark all A-to-B boundary paths as false paths**  
  ↳ rejected: Would break functional timing for real synchronous handshake paths and cause silicon failure on boundary registers  
  ↳ `mistral/R2`
- **Use clock period difference (5.0ns) as budget**  
  ↳ rejected: Ignores clock uncertainty and jitter, which account for 150ps of the observed failures; would still leave 100ps of violations unaddressed  
  ↳ `mistral/R2`
- **Keep 50/50 and let block B absorb the shortfall through optimization, adding a pipeline stage in the decode if it cannot.**  
  ↳ rejected: A pipeline stage changes cycle-level interface behaviour, so it needs an RTL change, a verification re-run, and architecture sign-off - weeks of downstream churn spent to avoid redoing constraint arithmetic.  
  ↳ `opus/R2`
- **Split strictly by measured depth: 250 ps to A, 720 ps to B.**  
  ↳ rejected: It leaves A with essentially no room for top-level buffering that had not yet been placed. When the real top-level route came in worse than the 220 ps estimate, the entire shortfall would land on the block already signed off, forcing a re-open of A.  
  ↳ `opus/R2`
- **Declare the configuration-write subset a false path, since software writes those registers once at boot and never during traffic - which is what was requested.**  
  ↳ rejected: Those writes are synchronous same-domain transfers. A false path removes hold checking as well as setup, and the hold check on that short, lightly-loaded path is the one actually protecting it; a boot-only path can still be sampled wrong on the cycle after the write, producing an intermittent silicon-visible failure.  
  ↳ `opus/R2`
- **Pad the top-level interconnect estimate from 220 ps to 400 ps for safety, shrinking both sides' budgets.**  
  ↳ rejected: Unearned pessimism at a boundary buys area on both sides simultaneously, and it destroys the ability to detect a genuine top-level route regression later, because the estimate no longer tracks any measured quantity.  
  ↳ `opus/R2`
- **Increase the internal block routing budget for Block A from 150ps to 250ps by reducing the off-chip budget to 300ps.**  
  ↳ rejected: The board-level signal integrity team confirmed that 400ps is the absolute minimum required to meet the eye-diagram specs for the PCB traces; reducing it would cause system-level bit errors.  
  ↳ `qwen/R2`
- **Insert a synchronous FIFO (async boundary) between Block A and Block B to break the timing path.**  
  ↳ rejected: It would add 2 cycles of latency to the memory access path, violating the strict performance requirement for the compute block's L2 cache miss penalty, and would require 3 weeks of RTL redesign and verification.  
  ↳ `qwen/R2`
- **Relax the clock skew constraint between the two blocks from 50ps to 150ps in the SDC.**  
  ↳ rejected: The two blocks share the same PLL, and the physical distance of the clock tree makes a 150ps skew physically unachievable without adding massive, area-prohibitive clock buffers that would violate the power budget.  
  ↳ `qwen/R2`
- **Apply a blanket 2-cycle multicycle exception to all 2,150 boundary paths (simplest SDC, passes timing easily)**  
  ↳ rejected: The 640 read data paths require 3-cycle latency per spec, not 2. A 2-cycle multicycle would make the design pass timing but fail functionally — reads would return data 1 cycle early, corrupting the pipeline. The 480 write data paths require 2-cycle latency, so a 2-cycle multicycle on writes is correct, but applying it uniformly to reads would break the design. The blanket approach loses the per-transaction-type latency differentiation that the spec requires.  
  ↳ `solar pro/R2`
- **Apply a tight single-cycle constraint to all 2,150 boundary paths (most conservative, no multicycle, no false paths)**  
  ↳ rejected: The 640 read data paths have a 3-cycle spec requirement — constraining them to 1 cycle would force the optimizer to meet an unrealistically tight timing target, driving excessive buffer insertion and logic duplication that would inflate area by an estimated 8-12% on the CPU block (based on prior similar interfaces) and degrade the 1.2 GHz core WNS by an estimated 0.15-0.2ns (the core block only has 0.14ns WNS margin). The 960 return paths have variable latency per transaction type (some are 1-cycle, some are 3-cycle) — a blanket 1-cycle constraint on all of them would over-constrain the 3-cycle transactions and cause the same area and timing degradation. The conservative approach wastes power, area, and timing margin on paths that legitimately have multi-cycle budgets.  
  ↳ `solar pro/R2`
- **Derive a per-group budget: 3-cycle multicycle on 640 read data paths (matching the spec), 2-cycle multicycle on 480 write data paths (matching the spec), single-cycle on 70 control paths (matching the spec), and per-transaction-type budget on the 960 return paths based on the transaction-type breakdown from the microarchitecture spec (1-cycle for ACK/invalidate, 2-cycle for snoop response, 3-cycle for cache line fill return). Reject the blanket 2-cycle approach because it under-budgets the reads; reject the blanket 1-cycle approach because it over-constrains everything and wastes area/timing/power.**  
  ↳ rejected: None  
  ↳ `solar pro/R2`
- **Keep the flat 2-cycle MCP exception for the entire boundary (the original approach)**  
  ↳ rejected: silently under-constrains the unsynchronized quasi-static control paths, which could then route/optimize with insufficient margin and risk real metastability or setup failure in silicon since those paths have no synchronizer to absorb it  
  ↳ `sonnet/R2`
- **False-path the entire boundary and rely on functional/CDC verification alone**  
  ↳ rejected: would mask real single-cycle timing risk on paths that ARE expected to close within one cycle (the synchronized data paths' first stage still has a real timing requirement into the synchronizer), and blanket false-pathing a CDC boundary was flagged as a sign-off risk by the CDC verification team  
  ↳ `sonnet/R2`
- **Manually derive per-path budgets from RTL-level classification: MCP(2) only for paths verified to terminate in the synchronizer structure; single-cycle SDC budget for quasi-static control paths, backed by a functional-verification waiver for their true static behavior**  
  ↳ rejected: None  
  ↳ `sonnet/R2`
- **Equal split: 500ps A-side, 500ps B-side**  
  ↳ rejected: Block B at -100ps internal WNS leaves only -400ps margin for 500ps boundary budget; insufficient given B's existing struggle; would force massive B-side ECOs with schedule risk  
  ↳ `yuanbao/R2`
- **Asymmetric: 700ps A-side, 300ps B-side**  
  ↳ rejected: NOT rejected - chosen as optimal balance  
  ↳ `yuanbao/R2`
- **Asymmetric: 800ps A-side, 200ps B-side**  
  ↳ rejected: Too aggressive against A; A needs significant optimization for 100 signals in 700ps when A's internal paths already consume ~200ps of phase; risk of creating A-side violations  
  ↳ `yuanbao/R2`
- **No budget - flat top-level implementation**  
  ↳ rejected: Top-level is 1.5M instances; flat STA takes 20+ hours per run; hierarchical budgeting mandatory for schedule  
  ↳ `yuanbao/R2`

<!-- total pairs: 266 -->
