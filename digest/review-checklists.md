# Signoff Review Checklists — merged from Prompt I outputs

**Status: DRAFT SCAFFOLDING, NOT EXPERT DATA.** Merged model output collected 2026-08-31. Enters any
downstream use as `provenance: synthetic-fixture`, run marker `free-model-harvest/I/2026-08-31`.
Nothing here is a review checklist any real team uses; it is a reconstruction of what models believe
such a checklist contains, and it graduates only through the expert's rewriting.

**Corpus:** 13 `* i.json` files (Prompt I, `prompts/PROMPT-I-REVIEW-CHECKLISTS.md`, I-v1). **11
models produced the demanded 4-gate array — 44 gate objects carrying 339 individual checks.** Two
files needed salvage: `mimo i.json` (prose refusal, gate-structured, skimmed) and
`minimax m3 i.json` (mid-string corruption plus a truncated tail — 10 orphan check-objects
recovered). Format compliance was otherwise the best of any slice in the collection.

**Why this slice is different from F and G.** Prompt I asks for something with no textbook: the
*ordered questions* a reviewer asks and the answer that stops the review. The models converge hard on
the questions (which suggests shared provenance) but diverge sharply on the **thresholds** and on
`waiver_culture` — and the waiver answers are the part that reads least like a textbook and most like
someone describing what actually happens. That is where the value is, and it is flagged throughout.

**Reading the merge.** Per gate: purpose (merged), the ordered check sequence with the sharpest
`red_flag` kept and per-check `models:` provenance, kill questions, and waiver culture. `disputed:`
marks substantive disagreement — usually a numeric threshold.

---

## Gate 1 — Floorplan review (before placement starts)

`models: chatgpt, deepseek, gemini, grok, kimi, meta, minimax m2.7, mistral, qwen, sonnet, yuanbao` (11/11)
`confidence range: 0.60–0.96`

**Purpose (merged).** Catch the decisions that are cheap now and multi-week later: macro placement,
power-grid topology, boundary pin assignment, hierarchy partition. Best phrasings — deepseek:
*"This is the only gate where moving a macro by 10 µm costs minutes."* sonnet: *"the last point where
geometry is free."* kimi adds the dependency chain: *"once cells are placed, moving a macro
invalidates placement, CTS, and everything downstream of it."*

### The ordered check sequence

**1. Macro channel width against what has to cross it.** `models: all 11`
- *Evidence:* channel-width histogram between adjacent macro pairs; the count of signals crossing each
  channel; pin-bearing edge track counts.
- *Red flag:* deepseek — *"worst-case channel under 50 µm at 28nm (or 30 µm at 7nm) without a
  justification"*; meta — *"any channel < 2× row height where >100 pins need to escape"*; sonnet —
  *"any two macros close enough that the channel between them can't route the signal count crossing
  it."*
- *Why:* this is the defect the whole congestion class in `diagnosis-library.md` traces back to.

**2. Pin access on the largest macros.** `models: chatgpt, gemini, grok, kimi, meta, minimax m2.7, mistral, qwen, sonnet, yuanbao` (10)
- *Evidence:* kimi — *"pin-access analysis for every macro with >100 pins; how many accessible routing
  tracks exist on each pin-bearing edge."*
- *Red flag:* pins facing a macro wall or a dead corner rather than open core (gemini, yuanbao);
  maximum pin density on any one side above what the edge's tracks can escape (mistral).

**3. Local utilization distribution, not the average.** `models: all 11`
- *Evidence:* chatgpt — *"the utilization distribution, not just the average. Where are the local
  density peaks and how much whitespace is actually available around macros and critical
  interfaces?"* minimax m2.7 asks specifically for density *"within 10 µm of every hard macro."*
- *Red flag:* sonnet — *"any region exceeding ~75–80% (node-dependent — closer to 70% at advanced
  nodes with tighter track counts) before cell insertion has even started."*
- *Node split:* the models agree the number tightens at advanced nodes and disagree on where; see
  `disputed:` below.

