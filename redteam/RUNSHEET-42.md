# RUNSHEET-42 — 42 red-team paste blocks for `prompts/J-EPISODE-REDTEAM-V3.md` (2026-09-08)

Every paper-episode object in the corpus, rendered from `extractions/*.episodes.json`. No rewording,
no enrichment. **One disclosed normalisation, described below; every other byte is verbatim.**

## The one normalisation — `direct_quote` line-wrap, 18 of 42 blocks

Stored quotes carry the PDF's `\r\n` line breaks, often mid-word. **18 of the 42 are affected, and
two whole pools are affected entirely** (Niagara 6/6, POWER4-circuit-physical 8/8). Left in, they
make `quote_plausibility` judge PDF extraction artifacts rather than prose on 43% of the run.

J-v3 already resolved this for the one block it controls — its BUILD NOTE records collapsing the
exemplar's wrap points to single spaces *"so quote_plausibility judges prose rather than line-wrap
artifacts. No words changed."* **The same collapse is applied here to all 18, and to nothing else.**
The builder asserts it: the whitespace-split word sequence of every quote must be identical before
and after, and every other field must compare byte-equal to its source object, or the build aborts.

**Consequence, verified:** substituting Block 8 reproduces the unmodified J-v3 prompt exactly —
same JSON object, same `PAPER:` line. Before this normalisation it did not, which is how the issue
was found.

**One quote is degenerate and was NOT repaired.** Block 34 (`POWER4-d2true` ep05) reads `"Eight-way, 128-byte line \x011.5 MB"` — a stray control character
from the PDF layer survives the wrap collapse. Repairing it would be a content edit. Treat
`quote_plausibility` on that block as uninformative rather than as a fabrication signal.

## ⛔ How to paste — READ THIS, the obvious method is wrong

J-v3 is a **standalone** prompt: it already contains a worked exemplar under the heading
*"The draft under review:"*. Appending a block after it gives the model **two** drafts and no
statement of which to review.

**For each block: paste J-v3 with the block SUBSTITUTED IN, not appended.** Replace the prompt's
`PAPER:` line and the JSON fence that follows it with the block's `PAPER:` line and JSON fence.
Everything else in the prompt — the review schema, the hard rules, the version tag — stays byte
identical. Stop at the `---` rule; the BUILD NOTE below it is not part of the paste.

*(The same ambiguity exists in the `RUNSHEET-34.md` / `J-ISSUE-REDTEAM-V1.md` pairing, which says
"paste ONE block together with the prompt". Substitution is the correct reading there too.)*

## Contents — 42 blocks, 5 papers, 6 extraction files

| blocks | paper | extraction file |
|---|---|---|
| 01–07 | Alpha 21264 | `Alpha21264.episodes.json` |
| 08–13 | Niagara | `Niagara.episodes.json` |
| 14–20 | Pentium 4 | `Pentium4.episodes.json` |
| 21–28 | POWER4 circuit/physical | `POWER4-circuit-physical-design.episodes.json` |
| 29–34 | POWER4 system — d2true pool | `POWER4-d2true.episodes.json` |
| 35–42 | POWER4 system | `POWER4-system-microarchitecture.episodes.json` |

**Schema pre-check passed:** all 42 episodes carry exactly J-v3's nine keys — `title`,
`section_or_page_locator`, `decision`, `alternatives_or_rejected`, `rationale`, `outcome`,
`direct_quote`, `gaps`, `confidence` — with no extras and none missing. This check is the one that
was never run for J-v2 against the issue-episode set, which is why that pairing collapsed to its own
escape clause on all 34 blocks (`SESSION-MEMORIAL-2026-09-08-REDTEAM.md` §1). J-v3 genuinely fits
this pool.

**Operator notes — not part of any paste:**

- **Block 8 is the exemplar baked into J-v3 itself.** Run it as a **calibration check**: J-v3's BUILD NOTE calls this a
  known-**sound** episode, so a reviewer returning many fatal objections here is miscalibrated, and
  its other 41 verdicts should be read in that light. It is not new evidence.
- **Two POWER4 pools describe the same paper** (IBM JRD 46(1) pp. 5–25). `POWER4-d2true` was
  authored 2026-09-04 from verified claims in `digest/episode-draft-bank.md`;
  `POWER4-system-microarchitecture` is the direct extraction. No two titles are identical, but
  **Block 32 (d2true, "Absolute binary-compatibility requirement...") and Block 36 (sys,
  "Maintain binary compatibility with prior PowerPC systems") are the same decision extracted twice.** A
  reviewer should reach compatible verdicts on both; divergence is a finding about the reviewer or
  about one of the two extractions.
- **Alpha 21264 blocks carry two 2026-09-08 corrections.** `SESSION-MEMORIAL-2026-09-08-REDTEAM-3.md`
  fixed `outcome` percentages in ep00 (`5%`→`90%`) and ep06 (`95%`→`85%`) against
  `sources/Alpha21264-pagemarked.txt`. These blocks render the corrected values. A reviewer
  objecting to either number is objecting to the source text.
- **Quote-completeness differs sharply by pool and will skew `quote_plausibility`.** J-v3's BUILD
  NOTE measured it: Alpha, Pentium 4 and POWER4-system stored quotes are 37–58-character
  **mid-phrase fragments**; POWER4-circuit and Niagara quotes are complete sentences. A fragment is
  a property of the extraction, **not** evidence the quote is fabricated. Expect
  `quote_plausibility` to be least reliable on blocks 01–07, 14–20 and 35–42.
- **`direction_check` can be graded against each model's own prior recall.** All 13 panel models
  answered PROMPT-L/M/N/O/P on 2026-08-31 (Day 1) and the five D2-* prompts (Day 4) on the same five
  papers. A model contradicting its own recall is a stronger signal than one contradicting an
  unaided judgment.

---

## Block 01 — Tournament branch predictor combining local and global history [Alpha21264.episodes.json ep00]

PAPER: R. E. Kessler, "The Alpha 21264 Microprocessor," IEEE Micro, vol. 19, no. 2, pp. 24-36, March-April 1999.

```json
{
  "title": "Tournament branch predictor combining local and global history",
  "section_or_page_locator": "Branch prediction, page 3",
  "decision": "Implement a two-level tournament branch predictor that selects, per branch invocation, between a local-history prediction path and a global-history prediction path via a chooser (choice prediction) table indexed by path history.",
  "alternatives_or_rejected": "Using only a larger table of either the individual local-history method or the global-history method was chosen against; the paper states the tournament result delivers better accuracy. An idealized single larger table is the rejected side.",
  "rationale": "Branches exhibit both local correlation (relying on a branch's past behavior) and global correlation (relying on the past behavior of preceding branches), so dynamically choosing the best method per branch minimizes mispredicts.",
  "outcome": "Better prediction accuracy than larger tables of either individual method, with a 90% to 100% success rate on most simulated applications/benchmarks. The processor adapts to dynamically choose the best method for each branch.",
  "direct_quote": "accuracy than larger tables of either individual",
  "gaps": [
    "The paper does not state the exact mispredict rate, the chooser table replacement/training policy details beyond chooser counters trained to prefer the correct prediction when local and global predictions differ, or quantitative comparison to a solely local or solely global baseline on real (non-simulated) hardware.",
    "The paper does not give absolute accuracy percentages for the local-only or global-only predictors to quantify the advantage.",
    "The paper does not state the silicon area or power cost of the tournament predictor versus a single large table.",
    "2026-09-04 repair: stored Y-encoded fragment replaced with the true pagemarked-source span (byte-verbatim)."
  ],
  "confidence": 0.75
}
```

## Block 02 — Register file clustering (split integer register file into two clusters) [Alpha21264.episodes.json ep01]

PAPER: R. E. Kessler, "The Alpha 21264 Microprocessor," IEEE Micro, vol. 19, no. 2, pp. 24-36, March-April 1999.

```json
{
  "title": "Register file clustering (split integer register file into two clusters)",
  "section_or_page_locator": "Execution engine, pages 7",
  "decision": "Split the four integer execution pipes into two clusters, each cluster made of two pipes accessing a duplicate 80-entry (integer) register file, to simplify and speed the design.",
  "alternatives_or_rejected": "A single unclustered register file / idealized unclustered implementation. Two clusters were chosen; the trade-off is an extra cycle of latency to broadcast results from one integer cluster to the other, with only a few percent or less performance cost in most applications.",
  "rationale": "Clustering makes the design simpler and faster and provides much of the implementation simplicity, lower risk, and higher speed of a two-issue machine, while retaining the performance benefits of four-way integer issues.",
  "outcome": "Approximately the design is a few percent slower than an idealized unclustered implementation in most applications; the two-cluster arrangement became the shipped design.",
  "direct_quote": "simpler and faster, although it costs an extra",
  "gaps": [
    "The paper does not state the exact number of extra cycles in absolute clock terms beyond the broadcast latency, nor specify which specific integer operations can only execute on the upper/lower pipes.",
    "The paper does not quantify the 'few percent or less' performance cost with a concrete benchmark number.",
    "The paper does not describe how duplicate register files are kept coherent across the two clusters.",
    "2026-09-04 repair: stored Y-encoded fragment (with 'q' for comma) replaced with the true source span; the passage was identified by its unique decoded wording."
  ],
  "confidence": 0.8
}
```

## Block 03 — Double-pumped data cache to provide two memory ports [Alpha21264.episodes.json ep02]

PAPER: R. E. Kessler, "The Alpha 21264 Microprocessor," IEEE Micro, vol. 19, no. 2, pp. 24-36, March-April 1999.

