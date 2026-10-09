# RUNSHEET-34 — 34 red-team paste blocks (re-rendered 2026-09-08 for JI-v1)

**Loop:** paste ONE block together with the text of `prompts/J-ISSUE-REDTEAM-V1.md` into the free
AI; record the verdict in `TALLY-34.md`. Paste the prompt down to (not including) the `---` rule —
everything below that rule is a BUILD NOTE and is not part of the paste.

Blocks render extraction-file objects **VERBATIM** (no rewording, no enrichment). Sources:
`extractions/issue-episodes.json` and `extractions/issue-episodes-batch2.json`.

**Why this file was re-rendered.** It previously paired these blocks with
`prompts/J-EPISODE-REDTEAM-V2.md`, whose schema was verified against the five *paper*-episode
files only. All 34 blocks here are *issue* episodes: they carry
`prior_state`/`observation`/`hypothesis`/`candidates_considered`/`chosen_intervention`/`post_state`
and have no `decision`, `alternatives_or_rejected`, `rationale` or `outcome`. J-v2 asks the reviewer
to attack the decision DIRECTION and to judge a quote against a recalled paper, so on every one of
these blocks both of its pre-screens collapsed to its own `cannot-judge-without-the-paper` escape.
JI-v1 replaces those with `mechanism_check` / `evidence_check` / `attribution_check`, which are
answerable from the pasted record alone. See `SESSION-MEMORIAL-2026-09-08-REDTEAM.md` §1.

**Operator notes — not part of any paste:**
- The old per-block `*Schema note:*` footnotes are gone. They flagged these objects as deviating
  from the 9-key paper schema; under JI-v1 this shape IS the expected shape, and leaving the note in
  told the reviewer their input was malformed.
- **Blocks 04, 05 and 06 carry no `direct_quote` and no `section_or_page_locator`.** That is a real
  property of those records, not a rendering fault. It is deliberately NOT flagged in the block —
  detecting it is what `attribution_check` is for. The prompt's field-level escape
  (`not-determinable-from-this-record`) is the correct answer there.
- Every block is a GitHub issue thread: 31 in `The-OpenROAD-Project/OpenROAD`, 1 in
  `The-OpenROAD-Project/OpenROAD-flow-scripts`, 2 in `librelane/librelane`.
- Block 01 is the exemplar baked into JI-v1 itself. Running it is a **calibration check**, not new
  evidence: the prompt's BUILD NOTE states the expected shape of a competent review (unmeasured
  `post_state` under `evidence_check`, plus the #5971 deferral). A model that returns bare SOUND on
  Block 01 is miscalibrated and its other 33 verdicts should be read with that in mind.

## Block 01 — BoomTile/Megaboom: 20k routing congestion DRCs at only 0.24 placement density [issue-episodes.json]

RECORD: OpenROAD issue #6066, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "title": "BoomTile/Megaboom: 20k routing congestion DRCs at only 0.24 placement density",
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6066",
  "prior_state": "BoomTile (Megaboom-derived) design in asap7, ORFS v3.0-1735-gdefc349e. Placement density was only 0.24 with a lot of open space, especially at the top of the die, yet the design failed GRT.",
  "observation": "20k routing congestion DRCs while placement density is only 0.24. Congestion heatmap shows a large region at the top of the die and around the macro. Reported via `run-me-BoomTile-asap7-base.sh gui`.",
  "hypothesis": "The GRT routing-layer adjustment of 0.45 (originally derived from other asap7 designs) is too aggressive for this design; the default 30 congestion iterations were also insufficient. A separate suspected cause named in the thread is a global-route path 'looping around the macro' many times (tracked separately in issue #5971).",
  "candidates_considered": "Increasing the number of overflow/congestion iterations (asked early on and swept, default 30); changing the routing layer adjustment from 0.45 to 0.2; increasing congestion iteration count to 35; macro-placement improvements (issue #5971).",
  "chosen_intervention": "Per eder-matheus (MEMBER): 'we could finish GRT by changing the routing layer adjustments from 0.45 to 0.2... We also changed the number of congestion iterations to 35 to complete BoomTile.'",
  "post_state": "GRT was reported to complete ('could finish GRT', 'complete BoomTile') after reducing the layer adjustment to 0.2 and setting congestion iterations to 35. No re-measured DRC count was given.",
  "gaps": [
    "No measured post-fix DRC count or runtime is reported.",
    "The issue was closed automatically as not_planned/Stale in 2026; whether the reported parameter change was actually merged as a code change is not stated.",
    "No PR link for the fix. The macro-loop root cause is deferred to #5971 and was not resolved here.",
    "We (eder-matheus) note the layer-adjustment is documented at set-global-routing-layer-adjustment; exact meaning of a high vs low value only explained in prose."
  ],
  "confidence": 0.8,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6066",
  "source_type": "github-issue",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6066",
  "direct_quote": {
    "text": "we could finish GRT by changing the routing layer adjustments from 0.45 to 0.2.",
    "by": "eder-matheus",
    "date": "2024-11-14",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6066"
  }
}
```


## Block 02 — GPL-0314: getFillerGCell index out of bounds during global placement [issue-episodes.json]

RECORD: OpenROAD issue #8422, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "title": "GPL-0314: getFillerGCell index out of bounds during global placement",
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/8422",
  "prior_state": "Design (via LibreLane/librelane-tree, GF180, wbqspiflash) at the OpenROAD ioplacement stage on OpenROAD v2.0-24788-g6524d9a82d. Placement: global_placement -density 0.6 -timing_driven -routability_driven; 2675 instances (2003 movable, 672 fixed), 51.6% utilization.",
  "observation": "During nesterov global placement the run aborts with '[ERROR GPL-0314] getFillerGCell: index 282 out of bounds (fillerStor_.size() = 265)'. Immediately before, GPL removed fillers (count 341 → 265, -22.29%; area -22.39%) during the routability-driven iteration.",
  "hypothesis": "The routability-aware placement removes fillers, and afterwards a GCell/Filler index (282) is queried against a filler store that has shrunk to 265 — an internal size/index mismatch. The reporter frames it as 'the error should be actionable' when the design is unusual.",
  "candidates_considered": "No explicit alternative fixes are discussed; the thread treats it as a code defect (assignee gudeh) and the reporter only demands a non-crashing, actionable diagnostic. Netlist/route congestion is nominal (top 0.5% congestion 1.2270).",
  "chosen_intervention": "Not stated in the thread at fix level — gudeh replied 'It has been solved on the latest version. Please let us know if you see it solved on your end.' and the reporter confirmed 'Confirmed resolved.' No code change, PR, or root-cause is described.",
  "post_state": "Reporter confirms the ODB-1200-free run on the latest build and closed as completed. No numeric result is given.",
  "gaps": [
    "The actual code fix / owning commit / PR is not named in the thread — only 'solved on the latest version'.",
    "No repro-verification metrics, no test added, no explanation of the fillerStore/GCell mismatch resolution.",
    "No QoR numbers before/after."
  ],
  "confidence": 0.5,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/8422",
  "source_type": "github-issue",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/8422",
  "direct_quote": {
    "text": "It has been solved on the latest version.",
    "by": "gudeh",
    "date": "2025-09-29",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/8422"
  }
}
```


## Block 03 — RUDY and global-route congestion maps disagree for ICCAD04 risc2 testcase [issue-episodes.json]

RECORD: OpenROAD issue #5300, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "title": "RUDY and global-route congestion maps disagree for ICCAD04 risc2 testcase",
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/5300",
  "prior_state": "ICCAD04 'risc2' testcase (lef/risc2.lef.gz, def/risc2.def.gz), 6-layer, ~90%+ placement density (global_placement -density 0.95), large RAMs with OBS blocking M1–M5 (only M6 free over them), RING/PLACED macros. No init_floorplan centering done.",
  "observation": "The RUDY congestion heatmap looks routable but differs sharply from the global-route heatmap; GRT-0118/GRT-0232 'Routing congestion too high'. GRT report shows metal1 usage 1043.75%, total 194.23%, total overflow 180004, and detailed placement failed on 62 instances (DPL-0036). GRT finished 'with overflow' (GRT-0115).",
  "hypothesis": "A mismatch in how RUDY (usage of 'available' routing resources) vs GRT (usage of total resources) computes congestion; the large RAMs blocking M1–M5 leave only M6 available so GRT inflates red even when those layers are sparse; bad/neighboring macro placement (no halos, FIXED macros with pins down); the design's ~90% density making it effectively unroutable.",
  "candidates_considered": "Make RUDY display available-vs-total routing resources consistently with GRT; fix macro placement (use halos, flip macros so pins face out); change RAM CLASS from RING to BLOCK; fix macros to original placement; move metal2 pins to metal4 for pin access; reduce density/larger die; expose GPL's own congestion model; increase macro-OBS violation cost for groute.",
  "chosen_intervention": "No single code intervention was adopted in this thread. After extensive investigation the thread concludes the design is ~>90% utilized (a bogus/unroutable def), the GRT congestion model and macro placement are wrong, and the groute map is 'completely wrong'. The reporter closed the issue without a code fix being described.",
  "post_state": "The thread ends in diagnosis/negation rather than an outcome: reporter states 'So groute map is wrong, without macros this should be easily routable.' No post-fix metric or merged change is given.",
  "gaps": [
    "No code fix, PR, or commit is referenced — the 'fix' never materializes in the thread.",
    "No post-fix DRC/runtime numbers.",
    "The RUDY-vs-GRT discrepancy is never conclusively attributed to a single code root cause in the thread; hypotheses (available-vs-total resources, macro OBS, density) remain open.",
    "Whether the closing was via a resolve or just the author's conclusion is not stated."
  ],
  "confidence": 0.55,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/5300",
  "source_type": "github-issue",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/5300",
  "direct_quote": {
    "text": "This design has 90+% placement density so it seems unlikely it was ever routable.",
    "by": "maliberty",
    "date": "2024-06-27",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/5300"
  }
}
```


## Block 04 — GRT DRC-error cap (10000) hides congestion hotspots and macro-overlap errors [issue-episodes.json]

RECORD: OpenROAD issue #6386, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "title": "GRT DRC-error cap (10000) hides congestion hotspots and macro-overlap errors",
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6386",
  "prior_state": "Global routing on MegaBoom, with macros placed in very slight overlap (intended abutment). GRT reports DRC errors that are capped at 10000 and viewed in the GUI.",
  "observation": "In a MegaBoom DRC blob, the global-routing DRC failures stop at a vertical line; reporter suspects this is the 10000 cap — though the placement heatmap has a similar vertical line. Separately, in a macro-overlap case the first 10000 errors did NOT include the macro-overlap errors until deltaDebug.py whittled the problem down.",
  "hypothesis": "The 10000 cap returns only the first 10000 errors (in some order), misleading the user into thinking the problem is localized to one region; errors in macro-overlap / hard-to-fix areas fall outside the reported window until the design is reduced. The vertical-line stop was thought to be the cutoff (but the placement map shows an analogous line).",
  "candidates_considered": "Ideally limit at the '10000 most interesting' errors; in lieu of that, cap at 10000 random DRC errors to give an overall impression of where the problem is; the reporter notes some DRC errors are unfixable / tied to impossible problems.",
  "chosen_intervention": "Not stated in the thread — the issue was closed as completed with 0 comments; no maintainer reply describes an implemented change.",
  "post_state": "Only the issue was closed; no confirmation that random-sampling or 'most-interesting' selection was implemented, and no metric is reported.",
  "gaps": [
    "No fix, PR, or commit is mentioned; whether the random-cap behavior was actually implemented is unknown.",
    "No before/after DRC-report behavior measurement.",
    "The relationship between the vertical line and the true congestion is left ambiguous in the thread."
  ],
  "confidence": 0.4,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6386",
  "source_type": "github-issue"
}
```


## Block 05 — repair_timing ODB-1200 with Liberty flip-flops defining Q→QN output-to-output arcs [issue-episodes.json]

RECORD: OpenROAD issue #10994, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "title": "repair_timing ODB-1200 with Liberty flip-flops defining Q→QN output-to-output arcs",
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/10994",
  "prior_state": "RV32I core mapped to OSU GF180 library (gf180mcu_osu_sc_gp12t3v3), SiliconCompiler flow doing CTS.repair_timing on OpenROAD 26Q2 commit 553ed63bc9. Three flip-flop cells define a combinational 'related_pin: QN' Q→QN timing group.",
  "observation": "Hold repair aborts with '[ERROR ODB-1200] InsertBufferBeforeLoads: Load pin dp_pcreg_q_reg_24_/Q is not connected to net n4128'. OpenSTA emitted '[WARNING STA-1212] timing group from output port' at three Liberty lines. 280 endpoints had hold violations (WNS -3.347, TNS -220.074) before the crash.",
  "hypothesis": "The Q→QN combinational timing group makes the timing graph treat Q as a load of QN during buffer insertion, so the resizer tries to insert a buffer 'before' an output pin, then fails the isolation check. Removing the three arcs makes the full flow complete cleanly, isolating the cause.",
  "candidates_considered": "Handle (or cleanly ignore) output-to-output arcs in the timing graph so repair_timing can insert buffers; reject such library data up front with an actionable message instead of a fatal internal error; or strip the arcs (reporter's manual repro isolation).",
  "chosen_intervention": "Reporter confirms it is fixed in current master: commit 069d43dcb9 ('syn: Fix assertion failure on output->output edges') — old code asserted a timing arc's source must be an input pin; the fix explicitly tolerates output-to-output edges. Rebuilt on 26Q3-904-geaaa6e36cb (built 2026-07-30) and re-ran the testcase.",
  "post_state": "repair_timing completes without the ODB-1200 error, and the full RTL-to-GDS flow now runs to completion with the completely unmodified Liberty. The Q→QN arcs remain and still produce the benign STA-1212 parsing warnings.",
  "gaps": [
    "The commit attribution (069d43dcb9) is the reporter's inference from history, not a bisect — the reporter explicitly says 'I haven't bisected to confirm'.",
    "No regression test is named, and no slack/area/timing QoR delta is reported.",
    "The maintainer (jhkim-pii) initially could not reproduce on latest; the resolution was confirmed largely by the reporter's retest."
  ],
  "confidence": 0.85,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/10994",
  "source_type": "github-issue"
}
```


## Block 06 — TritonCTS segfault in getBufferFanoutLimit when Liberty has no max_capacitance/max_transit [issue-episodes.json]

RECORD: OpenROAD issue #11165, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "title": "TritonCTS segfault in getBufferFanoutLimit when Liberty has no max_capacitance/max_transition",
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/11165",
  "prior_state": "IHP SG13G2 thick-oxide stdcell lib from IHP-Open-PDK PR #1103 first revision (CharLib liberty with no max_capacitance/max_transition anywhere), standalone mini.def with two flops on one clock; OpenROAD 26Q1-1024-gdcf36133a. clock_tree_synthesis run with explicit -buf_list.",
  "observation": "clock_tree_synthesis segfaults (SIGSEGV, null deref) in cts::TritonCTS::getBufferFanoutLimit() called from TritonCTS::setupCharacterization() (frames 2-4). Control: swapping to the same file with per-pin max_capacitance/max_transition + default_max_* makes the identical script finish without crashing.",
  "hypothesis": "getBufferFanoutLimit consults max-cap/fanout data of the selected buffer; with a liberty carrying none, a lookup returns null/empty and is dereferenced. (Reported as a reading of the backtrace, not an inspection of source.)",
  "candidates_considered": "Emit a diagnosable error ('liberty has no drive limits, cannot characterize buffers') and nonzero exit instead of segfault; add per-pin limits to the liberty (A/B-verified trigger); avoid -buf_list inference was ruled out since buffers were explicit.",
  "chosen_intervention": "Not stated in the thread — maintainer arthurjolo replied 'We actually check if the max fanout exists so the fact that there is none in the liberty should not give a crash. I am looking at the crash.' No fix/PR/commit is given.",
  "post_state": "Only diagnosis+repro, no confirmed resolution in the thread; the expected behavior (actionable error) was not yet delivered as far as the thread shows.",
  "gaps": [
    "No code change, PR, or commit is referenced; the fix was still in progress ('I am looking at the crash') at the last comment.",
    "No post-fix verification or test added.",
    "The 'likely cause' is inferred from the stack backtrace, not from source reading."
  ],
  "confidence": 0.75,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/11165",
  "source_type": "github-issue"
}
```


## Block 07 — CTS NDRs on heavily gated clocks cause routing congestion (level definition + GRT/DRT mism [issue-episodes.json]

RECORD: OpenROAD issue #8579, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "title": "CTS NDRs on heavily gated clocks cause routing congestion (level definition + GRT/DRT mismatch)",
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/8579",
  "prior_state": "Designs with many gated clocks (mempool_group, ca53, ibex) where NDRs (2s1w) are applied to clock nets on the first half of the clock tree levels, ignoring leaves. CTS considers every gated clock a separate builder so each gated clock root is 'level 0'.",
  "observation": "Routing congestion where many clock-gate (CG) cells concentrate; congestion happens on the upper metal layers reserved for clock nets (except leaf nets). GRT is 'overly cautious, overestimating the net edge cost', making NDR routing harder; high overflow counts cause timeout. A 'soft NDR' (disable NDR during GRT) was prototyped.",
  "hypothesis": "Defining clock-tree 'level' per gated-clock builder resets the depth at every CG, so NDRs pile up in CG-dense regions; plus a GRT-vs-DRT behavior mismatch (DRT tapers near pins but GRT does not model that, overestimating cost); plus GPL is unaware of NDRs.",
  "candidates_considered": "Define 'level'/depth from the root uniformly regardless of whether a node is a CG or buffer; apply root-only NDR for gated clocks; the 'soft NDR' that disables NDR only during GRT; make GRT reflect DRT tapering; make GPL NDR-aware.",
  "chosen_intervention": "jfgava: 'Fixed in #11136'. The specific change (which of the above) is not detailed in this thread.",
  "post_state": "Closed as completed via the referenced fix; no post-fix timing/congestion/(skew/skew) numbers are reported here.",
  "gaps": [
    "The content of PR #11136 (which candidate was implemented) and whether it changed level definition vs GRT behavior is not stated in this thread.",
    "No post-fix QoR (skew, congestion, runtime) is reported.",
    "The outcome of jfgava's planned tests ('I will do some tests') is not shown here."
  ],
  "confidence": 0.6,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/8579",
  "source_type": "github-issue",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/8579",
  "direct_quote": {
    "text": "Fixed in #11136",
    "by": "jfgava",
    "date": "2026-08-19",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/8579"
  }
}
```


## Block 08 — asap7 cva6 hierarchical-synth GRT congestion report references a nonexistent net [issue-episodes.json]

RECORD: OpenROAD-flow-scripts issue #3245, The-OpenROAD-Project/OpenROAD-flow-scripts (GitHub issue thread).

```json
{
  "title": "asap7 cva6 hierarchical-synth GRT congestion report references a nonexistent net",
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/issues/3245",
  "prior_state": "asap7 cva6 hierarchical-synthesis run via OpenROAD-flow-scripts (commit 7cadc3e9; branch 8227b4909, PR #3244). GRT run in incremental mode with -congestion_report_file after a large repair_timing (2375 setup-violation endpoints).",
  "observation": "GRT fails with a single congestion issue (GRT-0232 / GRT-0116 'Routing congestion too high'); the congestion report/DRC-viewer marker references a net that does not exist in the netlist, and the marker sits where RUDY says the area is not congested. repair_timing logs show very many inserted and removed buffers.",
  "hypothesis": "povik: 'This has all the signs of an issue with handling of merged nets in incremental groute.' eder-matheus: 'The net that doesn't exist in ODB is probably a net that was merged with another during repair_timing, and we didn't update the congestion heatmap with it.'",
  "candidates_considered": "Fix merged-net handling in incremental groute; update/refresh the congestion report when a net is deleted so stale markers are not shown; align GRT with RUDY.",
  "chosen_intervention": "eder-matheus: 'PR https://github.com/The-OpenROAD-Project/OpenROAD/pull/7650 fixes the congestion issue you see.' Plus a follow-up: 'I'll work on update the congestion report when a net is deleted, but you should not see these small congestion errors anymore.'",
  "post_state": "jeffng-or (reporter) closed with 'sounds like it was resolved.' No numeric post-fix result is given.",
  "gaps": [
    "The specifics of PR #7650 and whether it changed net merging, the report, or both, are not elaborated in this thread.",
    "No post-fix DRC/runtime/overflow metric is reported.",
    "Whether the 'update congestion report when a net is deleted' follow-up actually landed is not confirmed here."
  ],
  "confidence": 0.8,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/issues/3245",
  "source_type": "github-issue",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/issues/3245",
  "direct_quote": {
    "text": "PR https://github.com/The-OpenROAD-Project/OpenROAD/pull/7650 fixes the congestion issue you see.",
    "by": "eder-matheus",
    "date": "2025-06-25",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/issues/3245"
  }
}
```


## Block 09 — STA: false hold/setup violations in floorplan from ideal top-level clock mixed with propag [issue-episodes-batch2.json]

RECORD: OpenROAD issue #6181, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "title": "STA: false hold/setup violations in floorplan from ideal top-level clock mixed with propagated-clock macro timing models",
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6181",
  "prior_state": "megaboom (asap7, ORFS) in floorplan timing repair, before CTS: top-level clock is ideal (0 latency), but hard macros carry non-trivial internal clock insertion latency in their Liberty timing models. megaboom uses HOLD_SLACK_MARGIN=-300. OpenROAD ~v2.0-17100-era (issue opened 2024-11-18).",
  "observation": "Floorplan hold repair gnaws on violations that do not exist post-CTS: '[INFO RSZ-0046] Found 2048 endpoints with hold violations' in the mock-array repro, consuming very long runtimes; reporter also exhibits a believed-false setup violation ('156.17 156.17 ^ ces_0_4/io_lsbOuts_3' including ca. 70ps of macro clock insertion delay).",
  "hypothesis": "parallaxsw (OpenSTA): 'If the timing model is generated with propagated clocks, the timing model setup/hold times will include the clock network delays. If the model is then used in a context with ideal clocks, the setup/hold times will be incorrect' — the model bakes macro-internal clock-tree delay into setup/hold requirements that are wrong for an ideal-clock context, and Liberty min/max_clock_tree_path cannot reverse it per-path.",
  "candidates_considered": "Turn off hold fixing in floorplan entirely (maliberty's initial plan — leaves false setup risk); turn off clock propagation until after CTS (tspyrou); generate two Liberty models per macro, one for ideal-clock contexts (parallaxsw — rejected as impractical for third-party IP, though precisionmoon noted third-party .lib can be edited); negative HOLD_SLACK_MARGIN sized below -max(macro insertion latency) (oharboe workaround); negative hold clock-uncertainty (precisionmoon).",
  "chosen_intervention": "jjcherry56's OpenSTA change (commit a82361ce, 'timing models rm clk tree delay clk->output w/ideal clk conttext' [sic]): OpenSTA now removes the liberty min/max_clock_tree_path delays from macro-model setup/hold times and clock-to-output delays when the context uses ideal clocks. Rolled into OpenROAD via the sta submodule update (eder-matheus merged 'the latest STA changes', 2025-01-21).",
  "post_state": "Reporter re-ran the mock-array repro with a82361ce: 'As expected, there are now no false timing violations to be repaired'. Companion ORFS PR #2615 fleshed out SETUP/HOLD_SLACK_MARGIN documentation.",
  "gaps": [
    "No quantified QoR/runtime delta (before/after) is reported; the confirmation is the reporter's re-run of mock-array, not a megaboom retest.",
    "jjcherry56 notes the fix 'will not be exactly the same as using a separate model built with ideal clocks but it should eliminate the bulk of the differences' — residual error unquantified."
  ],
  "confidence": 0.85,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6181",
  "source_type": "github-issue",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6181",
  "direct_quote": {
    "text": "If the timing model is generated with propagated clocks, the timing\r\nmodel setup/hold times will include the clock network delays. If the\r\nmodel is then used in a context with ideal clocks, the setup/hold\r\ntimes will be incorrect because they include clock network delays\r\ninside the macro.",
    "by": "parallaxsw",
    "date": "2024-11-29",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6181"
  }
}
```


