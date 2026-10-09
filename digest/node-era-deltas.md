# Node-Era Deltas, 28nm → 7nm/5nm — merged from Prompt K outputs

**Status: DRAFT SCAFFOLDING, NOT EXPERT DATA.** Merged model output collected 2026-08-31. Enters any
downstream use as `provenance: synthetic-fixture`, run marker `free-model-harvest/K/2026-08-31`.
Nothing here has been checked against silicon, a PDK, or a practitioner.

**Corpus:** 13 `* k.json` files (Prompt K, `prompts/PROMPT-K-NODE-DELTAS.md`, K-v1). **12 models
produced 110 deltas**; `mimo k.json` is a sixth prose refusal, skimmed. The 110 deltas collapse to
**11 canonical families**, every one of which is claimed by 9–12 models.

**Why the disputes are the deliverable.** The families themselves are near-unanimous and mostly
recoverable from any conference tutorial — *what* changed is not news. The value is in
`why_it_changed` and `what_breaks`, and **`why_it_changed` is where the models disagree, sometimes
diametrically.** A merged consensus that hid those disagreements would be worse than useless: it
would read authoritative while averaging over an unresolved physics question. Every `disputed:` block
below is a place where two models assert incompatible mechanisms for the same observed shift, and at
least one of them must be wrong.

**Confidence is again uninformative.** Range 0.50–0.99. sonnet self-rates 0.50–0.60 across all six of
its deltas and is the only model that declines to invent a mechanism it does not have; the models
carrying the physically wrong claims flagged below self-rate 0.83–0.93.

---

## Family 1 — Timing closure driver: cell delay → wire RC

`models: chatgpt, deepseek, gemini, grok, kimi, meta, minimax 2.7, minimax m3, mistral, qwen, sonnet, yuanbao` (12/12)
`confidence 0.60–0.98`

**At 28nm (consensus).** Cell delay dominates a typical critical path; wire is a second-order term
that buffering and sizing handle. Upsizing a driver is the reliable first move.

**At 7nm/5nm (consensus).** Interconnect — resistance in particular, and via resistance specifically —
becomes a first-order limiter on the lower layers, and the "upsize the driver" reflex stops working.

**`what_breaks` (the strongest in the whole slice).** meta gives the concrete arithmetic a reviewer
could check: *"28nm-trained engineer tries to fix −80 ps setup by upsizing driver from X2 to X4. At
7nm on M2, net delay drops 5 ps but cell delay improves 15 ps, still fails, while added capacitance
worsens IR and congestion. Symptom: timing wall that does not move with sizing."* chatgpt states the
same symptom as a report signature: *"a persistent negative tail of paths whose delay is almost pure
wire/via and that barely move with cell upsizing."* gemini names the specific unforced error:
*"allowing long timing-critical nets to route on default mid-level metals, resulting in un-closable
300 ps+ setup violations caused purely by wire resistance."*

`disputed:` **Three incompatible mechanisms are offered for the same shift.**

1. **Resistance-dominated, via surface scattering** — the majority (chatgpt, gemini, grok, kimi, meta,
   qwen, sonnet, yuanbao). The sharpest statement is gemini's: *"non-linear scaling of metal wire
   resistance as cross-sectional dimensions dropped below electron mean free path in copper
   (~39 nm)"*, with sonnet and meta adding the barrier/liner thickness that does not scale. This is
   the physically standard account.
2. **Capacitance-dominated, and the mechanism *changed*** — minimax 2.7 (conf 0.93) argues the shift
   is not more R but a **coupling-vs-self capacitance inversion**: *"Ccoupling/Cself inverts from
   roughly 0.3 at 28nm to roughly 1.5–2.0 at 7nm."* That is a different physical claim, not a
   rephrasing, and it implies different remedies (spacing/shielding rather than layer promotion).