```json
{
  "title": "Double-pumped data cache to provide two memory ports",
  "section_or_page_locator": "Internal memory system - Data path, page 8",
  "decision": "Implement the data cache as a double-pumped array referenced twice per processor clock cycle (once per clock phase) so it effectively operates at twice the processor-clock frequency, supplying the necessary two ports without conflict.",
  "alternatives_or_rejected": "A single-ported cache or a conventionally two-ported cache design; not explicitly stated as a rejected alternative, but the double-pumping is presented as the mechanism chosen to deliver the required two ports while supporting two loads/stores per cycle without conflicts.",
  "rationale": "The memory system supports any combination of two loads or stores per cycle without conflicts, and double-pumping provides the necessary two ports while also enabling read-modify-write sequences for store ECC updates and for write-back fills using the same bus data.",
  "outcome": "The data cache can be referenced twice each cycle, enabling two references per cycle and read-modify-write operations; part of the high-bandwidth, low-latency memory system.",
  "direct_quote": "In effect, the data cache operates at twice the",
  "gaps": [
    "The paper does not state the measured bandwidth or latency numbers attributable specifically to double-pumping versus a two-ported array.",
    "The paper does not state the area, power, or access-path penalty of double-pumping versus a multi-ported cache.",
    "The alternatives considered (single-port, SRAM dual-port, banker's dual-port, etc.) are not listed.",
    "2026-09-04 repair: stored Y-encoded fragment replaced with the true source span (the data-path occurrence, matching this episode)."
  ],
  "confidence": 0.65
}
```

## Block 04 — Dynamic store/load ordering adaptation using a load-wait table [Alpha21264.episodes.json ep03]

PAPER: R. E. Kessler, "The Alpha 21264 Microprocessor," IEEE Micro, vol. 19, no. 2, pp. 24-36, March-April 1999.

```json
{
  "title": "Dynamic store/load ordering adaptation using a load-wait table",
  "section_or_page_locator": "Store/load memory ordering, pages 11",
  "decision": "Handle the store-after-load (read-after-write) memory hazard by having the memory system squash the offending load and all subsequent instructions when it is discovered after issue, then set a bit in a load-wait table so subsequent executions delay the load's issue until all prior stores have issued.",
  "alternatives_or_rejected": "Relying on the register-renaming map stage to resolve memory read-after-write dependencies (rejected because the rename logic does not have the memory address until the instruction issues); also avoided the cost of load misspeculation by remembering the first misspeculation and delaying the load on subsequent executions.",
  "rationale": "The architecture must maintain an in-order architectural memory model, yet cannot use register renaming for memory dependencies since addresses are unknown at issue time; dynamically detecting the problem after issue and then adapting (delaying future loads) avoids repeated misspeculation.",
  "outcome": "The processor yields results identical to an in-order memory system while capturing the performance advantages of out-of-order execution; unmarked loads issue as early as possible while only marked (delayed) loads are held back. The load-wait table is periodically cleared to avoid unnecessary waits.",
  "direct_quote": "issue point of the marked load to be delayed",
  "gaps": [
    "The paper does not state the size of the load-wait table or how many distinct load PC/loads it can track simultaneously.",
    "The paper does not specify the exact interval at which the load-wait table is periodically cleared, nor the cost of an occasional unnecessary wait.",
    "The paper does not quantify the performance gain versus simply always delaying loads behind stores.",
    "2026-09-04 repair: stored Y-encoded fragment replaced with the true pagemarked-source span (byte-verbatim)."
  ],
  "confidence": 0.7
}
```

## Block 05 — Minirestart instead of full pipeline restart for load-miss speculation [Alpha21264.episodes.json ep04]

PAPER: R. E. Kessler, "The Alpha 21264 Microprocessor," IEEE Micro, vol. 19, no. 2, pp. 24-36, March-April 1999.

```json
{
  "title": "Minirestart instead of full pipeline restart for load-miss speculation",
  "section_or_page_locator": "Load hit/miss prediction, page 12",
  "decision": "When consumers (and beneficiaries) of a load's data have speculatively issued and the load later misses, squash only two integer issue cycles across all four integer pipes and pull those instructions back into the issue queue to be reissued later, rather than restarting the entire pipeline.",
  "alternatives_or_rejected": "Relying on the general speculative-execution engine's mechanisms to abort the speculatively executed consumers, which requires restarting the entire instruction pipelines; rejected because load misses can be frequent in some applications so that technique would be too expensive.",
  "rationale": "The two-cycle window is less costly than fully restarting the pipeline, and the three-cycle integer load-hit latency requires speculatively issuing consumers before the hit/miss indication is known.",
  "outcome": "Inexpensive reissue of consumers and beneficiaries; If a load is predicted to hit, the original schedule runs; if the load is (incorrectly) predicted to miss, the effective load latency is five cycles rather than the minimum three, but more unrelated instructions can issue.",
  "direct_quote": "than fully restarting the processor pipeline, it",
  "gaps": [
    "The paper does not quantify how often the two-cycle squashing actually occurs in real workloads or its average cost.",
    "The paper does not state the number of cycles required for the full (non-minirestart) pipeline restart that was avoided.",
    "The paper does not describe the exact hardware to identify 'beneficiary' instructions that must also be reissued.",
    "2026-09-04 repair: stored Y-encoded fragment replaced with the true source span; the passage was identified by its unique decoded wording."
  ],
  "confidence": 0.75
}
```

## Block 06 — Splitting conditional-move instructions to fit the two-source map [Alpha21264.episodes.json ep05]

PAPER: R. E. Kessler, "The Alpha 21264 Microprocessor," IEEE Micro, vol. 19, no. 2, pp. 24-36, March-April 1999.

```json
{
  "title": "Splitting conditional-move instructions to fit the two-source map",
  "section_or_page_locator": "Register renaming, page 6",
  "decision": "Split each Alpha conditional-move instruction into two instructions and map them separately, so each resulting instruction has only two register sources (the first places the move value plus a bit indicating ultimate success/failure into an internal register; the second reads that result plus the old destination to produce the final result).",
  "alternatives_or_rejected": "Mapping the conditional-move as a single three-source instruction (not stated as explicitly rejected, but the reason given is that conditional move is the only Alpha instruction requiring three register sources, which is why it must be split to expose only two sources to the map stage).",
  "rationale": "Register renaming assigns unique storage with each writer and the map stage must handle exactly two sources; because conditional move is the only Alpha instruction with three register sources, it must be split into two instructions that each expose only two sources so they can be mapped separately.",
  "outcome": "Conditional moves are handled specially by the map stage and carry a success/failure bit to decide between the new move value and the old destination value.",
  "direct_quote": "splits each conditional move instruction into two and maps them separate- ly.",
  "gaps": [
    "The paper does not state the performance or instruction-count cost of splitting every conditional move into two instructions.",
    "The paper does not state the cycle/pipe penalty, if any, of the extra internal instruction the split produces.",
    "The paper does not state whether an explicit alternative (e.g., a three-source map or a dedicated CMOV unit) was evaluated.",
    "2026-09-04 repair: stored text 'maps them separater' was a misreading of hyphenated 'separate-ly' across a line break; replaced with the true source span preserving the hyphenation artifact verbatim."
  ],
  "confidence": 0.6
}
```

## Block 07 — Line-and-way prediction for fast set-associative instruction fetch [Alpha21264.episodes.json ep06]

PAPER: R. E. Kessler, "The Alpha 21264 Microprocessor," IEEE Micro, vol. 19, no. 2, pp. 24-36, March-April 1999.

```json
{
  "title": "Line-and-way prediction for fast set-associative instruction fetch",
  "section_or_page_locator": "Line and way prediction, page 3",
  "decision": "Implement a line-and-way prediction technique that, on each four-instruction fetch block, predicts where to fetch the next four instructions including which of the two ways of the two-way set-associative instruction cache to read, using the wraparound path to fetch before the validity/tag check completes.",
  "alternatives_or_rejected": "Simple direct-mapped instruction cache and a conventional set-associative cache; the technique is chosen because it combines the advantages of set-associative behavior (higher hit rates) and fetch bubble elimination with the fast access time of a direct-mapped cache.",
  "rationale": "It is an important speed enhancement since the mispredict cost is low and line/way mispredictions are rare, and it avoids the mis-fetch penalty associated with a taken branch for predictable branches such as loop terminators. The line predictor is also trained with jump and subroutine-call targets to help indirect jumps whose address calculation requires eight cycles or more.",
  "outcome": "Line and way predictors are correct 85% to 100% of the time for most applications, so training is infrequent; most mispredictions cost a single cycle. A 2-bit hysteresis counter per fetch block eliminates overtraining.",
  "direct_quote": "enhancement since the mispredict cost is low",
  "gaps": [
    "The paper does not state the silicon area or power cost of the line-and-way predictor and its per-block training state.",
    "The paper does not give the measured fetch bandwidth or hit-rate numbers that result specifically from this technique.",
    "The paper does not compare power/area against a fully two-way-instruction fetch (fetching both ways) alternative.",
    "2026-09-04 repair: stored Y-encoded fragment replaced with the true pagemarked-source span (byte-verbatim)."
  ],
  "confidence": 0.65
}
```

## Block 08 — Adopt thread-rich (32-thread) throughput approach instead of single-thread ILP [Niagara.episodes.json ep00]  ⚠ CALIBRATION — this is the exemplar baked into J-v3 itself

PAPER: P. Kongetira, K. Aingaran, K. Olukotun, "Niagara: A 32-Way Multithreaded SPARC Processor," IEEE Micro, vol. 25, no. 2, pp. 21-29, March-April 2005.

