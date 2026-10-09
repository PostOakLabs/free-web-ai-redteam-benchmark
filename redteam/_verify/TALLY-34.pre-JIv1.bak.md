# TALLY-34 — red-team verdicts (fill per model run)

| # | Title | Model | Verdict | Fatal | Major | Note |
|---|---|---|---|---|---|---|
| 01 | BoomTile/Megaboom: 20k routing congestion DRCs at only 0.24 placement  |  |  |  |  |  |
| 02 | GPL-0314: getFillerGCell index out of bounds during global placement |  |  |  |  |  |
| 03 | RUDY and global-route congestion maps disagree for ICCAD04 risc2 testc |  |  |  |  |  |
| 04 | GRT DRC-error cap (10000) hides congestion hotspots and macro-overlap  |  |  |  |  |  |
| 05 | repair_timing ODB-1200 with Liberty flip-flops defining Q→QN output-to |  |  |  |  |  |
| 06 | TritonCTS segfault in getBufferFanoutLimit when Liberty has no max_cap |  |  |  |  |  |
| 07 | CTS NDRs on heavily gated clocks cause routing congestion (level defin |  |  |  |  |  |
| 08 | asap7 cva6 hierarchical-synth GRT congestion report references a nonex |  |  |  |  |  |
| 09 | STA: false hold/setup violations in floorplan from ideal top-level clo |  |  |  |  |  |
| 10 | GPL regression: too-early non-virtual timing-driven iteration makes pr |  |  |  |  |  |
| 11 | GPL: RePlAce divergence (GPL-0307) on megaboom — snapshot-delivery mit |  |  |  |  |  |
| 12 | Manual macro placement (R90, asap7 M2) leaves pins off routing grid -> |  |  |  |  |  |
| 13 | DRT assert in patchMetalShape_minStep: violation on last metal layer i |  |  |  |  |  |
| 14 | GRT heap underflow (GRT-0183) after antenna repair — FastRoute resourc |  |  |  |  |  |
| 15 | PDN: negative placement halo mis-applied to obstructions/pins shorts m |  |  |  |  |  |
| 16 | CTS crash (stack overflow in computeSinkArrivalRecur) after clock-gate |  |  |  |  |  |
| 17 | CTS design decision: balance macro insertion latency against register  |  |  |  |  |  |
| 18 | PDN legality decision: rings outside the die area become an error (wit |  |  |  |  |  |
| 19 | repair_timing non-determinism with threads>1: stale driver-vertex leve |  |  |  |  |  |
| 20 | eqy formal check exposes silent netlist corruption: RSZ journal restor |  |  |  |  |  |
| 21 | DRT runtime regression on ispd19_test6: misaligned GCELLGRID from read |  |  |  |  |  |
| 22 | DRT 4-hour pause after '100%': one 235k-pin unclocked net throttling p |  |  |  |  |  |
| 23 | DRT DRC decision: pin access 'not so close to the cell edge' — rule-dr |  |  |  |  |  |
| 24 | MegaBoom repair_timing spends 40000s repairing 1 endpoint and crashes  |  |  |  |  |  |
| 25 | GPL divergence with 0 HPWL: division-by-zero in gradient when the netl |  |  |  |  |  |
| 26 | DPL creates unroutable placement for centered (non-origin) floorplans  |  |  |  |  |  |
| 27 | GRT-attributed ODB non-determinism actually originates in pin_access ( |  |  |  |  |  |
| 28 | FlexGC-vs-KLayout signoff disagreement near SRAM macro pins resolved a |  |  |  |  |  |
| 29 | GRT guides over a single-layer planar region: DRT abandons guides for  |  |  |  |  |  |
| 30 | repairDesign core dump when buffering a net from an IO-pad core-side o |  |  |  |  |  |
| 31 | CTS signal-6 lockup "once in a blue moon" — closed unreproduced after  |  |  |  |  |  |
| 32 | RSZ-2008 "wire step options empty" in timing-driven placement — closed |  |  |  |  |  |
| 33 | LibreLane PDN-0179 "Unable to repair all channels" with SRAM macros —  |  |  |  |  |  |
| 34 | LVS fails on nets with >2 pins: magic extraction drops them and the ch |  |  |  |  |  |

## Per-model summary (one row per model pasted)

| Model | Date | SOUND | SOUND-WITH-RES | SUSPECT | IMPLAUSIBLE | Survivors first |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |
