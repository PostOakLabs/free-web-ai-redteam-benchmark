Context: the paper "The circuit and physical design of the POWER4 microprocessor" (Warnock et al., IBM Journal of Research and Development, Vol. 46, No. 1, 2002, pp. 27–52) is a verified example of a *processor implementation retrospective*: a published, citable account of how a real chip's physical design and timing closure was actually done, including problems hit and decisions made.

List as many OTHER published sources of this same genre as you can genuinely name: per-processor implementation/physical-design/timing-closure retrospectives in venues like the IBM Journal of R&D, ISSCC, VLSI Symposium, IEEE JSSC, IEEE Micro, or engineering books. Think across families: IBM POWER and z-Series, DEC Alpha, Intel Itanium/Pentium, AMD, Sun UltraSPARC, and any others.

**Output: a single bare JSON array** of `{title, authors_if_known, venue, year, pages_if_known, what_design_decisions_it_covers, confidence}` where `confidence` (0.0–1.0) is your confidence the source exists exactly as named.

**Hard rules:** only sources you can truly name — an entry you are unsure of gets a low confidence, and inventing one is the worst possible output. No prose outside the JSON.

[prompt-version: D1-v3 2026-08-31]