```json
{
  "title": "Adopt thread-rich (32-thread) throughput approach instead of single-thread ILP",
  "section_or_page_locator": "page 1 (introduction)",
  "decision": "Design Niagara to optimize for multithreaded throughput in a commercial server environment rather than for single- or dual-thread performance. Build a machine with many hardware threads that hide memory latency, exploiting thread-level parallelism (TLP).",
  "alternatives_or_rejected": "Single-thread/ILP optimization (multiple instruction issue, out-of-order issue, aggressive branch prediction) and machines optimized for single-thread performance. Also rejected: simply running ILP processors at lower clock frequencies to save power.",
  "rationale": "Diminishing returns from single-thread focus because of limits on latency to main memory and inherently low ILP of applications; the ILP approach brought complexity and power concerns. Commercial server workloads are dominated by TLP, so increasing throughput across many threads is effective.",
  "outcome": "Niagara supports 32 hardware threads in hardware; application performance is increased by improving throughput (total work across threads).",
  "direct_quote": "This approach increases application performance by improving throughput, the total amount of work done across multiple threads of execution.",
  "gaps": [
    "The paper does not quantify the measured power or performance difference versus a specific single-thread ILP processor.",
    "It does not state the target clock frequency for the thread-rich design.",
    "It does not give quantitative ILP-vs-TLP performance comparisons, only a qualitative figure and Table 1 (application ILP/TLP categories)."
  ],
  "confidence": 0.95
}
```

## Block 09 — Group threads into a shared SPARC pipe (4 threads per single-issue pipeline) [Niagara.episodes.json ep01]

PAPER: P. Kongetira, K. Aingaran, K. Olukotun, "Niagara: A 32-Way Multithreaded SPARC Processor," IEEE Micro, vol. 25, no. 2, pp. 21-29, March-April 2005.

```json
{
  "title": "Group threads into a shared SPARC pipe (4 threads per single-issue pipeline)",
  "section_or_page_locator": "page 3 (Niagara overview / Sparc pipeline)",
  "decision": "Organize four threads into a thread group; each group shares a single-issue, six-stage processing pipeline (the \"Sparc pipe\"), with eight groups yielding 32 threads. The pipeline hides memory and pipeline stalls of a thread by switching to other threads in the group with a zero-cycle switch penalty.",
  "alternatives_or_rejected": "The paper's hardware-multithreading primer explicitly contrasts this with simultaneous multithreading (SMT, instruction-level sharing across functional units on superscalar pipes), conventional fine/coarse-grained and vertical multithreading, and chip multiprocessing (independent single-threaded cores aggregated on a die). Niagara's fine-grained shared single-issue pipe is chosen over SMT/superscalar pipes.",
  "rationale": "Sharing a simple single-issue pipeline among multiple threads raises throughput while keeping area and complexity low, and the zero-cycle switch means threads hide each other's latencies.",
  "outcome": "Eight thread groups / SPARC pipes run 32 threads on the CPU; each thread has unique registers and instruction/store buffers while the group shares L1 caches, TLBs, execution units, and most pipeline registers.",
  "direct_quote": "organizes four threads into a thread group; the group shares a processing pipeline, referred to as the Sparc pipe.",
  "gaps": [
    "The paper does not state the required die area of the shared pipeline versus the SMT/CMP alternatives.",
    "It does not compare measured throughput of this grouping against a comparable SMT or CMP implementation.",
    "It does not explain how the choice of exactly four threads per group was determined."
  ],
  "confidence": 0.9
}
```

## Block 10 — Use a shared on-chip crossbar and shared L2 cache instead of off-chip coherent interconnect [Niagara.episodes.json ep02]

PAPER: P. Kongetira, K. Aingaran, K. Olukotun, "Niagara: A 32-Way Multithreaded SPARC Processor," IEEE Micro, vol. 25, no. 2, pp. 21-29, March-April 2005.

```json
{
  "title": "Use a shared on-chip crossbar and shared L2 cache instead of off-chip coherent interconnect",
  "section_or_page_locator": "page 3 (Niagara overview)",
  "decision": "Route memory references through a single on-chip crossbar to a banked, on-chip shared level-2 cache, rather than relying on a coherent interconnect between discrete processors.",
  "alternatives_or_rejected": "Conventional SMP systems built from discrete single-threaded processors using coherent system interconnects, where coherence misses travel over low-frequency off-chip buses or links. Also rejected: an SMP of multiple ILP-oriented processors (seen as neither power- nor cost-efficient).",
  "rationale": "Off-chip coherence misses have high latency; an SMP built to exploit ILP is not power or cost efficient. A shared on-chip cache eliminates these misses and replaces them with low-latency shared-cache communication, and on-chip communication is efficient for data sharing in commercial server applications.",
  "outcome": "The crossbar links SPARC pipes, L2 cache banks, and shared resources, providing more than 200 Gbytes/s of bandwidth and acting as the point of memory ordering for the machine.",
  "direct_quote": "and can have high latencies. The Niagara design with its shared on-chip cache",
  "gaps": [
    "The paper does not report the measured reduction in coherence misses or their average latency versus the off-chip interconnect alternative.",
    "It does not size the crossbar's area or power relative to an off-chip coherent interconnect approach.",
    "It does not quantify how much the eliminated coherence misses contributed to overall performance."
  ],
  "confidence": 0.9
}
```

## Block 11 — Provide a 3-Mbyte, 4-way banked, pipelined, 12-way set-associative shared L2 cache [Niagara.episodes.json ep03]

PAPER: P. Kongetira, K. Aingaran, K. Olukotun, "Niagara: A 32-Way Multithreaded SPARC Processor," IEEE Micro, vol. 25, no. 2, pp. 21-29, March-April 2005.

```json
{
  "title": "Provide a 3-Mbyte, 4-way banked, pipelined, 12-way set-associative shared L2 cache",
  "section_or_page_locator": "page 3 (Niagara overview / page 7 Memory subsystem)",
  "decision": "The 32 threads share a 3-Mbyte level-2 cache that is 4-way banked and pipelined for bandwidth, and made 12-way set-associative to reduce conflict misses from the many threads.",
  "alternatives_or_rejected": "not stated",
  "rationale": "Banking and pipelining provide the bandwidth demanded by many threads; higher associativity (12-way) minimizes conflict misses arising from many threads. The paper's rationale is implicit in the stated motivation to provide bandwidth for 32 threads.",
  "outcome": "A shared copy-back L2 with banks interleaved at 64-byte granularity and a directory shadowing L1 tags to maintain coherence at L1-line granularity.",
  "direct_quote": "The 32 threads share a 3-Mbyte level-2 cache. This cache is 4-way banked and pipelined for bandwidth;",
  "gaps": [
    "The paper does not state any rejected cache sizes, associativities, or bank counts.",
    "It does not give measured L2 miss rates or bandwidth utilization that justify 3 Mbytes / 4 banks / 12-way.",
    "It does not describe the performance or area trade-off versus smaller/larger or less-associative cache configurations."
  ],
  "confidence": 0.8
}
```

## Block 12 — Integrate four on-chip memory controllers for high memory bandwidth [Niagara.episodes.json ep04]

PAPER: P. Kongetira, K. Aingaran, K. Olukotun, "Niagara: A 32-Way Multithreaded SPARC Processor," IEEE Micro, vol. 25, no. 2, pp. 21-29, March-April 2005.

```json
{
  "title": "Integrate four on-chip memory controllers for high memory bandwidth",
  "section_or_page_locator": "page 2 / page 3 (memory interface, page 9)",
  "decision": "Provide a memory subsystem scaled for high bandwidth using four independent on-chip memory controllers, implemented as four channels of DDR2 DRAM supporting up to 128 Gbytes and in excess of 20 Gbytes/s.",
  "alternatives_or_rejected": "not stated",
  "rationale": "Having 32 threads places a heavy demand on the memory system for high bandwidth, so the memory subsystem is scaled up; on-chip controllers provide the required bandwidth to memory.",
  "outcome": "Four channels of DDR2 DRAM provide in excess of 20 Gbytes/s of memory bandwidth and up to 128 Gbytes of capacity.",
  "direct_quote": "Four independent on-chip memory controllers provide in excess of 20 Gbytes/s of bandwidth to memory.",
  "gaps": [
    "The paper does not state an explicit rejected alternative for memory organization (e.g., fewer channels, off-chip controllers, different DRAM generation).",
    "It does not provide measured bandwidth utilization or confirm the 20+ Gbytes/s under load.",
    "It does not explain how the number of channels (four) was chosen relative to the 32 threads' bandwidth demand."
  ],
  "confidence": 0.85
}
```

## Block 13 — Target low power/area (~60 W) by exploiting TLP instead of high clock frequency [Niagara.episodes.json ep05]

PAPER: P. Kongetira, K. Aingaran, K. Olukotun, "Niagara: A 32-Way Multithreaded SPARC Processor," IEEE Micro, vol. 25, no. 2, pp. 21-29, March-April 2005.

```json
{
  "title": "Target low power/area (~60 W) by exploiting TLP instead of high clock frequency",
  "section_or_page_locator": "page 2 (introduction)",
  "decision": "Target a low-power, area-efficient design (~60 W dissipated) by exploiting TLP to improve performance without pushing CPU clock frequency, and by sharing CPU pipelines among multiple threads.",
  "alternatives_or_rejected": "Reducing power by running ILP processors in server clusters at lower clock frequencies (rejected because the proportional performance loss makes it less desirable); also implicitly the high-power/high-complexity ILP approach.",
  "rationale": "Servers are deployed in high compute-density data centers where power supply and heat dissipation are significant cost factors; performance per watt is the key requirement, favoring a low-power thread-rich design.",
  "outcome": "Designers expect Niagara to dissipate about 60 W of power, making it attractive for high compute-density environments.",
  "direct_quote": "Designers expect Niagara to dissipate about 60 W of power, making it",
  "gaps": [
    "The paper does not give a measured power figure, only an expected ~60 W.",
    "It does not state the process technology or operating voltage/frequency at which this power is expected.",
    "It does not compare the resulting performance-per-watt against a specific ILP server processor numerically."
  ],
  "confidence": 0.9
}
```