## Block 10 — GPL regression: too-early non-virtual timing-driven iteration makes previously-working des [issue-episodes-batch2.json]

RECORD: OpenROAD issue #7581, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "title": "GPL regression: too-early non-virtual timing-driven iteration makes previously-working design unroutable",
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/7581",
  "prior_state": "dynamic_node design (sky130hd, SiliconCompiler flow) previously routed cleanly; regression window between commits 4b729ea and 6e29df07 (v2.0-22186), after 588bc37.",
  "observation": "Global route now fails on congestion after placement. povik's log diff: first routability-driven iteration spikes target density to 0.9584 (vs 0.6136 in the good run), final densities 0.84 vs 0.69, and the first routability iteration inflates area ~76% (good run: 13 iterations at ~1% each). Design starts at only ~70% initial overflow (ORFS designs usually ~100%).",
  "hypothesis": "Instances named 'placeXX' traced to PR #7485 (povik's resizer-in-gpl change). povik: 'the issue originates in global placement with a non-virtual TD iteration running too early' — buffer insertion at high overflow warps the placement; gudeh additionally showed the CG initial placement and nesterov disagree under timing-driven, and that making the first two TD iterations virtual prevents the twisting while TD weights alone (set to 1.0) do not.",
  "candidates_considered": "skip_initial_place (gadfort: 'even with skip-initial-place the design is not routable'); TD max weight 1.0 (gudeh: no effect); -keep_resize_below_overflow 0.0 / 0.30 (povik's per-design workarounds); disable timing-driven entirely (gadfort's reluctant fallback); PR #7711 (povik's fix pass) — improved but 1 of 3 designs still failed on the GPL iteration cap.",
  "chosen_intervention": "Two-part: PR #7711 (timing-driven placement fix), plus raising the effective GPL iteration budget for routability reverts — maliberty's ruling (2025-07-08): 'Increasing the limit by the number of reverted iterations make[s] sense. We should still have some overall cap to prevent endless reverting but it could be a lot higher.' gudeh implemented the new stop criteria and re-ran.",
  "post_state": "gudeh 2025-07-10: 'Finished as expected' (design completed after 30 routability iterations, hitting the then-5000 GPL iteration cap without failing); gadfort confirmed 2025-07-31: 'Works now. Thanks'.",
  "gaps": [
    "The stop-criteria change's own PR number is not cited in-thread (the decision and test evidence are).",
    "No before/after congestion or wirelength table for the final state; the secondary RSZ-2005 'cannot find a viable buffering solution' warning observed mid-thread was explained (ERC/max-fanout constraints) but not tied to this failure."
  ],
  "confidence": 0.8,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/7581",
  "source_type": "github-issue",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/7581",
  "direct_quote": {
    "text": "Based on the findings I believe the issue originates in global placement with a non-virtual TD iteration running too early.",
    "by": "povik",
    "date": "2025-06-27",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/7581"
  }
}
```


## Block 11 — GPL: RePlAce divergence (GPL-0307) on megaboom — snapshot-delivery mitigation while root c [issue-episodes-batch2.json]

RECORD: OpenROAD issue #6465, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "title": "GPL: RePlAce divergence (GPL-0307) on megaboom — snapshot-delivery mitigation while root cause stays open",
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6465",
  "prior_state": "megaboom placement on OpenROAD v2.0-17966; previously working; PLACE_DENSITY is swept with no effect. Divergence on stage 3-1 (skip-io) around iteration 500.",
  "observation": "'[ERROR GPL-0307] RePlAce divergence detected. Re-run with a smaller max_phi_cof value.' aborts placement. Independently corroborated by mikesinouye on two private-PDK designs (3.7M and 4.6M instances, one macro-less, Dec-11 build) with large area swings from the recently-enabled in-gpl resizer ('Timing-driven: RSZ delta area: 171131.8' followed by overlap regression).",
  "hypothesis": "gudeh: evidence points to blockage handling — gpl represents blockages as fixed dummy cells and has limited ability to move cells out; a bivariate-normal macro adjustment was reduced in PR #6438 without effect; macros eliminated as trigger when the delta-debugged testcase diverges with no macros ('a good elimination of a false track' — maliberty) though blockages remain; negative bin sizes suspected (PR #6530 merged to isolate). Root cause never pinned: 'I have spent a good amount of time investigating... I haven't yet pinpointed the exact cause' (gudeh, 2025-02-18).",
  "candidates_considered": "PLACE_DENSITY sweep (failed); increase die/core area (worked — megaboom PR #227); '-overflow 0.25' to converge before the trouble (maliberty, unverified); 10x-5x bin size (converges — 'we use the average area of movable cells divided by the target density as the bin area'); ignore blockages entirely by removing the fixed dummy cells (converges); keep_resize_below_overflow 0 (virtual-only timing-driven); deltaDebug on the testcase (ran days, shrank 68216->67151 instances, impractical).",
  "chosen_intervention": "Mitigation, not cure: gudeh implemented 'revert if diverge' — save a snapshot of the lowest overflow achieved and deliver it instead of erroring. On this artifact megaboom then finished with a plausible placement (overflow trajectory 0.753 -> 0.480 shown at iteration 340-390).",
  "post_state": "megaboom placement completes via snapshot delivery; divergence root cause remains unidentified. Issue stale-closed 2026-06-14.",
  "gaps": [
    "Root cause never identified in-thread; the blockage-dummy-cell hypothesis is unconfirmed.",
    "No PR number cited for the revert-if-diverge feature; no post-fix QoR comparison against a healthy run.",
    "mikesinouye's private-PDK divergence was never reconciled with the megaboom case ('I believe his issue is different')."
  ],
  "confidence": 0.5,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6465",
  "source_type": "github-issue",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6465",
  "direct_quote": {
    "text": "Apologies, everyone. I’ve spent a good amount of time investigating the megaboom divergence issue, but I haven’t yet pinpointed the exact cause.",
    "by": "gudeh",
    "date": "2025-02-18",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6465"
  }
}
```


## Block 12 — Manual macro placement (R90, asap7 M2) leaves pins off routing grid -> DRT-0418/DRT-0073 f [issue-episodes-batch2.json]

RECORD: OpenROAD issue #6267, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "title": "Manual macro placement (R90, asap7 M2) leaves pins off routing grid -> DRT-0418/DRT-0073 failures",
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6267",
  "prior_state": "asap7 mock-array with manual macro placement (RTLMP_FLOW=0); macros placed rotated (e.g. R90). Snapping exists in MacroPlacer2::placeMacro (Snapper::snapMacro) for non-right-angle rotations only.",
  "observation": "Detailed routing fails: '[WARNING DRT-0418] Term ces_6_3/io_ins_right[15] has no pins on routing grid' for many macro pins, then '[ERROR DRT-0073] No access point for ces_7_0/io_ins_left[11]' (and ces_1_0, ces_2_0) aborts 5_2_route.",
  "hypothesis": "joaomai: the unaligned pins are all in M2, and 'the interval between tracks in asap7's M2 layer isn't always the same' (multi-pattern tracks) — the current snapping mechanism cannot align M2 pins with the other layers; maliberty: m2 and m4 both carry LEF58_RIGHTWAYONGRIDONLY, so off-grid pins there are simply unusable ('such pins are unusable').",
  "candidates_considered": "Snapping for manual placement (already present except right-angle rotation — the gap); search farther for a snapping that satisfies M2 + other layers (maliberty's framing of the fix); error in MPL when pins land off-grid on RIGHTWAYONGRIDONLY layers (AcKoucher's proposal); move the DRT error into macro placement for early failure (rejected — running pin_access with unplaced std cells risks false positives).",
  "chosen_intervention": "PR #6507 merged (joaomai, 2025-01-14) — fixes the mock-array case; definitive multi-pattern track-grid snapping approach landed as PR #6738 (AcKoucher, 2025-05-01: 'Definitive approach made in #6738').",
  "post_state": "'make DESIGN_CONFIG=designs/asap7/mock-array/config.mk RTLMP_FLOW=0 nuke final' passes with #6507 per joaomai; #6738 supersedes the quick fix for non-uniform track pitches.",
  "gaps": [
    "The exact mechanism of #6507 vs #6738 (what each changed in the snapper) is not elaborated in-thread.",
    "Final confirmation quoted is the fixer's statement, not the reporter's re-run; no routing QoR numbers."
  ],
  "confidence": 0.75,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6267",
  "source_type": "github-issue",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6267",
  "direct_quote": {
    "text": "It looks like all the pins that are unaligned with the track-grid are in M2. The interval between tracks in asap7's M2 layer isn't always the same, which causes problems when snapping the macros' pins with our current snapping mechanism.",
    "by": "joaomai",
    "date": "2024-12-10",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6267"
  }
}
```


## Block 13 — DRT assert in patchMetalShape_minStep: violation on last metal layer indexes getLayer(lNum [issue-episodes-batch2.json]

RECORD: OpenROAD issue #7684, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "title": "DRT assert in patchMetalShape_minStep: violation on last metal layer indexes getLayer(lNum+1) out of range",
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/7684",
  "prior_state": "Detailed routing of a design whose technology's top routing layer is metal4; flow limits routing via set_routing_layers -signal ... (a GRT command); OpenROAD v2.0-20726.",
  "observation": "Abort during the 0th optimization iteration at 20%: 'vector::_M_range_check: __n (which is 9) >= this->size() (which is 9)'. Localized via gdb 'catch throw' (maliberty's tip) to FlexGCWorker::Impl::patchMetalShape_minStep(): 'tech_->getLayer(lNum + 1)' when the marker is on metal4 — the last metal layer — so lNum+1 does not exist. DRT was routing on metal4 although the user intended it to stop lower.",
  "hypothesis": "Two-layer finding: (1) the patch code assumes a layer above the violation exists; (2) the deeper cause of metal4 routing is that set_routing_layers scopes GRT only — osamahammad21: 'set_routing_layers is actually a grt command... That doesn't enforce any layer range for drt. If you want to limit the detailed router by metal4, you should specify -top_routing_layer argument in the detailed_route command.'",
  "candidates_considered": "Guard the last-layer index (the assert fix); document/require -top_routing_layer for DRT separately (status quo); unify the commands — maliberty: 'we should have the one command control both rather than have two different controls. I can't see when you would want these to differ'; osamahammad21 defended keeping GRT-soft vs DRT-hard distinction; gadfort sided with unification; maliberty's fallback if the flexibility is preserved: make -top/-bottom_routing_layer default to what set_routing_layers used.",
  "chosen_intervention": "PR #7835 merged fixing the assert ('the initial bug fixed by PR #7835 got merged' — titan73 closing); routing-layer command unification spun off to issue #7858 ('let's just have one command to rule both then' — maliberty).",
  "post_state": "Assert gone with #7835; issue closed by reporter 2025-07-21; unification tracked in #7858 (outcome outside this thread).",
  "gaps": [
    "PR #7835's exact code change is not quoted in-thread.",
    "#7858's resolution (single command for GRT+DRT layer ranges) is not recorded here.",
    "A transient 'fixed between v2.0-20726 and commit 29d1f469' observation was retracted by the reporter ('the issue is still here... in next iteration')."
  ],
  "confidence": 0.75,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/7684",
  "source_type": "github-issue",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/7684",
  "direct_quote": {
    "text": "That doesn't enforce any layer range for **drt**(detailed route). If you want to limit the detailed router by metal4, you should specify -top_routing_layer argument in the detailed_route command.",
    "by": "osamahammad21",
    "date": "2025-07-20",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/7684"
  }
}
```