**4. Power grid: IR budget closed before any cells exist.** `models: all 11`
- *Evidence:* static IR map plus the intended switching assumption; current density per strap;
  distance from the worst point to the nearest bump/pad.
- *Red flag:* meta — *">100 mV or >200 µm from bump"*; deepseek — *"any spot above 5% drop"*; gemini —
  *"static IR above 2% while starving M3–M5 routing tracks."*
- *The check the reviewer should actually make (sonnet):* *"Is the power-grid IR-drop budget closed at
  floorplan-time with a **worst-case switching activity** assumption, not an average one?"* — the
  only version that names the assumption rather than the number.

**5. Boundary pin assignment against the neighbouring block.** `models: chatgpt, deepseek, gemini, grok, kimi, meta, qwen, sonnet, yuanbao` (9)
- *Evidence:* pin ordering vs top-level netlist ordering and expected dataflow direction.
- *Red flag:* sonnet — pins assigned so the neighbour needs a routing detour; meta — *">200 signals
  crossing the block with no feedthrough channel."*
- *Why:* this is the physical half of the SDC budget problem in `sdc-patterns.md` pattern 1 — a
  budget derived correctly against a pin plan that forces a detour is still wrong.

**6. Clock entry, spine reservation and root placement.** `models: chatgpt, deepseek, grok, kimi, meta, minimax m2.7, mistral, qwen, sonnet, yuanbao` (10)
- *Evidence:* clock pad/root locations, spine route reservation, buffer placement regions.
- *Red flag:* kimi — *"maximum distance from any clock input to the planned clock root exceeds the skew
  budget"*; grok — a macro sitting on the reserved spine that will force a CTS detour.

**7. Routing-layer budget including special nets.** `models: chatgpt, gemini, grok, qwen` (4)
- *Red flag:* gemini — *"max metal layer utilization above 20% on signal layers"* consumed by the grid
  before signals exist.

**8. Node-appropriateness of the whole plan.** `models: chatgpt, minimax m2.7, sonnet` (3)
- chatgpt: *"What evidence says this floorplan is appropriate for the process node rather than merely
  familiar from an older node?"* sonnet: multi-patterning coloring feasibility for the macro-channel
  layout *"not just left to the router."* minimax m2.7: EM and self-heat on the narrowest strap at
  ≤7nm.
- Kept because it is the only check in the gate that interrogates the *method* rather than the data.

**Additional checks appearing once or twice, kept as singletons:** DFT/scan resources represented in
the floorplan (qwen); area reserved for spare cells and planned ECO margin (sonnet); analog/digital
isolation and guard rings (mistral); die aspect ratio against reticle limit and dicing streets
(yuanbao); documented reason for each macro's position — sonnet's *"or is placement just 'wherever it
fit'?"*

### Kill questions

Two forms recur, and they are different in kind:

- **Show me the trial route before a single cell is placed.** grok: *"Show me the trial global-route
  congestion map on this floorplan — are there any regions already red before a single standard cell
  is placed?"* and the counterfactual *"If I move this largest macro 50 µm, does any major bus or
  clock spine become unroutable?"*
- **Name the owner of every nanosecond and every amp.** chatgpt: *"Show me the timing and power
  budgets at the major block boundaries. Who owns every nanosecond and every high-current path?"*

### Waiver culture

Unanimous on the shape: **narrow channels and optimistic utilization are the things that get waived,
and they come back as a routing crisis.** Sharpest — meta: *"Teams waive pin alignment and channel
width to hit schedule, promising 'router will handle it', then pay 2 weeks later moving macros after
first detailed route fails with 5000 DRCs."* kimi puts a number on the return: *"a 2–4 week iteration
later when detailed route cannot resolve pin access and the floorplan must be reopened after CTS is
complete."* deepseek names a different waiver with a worse tail: *"IR drop hotspots are often waived
with a promise to add on-chip decap later, but that decap invariably gets squeezed out."*

