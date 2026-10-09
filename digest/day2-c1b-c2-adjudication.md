# Day 2 second batch — IRB · FRTB · MICA · CCD2 · RECEIPT · JCS (+ Solar cross-add)

**Input:** `../Web Model Tasks/Day 2/` — **86 files, 15 models × 6 prompts** (six absences, enumerated
in §7), plus `solar trid.json` / `solar ofac.json` cross-added to the first batch.
**Method:** identical to `day2-c1-adjudication.md`. Every shown computation re-executed
independently; verdict vocabulary VERIFIED / WRONG-INPUT / SELF-INCONSISTENT / WRONG-RULE /
INDETERMINATE; recomputation is the verdict and cross-model agreement is evidence only.

**Tooling, stated once.** The four C1 prompts were re-executed in scratch Python (CRE31 closed form
with `statistics.NormalDist`; normal-ES multipliers; a bisection APRC solver). The JCS slice was
graded against a **scratch RFC 8785 canonicalizer written for this pass** — not manual rule
application — self-tested first against the RFC's own published number vectors (`1e21` → `1e+21`,
`1e-7` → `1e-7`, `0.000001` → `0.000001`, `1e20` → `100000000000000000000`, `-0` → `0`,
`9007199254740992` → itself, `333333333.33333329` → `333333333.3333333`) and against UTF-16 key
ordering (`{"€","$","ü"}` → `$`, `ü`, `€`). All seven pass. The RECEIPT slice is the one prompt in
this batch with **no mechanical judge** — see §6, which corrects the commission's premise.

---

## 1. IRB — Basel CRE31 corporate risk-weight formula

Reference recomputation (LGD 45%, M 2.5, Φ⁻¹(0.999) = 3.090232):

| PD | R | b | Φ⁻¹(PD) | inner | Φ(inner) | **K** | **RW** |
|---|---|---|---|---|---|---|---|
| 0.5% | 0.213456 | 0.167086 | −2.575829 | −1.294550 | 0.097738 | **5.5689%** | **69.612%** |
| 1.0% | 0.192784 | 0.137486 | −2.326348 | −1.079100 | 0.140273 | **7.3853%** | **92.317%** |
| 3.0% | 0.146776 | 0.096478 | −1.880794 | −0.754400 | 0.225290 | **10.2750%** | **128.438%** |
| 10.0% | 0.120809 | 0.059856 | −1.281552 | −0.221300 | 0.412446 | **15.4470%** | **193.087%** |

The 92.317% at PD 1% reproduces the ≈92% figure the prompt names as its benchmark, so the reference
is anchored, not merely self-consistent.

### VERIFIED 4/4 — seven models

**chatgpt · deepseek · grok · meta · qwen · sonnet · kimi.** chatgpt, grok and meta agree to the
15th significant figure (`5.568938909768941`, `69.61173637211176`) — floating-point identity, not
agreement to 4dp. deepseek, qwen and kimi agree to 4dp; sonnet to ~3dp (15.4187 vs 15.4470 at PD 10%,
a normal-CDF precision difference, not a rule difference).

**kimi is the only model that cross-checks against published Basel material** rather than asserting a
benchmark: it takes the CRE99.2 worked example at LGD 40%, scales linearly to LGD 45%, and lands on
69.62% / 92.32%. That is the correct scaling (K is linear in LGD) and the correct figures.

> *Checker note.* My batch extractor read kimi's PD 0.5% case as PD 50% and skipped its PD 1% case —
> a field-name collision in my code, not a defect in kimi's file. Hand-checked: 4/4 exact. This is
> the third time in this collection that an automated checker has produced false failures; the miss
> rate is reported rather than hidden, and no failure in this document is reported unless
> hand-confirmed.

### 1.1 gemini — SELF-INCONSISTENT on one case, and the honesty field ratified the error

gemini's `formula_basis` is **correct**. Three of four cases are exact (7.39 / 10.28 / 15.45 and
92.35 / 128.44 / 193.1). The PD 0.5% case fails:

```
gemini writes:  (−2.575829 + 0.461987 × 3.090232) / 0.886887 = −1.293392 / 0.886887 = −1.458350
recomputed:      −2.575829 + 0.461987 × 3.090232 = −1.148102
correct inner:   Φ⁻¹(PD)/√(1−R) + √(R/(1−R))·Φ⁻¹(0.999)  =  −1.294550
```

The number it puts in the *numerator* slot, −1.293392, is the correct **final** inner value. It then
divides by √(1−R) a second time. Result: Φ(−1.458350) = 0.072372 instead of 0.097738, K 4.05% instead
of 5.5689%, RW 50.57% instead of 69.612%.

**The finding is not the slip — it is what the honesty field did with it.** gemini's `known_benchmark`
reads: *"Standard BCBS CRE31 corporate risk-weight curve yielding ~50.6% RW at 0.5% PD. Matches
accurately."* There is no such published anchor at 50.6%; the real curve gives 69.6%. The model
manufactured a benchmark that confirms its own wrong number, in the field designed to catch exactly
this. Its `weakest_point` then names *"precision of numerical approximation for standard normal
inverse CDF"* — the one thing that was not wrong.

**Verdict: SELF-INCONSISTENT ×1, with a fabricated corroborating benchmark.** The other three cases
stand.

### 1.2 The grouping error the prompt predicted — four models, four different spellings