## Block 14 — GRT heap underflow (GRT-0183) after antenna repair — FastRoute resource/NDR initialization [issue-episodes-batch2.json]

RECORD: OpenROAD issue #10273, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "title": "GRT heap underflow (GRT-0183) after antenna repair — FastRoute resource/NDR initialization saga",
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/10273",
  "prior_state": "tiny_rocket on IHP130 sg13g2 (SiliconCompiler flow), OpenROAD 26Q2; global route completes, then repair_antennas runs and re-enters routing.",
  "observation": "'[ERROR GRT-0183] Net _22574_: heap underflow during 3D maze routing' after antenna repair; later variants on other designs finish GRT with overflow without erroring.",
  "hypothesis": "jfgava, staged: first 'incorrect resource initialization when running repair_antennas' (FastRoute uninitialized on re-entry — same root as issue #10156); after the first fix, remaining failures traced to 'a FastRoute 2D-3D limitation' with NDR (non-default rule) nets — NDR costs in integer/float ('Net: clk NDR cost in met1 (float/int): 1.2352941/2') distort 3D resources; requires restructuring how 3D resources are managed during the 2D stage for NDR nets.",
  "candidates_considered": "Initialize routing resources on antenna-repair re-entry (first merged fix); patch NDR cost accounting incrementally (superseded); restructure 3D-resource management for NDR nets in FastRoute (chosen); companion fixes already landed en route: PR #10281 (wrong routing resources), CTS NDR wire-spacing bug fix for sky130 that changed starting conditions.",
  "chosen_intervention": "Series of FastRoute fixes merged into master around 2026-06-04 (commit 9400cb1e named: 'more pessimistic NDR cost during GRT now, but at the same time, the soft-NDR application was enhanced'); final closure by maintainer pointing at PR #11093 ('Fixed on https://github.com/The-OpenROAD-Project/OpenROAD/pull/11093', eder-matheus, 2026-08-13).",
  "post_state": "Original heap-underflow repro passes after the first fix; intermediate overflow reports on gadfort's other designs persisted through several rounds ('It seems like it's still a problem then... In the exact same way unfortunately', 2026-06-05); maintainer-closed as fixed by #11093.",
  "gaps": [
    "The reporter's confirmation after the FINAL fix (#11093) is not in the thread — closure rests on the maintainer's pointer.",
    "Multi-fix attribution: at least three PRs (unnamed first fix, 9400cb1e, #11093) plus CTS interplay; the exact division of labor is not written down.",
    "No NDR-cost or congestion metrics quantifying the 'more pessimistic NDR cost' tradeoff."
  ],
  "confidence": 0.6,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/10273",
  "source_type": "github-issue",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/10273",
  "direct_quote": {
    "text": "Fixes merged into master. Please, let me know if you find any other issues.",
    "by": "jfgava",
    "date": "2026-06-04",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/10273"
  }
}
```


## Block 15 — PDN: negative placement halo mis-applied to obstructions/pins shorts macro rings against c [issue-episodes-batch2.json]

RECORD: OpenROAD issue #2079, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "title": "PDN: negative placement halo mis-applied to obstructions/pins shorts macro rings against core rails",
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/2079",
  "prior_state": "OpenLane-era design (2022) with macro power rings and top-level PDN both using all metal layers; user deliberately sets a negative halo (-11) — the then-only way to let top-level met4 stripes enter the macro and reach its met5 ring when all layers are obstructed.",
  "observation": "met4 short between the macro ring and core rails at the macro's north side ('short around (2200.00000, 132.00000)'; screenshots show met4 shorts at top-left corner across builds 4a99e886 and later).",
  "hypothesis": "gadfort, from one question: 'Is there a reason your halo has negative values for the vertical? i.e. -11 vs 11?' -> 'It's the cause of the shorts... At the moment, the halo is getting incorrectly applied to obstructions and pins and that is the problem.' Negative halo itself remains a legitimate mechanism.",
  "candidates_considered": "Guard against negative halos outright (gadfort's first reflex — risked breaking the documented use pattern the user relies on); fix the halo application to pins/obstructions (chosen); design a proper PDNGEN capability so negative-halo hacks are unnecessary ('It seems like you are hacking your way around a limitation and a better solution would be to figure out what is missing and add that into PDNGEN' — deferred to a different issue, not landed in-thread).",
  "chosen_intervention": "Fix merged as commit cb3acc68084046d5b343da32c7d3ea16a6e82db9 (gadfort, 2022-08-29): 'negative was applied incorrectly, the fix has been merged to OpenROAD... When I run yours, it appears to work.'",
  "post_state": "Maintainer's repro passes post-fix; negative halo reaffirmed as valid ('Negative halo by itself is still a valid parameter for PDNGEN' — confirmed by gadfort). Issue later closed for inactivity ('No activity; please reopen if still relevant').",
  "gaps": [
    "The original reporter's own post-fix confirmation is never recorded in-thread.",
    "The underlying limitation (no first-class way to connect top-level stripes to a fully-obstructed macro's ring) was acknowledged but not fixed here."
  ],
  "confidence": 0.7,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/2079",
  "source_type": "github-issue",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/2079",
  "direct_quote": {
    "text": "Yes, negative was applied incorrectly, the fix has been merged to OpenROAD (https://github.com/The-OpenROAD-Project/OpenROAD/commit/cb3acc68084046d5b343da32c7d3ea16a6e82db9) please try the head of OR.",
    "by": "gadfort",
    "date": "2022-08-29",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/2079"
  }
}
```


## Block 16 — CTS crash (stack overflow in computeSinkArrivalRecur) after clock-gater handling merge d7c [issue-episodes-batch2.json]

RECORD: OpenROAD issue #6318, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "title": "CTS crash (stack overflow in computeSinkArrivalRecur) after clock-gater handling merge d7c5a8ae",
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6318",
  "prior_state": "CTS on a clock-gated design (paths like I_digital_top/.../u_i2c_bus_monitor/stop_o_reg/CP; many 'No paths found for pin' warnings) immediately after merge commit d7c5a8ae (PR #6134, 'Cts enhance clkgater handling', arthurjolo, 2024-11-21). Logs also show surprising zero-size sub-regions ('Sub-region size: 0.0000 X 0.0000' — explained by arthurjolo as expected when a region holds one instance).",
  "observation": "CTS crashes with no backtrace. gdb backtrace supplied by reporter: '#0 cts::TritonCTS::isSink(odb::dbITerm*) #1 cts::TritonCTS::computeSinkArrivalRecur(odb::dbNet*, odb::dbITerm*, float&, unsigned int&, sta::Graph*)' — unbounded recursion.",
  "hypothesis": "maliberty: 'That suggests some sort of loop in the clock tree which sounds odd... We could solve the recursion with a visited set but I'm afraid we might just be hiding some deeper issue.' Reproducibility itself was unstable (reporter first could not reproduce with identical sources and testcase, then could again; testcase delivered via PII sftp under NDA).",
  "candidates_considered": "Visited-set recursion guard (maliberty — feared masking the deeper issue); reproduce-and-debug on the uploaded testcase (chosen path; arthurjolo assigned).",
  "chosen_intervention": "Fix landed by arthurjolo out-of-thread (no commit/PR cited); reporter confirms 2025-04-15: 'Works fine now. Thanks for the fix!'",
  "post_state": "Crash gone on the reporter's testcase.",
  "gaps": [
    "The fixing commit/PR is never identified in the thread — attribution is only 'thanks for the fix' to the assigned maintainer.",
    "Whether the 'deeper issue' (clock-tree loop) was cured or the recursion merely guarded is not recorded.",
    "Flaky reproduction was never explained (reporter suspected environment/dependency differences)."
  ],
  "confidence": 0.55,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6318",
  "source_type": "github-issue",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6318",
  "direct_quote": {
    "text": "We could solve the recursion with a visited set but I'm afraid we might just be hiding some deeper issue.",
    "by": "maliberty",
    "date": "2024-12-16",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6318"
  }
}
```


## Block 17 — CTS design decision: balance macro insertion latency against register paths with delay buf [issue-episodes-batch2.json]

RECORD: OpenROAD issue #3759, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "title": "CTS design decision: balance macro insertion latency against register paths with delay buffers (feature PR #4607/#4678)",
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/3759",
  "prior_state": "Hierarchical flows (asap7 mock-array: Element macros with ~70ps internal insertion delay encoded as Liberty min_clock_tree_path cell_rise 70.88/cell_fall 72.71) build the top-level clock tree ignoring macro-internal latency, 'otherwise, you can end up with a lot of skew'. maliberty framed the two parts in 2023-08: record clock-tree delay in .lib abstracts (Liberty max_clock_tree_path/min_clock_tree_path), then account for it in top-level CTS.",
  "observation": "Measured skew driver: register sinks at ~329.534ps clock arrival vs macro pin arrival 442.233ps (which already includes the Element's ~70.88061ps insertion delay) — visible in the enhanced clock-tree viewer (macro vs register sinks colored differently, PR-delivered mid-investigation).",
  "hypothesis": "precisionmoon (Cho): skew between macro sinks and FF sinks can be reduced by balancing latency — insert additional buffers along clock-buffer-to-FF paths to match macro insertion delay, 'at the expense of area and power', trading insertion-delay-induced skew for latency matching; H-Tree enhanced to pull macros with insertion delays ahead of FF leaves.",
  "candidates_considered": "Balance by delay-buffer insertion with a derate knob (chosen: '-delay_buffer_derate' 1.0 default = all intended buffers, 0.0 = none); report insertion delay in report_clock_skew (landed as part of the OpenSTA enhancement); clock-tree viewer indication of min_clock_tree_path (rovinski's stretch-the-rectangle visual; deferred); do nothing / accept the skew.",
  "chosen_intervention": "Delay-buffer insertion checked in as PR #4607 (2024-02-07): 'if the difference in macro cell latencies and register cell latencies is 50 ps and each delay buffer delay is 10 ps, we need 5 delay buffers'; extended to single-sink macro trees and enabled by default via PR #4678 (2024-02-20) — '-no_insertion_delay' to disable.",
  "post_state": "Feature on by default; issue closed with the PR #4678 merge. mock-array used as the demonstration vehicle throughout.",
  "gaps": [
    "Quantified final skew before/after is shown only as viewer images and a preliminary results table (html) — no numeric skew table in text.",
    "Area/power cost of the inserted delay buffers is not quantified in-thread.",
    "This balances to average latency; per-sink residual skew inside macros is not addressed (adjacent topic of issue #6181's model side)."
  ],
  "confidence": 0.8,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/3759",
  "source_type": "github-issue",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/3759",
  "direct_quote": {
    "text": "Delay buffers are added such that average latencies of all macro cell paths and those of register cell paths can match.",
    "by": "precisionmoon",
    "date": "2024-02-07",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/3759"
  }
}
```