## Block 14 — Execution Trace Cache as L1 instruction cache instead of a conventional I-cache [Pentium4.episodes.json ep00]

PAPER: G. Hinton, D. Sager, M. Upton, D. Boggs, D. Carmean, A. Kyker, P. Roussel, "The Microarchitecture of the Pentium 4 Processor," Intel Technology Journal, Q1 2001.

```json
{
  "title": "Execution Trace Cache as L1 instruction cache instead of a conventional I-cache",
  "section_or_page_locator": "Page 2 (Trace Cache)",
  "decision": "Replace the conventional Level 1 instruction cache with an Execution Trace Cache that stores already-decoded IA-32 uops and sits between decode logic and the execution core.",
  "alternatives_or_rejected": "The conventional L1 instruction cache arrangement used on previous machines (e.g., the P6/Pentium III), which stores raw IA-32 instruction bytes and re-decodes them.",
  "rationale": "IA-32 instructions are cumbersome and variable-length to decode; caching decoded uops removes decoding from the main execution loop and reduces misprediction recovery time, since the target path need not be re-decoded. This lets the decoder be simplified to one instruction per clock cycle.",
  "outcome": "The Trace Cache holds up to 12K uops and delivers up to three uops per clock, with a hit rate similar to an 8K-16K byte conventional instruction cache.",
  "direct_quote": "Unlike conventional instruction caches, the",
  "gaps": [
    "Does not give the absolute comparison of the Trace Cache's power or die cost versus a conventional I-cache",
    "Does not state instruction-decoder silicon area or design-effort savings numerically",
    "Does not quantify branch-misprediction latency reduction in clock cycles"
  ],
  "confidence": 0.95
}
```

## Block 15 — Choosing a deeper pipeline to chase a high target frequency [Pentium4.episodes.json ep01]

PAPER: G. Hinton, D. Sager, M. Upton, D. Boggs, D. Carmean, A. Kyker, P. Roussel, "The Microarchitecture of the Pentium 4 Processor," Intel Technology Journal, Q1 2001.

```json
{
  "title": "Choosing a deeper pipeline to chase a high target frequency",
  "section_or_page_locator": "Page 3 (Clock Rates)",
  "decision": "Design a much deeper pipeline (~2x the P6) with fewer gates of logic per stage to reach a more than 1.6x higher frequency target on the same process.",
  "alternatives_or_rejected": "A shallower pipeline with more gates of logic per stage (the approach of the 286/386/486/P5 and, to a lesser degree, the P6).",
  "rationale": "Higher clock rates need deeper pipelines, lowering per-clock efficiency; but the frequency increase more than makes up for it. Example given: a 50% frequency increase buys only ~30% net performance gain.",
  "outcome": "The Pentium 4 misprediction pipeline grows to 20 stages versus the P6's 10 stages, achieving a much higher clock rate (1.5x the Pentium III at introduction).",
  "direct_quote": "There are tradeoffs when designing for higher clock rates.",
  "gaps": [
    "Does not give a quantitative efficiency-per-clock loss",
    "Does not quantify power/thermal impact of the deeper pipeline",
    "Does not state the exact target frequency numbers beyond relative ratios"
  ],
  "confidence": 0.9
}
```

## Block 16 — Double-pumped low-latency integer ALU while pushing rare functions off the fast loop [Pentium4.episodes.json ep02]

PAPER: G. Hinton, D. Sager, M. Upton, D. Boggs, D. Carmean, A. Kyker, P. Roussel, "The Microarchitecture of the Pentium 4 Processor," Intel Technology Journal, Q1 2001.

```json
{
  "title": "Double-pumped low-latency integer ALU while pushing rare functions off the fast loop",
  "section_or_page_locator": "Page 8 (Low Latency Integer ALU)",
  "decision": "Run the frequently used integer ALU at twice the main clock rate (a fast 2x clock) using a staggered add, keeping the core small to minimize metal length and loading.",
  "alternatives_or_rejected": "A single-speed ALU that processes operations at full main-clock latency rather than half-clock effective latency; and including the multiplier, shifts, flag logic, and branch processing in the fast ALU loop.",
  "rationale": "About 60-70% of integer uops use this ALU-bypass loop, so halving its latency speeds up most integer programs; the high-speed core is kept small for speed, and infrequently used functions are moved elsewhere.",
  "outcome": "ALU operations run with an effective latency of one-half a clock cycle via a three-fast-cycle staggered add (16-bit low, 16-bit high, then flags); this does not buy 2x but improves most integer applications.",
  "direct_quote": "multiplier, shifts, flag logic, and branch processing.",
  "gaps": [
    "Does not quantify the area or power saved by excluding those functions from the fast loop",
    "Does not state the exact fast-to-main clock ratio used for the multiplier/shift hardware",
    "Does not give measured integer IPC improvement"
  ],
  "confidence": 0.85
}
```

## Block 17 — Small low-latency L1 data cache backed by a large medium-latency L2 cache [Pentium4.episodes.json ep03]

PAPER: G. Hinton, D. Sager, M. Upton, D. Boggs, D. Carmean, A. Kyker, P. Roussel, "The Microarchitecture of the Pentium 4 Processor," Intel Technology Journal, Q1 2001.

```json
{
  "title": "Small low-latency L1 data cache backed by a large medium-latency L2 cache",
  "section_or_page_locator": "Page 9 (Low Latency Level 1 Data Cache)",
  "decision": "Use an 8K-byte, 4-way, write-through L1 data cache with 2-clock load-use latency for integer (6-clock for FP/SSE) instead of a larger but slower L1.",
  "alternatives_or_rejected": "A bigger, slower L1 data cache (a larger cache that would have higher access latency).",
  "rationale": "For most IA-32 programs, a small but very low-latency L1 backed by a large medium-latency L2 gives lower net load-access latency and higher performance than a larger, slower L1. The 2-clock latency is hard at high frequency and uses new access algorithms plus data speculation with replay.",
  "outcome": "L1 operates with a 2-clock load-use latency for integer and 6-clock for floating-point/SSE loads; up to four outstanding load misses are permitted, with replay used to re-execute dependent operations using incorrect data.",
  "direct_quote": "performance than a bigger, slower L1 cache.",
  "gaps": [
    "Does not quantify the trade-off between L1 size and real-world hit-rate",
    "Does not give the dead-code/prefetch cost of the replay mechanism",
    "Does not state bandwidth of the L1->L2 path in GB/s"
  ],
  "confidence": 0.9
}
```

## Block 18 — Second FP/SSE port chosen for cost/performance over a second full execution unit [Pentium4.episodes.json ep04]

PAPER: G. Hinton, D. Sager, M. Upton, D. Boggs, D. Carmean, A. Kyker, P. Roussel, "The Microarchitecture of the Pentium 4 Processor," Intel Technology Journal, Q1 2001.

```json
{
  "title": "Second FP/SSE port chosen for cost/performance over a second full execution unit",
  "section_or_page_locator": "Page 10 (FP/SSE Execution Units)",
  "decision": "Provide a simple second port that does FP/SSE moves and FP/SSE store data primitives rather than a second full FP/SSE execution unit.",
  "alternatives_or_rejected": "Two full FP/SSE execution units (the original design early in the development cycle), which cost a lot of hardware and did not buy much performance for most FP/SSE applications.",
  "rationale": "The tradeoff was shown to buy most of the performance of a second full-featured port with much less die size and power cost; FP/multi-media applications interleave multiplies and adds, so full pipelining of all FP/SSE hardware is not worth the cost.",
  "outcome": "A 128-bit execution port plus a 128-bit move/store port, giving a peak 6 GFLOPS (single) / 3 GFLOPS (double) at 1.5GHz.",
  "direct_quote": "This tradeoff was shown to buy most of",
  "gaps": [
    "Does not state the measured performance delta of the two-unit design",
    "Does not quantify the die-size or power savings in absolute terms",
    "Does not describe how the simple port maps to Figure 6's dispatch ports"
  ],
  "confidence": 0.95
}
```

## Block 19 — Separate ROB and register-file allocation instead of a single wide P6-style entity [Pentium4.episodes.json ep05]

PAPER: G. Hinton, D. Sager, M. Upton, D. Boggs, D. Carmean, A. Kyker, P. Roussel, "The Microarchitecture of the Pentium 4 Processor," Intel Technology Journal, Q1 2001.

```json
{
  "title": "Separate ROB and register-file allocation instead of a single wide P6-style entity",
  "section_or_page_locator": "Page 7 (Figure 5 discussion)",
  "decision": "Allocate the Reorder Buffer entries (status only, allocated sequentially) and the result-data Register File entries (allocated from a free list) separately.",
  "alternatives_or_rejected": "The P6 scheme, which allocates the data result registers and ROB entries as a single wide entity with both data and status fields, copying result data into a Retirement Register File upon retirement.",
  "rationale": "Separating the structures removes the physical copying of result data on retirement across the two structures.",
  "outcome": "Upon retirement, no result data values are actually moved from one physical structure to another.",
  "direct_quote": "result data values are actually moved",
  "gaps": [
    "Does not quantify the area or power savings versus the P6 scheme",
    "Does not state the size of the 128-entry physical register file vs. the ROB",
    "Does not explain the cost of the free-list allocation logic"
  ],
  "confidence": 0.8
}
```