3. **Not wire at all** — minimax m3 (conf 0.90) **reverses the delta**, titling it *"Timing closure
   dominated by wire delay → cell + variation delay"* and asserting *"resistance per unit length of
   BEOL scales sub-linearly with node"* while stage count and per-stage σ rise. Its `what_breaks`
   follows consistently: *"a 28nm-trained engineer chases wirelength and adds more buffers on long
   nets… the residual slack is in σ, not in C·load."*

**Resolution status: unresolved, and (3) contradicts (1) on a checkable fact.** mistral separately
states *"R ∝ 1/width²"* (superlinear) against minimax m3's "sub-linear" — those cannot both hold.
The majority account is the physically orthodox one and minimax m3's is the outlier, but the
interesting claim is minimax 2.7's, because it is *specific, quantitative and falsifiable against any
PDK's parasitic tables*. **Ask Alice to arbitrate 1 vs 2; treat 3 as probably wrong but note that its
`what_breaks` — buffer-saturated paths where the remaining slack is variation, not load — describes a
real situation regardless of whether its mechanism is right.**

---

## Family 2 — Congestion character: channel routing → pin access

`models: chatgpt, deepseek, gemini, grok, kimi, meta, minimax m3, mistral, qwen, sonnet, yuanbao` (11/12)
`confidence 0.55–0.98`

**The shift.** At 28nm congestion is a *supply* problem measured in tracks across a region — the
macro-channel failure that dominates `diagnosis-library.md`'s FAIL_CONGESTION class. At 7nm/5nm it
becomes an *access* problem at the cell pin: pins shrink to minimum dimensions, access needs specific
track alignment, and cut/via rules restrict where a via may land near a pin.

**The consensus `what_breaks`, stated six different ways and worth all six.** The global-route
overflow number stops predicting routability:
- yuanbao: *"a clean 0.2% global routing overflow report… >30,000 detailed route DRCs on lower metal
  layers."*
- gemini: *"spaces macros adequately and targets 75% utilization, then is surprised when detailed
  route aborts with 200,000+ shorts because the router cannot access cell pins on dense rows despite
  clean global-route overflow."*
- meta: *"DRC count flat after 3 iterations, all at the same locations"* — the non-convergence
  signature.
- chatgpt: the diagnostic error — *"treats congestion as a placement-density problem and tightens the
  placement to 'use the routing resources better'."*

**Direct link to the rest of the digest.** This family is the node-era explanation for the
red-teamed episode in `episode-draft-bank.md` §4 and for the FAIL_CONGESTION trap that 9/9 models
named in `diagnosis-library.md`: *"treating the block-average overflow percentage as the diagnosis."*
The K slice says that reflex is not merely bad practice — it is 28nm practice applied to a node where
the metric measures the wrong resource.

`disputed:` minor — kimi files this as a *utilization* delta and everyone else as a *congestion*
delta. Same content, different taxonomy; noted so the merge does not double-count it.

---

## Family 3 — Utilization targets fell

`models: chatgpt, gemini, kimi, meta, minimax 2.7, minimax m3, qwen, sonnet, yuanbao` (9/12)
`confidence 0.50–0.98`

**Numbers offered.** 70–80% → 60–65% (minimax m3); 70–75% → 55–65% effective (yuanbao); "10–20
percentage points" (minimax 2.7); meta gives it as a capacity ratio — *"effective routing capacity per
cell is ~60% of 28nm."* Broadly consistent; nobody derives the number from track supply.

**`what_breaks`.** meta: *"sets 75% utilization at 7nm to meet area, gets 0% overflow but 8000 DRCs at
pin access and IR drop >100 mV, plus no space for hold buffers. Must expand floorplan 10–15% late."*
minimax m3 adds the review-meeting version: *"presents a 78% utilization floorplan as 'lean' and
pushes density."*

`disputed:` **What actually consumes the missing capacity?** Three answers, and they imply different
fixes:
- **Pin access at the cell** (chatgpt, kimi, qwen, sonnet) — *"shrinking cells does not
  proportionally increase the number of legal connections that can escape each cell"* (chatgpt). Fix:
  cell architecture / placement spacing.