## Block 18 — PDN legality decision: rings outside the die area become an error (with an opt-out), core- [issue-episodes-batch2.json]

RECORD: OpenROAD issue #6445, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "title": "PDN legality decision: rings outside the die area become an error (with an opt-out), core-margin math documented",
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6445",
  "prior_state": "MegaBoom macros (e.g. btb_128x56) using the asap7 BLOCK_grid_strategy.tcl with a tight core margin; die area (0 0)-(47060 25232).",
  "observation": "PDN builds the power ring outside the die: ring area (-72 144)-(47106 25236) — the obstruction covers signal pins, so 'the pins are no longer accessible to the detailed router when we are trying to route BoomTile'. maliberty's arithmetic: the ring stack needs core_offset 0.084 + width 0.12 + spacing 0.072 + width 0.12 = 0.396 of core-to-die space, but the design has only 0.324; most ORFS designs use CORE_MARGIN >= 1-2 and never hit it.",
  "hypothesis": "Behavior was historically tolerated because OpenLane 'was inserting rings outside of the die area and then adjusting their die area' (gadfort); eFabless (donn) confirms they still intentionally generate rings outside the die, but their Magic-generated abstract LEFs 'don't draw obs' over pins so they don't hit the pin-blocking consequence.",
  "candidates_considered": "Silently keep generating out-of-die shapes (status quo — fails BoomTile); error out unconditionally (gadfort's proposal); error with an option to allow eFabless' use case (chosen: maliberty 2025-01-22, 'After discussing with @gadfort it looks like the best is to make it an error with an option to allow for eFabless' use case'); compute per-layer bounds in write_lef_abstract and downgrade to warning (maliberty's alternative, folded into the discussion of obs-over-pin behavior: 'Normally, obstructions block routing, except for when a pin port overlaps an obstruction').",
  "chosen_intervention": "Decision recorded: make out-of-die ring generation an error with an opt-in flag; implementation assigned to gadfort (landing PR not cited in-thread).",
  "post_state": "Decision settled 2025-01-22; issue closed 2025-01-23. The core-margin arithmetic (0.396 needed vs 0.324 present) is the reusable check.",
  "gaps": [
    "The implementing PR/commit and the flag's final name are not in this thread.",
    "No confirmation run of BoomTile post-change."
  ],
  "confidence": 0.65,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6445",
  "source_type": "github-issue",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6445",
  "direct_quote": {
    "text": "After discussing with @gadfort it looks like the best is to make it an error with an option to allow for eFabless' use case.",
    "by": "maliberty",
    "date": "2025-01-22",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6445"
  }
}
```


## Block 19 — repair_timing non-determinism with threads>1: stale driver-vertex level cache invalidated  [issue-episodes-batch2.json]

RECORD: OpenROAD issue #9781, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "title": "repair_timing non-determinism with threads>1: stale driver-vertex level cache invalidated by nothing",
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/9781",
  "prior_state": "gcd nangate45 post-global-route idempotency harness (run twice, hash the ODB) on master 9b0caf1a (2026-03-16); OpenROAD built with OpenMP; test.sh compares run_a/run_b hashes at a given thread count.",
  "observation": "threads=16: 'run_a=f95892c2f56ba174... run_b=6ae767385ecf10b2... NON-DETERMINISTIC' (hashes differ each run); threads=1: hashes always match. precisionmoon isolated the trigger: 'If I limit the transforms to sizing and pin swap only, results are deterministic... When \"buffer\" gets added to the sequence, results get non-deterministic.'",
  "hypothesis": "minjukim55's root cause: 'The Resizer maintained its own driver-vertex level cache (level_drvr_vertices_) that was not invalidated after BufferMove inserted buffers. Subsequent code (e.g. RepairDesign::repairDesign) iterated this stale list, and combined with OpenSTA's parallel BFS this produced non-determinism.' An earlier suspect — an OpenMP loop in DRT's FlexPA::updateDirtyInsts, which oharboe bisected to with a '#pragma omp' disable — was a red herring for this repro ('this patch is in DRT, which is long after repair_timing' — gadfort).",
  "candidates_considered": "Disable the DRT FlexPA parallel loop (oharboe's minimal patch — fixed the symptom, wrong component, rejected as the fix); wait for the STA-update non-determinism fix merged that weekend (maliberty's first guess — 'still happens'); fix RSZ cache invalidation at each buffer-mutation site (fragile); remove the local cache entirely and use OpenSTA's Levelize::levelizedDrvrVertices() (chosen).",
  "chosen_intervention": "PR #10155 'Driver vertex level cache': removes the Resizer's local cache and uses OpenSTA's Levelize, 'auto-invalidated via existing pin connect/disconnect callbacks, so all buffer-mutation paths are covered.'",
  "post_state": "'This appears to be already fixed in current master' (minjukim55, 2026-04-28); oharboe accepts: 'if the test case in this issue works, then for me this is solved.'",
  "gaps": [
    "No explicit re-run of the original two-hash harness is quoted post-fix — acceptance is oharboe's 'for me this is solved' plus the root-cause analysis.",
    "The FlexPA OpenMP suspicion was never separately resolved (may be a real but distinct nondeterminism)."
  ],
  "confidence": 0.85,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/9781",
  "source_type": "github-issue",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/9781",
  "direct_quote": {
    "text": "The Resizer maintained its own driver-vertex level cache (level_drvr_vertices_) that was not invalidated after BufferMove inserted buffers. Subsequent code (e.g. RepairDesign::repairDesign) iterated this stale list, and combined with OpenSTA's parallel BFS this produced non-determinism.",
    "by": "minjukim55",
    "date": "2026-04-28",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/9781"
  }
}
```


## Block 20 — eqy formal check exposes silent netlist corruption: RSZ journal restores optimizations out [issue-episodes-batch2.json]

RECORD: OpenROAD issue #5733, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "title": "eqy formal check exposes silent netlist corruption: RSZ journal restores optimizations out of order",
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/5733",
  "prior_state": "secure-CI on sky130hd/gcd runs eqy (formal equivalence) across repair_timing; PR #5693's changes innocuous but exposed the failure. Initial reading: pin swaps on non-swappable instances (a32o, a21oi in the transitive fanin of failing output net40); SKIP_PIN_SWAP=1 makes eqy pass.",
  "observation": "eqy reports nonequivalence after resize. QuantamHD traced net40 back to a gate whose IO 'has been broken by something other than pin swap': before resize _037_ = dpath.a_lt_b$in1[0] drives the and4b_1 C pin; after, net81 drives its B pin — connectivity changed under a 'swap' that was later undone.",
  "hypothesis": "precisionmoon reconstructed the exact sequence: '1) pin swap _455_ C->B 2) remove buffer _358_ 3) unswap _455_ B->C 4) unremove buffer _358_. Since the journal restore is done out of order, buffer restoration fails because the recorded pin connections before buffer removal is no longer valid.' And it fails silently: 'does it fail silently? — Yes, it doesn't know it failed.' (The SKIP_PIN_SWAP correlation was a red herring: 'random fluctuations leading to this thing not happening' — QuantamHD.)",
  "candidates_considered": "A) Fix RSZ journal save/restore to honor optimization order (patch-the-patch); B) remove RSZ journaling and rewrite on odb save/restore (chosen — maliberty: 'Let's do B as we keep hitting these and that's the best solution').",
  "chosen_intervention": "Rewrite of RSZ journaling on the odb journal; resolved per precisionmoon 2024-10-02 ('is this resolved now with the odb journal? — Yes.').",
  "post_state": "eqy passes on the secure-CI configuration; silent-failure class eliminated at the journaling layer.",
  "gaps": [
    "The implementing PR for the odb-journal rewrite is not cited in-thread.",
    "No statement on whether any historical tapeouts could have been affected by silent journal failures (the check that caught it — eqy in secure-CI — is not a default flow step)."
  ],
  "confidence": 0.85,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/5733",
  "source_type": "github-issue",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/5733",
  "direct_quote": {
    "text": "Since the journal restore is done out of order, buffer restoration fails because the recorded pin connections before buffer removal is no longer valid.",
    "by": "precisionmoon",
    "date": "2024-09-16",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/5733"
  }
}
```


## Block 21 — DRT runtime regression on ispd19_test6: misaligned GCELLGRID from read-guides path, plus a [issue-episodes-batch2.json]

RECORD: OpenROAD issue #3535, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "title": "DRT runtime regression on ispd19_test6: misaligned GCELLGRID from read-guides path, plus a thermal-throttling measurement confound",
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/3535",
  "prior_state": "ispd19_test6 routed via read-guides (guides from file rather than in-session global route); results kept from May 2022 (20min read_guides + 30min global route) for comparison; June 2023 rebuild.",
  "observation": "Route-guides runtime 20min -> 50min (DRT-0267 elapsed 00:29:38 -> 00:50:15) for the same technology and same guides, buying the fix of a single macro-pin violation. maliberty's iter-0 DRC inspection: the new build (3b67f4e0) shows 'a lot of weird violations and jogs' absent in the old (22b748a8); the oddities are periodic, 'nearly matches the worker size which makes me think it is a boundary condition', keyed to 'May2022: GCELLGRID X -100 DO 905 STEP 3000' vs 'June2023: GCELLGRID X 0 DO 905 STEP 3000'.",
  "hypothesis": "maliberty: 'The problem originates in GlobalRouter::updateDbCongestionFromGuides() which we only call when guides are read from a file. This will affect ispd benchmarks but not ORFS flows. That said we'll fix it.' Separately, the reporter's post-fix timings (61min, then 70min) turned out to be machine noise: after a reboot, 37min elapsed despite higher CPU time (4h20 vs 3h40) — 'don't trust any runtimes on M1 16GB MacBookAir MacOS Ventura without a reboot!' (QuantamHD had half-jokingly suggested the fridge test for thermal throttling.)",
  "candidates_considered": "Dismiss as quality-for-runtime trade ('less compelling as the old result was worse than the new result (1 drv vs 0)' — maliberty, initially); perf-profile both builds (QuantamHD's proposal, superseded by the GCELLGRID observation); fix the guides-reading congestion update (chosen); add a gross-error runtime CI (maliberty: 'Runtime CIs tend to be very noise... perhaps we need one for gross errors' — not landed).",
  "chosen_intervention": "Fix landed as PR #3545 (referenced by the reporter's post-fix log, 2023-06-28): GCELLGRID alignment restored ('Same GCELLGRID for May 2022 and Jun28 2023, so I'm running with the fix').",
  "post_state": "Guides-path regression fixed and confirmed via the GCELLGRID log line; residual runtime variance attributed to the reporter's machine (thermal/state), not the tool. maliberty's 40-CPU runs show 2023 ~15min elapsed.",
  "gaps": [
    "No post-fix 20-min-class timing from the reporter's machine is quoted (their post-fix numbers are confounded by the machine state until the 37min-after-reboot data point).",
    "The gross-error runtime CI was proposed but not implemented in-thread."
  ],
  "confidence": 0.75,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/3535",
  "source_type": "github-issue",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/3535",
  "direct_quote": {
    "text": "The problem originates in GlobalRouter::updateDbCongestionFromGuides() which we only call when guides are read from a file.  This will affect ispd benchmarks but not ORFS flows.  That said we'll fix it.",
    "by": "maliberty",
    "date": "2023-06-28",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/3535"
  }
}
```


