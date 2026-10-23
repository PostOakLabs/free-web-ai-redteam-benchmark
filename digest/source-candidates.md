# Source Candidates — every source ever claimed, deduplicated

> ### ⚠ Concurrency correction (written 14:50, after the deliverables above were drafted)
>
> A **parallel session was working the same material while this digest was being written.** Between
> 14:30 and 14:44 it produced two artefacts at the ASIC root that did not exist when this digest's
> corpus survey ran at 14:15:
>
> - **`../VERIFIED-SOURCES.md`** — the verification sweep LOG-RUN3 called for. All five consensus
>   sources acquired with verified citations and public URLs (bitsavers IBM JRD mirror, ETH course
>   mirrors, the openly-archived Intel Technology Journal); 7 multi-claimed titles all VERIFIED;
>   49 singletons at conf ≥0.8 checked and split VERIFIED / UNCERTAIN / NOT-FOUND.
> - **`../extractions/*.episodes.json`** — locator-cited extractions from **all five** PDFs:
>   36 episodes carrying `section_or_page_locator`, `direct_quote`, and **non-empty `gaps`** on
>   every entry (POWER4-circuit-physical 8, POWER4-microarch 8, Alpha 21264 7, Pentium 4 7,
>   Niagara 6).
>
> **Statements in this file that are now superseded:** anything describing the source PDFs as
> unmined, the verification sweep as pending, or locator-cited extraction as the next unstarted
> action. Those were true at 14:15 and are not true now. The findings that came from *reading* the
> POWER4 paper stand — including the third clock-philosophy inversion, which the parallel session's
> own extraction independently corroborates: its first POWER4-microarch episode is titled
> *"Embrace the speed-demon (high-frequency) design path"*.
>
> Corrected next actions are in `DIGEST-REPORT.md` §5.

**Status: model claims, not a bibliography.** A title in this list is an assertion by a model that a
paper exists as named. Most have not been checked. Do not cite anything from here without
verification; a plausible title in a real venue is the easiest thing for a model to produce and the
hardest to spot.

**Corpus:** Prompt D1 genre maps (15 files, 143 entries) + one URL-cited source recovered from a Prompt J red-team review (see Tier A++) + Prompt C outputs folded into run-2 A files
(9 entries) + the D2 file where gemini answered the wrong task and produced a genre map (10 entries)
+ stray source mentions in episode `source_basis` fields (zero — no episode ever claimed a named
source). **112 unique normalized titles from 152 claims.**

---

## 1. The five consensus sources are now all on disk

This is the material change since LOG-RUN3. The master's local-session queue says *"only
POWER4-microarch is in `sources/` so far; my mirror guesses for Alpha 21264 / Pentium 4 ITJ /
Niagara / POWER4-circuit-physical all failed."* That entry is **stale**. `../sources/` currently
holds five PDFs, covering the entire consensus five:

| File | Size | Mined? |
|---|---|---|
| `POWER4-system-microarchitecture-IBMJRD-46-1-2002.pdf` | 431 KB, 21 pp. | **Yes** — text extracted and used in this digest to verify/falsify 13 D2 recall claims (`episode-draft-bank.md` §3) |
| `POWER4-circuit-physical-design-IBMJRD-46-1-2002.pdf` | 1.5 MB | No — **the richest extraction target in the project and it is sitting unread** |
| `Alpha21264-microprocessor-IEEEMicro-1999.pdf` | 1.2 MB | No |
| `Pentium4-microarchitecture-IntelTechJournal-2001.pdf` | 224 KB | No |
| `Niagara-32way-multithreaded-SPARC-IEEEMicro-2005.pdf` | 126 KB | No |

**Consequence for the pipeline.** The bottleneck the run-3 log identified — "source-text acquisition
+ the expert's review time" — is now half resolved, and the half that resolved is the half an agent can
act on. Prompt D's Task 2 (locator-cited extraction, `gaps` non-empty) has been waiting for source
text since it was written; the source text is here. See `MISSED.md` §5.2.

**Verification note on the Alpha entry.** Five models claimed "The Alpha 21264 Microprocessor" and
disagreed about it: three said IEEE Micro 1999, two said IEEE JSSC 1998. The held PDF is the IEEE
Micro 1999 one (Kessler), matching LOG-RUN3's prior. The JSSC-1998 claimants were describing a
different, also-real paper (Gronowski et al., "High-performance microprocessor design", JSSC 33(5)
1998) — so this is two real papers collapsed into one title by normalization, not an error by the
models. Worth remembering when reading the counts below: **a high claim count can mean consensus, or
it can mean several distinct papers wearing one name.**

