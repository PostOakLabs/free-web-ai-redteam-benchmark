# SDC / Constraint-Derivation Patterns — merged from Prompt G outputs

**Status: DRAFT SCAFFOLDING, NOT EXPERT DATA.** Merged model output, 2026-08-31. Enters any
downstream use as `provenance: synthetic-fixture`, run marker `free-model-harvest/G/2026-08-31`.
This is the zero-prior-art category, which is exactly why the arithmetic below is checked rather
than trusted.

**Corpus:** 11 G-files → **88 pattern drafts** from 10 models (chatgpt 9, deepseek 10, gemini 7,
grok 10, meta 8, minimax 2.7 10, minimax 3 7, mistral 10, qwen 8, yuanbao 9) plus one prose-only
refusal (`mimo g.json`, skimmed — its content duplicates pattern 1 and adds nothing new).
The 88 drafts collapse to **13 canonical patterns**; convergence is high, which is itself
informative (see the closing note).

**Arithmetic policy.** Every worked example was recomputed. Patterns are marked:
`✅ closes` (the numbers are internally consistent), `⚠ partial` (arithmetic closes but a term is
misplaced or double-counted), `❌ does not close` (a stated formula or example is wrong). A red mark
is not a reason to discard the pattern — the *shape* is usually still right — but the numbers must
never be lifted without correction.

---

## Pattern 1 — Block-boundary input/output delay budget

`models: all 10` · `confidence 0.85–0.98` · **the universal pattern; 14 of 88 drafts**

**Situation.** A block is implemented before its neighbour exists, but its interface timing must
represent the eventual top-level contract.

**Derivation (merged, corrected).** Start from the interface period T. Account explicitly for:
upstream clock-to-Q, upstream logic, interconnect, downstream logic, capture setup, clock
uncertainty, and named margin. `set_input_delay` on a block's input = *everything that happens
outside the block before the data arrives* (upstream Tcq + upstream logic + interconnect).
`set_output_delay` on a block's output = *everything that happens outside the block after the data
leaves* (interconnect + downstream logic + downstream setup). The block's own internal budget is
`T − boundary_delay − uncertainty`.

**Best worked example (qwen, ✅ closes).** T = 1000 ps, wire W = 100 ps, capture setup S = 50 ps →
logic budget 850 ps, split 50/50 → L_A = C_B = 425 ps. Then
`set_output_delay(A) = W + C_B = 525 ps`, so A's internal path is constrained to
`1000 − 525 − 50 = 425 ps`; symmetrically `set_input_delay(B) = L_A + W = 525 ps`.
Closure check, stated by the model itself: `425 + 100 + 425 + 50 = 1000 = T`. ⚠ *one caveat:* the
per-block lines subtract S from both sides while the closure line counts it once; on A's side the
downstream setup is already inside `output_delay`, so subtracting it again is a small
double-count. The shape is right and the total closes — fix the A-side line before reuse.

**Second-best (grok, ✅ closes).** T = 2.0 ns; external clock uncertainty 0.15 + external logic 0.6
+ package 0.1 → `input_delay max = 0.85 ns`, internal must close in 1.15 ns. Clean and traceable to
named sources for every term.

`disputed:` **deepseek inverts the two delays (❌).** It states "Input Delay = T_wire + T_setup;
Output Delay = T_cko + T_wire" — that puts the *receiving* block's setup into the input delay and
the *launching* block's clock-to-Q into the output delay, which is backwards on both. Every other
model, and the closure arithmetic, gives input = upstream Tcq + wire, output = wire + downstream
setup. **Resolution: deepseek is wrong; do not reuse its formula.** Its confidence was 0.95.

`disputed:` **Percentage heuristics.** yuanbao offers "input ≈ 40% T, output ≈ 40% T, leaving ~20%
internal" while its own `wrong_way` field condemns percentage splits; minimax 3 offers "input_delay
= T_capture_margin / 2 rounded conservatively". Both are the very thing pattern 2 exists to replace.
Treat percentage splits as a *placeholder only when far-side depth is genuinely unknown*, which is
the one defensible use (see pattern 2).