## Block 22 — DRT 4-hour pause after '100%': one 235k-pin unclocked net throttling per-net post-processi [issue-episodes-batch2.json]

RECORD: OpenROAD issue #4612, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "title": "DRT 4-hour pause after '100%': one 235k-pin unclocked net throttling per-net post-processing",
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/4612",
  "prior_state": "TilePRCIDomain (megaboom test branch, asap7), NUM_CORES=16; 0th DRT optimization iteration reaches 'Completing 100% with 79991 violations' then stalls for ca. 4 hours with no output.",
  "observation": "Silent multi-hour pause after the 100% line (connectivity-check / guide-processing territory). osamahammad21's profiling: 'one extremely large net that needs to be partitioned... (235K pins). The net is causing throttling during operations that are performed on each net individually, such as connectivity checking and guide processing.' The net is auto_tap_clock_in_clock — a clock the reporter omitted from the .sdc ('out of ignorance by me') — plus a massive synchronous-reset net; the resizer had already logged '[WARNING RSZ-0069] skipping net auto_tap_clock_in_clock with 235689 pins.'",
  "hypothesis": "High-fanout nets surviving to DRT make per-net workloads pathological; the flow should surface them long before detailed routing. Early-thread meta-discussion established the debuggability constraint: progress output must preserve hermeticity/idempotency ('+1 to preserving hermiticity/idempotency as a top priority' — QuantamHD; maliberty: 'I don't see any way to measure time in an idempotent way').",
  "candidates_considered": "Warn in DRT when a net is pathologically large (osamahammad21: 'there should be a warning in DRT to detect such case and warn the user instead of leaving them in the dark for hours'); report top-10 highest-fanout nets right after synthesis (oharboe; maliberty: nets may legitimately be buffered later, so too early); add it to check_setup (rejected — 'Its not a violation to have a high fanout net early in the flow'); user-side max-fanout constraint + 'report_check_types -max_fanout' (maliberty's operational answer); PR #5676 (maliberty: 'a reasonable solution if the runtime is acceptable').",
  "chosen_intervention": "Diagnosis + guidance rather than a single code change: 'No nets should be high fanout when reaching drt' (maliberty) — catch unconstrained clocks/resets via a max-fanout limit and report_check_types -max_fanout; PR #5676 accepted as the reasonable fix path; the user's actual bug was the missing clock constraint.",
  "post_state": "Root cause identified to the user's satisfaction (missing .sdc clock + sync-reset fanout); issue closed 2024-08-31 with the RSZ-0069 warnings pointed out as the existing early signal.",
  "gaps": [
    "Whether the DRT-side large-net warning or #5676 actually landed is not confirmed in-thread.",
    "No runtime-after-fix number (fixing the .sdc presumably removes the 4-hour pause, but no re-run is quoted)."
  ],
  "confidence": 0.65,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/4612",
  "source_type": "github-issue",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/4612",
  "direct_quote": {
    "text": "It seems that there is one extremely large net that needs to be partitioned in my opinion(235K pins). The net is causing throttling during operations that are performed on each net individually, such as connectivity checking and guide processing.",
    "by": "osamahammad21",
    "date": "2024-08-31",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/4612"
  }
}
```


## Block 23 — DRT DRC decision: pin access 'not so close to the cell edge' — rule-driven ideal vs fixed  [issue-episodes-batch2.json]

RECORD: OpenROAD issue #6097, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "title": "DRT DRC decision: pin access 'not so close to the cell edge' — rule-driven ideal vs fixed 2x-width pragmatism",
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6097",
  "prior_state": "Mature technology whose GO1 cell library has site width not a multiple of the routing pitch ('This library is badly designed... They unfortunately won't redesign these cells' — 215 cells, irreplaceable); custom tracks impractical with two power domains (GO2 sites are correct). v2.0-16855.",
  "observation": "After 18 DRT iterations, 40 similar violations remain: M2 routing follows tracks strictly when switching to M1 at pin access, causing DRC. stefanottili's read: sites not a multiple of routing pitch means none of the stdcell pins are on-track. Root finding (maliberty): 'the row based search finds the lowest cost set of APs but they are not DRC free. I suppose it hopes that dr will find a solution and accepts it. Really we need to generate at least one AP that is not so close to the edge.'",
  "hypothesis": "Pin-access pattern generation terminates at MINNUMACCESSPOINT_STDCELLPIN without guaranteeing an access point far enough from the cell edge; on this library every candidate is edge-hugging, so DRT inherits unwinnable DRC. bnmfw's experiment (#6889): 'twice the layer width (getLayer(...)->getWidth() * 2) gave the best results... DRT flow still ended with DRVs but it reached the minimum of 4 during incremental repair instead of 55.'",
  "candidates_considered": "Workarounds: 'global_placement -pad_left 1 -density 0.8' + 'set_placement_padding -global -left 1', or '-min_access_points 5' (both confirmed working by maliberty); structural fix options — drive the 'not so close' threshold from actual DRC rules assuming a shape at minimum distance outside the cell (thorough), or fix it at 2x layer width (pragmatic).",
  "chosen_intervention": "maliberty's ruling: 'The most thorough solution would be to drive the \"not so close\" with the DRC rules... I don't want to spend too much effort on this corner case and think just picking 2 is fine so long as the runtime increase in \"normal\" designs isn't too large. I think there is a case for doing a PR and moving on.'",
  "post_state": "Decision recorded 2025-04-01 (2x layer width, runtime-guarded); PR to follow; issue closed 2025-04-02. The padding/min_access_points workarounds stand for affected libraries.",
  "gaps": [
    "The follow-up PR implementing the 2x-width rule is not identified in-thread, nor its runtime measurement on normal designs.",
    "4 residual DRVs (down from 55) remained even in bnmfw's best experiment — not fully zero."
  ],
  "confidence": 0.7,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6097",
  "source_type": "github-issue",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6097",
  "direct_quote": {
    "text": "The most thorough solution would be to drive the \"not so close\" with the DRC rules assuming a shape at the minimum possible distance outside the cell.  I don't want to spend too much effort on this corner case and think just picking 2 is fine so long as the runtime increase in \"normal\" designs isn't too large.",
    "by": "maliberty",
    "date": "2025-04-01",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6097"
  }
}
```


## Block 24 — MegaBoom repair_timing spends 40000s repairing 1 endpoint and crashes — 'hopeless repair'  [issue-episodes-batch2.json]

RECORD: OpenROAD issue #7274, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "title": "MegaBoom repair_timing spends 40000s repairing 1 endpoint and crashes — 'hopeless repair' tolerance diagnosed, not fixed",
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/7274",
  "prior_state": "MegaBoom CTS-era timing repair (48 threads, asap7 via bazel-orfs); previously ~reasonable; a successful docker run (v3.0-2863) of the same stage took ca. 45 minutes.",
  "observation": "The CTS step crashes with 'malloc(): corrupted top size' after ca. 40000s; the time sink is repair_timing (~27000s+): '[INFO RSZ-0094] Found 24253 endpoints with setup violations. [INFO RSZ-0099] Repairing 1 out of 24253 (0.00%) violating endpoints...' grinding for hours, one 182-buffer hold insertion visible ('Inserted 182 hold' with WNS -199.845 / TNS -251912.531 on one endpoint). precisionmoon reproduced: 'CTS took just 66 sec but setup fixing is taking more than 2 hours even with 0% TNS target.'",
  "hypothesis": "Termination tolerance, not a code regression: precisionmoon — 'Even with -repair_tns 0, we continue fixing since the WNS is not fully fixed. Currently, we terminate if there is no progress for 200 iterations, which may be too large.' oharboe's isolation: 'changing initial conditions will make repair timing finish quickly... there is something special about this exact test case and initial conditions that lead to repair timing taking forever, not a change in code as such' (megaboom PR #244 bumped ORFS). Runtime profile (perf top, vtunes) pointed at timer updates, 'especially required time updates', shared with povik for a runtime effort.",
  "candidates_considered": "Early-abort heuristics for hopeless repair (oharboe: 'It would be nice if hold repair gave up quickly on lost causes... some heuristic to error out early that this is never ever [fixable]'); natural stop when the worst endpoint changes during single-endpoint repair (oharboe's suggestion); '-skip_last_gasp' option (precisionmoon's available mitigation); reduce timer/required-time update cost (povik + vtunes data); treat as testcase-specific initial-conditions pathology and move on (the de facto outcome).",
  "chosen_intervention": "None landed: diagnosis + mitigation guidance only (-skip_last_gasp, smaller no-progress iteration budget considered 'too large' at 200), plus the runtime-effort handoff. Reporter shifted to updating ORFS on megaboom (PR #244) to change initial conditions.",
  "post_state": "Unresolved in-thread; stale-closed 2026-06-14. The 200-iteration no-progress termination and the timer-update hotspot are the recorded levers.",
  "gaps": [
    "No fix merged; the malloc crash itself was never root-caused (only suspected OOM via futile hold repair: 'futile hold repair running out of memory?').",
    "bazel-specific strangeness (signal 6 not stopping the job, no CPU used) unexplained.",
    "The vtunes/povik runtime effort's outcome is not in this thread."
  ],
  "confidence": 0.45,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/7274",
  "source_type": "github-issue",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/7274",
  "direct_quote": {
    "text": "Even with -repair_tns 0, we continue fixing since the WNS is not fully fixed.    Currently, we terminate if there is no progress for 200 iterations, which may be too large.",
    "by": "precisionmoon",
    "date": "2025-05-09",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/7274"
  }
}
```


## Block 25 — GPL divergence with 0 HPWL: division-by-zero in gradient when the netlist has no nets (moc [issue-episodes-batch2.json]

RECORD: OpenROAD issue #7745, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/7745",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/7745",
  "direct_quote": {
    "text": "The crash of the design happens due to a division to 0 during gradient calculations. If the HPWL gradient of all instances is 0, we should finish nicely with only the density portion of the gradient, although we don't reach 0.1 overflow.",
    "by": "gudeh",
    "date": "2025-07-15",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/7745"
  },
  "title": "GPL divergence with 0 HPWL: division-by-zero in gradient when the netlist has no nets (mocked-SRAM floorplans)",
  "prior_state": "asap7 tag-array floorplan built from mocked SRAMs (RTL eviscerated; only blockages + IO pins remain), global_placement skip-io stage; testcase global_place_skip_io_tag_array_64x184. Filed 2025-07-08.",
  "observation": "[ERROR GPL-0305] RePlAce diverged during gradient descent calculation, resulting in an invalid step length (Inf or NaN) around iteration 2210-2250, with HPWL stuck at exactly 0.000000e+00 and the penalty term exploding (1.42e+33 -> 6.67e+33). Bisect impractical: the most recent commit supporting the testcase ODB format (a090ebaa) fails too.",
  "hypothesis": "gudeh: with zero nets, the HPWL gradient is 0 for all instances, so gradient normalization divides by zero; placement should finish on the density-only gradient but instead creeps and dies. Deeper wrinkle found mid-investigation: a cluster of 66 instances stacked on top of each other, connected by dangling nets with a single iTerm, producing 'this strange force'.",
  "candidates_considered": "Avoid the error at 0 HPWL without warning (gudeh's first branch, gpl-avoid-error-at-0-hpwl); warn and proceed (oharboe's preference); accept as odd corner case and leave (maliberty's first reaction: 'I think that's fine as it is such an odd corner case'); maliberty's PR #7814 plus the alternative of every ~100 iterations bumping exactly-coincident instances apart via a location hash; gudeh's structural fix (remove skip_io mode entirely, GPL positions IO pins itself).",
  "chosen_intervention": "Structural: gudeh's skip_io removal work plus PR #10074 (same root cause as issue #9804) — gudeh: \"I would expect it to have been solved with latest version, after PR #10074 merged\".",
  "post_state": "oharboe closes 2026-05-06: \"Have not seen this problem for a while now.\" The reporter had worked around it in his bazel-orfs test suite and reverted the workaround once fixed.",
  "gaps": [
    "The exact content of PR #10074 and its relationship to PR #7814 (parked, possibly never landed) is not elaborated in-thread.",
    "No numeric post-fix placement quality data.",
    "The 66-instance dangling-net cluster was observed but never individually root-caused."
  ],
  "confidence": 0.75,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/7745",
  "source_type": "github-issue"
}
```


