# Day 2 Class-1 Adjudication — GLOBE · APPJ · TRID · OFAC

**Input:** `../Web Model Tasks/Day 2/` — **55 JSONs, 14 models × 4 prompts.** `glm 5.3 flash trid`
is absent, as the commission noted; not waited for. **Method:** every shown computation re-executed
independently in scratch Python; verdicts are mechanical, not judgment.

**Verdict vocabulary.** VERIFIED = correct steps, correct inputs, correct answer. WRONG-INPUT =
steps reproduce but start from a wrong constant (constant named). SELF-INCONSISTENT = steps do not
reproduce the model's own stated answer. Two extensions were unavoidable and are labelled as such:
**WRONG-RULE** (arithmetic exact, legal rule misapplied — a distinct defect the three given
categories cannot express) and **INDETERMINATE** (inputs under-specified; no verdict possible).

**Parse note.** 51 of 55 files loaded clean. `chatgpt` needed `raw_decode` on all four (trailing
prose after the array). `minimax m3` has token-level dropout in three of four files — see §6.

---

## 1. TRID — 12 CFR §1026.19(e)(3) fee tolerances

Recomputation: per-bucket sums; zero-tolerance per-fee overage; 10% test as **Σcd vs Σle × 1.10**
(aggregate-to-aggregate, not sum-of-increases); cure = excess.

| Model | Cases | Verdict |
|---|---|---|
| chatgpt | 5 | **VERIFIED 5/5** |
| gemini | 4 | **VERIFIED 4/4** |
| grok | 5 | **VERIFIED 5/5** |
| kimi | 5 | **VERIFIED 5/5** |
| meta | 5 | **VERIFIED 5/5** |
| mimo | 5 | **VERIFIED 5/5** |
| minimax 2.7 | 5 | **VERIFIED 5/5** |
| mistral | 5 | **VERIFIED 5/5** |
| qwen | 5 | **VERIFIED 5/5** |
| sonnet | 5 | **VERIFIED 5/5** |
| yuanbao | 5 | **VERIFIED 5/5** arithmetic — **1 anti-reversal flag**, see §5 |
| minimax m3 | 1 of 5 recovered | VERIFIED 1/1; file damaged |
| deepseek | 5 | **VERIFIED 4/5 · SELF-INCONSISTENT 1/5** |
| glm 5.3 flash | — | file absent |

### The one arithmetic failure

**deepseek, case 2 — "10% Bucket with Mixed Increases and Decreases – Violation Due to Aggregate
Increase" — SELF-INCONSISTENT.**

Its own `fees` table: Recording 100→200, Settlement 500→400, Survey 150→120.

```
Σle = 100 + 500 + 150 = 750
Σcd = 200 + 400 + 120 = 720
threshold = 750 × 0.10 = 75      allowed = 825
720 ≤ 825  →  NO VIOLATION  (aggregate DECREASED by 30)
```

The model states a **$55 violation**. Its `computation` field reveals why: it reached the same
conclusion I did — *"Aggregate increase = 720 − 750 = −30 (a decrease)… actually within tolerance"* —
and then wrote *"To create a violation, assume CD amounts: Recording = 250, Settlement = 450, Survey
= 180."* Against those substituted figures 880 − 825 = 55 ✓ arithmetically. **The stated data and the
stated answer belong to different fee tables.**

Worth separating clearly: deepseek's *method* is correct — it computes Σcd against Σle × 1.10 and
never falls into the sum-of-increases trap. The artefact is broken, not the reasoning.

### The trap the suite was built to catch — nobody fell into it

The prompt required ≥2 mixed-direction cases because sum-of-increases is the classic implementation
defect. **All 13 responding models applied the aggregate test.** In 31 mixed-direction cases the two
methods diverge, sometimes hugely — qwen's case 2 has +400 and −400 (sum-of-increases 400, aggregate
0); kimi's case 3 has sum-of-increases 500 against an aggregate delta of 300 — and no model reported
a violation the aggregate test does not support.

Three models state the distinction explicitly, which the prompt asked for: mimo (*"a sum-of-increases
implementation would incorrectly flag a violation"*), sonnet (*"this is the defect this test case is
designed to catch"*), and yuanbao (*"cure of 55 is the aggregate excess, which is less than the simple
sum of line-item increases (168)"*).

**Consensus check per the art-220 lesson:** consensus here is *not* the evidence — each case was
recomputed from its own fee table independently. The convergence is a consequence of correctness, not
a substitute for it.

---

## 2. OFAC 50 Percent Rule

Recomputation: fixpoint over the graph. Seeds = designated. An entity becomes blocked when blocked
owners hold ≥50% in aggregate; **a blocked entity's holdings are then attributed in full.** The
multiplicative alternative was computed alongside for comparison.

| Model | Cases | Verdict |
|---|---|---|
| deepseek | 5 | **VERIFIED 5/5** |
| glm 5.3 flash | 5 | **VERIFIED 5/5** — see §4 |
| grok | 5 | **VERIFIED 5/5** |
| kimi | 5 | **VERIFIED 5/5** |
| meta | 5 | **VERIFIED 5/5** |
| minimax 2.7 | 5 | **VERIFIED 5/5** |
| qwen | 5 | **VERIFIED 5/5** |
| sonnet | 5 | **VERIFIED 5/5** |
| yuanbao | 5 | **VERIFIED 5/5** |
| gemini | 4 | **VERIFIED 3/4 · WRONG-RULE 1/4** |
| mimo | 5 | **VERIFIED 4/5 · SELF-INCONSISTENT 1/5** |
| mistral | 5 | **VERIFIED 2/5 · SELF-INCONSISTENT 3/5** (incomplete verdicts) |
| minimax m3 | 1 of 5 recovered | VERIFIED 1/1; file damaged; **declares the multiplicative treatment** |
| chatgpt | — | **NOT ASSESSABLE — wrong content**, see §4 |

### 2.1 gemini — WRONG-RULE on the case the prompt was built around

Case 3, *"Chain Through Majority-Owned Intermediary"*: `SDN_1 →100%→ Intermediary_1 →70%→
Intermediary_2 →60%→ Target_Final`.

```
gemini:      100% × 70% × 60% = 42%  →  42% < 50%  →  Target_Final NOT blocked
attribution: Intermediary_1 blocked (100%);
             Intermediary_2 blocked (blocked owner holds 70%);
             Intermediary_2 holds 60% of Target_Final  →  Target_Final BLOCKED
```

Both computations are arithmetically exact. The divergence is the rule. gemini states its choice
plainly — *"Under OFAC rules, percentage ownership is multiplied down the tier chain; full 100%
attribution is NOT passed through majority-owned entities"* — citing *"OFAC Revised Guidance (2014) –
Multiplicative tier approach"*.

**Adjudication.** OFAC's 50 Percent Rule guidance turns on the intermediary itself becoming blocked:
a person owning ≥50% of Entity A blocks A, and A's own ≥50% holdings then block downstream entities.
deepseek's case 1 reproduces the canonical guidance example exactly — X owns 50% of A, A owns 50% of
B, **B is blocked** — which multiplication (25%) cannot yield. Twelve of the thirteen assessable
models apply attribution; gemini and minimax m3 apply multiplication. **Verdict: gemini WRONG-RULE**,
with the qualification that this is a legal-treatment judgment resting on the canonical example rather
than on retrieved primary text — the underlying guidance was not retrieved in this pass.

To gemini's credit its `weakest_point` names the exact fault line: *"Distinction between US OFAC
multiplicative approach and EU sanctions approach."* It identified the disputed axis and chose the
wrong side of it.

**minimax m3** does the same and labels it honestly: *"I am applying the multiplicative as the
conservative reading of FAQ 401, but flag this as 'unsure' in spirit."* Its single recovered case is
a direct 51% holding where both treatments agree, so no verdict divergence is observable.

### 2.2 mistral — verdicts omit the intermediaries

Case 3: `A →60%→ B →55%→ C`. Its computation is correct and explicit — *"Apply full attribution for
majority-owned intermediary (B)… 55% ≥ 50% → C is blocked"* — but `blocked_verdicts` reads `["C"]`.
**B is 60%-owned by a blocked person and is itself blocked; it is missing.** Same omission in cases 4
(B at 55% omitted) and 5 (B and C at 50% each omitted). The arithmetic is right, the rule is right,
the answer field is incomplete — and an incomplete blocked-list is the operative failure in a
sanctions screen. Graded SELF-INCONSISTENT: the verdict contradicts the model's own computation.

### 2.3 mimo — one internally contradictory case

Case 5 attributes **28% through a non-blocked 40%-owned intermediary** by multiplication
(40% × 70%), while cases 2 and 3 of the same file correctly hold that a sub-50% intermediary
transmits nothing. Its D-verdict (25% direct + 28% indirect = 53% → blocked) rests on a rule it
contradicts twice elsewhere. Cases 1–4 verify.

---

## 3. GLOBE and APPJ

### 3.1 APPJ — the strongest arithmetic in the batch

Every solvable equation was re-solved by independent bisection on the actuarial equation
`A = Σ P / [(1 + f·i)(1 + i)^k]`.

**chatgpt matches to ten significant figures on all four solvable cases:**

| Case | chatgpt's stated *i* | independently solved *i* | APR |
|---|---|---|---|
| 5,000 / 24 × 230, f=0 | 0.008071423385 | **0.008071423385** | 9.6857% → 9.69% |
| 6,000 / 36 × 200, f=19/30, t=1 | 0.009847090242 | **0.009847090242** | 11.8165% → 11.82% |
| 5,000 / 250 + 22×230 + 280 | 0.009079623982 | **0.009079623920** | 10.8955% → 10.90% |
| 1,000 → 1,080 over 255 days | Form 1: 100 × (365/255) × 0.08 | **11.450980%** | 11.45% |

**Verdict: chatgpt VERIFIED 5/5** (the fifth, a 30-year varying-payment mortgage, is consistent with
its stated i but the full 360-payment schedule is not enumerated — accepted on the equation form).

**Published-anchor convergence.** Four models independently reproduce **both** canonical Appendix J
results — 9.69% for the regular monthly case and 11.45% for the 255-day single-payment case:
**chatgpt, grok, kimi, yuanbao**. Both of deepseek's irregular variants also solve exactly
(23×230 + 280 → i = 0.008750391, APR 10.50% ✓; the biweekly 8/14-fraction case → i = 0.004701868,
26 × i = 12.22% ✓).

yuanbao additionally uses the closed forms correctly: Form 1 for the single-payment case, and Form 3
`I = 100[(P/A)^(1/t) − 1]` for a 2-year single payment — `1.24^0.5 = 1.113552873` → **11.36% ✓**.

**INDETERMINATE (1):** yuanbao's case 5, a skipped-payment 4-week loan. Its stated `i = 0.00923077`
is exactly `0.12 / 13`, i.e. back-derived from the target APR, and the (t, f) list is given for
"four series" without enumerating all 24 payments. Not reconstructible; no verdict.

**Honesty split worth recording.** chatgpt, deepseek, grok, kimi and yuanbao label their cases
`confident-in-appendix-j`; **glm 5.3 flash, meta and mistral label all five
`constructed-from-general-APR-knowledge`** — and their arithmetic is sound. Those are honest
constructed examples, exactly what the prompt said was acceptable, and they are correctly *not*
claiming Appendix J provenance.

### 3.2 GLOBE

**chatgpt VERIFIED 5/5**, and it is the only model to reproduce five distinct published examples with
every step closing:

```
5.2.1  Y1: 200 × (15% − 0%) = 30 ✓   Y2: 100 × 15% = 15 ✓  (ENTE carry-forward 15 established/used ✓)
5.3.7  1000 − 50 = 950 ✓ ; 950 − 500 = 450 ✓ ; 200×50% = 100, 200×45% = 90, remainder 10 ✓
       400×50% = 200, 400×45% = 180, remainder 20 ✓
5.5.2  annualise 12/6 = 2 ✓ ; (2 + 1 + 3)/3 = 2m ✓ ; (100 + 100 − 200)/3 = 0 ✓
9.1.1  10 / 20% = 50 ; 50 × 15% = 7.5 ✓ (×2 = 15) ✓
9.1.2  20% × 1000 = 200 ✓ ; 300/2000 = 15% ✓ ; 320/2000 = 16% ✓ ; (340 − 100)/2000 = 12% ✓
```

deepseek reproduces three of the same published examples with identical figures and adds a correctly
labelled constructed top-up example (120/1000 = 12%; 15 − 12 = 3%; 3% × 1000 = **30 ✓**).

**All 13 responding models VERIFIED on arithmetic.** No SELF-INCONSISTENT entries in GLOBE.

**WRONG-INPUT — the Article 9.2 transitional SBIE rates.** The models split on the constant:

| Rate pair claimed | Year assigned | Models |
|---|---|---|
| 10% payroll / 8% tangible | 2023 | meta, mimo |
| 9.8% / 7.8% | **2024** | minimax 2.7, sonnet, yuanbao |
| 9.6% / 7.6% | 2025 | sonnet |
| 9.8% / 7.8% | **2023** | glm 5.3 flash |
| **9.4% / 6.6%** | 2024 | deepseek |

Five models describe one self-consistent glide (10/8 in 2023 → 9.8/7.8 in 2024 → 9.6/7.6 in 2025).
**glm is one year out of step** on that schedule. **deepseek's pair cannot co-occur**: payroll and
tangible decline on separate monotone series from 10% and 8%, and 9.4/6.6 sits at different positions
on each — an internal inconsistency demonstrable without the source document.

The arithmetic using these rates closes in every case (200 × 9.4% = 18.8 ✓; 300 × 6.6% = 19.8 ✓;
50 × 9.8% = 4.9 and 200 × 7.8% = 15.6, SBIE 20.5 ✓). **Verdict: WRONG-INPUT (transitional-rate
constant) for deepseek and glm 5.3 flash; NEEDS-RETRIEVAL for the schedule itself** — the OECD table
was not retrieved in this pass and the majority reading is evidence, not ground truth.

**Direction check passes universally.** Every model that states a direction says the rates glide
**down**. No rate-direction reversals, and no top-up-allocation reversals.

---

## 4. Suspended and dropped models — explicit re-trial verdicts

### glm 5.3 flash — **SUSPENSION LIFTED for Class-1 work**

Suspended after submitting the same Alpha 21264 paper-recall text for eight consecutive prompts. On
Day 2 it produced **genuine, on-topic content for all three prompts it answered.** No wrong-content
recurrence.

Its OFAC file is among the best in the batch: **VERIFIED 5/5**, applying full attribution correctly,
and it is the only model to contribute a deliberate **gate case** — *"sub-50% intermediaries transmit
nothing"*, with two 40% intermediaries yielding zero attributed ownership to the target, which my
recomputation confirms exactly. Its "two parallel exactly-50% blocked intermediaries" case (A and B
each exactly 50%-owned, jointly conveying 55% to T) is the cleanest summation-through-attribution
vector produced by any model.

Its GLOBE and APPJ work is arithmetically sound and **honestly labelled** — all five APPJ cases as
`constructed-from-general-APR-knowledge`, three of four GLOBE as `probably-in-the-document`. Its one
defect is the **2023 transitional-rate assignment** (WRONG-INPUT, §3.2).

**Verdict: the wrong-content failure did not reproduce. Suspension lifted for deterministic-computation
work. Paper-recall reinstatement is not decided by this batch** — no recall prompt was run — and the
`trid` file is missing, which is a delivery gap, not a quality finding.

### minimax 2.7 — **DROP OVERTURNED for Class-1 work**

**VERIFIED 5/5 on TRID and 5/5 on OFAC**, with correct full-attribution treatment including a
three-tier cascade and a convergent two-intermediary case, both of which my fixpoint reproduces
exactly. GLOBE and APPJ arithmetic sound; APPJ honestly split across `probably` /
`confident-in-appendix-j` / `constructed`. No corruption in any of its four files — a change from the
token-level dropout recorded in earlier slices.

**Verdict: on Class-1 deterministic computation, minimax 2.7 performed at the level of the batch's
best. The drop was based on recall inversions and output-integrity failures; neither recurred here.
Recommend reinstatement for Class-1 work only.**

### minimax m3 — **DROP STANDS**

Content quality is not the problem: its single recovered TRID case verifies, and its OFAC
multiplicative choice is at least honestly flagged. **Three of its four files carry token-level
dropout:**

| File | The break |
|---|---|
| `trid` | `{"name": "…", "bucket": "ten_pct_aggregate", 500.00, "cd_amount": 350.00}` — the `"le_amount":` key is simply gone |
| `ofac` | `{"Co_Y", "blocked": false}` — the `"id":` key is gone |
| `appj` | a string value truncated mid-sentence and fused into the following key |

None is a truncation — all three files end with a proper `]`. Content resumes correctly after each
break, so this is serialization damage, not reasoning failure. It is the same class recorded in three
earlier slices. **Verdict: drop stands; the defect is delivery, and it has now persisted across five
collection days.**

### mimo — **DROP OVERTURNED on delivery; content caveat**

**mimo produced parseable JSON for all four prompts — the first time in the entire collection.**
Thirteen prior slices were prose refusals. TRID **VERIFIED 5/5**, and it is one of three models to
state the aggregate-vs-sum-of-increases distinction explicitly. OFAC 4/5 with one
self-contradictory case (§2.3).

**Verdict: the refusal behaviour did not reproduce. Reinstate.** Whatever changed in the delivery path
worked, and that fact is worth recording precisely because nothing in the artefacts explains it.

### chatgpt — **new wrong-content instance**

`chatgpt ofac.json` **contains its TRID content**: the object keys are `fees`, `violations`,
`clause_basis`, and the five case names are identical to its TRID file. Zero OFAC content.

This matters beyond one file. The wrong-content failure was diagnosed across eight slices as a
glm-specific defect. **It has now occurred in the model that has been the most reliable in the
collection**, which moves the diagnosis decisively away from "one bad model" and toward **a defect in
the collection or paste step**. chatgpt's other three Day-2 files are the strongest in the batch —
5/5 VERIFIED on GLOBE, 5/5 on APPJ with ten-significant-figure agreement, 5/5 on TRID.

**Verdict: OFAC NOT ASSESSABLE (wrong content). No quality inference drawn against chatgpt.** The
target-content pre-check recommended after the glm findings would have caught this instantly and is
now unambiguously required.

---

## 5. Honesty-label audit

**`weakest_point` populated on 55/55 files and on every individual item — 100% adoption.** Second
batch running (Prompt P scored 91%), and the first at complete coverage.

**Are they the actual weakest points?** Scored against my recomputation findings:

| Quality | Count | Examples |
|---|---|---|
| **Names the true fault line** | ~40% | gemini's OFAC entry naming the US-multiplicative vs EU-attribution distinction — the exact axis on which it is wrong; minimax m3 flagging its multiplicative reading as *"unsure in spirit"*; deepseek's *"transitional rates vary by year; this example assumes 2024 rates"* — precisely the constant that is wrong; yuanbao's TRID entries flagging bucket assignment as premise-dependent, which is the genuinely uncertain part |
| **Real but secondary** | ~45% | chatgpt's GLOBE 5.3.7 note that the example allocates SBIE inputs rather than computing the carve-out — true, not a weakness |
| **Boilerplate** | ~15% | *"real-world applications may be more complex"* (deepseek GLOBE 5.5.2); *"omits potential impact of valuation allowances"* |

**No missing or evasive labels.** Notably, **deepseek's TRID case 2 — the one SELF-INCONSISTENT entry
in the batch — does not flag the input substitution in its `weakest_point`.** The field caught the
GLOBE rate risk in the same file and missed the defect that actually invalidated an entry. Consistent
with the standing finding: `weakest_point` predicts what a reviewer will attack, but only where the
model perceives uncertainty; it does not catch mechanical self-contradiction.

---

## 6. Anti-reversal check

**One flag across 55 files.**

**yuanbao, TRID case 1.** `case_name`: *"Mixed-direction 10% bucket — **aggregate passes** despite one
large increase."* Its own computation and verdict: *"VIOLATION — aggregate CD 1100 exceeds permitted
1012 by 88."*

```
Σle = 920 ; Σcd = 1100 ; threshold = 92 ; allowed = 1012 ; 1100 > 1012 → violation, cure 88 ✓
```

The arithmetic is **VERIFIED**; the narrative label contradicts it. This is the D2 failure shape at
its mildest — a title that says the opposite of the computed result — and it is exactly what the
anti-reversal check exists to surface. Its second case, correctly named *"aggregate passes"*, does
pass, which suggests a label carried over rather than a misunderstanding.

**No other reversals.** No GLOBE rate-direction reversals, no top-up-allocation reversals, no OFAC
verdict contradicting its own aggregate, no APPJ narrative contradicting its solved rate.

---

## 7. Harvest — candidate fixture material

Listed by file and prompt; content not copied.

| Source | Why it is fixture-grade |
|---|---|
| `chatgpt appj.json` — cases 1–4 | Stated periodic rates match independent bisection to **1e-10**. Covers regular monthly, long odd first period (f = 19/30), single-advance-single-payment via Form 1, and irregular first-and-final payments. Four distinct Appendix J code paths with exact expected values |
| `yuanbao appj.json` — cases 3–4 | The only closed-form vectors: Form 1 for a sub-year single payment and **Form 3** `I = 100[(P/A)^(1/t) − 1]` for a 2-year term. Both verify exactly and need no iterative solver — ideal regression anchors |
| `glm 5.3 flash ofac.json` — the gate case and the two-parallel-50% case | The gate case (two 40% intermediaries transmitting **nothing**) is the only negative-control vector in the OFAC set; the parallel-50% case is the cleanest summation-through-attribution test. Together they pin the attribution rule from both sides |
| `sonnet ofac.json` — cases 2 and 5 | Near-miss aggregates at **35%** and **47%** — the boundary-adjacent cases that catch an off-by-one in the ≥50% comparison. No other model produced a 47% case |
| `kimi trid.json` — cases 2 and 3 | Matched pair on the same bucket structure: mixed directions passing (sum-of-increases 250, aggregate −50) and failing (sum-of-increases 500, aggregate +300). Discriminates the aggregate test from the sum-of-increases defect in a single before/after pair |
| `chatgpt globe.json` — Examples 5.5.2 and 9.1.2 | 5.5.2 exercises short-year annualisation and a **two-condition** de minimis test landing at exactly EUR 0 income; 9.1.2 exercises a grace-period limitation across three years with a state change in the third. Both close fully and both have branch structure, not just arithmetic |
| `qwen trid.json` — case 2 | +400 and −400 inside one bucket: aggregate delta exactly zero while sum-of-increases is 400. The single sharpest discriminator for the load-bearing rule |

**Not harvested:** anything depending on an unretrieved constant — all GLOBE transitional-rate cases,
and any OFAC case whose verdict turns on the attribution-vs-multiplication question, until the
guidance text is retrieved.

---

## 8. Summary

| Prompt | Files | VERIFIED | SELF-INCONSISTENT | WRONG-INPUT | WRONG-RULE | Not assessable |
|---|---|---|---|---|---|---|
| TRID | 13 | 12 models fully | 1 case (deepseek) | — | — | — |
| OFAC | 14 | 9 models fully | 4 cases (mistral 3, mimo 1) | — | 1 case (gemini) | 1 file (chatgpt) |
| GLOBE | 14 | all 13 responding | — | 2 models (rate constant) | — | — |
| APPJ | 14 | all 13 responding | — | — | — | 1 case INDETERMINATE |

**Class-1 prompts work.** Requiring step-by-step arithmetic made adjudication mechanical: **six
defects in roughly 250 computations, every one of them located to an exact step.** The three
categories of failure are cleanly separated — a broken artefact (deepseek's substituted table), a
misapplied legal rule with flawless arithmetic (gemini's multiplication), and an incomplete answer
field over correct work (mistral's omitted intermediaries) — and only the first is detectable by
recomputation alone.

**Two constants remain unretrieved and block use of the affected material:** the Article 9.2
transitional SBIE glide table, and OFAC's indirect-ownership treatment. Both are single retrievals.