The prompt anticipated confusion between `Φ⁻¹(PD)/√(1−R)` and `√(1−R)·Φ⁻¹(PD)`. Four models fell in,
and each one wrote the defect openly in its own `formula_basis`:

| Model | Stated formula fragment | Effect |
|---|---|---|
| **yuanbao** | `G(PD)*sqrt(1-R) + sqrt(R)*G(0.999)` | multiplies where it must divide → K 8.578% vs 4.1732% at M=1 |
| **solar** | `x = Φ⁻¹(PD) + √R × Φ⁻¹(0.999)` | omits the `/√(1−R)` entirely |
| **minimax 2.7** | `N(sqrt(1-R)*Phi^{-1}(PD) + …)` | multiplies, **plus** three further defects (below) |
| **mistral** | `× (1 + (M − 2.5)·b)` | the `/(1 − 1.5b)` divisor is absent **from the formula itself** |

**yuanbao — WRONG-RULE 4/4.** Its inputs use M = 1, and it correctly observes that M = 1 makes the
maturity adjustment exactly 1.0 (numerator = denominator). Correct K at M = 1 is
4.1732 / 5.8623 / 8.7880 / 14.0601%; yuanbao reports 8.578 / 9.981 / 11.691 / 15.719%. The arithmetic
is internally exact under its own (wrong) grouping.

**solar — WRONG-RULE 4/4, plus a units defect.** Its stated `b` is invented:
`(0.11852 − 0.05478·ln PD)²·(1−e^(−M/10))/M` — the second factor does not exist in CRE31 — and the
maturity term is `× (1 + b)` rather than `× (1+(M−2.5)b)/(1−1.5b)`. Its result object mixes units
inside one record: `k_pct: 0.054991` is a **ratio** while `risk_weight_pct: 68.7388` is a true
percent. The two are internally consistent (0.054991 × 12.5 × 100 = 68.74), so the object is coherent
and the field name is wrong.

**mistral — WRONG-RULE 4/4, plus a units defect, plus the batch's only `weakest_point: "None"`.**
Because the `/(1−1.5b)` divisor is missing, at M = 2.5 the maturity factor collapses to exactly 1 and
`K_before_maturity_adjustment` equals `K_after_maturity_adjustment` (both 0.041731993996807645) —
visible on the face of its own record. It reports `risk_weight_pct: 0.5216499249600955`, a ratio in a
percent field. It is the only model in 86 files to answer the honesty field with `"None"`.

**minimax 2.7 — WRONG-RULE 4/4 with four independent defects in one formula string:**

1. `sqrt(1-R)*Phi^{-1}(PD)` — the grouping error.
2. `b(PD) = 0.11852 - 0.05478*ln(PD)^2` — squares only the log, not the bracket, producing
   **b = −1.419273**. A negative correlation-slope term is facially impossible; nothing flagged it.
3. Invents a maturity factor `(1/M)^{1/6}` = 0.858374 that appears in no version of CRE31.
4. `phi_inv_PD: -2.3263` for PD = 0.005. That is Φ⁻¹(0.01). A **WRONG-INPUT** on top of the
   wrong rule.

**But minimax 2.7 caught itself.** Its `known_benchmark` reads: *"Published: ~45%, Computed: 54.99%,
COMPUTED DOES NOT MATCH KNOWN BENCHMARK"* and its `weakest_point` says the computed RW exceeds the
published estimate. It is wrong four ways and says so. This is the exact inverse of gemini, and the
pair is the most useful thing in the IRB slice: **the honesty fields are not weakly correlated with
correctness — they are independent of it in both directions.**

### 1.3 minimax m3 — SELF-INCONSISTENT, and the rationalization cites a fabricated table

Its `R` is wrong (0.200023 against 0.213456 — the 0.24 term is multiplied by 0.72283 instead of
0.77880). Downstream it computes a negative capital requirement, floors K to 0.0, and then explains
the zero with:

> *"Basel CRE31 grid (BCBS 128, Table 1) gives RW ≈ 53.4% … the raw formula … produces K which
> becomes negative (PD-floor case) … the disagreement is the floor convention, not the algebra."*

The raw formula does not produce a negative K at PD 0.5%; it produces 5.5689%. There is no PD-floor
question here (the 0.03% floor binds far below 0.5%). The model wrote a regulatory-convention
narrative, with a specific document and table citation, to explain away its own arithmetic slip —
and asserted in its `weakest_point` that *"the disagreement is the floor convention, not the
algebra."* It was the algebra.

**Verdict: SELF-INCONSISTENT, with fabricated authority.** This is the same shape recorded in
`narrative-vs-record` terms elsewhere in the digest: a self-sealing comment that certifies the record
it contradicts.

### IRB summary

| Verdict | Models |
|---|---|
| **VERIFIED 4/4** | chatgpt, deepseek, grok, kimi, meta, qwen, sonnet **(7)** |
| **VERIFIED 3/4 + SELF-INCONSISTENT 1** | gemini |
| **WRONG-RULE 4/4** | mistral, solar, yuanbao, minimax 2.7 |
| **SELF-INCONSISTENT** | minimax m3 |
| **no data** | glm 5.3 flash, mimo (files absent) |

---

## 2. FRTB — MAR33 expected shortfall

**The named defect class did not occur anywhere.** Not one of the fourteen files conflates ES with
VaR — no model uses 1.959964 as a multiplier. Every model that shows the constants gets them right:

| Constant | Correct | Models asserting it |
|---|---|---|
| φ(1.959964) | 0.058445 | 12 of 14 |
| φ(2.326348) | 0.026652 | 11 of 14 |
| ES₉₇.₅ multiplier = φ(z)/(1−α) | **2.337803** | **14 of 14** |
| ES₉₉ multiplier | **2.665214** | 12 of 14 |
| √(20/10) liquidity scaling | 1.414214 | 11 of 14 |

meta (3 of 7 anchors) and solar (2 of 7) show fewer constants because both files are structured as
prose-heavy nested objects rather than per-case records — a presentation difference, not an error;
their shown ES multipliers are correct.

**Every historical-simulation case names its fractional-observation convention explicitly** —
half-weight, ceiling-to-1, or linear interpolation between order statistics — which is the one place
an HS ES can silently differ by a full observation. No model left it implicit.

**Verdict: VERIFIED across the slice.** No WRONG-RULE, no SELF-INCONSISTENT, no INDETERMINATE. This
is the cleanest of the six prompts, and the clean result is itself the finding: a prompt built around
a specific confusion found that the confusion is not present in any current model.

---

## 3. MICA — reserve of assets

**Stress arithmetic closes in every file.** Spot examples, each recomputed:

```
60 + 38 + 16 = 114 ; 114/120 = 0.95      coverage 95%
45 + 39.9 + 11.9 = 96.8 ; 96.8/100 = 0.968
40 + 47.5 + 11.64 = 99.14 ; 99.14/100 = 0.9914
```

**`tail_convention` is present on every case of every model** (13 of 13 files; 4/4 cases each, except
where a nested-object layout collapses the count — see the parse note in §7). **Every model tests the
LOW/adverse tail for coverage.** The wrong-tail trap — computing coverage against the favourable tail,
which would make a thin reserve look adequate — did not fire once.

### 3.1 The own-funds figures are consensus, not verified — NEEDS-RETRIEVAL

Nine of thirteen files assert **EUR 350,000** as the fixed own-funds floor, and the same nine assert
**2% of the average reserve amount** as the alternative limb. Four (mistral, qwen, solar, sonnet) do
not state the figure at all.

**No model retrieved the text; this document does not either.** Nine-way agreement across models with
correlated training data is not evidence — the corpus has already recorded one case where thirteen
models agreed on a wrong constant. **Flagged NEEDS-RETRIEVAL: MiCA Title III own-funds floor and the
percentage limb, from the Regulation text.** Until that retrieval happens, no MICA case whose verdict
turns on the own-funds threshold should be promoted to fixture status.

### 3.2 Honest-uncertainty behaviour

qwen (4 flags), minimax 2.7 (3), sonnet (2), minimax m3 (1), mistral (1) used explicit
`UNKNOWN-CURRENT-VALUE` markers rather than asserting the threshold. **mistral gave
`article_basis: null` on all four cases** — the prompt permits it, and given that mistral's substantive
answers in this batch are the weakest, the null is the correct output, not a gap. Credit where the
label is load-bearing: on MICA, mistral's honest null is worth more than the nine confident 350,000s.

**Verdict: stress arithmetic VERIFIED across the slice; own-funds claims INDETERMINATE pending
retrieval.**

---

## 4. CCD2 — Consumer Credit Directive APRC

Recomputed by bisection on `Σ aₜ/(1+X)^tₜ = Σ bₜ/(1+X)^sₜ` with t in years — the CCD/CCD2 compound
form.

### VERIFIED — eight models

| Model | Result |
|---|---|
| **chatgpt** | 4/4 — 15.4489 / 19.9502 / 15.1289 / 20.0000 against stated 15.4 / 20.0 / 15.1 / 20.0 |
| **grok** | 5/5 |
| **qwen** | 5/5 |
| **yuanbao** | 5/5 |
| **mimo** | 5/5 |
| **sonnet** | 4/4 **+ 1 honest UNKNOWN** — declines to assert a numeric APRC on the case it cannot close, rather than producing one |
| **solar** | 1/1 — the 0% case: `Σ 83.3333/(1+X)^(k/12) = 1000` at X = 0. Correct, and the only zero-rate vector in the slice |

### 4.1 mistral — WRONG-RULE **and** SELF-INCONSISTENT (the same case, twice over)

mistral discounts with **simple interest**:

```
mistral:   10000 = 10500 / (1 + APRC × 365/365)     → its own equation solves to APRC = 5.00%
CCD form:  10000 = 10500 / (1 + X)^1                → X = 5.00%
mistral reports:  4.76%                             ( = 500/10500, the discount rate )
```

Two independent defects stacked: the wrong discounting convention (which happens to coincide with the
compound answer at exactly one year — so the rule error is invisible on this case and lethal on the
others), and then a reported figure that is not the solution to its own stated equation. 4.76% is
500/10500 — the *discount* rate, not the interest rate. **3 of 3 assessable cases.**

This is the same defect signature recorded for mistral in `hw-calc-formulas.md` (the inverted SPFM),
and now in §1.2 above (the dropped `/(1−1.5b)`): **mistral writes a formula that is missing a term,
computes it correctly, and reports a third number.**

### 4.2 deepseek — SELF-INCONSISTENT ×3: the equations reproduce, the answers do not

```
case 1:  12 × 879.16 on 10000   → recomputed APRC 10.4716%   deepseek states  5.0%
case 2:  12 × 879.16 on  9500   → recomputed APRC 21.7103%   deepseek states  8.2%
case 3:  12 ×  88.85 on  1000   → recomputed APRC 12.6854%   deepseek states  8.1%
```

879.16 is the exact annuity payment for 10 000 over 12 months at a **10% nominal** rate
(0.8333%/month). deepseek built a 10%-nominal schedule and then reported roughly half of it. Its
overdraft case verifies. The payment schedules are right, the equations are right, the answers are
disconnected from both.

### 4.3 gemini — SELF-INCONSISTENT ×3, nominal reported as effective

```
recomputed 10.4810%  vs stated 10.0%      ( 87.92/month on 1000 = the 10%-nominal annuity )
recomputed 21.7209%  vs stated 20.5%
recomputed 20.0392%  vs stated 20.4%
```

The first two are the nominal rate reported in the APRC field — the single most common real-world
APRC error, and the one the Directive exists to prevent. The third (0.36pp) is a solver-precision
difference, not a rule difference.

### 4.4 minimax m3 — SELF-INCONSISTENT ×3, one presented as a published annex example

```
86.27 × 12 on 1000  →  recomputed 6.6363%   stated 12.5%   ← labelled as an Annex worked example
recomputed 11.6253% vs stated 12.64%
recomputed 10.3647% vs stated  9.92%
```

The 12.5% is asserted as coming from the Directive's own annex with "explicit published numbers." The
schedule it publishes alongside yields 6.64%. Same shape as §1.3: **a citation attached to a number
that the model's own data contradicts.**

### 4.5 minimax 2.7 — WRONG-RULE ×2, self-consistent under a declared wrong convention

Its equation discounts as `(1 + APRC/12)^t` with t in **months** — nominal-monthly compounding, not
the CCD's `(1+X)^(t in years)`. Recomputed under the CCD form: 24.5236% and 19.7469% against its
stated 22.1% and 18.2%. Its numbers are right for the convention it wrote down. The convention is the
wrong one, and unlike the tail-convention discipline shown across the MICA slice, it is not flagged.

### CCD2 summary

| Verdict | Models |
|---|---|
| **VERIFIED** | chatgpt, grok, qwen, yuanbao, mimo, sonnet, solar, meta **(8)** |
| **SELF-INCONSISTENT** | deepseek (3), gemini (3), minimax m3 (3) |
| **WRONG-RULE** | minimax 2.7 (2), mistral (3 — plus self-inconsistency) |
| **no data** | kimi, glm 5.3 flash (files absent) |

---

## 5. JCS — RFC 8785 canonicalization

208 vectors across 15 files, every one canonicalized by the scratch implementation and compared
byte-for-byte. Three grading classes were needed:

- **WRONG** — a substantive divergence: number serialization, key order, or an escaping *rule*.
- **FORM** — the substance is right but the output is `\uXXXX`-escaped where RFC 8785 §3.2.2.2
  requires literal UTF-8 (JSON.stringify escapes only `"`, `\`, and controls below U+0020). A real
  defect against the spec, and a different one from getting the rule wrong.
- **not counted** — the duplicate-key vectors. RFC 8785 §3.1 requires duplicate-free input and
  defines no canonical form for it; models answering `null`, `ERROR`, or "REJECTED" are on firmer
  ground than my parser's last-wins. Excluded from the denominator in both directions.

| Model | OK | FORM | WRONG | score | note |
|---|---|---|---|---|---|
| **solar** | 17 | 2 | 0 | **17/19** | largest set (21 vectors); both misses are escaping form |
| **deepseek** | 13 | 0 | **2** | 13/15 | the only **key-order** failure in the batch — see §5.1 |
| **kimi** | 12 | 0 | 0 | **12/12** | flawless |
| **sonnet** | 12 | 0 | 0 | **12/12** | flawless |
| **chatgpt** | 10 | 1 | 0 | **10/11** | recovered only by salvage — see §5.4 |
| **grok** | 10 | 1 | 0 | 10/11 | |
| **meta** | 10 | 0 | 0 | **10/10** | one vector has an empty `input_json`; its stated output for it is correct |
| **mimo** | 9 | 2 | 0 | 9/11 | |
| **yuanbao** | 9 | 2 | 0 | 9/11 | |
| **qwen** | 9 | 0 | 1 | 9/10 | `-0` preserved |
| **glm 5.3 flash** | 9 | 0 | 2 | 9/11 | see §5.2 |
| **gemini** | 6 | 2 | 0 | 6/8 | |
| **minimax m3** | 6 | 0 | 3 | 6/9 | 2 vectors have malformed `input_json` |
| **minimax 2.7** | 5 | 2 | 3 | 5/10 | |
| **mistral** | 3 | 2 | 6 | **3/11** | six substantive failures — see §5.3 |

### 5.1 The UTF-16 ordering trap: 6 of 7 models got the *hard* part right

The vector class the prompt was built around — sorting keys by UTF-16 code units, so a supplementary-
plane character (leading surrogate D800–DBFF) sorts **before** U+E000 even though its code point is
far higher — was answered correctly by **grok, glm 5.3 flash, gemini, mimo, minimax 2.7, minimax m3
and yuanbao**. Seven models constructed the trap and stepped around it.

**deepseek is the sole failure, and it fails in both directions:**

```
input   {"𐀀":1,"":2}       U+10000 = D800 DC00 ;  D800 < E000
correct {"𐀀":1,"":2}                    U+10000 first
deepseek {"":2,"𠀀":1}                U+E000 first — code-point order, the trap
```

It also mis-transcribes U+10000 (𐀀) as U+20000 (𠀀) in both of its ordering vectors — a second,
independent error inside the same case. Its `certainty` on both is `rfc-exact`.

### 5.2 glm 5.3 flash stated the rule and then broke it in the same record

```
vector_name:      "No Unicode normalization: canonically equivalent keys stay distinct"
input:            {"Ω":1,"Ω":2}          U+03A9 GREEK OMEGA, U+2126 OHM SIGN
glm's output:     U+03A9, U+03A9                    ← both keys emitted as U+03A9
correct:          U+03A9, U+2126                    ← distinct code points, order preserved
```

It NFC-normalized U+2126 → U+03A9 while writing a vector whose entire purpose is to show that a
canonicalizer must **not** normalize. **Anti-reversal instance: the narrative field contradicts the
model's own output, in the same object.**

### 5.3 mistral — six substantive failures, spanning every rule family

| Vector | mistral | correct | rule broken |
|---|---|---|---|
| `large_integer` | `9007199254740993` preserved | `9007199254740992` | numbers are IEEE-754 doubles; 2⁵³+1 is not representable |
| `exponent_boundary` | `1E+21`, `1E-21` | `1e+21`, `1e-21` | ECMAScript emits lowercase `e` |
| `tiny_decimal` | `1E-7` | `1e-7` | same |
| `solidus_escaping` | `a\/b` | `a/b` | JSON.stringify does not escape `/` |
| `utf16_ordering` | U+E000 before 😀 | 😀 first | UTF-16 code-unit order |
| `nested_structures` | `{"a":{"b":[]},"c":[{}]}}` | `{"a":{"b":[]},"c":[{}]}` | an extra `}` — the deliverable is not valid JSON |

Every one carries `certainty: rfc-exact`. Combined with §1.2 and §4.1, mistral is the only model in
this batch that is bottom-quartile on **all three** of arithmetic, rule application, and output
integrity.

### 5.4 chatgpt — the file was not bad, the quoting was: a sixth salvage technique

`chatgpt jcs.json` initially yielded 33 unusable fragments of the shape `{"n": 0}`. Cause: every
string value embeds a JSON document with its **inner double quotes unescaped** —

```
"input_json": "{"n":-0}",
```

so the parser terminated each value at the first inner quote. A line-wise re-escape recovers **12
clean vectors**, and the content is among the best in the slice: `-0` → `0` ✓, `9007199254740993` →
`9007199254740992` ✓, `1e20` → full digits and `1e21` → exponential ✓, and `duplicate-key` answered
`REJECTED — no JCS canonical serialization`, which is the RFC-correct response. **10/11.**

**Salvage-ladder extension.** This pass added three techniques to the five already recorded:

| # | Shape | Seen in |
|---|---|---|
| 6 | **unescaped inner double quotes** inside string values | `chatgpt jcs.json` (33 fragments → 12 clean vectors) |
| 7 | **a `"key": "value"` pair sitting inside an array** of strings | `sonnet receipt.json` |
| 8 | **raw literal newlines inside string values** | `yuanbao receipt.json` |

Techniques 6 and 8 are emission bugs a stricter serializer would prevent; technique 7 is a schema
slip. All three were invisible to bracket-balancing and to truncation repair. **Without them, three
files — one of which is a top-quartile answer — would have been scored as absent.**

---

## 6. RECEIPT — risc0 receipt anatomy

### 6.1 A correction to the commission

The commission directs: *"grade structural claims against the actual receipt format the prompt embeds
— every field-role claim is checkable against the prompt's own material."* **The prompt embeds no
receipt.** `PROMPT-C2-RECEIPT-ANATOMY.md` names a hint list inside its schema (image id, journal
digest, exit code, input/output digests, control root, verifying key) and states that answers "will be
checked against real risc0 receipts and the risc0 source/docs" — material that is not in this
workspace and was not retrieved for this pass.

**There is therefore no mechanical judge for this slice**, and I will not manufacture one from my own
recollection of the risc0 codebase and present it as ground truth. What follows is coverage,
internal-consistency and convergence analysis, with the substantive claims marked NEEDS-RETRIEVAL.

### 6.2 Coverage — 15 of 15 files complete, after salvage

All fifteen files carry all seven required sections and a per-section `certainty_notes` object.
`meta`, `sonnet` and `yuanbao` reached 7/7 only via salvage techniques 4, 7 and 8 respectively; before
salvage all three scored zero sections and would have been misread as non-responses.

### 6.3 The field lists disagree, and the disagreement is the finding

| Field asserted at the top level of a Groth16 receipt | Models |
|---|---|
| `seal` | 11 |
| `claim` | 10 |
| `verifier_parameters` | 3 — deepseek, grok, mimo |
| `journal` | 2 — gemini, solar |
| `control_id` | 2 — mistral, qwen |
| **each of 17 further names** | **1 each** |

Ten models converge on `{seal, claim}` with a third field disputed three ways. Seventeen field names
are **single-source** — asserted by exactly one model and contradicted by silence from the other
fourteen. Single-source structural fields are the highest-risk material in this slice and none should
enter a fixture.

**minimax 2.7 is the clearest invention case:** it lists nine top-level fields — `a[0]`, `a[1]`,
`b[0..2]`, `c[0..1]`, `public_inputs[]`, `image_id`, `claim_digest`, `journal`, `exit_code`,
`post_state_digest` — i.e. it flattens the Groth16 proof's internal group elements *and* the claim's
components into the receipt struct. No other model does this. Whatever the true layout, a receipt
cannot simultaneously carry `claim` and its decomposed members as siblings.

### 6.4 Two files carry source-level detail the other thirteen do not

**meta** is the outlier by a distance: it names tagged-hash domain separators (`risc0.ReceiptClaim`,
`risc0.Output`), the 4-byte **selector** prefix on the encoded seal, the 128-bit split of the claim
digest into BN254 field elements, `imageId` as the **pre-state** digest rather than a receipt field,
and marks `control_root` / `BN254_CONTROL_ID` explicitly as *"verifier parameters, not in receipt but
in public inputs"* — the distinction most of the batch elides. 12 binding-chain steps; 25 mentions of
assumptions. **grok** is second, with the selector, the tagged-hash tag name, the 128-bit split and
the imageId/pre-state identification.

Only **meta and grok** identify imageId with the pre-state digest at all. If that identification is
correct, then every model listing `image_id` as a sibling of `claim` has the containment wrong.

**Verdict: NOT ADJUDICATED — no ground truth available.** Convergence is recorded, single-source
fields are flagged, and this slice is the highest-value retrieval target in the batch (§8).

---

## 7. Grid, absences, and the honesty audit

### 7.1 Delivery grid — six absences, all no-data

| model | irb | frtb | mica | ccd2 | receipt | jcs |
|---|---|---|---|---|---|---|
| chatgpt | 4 | 4 | 4 | 4 | ✓ | 33→12 |
| deepseek | 4 | 4 | 4 | 5 | ✓ | 16 |
| gemini | 4 | 4 | 4 | 4 | ✓ | 8 |
| **glm 5.3 flash** | **–** | **–** | **–** | **–** | ✓ | 12 |
| grok | 4 | 8 | 4 | 5 | ✓ | 12 |
| kimi | 4 | 4 | 4 | **–** | ✓ | 12 |
| meta | 4 | ✓ | 4 | ✓ | ✓ | 12 |
| **mimo** | **–** | 4 | 4 | 5 | ✓ | 12 |
| minimax 2.7 | 4 | 4 | 4 | 5 | ✓ | 11 |
| minimax m3 | ✓ | 5 | ✓ | 5 | ✓ | 12 |
| mistral | 4 | 4 | 4 | 3 | ✓ | 12 |
| qwen | 4 | 4 | 4 | 5 | ✓ | 11 |
| solar | 4 | ✓ | 4 | ✓ | ✓ | 21 |
| sonnet | 4 | 4 | 4 | 5 | ✓ | 12 |
| yuanbao | 4 | 4 | ✓ | 5 | ✓ | 12 |

**Six absent files, exactly as the commission predicted:** glm 5.3 flash × {irb, frtb, mica, ccd2},
kimi/ccd2, mimo/irb. **These are no-data, not failures.** No verdict of any kind is recorded against
a model for a file that did not arrive, and glm 5.3 flash's Class-1 standing — reinstated in the first
batch — is unaffected by four absences here.

A `✓` above marks a file whose cases are nested inside a single top-level object rather than an array,
so a per-case count is not meaningful; content was graded, the count was not.

### 7.2 `weakest_point` and per-section certainty — 100% adoption, zero predictive value

Every case in every C1 file carries at least one honesty field; every receipt file carries a
per-section `certainty_notes`; every JCS vector carries a `certainty`. **Adoption is complete and
adoption is not the question.**

Median honesty-text length per model (characters, C1 prompts, irb/frtb/mica/ccd2):

```
solar    341 / 532 /1495 / 183       sonnet   530 / 441 /1048 / 372
meta     365 / 194 / 964 / 182       minimax m3  709 / 195 /  0 / 376
minimax 2.7  309 / 353 / 811 / 316   kimi     330 / 153 / 668 / –
mimo       – / 267 / 956 / 227       qwen     225 / 247 / 527 / 195
grok     224 /   0 / 533 / 135       yuanbao  270 / 109 / 434 / 204
chatgpt  149 / 197 / 738 / 263       gemini   213 / 125 / 336 / 100
deepseek  59 /  61 / 541 / 102       mistral   14 /   4 /  45 /   4
```

**mistral's labels are effectively empty** (4–45 characters, including the batch's only
`weakest_point: "None"`), and mistral is the batch's weakest model on substance. That is the single
correlation in the table — and it runs through *absence* of a label, not through what any label says.

**Among models that write real labels, the field is uninformative in both directions:**

| | Example |
|---|---|
| **Long, specific, and wrong** | gemini's IRB `known_benchmark` invents a 50.6% anchor to confirm its own miscomputation (§1.1). minimax m3's CCD2 annex citation and its IRB "BCBS 128 Table 1" both attach a document to a number its own data contradicts (§1.3, §4.4) |
| **Long, specific, and right about being wrong** | minimax 2.7's IRB `known_benchmark`: *"COMPUTED DOES NOT MATCH KNOWN BENCHMARK"* — four rule errors, correctly flagged (§1.2) |
| **Right about the real fault line** | solar's OFAC `weakest_point` names full-attribution-vs-multiplicative as the load-bearing interpretive risk — which is exactly where it is wrong (§8.2). qwen's four MiCA `UNKNOWN-CURRENT-VALUE` flags sit on the one figure this document marks NEEDS-RETRIEVAL |
| **Silent on the actual defect** | mistral's `weakest_point: "None"` on a case with a missing formula term, a wrong reported figure, and a units error |

### 7.3 Anti-reversal check

**Two instances, both inside a single record:**

1. **glm 5.3 flash, JCS.** Vector titled *"No Unicode normalization"*; the model's own output
   normalizes U+2126 → U+03A9 (§5.2).
2. **gemini, IRB.** `known_benchmark` asserts *"Matches accurately"* against a benchmark that does not
   exist and a value that is 19 percentage points wrong (§1.1).

No reversals in FRTB, MICA or CCD2. The rate is far below the D2-era 19% and consistent with the
post-P-slice 3.6% measured in `anti-reversal-experiment.md`.

---

## 8. Solar cross-add to the first batch

### 8.1 solar trid — VERIFIED 5/5

Recomputed all five cases; every stated figure appears in the file and matches:

| Case | ΣLE | ΣCD | Δ | 10% threshold | excess cure | zero-tol cure |
|---|---|---|---|---|---|---|
| 1 | 1570.00 | 1625.00 | +55.00 | 157.00 | 0.00 | 0.00 |
| 2 | 1800.00 | 1855.00 | +55.00 | 180.00 | 0.00 | 0.00 |
| 3 | 2000.00 | 2175.00 | +175.00 | 200.00 | **0.00** | 0.00 |
| 4 | 2450.00 | 2850.00 | +400.00 | 245.00 | **155.00** | 0.00 |
| 5 | 900.00 | 900.00 | 0.00 | 90.00 | 0.00 | **100.00** |

**Case 3 is the discriminator.** Sum-of-increases is 300.00 against a 200.00 threshold — the defect
method would report a violation — while the aggregate delta is 175.00 and there is none. solar labels
the case *"illustrates the defect this suite catches"* and computes it the right way. Case 4 pairs
with it: sum-of-increases 460.00, aggregate 400.00, correct cure 155.00 (400 − 245), which solar
states exactly.

This makes **14 of 14 delivered TRID files** avoiding the sum-of-increases trap across the two
batches.

### 8.2 solar ofac — VERIFIED 2/5, WRONG-RULE 3/5 — and it is a *third* interpretation

Batch 1 adjudicated the rule as a **full-attribution fixpoint**: a blocked owner's ≥50% holding blocks
the intermediary, the intermediary's own holdings then count in full, and a **sub-50% intermediary
transmits nothing** (glm 5.3 flash's gate case; mimo was marked contradictory for the opposite move).

solar applies full attribution through blocked intermediaries **and then adds a multiplicative
contribution through non-blocked ones**, declaring it: *"(Multiplicative treatment applies through
non-blocked intermediaries.)"*

| Case | fixpoint aggregate | solar | solar's extra term | verdict changes? |
|---|---|---|---|---|
| 1 | 55% → blocked | 55% | — | **VERIFIED** |
| 2 | 10 + 30 = **40% → NOT blocked** | **50% → blocked** | +10% via B2 (40%×25%) | **YES** |
| 3 | 20 + 35 = 55% → blocked | 62% | +7% via G (35%×20%) | no |
| 4 | 10 + 45 = 55% → blocked | 55% | — | **VERIFIED** |
| 5 | 10+10+20+15 = 55% → blocked | 60.6% | +3.6% via B3, +2% via B4 | no |

**Case 2 is the whole finding.** Under the adjudicated rule the target sits at 40% and is not blocked.
solar's hybrid lands it on **exactly 50.0%** and blocks it. One case, one rule choice, opposite legal
outcome, at the threshold.

**Verdict: WRONG-RULE under the batch-1 standard**, applied consistently and arithmetically exactly
under its own declared variant (10+30+10 = 50 ✓; 20+35+7 = 62 ✓). It is *not* self-inconsistent: the
computation section declares the hybrid. Its verdict lines are looser — they attribute the number to
"the full-attribution-through-blocked-intermediaries approach" without naming the multiplicative
tail-add — so a reader taking only the verdict field would be misled about which rule produced 50%.

**Two things are owed here.** First, solar's `weakest_point` names the exact fault line before being
asked: *"whether the intermediary's full downstream ownership is attributed … or only the
multiplicative share … I am not certain which OFAC has officially prescribed, and this is the key
interpretive risk."* That is the best available honesty posture on a contested rule. Second, this
axis is already flagged NEEDS-RETRIEVAL in `day2-c1-adjudication.md`, and solar's hybrid is now the
**third** distinct reading in the corpus (pure full-attribution; pure multiplicative — gemini,
minimax m3; hybrid — solar). **The retrieval is no longer optional**: three readings, and one
threshold case where they disagree, is a specification gap rather than a model failure.

---

## 9. Harvest — candidate fixture material

Nominated on cleanliness of the *step sequence*, not on topic. No content copied.

| File · prompt | Why |
|---|---|
| `chatgpt irb.json` / `grok irb.json` / `meta irb.json` | Three independent files agreeing to 15 significant figures on the CRE31 closed form. A golden-vector triple where any implementation bug shows immediately |
| `kimi irb.json` | The only file that *derives* its benchmark — CRE99.2 at LGD 40% scaled to 45% — instead of asserting one. The scaling step is itself the fixture |
| `chatgpt ccd2.json` | Four Directive-form APRC solves, all closing under independent bisection, including a 20.0000% exact case |
| `solar trid.json` cases 3+4 | Matched pair on the same bucket structure: sum-of-increases 300 vs threshold 200 with **no** violation, then 460 vs 245 with a 155.00 cure. Discriminates the aggregate test from the defect method and pins the cure arithmetic in one pair |
| `solar ofac.json` case 2 | The corpus's sharpest rule discriminator: 40% (fixpoint, not blocked) vs 50.0% (hybrid, blocked) on one graph. **Park until the OFAC retrieval lands** — it is a fixture for whichever rule turns out to be right, and a negative control for the other |
| `kimi jcs.json` / `sonnet jcs.json` | 12/12 each against a reference canonicalizer, no escaping-form defects. Directly usable as RFC 8785 conformance vectors |
| `chatgpt jcs.json` (post-salvage) | Covers `-0`, 2⁵³+1 rounding, both sides of the 1e21 exponent boundary, and the duplicate-key rejection. The most complete number-serialization set in the slice, once the quoting is repaired |
| `solar ccd2.json` | The only zero-rate APRC vector: `Σ 83.3333/(1+X)^(k/12) = 1000` at X = 0. Every solver needs one |
| `meta receipt.json` | **Retrieval target, not a fixture.** The only file with domain-separator tags, the 4-byte selector, the 128-bit claim-digest split, and imageId identified as the pre-state digest. Verify against risc0 source, then promote or discard |
| `minimax 2.7 irb.json` | **Negative control.** Four independent rule defects — grouping, a negative `b`, an invented `(1/M)^{1/6}`, and Φ⁻¹(0.01) used for PD 0.005 — with a correct self-flag. A regression fixture for "does the checker catch a model that already knows it is wrong" |

**Not harvested:** every MiCA own-funds case (§3.1), every single-source receipt field (§6.3), and
every OFAC case whose verdict turns on the attribution question — all pending retrieval.

---

## 10. Summary

| Prompt | Files | Clean | SELF-INCONSISTENT | WRONG-RULE | WRONG-INPUT | Not adjudicable |
|---|---|---|---|---|---|---|
| **IRB** | 13 | **7 models 4/4** | gemini (1), minimax m3 | mistral, solar, yuanbao, minimax 2.7 | minimax 2.7 (1) | — |
| **FRTB** | 14 | **14 of 14** | — | — | — | — |
| **MICA** | 13 | **13 of 13** (stress arithmetic) | — | — | — | own-funds figure (all) |
| **CCD2** | 13 | **8 models** | deepseek (3), gemini (3), minimax m3 (3) | minimax 2.7 (2), mistral (3) | — | — |
| **JCS** | 15 | **131/171 exact**, +13 form-only | — | deepseek (order), glm flash (normalization) | — | duplicate-key vectors |
| **RECEIPT** | 15 | 15/15 complete | — | — | — | **all — no ground truth** |
| **solar TRID** | 1 | **5/5** | — | — | — | — |
| **solar OFAC** | 1 | 2/5 | — | 3/5 (declared hybrid) | — | — |

**Four things this batch establishes.**

1. **Purpose-built confusions mostly do not fire.** FRTB's ES-vs-VaR conflation: zero instances.
   MiCA's wrong-tail trap: zero. TRID's sum-of-increases defect: zero across 14 files and two batches.
   JCS's UTF-16 ordering trap: 7 of 8 models that built it stepped around it. **The named defect is
   found in the models that were not asked about it** — mistral's simple-interest APRC, minimax 2.7's
   nominal-monthly discounting, solar's OFAC hybrid.

2. **Honesty fields reached 100% adoption and remain independent of correctness.** gemini fabricated
   a benchmark to confirm an error; minimax 2.7 correctly flagged four of its own errors; minimax m3
   cited a specific table and paragraph to explain away arithmetic that was simply wrong. The only
   signal in the whole audit is *absence* of a label — mistral, at 4–45 characters, is the batch's
   weakest model. **A short label predicts a weak answer; a long one predicts nothing.**

3. **Salvage is not a formality — it decides scores.** Three techniques new to this pass recovered
   `chatgpt jcs` (a bottom-of-table 0/33 became a 10/11), `sonnet receipt` and `yuanbao receipt`
   (both zero sections became 7/7). Emission bugs are not quality signals and must not be scored as
   content. The ladder is now eight techniques deep.

4. **One specification gap is now blocking.** Three distinct OFAC attribution rules are live in the
   corpus, and case 2 of `solar ofac.json` flips at exactly the 50% threshold between two of them.
   Together with the MiCA own-funds figure and the risc0 receipt layout, that is **three retrievals**
   — and they gate the harvest, not the grading.

`TODO(alice): §6 is coverage-and-convergence only. No risc0 source or real receipt was consulted;
the two strongest files (meta, grok) are nominated for verification, not accepted. Do not treat any
receipt field-role claim in this document as adjudicated.`
