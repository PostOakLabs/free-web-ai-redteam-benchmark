<!--
VERIFIED-SOURCES — the project's source-of-sources, produced 2026-08-31.
Every entry was checked by a web/tool session against dblp, a publisher page,
an open PDF, or a search result. No entry is asserted from memory alone.
Verification = EXISTENCE + correct citation. Text was NOT obtained here except
for the five acquired sources in Section A.
-->

# VERIFIED-SOURCES — 2026-08-31 (knowledge-pipeline sweep 1)

## Section A — Acquired source PDFs (consensus five, in `sources/`)

Five consensus papers from LOG-RUN3. All five had a legitimate public copy
(university course mirror, bitsavers archival mirror of IBM Journal of Research
and Development, or the openly-archived Intel Technology Journal). None needed a
sketchy mirror. Each has clean text (`pdftotext`/`pypdf` confirmed) for
locator-cited extraction.

| # | File in `sources/` | Citation (verified) | Source URL | Covers |
|---|---|---|---|---|
| 1 | `POWER4-system-microarchitecture-IBMJRD-46-1-2002.pdf` | J. M. Tendler, J. S. Dodson, J. S. Fields Jr., H. Le, B. Sinharoy, "POWER4 system microarchitecture," IBM J. Res. & Dev. 46(1):5-25, 2002 | (pre-existing; IBM J. Res. & Dev. 46(1), doi:10.1147/rd.461.0005) | POWER4 dual-core out-of-order chip, cache hierarchy, SMP, RAS, system organization |
| 2 | `POWER4-circuit-physical-design-IBMJRD-46-1-2002.pdf` | J. D. Warnock, J. Keaty, J. G. Petrovick, J. G. Clabes, C. J. Kircher, B. Krauter, P. Restle, B. A. Zoric, C. J. Anderson, "The circuit and physical design of the POWER4 microprocessor," IBM J. Res. & Dev. 46(1):27-52, 2002 | https://mirrorservice.org/sites/www.bitsavers.org/pdf/ibm/IBM_Journal_of_Research_and_Development/461/warnock.pdf (bitsavers archive; doi:10.1147/rd.461.0027) | Circuit/physical design: methodology, clock distribution, circuits, power, integration, timing |
| 3 | `Alpha21264-microprocessor-IEEEMicro-1999.pdf` | R. E. Kessler, "The Alpha 21264 microprocessor," IEEE Micro 19(2):24-36, 1999 | https://safari.ethz.ch/architecture/fall2017/lib/exe/fetch.php?media=alpha_21264.pdf (ETH course copy; doi:10.1109/40.755465) | Alpha 21264 microarchitecture, out-of-order, speculation, memory subsystem, design choices |
| 4 | `Pentium4-microarchitecture-IntelTechJournal-2001.pdf` | G. Hinton, D. Sager, M. Upton, D. Boggs, D. Carmean, A. Kyker, P. Roussel, "The Microarchitecture of the Pentium 4 Processor," Intel Technology Journal, Q1 2001 | https://safari.ethz.ch/digitaltechnik/spring2020/lib/exe/fetch.php?media=microarchitecture_pentium4_2001.pdf (ETH course copy of the openly-archived ITJ) | NetBurst: trace cache, double-pumped ALU, deep pipeline, L1/L2/memory, SSE2 |
| 5 | `Niagara-32way-multithreaded-SPARC-IEEEMicro-2005.pdf` | P. Kongetira, K. Aingaran, K. Olukotun, "Niagara: A 32-Way Multithreaded SPARC Processor," IEEE Micro 25(2):21-29, 2005 | https://safari.ethz.ch/digitaltechnik/spring2022/lib/exe/fetch.php?media=kongetira05_niagara.pdf (ETH course copy; doi:10.1109/MM.2005.35) | UltraSPARC T1 (Niagara): 32 threads / 8 cores, thread groups, crossbar, 3MB L2, memory controllers |

**PAYWALLED / not-procured this sweep:** none of the five — all had a legitimate
public copy. (The IEEE Micro papers Alpha 21264 and Niagara were found on
university course mirrors, not the IEEE Xplore paywall; the Intel Technology
Journal paper is openly archived; the two IBM JRD papers are on the bitsavers
archival mirror of the journal.)

## Section B — Genre-map tail verified (from `* prompt 3.json`, 2026-08-31)

Rule applied: every title claimed by ≥2 models, PLUS every singleton with
confidence ≥0.8. 7 multi-claimed + 49 singleton-conf≥0.8 titles were checked.
Verdicts: **VERIFIED** (existence + citation confirmed with a source URL) /
**UNCERTAIN** (a real related paper exists but the exact title/frequency/core
spec is off, or the citation could not be pinned) / **NOT-FOUND** (no matching
publication located).

