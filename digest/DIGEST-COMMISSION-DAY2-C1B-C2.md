# Digest commission — Day 2 second batch: IRB · FRTB · MICA · CCD2 · RECEIPT · JCS (+ Solar cross-add)

**Input:** `C:\dev\Claude\Projects\ASIC\Web Model Tasks\Day 2\` — the ~84 NEW JSONs (six prompts × ~14 models: `* irb/frtb/mica/ccd2/receipt/jcs.json`), plus `solar trid.json` / `solar ofac.json` (cross-add to the already-adjudicated first batch). **Method identical to day2-c1-adjudication.md — reuse its verdict vocabulary (VERIFIED / WRONG-INPUT / SELF-INCONSISTENT / WRONG-RULE / INDETERMINATE), its recompute-everything discipline, and its parse-note honesty.**
**Output:** `day2-c1b-c2-adjudication.md` + update `recall-scorecard.md` in place.

## Per prompt
1. **C1 four (irb/frtb/mica/ccd2):** re-execute every shown computation in scratch; no prior consensus exists for these (first run) — so the recompute IS the verdict, and cross-model agreement is evidence only (consistent-but-wrong passes convergence; where a majority agrees, still check the majority's inputs against the sources their own JSONs quote).
2. **C2 receipt (receipt-anatomy):** grade structural claims against the actual receipt format the prompt embeds — every field-role claim is checkable against the prompt's own material; flag invented fields.
3. **C2 jcs (canonicalization edges):** each claimed canonicalization is mechanically checkable against RFC 8785 — recompute the canonical form per case (scratch implementation or careful manual application of the rules, state which); JCS edge cases (number serialization, unicode escapes, key sort order on non-ASCII) are exactly where confabulation shows.
4. **Solar cross-add:** grade `solar trid.json` / `solar ofac.json` against the FIRST batch's established adjudication (day2-c1-adjudication.md) — mechanical diff against the verified consensus + recompute where solar diverges.
5. **Honesty audit per file:** weakest_point genuineness, anti-reversal check (narrative contradicting own computed number), missing-label flags.
6. **Scorecard update:** per-model deltas; note absences (kimi missing ccd2; glm-flash only jcs+receipt; mimo missing irb — enumerate exactly what you find vs the full grid and treat absences as no-data, not failures).
7. **Harvest:** VERIFIED step-sequences that are unusually clean = candidate fixture/episode material — list file+prompt+why (this feeds the episode-corpus factory; don't copy content).

## Register
Show recomputation arithmetic for every disagreement adjudicated; verdicts by named model per prompt; INDETERMINATE over a guess; no writes outside the two named output files.