## Block 26 — DPL creates unroutable placement for centered (non-origin) floorplans — fixed by the new l [issue-episodes-batch2.json]

RECORD: OpenROAD issue #6704, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6704",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6704",
  "direct_quote": {
    "text": "FARADAY_ICCAD04Bench/RISC2 with the \"noram.def\" can be placed and routed both with/without -use_negotiation.",
    "by": "stefanottili",
    "date": "2026-06-25",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6704"
  },
  "title": "DPL creates unroutable placement for centered (non-origin) floorplans — fixed by the new legalizers",
  "prior_state": "ICCAD04 testcase with a centered DIEAREA (origin not 0,0); gpl/rudy/grt/drt/gui all handle it correctly; detailed_placement is the outlier. Worked as of 2024-08-15 (issue #5557 era); bisect impractical (older versions fail to build with boost 1.87). v2.0-18955.",
  "observation": "detailed_placement 'messes up the stdcells and creates an unroutable placement'; the identical netlist on a first-quadrant floorplan legalizes fine (total displacement 107598.5u, delta HPWL 9%).",
  "hypothesis": "Regression in the hybrid-rows rework of the detailed placer for non-origin core areas (maliberty attributed it to the substantial hybrid-row changes; initially \"This has no priority to fix\").",
  "candidates_considered": "Bisect to the breaking change (rejected: boost 1.87 build incompatibility); leave unfixed as no-priority (superseded); fix within the old legalizer; replace the legalizer — PR #10064 (negotiation-based legalization) and the Diamond Search fixes in PR #10727.",
  "chosen_intervention": "New legalization algorithms: PR #10064 (negotiation-based, planned to become default with the old one retired — maliberty 2026-04-14: \"The plan is to make it the default\") and PR #10727 fixing centered-floorplan handling in Diamond Search.",
  "post_state": "Reporter verifies 2026-06-25: \"FARADAY_ICCAD04Bench/RISC2 with the \\\"noram.def\\\" can be placed and routed both with/without -use_negotiation.\" Further negotiation-legalizer changes still queued at close.",
  "gaps": [
    "No single commit was identified as the original regression.",
    "QoR comparison old-vs-new legalizer not quantified in-thread.",
    "Issue was nearly stale-closed twice before the fix landed; the reporter had to keep it alive."
  ],
  "confidence": 0.7,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/6704",
  "source_type": "github-issue"
}
```


## Block 27 — GRT-attributed ODB non-determinism actually originates in pin_access (microwatt, sky130hd) [issue-episodes-batch2.json]

RECORD: OpenROAD issue #10023, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/10023",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/10023",
  "direct_quote": {
    "text": "The non-determinism was caused by the pin_access. A PR is coming with the fixes, but in my last run with your testcase, I got the expected output:",
    "by": "eder-matheus",
    "date": "2026-04-08",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/10023"
  },
  "title": "GRT-attributed ODB non-determinism actually originates in pin_access (microwatt, sky130hd)",
  "prior_state": "sky130hd/microwatt global route; CI had seen the antenna-diode count metric jump 2425 -> 4276 (limit 2635) in #4080; reporter built a self-contained two-run ODB-hash harness (global_route_diode_ndet.tar.gz). Filed 2026-04-01.",
  "observation": "Two back-to-back identical runs produce different ODB files. eder-matheus's isolation: the output guide files are byte-identical across all 10 runs, but the ODB files differ — \"I'm not sure if GRT is the cause of this, since its output is the same across the runs.\"",
  "hypothesis": "The ODB mutation happens outside GRT proper: pin_access writes into the database; its ordering/content varies run to run, which both changes the ODB hash and (in the CI case) plausibly perturbs downstream diode insertion.",
  "candidates_considered": "Blame GRT (the initial framing, disproven by identical guides); environment factors (ASLR, CPU affinity — explicitly tested against and ruled out by the fix verification matrix).",
  "chosen_intervention": "pin_access determinism fixes (PR number not stated in-thread: \"A PR is coming with the fixes\").",
  "post_state": "Verification matrix from eder-matheus (2026-04-08): 8 conditions (baseline x2, aslr-off, taskset-cpu0, taskset-cpu0-3, repeat x3) all produce diodes=2425 and identical odb_sha1 14444758b22d061a307b.",
  "gaps": [
    "The fixing PR is referenced as forthcoming but never numbered in the thread.",
    "The link from pin_access nondeterminism to the #4080 diode-count jump is described as \"likely\", not proven."
  ],
  "confidence": 0.8,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/10023",
  "source_type": "github-issue"
}
```


## Block 28 — FlexGC-vs-KLayout signoff disagreement near SRAM macro pins resolved as KLayout hierarchic [issue-episodes-batch2.json]

RECORD: OpenROAD issue #11326, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/11326",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/11326",
  "direct_quote": {
    "text": "The 4 markers flagged by KLayout (`m2.2` x 1, `m3.2` x 3) are **hierarchical cross-cell boundary false positives** produced by KLayout's pure-geometry runset (`sky130hd.lydrc`) running in `deep` mode without connectivity information.",
    "by": "Talha-Dmr",
    "date": "2026-09-03",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/11326"
  },
  "title": "FlexGC-vs-KLayout signoff disagreement near SRAM macro pins resolved as KLayout hierarchical false positive",
  "prior_state": "sky130hd design with sky130_sram_1rw1r_64x256_8 macro after detailed routing; independent signoff DRC run with KLayout sky130hd.lydrc in deep mode. Filed and self-resolved the same day (2026-09-03).",
  "observation": "DRT finishes clean (\"DRT-0199 Number of violations = 0\") while KLayout flags 4 metal-spacing markers on dense macro pin escapes: m2.2 x 1 on dout0[54], m3.2 x 3 on dout0[52]. Initial framing: a silent FlexGC DRC miss.",
  "hypothesis": "Reporter's own RCA reversal after dissecting GDS shapes and FlexGC_init.cpp initNet_pins_polygon: the KLayout markers are hierarchical cross-cell-boundary false positives — the pure-geometry runset without connectivity treats same-net abutting shapes across the macro boundary as unmerged; when flattened and unioned as manufactured, the violations disappear (survives_flat_merged_spacing_recheck: false). FlexGC correctly unions same-net route and pin polygons.",
  "candidates_considered": "Treat as FlexGC silent miss (initial hypothesis, reversed); treat as KLayout runset limitation in deep mode without connectivity (confirmed); adjust the signoff deck to union same-net geometry before spacing checks.",
  "chosen_intervention": "None in OpenROAD: FlexGC upheld; the resolution is methodological — connectivity-aware or flattened-merged recheck before trusting pure-geometry hierarchical markers at macro boundaries.",
  "post_state": "Issue closed by reporter 80 minutes after opening with the RCA update; no maintainer involvement.",
  "gaps": [
    "No maintainer confirmation of the root-cause analysis.",
    "No fix or deck change landed anywhere — the outcome is the analysis itself.",
    "Single data point (one design, one macro type)."
  ],
  "confidence": 0.35,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/11326",
  "source_type": "github-issue"
}
```


## Block 29 — GRT guides over a single-layer planar region: DRT abandons guides for a shorter path and s [issue-episodes-batch2.json]

RECORD: OpenROAD issue #2577, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/2577",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/2577",
  "direct_quote": {
    "text": "The problem isn't the guides but that drt doesn't follow them as it sees a much shorter path.",
    "by": "maliberty",
    "date": "2022-12-06",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/2577"
  },
  "title": "GRT guides over a single-layer planar region: DRT abandons guides for a shorter path and shorts",
  "prior_state": "GF180 design; macro obstruction on Metal4 leaves Metal5 as the only available layer in a region; GRT creates two Metal5 guides there (related to #1518). 2022-12.",
  "observation": "drt finishes with one short between two nets whose GRT guides were separate; maliberty's counter-diagnosis with screenshots: \"The problem isn't the guides but that drt doesn't follow them as it sees a much shorter path\" — the guides themselves are \"pretty ugly and suggest major detouring due to congestion\".",
  "hypothesis": "Out-of-guide cost is too low in planar (single-layer) regions, so DRT rips off the guide for marginal wirelength, creating the short and potentially large detours/hold risk upstream (reporter: \"drt could drastically change the wire length (as it has above) and create hold violations\").",
  "candidates_considered": "Increase out-of-guide cost in planar routing areas (maliberty); cost wrong-way edges higher in planar regions (maliberty's second option); raise GUIDECOST globally (reporter's suggestion, with the caveat it 'could negatively impact some designs'); reduce the GRT layer derating (50% default in ORFS) that produces the ugly guides in the first place.",
  "chosen_intervention": "None recorded — design discussion only; issue closed stale 2025-08-26 (\"stale\" — maliberty).",
  "post_state": "Unfixed; the two cost-tuning directions (out-of-guide cost in planar regions; wrong-way edge costing) remain the recorded proposal set.",
  "gaps": [
    "No fix, PR, or benchmark of any candidate landed.",
    "Closed stale after ~2.7 years.",
    "The exact DRC/short mechanism at the Metal5 planar pinch was never traced to a code line."
  ],
  "confidence": 0.4,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/2577",
  "source_type": "github-issue"
}
```


## Block 30 — repairDesign core dump when buffering a net from an IO-pad core-side output to an SRAM mac [issue-episodes-batch2.json]

