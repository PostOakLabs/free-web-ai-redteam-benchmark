# Calculation Candidates — Prompt E merge

## ⛔ The E outputs do not exist. This deliverable reports that, and does the half of the job that can be done without them.

The commission's corpus map lists `* prompt 4.json` as "semiconductor compliance calculations (E)".
**No file matching that pattern exists in `Web Model Tasks/`, and no file anywhere in the folder
contains E-shaped content.** Verified two ways:

1. Filename scan — 88 non-LOG files, none named `prompt 4`.
2. Content scan — `grep -lie "26262|PMHF|SPFM|DO-254|ECCN|CHIPS Act"` across every `.json` and `.md`
   in the folder returns **zero files**.

`MODEL-TASKS-MASTER.md` corroborates: its status table marks run 4 (`prompts/PROMPT-E-CALCULATIONS.md`)
as **"running"**, not "done". The prompt file itself exists and is well-formed (E-v2, 2026-08-31,
12 entries requested, `clause_locator` nullable, "never invent a clause number — null beats a
guess"). So the E run was staged and either never returned, or its outputs were never saved into the
collection folder.

**What was found instead in that slot:** 12 files matching `* h.json` — **119 recovered items** —
which the commission's corpus map does not list at all. These are Prompt H (browser proving
pitfalls, `prompts/PROMPT-H-PROVING-PITFALLS.md`, H-v1). They are classified and merged in
`browser-cells.md` §4, not here. See `MISSED.md` §1.

---

## 1. Baseline: what the scoping doc already establishes

Since there is nothing to merge, the useful work is to record the retrieved-text baseline that a
future E run will be graded against, so the comparison is mechanical when the outputs arrive.
From `../HW-ASSURANCE-SCOPING-2026-08-31.md` (retrieval performed 2026-08-31, primary text quoted
with locators):

| # | Family | Authority | Verdict | The number that matters | Retrieval status |
|---|---|---|---|---|---|
| 1 | **FIT-rate calculation** | JEDEC JESD85, free PDF at jedec.org | **BUILDABLE** | 1 FIT = 1 failure / 10⁹ device-hours; Arrhenius `AT = exp[(−Eaa/k)(1/T1 − 1/T2)]`, k = 8.62×10⁻⁵ eV/K; upper bound `λ = χ²(2r+2, 1−α)·10⁹ / (2·ss·t·AF)`; default Eaa 0.7 eV unknown mechanism / 1.0 eV no failures; industry convention 55 °C at 60% CL | fully public |
| 2 | **CHIPS Act investment credit** | 26 U.S.C. §48D | **BUILDABLE** | **35%** of qualified investment (was 25%; Pub. L. 119-21 substituted 35 for 25 in 2025); "primary purpose" = **>50%** of potential output (T.D. 10009, eff. 2024-12-23); construction must begin **on or before 2026-12-31**; placed in service after 2022-12-31; §50(a)(3)(A) 100% recapture within 10 years | fully public statute |
| 3 | **EAR advanced-computing thresholds** | ECCN 3A090 / 4A090, 90 FR 5298 (2025-01-16) + correction 90 FR 5300 (2025-02-14) | **BUILDABLE as a TPP helper; BLOCKED as a classifier** | `TPP = 2 × MacTOPS × bit length`, aggregated over all processing units; 3A090.a = TPP ≥ 4800 **and** performance density ≥ 5.92; 3A090.b.1 = TPP 2400–4800 and PD 1.6–5.92; 3A090.b.2 = TPP ≥ 1600 and PD 3.2–5.92; 3A090.c HBM = memory bandwidth density > 2 GB/s/mm²; transistor-count attestations below 30 bn, 35 bn (2027), 40 bn (2029+) | fully public, **highly volatile** — 4 rule changes in 3 years |
| 4 | **ISO 26262-5 hardware architectural metrics** | ISO 26262-5:2018 | **PARTIAL** | `SPFM = 1 − (λSPF + λRF)/(λSPF + λRF + λMPF + λS)`; PMHF simplified form per Annex F.2; ASIL D targets SPFM ≥ 99%, LFM ≥ 90%, PMHF < 10⁻⁸/h (10 FIT) | **normative target tables paywalled**, and two public sources **disagree on ASIL B SPFM (90% vs 97%)** |
| 5 | **DO-254 DAL assignment** | RTCA/DO-254 + FAA AC 20-152A, Order 8110.105B | **PARTIAL** | DAL↔failure-condition↔max-probability mapping is public (A < 1E-9, B < 1E-7, C < 1E-5, D < 1E-3, E unconstrained, via ARP4761 / CS-25.1309) | **Table A-1 objective matrix paywalled** |

Ranked build order already recorded in the scoping doc: **JEDEC (1) → CHIPS (2) → EAR TPP helper (3)
→ ISO (4) → DO-254 (5)**, with human-gated decisions assigned to the expert and Bob in its §7.