`disputed:` **The utilization red-flag number.** 70% (sonnet, advanced nodes) / 75–80% (sonnet,
general) / 75% local at floorplan (gemini) / 85% (meta, as a placement-stage figure). No model
derives the number from track count, and the honest reading is that it is a house convention rather
than a physical threshold. **Worth asking the expert for their own, and for what it is derived from.**

`TODO(expert): review`

---

## Gate 2 — Pre-CTS review (placement done, clocks next)

`models: 11/11` · `confidence 0.55–0.97`

**Purpose (merged).** Decide whether the placement is fit to build a clock tree on. The gate exists
because CTS cannot repair a placement problem and will amplify it: gemini — *"pre-CTS setup timing
tails are often waived assuming clock tree useful skew will fix them, which invariably leads to CTS
power bloat and hold timing disasters."*

### The ordered check sequence

**1. The setup-slack histogram by clock group — shape, not WNS.** `models: all 11`
- This is the single most-repeated check in the entire I slice, and the prompt's own example. Best
  phrasing, sonnet: *"Show me the histogram of setup slack by clock group. A healthy pre-CTS review
  has the wall at zero — not a tail at −300 ps."* grok makes it a question about intent: *"if the wall
  is not near zero, why are we inserting clocks instead of fixing placement?"*
- *Red flag thresholds:* −300 ps recurs across kimi, meta, minimax m2.7 and deepseek (deepseek in the
  form *">5 paths worse than −200 ps"*). kimi supplies the mechanism that makes −300 ps the number:
  *"clock tree synthesis can realistically buy only 50–100 ps of setup slack, and a −300 ps pre-CTS
  WNS almost always becomes a −200 ps post-route WNS requiring a metal spin."*

**2. Congestion map with the clock tree not yet in it.** `models: all 11`
- *Red flag:* gemini — *"max global routing overflow above 0.5% before clock buffers are added"*;
  kimi — *"any macro channel with >10% overflow"*; meta — *"overflow >2% where it overlaps the worst
  timing region."*
- *Why:* meta names the arithmetic nobody else does — *"CTS adds 10–15% more cells and makes
  congestion worse."*

**3. Placement density by region, with the clock tree's growth budgeted.** `models: chatgpt, deepseek, gemini, kimi, meta, minimax m2.7, mistral, qwen, sonnet, yuanbao` (10)
- *Evidence:* density histogram in fixed bins (kimi: 100×100 µm; mistral: 50×50 µm).
- *Red flag:* deepseek — *">85% density at 28nm or >75% at 7nm coinciding with congestion"*; meta asks
  the operational version: *"where can we still insert 1000 buffers for setup fixing?"*
- *sonnet's version is the one a reviewer would actually catch something with:* is density uniform,
  *"or are there placement-tool artifacts — rows of empty sites next to rows of near-100% density?"*

**4. Clock sink distribution and CTS feasibility.** `models: chatgpt, deepseek, grok, kimi, meta, minimax m2.7, mistral, qwen, sonnet, yuanbao` (10)
- *Evidence:* estimated insertion delay and buffer count per domain; ICG placement relative to fanout
  centroid; whitespace near sink clusters.