## Block 20 — Quad-pumped 400MHz source-synchronous system bus for high streaming bandwidth [Pentium4.episodes.json ep06]

PAPER: G. Hinton, D. Sager, M. Upton, D. Boggs, D. Carmean, A. Kyker, P. Roussel, "The Microarchitecture of the Pentium 4 Processor," Intel Technology Journal, Q1 2001.

```json
{
  "title": "Quad-pumped 400MHz source-synchronous system bus for high streaming bandwidth",
  "section_or_page_locator": "Page 11 (400MHz System Bus)",
  "decision": "Use a 64-bit wide, source-synchronous protocol that quad-pumps the 100MHz bus to achieve 400 million data transfers per second (3.2 GB/s).",
  "alternatives_or_rejected": "Bringing the bus base clock up to the transfer rate (a non-quad-pumped bus and/or a wider/fully synchronous bus).",
  "rationale": "A high-bandwidth system bus is a key enabler for streaming-data applications (3D, video, content creation) that cannot be satisfied by cache sizes; it must deliver high effective bandwidth in real systems.",
  "outcome": "A 3.2 GB/s system bus with a split-transaction, deeply pipelined protocol and 64-byte access length.",
  "direct_quote": "uses a source-synchronous protocol that quad-pumps the",
  "gaps": [
    "Does not compare the quad-pumped width/rate against alternative point-to-point or wider bus options",
    "Does not quantify latency or the cost/complexity of quad-pumping versus a faster base clock",
    "Does not state power consumption contributed by the bus"
  ],
  "confidence": 0.85
}
```

## Block 21 — Predominantly static-circuit design with sparing use of dynamic circuits [POWER4-circuit-physical-design.episodes.json ep00]

PAPER: J. D. Warnock, J. M. Keaty, J. Petrovick, J. G. Clabes, C. J. Kircher, B. L. Krauter, P. J. Restle, B. A. Zoric, C. J. Anderson, "The circuit and physical design of the POWER4 microprocessor," IBM Journal of Research and Development, vol. 46, no. 1, pp. 27-52, January 2002.

```json
{
  "title": "Predominantly static-circuit design with sparing use of dynamic circuits",
  "section_or_page_locator": "Circuit design (===PAGE 7===)",
  "decision": "Adopt a primarily static-circuit design strategy across the chip, using dynamic circuits only sparingly in SRAMs and other critical regions of the processor core.",
  "alternatives_or_rejected": "Reject dynamic-circuit design more broadly; dynamic circuits are confined to registers, array circuitry, and load/store circuitry interfacing the data-cache array.",
  "rationale": "Power dissipation was a significant concern; SOI floating-body modeling uncertainties affecting noise immunity and chip decoupling capacitance; schedule risk from size/logical complexity, favoring a simple robust style with efficient CAD and design-resource use.",
  "outcome": "Static designs used predominantly; dynamic circuits limited to some register files, array circuitry, and load/store circuitry; the design was completed on schedule.",
  "direct_quote": "adoption of a primarily static-circuit design strategy, with dynamic circuits used only sparingly in SRAMs and other critical regions of the processor core.",
  "gaps": [
    "The paper does not quantify the exact area or fraction of the chip implemented in dynamic circuitry.",
    "The paper does not state which specific SRAMs/regions used dynamic circuits beyond register files, array circuitry, and load/store.",
    "The paper does not state the power or schedule savings attributable to choosing static vs. dynamic."
  ],
  "confidence": 0.85
}
```

## Block 22 — Single chip-wide global clock domain with no skew feedback or adjustment [POWER4-circuit-physical-design.episodes.json ep01]

PAPER: J. D. Warnock, J. M. Keaty, J. Petrovick, J. G. Clabes, C. J. Kircher, B. L. Krauter, P. J. Restle, B. A. Zoric, C. J. Anderson, "The circuit and physical design of the POWER4 microprocessor," IBM Journal of Research and Development, vol. 46, no. 1, pp. 27-52, January 2002.

```json
{
  "title": "Single chip-wide global clock domain with no skew feedback or adjustment",
  "section_or_page_locator": "Clock design (===PAGE 5===)",
  "decision": "Use a single chip-wide global clock domain with no skew feedback or adjustment settings, tuned from one global net covering the entire chip.",
  "alternatives_or_rejected": "Reject clock-distribution schemes that use feedback or adjustment circuitry to control skews (used common in prior designs dominated by skew-error concern).",
  "rationale": "Modeled skew was negligible, so clock timing reduced to an uncertainty due to model/process errors; allows simple constant clock uncertainty across the whole chip, giving simple clock timing and rapid bring-up.",
  "outcome": "Achieved measured jitter of 35 ps, skew of 20 ps, and a \"correct-by-design\" clock-distribution methodology; chip-to-chip jitter 150 ps.",
  "direct_quote": "using a single chip-wide global clock domain with no skew feedback or adjustment settings.",
  "gaps": [
    "The paper does not state the power or area cost of the single global clock net versus a skew-adjusted scheme.",
    "The paper does not describe the exact 35 ps jitter and 20 ps skew measurement conditions beyond use of I/Os and probe pads."
  ],
  "confidence": 0.9
}
```

## Block 23 — Transistor-level timing of custom macros rather than block-based timing [POWER4-circuit-physical-design.episodes.json ep02]

PAPER: J. D. Warnock, J. M. Keaty, J. Petrovick, J. G. Clabes, C. J. Kircher, B. L. Krauter, P. J. Restle, B. A. Zoric, C. J. Anderson, "The circuit and physical design of the POWER4 microprocessor," IBM Journal of Research and Development, vol. 46, no. 1, pp. 27-52, January 2002.

```json
{
  "title": "Transistor-level timing of custom macros rather than block-based timing",
  "section_or_page_locator": "Design flow and tools (===PAGE 5===)",
  "decision": "Time custom macros at the transistor level using Pathmill, and perform transistor-level noise analysis with Harmony.",
  "alternatives_or_rejected": "Reject a block-based timing approach for the custom macros.",
  "rationale": "Timing at the transistor level avoids inaccuracies and needless pessimism that arise from a block-based timing approach.",
  "outcome": "Transistor-level timing and noise runs produced both macro-internal reports and timing/noise rules used at upper hierarchy levels; rule-compliant macros via EinsCheck.",
  "direct_quote": "By timing at the transistor level, inaccuracies and needless pessimism that arise from a block-based timing approach were avoided.",
  "gaps": [
    "The paper does not quantify the timing accuracy or pessimism difference between the transistor-level and block-based approaches.",
    "The paper does not state the run-time cost of transistor-level timing per macro."
  ],
  "confidence": 0.85
}
```

## Block 24 — Fourteen-wiring-track power grid image with more power buses [POWER4-circuit-physical-design.episodes.json ep03]

PAPER: J. D. Warnock, J. M. Keaty, J. Petrovick, J. G. Clabes, C. J. Kircher, B. L. Krauter, P. J. Restle, B. A. Zoric, C. J. Anderson, "The circuit and physical design of the POWER4 microprocessor," IBM Journal of Research and Development, vol. 46, no. 1, pp. 27-52, January 2002.

```json
{
  "title": "Fourteen-wiring-track power grid image with more power buses",
  "section_or_page_locator": "Power distribution (===PAGE 15===)",
  "decision": "Adopt a fourteen-wiring-track power-grid image devoting four wiring tracks to power/ground and ten to signal wiring.",
  "alternatives_or_rejected": "Reject the long-standing IBM top-metal power distribution of wide power/ground buses repeated along the C4 rows (with lower-level wide buses at wide intervals), which had always satisfied dc requirements but not common-mode noise requirements.",
  "rationale": "Early common-mode noise analyses showed the inherited design would not satisfy common-mode noise requirements; adding power buses reduces return-path inductance and resistance and creates more quiet wiring tracks.",
  "outcome": "A fourteen-wiring-track image was selected; some additional tracks were gained via a new rectangular metal C4 pad design; exceptions allowed if power/ground used at least 25% of tracks and no more than ten signal wires between power buses.",
  "direct_quote": "the power grid that came closest to meeting the dc-noise, common-mode-noise, quiet-wiring-track, and wirability requirements was a fourteen-wiring-track image.",
  "gaps": [
    "The paper does not state the final measured/common-mode noise achieved versus the 200 mV limit.",
    "The paper does not state how many units could not strictly conform and required exceptions."
  ],
  "confidence": 0.85
}
```

## Block 25 — Selective use of low-threshold-voltage (low-Vt) devices [POWER4-circuit-physical-design.episodes.json ep04]

PAPER: J. D. Warnock, J. M. Keaty, J. Petrovick, J. G. Clabes, C. J. Kircher, B. L. Krauter, P. J. Restle, B. A. Zoric, C. J. Anderson, "The circuit and physical design of the POWER4 microprocessor," IBM Journal of Research and Development, vol. 46, no. 1, pp. 27-52, January 2002.