- **Track loss to power grid and coloring keepouts** (meta, kimi, gemini) — capacity taken before
  signals compete for it. Fix: grid planning.
- **Multi-patterning arithmetic** (minimax 2.7) — *"At 7nm with double-patterning, the same drawn
  layer provides N/2 tracks per mask, requiring both masks to be used to achieve equivalent routing.
  If color assignment is imperfect, effective routing capacity is N × 0.7."*

⚠ **The third is physically wrong as stated.** Double patterning decomposes one drawn layer across two
exposures; it does not halve the available tracks — the tracks are the same set, printed in two
passes. The *real* cost is decomposition-driven spacing and colouring conflicts, which is what the
model's own "N × 0.7" fudge factor is standing in for. **Flag: the conclusion (effective capacity
falls) is right; the stated mechanism is not.** minimax 2.7 rated this 0.90.

---

## Family 4 — Hold closure: afterthought → co-equal with setup

`models: all 12` · `confidence 0.50–0.96`

**The shift.** At 28nm hold is a post-CTS ECO measured in hundreds of buffers and a day. At 7nm/5nm
it is a first-class closure problem competing for the same area and tracks as everything else.

**`what_breaks`.** meta names the loop: *"fixes setup first, then adds hold buffers at end, creating
congestion that breaks setup again, loop never ends. Or uses zero hold uncertainty at 7nm, gets
silicon hold failure that cannot be fixed by frequency reduction."* That last clause is the sharpest
consequence stated anywhere in the slice — **a hold failure cannot be binned out, unlike a setup
failure.** grok/mistral add the cross-corner version: post-route hold fixing that *"causes hundreds of
new setup violations to appear in the slow-temperature corner."*

`disputed:` **Did nominal clock skew get bigger, or did the skew budget get smaller?** This is the
sharpest model-vs-model contradiction in the K slice, and the two claims are mutually exclusive:
- **Skew got bigger** — minimax 2.7 (conf 0.88): *"Clock skew at 7nm is inherently larger (50–100 ps
  vs 20–30 ps at 28nm) due to longer clock wires and less ideal mesh topologies."*
- **Skew is fine; the budget shrank and the derate grew** — kimi (conf 0.85): *"50 ps of skew was
  tolerable at 1 ns but consumes the entire margin at 500 ps"*; and minimax m3 (conf 0.85) goes
  further, asserting hold fails *"even with a perfectly balanced tree"* because *"nominal skew is
  small compared to derate-adjusted skew."*

**These cannot both be the primary mechanism**, and they point at different remedies — mesh
re-architecture (minimax 2.7) versus variation-aware budgeting and useful-skew discipline (kimi,
minimax m3, sonnet). Note the internal tension in the corpus: Family 5 has near-unanimous agreement
that the *reason* meshes were adopted was to **reduce** skew and its variation, which sits badly with
minimax 2.7's claim that 7nm skew is inherently larger because meshes are "less ideal".

**Secondary mechanism split, less sharp:** variation/OCV (deepseek, grok, sonnet, minimax m3, mistral,
qwen), physical space for delay buffers (chatgpt), clock insertion growing faster than data paths
shrink (meta), and near-threshold VDD non-linearity plus multi-Vt corner divergence (gemini). meta is
the only model to quantify: variation is *"30% of path vs 10% at 28nm."* **Unverified and worth
checking — it is the kind of number that would anchor a whole methodology if true.**

---

## Family 5 — Clock distribution: tree → mesh / spine / hybrid with useful skew

`models: chatgpt, deepseek, gemini, grok, kimi, minimax 2.7 (×2), minimax m3, mistral, qwen` (10/12)
`confidence 0.82–0.94`

**The shift.** Balanced H-tree with a tool-optimized CTS gives way to mesh or trunk-plus-mesh
topologies, deliberate useful skew, and in some accounts deskew loops — with clock topology becoming
a *planning* decision at floorplan rather than a CTS-tool outcome.

