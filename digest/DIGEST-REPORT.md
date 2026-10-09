# DIGEST REPORT — the complete web-model collection effort, A through T

**Scope:** every file in `../Web Model Tasks/`, salvage-parsed, merged, and — where ground truth or
recomputation applies — graded against it. **Written:** 2026-08-31, refreshed after the P/Q/S/T
slices landed. **Writes confined to** `Web Model Tasks/` and `digest/`; no repository was modified.

**Corpus: 233 files, 2.34 MB, 1,550 JSON items across 18 slices.** Nineteen files yield no JSON on a
first load; all nineteen were read and salvaged rather than discarded.

---

## 1. Deliverables

| File | What it is |
|---|---|
| `episode-draft-bank.md` | **A / D2 / J / L / M / N / O** — 78 episode drafts, five paper-recall adjudications, the red-team review, 266-pair rejection appendix |
| `recall-scorecard.md` | **The model scorecard** — 309 recall claims over 6 slices × 13 models, honesty-field calibration, **arithmetic-reliability column** from S/T, rotation |
| `anti-reversal-experiment.md` | **P** — the controlled rerun that settles the warning-vs-paper confound |
| `hw-calc-formulas.md` | **S** — 4 calculation families, consensus formulas stated symbolically, every worked example recomputed, thresholds marked NEEDS-RETRIEVAL |
| `hw-calc-vectors.md` | **T** — 113 vectors recomputed; 101 survivors as a candidate fixture suite, 12 failures with the exact broken step, coverage gaps named |
| `diagnosis-library.md` | **F** — 6 failure classes, deduplicated symptoms / causes / checks / traps, `disputed:` markers |
| `sdc-patterns.md` | **G** — 88 drafts → 13 canonical patterns, every worked example recomputed |
| `node-era-deltas.md` | **K** — 110 deltas → 11 families, 28nm vs 7nm/5nm, five mechanism disputes flagged |
| `review-checklists.md` | **I** — 4 signoff gates, 339 checks, thresholds marked `disputed:` |
| `browser-cells.md` | **B** graded against real browser measurements; **H** (122 items) classified |
| `source-candidates.md` | **C / D1** — 152 claims → 112 unique titles, verification status, priority tiers |
| `interview-guide.md` | **Q** — ⏸ **PARKED**: soft/qualitative, off the deterministic north star, retained for a future human expert |
| `calculation-candidates.md` | **E** — reports that the slice does not exist; specifies the grading rule for when it does |
| `MISSED.md` | What the graded logs missed; corrections to the record; ranked next-prompt angles |

---

## 2. Recovery counts

| Slice | Prompt | Files | Items | No-JSON | Note |
|---|---|---|---|---|---|
| R1 / R2 | A · A/B/C | 15 / 15 | 100 / 91 | 1 / 1 | R2's minimax 2.7 JSON was never saved — the only real data loss |
| D1 | genre maps | 15 | 143 | 1 | the no-JSON file is a URL-cited genre map — largest single salvage |
| D2 | POWER4 recall | 9 | 44 | 1 | |
| F · G | diagnosis · SDC | 11 · 11 | 74 · 88 | 1 · 1 | |
| H | proving pitfalls | 12 | 122 | 1 | ungraded until this digest |
| I · J | checklists · red-team | 13 · 13 | 54 · 66 | 1 · 1 | J needed two new salvage techniques |
| K | node deltas | 13 | 110 | 1 | |
| L · M · N · O | Alpha · P4 · POWER4-phys · Niagara | 13 each | 52 · 52 · 48 · 59 | 1 · 1 · 2 · 1 | |
| **P** | POWER4 recall v2 | 13 | 56 | 1 | **the controlled experiment** |
| **Q** | interview guide | 14 | 212 | 1 | largest per-file yield; parked |
| **S** | calc formulas | 13 | 66 | 1 | |
| **T** | test vectors | 14 | 113 | 1 | |
| E | compliance calcs | **0** | **0** | — | **slice does not exist**; master still marks run 4 "running" |
| **TOTAL** | | **233** | **1,550** | **19** | |

**Salvage ladder — five techniques.** Balanced-bracket scan; element-wise re-parse for truncation;
invalid-escape repair (one stray `\ldots` made a whole review unreadable); trailing-content tolerance
(a valid object followed by a real citation); and **wrong-paper detection**, which no parser can do —
only content-versus-target comparison.

---

## 3. Top 10 across the entire effort

1. **P settles the anti-reversal question.** Same paper, same models, warning added: contradictions
   **19% → 3.6%**, inversions **3 → 0**. The confound between prompt and paper is resolved in favour
   of the prompt, and the fix is a sentence plus a mandatory field. `anti-reversal-experiment.md`.
2. **meta scored 25/25 across five papers** — full coverage, exact figure-caption numbers, zero errors
   of any kind, and clean arithmetic in S/T as well. The only model strong at both competencies.
3. **glm 5.3 flash submitted the same Alpha 21264 text for eight different prompts** — M, N, O, P, Q,
   S, T and its own L. Well-formed JSON, valid schema, populated honesty fields, entirely wrong.
   **No automated check in the pipeline can see this**; only content-versus-target comparison finds it.
4. **mistral's inverted SPFM, stable across S and T.** `SPFM = λ_SPF / Σλ` instead of its complement —
   reporting **95% where the correct value is 3%**, in a formula and in all three vectors derived from
   it. Plausible ASIL percentages, wrong by an order of magnitude. The most consequential single
   defect in the corpus, and it was in a file the task brief described as empty.
5. **The J red team converged on exactly the claim the author had self-flagged.** All 13 models
   attacked the same DRC transition that opus's own `weakest_point` calls "the least defensible".
   `weakest_point` predicts what review attacks; `confidence` does not — now confirmed across six
   graded slices, and **91% adoption on first request** when P made the field mandatory.
6. **Arithmetic correctness and rule correctness are independent failure modes.** gemini computes TPP
   flawlessly and states 3A090.a as an OR of two conditions the regulation ANDs; grok computes TPP
   flawlessly and invents an "a.2" band. A recomputation gate catches neither.
7. **101 of 113 test vectors survive recomputation** — a candidate fixture suite with exact ASIL
   90/97/99 boundaries, an 8-unit near-miss on the 4800 TPP threshold, and AF = 1 / r = 0 degenerate
   cases. Four coverage gaps named, none needing a model to fill.
8. **Two models independently asserted directory-based coherence for a snoop-based design**, and ten
   independently agree on an ASIL B SPFM target the public literature disputes. **Multi-model
   agreement tracks a shared prior, not truth** — three separate demonstrations now.
9. **grok recalled POWER4's circuit constraints at circuit-designer resolution** — the one-third-cycle
   global slew limit and the late-binding low-Vt swap, both verbatim, on the paper closest to Alice's
   domain.
10. **The 266 rejection-rationale pairs** — more than double the logged estimate, merged and grouped.
    The largest reusable artefact, and the one that survives whatever happens to the episode numbers.

---

## 4. Per-model summary

| Model | Recall (309 claims) | Arithmetic (S/T) | Generative | Verdict |
|---|---|---|---|---|
| **meta** | **100%** | **EXCELLENT** | broad, node-aware | **First call, both competencies** |
| **chatgpt** | 92%, inversion corrected in P | **EXCELLENT** | best structural contributor | **Deterministic math + structure**; verify citations |
| **yuanbao** | 92% | **EXCELLENT**, one convention divergence | most operationally specific | **Recall + math**, pin its SPFM denominator |
| **grok** | 92% | MIXED — a 10³ FIT slip, an invented EAR band | decisive-experiment framing | **Recall yes, math spot-check** |
| **sonnet** | 100% (low volume) | GOOD, most honest PMHF answer | high-value singletons | **Verifier, both competencies** |
| **qwen** | 100% (low volume) | **POOR formula, GOOD honesty** — fabricated SPFM, 3 honest UNKNOWN flags | closure-checked SDC derivation | **Recall-verifier only** |
| **gemini** | 88% | MIXED — best idea in S, wrong classification rule | excellent structure | Structure only; never its numbers or rules |
| **kimi** | 79% | GOOD | strong H and B work | Generative, mid-tier |
| **deepseek** | 80%, same 3 errors in D2 and P | MIXED — dimensionally wrong PMHF | useful thresholds | Generative, spot-check |
| **minimax 2.7** | 38% | GOOD arithmetic, stale CHIPS rate | ordering rationales | **Drop** — 4 integrity failure modes |
| **minimax m3** | 38% | convention-divergent | high volume | **Drop** |
| **mistral** | not in recall slices | **DISQUALIFYING** | Q material fine | **Drop from all math work** |
| **glm 5.3 flash** | **10%** | NOT ASSESSABLE | — | **Suspend** — wrong content ×8 |
| **mimo** | 63% (prose) | prose refusals | substantive when it answers | **Undeliverable** — 13 refusals |

---

## 5. Five next-prompt angles, ranked by expected yield

1. **Retrieve the ASIL B SPFM target and the current 3A090 bands from primary text.** Not a model
   prompt — a retrieval task. Ten models agree on 90%; the scoping doc shows the public sources
   disagree and the normative value is paywalled. **Every S and T deliverable is blocked on this**, and
   no further model output can resolve it.
2. **Pin the SPFM denominator convention.** One sentence from Alice decides the expected value of
   30-plus fixtures. Three conventions are live in the corpus, all arithmetically self-consistent.
3. **Back-port the P-v1 package to every factual prompt** — anti-reversal sentence, mandatory
   `weakest_point`, optional `provenance_note`. Evidence: 3 → 0 inversions, 91% field adoption on
   first request. Expect it to fix direction errors only; deepseek's content errors survived it
   unchanged.
4. **Add a target-content pre-check before grading any slice.** Keyword overlap against the requested
   paper or task. It is the only thing that catches the glm class, which has now contaminated eight
   slices, and it costs a few lines.
5. **Locator-cited extraction against the two unmined papers**, using meta / grok / yuanbao only. The
   only path that produces `retrospective`-candidates, now that the tier is empirically established.

**Not recommended:** further Prompt A runs (five runs, zero named-source jackpots, `post_state`
numbers that track the prompt); further Q iteration (parked); any new slice until the manifest problem
in `MISSED.md` §1b is fixed.

---

## 6. Overall assessment

Eighteen slices, zero spend, 1,550 items. The integrity rule held throughout: nothing here is expert
data, nothing pretends to be, and no episode invented a chip, company or person.

**What the effort produced, in order of durability:**

- **Two model competency rankings established against ground truth** — recall (six slices, 309 claims,
  graded against extracted paper text) and arithmetic (two slices, every example recomputed). They do
  not correlate, and both were surprising: a model can be 100% on recall and fabricate a formula.
- **One clean controlled experiment.** P is the only place in the collection where a single variable
  was changed and measured, and it produced an actionable result for the cost of one run.
- **Merged libraries that are scaffolding, not data** — diagnosis, SDC patterns, review checklists,
  node deltas, calculation formulas, a 101-vector fixture suite, 266 rejection rationales. Value
  concentrated in the `disputed:` markers and failure narratives, not the consensus layers.
- **A calibrated honesty machinery.** `weakest_point` works and is now cheap to require.
  `paper_vs_general` is a weak two-way-failing signal. **`confidence` is uninformative across every
  graded slice and should be removed from every prompt that carries it.**

**Three lessons that outlive the corpus:**

1. **Consensus is not evidence.** Demonstrated three times — POWER4 coherence, the shared FPU, the
   ASIL B target. Models agreeing means they share a prior.
2. **Recomputation catches one failure shape out of three.** It finds steps that do not reproduce
   their output; it is blind to correct arithmetic against a wrong rule, and to correct arithmetic
   against a different convention.
3. **Delivery failures masquerade as reasoning failures.** Without a run manifest, a model that
   answered the wrong question is indistinguishable from a model that answered badly — and this
   corpus contains eight slices' worth of exactly that.

The bottleneck is unchanged and correctly placed: **primary-text retrieval, and Alice's review time.**
Collection has not been the constraint for some time; it is now producing slices faster than anything
records that they exist.