```json
{
  "title": "Selective use of low-threshold-voltage (low-Vt) devices",
  "section_or_page_locator": "Circuit styles (===PAGE 9===)",
  "decision": "Use low-Vt n-FET and p-FET devices selectively, only in the most timing-critical parts of the design.",
  "alternatives_or_rejected": "Reject widespread use of low-Vt devices, which deliver about 10% performance improvement but at higher off-state leakage currents.",
  "rationale": "Avoid a large increase in chip standby current while still capturing the performance benefit; process ground rules allowed swapping from normal Vt to low Vt at the last moment with minimal layout effect, postponing the decision.",
  "outcome": "Less than 10% of logic transistors implemented with low-Vt devices; low-Vt books used only where necessary on critical paths and ICC (ECC) logic.",
  "direct_quote": "it was desirable to use these low-Vt devices selectively, in only the most timing-critical parts of the design.",
  "gaps": [
    "The paper does not state the numerical leakage-power penalty avoided by the selective approach.",
    "The paper does not list which specific circuits received low-Vt devices beyond the ICC/ECC logic."
  ],
  "confidence": 0.85
}
```

## Block 26 — Split (transparent master/slave) latch scheme for critical timing paths [POWER4-circuit-physical-design.episodes.json ep05]

PAPER: J. D. Warnock, J. M. Keaty, J. Petrovick, J. G. Clabes, C. J. Kircher, B. L. Krauter, P. J. Restle, B. A. Zoric, C. J. Anderson, "The circuit and physical design of the POWER4 microprocessor," IBM Journal of Research and Development, vol. 46, no. 1, pp. 27-52, January 2002.

```json
{
  "title": "Split (transparent master/slave) latch scheme for critical timing paths",
  "section_or_page_locator": "Latch design (===PAGE 8===)",
  "decision": "Provide separate master and slave latch designs that can be inserted at arbitrary points in the logic so logic can propagate through alternating cycle-boundary and mid-cycle latches without a setup-time penalty.",
  "alternatives_or_rejected": "Reject reliance solely on the standard transmission-gate master-slave flip-flop, which includes two embedded inverters and a built-in setup-time penalty for clock skew, process variability, and ACLV.",
  "rationale": "Reduces latch overhead on critical paths, provides resistance to clock skew and process variation; logic timing can be borrowed/given between cycles.",
  "outcome": "Averaged half-cycle of logic allowed between c1 and c2 latches; split-latch designs added timing complexity and ac-test difficulty but were used to reduce critical-path latency.",
  "direct_quote": "Separate master and slave latch designs were provided, which could be inserted at arbitrary points in the logic.",
  "gaps": [
    "The paper does not quantify the setup-time/latency savings versus the standard flip-flop on critical paths.",
    "The paper does not state how widely split latches were used relative to standard latches."
  ],
  "confidence": 0.8
}
```

## Block 27 — Tunable sector trees driving a single full-chip clock grid [POWER4-circuit-physical-design.episodes.json ep06]

PAPER: J. D. Warnock, J. M. Keaty, J. Petrovick, J. G. Clabes, C. J. Kircher, B. L. Krauter, P. J. Restle, B. A. Zoric, C. J. Anderson, "The circuit and physical design of the POWER4 microprocessor," IBM Journal of Research and Development, vol. 46, no. 1, pp. 27-52, January 2002.

```json
{
  "title": "Tunable sector trees driving a single full-chip clock grid",
  "section_or_page_locator": "Global clock-distribution network (===PAGE 6===)",
  "decision": "Drive a single full-chip clock grid with 64 tunable sector trees driven by symmetric H-trees, tuned by a patented algorithm over more than 2000 tunable transmission lines.",
  "alternatives_or_rejected": "Reject (or forgo) purely symmetric H-trees, which were desired but had to be replaced by more complex tree structures due to silicon and wiring blockages.",
  "rationale": "Tunable trees driving a single grid give low skew among any of the 15200 clock pins regardless of proximity, and the grid is designed very early so designers are insulated from late grid changes.",
  "outcome": "Long-distance skews of 20-40 ps on actual chips, improved over ~70 ps skew from early test-chip channel-length variations; longer wires split into multiple-fingered transmission lines with Vdd/ground shields for inductance control.",
  "direct_quote": "While symmetric H-trees were desired, silicon and wiring blockages often forced more complex tree structures, as shown.",
  "gaps": [
    "The paper does not state the tuning algorithm's convergence time or die-area overhead.",
    "The paper does not quantify the skew contribution of the tunable trees versus the H-tree and grid segments."
  ],
  "confidence": 0.8
}
```

## Block 28 — Custom design for dataflow macros and logic synthesis for control logic [POWER4-circuit-physical-design.episodes.json ep07]

PAPER: J. D. Warnock, J. M. Keaty, J. Petrovick, J. G. Clabes, C. J. Kircher, B. L. Krauter, P. J. Restle, B. A. Zoric, C. J. Anderson, "The circuit and physical design of the POWER4 microprocessor," IBM Journal of Research and Development, vol. 46, no. 1, pp. 27-52, January 2002.

```json
{
  "title": "Custom design for dataflow macros and logic synthesis for control logic",
  "section_or_page_locator": "Circuit design (===PAGE 7===)",
  "decision": "Use custom design techniques for most dataflow macros and logic synthesis for most control logic, matching early cycle-time feasibility studies.",
  "alternatives_or_rejected": "Reject a uniform design approach; the alternative (using synthesized control flow or full-custom everywhere) is left implicit in the decision to split methodologies by macro type.",
  "rationale": "Ongoing cycle-time target set early; critical timing paths simulated in detail to verify feasibility and structure the pipeline for maximum performance, then circuit design aimed to match those early studies.",
  "outcome": "Most critical dataflow designs used full-custom techniques with optimal area/wire usage; control logic implemented as synthesized RLMs with a wide-option standard-cell library that allowed timing closure to be deferred late.",
  "direct_quote": "with custom design techniques for most of the dataﬂow macros and logic synthesis for most of the control logic",
  "gaps": [
    "The paper does not state the proportion of custom versus synthesized macros at the transistor count level (it lists macro counts: 442 custom vs. 523 RLM).",
    "The paper does not state the development-time difference between the custom and synthesized design approaches.",
    "The direct_quote preserves the source ligature dataﬂow (U+FB02) and CRLF line breaks verbatim; the prior stored text had normalized them to ASCII data flow on one line."
  ],
  "confidence": 0.8
}
```

## Block 29 — Pervasive RAS: transform checkstops into synchronous machine interrupts instead of relying on reliable parts plus ECC [POWER4-d2true.episodes.json ep00]

PAPER: J. M. Tendler, J. S. Dodson, J. S. Fields, Jr., H. Le, B. Sinharoy, "POWER4 system microarchitecture," IBM Journal of Research and Development, vol. 46, no. 1, pp. 5-25, January 2002.

```json
{
  "title": "Pervasive RAS: transform checkstops into synchronous machine interrupts instead of relying on reliable parts plus ECC",
  "section_or_page_locator": "p.2, Guiding principles / Leadership in RAS",
  "decision": "Require a RAS approach that eliminates outages and provides redundancy where errors cannot be eliminated, working to transform hard machine stops (checkstops) into synchronous machine interrupts to software, rather than relying only on choosing reliable parts and ECC logic in major arrays.",
  "alternatives_or_rejected": "Achieving high reliability only by choosing reliable parts and incorporating error-correction-code (ECC) logic into major arrays; the paper states one does not achieve high levels of reliability that way alone.",
  "rationale": "Servers had evolved toward continuous operation, and the team had already begun designing in RAS attributes previously seen only in mainframe systems; converting checkstops into software-visible synchronous interrupts lets the system circumvent problems where possible.",
  "outcome": "Mainframe-class RAS attributes designed into POWER4 systems; the complete RAS treatment is deferred to the companion paper by Bossen et al.",
  "direct_quote": "machine stops (checkstops) into synchronous machine interrupts to software",
  "gaps": [
    "The paper defers the complete RAS discussion to the companion paper by Bossen et al. and does not quantify outage-elimination coverage here.",
    "The paper does not state which specific error classes convert to synchronous interrupts versus remaining hard stops."
  ],
  "confidence": 0.95
}
```

## Block 30 — Full-system co-design: design processor, memory, I/O and packaging together up front [POWER4-d2true.episodes.json ep01]

PAPER: J. M. Tendler, J. S. Dodson, J. S. Fields, Jr., H. Le, B. Sinharoy, "POWER4 system microarchitecture," IBM Journal of Research and Development, vol. 46, no. 1, pp. 5-25, January 2002.

```json
{
  "title": "Full-system co-design: design processor, memory, I/O and packaging together up front",
  "section_or_page_locator": "p.2, Guiding principles / Full-system design approach",
  "decision": "Begin with the full design in mind up front and design the entire system together, process technology, packaging, microarchitecture, processor, memory and I/O bridge chips, so software can exploit them.",
  "alternatives_or_rejected": "Designing the processor in isolation against an existing subsystem; the paper states a new high-performance processor needs a new subsystem to feed it effectively.",
  "rationale": "To optimize the system rather than the chip alone; the co-designed marriage of process, packaging and microarchitecture is what software exploits, and the processor must fit effectively in that environment.",
  "outcome": "Processor, memory and I/O bridge chips designed together as one system, with the processor fitted to the co-designed environment built to feed it.",
  "direct_quote": "we began with the full design in mind up front",
  "gaps": [
    "The paper does not quantify the performance cost of a chip-only alternative or name a prior program that took it.",
    "The paper does not enumerate which process or packaging parameters were fixed first in the co-design sequence."
  ],
  "confidence": 0.95
}
```

## Block 31 — SMP-throughput optimization as the organizing principle: spend transistors on total system performance [POWER4-d2true.episodes.json ep02]

PAPER: J. M. Tendler, J. S. Dodson, J. S. Fields, Jr., H. Le, B. Sinharoy, "POWER4 system microarchitecture," IBM Journal of Research and Development, vol. 46, no. 1, pp. 5-25, January 2002.