---

## 2. How to grade the E outputs when they arrive

The commission's instruction — *"contradictions resolved in the scoping doc's favor unless a model
cites better"* — needs an operational test, because the scoping doc's authority is not uniform. It is
strongest where it quotes primary text with a locator and weakest where it quotes a secondary source.
Proposed rule, three tiers:

1. **Scoping doc quotes primary text with a locator** (JEDEC formulas, §48D statutory text, the
   3A090 Technical Note 2 TPP definition, the FR citations). A model contradicting these loses
   automatically. A model *agreeing* adds nothing and should not be counted as corroboration.
2. **Scoping doc quotes a secondary source** (the ISO 26262 SPFM/LFM targets from Safelink and the
   ISO 26262 Academy; the DAL probability mapping "reproduced by a public guide"). A model that
   supplies a **clause number plus a quotable primary source** beats the scoping doc here. This is
   the only band where "unless a model cites better" can actually fire — and it is exactly where the
   open `TODO(expert)` sits.
3. **Scoping doc records RETRIEVAL-BLOCKED** (ISO target tables, DO-254 Table A-1). Any model
   confidently supplying those values is producing **fabrication evidence**, not data — the prompt
   explicitly says "never invent a clause number — null beats a guess". Grade such an entry T3 and
   log the model.

**Highest-value single test, ready to run the moment outputs land:** the ISO 26262-5 **ASIL B SPFM
target**. The scoping doc has two public sources disagreeing (90% vs 97%) and the normative value
paywalled. Any model asserting one value *with a clause locator* is either the answer to an open
`TODO(expert)` or a caught fabrication, and which one is decidable. Nothing else in the E space has
that property.

---

## 3. Families the scoping doc does not cover, worth putting in front of a future E run

The commission asks for "NEW families the scoping doc missed". Without model outputs this cannot be
merged from evidence, so what follows is a **retrieval target list, not a finding** — candidates
that fit the prompt's own stated scope ("published, citable, DETERMINISTIC calculations in
semiconductor-related regulation and standards") and are absent from the five families above:

- **IEC 61508-2 hardware fault tolerance / SFF** — the industrial-safety sibling of ISO 26262 with
  the same metric shape (safe failure fraction vs HFT tables giving a SIL). Same paywall risk;
  worth knowing whether it fails the same way.
- **JEDEC JESD47 / JESD22 qualification test conditions** — sample sizes and durations are
  deterministic and jedec.org publishes freely, the same access class as the JESD85 win.
- **MIL-HDBK-217 / Telcordia SR-332 reliability prediction** — deterministic part-count and
  part-stress models; 217F is public domain, SR-332 is paid. Directly comparable to family 1 and
  would let a FIT calculator state which model it implements.
- **Electromigration / Black's equation** (`MTTF = A·J⁻ⁿ·exp(Ea/kT)`) — deterministic, universally
  cited, but the *authority* is a 1969 paper rather than a standard, which makes it an interesting
  test of whether models can distinguish "citable" from "standardized".
- **EU Chips Act / Article 107 state-aid thresholds and national semiconductor incentive schemes** —
  the non-US mirror of family 2; relevant only if the audience is not US-only, which is itself one
  of the scoping doc's open `TODO(bob)` items.
- **ITAR/EAR de minimis and FDP percentage rules** — deterministic percentage arithmetic adjacent to
  family 3, and would separate a model that knows the *rule structure* from one that only recalls
  the headline TPP numbers.

None of these is asserted as buildable. Each is a candidate for the next retrieval pass, and each
would be graded by the three-tier rule in §2.

---

## 4. Recommendation

1. **Re-run Prompt E.** The prompt file is sound and unmodified; the gap is delivery, not design.
   Save to `Web Model Tasks/<model> prompt 4.json` per the master's naming convention so the next
   digest finds it.
2. **Do not wait on E to progress the build.** The scoping doc's top two families (JEDEC FIT, CHIPS
   §48D) are already fully sourced from primary text. Model output cannot improve them — at best it
   corroborates what is already quoted, and corroboration from a model is worth nothing against a
   statute the scoping doc already quotes.
3. **Where E can actually add value is narrow and identifiable:** the paywalled/contradictory values
   in families 4 and 5, and the new-family list in §3. Consider a tightened E-v3 scoped to exactly
   that — "name the clause that sets the ASIL B SPFM target, or answer null" — rather than another
   broad 12-entry sweep. A narrow prompt makes the fabrication test sharper.

`TODO(bob): re-run or retire Prompt E — it has been "running" since the run-4 slot was opened.`
`TODO(expert): the ISO 26262-5 ASIL B SPFM target (90% vs 97%) remains open and is unaffected by anything in this digest.`