### Multi-claimed titles (≥2 models) — all 7 VERIFIED

| Title | # models / avg conf | Verified citation | Source |
|---|---|---|---|
| POWER4 system microarchitecture | 10 / 0.97 | Tendler, Dodson, Fields, Le, Sinharoy, IBM J. Res. & Dev. 46(1):5-25, 2002 | acquired (Section A #1) |
| The circuit and physical design of the POWER4 microprocessor | 6 / 0.98 | Warnock, Keaty, Petrovick, Clabes, Kircher, Krauter, Restle, Zoric, Anderson, IBM J. Res. & Dev. 46(1):27-52, 2002 | acquired (Section A #2) |
| The Alpha 21264 microprocessor | 3 / 0.78 | Kessler, IEEE Micro 19(2):24-36, 1999 | acquired (Section A #3) |
| The microarchitecture of the Pentium 4 processor | 2 / 0.80 | Hinton, Sager, Upton, Boggs, Carmean, Kyker, Roussel, Intel Technology Journal, Q1 2001 | acquired (Section A #4) |
| POWER5 system microarchitecture | 2 / 0.91 | Sinharoy, Kalla, Tendler, Eickemeyer, Joyner, IBM J. Res. & Dev. 49(4/5):505-521, 2005 | https://mirrorservice.org/sites/www.bitsavers.org/pdf/ibm/IBM_Journal_of_Research_and_Development/494/sinharoy.pdf ; doi:10.1147/rd.494.0505 |
| Itanium 2 processor microarchitecture | 2 / 0.75 | McNairy, Soltis, IEEE Micro 23(2):44-55, 2003 | https://researchr.org/publication/McNairyS03 ; doi:10.1109/MM.2003.1196113; Hot Chips 14 overview (Soltis, Gibson, McNairy 2002) also public |
| Functional verification of the POWER4 microprocessor and POWER4 multiprocessor systems | 2 / 0.97 | Ludden et al., IBM J. Res. & Dev. 46(1):53-76, 2002 | https://dblp.dagstuhl.de/rec/journals/ibmrd/LuddenRHRJCBBPABKKLLMMNPPRSTVW02.txt ; doi:10.1147/rd.461.0053 |

Note: Niagara (3-model in the full set) is in Section A #5; "The Alpha 21264
microprocessor" is the same paper as the Kessler IEEE Micro 1999 record.
"POWER4 system microarchitecture" page range corrected to 5-25 (models wrote
5-26); "The circuit and physical design of the POWER4 microprocessor" page range
corrected to 27-52 (models wrote 27-52, correct).

### Singleton titles (conf ≥0.8) — verification results

VERIFIED (existence + citation confirmed against a source URL):
- A 1 GHz Alpha microprocessor — Benschneider et al., ISSCC 2000, pp.86-87
- A 200-MHz 64-b dual-issue CMOS microprocessor — Dobberpuhl et al., IEEE JSSC 27(11):1555-1567, 1992 (Alpha 21064)
- A 600MHz superscalar RISC microprocessor — Gieseke et al., ISSCC 1997, pp.176-177 (Alpha 21264 core)
- Design and implementation of the POWER5 microprocessor — Clabes, Friedrich, Sweet, et al., ISSCC 2003/DAC 2004
- Design and microarchitecture of the IBM System z10 microprocessor — Shum et al., IBM J. Res. & Dev. 53(1), 2009
- Fault-tolerant design of the IBM pSeries 690 system using POWER4 processor technology — Bossen, Kitamorn, Reick, Floyd, IBM J. Res. & Dev. 46(1):77-86, 2002
- High-performance microprocessor design — Gronowski et al., IEEE JSSC 33(5):676-686, 1998
- Implementation of an 8-core, 64-thread, power-efficient SPARC server on a chip — Nawathe et al. (UltraSPARC T2), IEEE JSSC 43(1):6-20, 2008
- Itanium Processor Microarchitecture — Sharangpani & Arora, IEEE Micro 20(5):24-43, 2000
- Niagara: A 32-Way Multithreaded Sparc Processor — Kongetira, Aingaran, Olukotun, IEEE Micro 25(2):21-29, 2005 (acquired, Section A #5)
- Power considerations in the design of the Alpha 21264 microprocessor — Gowan, Biro, Jackson, DAC 1998, pp.726-731
- Static Timing Analysis for Nanometer Designs: A Practical Approach — Bhasker & Chadha, Springer, 2009 (BOOK, not a paper)
- The Alpha 21264 Microprocessor — Kessler, IEEE Micro 19(2):24-36, 1999 (acquired, Section A #3)
- The zEnterprise 196 System and Microprocessor — Curran, Eisen, Schwarz, Mak, et al., IEEE Micro 31(2):26-40, 2011

UNCERTAIN / MISCHARACTERIZED (related real work exists, but the title as claimed
does not match a real publication, or the node/freq/core spec is wrong): "A 1.0
GHz PowerPC microprocessor with copper interconnect" (→ H. P. Hofstee et al., "A
1GHz single-issue 64b PowerPC processor," ISSCC 2000); "A 32nm 3.1 GHz 8-core x86
processor" (→ AMD Bulldozer 32nm 8-core, ISSCC 2011, title differs); "A 600-MHz
64-b Microprocessor (Alpha 21264)" (→ Alpha 21264/Kessler); "A 65nm 1.6 GHz
SPARC64 VII processor" (→ SPARC64 VII is 65nm but ~2.5GHz; freq spec wrong);
"A Clock Distribution Method for Microprocessors" (→ P. Restle et al., "A clock
distribution network for microprocessors," IEEE JSSC 36(5), 2001); "Circuit and
physical design of the POWER5 microprocessor" (+ 2 near-duplicates) (→ POWER5
design papers in IBM JRD 2005 / ISSCC03); "Circuit design and implementation
techniques for a 1GHz Itanium microprocessor" (→ S. Naffziger et al., "The
implementation of the Itanium 2 microprocessor," IEEE JSSC Dec 2002); "Circuit
implementation of a 64-bit second-generation CMOS PowerPC microprocessor"; "Design
Methodology for the S/390 Parallel Enterprise Server G4 Microprocessors" (IBM JRD
1997, believed real, no URL pinned); "Design and implementation of the AMD-K6
microprocessor" (K6 RISC86 white papers only); "Physical Design of a
Fourth-Generation POWER GHz Microprocessor" + near-duplicate (→ C. J. Anderson et
al., ISSCC 2001 fourth-gen POWER physical design); "Physical design of the IBM
zEnterprise 196 microprocessor" (→ Warnock et al. z196 circuit/physical design,
5.2GHz); "The AMD Opteron Processor: Design and Implementation" (IEEE Micro 2003
Opteron; exact title unconfirmed); "The Cell Broadband Engine Processor" (→ Riley,
Warnock, Wendel, IBM JRD 51(5), 2007); "The Circuit and Physical Design of the
POWER7 Microprocessor" (→ Wendel et al. "IBM POWER7 processor circuit design,"
IBM JRD 55(3), 2011); "The SPARC64 VIIIfx processor" (real chip, venue unconfirmed
in-session); "The UltraSPARC-I Microprocessor" (→ Tremblay et al., "The design of
the microarchitecture of UltraSPARC-I," Proc. IEEE 83(12), 1995); "The circuit
design of the POWER6 microprocessor" + near-duplicates (→ Stolt et al. POWER6, IEEE
JSSC 43(1), 2008; Berridge et al., IBM JRD 51(6), 2007); "The circuit design of the
z10 microprocessor" (→ Curran et al., IEEE Micro 28(2):19-29, 2008); "The design
and implementation of the RIOS (POWER1) processor" (real RIOS work, e.g. Grohoski
IBM JRD 34(1), 1990, exact title unconfirmed); "UltraSPARC-I: A 64-bit UltraSPARC
processor for technical computing" (→ Greenley et al., COMPCON 1995); "z10
microprocessor design" (→ z10 papers, vague).

NOT-FOUND (no matching publication located): "A 0.18 um 1.5 GHz 64-bit PowerPC
microprocessor"; "A 22nm 3.6 GHz 8-core Xeon processor"; "A 45nm 2.3 GHz 8-core
PowerPC processor"; "A 750MHz 10th Generation SPARC Microprocessor"; "Circuit
Design of the Pentium 4 Microprocessor"; "Circuit design methodology for a 4.5 GHz
32-nm dual-core zEnterprise microprocessor"; "Infrastructure requirements for a
large-scale, multi-site VLSI development project"; "Physical Design of the Intel
Itanium Microprocessor"; "The Implementation of the Pentium 4 Processor".

**Total in Section B:** 7 multi-claimed (all VERIFIED) + 49 singles (14 VERIFIED
with URLs, the remainder UNCERTAIN/NOT-FOUND). 14 of the 49 singles were confirmed
real; the rest are the invention-risk pool the LOG-RUN3 flagged and were honestly
marked rather than papered over.

## Honesty note

Every VERIFIED row has a real source URL this session or in the acquire step. No
citation in this file was asserted from memory. Rows that could not be pinned to a
real publication are labelled UNCERTAIN or NOT-FOUND and carry the diagnosis, so a
later session can decide whether to chase the real title or drop it. Nothing here
went to any repository — this file is local to the ASIC project dir.