```json
{
  "title": "SMP-throughput optimization as the organizing principle: spend transistors on total system performance",
  "section_or_page_locator": "p.2, Guiding principles / SMP optimization",
  "decision": "Optimize the server for SMP operation, spending a large number of transistors to improve total system performance for high-throughput multitasking environments where servers process disparate information with multiple processes concurrently.",
  "alternatives_or_rejected": "No explicitly rejected alternative is stated in the paper: the SMP-optimization principle and its workload rationale are given, but no single-thread-first or uniprocessor-first counter-option is discussed. Recorded as absent, not inferred.",
  "rationale": "Servers by nature process disparate information with multiple processes active concurrently, so transistor spend buys the most total performance in SMP throughput.",
  "outcome": "SMP-first direction set for the program, realized as a dual-processor chip scaling through the distributed-switch hierarchy to 8-way modules and 32-way SMPs.",
  "direct_quote": "be optimized for SMP operation, in which a large number of transistors can be used to improve total",
  "gaps": [
    "No explicitly rejected alternative is stated in the paper; the single-thread-first counter-direction is not discussed.",
    "The paper does not give a transistor budget split between SMP-throughput structures and single-thread performance."
  ],
  "confidence": 0.95
}
```

## Block 32 — Absolute binary-compatibility requirement after task forces found no technical impediment to scaling PowerPC [POWER4-d2true.episodes.json ep03]

PAPER: J. M. Tendler, J. S. Dodson, J. S. Fields, Jr., H. Le, B. Sinharoy, "POWER4 system microarchitecture," IBM Journal of Research and Development, vol. 46, no. 1, pp. 5-25, January 2002.

```json
{
  "title": "Absolute binary-compatibility requirement after task forces found no technical impediment to scaling PowerPC",
  "section_or_page_locator": "p.2, Guiding principles / Binary compatibility",
  "decision": "Accept the absolute requirement of maintaining binary compatibility for 32-bit and 64-bit applications with prior PowerPC and PowerPC AS systems, keeping customers' software investment intact.",
  "alternatives_or_rejected": "Changing the architecture and breaking compatibility; the task forces had concluded PowerPC had no technical impediments to scaling to significantly higher frequencies with excellent performance, leaving no technical reason to change.",
  "rationale": "The task-force conclusion meant compatibility could be kept at no technical cost, and keeping it protected customer software investment.",
  "outcome": "Compatibility locked as an absolute requirement for 32-bit and 64-bit applications with prior PowerPC and PowerPC AS systems.",
  "direct_quote": "absolute requirement of maintaining binary compatibility",
  "gaps": [
    "The paper does not detail the task forces' frequency-scaling evidence beyond the stated conclusion.",
    "The paper does not quantify any performance cost paid for maintaining compatibility."
  ],
  "confidence": 0.93
}
```

## Block 33 — Distributed-switch interconnect for chip-to-system SMP scaling (8-way module, 32-way system) [POWER4-d2true.episodes.json ep04]

PAPER: J. M. Tendler, J. S. Dodson, J. S. Fields, Jr., H. Le, B. Sinharoy, "POWER4 system microarchitecture," IBM Journal of Research and Development, vol. 46, no. 1, pp. 5-25, January 2002.

```json
{
  "title": "Distributed-switch interconnect for chip-to-system SMP scaling (8-way module, 32-way system)",
  "section_or_page_locator": "p.2, Overview / distributed switch; p.3, POWER4 chip / eight-way and 32-way SMP",
  "decision": "Interconnect POWER4 chips with a distributed-switch topology to form symmetric multiprocessors of any size up to a 32-way SMP.",
  "alternatives_or_rejected": "No explicitly rejected interconnect alternative is stated in the paper: the topology is called new to the industry, but no centralized-bus counter-option is discussed. Recorded as absent, not inferred.",
  "rationale": "POWER4 is an architecture within which a set of chips are designed together to realize a system, and the interconnect is the structure that turns chips into SMPs of any size up to 32-way.",
  "outcome": "Four POWER4 chips package on a single module as an eight-way SMP and four such modules interconnect as a 32-way SMP, each chip carrying five primary interfaces.",
  "direct_quote": "referred to as a distributed switch, is new to the industry.",
  "gaps": [
    "No rejected interconnect alternative is stated; prior IBM interconnect practice is not contrasted.",
    "The paper does not quantify the switch's latency or bandwidth advantage over any alternative."
  ],
  "confidence": 0.9
}
```

## Block 34 — Large shared on-chip L2 (about 1.5 MB, eight-way) serving both cores through the CIU crossbar [POWER4-d2true.episodes.json ep05]

PAPER: J. M. Tendler, J. S. Dodson, J. S. Fields, Jr., H. Le, B. Sinharoy, "POWER4 system microarchitecture," IBM Journal of Research and Development, vol. 46, no. 1, pp. 5-25, January 2002.

```json
{
  "title": "Large shared on-chip L2 (about 1.5 MB, eight-way) serving both cores through the CIU crossbar",
  "section_or_page_locator": "p.11, Storage hierarchy / Table 3 (L2 capacity); p.2, POWER4 chip / shared unified L2 via CIU",
  "decision": "Implement the second-level cache as a unified about-1.5 MB eight-way set-associative cache with 128-byte lines, shared by both on-chip processors through the CIU crossbar's three autonomous L2 controllers.",
  "alternatives_or_rejected": "No explicitly rejected cache organization is stated in the paper: the shared unified L2 is described, but no per-core private-L2 counter-option is discussed. Recorded as absent, not inferred.",
  "rationale": "Both processors share one unified L2 through the CIU, whose three controllers operate concurrently and feed 32 bytes of data per cycle, keeping both cores fed from a single coherent level.",
  "outcome": "Shared L2 realized per the storage-hierarchy table (eight-way, 128-byte line, about 1.5 MB per chip) with ECC-protected data arrays, redundant directory arrays, and CIU crossbar access from either core.",
  "direct_quote": "Eight-way, 128-byte line \u00011.5 MB",
  "gaps": [
    "The capacity cell carries a leading \\x01 control character in the extracted text (extraction artifact, preserved verbatim).",
    "No rejected cache organization is stated; per-core private L2s are not discussed.",
    "The paper does not quantify the sharing benefit (hit-rate or traffic) versus a split design."
  ],
  "confidence": 0.95
}
```

## Block 35 — Embrace the speed-demon (high-frequency) design path [POWER4-system-microarchitecture.episodes.json ep00]

PAPER: J. M. Tendler, J. S. Dodson, J. S. Fields, Jr., H. Le, B. Sinharoy, "POWER4 system microarchitecture," IBM Journal of Research and Development, vol. 46, no. 1, pp. 5-25, January 2002.

```json
{
  "title": "Embrace the speed-demon (high-frequency) design path",
  "section_or_page_locator": "p.1, Introduction / speed demons vs. braniacs",
  "decision": "The POWER4 design adopted the speed-demon (high clock-rate) approach while remaining in the braniac camp on instructions-per-cycle, delivering initial processor frequencies of 1.1 GHz and 1.3 GHz.",
  "alternatives_or_rejected": "The alternative - remaining purely in the traditional IBM 'braniac' camp (more complex design but a higher instructions-per-cycle rate), which IBM UNIX-based systems had historically favoured - was not chosen but was retained as a joint influence (emphasize high IPC while also pursuing high frequency).",
  "rationale": "After the ongoing 'speed demons' vs. 'braniacs' debate in which IBM UNIX systems had traditionally been in the braniac camp, 'With the POWER4, IBM opted to also embrace the speed-demon approach' in order to maintain a leadership position on operating frequency while still delivering balanced performance across workloads.",
  "outcome": "The POWER4 design was initially introduced at processor frequencies of 1.1 GHz and 1.3 GHz, surpassing all other 64-bit microprocessors in some key performance benchmarks, while the design still also addressed commercial and technical requirements.",
  "direct_quote": "opted to also embrace the speed-demon approach.",
  "gaps": [
    "The paper does not state which specific alternatives were formally rejected or the comparative IPC or other performance data for the braniac-only option.",
    "The paper does not quantify the frequency gain or IPC trade-off target used to select this approach."
  ],
  "confidence": 0.7
}
```

## Block 36 — Maintain binary compatibility with prior PowerPC systems [POWER4-system-microarchitecture.episodes.json ep01]

PAPER: J. M. Tendler, J. S. Dodson, J. S. Fields, Jr., H. Le, B. Sinharoy, "POWER4 system microarchitecture," IBM Journal of Research and Development, vol. 46, no. 1, pp. 5-25, January 2002.

```json
{
  "title": "Maintain binary compatibility with prior PowerPC systems",
  "section_or_page_locator": "p.2, Guiding principles: binary compatibility",
  "decision": "The design accepted an absolute requirement of maintaining binary compatibility for both 32-bit and 64-bit applications with prior PowerPC and PowerPC AS systems.",
  "alternatives_or_rejected": "The implied alternative - changing the architecture or scaling in a way that would break existing binaries - was rejected because the task forces found no technical reason to change.",
  "rationale": "Internal IBM task forces in the first half of the 1990s concluded that the PowerPC Architecture had no technical impediments to scaling to significantly higher frequencies with excellent performance. With no technical reason to change, the team kept customers' software investment intact, so binary compatibility was required.",
  "outcome": "The design preserved binary compatibility for both 32-bit and 64-bit applications with prior PowerPC and PowerPC AS systems, and the paper later notes software-override/reserved-bit techniques were chosen partly to keep 100% binary compatibility.",
  "direct_quote": "absolute requirement of maintaining binary compatibility",
  "gaps": [
    "The paper lists this as a guiding acceptance rather than an active decision with formal rejected alternatives.",
    "The paper does not quantify the customer software-critical work or the cost that a break would have imposed."
  ],
  "confidence": 0.8
}
```

