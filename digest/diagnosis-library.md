# Differential-Diagnosis Library — merged from Prompt F outputs

**Status: DRAFT SCAFFOLDING, NOT EXPERT DATA.** Everything below is merged model output collected
2026-08-31 under the free-model collection pipeline. Per the integrity rule in
`../MODEL-TASKS-MASTER.md`, nothing here enters the corpus as an episode; if any of it is used it
enters as `provenance: synthetic-fixture` with run marker `free-model-harvest/F/2026-08-31`. It
graduates only through the expert's rewriting or a reproduced flow run.

**Corpus:** 11 F-files, 9 models producing well-formed 6-class objects
(chatgpt, deepseek, gemini, grok, meta, minimax 2.7, mistral, qwen, yuanbao), plus 20 salvaged
orphan cause-objects from a truncated `minimax m3 f.json`, plus one prose-only refusal
(`mimo f.json`) skimmed for salvage. 54 complete class objects + 20 fragments.

**How to read the merge.** Under each failure class:
- *Symptom shapes* — the reading-the-report signatures, deduplicated. This is the highest-value
  layer; it is what a triage UI would show first.
- *Candidate causes* — union across models, with the sharpest `distinguishing_check` kept and the
  claimed check/fix cost. Where models gave the same cause in different words, one entry carries
  all `models:`.
- *Traps* — the `classic_trap` field, best phrasings kept verbatim.
- *`disputed:`* — marks substantive disagreement between models. Disagreements are findings.

Every class ends with `TODO(expert): review`.

---

## FAIL_CONGESTION

`models: chatgpt, deepseek, gemini, grok, meta, minimax 2.7, mistral, qwen, yuanbao` (9/9)
`confidence range: 0.85–0.95`

### Symptom shapes (deduplicated union)

1. **Spatially sharp overflow against a comfortable block average.** Global-route overflow
   concentrated in a narrow region, macro channel or macro edge while the rest of the block is
   well under capacity. Several models give thresholds: `>5–10% overflow inside 1–2 regions with
   low block-average` (grok), `>5% overflow in <10% of gcells` (deepseek), `>2% concentrated in
   macro-to-macro channels with near-zero elsewhere` (meta).
   `models: chatgpt, deepseek, gemini, grok, meta, qwen, yuanbao`
2. **Directional asymmetry.** Horizontal overflow materially worse than vertical (or vice versa),
   with the bad direction aligned to a channel, a pin-facing macro edge, or a layer restriction —
   distinguishes *directional resource starvation* from generic cell-density excess. meta quantifies:
   `horizontal > vertical by 3–5× on one layer, often M3/M4`. `models: chatgpt, meta`
3. **Congestion tracks pin density, not cell density.** A region with modest placement utilization
   can carry severe routing demand because many pins must enter/leave through it.
   `models: chatgpt, gemini, meta, qwen`
4. **Post-CTS jump.** Pre-CTS placement was acceptable; new hotspots appear after CTS and
   spatially correlate with clock buffers and the regions the clock tree traverses.
   `models: chatgpt, gemini, grok, minimax 2.7`
5. **Detailed-route DRC dominated by one layer.** e.g. 90% of shorts on M4/M5 — pin-access and
   track-supply problems concentrate on one layer; distributed-across-layers means something else.
   `models: minimax m3 (fragment), deepseek, gemini`
6. **Route stalls at an asymptote rather than decaying.** DRC count plateaus across successive
   route-opt iterations instead of converging; wirelength stays within expected bounds while the
   router reports "unroutable". `models: deepseek, grok, yuanbao`
7. **Wirelength histogram has a long tail only inside the congested bins** (nets >2× expected
   length confined to hotspot gcells). `models: grok`

### Candidate causes (union, cheapest check first)