**wrong_way (sharpest, chatgpt).** "Assigning a convenient value such as 50% of the period to
input_delay and 50% to output_delay without accounting for clock-to-Q, interconnect, setup, skew,
uncertainty, or asymmetry silently transfers an impossible burden to one block. The downstream
symptom is often a block that is 'clean' under its local SDC but fails when integrated."

**signoff_risk.** Too tight → the block over-optimizes: buffering, area, power, congestion, and
possibly damage to unrelated timing. Too loose → the block passes local STA while the integrated
path has no time for the neighbouring logic; discovered after both blocks are frozen, patchable only
by ECO or a frequency cut (yuanbao).

**Missing from all 10 drafts:** nobody pairs `-max` with `-min` in the *main* derivation except
yuanbao, which states it plainly — "skipping `-min` leaves hold unconstrained on boundary paths."
That omission is itself the most common real-world version of this bug and belongs in the pattern.

---

## Pattern 2 — Asymmetric (logic-depth-proportional) split between two unimplemented blocks

`models: chatgpt, gemini, grok, meta, minimax 2.7, minimax 3, mistral, qwen, yuanbao` (9)
`confidence 0.75–0.98`

**Derivation.** Split the residual budget by estimated logic depth, not by halves. meta:
20 FO4 stages vs 10 → 66/33 (✅ closes: 20/30 = 66.7%). mistral/qwen use
`T_A = T_total × L_A / (L_A + L_B + L_wire)`. minimax 3 allocates 60% blocks / 20% interconnect /
20% skew+margin (✅ sums to 100). yuanbao: "give the harder block more of the period… document the
assumption explicitly: 'B assumed to need 3 logic levels, A assumed 1'."

**Best worked example (qwen, ✅ closes).** T = 1000 ps; 2 pipeline stages at 400 ps each + 100 wire
+ 50 setup = 950, leaving 50 ps slack. `output_delay(A) = 100 + 400 = 500`, then a documented 15%
over-constraint → 575 ps, so A must close in `1000 − 575 − 50 = 375 ps` rather than 400. Every step
recomputes correctly, and the 15% is named as an assumption for later relaxation — the only draft in
the corpus that separates *budget* from *margin* explicitly.

**gemini's worked example is the corpus's most instructive failure (❌ does not close).**
T = 2.0 ns, block A 10 levels ≈ 0.80 ns, block B 4 levels ≈ 0.32 ns, interconnect 0.20 ns. It
computes `T_A = 0.80 + 0.10 = 0.90` and `T_B = 2.0 − 0.90 = 1.10`, then writes
`set_output_delay -max 1.10` on A and `set_input_delay -max 0.90` on B — **the two values are
applied to the wrong ports**, and B's 1.10 ns "budget" bears no relation to its measured 0.32 ns of
logic. The `wrong_way` field attached to it is nonetheless correct and quantitatively consistent
(under a 50/50 split B holds 680 ps of unexploited slack: 1.0 − 0.32 = 0.68 ✅). **Keep the
wrong_way, discard the derivation.** gemini rated this 0.95.

**wrong_way (sharpest, minimax 2.7).** "Splitting the budget 50/50 because it is simple, without
considering that one block may be fundamentally more complex — one block ends up over-budget, the
other under-utilized, and the frequency target is silently missed."

**signoff_risk.** yuanbao names the failure that actually happens: "an interface that was never
jointly validated against real netlists is a classic source of last-minute frequency cuts." grok
names the second-order effect: "one side too tight: that block burns area while the other has unused
margin; frequency cannot be raised."

**Consensus caveat worth keeping (yuanbao):** "output delay on A is the same physical constraint as
input delay on B — defining them inconsistently (different clocks, different margins) creates a
contradictory budget that neither side can meet."

---

## Pattern 3 — False path vs multicycle path

`models: all 10` · `confidence 0.85–0.98` · **the highest-confidence pattern in the corpus**

**Derivation (consensus, correct).** Ask whether the path can *ever* be launched and captured in
adjacent cycles under any legal sequence. If no — mutually exclusive modes, static configuration,
scan-only — it is a false path. If yes but the protocol guarantees N cycles, it is a multicycle:
`set_multicycle_path N -setup` **paired with** `set_multicycle_path N-1 -hold`. The cycle count comes
from the RTL/protocol event sequence, never from the amount of slack wanted.
`models agreeing on N / N-1: chatgpt, gemini, grok, meta, minimax 3, qwen, yuanbao` (7)