- *Red flag:* clock-gating cells far from their fanout centroid (grok, mistral, qwen — and the same
  defect appears as a cause in `diagnosis-library.md` FAIL_CTS #3).

**5. Constraint sanity *before* CTS optimizes against them.** `models: chatgpt, gemini, minimax m2.7, qwen, sonnet` (5)
- chatgpt: *"Are the major timing constraints and exceptions proven before we let CTS optimize against
  them?"* gemini: *"zero unconstrained endpoints or invalid clock transfers."* minimax m2.7 escalates
  one case to a stop: a CDC crossing without a synchronizer chain is *"a functional correctness issue
  and the review stops here."*
- This is the gate where `sdc-patterns.md` and this checklist meet: every constraint defect in that
  file is cheapest to catch at exactly this point.

**6. Hold shape pre-CTS.** `models: chatgpt, deepseek, mistral, qwen, sonnet, yuanbao` (6)
- chatgpt: *"Are hold violations structurally localized to genuinely short paths, or is there a broad
  constraint/data-path problem before CTS?"* — the same shape-reading discipline as the setup check.

**7. High-fanout nets and design-rule violations (max transition / capacitance / fanout).**
`models: gemini, grok, meta, mistral, qwen, sonnet, yuanbao` (7)
- *Red flag:* meta — *"nets with fanout >32 or transition >300 ps at 28nm / >150 ps at 7nm"*; grok —
  unbuffered high-fanout non-clock nets above the agreed threshold.

**8. Scan chain order against physical placement.** `models: deepseek, gemini, grok, kimi, qwen` (5)
- Scan reordering after this point creates long routes and, per `diagnosis-library.md`, a recognizable
  hold-failure population.

**9. IR with real placement and a real activity vector.** `models: kimi, meta, minimax m2.7, mistral, sonnet` (5)
- *Red flag:* meta — *"dynamic IR >8% VDD anywhere"* at 20% toggle.

**10. Leftover synthesis artefacts.** `models: grok, meta` (2)
- meta: *"don't-touch and ideal-networks that block optimization — are there leftover ideal nets from
  synthesis?"* grok: don't-touch/size-only/path-group constraints that stopped placement optimizing
  the structure it needed to. A small, specific, easily-missed class.

### Kill questions

- **The histogram question**, in every model's words. gemini's is the crispest: *"Does the setup timing
  slack histogram show a sharp wall at zero, or is there a long failing tail below −300 ps?"*
- **Where will the clock physically live?** chatgpt: *"Show me where the clock tree is physically going
  to live. Which regions have the whitespace and routing capacity to absorb it?"*

### Waiver culture

Unanimous, and this is the strongest consensus in the whole slice: **"CTS will fix it" is the most
expensive waiver in the flow.** minimax m2.7 states it flatly — *"Setup slack violations get waived at
pre-CTS with the assumption that CTS will fix them through gate sizing — this is the most expensive
waiver in ASIC design. CTS cannot fix −300 ps of negative slack; it can only redistribute skew."*
meta describes the congestion version of the same waiver and prices it at *"a loop back to placement
3 days later."* deepseek describes the hold version: buffers promised at CTS *"then cause additional
congestion and sometimes create new setup violations."*

`disputed:` **Is any pre-CTS hold violation acceptable?** deepseek stops the review on *any* hold
violation at this stage; chatgpt, sonnet and yuanbao treat pre-CTS hold as a shape to read rather than
a gate to pass, on the grounds that CTS will move every clock arrival anyway. The second position is
the more common one in the corpus and the more defensible on mechanism, but deepseek's is a coherent
house rule. Flagged, not resolved.

`TODO(expert): review`

---

## Gate 3 — Pre-tapeout timing signoff review

`models: 11/11` · `confidence 0.55–0.98` (the highest-confidence gate; chatgpt, gemini, mistral all ≥0.97)

**Purpose (merged).** The last gate at which a timing problem is cheaper than a respin. chatgpt frames
it as an evidence gate rather than a number gate: prove that nothing is *missing* from the analysis,
then prove the numbers.

### The ordered check sequence

**1. Unconstrained endpoints and broad exceptions — what is *not* being timed.** `models: chatgpt, gemini, grok, kimi, meta, minimax m2.7, qwen, sonnet, yuanbao` (9)
- chatgpt's kill question: *"Show me every unconstrained path and every broad timing exception, and
  prove why each one is intentionally absent from timing signoff."*
- *Red flag:* meta — *"any internal endpoint unconstrained, or false paths >10%"*; gemini —
  *"wildcard false path waivers anywhere in the MCMM matrix."*
- *Why first:* every other check in this gate is conditional on the analysis covering the design. This
  is also where `sdc-patterns.md` pattern 3's warning lands — a false path on a real path passes
  signoff silently.

**2. Every exception justified against RTL or protocol.** `models: chatgpt, deepseek, gemini, grok, kimi, minimax m2.7, qwen, sonnet, yuanbao` (9)
- grok's version is a review technique, not a check: *"Walk me through the three most powerful
  false-path or multicycle exceptions and the protocol evidence that justifies them."*

**3. The full corner × mode matrix, run simultaneously.** `models: all 11`
- *Red flag:* sonnet — *"is timing closed across ALL required corners and scenarios — not just the
  nominal worst case?"*; minimax m2.7 — *"if any path has negative slack at any signoff corner, we are
  not tapeout-ready."*
- *The mode nobody remembers:* test/scan-shift/at-speed/MBIST modes (chatgpt, kimi, meta, qwen).

**4. Real extracted parasitics, at the right stage.** `models: chatgpt, gemini, kimi, minimax m2.7, mistral, qwen, sonnet` (7)
- *Red flag:* gemini — signoff run against trial-route estimates rather than the signoff RC engine;
  mistral — *"RC correlation error >5%."*

**5. Slack decomposition on the worst paths.** `models: chatgpt, meta, sonnet` (3)
- chatgpt: *"For the worst setup and hold paths, can you decompose the slack loss into data delay,
  clock arrival/skew, uncertainty, variation…?"* — the same discipline as the FAIL_TIMING shape read,
  applied as a review demand. Rare and good.

**6. Derating consistent with the methodology agreed at project start.** `models: chatgpt, grok, kimi, meta, minimax m2.7, qwen, sonnet, yuanbao` (8)
- meta asks for the pessimism budget explicitly: *"WNS/TNS with PBA vs GBA, and with AOCV/POCV vs flat
  derate — how much is pessimism?"*

**7. Hold at the fast corner, after the final hold ECO.** `models: chatgpt, deepseek, gemini, grok, kimi, meta, qwen, sonnet` (8)
- chatgpt asks the question that catches the real failure: *"Are hold corners clean after the final
  hold-buffer ECO, and did those buffers re-break setup in any related corner?"*

**8. SI / crosstalk on final routes, with timing windows updated.** `models: chatgpt, gemini, grok, minimax m2.7, qwen, sonnet` (6)

**9. ECO stability trend.** `models: kimi, meta, minimax m2.7, sonnet` (4)
- meta: *"ECO count and last 2 weeks of timing trend — is WNS stable or bouncing?"* sonnet: is the
  final state *"a true global optimum, not a whack-a-mole endpoint?"* This is a process check, and it
  is the one a checklist would normally miss.

**10. Interface budgets reconciled against the top level.** `models: kimi, meta, qwen` (3)
- meta: *"interface budget vs top 0-wire. If sum > period, stop — block will fail at top."* Directly
  the failure mode `sdc-patterns.md` pattern 1 predicts.

**11. Aging, silicon correlation, statistical timing at advanced nodes.** `models: minimax m2.7, qwen, sonnet` (3)
- minimax m2.7: *"has the timing library been validated against silicon at this node? If there is no
  silicon correlation data and this is 7nm or below, the signoff is not complete."*

### Waiver culture

The most quotable answers in the slice. minimax m2.7: *"Minor timing violations (<10 ps) get waived as
'ECO will handle it' — but ECO slots at pre-tapeout are already consumed by functional fixes. The
culture of 'we'll ECO it' at timing signoff is responsible for more late-stage respins than any other
single factor."* chatgpt states the mechanism rather than the anecdote: *"a numerical timing waiver
normally becomes an explicit tapeout liability because the waived margin is no longer available to
absorb later ECO or extraction movement."* kimi describes the tail: small waived violations cause
*"occasional functional failures at corner-case voltage and temperature that require a metal spin or a
firmware workaround to disable the failing feature."*

`disputed:` **Is a small negative slack ever waivable?** deepseek and minimax m2.7 say no at any
corner. chatgpt, grok and kimi describe a documented-waiver path with an owner and a risk assessment.
gemini takes the middle position and names the specific case where it goes wrong: *"small hold
violations in fast corners are sometimes waived under deadline pressure, leading to dead-on-arrival
silicon if post-silicon clock tree skew exceeds expectations."* The disagreement is about house policy,
not physics — but it is exactly the kind of thing a reviewer's checklist encodes.

`TODO(expert): review`

---

## Gate 4 — Physical verification signoff (DRC / LVS / antenna / ERC)

`models: 11/11` · `confidence 0.55–0.99`

**Purpose (merged).** Prove that the database going to the mask shop is the one that was verified, with
the deck that the foundry will use. chatgpt's framing is the operationally sharp one: the gate is about
**provenance of the artefact**, not just cleanliness of the report.

### The ordered check sequence

**1. Deck and database provenance — the check that precedes every other.** `models: chatgpt, gemini, grok, kimi, minimax m2.7, qwen, sonnet, yuanbao` (8)
- chatgpt's kill question: *"Show me the exact final tapeout database, the qualified rule-deck version,
  and the clean DRC/LVS/antenna/ERC results generated from that exact combination. **What changed
  after the last clean run?**"*
- *Red flag:* sonnet — *"the PDK-bundled deck rather than the foundry's latest"*; minimax m2.7 — *"deck
  more than 6 months old"*; grok — version strings that do not match the netlist that timed clean.

**2. DRC clean at zero, with every remaining marker traceable to an approved waiver.** `models: all 11`
- *Red flag:* minimax m2.7 — *"a single unresolved DRC violation of category 'short' or 'open' … shorts
  and opens are not waivable — they are functional failures."*
- chatgpt adds the distinction that matters: a waiver must say *"why it is safe under the current
  foundry rules rather than merely why the marker has historically been ignored."*

**3. LVS true-clean, including properties.** `models: all 11`
- *Red flag:* sonnet — *"any 'don't care' nets, shorted/open exclusions, or property mismatches"*
  hidden behind a headline match; kimi — *"zero shorts, zero opens, **zero soft-connects**."*

**4. Antenna resolved, per layer, with the real charge-accumulation rules.** `models: all 11`
- *Red flag:* deepseek — *"any antenna violation on a clock net is an automatic no."*
- sonnet catches the case the others miss: antenna checked *"for every metal layer, including layers
  added late"* (fill, redistribution).

**5. ERC: floating gates, wells, taps, latch-up spacing, ESD.** `models: chatgpt, deepseek, gemini, grok, kimi, minimax m2.7, mistral, qwen, sonnet, yuanbao` (10)
- sonnet again names the omission: ERC must cover *"floating gates, unconnected inputs, and
  well/substrate tap density — not just the 'headline' DRC/LVS."*

**6. Density and fill, at full-chip scope, after the last ECO.** `models: chatgpt, deepseek, gemini, grok, kimi, meta, mistral, qwen, sonnet` (9)
- *Why it is ordered here and not earlier:* fill is inserted last and can create new DRC, new coupling,
  and new antenna. meta prices the coupling: *"fill adds coupling that breaks timing by 50–100 ps."*

**7. Was verification re-run on the FULL design after the last ECO?** `models: chatgpt, grok, qwen, sonnet` (4)
- sonnet: *"For any block that changed after the last full DRC/LVS run (a late ECO), was verification
  re-run on the FULL design, or only on the changed block?"* This is the single most specific
  escape-catching question in the gate.

**8. GDS round-trip and diff against the frozen version.** `models: qwen, sonnet` (2)
- sonnet: import the final GDS *back* into the layout tool and re-run DRC/LVS; XOR it against the
  previous frozen version *"so that only intended ECOs appear."* Two models out of eleven — and it is
  the check that catches a broken write, which no upstream check can.

**9. Are the remaining DRCs local defects or a systematic pattern?** `models: chatgpt, meta, qwen, yuanbao` (4)
- meta turns it into a stop: *">0 systematic DRCs at the same macro pins after 3 iterations → stop,
  router cannot fix, need floorplan change."* The link back to Gate 1, closing the loop.

**10. Real cells, real IP, real IO ring — not abstracts.** `models: kimi, minimax m2.7, qwen, sonnet` (4)
- sonnet: *"all standard cells and macros represented by their real GDS, not LEF abstract"*; kimi: IO
  cells are *"the foundry-provided complete versions, not the abstracted place-and-route versions."*

**11. Die-to-package interface.** `models: kimi, sonnet` (2) — bump/pad coordinates against the package,
polarity marks, orientation.

**12. Reproducibility by an independent reviewer** from the released data package. `models: chatgpt` (1)

### Waiver culture

The most honest divergence in the file. deepseek and minimax m2.7 hold that DRC waivers are near-fatal
(*"a waived DRC violation that causes a mask failure costs $3–10M and 6–12 months"*). chatgpt, grok and
kimi describe an established, foundry-approved waiver practice that is normal and safe *when
documented* — grok: *"minor density and antenna waivers are common and usually accepted by the foundry
with documentation; what later hurts is waiving LVS discrepancies or via-enclosure issues that turn
into yield or reliability problems once the part is in volume."* gemini names the specific mechanism
for the fill case: waived density rules *"occasionally causing CMP planarization defects that destroy
yield on specific wafer zones."* kimi names the antenna case: *"the gate oxide will survive"* arguments
producing *"parametric drift or early-life failure, sometimes caught only at burn-in test."*

**The synthesis worth keeping:** the waiver itself is not the risk; the *stale* waiver is. chatgpt —
*"undocumented or stale waivers are dangerous because a late rule-deck or layout change can invalidate
the original justification."*

`TODO(expert): review`

---

## Cross-gate observations

1. **Convergence on questions, divergence on numbers.** All 11 models ask about channel width,
   histogram shape, corner coverage and deck provenance. They disagree on nearly every threshold —
   utilization (70/75/80/85%), pre-CTS WNS stop (−200/−300 ps), IR (2%/5%/100 mV), overflow
   (0.5%/1.5%/2%/10%). The questions look like shared provenance; the numbers look like guesses. **Use
   the questions, not the numbers.**
2. **`waiver_culture` is the field that earns this prompt its place.** It is the only field in the
   whole collection that describes organizational behaviour rather than technical fact, and it is where
   the models produced material that reads like experience: "CTS will fix it", "we'll ECO it", "the
   router will handle it", "the foundry will fix it with fill". Each is a named waiver with a named
   downstream cost. Whether those costs are accurate is exactly what the expert can adjudicate quickly.
3. **The gates cross-reference the rest of the digest cleanly.** Gate 1 check 1 is the root cause of
   the whole FAIL_CONGESTION class; Gate 2 check 5 is where every `sdc-patterns.md` defect is cheapest
   to catch; Gate 3 check 10 is the failure predicted by SDC pattern 1; Gate 4 check 9 loops back to
   Gate 1. That coherence is a mild positive signal — the models are not producing four unrelated
   lists.
4. **sonnet is the outlier worth reading first.** It self-rates 0.55–0.60 (every other model 0.85–0.99)
   and contributes the most singleton checks that catch real escapes: the GDS round-trip, full-design
   re-verification after a late ECO, placement-tool density artefacts, worst-case-not-average IR
   assumption, and "is there a documented reason this macro is here". The same anti-correlation between
   confidence and value seen in `episode-draft-bank.md` §2 Finding 5 holds in this slice.

## Salvage notes

- **`mimo i.json` — prose refusal, content preserved.** Same opening sentence as its other four
  refusals. Its four gates are structured and substantive; nothing unique was lost, but its content is
  unreachable by any JSON parser. See `MISSED.md` §2.
- **`minimax m3 i.json` — corruption plus a truncated tail.** The JSON breaks at char 606 on a
  malformed key, and the file ends mid-string with the literal marker
  `[blocked]](streamdown:incomplete-link)` — **a web-UI streaming artefact, not a model truncation.**
  That is a distinct failure cause from the same model's `f.json` truncation and it points at the
  capture step, not the model. 10 orphan check-objects were recovered element-wise and folded in where
  they added a distinct check.