| # | Cause | Distinguishing check (sharpest phrasing kept) | check | fix | models |
|---|---|---|---|---|---|
| 1 | **Macro placement creating narrow channels / pin-access walls** — the consensus #1 prior | Overlay the congestion map on the floorplan; if overflow tracks macro boundaries and *moving or removing one macro drops local overflow >50%*, it is floorplan-limited (grok). deepseek: "if overflow bins align exactly with macro-to-macro gaps and are absent elsewhere". | min–hrs | hrs–days | all 9 |
| 2 | **Local placement density / insufficient whitespace** | Overlay overflow on local density bins and run a *controlled density-screen experiment in the hotspot only*. If overflow falls substantially without touching macro geometry or routing rules, cell packing is primary; if it barely moves, look elsewhere (chatgpt). Thresholds offered: local >85% vs block average <70% (deepseek), >80% density (gemini). | minutes | hours | all 9 |
| 3 | **Power grid / PG mesh over-blocking tracks** | Compare demand vs *available* capacity per layer/direction with blocked tracks subtracted; or toggle PG visibility — if overflow disappears when M4–M7 straps are hidden and layer-wise overflow drops >50%, PG is the limiter (meta). grok: temporary strap thin-out as the experiment. | hrs | hrs–days | chatgpt, deepseek, grok, meta, minimax 2.7, qwen, yuanbao |
| 4 | **Pin-access / pin-density concentration** (cell orientation, insufficient access layers) | Cluster DRC markers by cell pin, macro pin, orientation and via location; if errors repeat at the same access geometries and track pin density rather than broad overflow, it is access, not track capacity. gemini quantifies: ">1.5 unreachable pin access points per cell" in dense FinFET clusters. | hrs | hrs | chatgpt, gemini, meta, qwen, yuanbao |
| 5 | **High-fanout / bus / connectivity concentration** | Rank nets crossing the hottest gcells; if a small set of high-fanout nets or wide buses accounts for a disproportionate share of crossings — deepseek: ">50% of overflow in those bins" — and removing one cluster in a what-if collapses the hotspot, connectivity is causal. | min–hrs | hrs–days | chatgpt, deepseek, gemini, grok, mistral, qwen |
| 6 | **Clock-tree / optimization-buffer growth consuming tracks pre-signal-route** | Compare pre- vs post-CTS cell/net counts and congestion maps; a temporal jump plus spatial correlation with new buffers means implementation growth, not floorplan. grok's decisive experiment: **route only non-clock nets first — if congestion collapses, clock/scan pre-routes are the culprit.** gemini: filter the congested gcell instance list by cell type, check whether clock buffers/inverters are >30% of local cell area. | min–hrs | hrs | chatgpt, gemini, grok, minimax 2.7, yuanbao |
| 7 | **Non-default rule / layer assignment too aggressive** | Check overflow by layer; if one layer holds >80% of overflow and carries a non-default width/spacing rule or the wrong preferred direction, compare against the route-rule report. | minutes | minutes | chatgpt, grok, meta, qwen |
| 8 | **Floorplan aspect ratio too extreme** — long/narrow block forcing global wires through a central corridor | Look for a single dense band across the centre; check aspect ratio and the wirelength distribution for that corridor. | hrs | days | deepseek |
| 9 | **Over-the-block routing demanded of a hard macro with no feedthrough** | Check whether top-level nets are being routed across a block that provides no feedthrough path. | hrs | days | meta, yuanbao |
| 10 | **Repeated identical logic with identical pin patterns** (e.g. a 32-bit adder array) creating a periodic pin-density comb | Inspect pin patterns for periodicity aligned to the overflow bins. | hrs | hrs | qwen |

### Traps

- **The headline trap, stated by 9/9 models in different words:** treating the *block-average*
  overflow percentage as the diagnosis and lowering global utilization, when the defect is a narrow
  channel, a pin-access wall, a directional shortage or a few connectivity-heavy regions.
  Best phrasing (chatgpt): "Treating the reported congestion percentage or average utilization as
  the diagnosis and globally lowering utilization, when the real failure is often a narrow macro
  channel, pin-access wall, directional capacity shortage, or a few connectivity-heavy regions."
- **The router-effort trap** (yuanbao, sharpest): "Engineers re-run detailed routing with higher
  effort hoping the router 'finds a way', when the root cause is floorplan/macro placement. Routing
  tweaks never fix a structurally unroutable region — you burn hours/days on iterations that cannot
  succeed."
- **The wrong-remedy-for-the-right-symptom trap** (deepseek): "Misdiagnosing as a placement-density
  problem and respreading cells, when the root cause is macro channel blockage — respreading worsens
  the issue by moving cells away from macros but does nothing to open the routing channels."
- **The blanket-halo trap** (meta): "Immediately dropping utilization globally or adding routing
  halo everywhere, which hurts timing and area, when the real cause is 2–3 macro pins aligned badly
  blocking one channel."