**Best statement of *why* N−1 (qwen).** "The hold is set to N−1 because the default hold check is at
the same edge; with setup at edge N, hold must be checked at edge N−1 to maintain the correct
relationship." gemini supplies the cost of omitting it: with `set_multicycle_path 4 -setup` and no
hold exception at T = 1.0 ns, "STA defaults the hold check to one cycle prior to the setup capture
edge, forcing P&R to insert 3.0 ns worth of redundant delay buffers on the data path, causing area
bloat and routability failure." ✅ arithmetic consistent.

`disputed:` **minimax 2.7 gets the multiplier wrong (❌).** It states "Set multicycle = N − 1 for
setup. Example: 2-cycle read RAM → `set_multicycle_path -setup 1`" and "hold multicycle = 0".
`-setup 1` is the default single-cycle check — it relaxes nothing — and the paired hold value is
wrong. **Resolution: 7 models against 1, and the majority is correct. Setup takes N, hold takes
N−1.** minimax 2.7 rated it 0.91. This is the clearest case in the corpus of a confident,
plausible-sounding, *off-by-one* constraint that would pass casual review and silently under- or
over-constrain a real design.

**wrong_way (sharpest, minimax 3).** "Defaulting to `set_false_path` for anything that 'looks slow'
to make timing clean. The tool removes it from optimization entirely, so the cells on that path
never get sized for delay and never get checked for hold — at signoff the path either fails hold (if
it is actually exercised under some test mode or scan) or draws excessive leakage because the cells
were left at minimum size." The leakage consequence is unique to minimax 3 and is a genuinely
non-obvious second-order effect.

**signoff_risk (sharpest, yuanbao).** "These are among the most dangerous SDC errors because they
pass STA cleanly yet fail in silicon." grok localizes it: "a rare corner or a software change
activates the path and the chip fails in the field."

**Extra check worth keeping (qwen).** Verify the N-cycle guarantee holds *across all modes* —
"normal, debug, scan, low-power. If any mode collapses the path to fewer cycles, the multicycle
constraint is wrong."

---

## Pattern 4 — Asynchronous CDC constraint

`models: all 10` · `confidence 0.80–0.98`

**Derivation (consensus).** Establish first whether the clocks genuinely have no phase relationship.
If asynchronous *and* every crossing signal passes a real synchronizer:
`set_clock_groups -asynchronous -group {clkA} -group {clkB}`. Then — and this is where the models
split — bound the synchronizer's own data path with `set_max_delay -datapath_only` so the router
cannot take a long detour and eat the metastability resolution window.

`disputed:` **Does the CDC path get a max_delay, or nothing at all?**
- *Bound it* (chatgpt, grok, meta, mistral, qwen, yuanbao, deepseek — 7 models): grok gives the
  quantity — "`set_max_delay` from async input to first synchronizer flop equal to a fraction of the
  receiving clock period (often ½ or ⅔) to force a short path and reduce MTBF impact." qwen gives
  the concrete case: gray-code FIFO pointers, "e.g. 500 ps for a 1 GHz design."
- *Do not bound it* (minimax 2.7, and minimax 3 for handshakes): "Do NOT `set_max_delay` on async
  paths — a max delay constraint implies a timing relationship that does not exist, and the tool
  will try to optimize it."
- **Resolution: the majority is right and the minority is confusing two different paths.** The
  `-datapath_only` max_delay bounds *wire delay on the data path into the first synchronizer flop*,
  which is a physical quantity with no implied clock relationship; it does not assert an edge
  relationship. minimax 2.7's objection would be correct only for a max_delay that spans the clock
  boundary *without* `-datapath_only`. Worth stating explicitly, because the distinction is exactly
  what makes the constraint safe.