RECORD: OpenROAD issue #3563, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/3563",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/3563",
  "direct_quote": {
    "text": "I can reproduce the crash. It is happening when the repairDesign is trying to fix the rst_int net.",
    "by": "openroadie",
    "date": "2023-07-05",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/3563"
  },
  "title": "repairDesign core dump when buffering a net from an IO-pad core-side output to an SRAM macro input",
  "prior_state": "A non-clock net driven from the core-side output of an IO pad into an SRAM macro input, with fan-out to registers (2 flops triggers it in resizer.tcl; 162 flops in gpl.tcl). 2023-07.",
  "observation": "Core dump during repairDesign/repair_timing buffering; openroadie reproduced on the rst_int net (\"I can reproduce the crash. It is happening when the repairDesign is trying to fix the rst_int net\") and questioned whether fanout fixing should target what looks like a reset; chaufe's domain answer: fanout fixing is required for any net (transition times outside characterized range, switching-current and electromigration reliability).",
  "hypothesis": "Buffering a mixed-domain net (pad output to macro input) trips a crash in the resizer's buffer insertion; the thread does not isolate the code path.",
  "candidates_considered": "Skip fanout repair on reset-like nets (rejected on timing/reliability grounds); fix the crash in buffering (chosen); file as two testcases under one root cause (reporter's framing, accepted).",
  "chosen_intervention": "Fix landed out-of-thread (commit/PR not identified); reporter confirms 2023-07-20: \"Thanks for the fix. The core-dumps are gone now.\"",
  "post_state": "Both testcase variants pass.",
  "gaps": [
    "The fixing commit/PR is never named.",
    "No root-cause statement survived in the thread (what specifically about the pad-to-macro net crashed the buffer inserter)."
  ],
  "confidence": 0.5,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/3563",
  "source_type": "github-issue"
}
```


## Block 31 — CTS signal-6 lockup "once in a blue moon" — closed unreproduced after overnight loop attem [issue-episodes-batch2.json]

RECORD: OpenROAD issue #7752, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/7752",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/7752",
  "direct_quote": {
    "text": "We need a better reproduction procedure or it is too costly to pursue. Closing.",
    "by": "oharboe",
    "date": "2025-07-10",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/7752"
  },
  "title": "CTS signal-6 lockup \"once in a blue moon\" — closed unreproduced after overnight loop attempts",
  "prior_state": "CTS on a large clock (\"[INFO CTS-0099] Sinks 121655\"); intermittent hang or abort, \"doesn't always happen. If it happens, reproducible in minutes and the job hangs(OpenROAD does not exit with an error)\".",
  "observation": "Nondeterministic CTS lockup/crash (signal 6) with a Google-Drive repro; both reporter and maintainer looped the testcase overnight without a single recurrence (\"I left the testcase running throw the night in a loop. I didn't get any crash\" / \"Same here\").",
  "hypothesis": "Never formed — the failure never recurred under controlled conditions, so no diagnosis could start.",
  "candidates_considered": "Overnight loop reproduction attempts (both parties); collecting more occurrences in the wild with better telemetry; closing as unreproducible (chosen).",
  "chosen_intervention": "Closure decision by oharboe (2025-07-10): 'We need a better reproduction procedure or it is too costly to pursue. Closing.'",
  "post_state": "Closed without diagnosis; no fix.",
  "gaps": [
    "Root cause unknown; even the failure signature beyond \"signal 6 / hang\" is unrecorded.",
    "No telemetry hook was added to catch future occurrences in CI."
  ],
  "confidence": 0.3,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/7752",
  "source_type": "github-issue"
}
```


## Block 32 — RSZ-2008 "wire step options empty" in timing-driven placement — closed as not reproducible [issue-episodes-batch2.json]

RECORD: OpenROAD issue #8229, The-OpenROAD-Project/OpenROAD (GitHub issue thread).

```json
{
  "issue_url": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/8229",
  "section_or_page_locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/8229",
  "direct_quote": {
    "text": "I'm going to close this issue, as it does not show up with LibreLane 3.0 and a recent OpenROAD.\nShould it come up again, I'll prepare a fresh test case.",
    "by": "mole99",
    "date": "2026-03-30",
    "locator": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/8229"
  },
  "title": "RSZ-2008 \"wire step options empty\" in timing-driven placement — closed as not reproducible on current stack",
  "prior_state": "Full-chip gf180mcuD design; global placement with -timing_driven; OpenROAD + LibreLane of the day (activity 2025-11 to 2026-03).",
  "observation": "\"[CRITICAL RSZ-2008] buffering pin gf180mcu_fd_io__in_s_clk/Y: wire step options empty\" aborts timing-driven placement; omitting -timing_driven completes successfully.",
  "hypothesis": "The buffering engine found no legal wire-step option for the IO-cell pin under the gf180mcu Liberty/RC data; the thread chased reproducibility (mole99's LibreLane reproducible had broken absolute paths in _env.tcl, fixed and re-grepped) rather than the engine logic, and the failure never reproduced on LibreLane 3.0 + recent OpenROAD.",
  "candidates_considered": "Fix the reproducible and re-test (twice); treat as an old-stack artifact (chosen); prepare a fresh testcase if it recurs (reporter's standing offer).",
  "chosen_intervention": "None — version-drift closure. mole99 (2026-03-30): \"I'm going to close this issue, as it does not show up with LibreLane 3.0 and a recent OpenROAD. Should it come up again, I'll prepare a fresh test case.\"",
  "post_state": "Closed unresolved-by-code; presumed fixed incidentally by intervening changes.",
  "gaps": [
    "No root cause or fixing commit identified — \"fixed by drift\".",
    "The RSZ-2008 diagnostic quality (what \"wire step options empty\" should tell a user) was not improved."
  ],
  "confidence": 0.35,
  "x_source": "https://github.com/The-OpenROAD-Project/OpenROAD/issues/8229",
  "source_type": "github-issue"
}
```


## Block 33 — LibreLane PDN-0179 "Unable to repair all channels" with SRAM macros — resolved as user dec [issue-episodes-batch2.json]

RECORD: LibreLane issue #908, librelane/librelane (GitHub issue thread).

```json
{
  "issue_url": "https://github.com/librelane/librelane/issues/908",
  "section_or_page_locator": "https://github.com/librelane/librelane/issues/908",
  "direct_quote": {
    "text": "This looks like a common issue during floorplanning: the macros are placed in such a way that there are small channels of standard cell rows. These channels are not large enough to insert power straps for VDD/VSS.",
    "by": "mole99",
    "date": "2026-03-31",
    "locator": "https://github.com/librelane/librelane/issues/908"
  },
  "title": "LibreLane PDN-0179 \"Unable to repair all channels\" with SRAM macros — resolved as user deck fault, not upstream",
  "prior_state": "SG13G2 (ihp) wrapper_with_sram probe: 4 real SRAM macros, custom PDN deck and config; failing step 20-openroad-generatepdn. Reported through LibreLane per OpenROAD maintainers' recommendation. 2026-03.",
  "observation": "\"PDN-0179 Unable to repair all channels\" preceded by \"PDN-0178 Remaining channel ... on Metal1 for nets: VDD, VSS\". Earlier unrelated failure modes (RCX/DEF parser, TopMetal2 cross-connect) already ruled out by the reporter's own sweeps.",
  "hypothesis": "mole99's floorplan reading: macro placement leaves small standard-cell-row channels too narrow for power straps. The reporter's four-variant placement sweep (inset_240um / flush_to_core_edge, each with low-halo variants) tested exactly this — and the error persisted in all, which pointed away from pure channel width.",
  "candidates_considered": "Move macros to eliminate/widen channels (tested via the 4-variant sweep — not sufficient); LibreLane reproducible iterations (first ZIP missing DEF, rebuilt; ODB then failed to open with \"string pointer is null\"); send design-only sources (chosen for final diagnosis); rebuild on the official ihp-sg13g2 template (the actual resolution).",
  "chosen_intervention": "Config rebuild: on the official template the flow completes; the remaining faults were the user's (SRAM fast-corner mapping, Checker.IllegalOverlap setting, MACROS.instances/PDN_CFG path alignment). Not an upstream bug.",
  "post_state": "\"the unmodified official IHP template runs to Flow complete / our template-native 4x SRAM probe runs to Flow complete / a small template-native KAN 2x-style design with 4 real SRAM macros also runs to Flow complete.\" mole99 also asked the reporter to stop relaying replies through an LLM.",
  "gaps": [
    "No OpenROAD/pdngen code change resulted.",
    "The reproducible never opened cleanly in the maintainer's GUI (ODB \"string pointer is null\") — that tooling wrinkle was left unexplained.",
    "The channel-width threshold below which PDN-0178/0179 fires is not documented anywhere in-thread."
  ],
  "confidence": 0.6,
  "x_source": "https://github.com/librelane/librelane/issues/908",
  "source_type": "github-issue"
}
```


## Block 34 — LVS fails on nets with >2 pins: magic extraction drops them and the checker mis-parses net [issue-episodes-batch2.json]

RECORD: LibreLane issue #111, librelane/librelane (GitHub issue thread).

```json
{
  "issue_url": "https://github.com/librelane/librelane/issues/111",
  "section_or_page_locator": "https://github.com/librelane/librelane/issues/111",
  "direct_quote": {
    "text": "Tracking in https://github.com/RTimothyEdwards/netgen/issues/78...",
    "by": "ohl-bot",
    "date": "2025-04-18",
    "locator": "https://github.com/librelane/librelane/issues/111"
  },
  "title": "LVS fails on nets with >2 pins: magic extraction drops them and the checker mis-parses netgen JSON",
  "prior_state": "OpenLane 2.0.0a47-era flow (migrated issue, originally efabless/openlane2#111, 2023-07): Magic SPICE extraction + netgen LVS via Checker.LVS, tinytapeout-04 multiplexer design. Migrated to librelane/librelane 2025-04.",
  "observation": "Two distinct faults: (1) spice extraction ignores nets with more than two pins, fixed locally by adding \"ext2spice short resistor\" to extract_spice.tcl (netgen then passes: \"Circuits match uniquely\"); (2) Checker.LVS reports mismatches because the netgen JSON report's pin lists diverge from the text report — \"The JSON report is basically fine for the first three, then it breaks.\"",
  "hypothesis": "Extraction-side: Magic's default ext2spice handling splits multi-pin nets into resistor islands unless shorting is enabled. Checker-side: a netgen report-format change breaks the JSON parse (donn: \"OpenLane parses the JSON report, so that's why it's reporting mismatches\").",
  "candidates_considered": "Add ext2spice short resistor to the flow script (user-side fix, later PR'd by urish); report upstream to netgen (chosen — tracked as RTimothyEdwards/netgen#78); patch Checker.LVS parsing locally.",
  "chosen_intervention": "Upstream netgen fix (netgen#78) + the extraction-script change (\"Actually, we're still missing ext2spice short resistor. When I tested locally, I already had that fix applied. I'll send a PR.\" — urish).",
  "post_state": "\"Tested and confirm it's working well now. Thanks for fixing this so quickly!\" (urish, 2023-07-13); the ext2spice PR followed.",
  "gaps": [
    "The exact netgen commit/PR that fixed #78 is not named in this thread.",
    "All content is from the migrated openlane2 issue; no LibreLane-era re-verification.",
    "Quote recovered verbatim from the ohl-bot migration comment (2025-04-18), which reposts donn's 2023-07-11T11:15:32Z comment from efabless/openlane2#111 (see the comment's '[Originally posted]' header) — migration disclosure retained from the prior citation."
  ],
  "confidence": 0.7,
  "x_source": "https://github.com/librelane/librelane/issues/111",
  "source_type": "github-issue"
}
```