---

## 2. Full deduplicated list

Sorted by claim count then max confidence. `claims` = number of distinct models asserting the title.
`max conf` = highest self-rated confidence any model attached. Everything not marked **HELD** is
**UNVERIFIED** — no title below was checked against dblp, ACM DL or a publisher page in this session.


| claims | max conf | title | venue · year | claimed by | status |
|---|---|---|---|---|---|
| 13 | 1.0 | POWER4 system microarchitecture | IBM Journal of Research and Development · 2002 | deepseek, gemini, glm 5.3, meta, mimo, minimax 2.7, minimax 3, mis | **HELD** `sources/POWER4-system-microarchitecture-IBMJRD-46-1-2002.pdf` — content verified against text in this digest |
| 8 | 1.0 | The circuit and physical design of the POWER4 microprocessor | IBM Journal of Research and Development · 2002 | deepseek, glm 5.3, mimo, minimax 2.7, minimax 3, nemotron, solar p | **HELD** `sources/POWER4-circuit-physical-design-IBMJRD-46-1-2002.pdf` — acquired, not yet mined |
| 5 | 0.95 | The Alpha 21264 Microprocessor | IEEE Journal of Solid-State Circuits · 1998 | deepseek, glm 5.3, mimo, mistral, nemotron | **HELD** `sources/Alpha21264-microprocessor-IEEEMicro-1999.pdf` — acquired, not yet mined |
| 3 | 1.0 | The microarchitecture of the Pentium 4 processor | Intel Technology Journal · 2001 | glm 5.3, meta, opus 5 | **HELD** `sources/Pentium4-microarchitecture-IntelTechJournal-2001.pdf` — acquired, not yet mined |
| 3 | 0.9 | Niagara: A 32-Way Multithreaded Sparc Processor | IEEE Micro · 2005 | glm 5.3, opus 5, qwen | **HELD** `sources/Niagara-32way-multithreaded-SPARC-IEEEMicro-2005.pdf` — acquired, not yet mined |
| 3 | 0.85 | Circuit and physical design of the POWER5 microprocessor | IBM Journal of Research and Development · 2004 | mistral, nemotron, qwen | UNVERIFIED |
| 2 | 1.0 | A 200 MHz 64-b Dual-Issue CMOS Microprocessor | IEEE Journal of Solid-State Circuits · 1992 | gemini, mimo | UNVERIFIED |
| 2 | 1.0 | Functional verification of the POWER4 microprocessor and POWER4 multiprocessor systems | IBM Journal of Research and Development · 2002 | meta, yunbao | UNVERIFIED |
| 2 | 1.0 | High-performance microprocessor design | IEEE Journal of Solid-State Circuits · 1998 | meta, opus 5 | UNVERIFIED |
| 2 | 0.97 | POWER5 system microarchitecture | IBM Journal of Research and Development · 2005 | deepseek, meta | UNVERIFIED |
| 2 | 0.95 | Physical Design of a Fourth-Generation POWER GHz Microprocessor | IEEE International Solid-State Circuits Conference · 2001 | meta, yunbao | UNVERIFIED |
| 2 | 0.9 | Itanium 2 processor microarchitecture | IEEE Micro · 2003 | glm 5.3, nemotron | UNVERIFIED |
| 2 | 0.9 | The circuit and physical design of the POWER6 microprocessor | IBM Journal of Research and Development · 2008 | minimax 2.7, mistral | UNVERIFIED |
| 2 | 0.9 | Itanium Processor Microarchitecture | IEEE Micro · 2000 | minimax 3, mistral | UNVERIFIED |
| 2 | 0.85 | Static Timing Analysis for Nanometer Designs: A Practical Approach | Springer (book) · 2009 | minimax 3, opus 5 | UNVERIFIED |
| 2 | 0.8 | Cell Broadband Engine Processor | IBM Journal of Research and Development · 2005 | mimo, mistral | UNVERIFIED |
| 1 | 1.0 | Design and implementation of the POWER5 microprocessor | Design Automation Conference (DAC) · 2004 | gemini | UNVERIFIED |
| 1 | 1.0 | Fault-tolerant design of the IBM pSeries 690 system using POWER4 processor technology | IBM Journal of Research and Development · 2002 | yunbao | UNVERIFIED |
| 1 | 1.0 | Infrastructure requirements for a large-scale, multi-site VLSI development project | IBM Journal of Research and Development · 2002 | yunbao | UNVERIFIED |
| 1 | 0.95 | A 600MHz superscalar RISC microprocessor | IEEE Journal of Solid-State Circuits · 1997 | gemini | UNVERIFIED |
| 1 | 0.95 | Circuit design methodology for a 4.5 GHz 32-nm dual-core zEnterprise microprocessor | IBM Journal of Research and Development · 2011 | gemini | UNVERIFIED |
| 1 | 0.95 | Circuit design and implementation techniques for a 1GHz Itanium microprocessor | IEEE Journal of Solid-State Circuits · 2000 | gemini | UNVERIFIED |
| 1 | 0.95 | The circuit design of the POWER6 microprocessor | IEEE International Solid-State Circuits Conference · 2007 | gemini | UNVERIFIED |
| 1 | 0.95 | A 1 GHz Alpha microprocessor | IEEE Journal of Solid-State Circuits · 1998 | gemini | UNVERIFIED |
| 1 | 0.95 | A 1.0 GHz PowerPC microprocessor with copper interconnect | ISSCC · 1999 | nemotron | UNVERIFIED |
| 1 | 0.95 | The Soul of a New Machine | Little, Brown (book); Pulitzer Prize for General N · 1981 | opus 5 | UNVERIFIED |
| 1 | 0.94 | Design closure lessons from the IBM POWER4 microprocessor | IBM Journal of Research and Development · 2002 | chatgpt | UNVERIFIED |
| 1 | 0.92 | Power considerations in the design of the Alpha 21264 microprocessor | DAC · 1998 | meta | **HELD** `sources/Alpha21264-microprocessor-IEEEMicro-1999.pdf` — acquired, not yet mined |
| 1 | 0.9 | UltraSPARC-I: A 64-bit UltraSPARC processor for technical computing | IEEE Micro · 1995 | gemini | UNVERIFIED |
| 1 | 0.9 | Design and implementation of the AMD-K6 microprocessor | IEEE Micro · 1997 | gemini | UNVERIFIED |
| 1 | 0.9 | Design and microarchitecture of the IBM System z10 microprocessor | IBM Journal of Research and Development · 2009 | meta | UNVERIFIED |
| 1 | 0.9 | The Implementation of the Pentium 4 Processor | IEEE Journal of Solid-State Circuits · 2000 | mistral | UNVERIFIED |
| 1 | 0.9 | Circuit implementation of a 64-bit second-generation CMOS PowerPC microprocessor | ISSCC · 1995 | nemotron | UNVERIFIED |
| 1 | 0.9 | A 0.18 µm 1.5 GHz 64-bit PowerPC microprocessor | ISSCC · 2001 | nemotron | UNVERIFIED |
| 1 | 0.9 | A 32nm 3.1 GHz 8-core x86 processor | ISSCC · 2011 | nemotron | UNVERIFIED |
| 1 | 0.9 | The design and implementation of the RIOS (POWER1) processor | IBM Journal of Research and Development · 1990 | nemotron | UNVERIFIED |
| 1 | 0.9 | A 45nm 2.3 GHz 8-core PowerPC processor | ISSCC · 2008 | nemotron | UNVERIFIED |
| 1 | 0.9 | A 22nm 3.6 GHz 8-core Xeon processor | ISSCC · 2013 | nemotron | UNVERIFIED |
| 1 | 0.9 | The Circuit and Physical Design of the POWER7 Microprocessor | IBM Journal of Research and Development · 2011 | qwen | UNVERIFIED |
| 1 | 0.9 | Design Methodology for the S/390 Parallel Enterprise Server G4 Microprocessors | IBM Journal of Research and Development · 1997 | yunbao | UNVERIFIED |
| 1 | 0.9 | The Implementation of the IBM z10 Microprocessor | IBM Journal of Research and Development · 2008 | chatgpt | UNVERIFIED |
| 1 | 0.9 | ISSCC / VLSI Symposium chip-design session papers describing physical-implementation challen | IEEE International Solid-State Circuits Conference · annual, 1954-present | opus | UNVERIFIED |
| 1 | 0.88 | The zEnterprise 196 System and Microprocessor | IEEE Micro · 2011 | meta | UNVERIFIED |
| 1 | 0.88 | The design methodology of the VA Linux 64-bit server microprocessor | IEEE Journal of Solid-State Circuits (JSSC), Vol.  · 2002 | minimax 2.7 | UNVERIFIED |
| 1 | 0.85 | Implementation of an 8-core, 64-thread, power-efficient SPARC server on a chip | IEEE Journal of Solid-State Circuits · 2008 | meta | UNVERIFIED |
| 1 | 0.85 | The UltraSPARC-I Microprocessor | IEEE Journal of Solid-State Circuits · 1996 | mistral | UNVERIFIED |
| 1 | 0.85 | The SPARC64 VIIIfx processor | ISSCC · 2010 | nemotron | UNVERIFIED |
| 1 | 0.85 | A 65nm 1.6 GHz SPARC64 VII processor | ISSCC · 2008 | nemotron | UNVERIFIED |
| 1 | 0.85 | z10 microprocessor design | IBM Journal of Research and Development · 2009 | nemotron | UNVERIFIED |
| 1 | 0.85 | A 200MHz 64b dual-issue CMOS microprocessor | IEEE Journal of Solid-State Circuits, Vol. 27, No. · 1992 | opus 5 | UNVERIFIED |
| 1 | 0.85 | Physical design of the IBM zEnterprise 196 microprocessor | IBM Journal of Research and Development · 2012 | qwen | UNVERIFIED |
| 1 | 0.85 | Circuit Design of the Pentium 4 Microprocessor | IEEE International Solid-State Circuits Conference · 2000 | qwen | UNVERIFIED |
| 1 | 0.85 | Physical Design of the Intel Itanium Microprocessor | IEEE International Solid-State Circuits Conference · 2000 | qwen | UNVERIFIED |
| 1 | 0.85 | A Clock Distribution Method for Microprocessors | IEEE Journal of Solid-State Circuits · 2001 | yunbao | UNVERIFIED |
| 1 | 0.85 | ISPD (International Symposium on Physical Design) contest reports and invited industry talks | ACM International Symposium on Physical Design · annual, 1997-present;  | opus | UNVERIFIED |
| 1 | 0.85 | OpenROAD and OpenLane / LibreLane project issue trackers and design-flow reports | GitHub (The-OpenROAD-Project and associated reposi · roughly 2019-present,  | opus | UNVERIFIED |
| 1 | 0.82 | A 0.18μm logic base technology platform for high-performance and low-power SoC applications | IBM Journal of Research and Development, Vol. 46,  · 2002 | minimax 2.7 | UNVERIFIED |
| 1 | 0.82 | Itanium 2: a 6-core 90nmitanium-family processor | IEEE International Solid-State Circuits Conference · 2005 | minimax 2.7 | UNVERIFIED |
| 1 | 0.8 | The anatomy of a high-end microprocessor: a systems perspective | IEEE Computer Society Press / book (Advances in Co · 2000 | minimax 2.7 | UNVERIFIED |
| 1 | 0.8 | Circuit and physical design of the Pentium 4 processor in 0.18μm technology | IEEE International Solid-State Circuits Conference · 2000 | minimax 2.7 | UNVERIFIED |
| 1 | 0.8 | The circuit design of the z10 microprocessor | IBM Journal of Research and Development · 2008 | mistral | UNVERIFIED |
| 1 | 0.8 | The AMD Opteron Processor: Design and Implementation | IEEE Journal of Solid-State Circuits · 2003 | mistral | UNVERIFIED |
| 1 | 0.8 | A 600-MHz 64-b Microprocessor (Alpha 21264) | IEEE International Solid-State Circuits Conference · 1998 | qwen | UNVERIFIED |
| 1 | 0.8 | A 750MHz 10th Generation SPARC Microprocessor | IEEE International Solid-State Circuits Conference · 2001 | qwen | UNVERIFIED |
| 1 | 0.8 | DAC (Design Automation Conference) Designer Track / user-track presentations | ACM/IEEE Design Automation Conference · annual; the designer/u | opus | UNVERIFIED |
| 1 | 0.78 | Physical design of a 1 GHz Alpha processor | IEEE International Solid-State Circuits Conference · 1999 | minimax 2.7 | UNVERIFIED |
| 1 | 0.75 | The 1.0 GHz Intel Itanium 2 processor | ISSCC 2003 · 2003 | deepseek | UNVERIFIED |
| 1 | 0.75 | The AMD Opteron processor | IEEE Micro · 2003 | deepseek | UNVERIFIED |
| 1 | 0.75 | Design methodology and毛片 implementation of the SPARC v9 processor | IEEE Journal of Solid-State Circuits (JSSC), Vol.  · 1996 | minimax 2.7 | UNVERIFIED |
| 1 | 0.75 | The IBM Journal of Research and Development POWER4 issue (Vol. 46, No. 1, 2002) as a whole | IBM Journal of Research and Development · 2002 | opus 5 | UNVERIFIED |
| 1 | 0.75 | A 130nm 1.5V 1GHz AMD Opteron | IEEE International Solid-State Circuits Conference · 2003 | qwen | UNVERIFIED |
| 1 | 0.75 | A Pseudo-Hierarchical Methodology for High-Performance Microprocessor Design | Proceedings of the International Symposium on Phys · 1997 | yunbao | UNVERIFIED |
| 1 | 0.7 | The design and implementation of the IBM z10 microprocessor | IBM Journal of Research and Development · 2009 | deepseek | UNVERIFIED |
| 1 | 0.7 | Circuit design of the Alpha 21264 microprocessor | ISSCC (or IEEE Journal of Solid‑State Circuits) · 1998/1999 | deepseek | **HELD** `sources/Alpha21264-microprocessor-IEEEMicro-1999.pdf` — acquired, not yet mined |
| 1 | 0.7 | UltraSPARC III: A 1‑GHz 64‑bit microprocessor | IEEE Micro · 2001 | deepseek | UNVERIFIED |
| 1 | 0.7 | A 0.18μm CMOS IA-32 Processor with a 4GHz Integer Execution Unit | IEEE International Solid-State Circuits Conference · 2001 | mimo | UNVERIFIED |
| 1 | 0.7 | Design of the Itanium 2 microprocessor | IEEE Micro · 2003 | minimax 3 | UNVERIFIED |
| 1 | 0.7 | The implementation of the Itanium 2 microprocessor | IEEE Journal of Solid-State Circuits, Vol. 37, No. · 2002 | opus 5 | UNVERIFIED |
| 1 | 0.7 | The 12-core POWER8 processor (ISSCC 2014) | IEEE Journal of Solid-State Circuits (ISSCC 2014 e · 2015 | yunbao | UNVERIFIED |
| 1 | 0.65 | The Implementation of the Next-Generation 64-Bit Itanium Microprocessor | IEEE International Solid-State Circuits Conference · 2002 | mimo | UNVERIFIED |
| 1 | 0.65 | A multigigahertz clocking scheme for the Pentium 4 microprocessor | IEEE Journal of Solid-State Circuits, Vol. 36, No. · 2001 | opus 5 | UNVERIFIED |
| 1 | 0.6 | A 600-MHz superscalar RISC microprocessor with out-of-order execution (Alpha 21264) | ISSCC Digest of Technical Papers · 1997 | glm 5.3 | UNVERIFIED |
| 1 | 0.6 | POWER6: A 4.6 GHz Microprocessor | IEEE International Solid-State Circuits Conference · 2007 | mimo | UNVERIFIED |
| 1 | 0.6 | The Implementation of the POWER7 Processor | IEEE International Solid-State Circuits Conference · 2010 | mimo | UNVERIFIED |
| 1 | 0.6 | The UltraSPARC-III Processor | IEEE International Solid-State Circuits Conference · 2000 | mimo | UNVERIFIED |
| 1 | 0.6 | The design of a high performance, low power microprocessor (StrongARM SA-110) | International Symposium on Low Power Electronics a · 1996 | opus 5 | UNVERIFIED |
| 1 | 0.6 | IBM z-Series processor implementation papers in the IBM Journal of Research and Development | IBM Journal of Research and Development (per-gener · roughly 2004-2015 acro | opus 5 | UNVERIFIED |
| 1 | 0.6 | Physical design implementation of the processor module and adaptive clocking system (28nm hi | IEEE Journal of Solid-State Circuits (ISSCC 2014 e · 2015 | yunbao | UNVERIFIED |
| 1 | 0.6 | 4.3B-transistor 15-core enterprise Xeon processor (22nm tri-gate CMOS) | IEEE Journal of Solid-State Circuits (ISSCC 2014 e · 2015 | yunbao | UNVERIFIED |
| 1 | 0.6 | Static Timing Analysis for Nanometer Designs | Springer (book), authors J. Bhasker and Rakesh Cha · 2009 | sonnet | UNVERIFIED |
| 1 | 0.55 | POWER5 system architecture and implementation (IBM J. R&D POWER5 issue) | IBM Journal of Research and Development, Vol. 49,  · 2005 | glm 5.3 | UNVERIFIED |
| 1 | 0.55 | A 300-MHz CMOS RISC microprocessor (Alpha 21164) | IEEE Journal of Solid-State Circuits, Vol. 30, No. · 1995 | glm 5.3 | UNVERIFIED |
| 1 | 0.55 | A 1.3 GHz fifth-generation SPARC64 microprocessor | IEEE Journal of Solid-State Circuits (likely Vol.  · 2002 | minimax 3 | UNVERIFIED |
| 1 | 0.55 | Alpha 21364: A 1.25 GHz 64-bit Dual-Issue CPU | IEEE International Solid-State Circuits Conference · 2003 | minimax 3 | UNVERIFIED |
| 1 | 0.55 | Clocking design and analysis for a 600-MHz Alpha microprocessor | IEEE Journal of Solid-State Circuits, Vol. 33, No. · 1998 | opus 5 | UNVERIFIED |
| 1 | 0.55 | IBM POWER5 / POWER6 / POWER7 per-generation papers in the IBM Journal of Research and Develo | IBM Journal of Research and Development · roughly 2005-2011 | opus 5 | UNVERIFIED |
| 1 | 0.55 | Tukwila: quad-core Itanium processor in 65nm | IEEE Journal of Solid-State Circuits (ISSCC 2008 e · 2009 | yunbao | UNVERIFIED |
| 1 | 0.5 | IBM z900 microprocessor and system papers (dedicated issue) | IBM Journal of Research and Development, Vol. 46,  · 2002 | glm 5.3 | UNVERIFIED |
| 1 | 0.5 | The IBM eServer z990 Microprocessor | IBM Journal of Research and Development · 2004 | mimo | UNVERIFIED |
| 1 | 0.5 | The IBM System z10 Processor | IBM Journal of Research and Development · 2009 | mimo | UNVERIFIED |
| 1 | 0.5 | The SPARC64 V Processor | IEEE International Solid-State Circuits Conference · 2004 | mimo | UNVERIFIED |
| 1 | 0.5 | A 130-nm 600-MHz G6 PowerPC microprocessor | IEEE Journal of Solid-State Circuits, Vol. 36, No. · 2001 | minimax 3 | UNVERIFIED |
| 1 | 0.5 | Design of the DEC Alpha 21364 (EV7) microprocessor | IEEE Micro · 2000 | solar pro | UNVERIFIED |
| 1 | 0.5 | The Pentium 4 microprocessor | IEEE Micro · 2001 | solar pro | UNVERIFIED |
| 1 | 0.5 | The Chip Design / physical-design practitioner discussion communities | Long-running EDA and chip-design forums and Q&A si · 2000s-present | opus | UNVERIFIED |
| 1 | 0.45 | The implementation of the IBM z10 processor (dedicated J. R&D issue) | IBM Journal of Research and Development, Vol. 53,  · 2009 | glm 5.3 | UNVERIFIED |
| 1 | 0.45 | Circuit and physical design of a 1-GHz microprocessor | IEEE International Solid-State Circuits Conference · ~1999 | minimax 3 | UNVERIFIED |
| 1 | 0.4 | Timing Closure for Deep Submicron Designs | Springer (book chapter, in 'Timing Analysis and Op · ~2003-2005 | minimax 3 | UNVERIFIED |
| 1 | 0.4 | SemiWiki (industry blog/forum, various authors including Daniel Nenni) | semiwiki.com · ? | sonnet | UNVERIFIED |
| 1 | 0.3 | A 1.0-V 90-nm 80-pF dynamic-random-access memory with a 3.0-GHz data rate and 2.5-V analog f | IEEE Journal of Solid-State Circuits · 2004 | solar pro | UNVERIFIED |
| 1 | 0.3 | Sun UltraSPARC III Cu implementation | IEEE Journal of Solid-State Circuits or ISSCC · 2000 | solar pro | UNVERIFIED |
| 1 | 0.2 | AMD K8 Opteron design retrospective | ? · ? | solar pro | UNVERIFIED |


---

## 3. Verification priority

Verification is one search per title. Spending it well matters more than spending it widely.

### Tier A — verify next (high claim count or high extraction value, all unverified)

1. **Circuit and physical design of the POWER5 microprocessor** (3 models, IBM JRD, 2004/2005 —
   models disagree on year). If real, it is the direct successor to the paper this project already
   holds and mines, in the same venue and format. Highest expected value of any unverified title.
2. **Functional verification of the POWER4 microprocessor and POWER4 multiprocessor systems**
   (2 models, both conf 1.0, IBM JRD 2002). Same issue as the held POWER4 papers — the paper this
   digest read explicitly names companion papers in the same volume, so a companion is *prima facie*
   plausible, which cuts both ways: it is also the easiest kind of title to confabulate.
3. **Physical Design of a Fourth-Generation POWER GHz Microprocessor** (2 models, ISSCC 2001).
   Claimed to cover "170M transistor floorplan, dual-core + L2 on die, 0.18 µm SOI + copper, clock
   grid distribution, power delivery" — that is the POWER4 physical-design content at ISSCC length,
   and the transistor count is close to the 174 M the paper actually states. Verify.
4. **High-performance microprocessor design** (Gronowski et al., JSSC 33(5), 1998, 2 models).
   Alpha-family circuit/physical methodology overview; likely real (see §1 note) and directly
   on-target.
5. **The circuit and physical design of the POWER6 microprocessor** (2 models, IBM JRD 52(1/2)
   2008) and **The circuit design of the POWER6 microprocessor** (2 models, ISSCC 2007). Two
   distinct claimed papers on the same chip in different venues — verifying both distinguishes a
   real pair from one paper duplicated with drift.


### Tier A+ — the qwen essay's IBM line (not in the table above; recovered from a non-JSON file)

`qwen Deconstructing Chip Design Decisions_ …md` was counted as a format failure and its genre map
never entered the aggregate. It contains 12 rows with author lists and 39 inline source URLs, and it
contributes four titles no other model produced, all IBM JRD, all sharing the author who wrote the
POWER4 circuit-and-physical paper already on disk:

| title | authors as given | venue · year | conf |
|---|---|---|---|
| IBM z13 circuit design and methodology | J. D. Warnock, C. J. Berry, M. H. Wood, et al. | IBM JRD · 2015 | 0.95 |
| The Circuit and Physical Design of the POWER7 Microprocessor | J. Warnock, F. Busaba, P. Harvey, et al. | IBM JRD · 2011 | 0.90 |
| Physical design of the IBM zEnterprise 196 microprocessor | F. Busaba, et al. | IBM JRD · 2012 | 0.85 |
| IBM z15: Physical design improvements to significantly increase content in the same technology | C. Berry, et al. | IBM JRD · 2020 | 0.85 |

**Verify these as one author search, not four title searches.** J. D. Warnock is the verified first
author of the held POWER4 circuit-and-physical paper; if the attribution holds, a single search
resolves a publication line spanning POWER4 → POWER5 → POWER7 → z196 → z13 → z15 in one venue. That
is the highest expected-value verification action in this entire file.


### Tier A++ — the only URL-cited source produced by a red-team review

`chatgpt j.json` appended a reference link after its JSON object (which is why a strict parser
rejected the file — see `MISSED.md` §1c):

> **"PNR: A Complete 28nm Physical Design Case Study Using Synopsys ICC2"** — ResearchGate
> publication 399339596.

**Why this outranks most of the table.** It is (a) the only source any model cited *in support of a
technical objection* rather than in answer to a source-hunting prompt, (b) on the exact node and exact
subject matter of the flagship congestion episode, and (c) a complete published case study — the
genre the project has been trying to find for five runs, in the ASIC-flow-level form the expert actually
works in, rather than the processor-retrospective form the D1 genre map keeps returning.

**Caveats before anyone gets excited.** The `utm_source=chatgpt.com` parameter on the URL shows the
model surfaced this through its own browsing, so the title and ID come from a retrieval, not from
recall — better provenance than most of this file. But ResearchGate hosts author uploads of widely
varying quality; this could be a peer-reviewed paper, a thesis chapter, or coursework. **Verify what
it actually is before treating it as an anchor**, and note it names a commercial tool in its title,
which the project's own prompts forbid models from doing — that is a property of the source, not a
disqualification, but it shapes how any extracted episode would have to be written.

### Tier B — verify if Tier A pays off (the IBM/z-series seam)

`Circuit design methodology for a 4.5 GHz 32-nm dual-core zEnterprise microprocessor` (IBM JRD
2011), `The Circuit and Physical Design of the POWER7 Microprocessor` (IBM JRD 2011),
`Physical design of the IBM zEnterprise 196 microprocessor` (IBM JRD 2012), `The Implementation of
the IBM z10 Microprocessor` (IBM JRD 2008), `Design and microarchitecture of the IBM System z10
microprocessor` (IBM JRD 2009). ChatGPT's run-2 z10 claim was graded T1 in LOG-RUN2 with the note
that the J.R&D z10 issue is 2009 rather than the claimed 2008 — **both years appear in this list
from different models**, which is consistent with one real issue and some drift, not with two.

### Tier C — do not verify individually; they are the risk pool

**88 of the 112 titles are singletons** (claimed by exactly one model). LOG-RUN3's guidance stands:
verify only high-confidence singletons with promising coverage descriptions, discard the rest
unexamined. Three singletons are worth naming as *negative* calibration rather than candidates:

- **"The design methodology of the VA Linux 64-bit server microprocessor"** (minimax 2.7, conf 0.88,
  claimed JSSC 37(11) 2002). VA Linux Systems was a Linux hardware/services company; it did not
  design a 64-bit server microprocessor. Almost certainly fabricated, and it carries a *volume and
  issue number*, which is the fabrication signature the D1 prompt was built to expose.
- **"Design closure lessons from the IBM POWER4 microprocessor"** (chatgpt run-2 Prompt C,
  conf 0.94). This is the C-output that LOG-RUN2 graded as the jackpot. The **underlying papers are
  real and are now on disk** — but this exact title is not one of them. The lead was good; the
  citation was not. Worth logging because it is the difference between "the model found a source"
  and "the model found a title".
- **"Design methodology and 毛片 implementation of the SPARC v9 processor"** (minimax 2.7, conf 0.75).
  A Chinese-language string unrelated to the subject (and lexically obscene) is spliced into the
  middle of the title. See `MISSED.md` §3 — this is token-level corruption, not a citation error,
  and it says something about that model's output integrity that no confidence field captures.

### Non-paper leads (do not fit the table, do not lose)

- **OpenROAD / OpenLane / LibreLane GitHub issue trackers** (opus, run 2, conf 0.85). LOG-RUN2
  called this "genuinely actionable… real closure failures, real metrics, real fixes, clean public
  provenance, and it's OUR flow." It remains unmined and is the only lead in the entire corpus that
  can produce episodes with **both** public provenance and reproducibility — i.e. the only path to
  `reproduced` rather than merely `retrospective`.
- **ISPD contest reports / DAC Designer Track / ISSCC-VLSI chip sessions** (opus, run 2, conf
  0.8–0.9). Venue pointers, not citations, and honestly labelled as such by the model. Useful as
  search scope, not as sources.
- **Static Timing Analysis for Nanometer Designs** (Bhasker & Chadha, Springer 2009; 2 models). The
  one book claim that is almost certainly real. Reference literature rather than a retrospective —
  relevant to `sdc-patterns.md` rather than to the episode bank.

---

## 4. What the claim distribution says

- **152 claims → 112 unique titles → 88 singletons.** The concentration is entirely at the top: two
  titles account for 21 of the claims, and everything below three claims is effectively one model's
  word.
- **Confidence is again uninformative.** The fabricated VA Linux title carries 0.88; the real
  Bhasker/Chadha book carries 0.85. Claim count is the better signal, and even it is weak (see the
  Alpha collapse in §1).
- **gemini answered the wrong prompt and produced the most useful new material.** Asked for D2
  extraction, it emitted a 10-entry genre map including six titles no D1 model produced (DAC 2004
  POWER5, JSSC 2000 Itanium circuit design, JSSC 1997 Alpha 21264 600 MHz, IEEE Micro 1995
  UltraSPARC-I, IEEE Micro 1997 AMD-K6, JSSC 1998 1 GHz Alpha). A format failure that expanded the
  search space — worth noting before the pipeline optimizes format compliance too hard.