`disputed:` **Where does a veteran look first?** Two orderings, and the split is real, not verbal.
*Floorplan-first* (grok, deepseek, meta, qwen, minimax 2.7, yuanbao — "macro placement has the
highest prior in a macro-dense block"). *Cheapest-reversible-experiment-first* (chatgpt, gemini —
"start with the cheapest spatial correlations and reversible local experiments, then move upstream
to macro changes only after proving the hotspot is not simply a local resource imbalance"). These
give different first actions when both a macro channel and a density peak are present. Worth
putting to the expert as a direct question — it is the kind of ordering judgment that separates a
practitioner's triage from a checklist.

`disputed:` **Cost of the fix.** deepseek/gemini/qwen imply a good congestion fix also improves
timing; chatgpt/meta/yuanbao state or imply it costs timing. See `episode-draft-bank.md` §Cross-run
finding 1 — the episode data shows this flipped almost universally once the prompt told models a
congestion fix usually costs timing, which means neither position here is independent evidence.

`TODO(expert): review`

---

## FAIL_TIMING (setup)

`models: chatgpt, deepseek, gemini, grok, meta, minimax 2.7, mistral, qwen, yuanbao` (9/9)
`confidence range: 0.86–0.96` (highest-confidence class in the corpus)

### Symptom shapes — the three-way discrimination this class exists for

The whole value here is the *shape* read that separates constraint / logic-depth / physical before
any tool is run. Merged, the models describe four discriminating axes:

1. **Count × magnitude.** Few paths with large negative slack (−400 to −800 ps) → logic depth or a
   mis-placed macro. Thousands of paths with small negative slack (−20 to −80 ps) spread across
   unrelated hierarchies, large TNS but small WNS → a global effect: constraint, clock skew, OCV
   derate, or utilization drag. `models: gemini, meta, minimax 2.7, qwen, yuanbao`
2. **Clustering on a shared term.** Hundreds-to-thousands of endpoints failing by a *near-identical*
   magnitude, all sharing one launch clock, one capture clock, or one gating cell → constraint.
   gemini: "failing by near-identical magnitudes matching half or full clock period" is the
   signature of a missing clock group or false path. minimax 2.7 states the read as a rule:
   "a tight unimodal cluster in one domain → go straight to SDC."
   `models: chatgpt, gemini, grok, meta, minimax 2.7, mistral, qwen, yuanbao`
3. **Cell-delay vs net-delay split.** Cell delay >60–70% with >18–22 stages → logic depth. Net delay
   >50–70% of path delay across wide floorplan spans → physical. yuanbao names the single check that
   decides it: run the design-analysis report that splits logic-bound from net-bound "(minutes) —
   this single check determines whether the fix is synthesis/upsize (cheap) or floorplan/placement
   (expensive)." `models: chatgpt, deepseek, gemini, grok, meta, qwen, yuanbao`
4. **When the failure appeared.** Endpoints that move from passing to failing only when clocks
   become propagated, or only after extraction, point at CTS or post-route parasitics/SI rather than
   synthesis logic depth. `models: chatgpt, grok`

Additional shape offered by one model and worth keeping: **a slack discontinuity at a block boundary
or clock-domain crossing** (0.5–1 ns delta on one net) indicates budget/SDC or clock-insertion
mismatch, not cell speed. `models: meta`

### Candidate causes (union)

| # | Cause | Distinguishing check | check | fix | models |
|---|---|---|---|---|---|
| 1 | **Incorrect/incomplete constraints** (missing clock group, wrong generated clock, missing MCP/false path, wrong IO delay, double-applied derate) | Constraint audit of clocks, generated clocks, groups, IO delays, exceptions, uncertainty; compare the failing set against differently-constrained endpoints. "If the failure disappears or changes class when the intended constraints are corrected, it is not a physical closure problem" (chatgpt). | minutes | min–hrs | all 9 |
| 2 | **Excessive logic depth / undersized cells** | Split the worst paths into cell vs net delay; if cell delay dominates and the same stages recur across many failing paths at reasonable wire length, test larger drive strength or restructuring in a what-if. Thresholds: >10 levels at 1 GHz/28nm (deepseek), >18–22 stages (meta), >25–30 levels (gemini). | minutes | days | all 9 |
| 3 | **Placement / wirelength / detour** | Compare placed vs pre-placement estimate; check physical coordinates, fanout, transition, net RC. meta's test: net length >3× straight-line distance, or the path routes around a macro channel. deepseek: Manhattan distance >200 µm on a small block with net delay dominant. | min–hrs | hours | all 9 |
| 4 | **Clock skew / insertion-delay mismatch (capture early relative to launch)** | Decompose setup into launch arrival, data arrival, capture arrival, uncertainty, required time. "If failing paths share an anomalous capture-minus-launch skew signature while data delay is normal, the clock tree is the primary lever" (chatgpt). deepseek: skew >50 ps beyond budget. meta: skew >15% of cycle *and* slack recovers under ideal clocks. | minutes | hours | all 9 |
| 5 | **Post-route RC / crosstalk / extraction** | Compare identical endpoints at placed → post-CTS → extracted → signoff. If slack loss appears predominantly at extraction and decomposes into net RC and/or SI delta-delay with unchanged topology, the route is causal. deepseek: SI adds >50 ps. | hrs | hours | chatgpt, deepseek, grok, qwen |
| 6 | **High-fanout net (reset, scan-enable) with weak driver / poor slew** | Fanout and transition report; if a net with fanout >20–30 appears in multiple failing paths with slow transition, **isolate it by temporary idealization** (grok — the cheapest decisive experiment in this class). | minutes | hours | grok, meta, mistral, qwen |
| 7 | **OCV / AOCV / POCV derate or IR-induced pessimism** | Compare PBA vs GBA and nominal vs derated. meta's threshold: if PBA recovers >30% of the violation and derate >10% (28nm) / >15% (7nm), and the IR map overlaps, it is pessimism or IR-induced, not topology. | hrs | days | chatgpt, grok, meta, minimax 2.7, qwen, yuanbao |
| 8 | **Clock period itself unrealistic for the design** | Sanity-check the target against achievable FO4 depth before optimizing anything. | minutes | — | mistral, minimax 2.7 |
| 9 | **Library characterization mismatch** (NLDM tables optimistic for high-Vt cells at 28nm) | Compare reported cell delays against SPICE or datasheet at the same corner. | hrs | hrs | mistral, qwen, yuanbao |
| 10 | **Clock network latency exceeding ~30% of the period** | Read insertion delay as a fraction of period before attributing slack loss to the datapath. | minutes | hours | qwen |

### Traps

- **Sizing everything that fails** (chatgpt, best phrasing): "Upsizing cells on every failing setup
  path without first separating clock skew, net delay, and constraint problems, which can worsen
  congestion and create hold failures without addressing the real bottleneck."
- **Weeks lost to the wrong layer** (minimax 2.7, sharpest on cost): "Restructuring logic or
  re-running placement without first checking the constraint — spending weeks fixing a problem that
  was set up wrong, discovered too late because no one re-read the SDC before touching the design."
- **The inverse trap** (grok): "Blaming the clock tree for every setup failure when the real problem
  is a single long data net or an unconstrained false path; engineers then over-constrain CTS and
  create hold problems."
- **Treating all setup violations identically** (yuanbao): "Blindly upsizing cells on a
  net-delay-dominated path adds area and power but does not fix wirelength. Conversely, spreading
  cells to fix congestion can worsen setup by lengthening wires."
- **The −30 ps wall** (meta): "Treating a wall of −30 ps failures as needing logic restructuring
  when it's actually a clock skew or derate issue; sizing up cells makes congestion and power worse
  with no WNS gain."

`disputed:` **Does a wall of thousands of small violations mean constraint, or derate/skew?**
gemini and minimax 2.7 read a uniform wall as *constraint* first; meta and yuanbao read the same
shape as *OCV/derate/IR pessimism* first. Both are internally consistent — the discriminator neither
side states is whether the wall's magnitude equals a clock-period fraction (constraint) or scales
with path length/derate (pessimism). **This gap is a genuine content hole worth asking the expert to
fill; it is the single most useful missing check in this class.**

`disputed:` **FPGA contamination.** yuanbao lists "SLR crossing in multi-die (SSI) devices" as a
setup cause. That is a Xilinx FPGA concept, not ASIC physical design. Excluded from the merged table
above; recorded here because it marks a model whose ASIC/FPGA boundary is porous (see
`MISSED.md` §4).

`TODO(expert): review`

---

## FAIL_TIMING (hold)

`models: chatgpt, deepseek, gemini, grok, meta, minimax 2.7, mistral, qwen, yuanbao` (9/9)
`confidence range: 0.84–0.96`

### Symptom shapes

1. **Very short paths failing while long paths are clean** — 0–2 logic levels, small data delay,
   minimum-delay paths failing. `models: all 9`
2. **Unrelated data cones sharing one capture/launch clock pair and a similar negative slack** —
   the common signature is the *clock*, not a shared data path. `models: chatgpt, deepseek, grok, meta, qwen`
3. **Explosion after CTS, tracking one branch or region**, with capture-minus-launch arrival
   changing sharply. `models: chatgpt, deepseek, gemini, minimax 2.7`
4. **Fast-corner-only**: hold bad at min-delay/fast corner while setup is fine at slow corner.
   `models: chatgpt, gemini, grok, meta`
5. **Appears only after setup fixing** — inverse correlation with setup work indicates
   over-aggressive LVT swaps and downsizing. `models: deepseek, meta`
6. **Concentrated at block-to-block interfaces or on scan-shift paths, not in random logic** —
   points at interface clock skew or scan hold rather than a datapath problem.
   `models: meta, qwen`

### Candidate causes (union)

| # | Cause | Distinguishing check | check | fix | models |
|---|---|---|---|---|---|
| 1 | **Adverse clock skew / CTS arrival relationship** | Decompose the hold report into launch arrival, capture arrival, data arrival, requirement. "If unrelated failing paths share the same skew signature and the data delays are not anomalously small, the common clock relationship is causal" (chatgpt). deepseek's threshold: (capture − launch) < −100 ps on most failing paths. | minutes | hours | all 9 |
| 2 | **Genuinely too-short/too-fast data path** | Rank failing paths by data delay and logic depth; if the deficit disappears when a delay element is inserted in a controlled what-if, it is a real minimum-delay problem. gemini: zero combinational gates and Q→D distance under 5 µm. | minutes | hours | all 9 |
| 3 | **Over-aggressive setup fixing (LVT swap, downsizing) creating fast paths** | Check library mix — if failing cells are all LVT/SVT, the setup-fixed region overlaps the hold region, and the delay distribution shows a bimodal fast tail. | minutes | hours | deepseek, meta, mistral |
| 4 | **ICG / clock-gating cell placement creating local skew** | If all hold failures share one ICG and moving or re-buffering it removes the cluster, the ICG is the source. deepseek: compare gated vs ungated insertion delay, >100 ps difference consistently. | minutes | hrs–days | deepseek, grok, meta, mistral, qwen, yuanbao |
| 5 | **OCV / derate / missing CRPR (common-path pessimism removal)** | Re-run hold with CRPR enabled or reduced derate; if the violations disappear, the margin stack-up was artificial. meta: min derate >10% with CCP removal not applied. | minutes | minutes | chatgpt, deepseek, grok, meta, minimax 2.7 |
| 6 | **Wrong min-delay constraints / hold uncertainty** (uncertainty = 0, or a positive setup-style uncertainty reused for hold) | Audit the minimum-delay scenario; "if unrelated paths fail with an identical requirement-side offset, the problem is the timing setup rather than the datapath" (chatgpt). meta's node guidance: realistic hold uncertainty 50–100 ps at 28nm, 30–60 ps at 7nm. | minutes | minutes | chatgpt, deepseek, meta |
| 7 | **Placement-induced short interconnect / post-route minimum RC** | Compare pre- vs post-route min-delay on the same endpoints; a large extracted-stage-only delta on a set of nets indicates a route effect. | hrs | hours | chatgpt |
| 8 | **Fast-corner library or operating-condition mismatch** | Compare reported min-delay arcs against SPICE/datasheet at that corner; "if library min-delay is unrealistically small, library or corner definition is wrong" (grok). | hrs | hours | chatgpt, grok |
| 9 | **Scan-chain ordering creating extremely short adjacent-flop paths** | Check whether failures are on scan-shift paths only. | minutes | hours | mistral, qwen |
| 10 | **Clock tree *too* balanced** — near-zero skew leaves no hold margin | Look for a design where launch and capture arrive within a few ps by construction. | minutes | hours | yuanbao |

### Traps

- **Buffer-bombing** (all 9 in some form; chatgpt sharpest): "Blindly adding hold buffers to every
  violating path when the common signature is actually one CTS branch or incorrect clock
  relationship; this can create unnecessary area, congestion, power, and setup damage."
- **The fix-loop** (deepseek): "Adding a large delay buffer to every failing path, which then
  creates new setup violations on the same paths or nearby, entering a fix-loop cycle."
- **Fixing hold on the clock** (yuanbao, and the most operationally specific rule in the class):
  "Fixing hold by adjusting the clock period or by adding delay to the clock path. Clock-period
  changes break setup globally; clock-path delay hurts all paths reaching that flip-flop. **Hold fix
  belongs on the DATA path only.** Also, engineers often ignore hold until post-CTS, causing
  expensive ECO loops near tapeout."
- **Sequencing** (meta): "Fixing hold by blindly inserting thousands of buffers before CTS
  stability… correct order is fix clock skew first, then only truly short data paths."

`disputed:` **Hold uncertainty sign convention.** deepseek asserts hold uncertainty is "often
negative… we can set negative for hold if the tool doesn't handle jitter"; grok and meta describe
hold uncertainty as a smaller *positive* subset of the setup number (local OCV only, because global
jitter is common-mode). deepseek's account is muddled in its own text and is the outlier. Flagged
rather than resolved — it is a convention question a practitioner settles in one sentence.

`TODO(expert): review`

---

## FAIL_IR_DROP

`models: chatgpt, deepseek, gemini, grok, meta, minimax 2.7, mistral, qwen, yuanbao` (9/9)
`confidence range: 0.82–0.94` (lowest-confidence class — the models know it least well)

### Symptom shapes

1. **Static: a broad, stationary depression** around a weak or resistive grid region, following the
   PG pitch, worst mid-pitch away from straps — spatially unlike an activity hotspot.
   `models: chatgpt, gemini, grok, meta, qwen, yuanbao`
2. **Dynamic: compact, scenario-dependent droop** aligned to clock edges or a specific bus toggling;
   *the hotspot moves when the activity pattern changes*. That mobility is the discriminator.
   `models: chatgpt, deepseek, gemini, grok, minimax 2.7, qwen`
3. **Vectorless clean, vector-based violating** — indicates workload-dependent simultaneous
   switching rather than static grid resistance. `models: meta, deepseek`
4. **Worst locations track long power paths, sparse straps, macro boundaries, or via bottlenecks**
   rather than simply the highest logic density. `models: chatgpt, gemini, grok`
5. **Timing degradation spatially correlated with the IR hotspot**, recovering when analysed at
   nominal supply. `models: chatgpt, deepseek, gemini, minimax 2.7`

Thresholds offered (node-dependent, unverified): >5% VDD static / >10% dynamic (deepseek);
3–5% static / 10–15% dynamic (gemini); 80–100 mV in 50×50 µm hotspots (meta); yuanbao adds the
node caveat — "at ≤7nm, assuming a 28nm-style 5% IR budget is safe is wrong; advanced nodes require
≤3% due to lower Vdd and higher R."

### Candidate causes (union)

| # | Cause | Distinguishing check | check | fix | models |
|---|---|---|---|---|---|
| 1 | **Insufficient / resistive PG topology (strap width, pitch, mesh density)** | Structural PG check tracing worst-drop locations back to strap width, pitch, resistance, grid discontinuities and distance to supply entry. "If the same locations remain hot under multiple activity assumptions, the topology is causal" (chatgpt) — this is the static-vs-dynamic discriminator stated as an experiment. | hrs | days | all 9 |
| 2 | **Dynamic simultaneous-switching event** (clock edge, register bank, wide bus) | Compare static vs dynamic with controlled activity scenarios; "if the hotspot *moves with the switching group*, the failure is transient demand rather than static grid resistance" (chatgpt). | hrs | days | all 9 |
| 3 | **Insufficient / mis-placed decap** | Map decap density against dynamic peaks; gemini's threshold: decap coverage under 5% in high-drop regions. minimax 2.7 and qwen both note decap must be *near* the switching instances, not merely present. | min–hrs | min–hrs | deepseek, gemini, grok, minimax 2.7, mistral, qwen, yuanbao |
| 4 | **Via bottleneck / weak layer transition** | Cross-probe the worst-drop region onto the PG geometry and inspect via count and current density at layer transitions; a localized discontinuity at a sparse via stack that improves with redundant vias identifies it. | hrs | hours | chatgpt, deepseek, gemini, grok |
| 5 | **Macro power-pin starvation / power-domain placement** | PG resistance extraction on macro pins; a hotspot that stays tied to a macro edge across activity scenarios is a distribution-geometry problem. | minutes | hrs–days | chatgpt, gemini, yuanbao |
| 6 | **Clock-tree buffer current concentration** | Per-instance current map; deepseek's threshold: drop region coincides with clock-buffer density >5× average. | hrs | days | deepseek, mistral, qwen |
| 7 | **Package / bump / C4 / board PDN** | Compare drop from pad/bump to hotspot; "if the majority of the drop is between the package pin and the die edge, package or pad placement is limiting" (grok). deepseek: check whether the droop frequency matches board resonance. | hrs–days | days–weeks | deepseek, grok, minimax 2.7, mistral, qwen, yuanbao |
| 8 | **Wrong activity annotation / library power** (instance current above library expectation) | Compare instance current vs power report under the same vector. | hrs | hours | grok |
| 9 | **EM-limited via arrays** (IR and EM co-limited) | Via current-density report co-located with the IR hotspot; if increasing via count improves both, via sizing is causal. | hrs | hours | grok, qwen |
| 10 | **IR-induced timing feedback misread as a standalone timing problem** | Correlate signoff timing degradation with an IR-aware run and spatially match affected cells to the voltage map; if endpoints recover at nominal voltage, the timing failure is downstream of power integrity. | hrs | days | chatgpt, minimax 2.7 |

### Traps

- **Static remedy for a dynamic defect** (yuanbao, sharpest): "Engineer widens straps, spends days
  re-routing, but dynamic droop persists because the root cause is insufficient decoupling or
  switching-peak concentration."
- **Blanket decap** (grok): "Adding blanket decap everywhere when the real problem is a missing power
  strap or sparse via array under one block; the extra decap then hurts congestion and area without
  solving the root IR path."
- **Misattributing IR-induced timing** (minimax 2.7): "Running more placement iterations or
  re-characterizing the library fixes nothing if the voltage at the cell is below what the library
  model assumes."
- **Node-budget carry-over** (yuanbao): applying a 28nm 5% IR budget at ≤7nm.

`disputed:` **First check — static or dynamic?** gemini/mistral/meta start with cheap static grid
and decap-density checks; yuanbao insists on running *both* analyses first because the whole class
turns on that distinction; chatgpt frames it as an experiment (does the hotspot move?) rather than a
sequence. The chatgpt framing is the one to keep — it is the only version that yields a decision
rather than an ordering.

`TODO(expert): review`

---

## FAIL_CTS (clock tree)

`models: chatgpt, deepseek, gemini, grok, meta, minimax 2.7, mistral, qwen, yuanbao` (9/9)
`confidence range: 0.83–0.95`

### Symptom shapes

1. **Latency and skew both poor across many sinks**, with large insertion-delay spread and
   inconsistent branch depths → topology/distribution, not one bad sink.
   `models: chatgpt, gemini, grok, mistral`
2. **Setup and hold failures appearing together after CTS with opposite skew signatures on the same
   clock pair** → clock-arrival movement, not independent datapath regressions. `models: chatgpt`
3. **A long tail on the skew histogram**: a small subset (<5%) of sinks with far larger insertion
   delay than the rest. `models: deepseek, grok`
4. **Transition/capacitance violations localized to one branch or sink cluster** while others are
   healthy. `models: chatgpt, deepseek, gemini`
5. **CTS acceptable pre-route, degrading after clock routing** where clock routes cross congested or
   blocked regions. `models: chatgpt, grok`
6. **A constant slack shift across all paths post-CTS** (e.g. every path degrades by ~100 ps),
   indicating systematic latency rather than per-path problems. `models: deepseek`
7. **Clock power bloat**: clock buffers consuming >30–40% of block dynamic power, with deep trees
   (>15–20 buffer levels). `models: gemini`

### Candidate causes (union)

| # | Cause | Distinguishing check | check | fix | models |
|---|---|---|---|---|---|
| 1 | **Bad sink clustering / topology / uneven sink distribution** | Inspect sink distribution and branch topology; "if one branch spans an unusually large physical distance or mixes geographically separated clusters while nearby sinks are balanced, compare a controlled clustering change" (chatgpt). grok: one cluster with 2–3 more buffer levels than average. | min–hrs | hours | all 9 |
| 2 | **Macro / blockage forcing clock detours** | Check the routed clock path; "if it must route around a large macro and the delayed sinks are exactly those on the far side" (deepseek). grok's cheap version: compare routed clock length vs Manhattan. | min–hrs | hrs–days | chatgpt, deepseek, gemini, grok, minimax 2.7, qwen, yuanbao |
| 3 | **ICG / clock-gating placement or depth** | Group failing sinks by gating cell or generated-clock source; "if latency jumps occur exactly at ICG boundaries and moving the ICG removes the jump" (grok). deepseek: gated vs ungated insertion delta >100 ps consistently. | minutes | hrs–days | chatgpt, deepseek, grok, meta, minimax 2.7, mistral, qwen, yuanbao |
| 4 | **Over-constrained CTS target (skew/latency too tight)** | Read the CTS constraint file — target skew <20 ps at 28nm (deepseek) or <10 ps on a large FinFET block (gemini) is not physical; the tool responds by over-buffering. | minutes | hrs | deepseek, gemini, grok, meta, qwen |
| 5 | **Excessive fanout / buffer sizing / transition violations on a branch** | Compare fanout, capacitance, transition, buffer count and drive against healthy branches; qwen's threshold: branches with >5× load disparity; deepseek: fanout >200. | minutes | hours | chatgpt, deepseek, gemini, qwen |
| 6 | **Routing congestion / clock-route resource limitation** | Overlay CTS branches with routing congestion and clock-route DRCs; repeated detours, excessive vias or constrained layers exactly where congestion is high. | hrs | hours | chatgpt, grok, qwen |
| 7 | **Stale CTS — not re-run after a placement change** | minimax 2.7's cheapest-first check, and the only model to name it: "the most common reason skew suddenly appears after an ECO." | minutes | hours | minimax 2.7 |
| 8 | **Non-register pins swept into the sink list / missing clock definition** | Report the CTS sink list and check for memory control inputs or combinational pins appearing as sinks. | minutes | minutes | gemini |
| 9 | **Skew-group vs clock-group confusion in multi-domain designs** | yuanbao: "confusing clock groups (for STA) with skew groups (for CTS)… leads to inter-domain skew that no amount of buffering can fix." | minutes | hours | yuanbao, minimax 2.7 |
| 10 | **OCV/AOCV derates driving an over-conservative tree** | Re-run CTS with reduced derate or CRPR-aware mode; if skew and buffer count drop substantially while real margin is preserved, derate was excessive. | hrs | hours | grok |
| 11 | **Per-domain buffer/layer inconsistency causing systematic inter-domain skew** | Compare insertion delays of two domains sharing a root; >200 ps consistent difference points at buffer-cell or layer assignment. | hrs | days | deepseek |
| 12 | **Useful-skew overshoot** — skew added for setup has eaten hold margin | Check whether hold failures cluster on exactly the branches that received useful skew. | minutes | hours | qwen, yuanbao |

### Traps

- **Skew as a scalar objective** (chatgpt): "Trying to minimize skew as a single scalar objective and
  declaring CTS successful, while ignoring insertion latency, transition, power, hold impact,
  congestion, and the physical difficulty of the routed clock branches."
- **Tightening the target to fix a local problem** (qwen): "Tightening global skew targets to fix a
  local hotspot, which causes the CTS tool to insert massive amounts of buffering and wreck the
  design area." grok adds the consequence chain: "the tighter target then explodes buffer count and
  creates new IR and congestion issues."
- **Iterating a broken placement** (yuanbao, and the best single sentence in this class): "CTS
  failure is primarily a placement-quality test — veterans roll back to placement FIRST before
  touching CTS knobs… 80% of CTS failures are placement or constraint issues, not CTS engine issues."
- **Leaf-level buffering against an upstream cause** (minimax 2.7): "Adding buffers to balance skew
  at the leaves when the real problem is upstream (gate distribution, macro pin diversity) creates a
  larger clock tree with more power and more variation, not a better one."

`disputed:` **Is CTS failure primarily a CTS problem?** yuanbao and minimax 2.7 argue the class is
mostly mislabeled placement/constraint failure and the first move is to roll back rather than tune;
chatgpt/gemini/grok treat it as a genuine CTS-parameter class. This is a framing disagreement with
real consequences for a triage UI's first question, and it is worth the expert's ruling.

`TODO(expert): review`

---

## FAIL_DRC (routing DRCs)

`models: chatgpt, deepseek, gemini, grok, meta, minimax 2.7, mistral, qwen, yuanbao` (9/9)
`confidence range: 0.85–0.96`

### Symptom shapes

1. **One rule + one layer dominating** repeated markers → a systemic routing-rule or resource
   problem, not scattered geometry errors. `models: chatgpt, deepseek, grok, qwen`
2. **Clustering around pins, macro edges and via transitions** while ordinary wire spacing elsewhere
   is clean → access/enclosure, not general congestion. `models: chatgpt, gemini, meta`
3. **Markers co-located with the previous congestion map** — grok gives the decisive threshold:
   ">70% of shorts/spacing inside the top-10 overflow gcells means congestion is still the root."
   `models: chatgpt, deepseek, grok, yuanbao`
4. **Antenna violations correlated with long partially-connected metal**, appearing even where
   spacing is clean → a process/layer-connectivity issue, not crowding.
   `models: chatgpt, deepseek, gemini, grok`
5. **New markers appearing only after metal fill, or only after a late ECO** → the fill rules or the
   ECO, not the router. `models: grok, gemini, minimax 2.7`
6. **DRC count rises sharply only at detailed route**, in compact clusters exactly where the router
   was forced into detours or via stacks. `models: chatgpt`

### Candidate causes (union)

| # | Cause | Distinguishing check | check | fix | models |
|---|---|---|---|---|---|
| 1 | **Residual congestion the detailed router could not resolve** | Map markers by layer/coordinate onto the congestion and demand maps; grok's >70%-in-top-10-gcells test. | minutes | hours | chatgpt, deepseek, grok, mistral, qwen, yuanbao |
| 2 | **Pin-access / via-access failure** (cell orientation, limited hit points at ≤7nm) | Cluster markers by cell pin, orientation and via location; gemini: >80% on M1/M2 at standard-cell boundaries means pin access, not routing. | hrs | hours | chatgpt, deepseek, gemini, meta, qwen |
| 3 | **Antenna** | Filter antenna markers and inspect metal area/length by layer and diode presence; "if the marker follows long unprotected metal and clears when protection or a layer break is applied" (chatgpt). Cheap and often the whole story. | minutes | hours | chatgpt, deepseek, gemini, grok, qwen, yuanbao |
| 4 | **Via / cut-layer rules (enclosure, min-area, redundant via)** | Filter by via/cut type; a dominant enclosure or min-area family on one via definition means the via construction, not the route. | minutes | hours | chatgpt, grok, meta, mistral |
| 5 | **Wrong or inconsistent rule deck / tech LEF between P&R and signoff** | "The same geometry passes in a reference deck or a pure geometric check but fails in the signoff deck; or identical patterns elsewhere in the design are clean" (grok). gemini: run a 1-net test route to see whether the P&R router considers the geometry legal. | hrs | hrs–days | chatgpt, deepseek, gemini, grok, minimax 2.7, mistral, yuanbao |
| 6 | **NDR / layer-allocation policy too aggressive** | Group by rule, layer and net class and compare actual geometry against the intended routing constraints. | hrs | hours | chatgpt, qwen, mistral |
| 7 | **Late ECO / manual edit ignoring existing routes** | "If markers sit exactly on the new ECO cells or their new pins and the rest of the design is clean, the ECO is the source" (grok). minimax 2.7 makes checking the ECO log its *first* move. | minutes | min–hrs | gemini, grok, minimax 2.7, yuanbao |
| 8 | **Metal-fill / dummy-fill interactions** | Compare DRC before vs after fill; new markers only on fill shapes or at fill-to-signal interfaces. | minutes | hours | grok, mistral |
| 9 | **Blockage forcing signal routing onto lower layers with tighter rules** | Compare the marker map with the macro/blockage map; violations only where upper layers are blocked. | hrs | days | deepseek, qwen |
| 10 | **Node-specific advanced interactions** (cut spacing, multi-patterning/coloring, local density) | Classify by rule family and compare against the node-qualified routing methodology; "if the violation is absent under an older-node rule model, do not apply an old-node fix blindly" (chatgpt). | hrs | days | chatgpt, gemini, qwen |
| 11 | **Overly conservative deck for the corner** | Check whether violations sit exactly at the rule limit and are all one type; consult the foundry recommended-vs-mandatory distinction. | hrs | weeks (waiver) | deepseek |
| 12 | **Block-vs-top assembly mismatch** (block DRC-clean, top not) | Compare block and top rule context for the same geometry. | hrs | days | yuanbao, mistral |

### Traps

- **Marker-by-marker repair against a systemic cause** (chatgpt): "Fixing DRC markers one by one with
  local route edits while leaving the underlying congestion, pin-access, layer-allocation or via
  strategy problem intact, causing the router to recreate the same violations elsewhere."
- **The infinite loop** (yuanbao, most concrete): "Running auto-DPR 'fix all DRC' which patches
  spacing violations by nudging wires, but the underlying congestion remains — new DRCs appear
  elsewhere, creating an infinite loop." grok: "the router keeps producing the same shorts because
  there is simply no space."
- **Effort instead of diagnosis** (qwen): "Running the detailed router with higher effort levels to
  fix spacing violations that are actually caused by fundamental placement congestion."
- **Missing the cheap win** (deepseek): "Re-routing the entire block when the DRCs are all antenna
  violations that could have been fixed by adding a single diode per violating net in minutes."
- **DFM blind spot** (yuanbao): "At ≤7nm, ignoring DFM/DFY rules (CMP, litho hotspots) in DRC
  signoff leads to yield disasters even with 'clean' DRC."

`disputed:` **First filter — antenna or congestion?** deepseek orders antenna first (cheapest to fix,
often the bulk); grok/yuanbao/chatgpt order congestion-overlay first (highest prior for a
non-converging route). Both are defensible and the choice depends on whether the route converged at
all — a distinction none of the models make explicit. Worth adding as a precondition when the expert
reviews.

`TODO(expert): review`

---

## Salvage notes

- **`mimo f.json` — prose refusal, content preserved.** mimo declined the prompt as
  "instructions embedded in reference content", then answered the same question in prose. Its six
  classes were skimmed: the content adds one framing worth keeping —
  *"the classic trap is assuming uniform congestion means uniform causes — often it's one badly
  placed macro cluster"* — and one triage sequence for FAIL_TIMING (setup) identical in substance to
  the consensus. Nothing unique was lost by its format failure, but see `MISSED.md` §2: mimo refused
  **every** later prompt in the same way, so its output is systematically unparseable.
- **`minimax m3 f.json` — truncated mid-object.** The first parser recovered 1 item; an
  element-wise re-parse recovered 20 cause-objects. Those fragments are folded into the tables above
  where they add a distinct cause (notably the "DRC dominated by one layer" symptom and the CTS
  topology-vs-geometry framing). The tail of the file is unrecoverable — the JSON simply stops.