**`what_breaks`.** minimax m3: *"builds a 'skew-minimal' tree first and applies small useful skew to
critical paths. Symptom: hold fails massively across the chip because OCV derate exceeds intentional
skew; large-scale mesh restructuring."* gemini: *"relies on default P&R CTS synthesis without
structured trunk planning; clock skew and corner-to-corner skew variation consume over 25% of the
target clock period."*

`disputed:` **Why mesh?** Four mechanisms, only partly compatible:
- **Averaging against variation** (deepseek, minimax m3, mistral) — a mesh averages many drivers so
  local variation cancels. deepseek adds the cost honestly: *"but power becomes a bigger concern."*
- **Wire resistance on the trunk** (minimax 2.7) — quantified: *"a 5 mm clock wire that was 10 Ω at
  28nm becomes 50–60 Ω at 7nm"* and a buffer *"cannot equalize delay across it."*
- **Clock power** (gemini) — *"up to 40% of block dynamic power."*
- **Sink count and physical complexity** (chatgpt) — more sinks, tighter geometry.

These are not mutually exclusive, but they rank differently and the first two conflict with each
other on whether the problem is *statistical* (variation, solved by averaging) or *deterministic*
(trunk RC, solved by topology and shielding). **The cheap discriminator Alice could give in one
sentence: does the 7nm skew problem shrink when you reduce derate, or only when you change topology?**

⚠ **gemini's title says "Unstructured CTS Trees → H-Tree and Mesh"**, placing H-tree as the *modern*
end state; every other model places balanced H-tree at the **28nm** end and mesh at the modern end.
Probably loose wording rather than a claim, but it inverts the delta as written.

---

## Family 6 — Multi-patterning and colouring enter placement

`models: chatgpt, deepseek, gemini, grok, kimi, meta, minimax 2.7, minimax m3, mistral, qwen, yuanbao` (11/12)
`confidence 0.80–0.97`

**The shift.** Placement moves from a continuous geometric problem to a constrained-discrete one:
track-aligned, colour-aware, with legality that a router cannot repair after the fact. minimax 2.7's
framing is the crispest — *"decomposes placement from a continuous to a constrained-discrete
problem."*

**`what_breaks` — the best-specified mistake in the entire slice.** kimi: *"a cell shifted by half a
track can block access to adjacent pins or create spacing violations that no router can resolve."*
gemini extends it to the review symptom: *"manually shifts a cell by half a track to fix a local
timing violation, creating a coloring conflict that propagates across the row and produces thousands
of unresolvable detailed-route DRCs."* meta names the odd-cycle failure explicitly — a colouring
conflict with no legal two-colour assignment, which is a *graph* property, not a spacing one, and
therefore genuinely unfixable by local repair.

`disputed:` **The single-exposure pitch limit.** meta says *"pitch below 40 nm exceeds single exposure
lithography resolution for 193i"*; minimax 2.7 says *"at 28nm, 193 nm immersion could print ~80 nm
features."* **Resolvable: these are half-pitch versus pitch.** 193i single-exposure resolves roughly
80 nm pitch ≈ 40 nm half-pitch, so both are right in their own units and neither says which it means.
Recorded because a reader merging them naively would get a 2× error.

`disputed:` **Does EUV remove the problem?** chatgpt and yuanbao say it moves *some* layers to single
exposure but does not eliminate multi-patterning; minimax m3 says EUV *"relaxes some LELE rules but
SADP-finned BEOL still needs color constraints"*; gemini implies EUV brings its own *"tight design
constraints"* and rigid 1D gridded rules. Directionally compatible, and the honest merged statement
is "EUV changes which layers are affected, not whether colouring is a placement constraint."

---

## Family 7 — Library / Vt mixing: 2–3 flavours → fine-grained multidimensional selection

`models: deepseek, grok, kimi, meta, minimax m3, mistral, qwen` (7/12) · `confidence 0.80–0.93`