`disputed:` **yuanbao additionally proposes a `set_min_delay` on the CDC path** ("ensure the signal
does not arrive too fast, which can cause the second flop of the synchronizer to see an illegal
transition"). No other model proposes this and the stated mechanism is dubious — the second flop is
protected by the first flop's clock, not by data arrival time. **Flagged as probably wrong; do not
propagate without Alice's ruling.**

**wrong_way (sharpest, qwen).** "Blanket `set_clock_groups -asynchronous` between all clock pairs
without auditing whether synchronizers actually exist on every crossing signal. This makes STA pass
cleanly but hides paths that have no metastability protection." meta adds the failure mode nobody
else names: "using `set_clock_groups -logically_exclusive` for async clocks, which is for muxed
clocks, not async, and causes incorrect crosstalk and CRPR analysis."

**signoff_risk (sharpest, yuanbao).** "CDC mistakes are a leading cause of chips that 'work on the
bench but fail in the field'."

**Nice extra (minimax 3).** The only draft that puts real arithmetic on the *right* quantity: the
constraint carries no arithmetic, the MTBF does — `MTBF = exp(t_res / C) / (fA · fB · fc)`, "require
MTBF >> product lifetime." Symbolic, unverified, but it points at the calculation that actually
governs the decision.

---

## Pattern 5 — Virtual clock for external / off-chip I/O

`models: all 10` · `confidence 0.84–0.96`

**Derivation (consensus, correct).** Create a virtual clock with the *external* reference period.
`set_input_delay -max` = external device clock-to-out (max) + board/package trace (max);
`set_input_delay -min` = external Tco(min) + trace(min). `set_output_delay -max` = downstream setup +
trace; `-min` = −(downstream hold − trace skew). The virtual clock is a reference, not a claim that
the external clock exists inside the block.

**Best worked example (gemini, ✅ closes).** T = 10.0 ns; external Tco max 4.5 / min 1.0; board
flight max 1.2 / min 0.8 → `input_delay -max = 5.7`, `-min = 1.8`. Every term named and sourced.

**Second (qwen, ✅ closes).** External PHY 10 ns period, data valid 2 ns after the PHY edge →
`input_delay = 2 ns`, internal capture path has `10 − 2 − setup ≈ 7.5 ns`.

**gemini's source-synchronous output example (⚠ partial).** T = 2.5 ns (400 MHz ✅), half-period
1.25 ✅; `max output delay = 1.25 − 0.25 − 0.05 = 0.95` ✅; `min = 0.25 + 0.05 = 0.30` ✅ — but the
SDC line then reads `set_output_delay -min -0.30`, negating a value it just computed as positive.
Either the sign or the derivation is wrong; both conventions exist for centre-aligned DDR, which is
precisely why the draft cannot be reused without resolving it.

**meta's formula contradicts its own example (❌).** Stated: "`set_input_delay` = T_ext − Tsu_ext −
board_delay + margin." Worked: "external device Tco 2 ns, board 0.5 ns, T = 4 ns ⇒ input_delay =
2.5 ns." The example computes `Tco + board` (correct); the formula says something else entirely.
**Keep the example, discard the formula.**

**mistral's formula is wrong (❌).** "`set_input_delay -max = (T_ext/2) − T_setup_internal −
T_uncertainty`" pulls the *internal* setup into an *external* budget, which is the exact error the
pattern exists to prevent, and the half-period term is unexplained. Its own `wrong_way` field then
correctly warns against conflating internal and external clocks — the draft contradicts itself.

**wrong_way (sharpest, gemini).** "Constraining DATA_IN relative to internal root clock CLK_CORE
instead of virtual clock VCLK_EXT. The P&R tool factors internal clock tree insertion delay (e.g.
2.5 ns) into the I/O path calculation, artificially over-constraining the input path by 2.5 ns and
causing impossible setup closure."

**signoff_risk (sharpest, yuanbao).** "This class of error is especially nasty because it may pass
STA but fail on the board due to the optimistic board-model assumptions baked into the virtual
clock."

**Consensus omission worth keeping (yuanbao, grok).** Always pair `-max`/`-min`; and for a pure
pad-to-pad combinational path, `input_delay + feedthrough + output_delay = virtual clock period` is
the closure identity.

---

## Pattern 6 — Generated / divided clock derivation

`models: all 10` · `confidence 0.85–0.97`

**Derivation (consensus, correct).** `create_generated_clock -source <physical pin of the master> …
-divide_by N` (or `-multiply_by M -divide_by N`, or `-edges`) **on the generating pin**, never a
fresh `create_clock`. The tool then derives period, phase and source latency. yuanbao states the
rule most precisely: "`-source` must be the master clock's physical origin (e.g. the CK pin of the
divider flop, or the input of the PLL), not an arbitrary node" — and adds the mux case: "if the
generated clock passes through a mux with multiple sources, each source needs its own
`create_generated_clock` with `-add`… paths under an unmodeled source become untimed."

**Arithmetic.** minimax 3 states the only closure identity in the group: "if generated frequency is
`f_src · M/N`, the period is `T_src · N/M`, and any IO budget at that boundary uses T_generated."
✅ consistent.

**wrong_way (unanimous).** Declaring an independent `create_clock` on the divider output with the
derived period. Consequences, merged: launch/capture edge misalignment, meaningless cross-domain
exceptions, misleading CTS behaviour, and — grok's version — "setup/hold windows wrong by a factor
of N."

**Underrated caveat (chatgpt).** "Assuming a divide-by-N waveform is always a simple 50%-duty-cycle
clock can be wrong for implementations whose actual edge sequence is asymmetric." Only chatgpt
raises duty cycle at all; it is the failure mode that survives an otherwise-correct `-divide_by`.

**Second underrated caveat (minimax 3).** "Using `-multiply_by M` without checking that the PLL is
configured for that M in the actual silicon; the generated clock period in SDC doesn't match the
silicon." A constraint that is internally perfect and externally false.

**signoff_risk (sharpest, yuanbao).** "At advanced nodes, a wrong generated-clock phase can create
millions of false violations that obscure real ones, or hide real violations behind a wrongly
relaxed check."

---

## Pattern 7 — Early over-constraint with staged relaxation

`models: chatgpt, deepseek, grok, meta, minimax 2.7, mistral, qwen, yuanbao` (8)
`confidence 0.75–0.96` · **the widest spread of advice in the corpus**

**The disagreement is the finding.** Recommended early over-constraint factor:

| Model | Recommendation | Recomputed |
|---|---|---|
| qwen | period × 0.80–0.85 early → 0.90 at RTL freeze → 1.0 at tapeout readiness | ✅ stated schedule, milestone-tied |
| minimax 2.7 | constrain at 1.2 GHz for a 1 GHz target = 833 ps, "~17% headroom" | ✅ (1000−833)/1000 = 16.7% |
| meta | period × 0.9, +100 ps uncertainty at 28nm / 60 ps at 7nm, `set_max_delay 0.85·T` on boundaries | ✅ internally consistent |
| deepseek | period × 0.85, calibrated from "typical 15% degradation synthesis→post-route on this node, from previous tapeouts" | ✅ and it is the only draft that names *where the number comes from* |
| grok | +30–50 ps extra uncertainty only (not a period squeeze) | — |
| mistral | uncertainty = 0.15·T setup / 0.10·T hold; `set_max_delay 0.7·T` inter-block | ⚠ 15% of period as uncertainty is very large; no source given |
| yuanbao | uncertainty 0.25 ns pre-CTS → 0.12 post-CTS → 0.08 + OCV post-route | ✅ and uniquely insists on **never relaxing to zero guardband** |

`disputed:` **Squeeze the period, or add uncertainty?** grok and yuanbao add margin through
*uncertainty* and leave the period alone; qwen, meta, minimax 2.7 and deepseek squeeze the *period*.
The distinction matters: a period squeeze scales every path including ones with no real risk, while
uncertainty targets the clock-related unknown that is actually unknown pre-CTS. Nobody argues the
point explicitly. **This is the most useful open question in the G corpus for an expert to settle.**

**wrong_way (two directions, both real).** Never relaxing (meta, quantified): "keeping 0.9T to
signoff… at 28nm this causes 20–30% extra buffers, 15% more area, IR and congestion death; at 7nm
impossible DRC and power blow-up." Relaxing carelessly (chatgpt): "arbitrarily relaxing constraints
later because the tool is failing… can make implementation appear healthy while silently reducing
the guaranteed signoff margin."

**Best discipline statement (yuanbao).** "Initial uncertainty = jitter + estimated_skew + guardband;
final uncertainty = jitter only. If initial was 250 ps and final is 80 ps, the design gains 170 ps of
slack at signoff — but if the design barely closed under the optimistic final constraints, any
process variation at silicon will cause failures. Carry a guardband through to signoff. Never relax
all the way to zero margin." ✅ arithmetic consistent (250 − 80 = 170).

**Third failure mode only yuanbao names.** "Relaxing uncertainty but forgetting to switch from ideal
to propagated clocks, or forgetting to enable OCV/AOCV/POCV derating — STA reports artificially rosy
slack." That is a relaxation that removes margin *twice* without anyone noticing.

---

## Pattern 8 — Clock uncertainty composition (jitter + skew)

`models: deepseek, gemini, grok, meta` (4) · `confidence 0.88–0.95`

**gemini's worked example (✅ closes).** T = 1.0 ns. Pre-CTS: skew 50 + jitter 30 + SI 40 = 120 ps.
Post-CTS with measured skew 42 ps: drop the skew term (now real in the propagated clock) → 30 + 40 =
70 ps. Post-route with SI extraction on: → 30 ps jitter only. Each stage removes exactly the term
that has become real. This is the cleanest derivation in the entire G corpus.

**deepseek's example (⚠ partial).** "50 ps rms jitter → pk-pk = 6σ = 300 ps" ✅; "setup uncertainty
= 300 + 80 = 380 ps" ✅. But the hold half is muddled — "hold uncertainty = −(jitter + skew)…
often set `-hold 50 ps`… but actually we can set negative for hold if the tool doesn't handle
jitter" — three incompatible statements in one field. And 380 ps of uncertainty is very large in
absolute terms; no period is given, so closure cannot be checked.

**The correct principle, stated by grok.** "For setup use the full sum; for hold use a smaller
subset (often only local OCV + small margin) **because global jitter is common-mode**." That single
clause is the reason deepseek's negative-hold-uncertainty confusion arises, and it resolves it.

**wrong_way (grok).** "Using a single flat 100 ps for every clock regardless of period or PLL
quality, or forgetting to reduce uncertainty for hold analysis; hold becomes artificially hard or
setup is under-protected."

---

## Pattern 9 — Mode-dependent / multi-mode constraint derivation

`models: chatgpt, mistral` (2) · `confidence 0.90–0.97`

**Derivation (chatgpt, correct and the best-reasoned draft in the corpus).** Enumerate legal modes
first; for each, derive active clocks, generated-clock relationships, case assumptions, IO budgets
and exceptions from the actual configuration. "A path should be excluded only when the mode
configuration makes it impossible; if two clocks are mutually exclusive, constrain that exclusivity
rather than declaring all paths between their domains universally false. **The final MMMC constraint
set is the union of these mode-specific legal timing relationships, not the intersection of every
possible clock relationship.**"

**wrong_way (chatgpt).** "Writing one broad false path that covers all modes because two clocks are
asynchronous in one configuration can disable real timing checks in another configuration."

**mistral's version uses invented syntax (❌).** `set_max_delay -from A -to B 3.0 -case 010` and
`set_clock_uncertainty -setup 0.05 -case 010`. There is no `-case` option on those commands; modes
are handled by separate constraint sets / MMMC views, not a per-command switch. The *idea* is right;
the commands would not run.

---

## Pattern 10 — Point-to-point max/min delay for non-clocked interfaces

`models: grok` (1) · `confidence 0.84` · **singleton worth keeping**

`set_max_delay` / `set_min_delay` from launch pins to capture pins, where
`budget = required external window − external setup/hold − board delay`. "The max_delay forces the
tool to keep the path short; the min_delay prevents it from becoming so short that external hold is
violated." wrong_way: "relying only on a false_path (tool does nothing) or on a clocked IO delay
that does not match the actual external strobe timing."

Kept because it is the only pattern addressing interfaces with no usable clock reference at all, and
because its `signoff_risk` enumerates all four failure directions (max too tight/too loose, min too
large/missing) rather than the usual two.

---

## Pattern 11 — Source-synchronous / forwarded-clock interface budgeting

`models: gemini` (1, with partial support from yuanbao's DDR notes) · `confidence 0.96`

Distinct from pattern 5 because internal clock-tree latency **cancels at the receiver** when the
clock is forwarded alongside the data — so constraining to the internal clock forces P&R to remove a
skew that would have cancelled anyway. gemini's `wrong_way` states this precisely and it is the only
draft in the corpus that identifies a case where over-constraining is wrong *for a structural
reason* rather than a budget reason.

yuanbao supplies the complementary detail set: source-synchronous input
`-max = Tco_max + board_trace_max − board_clock_trace_min` (and the mirrored `-min`); DDR needs both
edges (`-clock_fall -add_delay`); "forgetting `-add_delay` on DDR interfaces: the second constraint
**overrides** the first, leaving one edge unconstrained." That override behaviour is a silent
failure and appears nowhere else in the corpus.

---

## Pattern 12 — Clock-network latency inclusion/exclusion

`models: mistral` (1) · `confidence 0.97` · **flagged: syntax and reasoning both suspect**

The pattern names a real question (when does clock network latency enter the check) but states it
with commands that do not exist (`set_clock_network_latency -max -include`) and a claim that is only
half true ("clock latency does not affect hold because it cancels out in the hold check formula" —
it cancels only over the *common* portion of the two clock paths, which is what CRPR exists to
credit). **Recorded, not recommended.** Kept in the list because the underlying question — ideal vs
propagated clocks and what CRPR credits — is real and unaddressed by any other draft.

---

## Pattern 13 — Reset and static-configuration false paths

`models: yuanbao` (1) · `confidence 0.80` · **singleton, high practical value**

The only draft that treats false-path *scoping* as the skill: "scope the false path as narrowly as
possible — for a scan enable mux, false-path only through the select pin, not through the entire
mux, so data paths that mux between functional and scan sources remain timed." Pairs it with the
distinction nobody else draws: "**false path removes the timing check; `set_case_analysis` removes a
logic state from analysis.** Use both where appropriate."

wrong_way covers three real errors: wildcard `set_false_path -from [get_cells *]`; false-pathing a
reset that is synchronous in some modes ("the reset deassertion timing matters"); and false-pathing
scan paths in the functional SDC while forgetting to re-enable them in the DFT SDC. Its closing
observation is the sort of thing only practice teaches: "after an ECO, stale false paths are a
notorious source of escaped bugs."

---

## Cross-pattern observations

1. **Convergence is high and that is a warning, not a comfort.** 88 drafts → 13 patterns, with 5
   patterns claimed by all 10 models in near-identical structure. That distribution looks like
   shared textbook provenance rather than independent knowledge. The differentiated material is
   almost entirely in the *singletons* (patterns 10–13) and in the `wrong_way` fields, not in the
   derivations.
2. **The `wrong_way` and `signoff_risk` fields are worth more than the derivations.** The
   derivations are recoverable from any STA reference; the failure narratives — override-not-error
   on DDR `-add_delay`, leakage from unsized false-pathed cells, stale false paths after ECO,
   skew-group vs clock-group confusion — are the parts that read like experience.
3. **Arithmetic error rate: 4 hard errors (❌) and 3 partials (⚠) across the ~25 drafts that carry
   worked numbers**, i.e. roughly one in four numeric derivations does not survive recomputation:
   deepseek's inverted I/O delays, minimax 2.7's off-by-one multicycle, gemini's swapped port
   assignment, meta's formula-vs-example contradiction, mistral's internal-setup-in-external-budget
   and invented `-case` syntax, gemini's DDR sign. **None of these was caught by the models' own
   confidence fields** — the erroneous drafts self-rated 0.85–0.98, the same band as the correct
   ones. Confidence in this corpus predicts fluency, not correctness.
4. **`set_multicycle_path` hold pairing is the single most repeated substantive claim** (7 models,
   independently phrased, with three different explanations of *why* N−1). If any one thing in this
   file is safe to treat as consensus practice, it is that — and it is still worth Alice's
   confirmation for the opposite-edge case, which two drafts flag as an exception and none resolves.

`TODO(alice): review — priority order is pattern 7 (period-squeeze vs uncertainty), pattern 4
(max_delay on CDC), pattern 1 (the -min omission), then the rest.`