## Block 37 — Single-port I-cache to save area rather than multi-port it [POWER4-system-microarchitecture.episodes.json ep02]

PAPER: J. M. Tendler, J. S. Dodson, J. S. Fields, Jr., H. Le, B. Sinharoy, "POWER4 system microarchitecture," IBM Journal of Research and Development, vol. 46, no. 1, pp. 5-25, January 2002.

```json
{
  "title": "Single-port I-cache to save area rather than multi-port it",
  "section_or_page_locator": "p.6, Instruction fetch (I-cache)",
  "decision": "The L1 instruction cache was designed with a single port that reads or writes one 32-byte sector per cycle, rather than a more ported design, while still fetching up to eight instructions per cycle.",
  "alternatives_or_rejected": "The rejected alternative was a more heavily ported instruction cache that could serve more concurrent accesses; it was avoided because I-cache misses are infrequent.",
  "rationale": "Since I-cache misses are infrequent, the design accepted a single port to save area, writing returned lines during cycles when instruction fetching is not using the I-cache so writes are hidden.",
  "outcome": "The I-cache fetches up to eight instructions per cycle and is single-ported; critical-sector instructions are forwarded promptly and the cache line is written into the instruction-prefetch buffer on a miss.",
  "direct_quote": "to save area, the I-cache has been designed to",
  "gaps": [
    "The paper does not state how much area a single-port choice actually saved versus a ported design.",
    "The paper does not discuss a performance penalty trade-off estimate for limiting to one port."
  ],
  "confidence": 0.8
}
```

## Block 38 — Track machine state at group boundaries, not per-instruction [POWER4-system-microarchitecture.episodes.json ep03]

PAPER: J. M. Tendler, J. S. Dodson, J. S. Fields, Jr., H. Le, B. Sinharoy, "POWER4 system microarchitecture," IBM Journal of Research and Development, vol. 46, no. 1, pp. 5-25, January 2002.

```json
{
  "title": "Track machine state at group boundaries, not per-instruction",
  "section_or_page_locator": "p.7, Decode, crack, and group formation",
  "decision": "Machine state is preserved and tracked at group boundaries rather than at individual instruction boundaries within a group; any exception restores the machine to the state of the oldest group prior to the exception.",
  "alternatives_or_rejected": "The rejected alternative was tracking state at individual instruction boundaries within an instruction group, which would require more logic to remember program order across the large number of in-flight instructions.",
  "rationale": "To minimize the logic necessary to track a large number of in-flight instructions, groups of instructions are formed and tracked; state is preserved at group boundaries, not at an instruction boundary within a group.",
  "outcome": "Groups of up to five internal instructions (IOPs) are formed, only one group is dispatched and completed per cycle, and exceptions/in-service events are handled by flushing and redispatching groups.",
  "direct_quote": "group boundaries, not at an instruction boundary within a",
  "gaps": [
    "The paper does not quantify the logic-area or tracking cost saved versus per-instruction tracking.",
    "The paper does not state a performance cost of restoring to the older group boundary instead of the exact faulting instruction."
  ],
  "confidence": 0.85
}
```

## Block 39 — Limit each instruction to two read registers and one write register [POWER4-system-microarchitecture.episodes.json ep04]

PAPER: J. M. Tendler, J. S. Dodson, J. S. Fields, Jr., H. Le, B. Sinharoy, "POWER4 system microarchitecture," IBM Journal of Research and Development, vol. 46, no. 1, pp. 5-25, January 2002.

```json
{
  "title": "Limit each instruction to two read registers and one write register",
  "section_or_page_locator": "p.7, Decode, crack, and group formation",
  "decision": "Internal instructions are limited to reading at most two registers and writing at most one register, and any architected instruction violating this is split (cracked or millicoded) into IOPs to satisfy the rule.",
  "alternatives_or_rejected": "The rejected alternative was allowing instructions to read/write an unrestricted number of registers, which would have been harder to sustain at high frequency. A limited exception was allowed for performance: fused multiply-and-add instructions are handled directly in the FP unit though they require three sources.",
  "rationale": "To achieve high-frequency operation, instructions were limited to reading at most two registers and writing at most one register, so that otherwise non-conforming instructions are split.",
  "outcome": "Instructions such as 'load with update' are cracked into a load and an add, and 'load multiple word' is implemented with multiple load word instructions; cracked IOPs must stay in the same group and millicoded instructions always begin a new group.",
  "direct_quote": "at most two registers and write at most one register.",
  "gaps": [
    "The paper does not state how much frequency was gained by this restriction.",
    "The paper does not state the performance cost of cracking/millicode beyond noting such instructions begin new groups."
  ],
  "confidence": 0.85
}
```

## Block 40 — L3 sources S-state data only to its own L2s to cut cross-module traffic [POWER4-system-microarchitecture.episodes.json ep05]

PAPER: J. M. Tendler, J. S. Dodson, J. S. Fields, Jr., H. Le, B. Sinharoy, "POWER4 system microarchitecture," IBM Journal of Research and Development, vol. 46, no. 1, pp. 5-25, January 2002.

```json
{
  "title": "L3 sources S-state data only to its own L2s to cut cross-module traffic",
  "section_or_page_locator": "p.15, L3 cache coherency states",
  "decision": "When an L3 line is in the S (shared) state, the L3 sources data only to its own L2s, whereas in the T/Trem states it sources to any requestor in the system.",
  "alternatives_or_rejected": "The alternative - allowing an S-state L3 to source its data to requestors on other processor modules - was avoided because it would increase inter-module data traffic.",
  "rationale": "This minimizes data traffic on the buses between processor modules, since, whenever possible, data is sourced by an L3 cache on the requesting processor module.",
  "outcome": "Data in the S state is not sourced to remote modules, reducing bus traffic; T/Trem and O states source data under the 'no other cache is sourcing and no snooper retried' rules.",
  "direct_quote": "the L3 will source data only to its own L2s.",
  "gaps": [
    "The paper does not quantify the bus-traffic or latency reduction achieved by this constraint.",
    "The paper does not state the latency consequence for a remote S-state request that is instead satisfied elsewhere."
  ],
  "confidence": 0.8
}
```

## Block 41 — Classify cached data as T vs. Trem to skip memory address-range decode [POWER4-system-microarchitecture.episodes.json ep06]

PAPER: J. M. Tendler, J. S. Dodson, J. S. Fields, Jr., H. Le, B. Sinharoy, "POWER4 system microarchitecture," IBM Journal of Research and Development, vol. 46, no. 1, pp. 5-25, January 2002.

```json
{
  "title": "Classify cached data as T vs. Trem to skip memory address-range decode",
  "section_or_page_locator": "p.15, L3 cache coherency states",
  "decision": "The L3 distinguishes 'tagged' (T) from 'remote tagged' (Trem) states so it can determine whether a cast-out goes to its attached memory controller or must be issued as a fabric bus transaction.",
  "alternatives_or_rejected": "The rejected alternative was performing a memory address-range decode at cast-out time; this design avoids that decode, at the cost of performing the decode at snoop time instead.",
  "rationale": "This design point was chosen to avoid the need for a memory address-range decode when the L3 performs a cast-out operation, because the T/Trem distinction reveals whether the data can be written to the attached memory controller or must be issued as a fabric bus transaction.",
  "outcome": "The L3 can write T-state data to its attached memory controller while Trem-state data is issued as a fabric bus transaction; an address decode is done at snoop time to choose the state.",
  "direct_quote": "need for a memory address-range decode when the L3",
  "gaps": [
    "The paper does not state the performance or logic cost of doing the decode at snoop time instead of cast-out time.",
    "The paper does not describe the exact latency of the snoop-time decode versus a cast-out-time decode."
  ],
  "confidence": 0.8
}
```

## Block 42 — Prefetch the fifth cache line instead of the second in each stream [POWER4-system-microarchitecture.episodes.json ep07]

PAPER: J. M. Tendler, J. S. Dodson, J. S. Fields, Jr., H. Le, B. Sinharoy, "POWER4 system microarchitecture," IBM Journal of Research and Development, vol. 46, no. 1, pp. 5-25, January 2002.

```json
{
  "title": "Prefetch the fifth cache line instead of the second in each stream",
  "section_or_page_locator": "p.16, Hardware data prefetch",
  "decision": "When a sequential prefetch stream stages a line from the L3 into the L2, the hardware prefetches the fifth cache line rather than the second line.",
  "alternatives_or_rejected": "The alternative - prefetching the second cache line - was rejected because it does not account for the longer L2-from-L3 latency relative to the L1-from-L2 latency.",
  "rationale": "Since the latency to load the L2 from the L3 is longer than the latency to load the L1 from the L2, rather than prefetch the second cache line, the fifth is prefetched, while prior references have already staged the second through fourth lines from the L2 to the L1 data cache.",
  "outcome": "Under sequential stream detection, the prefetch engine stages one line into the L1 from the L2 and simultaneously requests the L3 to stage a line into the L2; a 512-byte line is prefetched from memory into the L3 every fourth line referenced.",
  "direct_quote": "from the L2, rather than prefetch the second cache line,",
  "gaps": [
    "The paper does not state the actual cycle counts for L1-from-L2 versus L2-from-L3 latency, so the rationale cannot be precisely quantified.",
    "The paper does not state whether the offset 'fifth' was empirically tuned or analytically derived."
  ],
  "confidence": 0.8
}
```