**The shift.** From a simple HVT/SVT/LVT swap late in closure to fine Vt granularity plus channel-length
biasing and (per minimax m3) fin-count as an additional axis, applied throughout closure rather than
at the end.

**`what_breaks`.** qwen: *"uses LVT cells liberally to close timing easily, then faces a 30–50%
static-power overshoot that requires full netlist re-synthesis and placement restart."* meta gives the
two-sided version — LVT everywhere blows leakage, HVT everywhere gives a setup wall — with the symptom
*"power vs timing Pareto never converges."* minimax m3 names the scheduling error: *"defers Vt/fin
swaps to 'when we run out of slack'."*

`disputed:` **Is leakage the binding constraint?** Ten models across this and other families assume it
is. **minimax m3 asserts the opposite** — *"dynamic power is low enough that a small per-cell leakage
increase is acceptable"* — which inverts the premise the entire family rests on. Given that every
`what_breaks` in this family describes a leakage overshoot, minimax m3's premise contradicts its own
neighbours and probably its own `what_breaks`.

⚠ **mistral's mechanism is physically wrong.** *"FinFETs offer independent gate control, enabling more
Vt options."* Multi-Vt in production FinFET libraries comes from **work-function metal engineering**
(and channel-length biasing), not independent gate control — which is a distinct device structure not
used for standard-cell Vt flavours. deepseek states the correct mechanism (*"work-function differences
and fin-height variations"*), so the corpus contains both the right and the wrong account at similar
confidence (0.87 vs 0.93). **The wrong one is more confident.**

---

## Family 8 — Signoff corner and variation-model explosion

`models: chatgpt, deepseek, gemini, grok, kimi, meta, minimax 2.7, mistral, qwen, sonnet, yuanbao` (11/12)
`confidence 0.55–0.98`

**The shift.** From a manageable corner matrix with flat OCV derates to MCMM matrices measured in
hundreds of scenario-corner combinations, with AOCV/POCV or statistical timing replacing flat derate.

**`what_breaks` — two genuinely non-obvious silicon failures:**
- **Temperature inversion.** grok: *"signs off at typical, best, and worst cases, then sees silicon
  failures at a corner where temperature inversion makes the fast-fast corner slower than typical,
  violating assumptions built into the timing budget."* This is the single best cross-era trap in the
  slice — the 28nm intuition that cold-and-fast is the hold corner and hot-and-slow the setup corner
  stops holding at low VDD.
- **Low-voltage corner divergence.** meta: *"signs off at TT only with flat derate, misses
  slow-low-voltage corner that is 25% slower than SS at nominal VDD, causing speed bin failure."*

`disputed:` nothing substantive on mechanism. The one methodological split is whether POCV/statistical
timing is now standard (yuanbao, minimax 2.7) or still an option layered on AOCV (grok, meta) —
plausibly a house/foundry difference rather than a disagreement about the world.

---

## Family 9 — IR drop and EM: late check → first-class, floorplan-stage constraint

`models: chatgpt, deepseek, grok, kimi, meta, minimax 2.7, minimax m3, mistral, qwen, sonnet, yuanbao` (11/12)
`confidence 0.55–0.99`

**The shift.** IR/EM moves from a post-route signoff check to a constraint that shapes floorplan and
placement, and becomes coupled to timing rather than checked beside it.

**`what_breaks`.** chatgpt: *"defers IR/EM signoff until after route. Symptom: last-mile IR-drop
hotspots near clock-tree spines and high-activity regions force global restructure of the clock and
P/G, blowing the schedule."* gemini contributes the placement-level version that a 28nm engineer would
actively believe is good practice: *"tightly clusters register banks to minimize clock latency,
causing severe dynamic IR drop during simultaneous switching that degrades silicon operating frequency
below STA predictions."* meta quantifies: same PG pitch carried over from 28nm gives *"dynamic IR
80–120 mV hotspot that degrades timing 80 ps."*

**Cross-reference:** this is the same defect `diagnosis-library.md` FAIL_IR_DROP catalogues as
"static remedy for a dynamic defect", and `review-checklists.md` Gate 1 puts at check 4. The K slice's
contribution is the era claim: at 28nm deferring it was *survivable*, and that is what changed.

---

## Family 10 — Power grid versus signal routing: background resource → direct competition

`models: chatgpt, deepseek, grok, kimi, meta, mistral, yuanbao` (7/12) · `confidence 0.88–0.97`

**The shift.** The grid stops being something laid down early and forgotten, and becomes a direct
competitor for the same tracks the router needs — with the added trap that strengthening it late is
the one fix guaranteed to break routing.

**`what_breaks`** — the cleanest deadlock statement in the slice, deepseek: *"uses the same power grid
density as before, but the block fails IR drop at signoff; when adding more stripes, congestion blows
up, and routing becomes impossible because they didn't reserve extra tracks."* chatgpt names the
planning error: *"plans a sparse power grid and adds straps late in the flow, only to discover that
the added straps block critical routes."*

---

## Family 11 — DRC character: spacing/width → via enclosure, cut rules and pin access

`models: chatgpt, deepseek, grok, kimi, meta, minimax 2.7, minimax m3, mistral` (8/12)
`confidence 0.80–0.98`

**The shift.** The dominant DRC families change identity: from spacing and width violations that a
router can nudge away, to via enclosure, cut spacing, end-of-line and pin-access violations that are
often unfixable without moving cells.

**`what_breaks`.** meta gives the trap most likely to catch a careful engineer doing the *right* 28nm
thing: *"enables automatic double via everywhere to help EM, then gets 2000 via enclosure DRCs that
router cannot fix without ripping up M1. Tries to waive as 'via will be fixed later', but they are
real manufacturing violations."* minimax m3 names the interaction that makes late cleanup fail:
*"hundred-thousands of color/decoloration/equivalent-via violations that interact with each other."*

**Cross-reference:** `review-checklists.md` Gate 4 check 9 — "are the remaining DRCs local defects or a
systematic pattern?" — is the review-time expression of exactly this delta.

---

## Cross-family observations

1. **Unanimity on *what*, disagreement on *why*.** All 11 families are claimed by 9–12 models; five
   carry mechanism contradictions where at least one model must be wrong. **The consensus layer of
   this slice is worth little and the disputed layer is worth a lot** — the opposite of how a merge is
   normally read.
2. **Four checkable physical errors, all from confident models.** minimax 2.7's double-patterning
   track arithmetic (0.90), minimax m3's sub-linear BEOL resistance (0.90) against mistral's R ∝ 1/w²
   (0.98), mistral's independent-gate-control account of multi-Vt (0.93), and gemini's inverted
   H-tree/mesh ordering (0.94). Each is decidable in one sentence by anyone who has done the node.
   **They are the highest-value questions to put to Alice from this slice, because each is cheap to
   answer and each currently sits in the corpus at high confidence.**
3. **`what_breaks` delivered what the prompt promised.** It is the field with the least
   model-to-model overlap and the most operational content — the half-track cell shift, the automatic
   double-via backfire, temperature inversion, the hold failure that cannot be binned out, the
   0.2%-overflow / 30,000-DRC gap. Whether or not the mechanisms survive review, these are
   recognizable-or-not in one reading by a practitioner, which makes them fast to grade.
4. **This slice is the era key for the rest of the digest.** It explains why `diagnosis-library.md`'s
   FAIL_CONGESTION advice needs a node qualifier, why the SDC over-constraint patterns behave
   differently at 7nm, and why `review-checklists.md`'s thresholds split by era. If any of the K
   material graduates, it should graduate as annotations on those files rather than as standalone
   episodes.

## Salvage note

`mimo k.json` — sixth consecutive refusal-then-answer, same opening sentence. Its prose covers the
same families and adds nothing unique. See `MISSED.md` §2.

`TODO(alice): review — the four checkable errors in observation 2 first, then the two mechanism
disputes in Families 1 and 4.`
