# Hardware-Assurance Calculation Formulas — merged from Prompt S

**Status: DRAFT SCAFFOLDING, NOT VERIFIED MATH.** Merged model output, 2026-08-31, run marker
`free-model-harvest/S/2026-08-31`. Every worked example below was **recomputed step by step**; every
threshold value is marked **NEEDS-RETRIEVAL** unless `../HW-ASSURANCE-SCOPING-2026-08-31.md` quotes
primary text for it. Nothing here is usable until the clause locators are checked against the
authoritative documents.

**Corpus:** 13 `* s.json` files. **10 models produced the demanded 4-family shape** (chatgpt,
deepseek, gemini, grok, kimi, meta, minimax 2.7, sonnet, yuanbao — plus minimax m3 and mistral in a
flattened shape that was recovered). One prose refusal (mimo). **87 formula objects, ~40 carrying
worked examples.**

⚠ **`glm 5.3 flash s.json` contains the Alpha 21264 paper recall** — the same five entries it has now
submitted for seven different prompts. Not gradable as formulas; excluded. See
`anti-reversal-experiment.md` §3.

**Arithmetic is the judge.** ✅ = recomputes exactly. ⚠ = closes but a convention or classification
rule is wrong. ❌ = does not close; **per the prompt's own rule, that discredits the entry.**

---

## Family 1 — ISO 26262-5 hardware architectural metrics

### SPFM — strong consensus, one structural dissent

**Consensus expression (9 of 11 models, symbolically identical):**

```
SPFM = 1 − ( Σλ_SPF + Σλ_RF ) / Σλ
   where Σλ = Σ(λ_SPF + λ_RF + λ_MPF + λ_S)
```

Equivalently `SPFM = Σ(λ_MPF + λ_S) / Σλ`, which three models state as a cross-check on the first —
a useful property for a calculator to assert internally.

`disputed:` **mistral states it inverted.** `SPFM = λ_SP / (λ_SP + λ_MP + λ_SF)` — a bare ratio, not
its complement, and with the numerator being the *single-point* rate rather than the covered
remainder. On its own worked numbers this returns **95% where the consensus formula returns 3%**. The
same structural error propagates into all three of its T-slice vectors (`hw-calc-vectors.md` §2), so
it is a stable model-level defect rather than a typo. **Do not merge mistral's ISO family.**

`disputed:` **the denominator convention — three variants in play, and this is a real finding.**
1. *All components*, Σλ = SPF + RF + MPF(detected) + MPF(latent) + safe — chatgpt, gemini, kimi, meta,
   sonnet, grok.
2. *Safety-related excluding safe faults* — yuanbao's T-slice vectors compute against
   `λ_SPF + λ_RF + λ_MPF,latent + λ_MPF,detected`, explicitly excluding λ_safe.
3. *Excluding detected multiple-point faults* — minimax m3 uses `SPF + RF + safe + MPF_latent`.

All three close arithmetically on their own inputs, and they give **materially different SPFM for the
same fault distribution**. ISO's definition is variant 1. **A calculator must pin the convention
explicitly, and any fixture suite must state which one it assumes** — this is the single most likely
source of a "correct-looking but wrong" calculator in this family.

**Worked examples recomputed:**

| Model | Example | Verdict |
|---|---|---|
| chatgpt | Σλ=100, SPF=2, RF=1 → 1 − 3/100 = 0.97 | ✅ |
| gemini | Σλ=1000, SPF=5, RF=15 → 1 − 20/1000 = 0.98 | ✅ |
| deepseek | λ=1000, SPF=50, RF=30 → 1 − 80/1000 = 0.92 | ✅ |
| minimax 2.7 | Σλ_safety=1000, SPF=40, RF=30 → 1 − 70/1000 = 0.93 | ✅ |
| sonnet | Σλ=20, Σ(SPF+RF)=0.2 → 1 − 0.01 = 0.99 | ✅ |
| **yuanbao** | two elements summed: numerator 7+4=11; denominator 7+4+15+3+121=150; 1 − 11/150 = 0.926667 | ✅ **the only multi-element example in the slice** — and the only one that exercises the Σ-over-elements semantics the standard actually requires |

### LFM — strong consensus

```
LFM = 1 − Σλ_MPF,latent / ( Σλ − Σλ_SPF − Σλ_RF )
```

Eight models symbolically identical. Two state the equivalent
`LFM = 1 − Σλ_MPF,L / (Σλ_MPF,L + Σλ_MPF,D + Σλ_S)`, which is the same quantity when variant-1
denominators are used — worth keeping as an internal cross-check.

| Model | Example | Verdict |
|---|---|---|
| chatgpt | denom 100−2−1=97; 1 − 3/97 = 0.969072 | ✅ |
| gemini | denom 1000−5−15=980; 1 − 80/980 = 0.918367 | ✅ |
| deepseek | denom 920; 1 − 100/920 = 0.891304 | ✅ |
| yuanbao | denom 3+15+121=139; 1 − 3/139 = 0.978417 | ✅ |
| minimax 2.7 | denom 930; 93/930=0.1 → 0.90 | ✅ |
| sonnet | denom 19.8; 1 − 1.98/19.8 = 0.90 | ✅ |

### PMHF — **no consensus, and the arithmetic is worst here**

Six structurally different expressions were offered. This is the family's weak point and it should be
treated as unresolved:

| Form | Models |
|---|---|
| `PMHF ≈ λ_SPF + λ_RF + (λ_DPF,det × λ_DPF,latent × T_lifetime)` — the Annex-F-style approximation | chatgpt, gemini, meta, yuanbao |
| `PMHF = λ_SPF + λ_RF + λ_MPF,L` (no lifetime term) | minimax 2.7, one other |
| `PMHF = Σ λ_i × (1 − DC_i) × t_lifetime` | deepseek |
| `PMHF = (λ_SPF + λ_RF) + (λ_MP × DC)/(2 × T_mission)` | one model |
| "requires fault-tree or Markov analysis; no single closed form" | grok, sonnet — **the most honest answers in the family** |

`disputed:` **the dual-point term's dimensions.** The λ×λ×T form is dimensionally coherent
(h⁻¹·h⁻¹·h = h⁻¹) and matches the scoping doc's quoted Infineon rendering of Annex F.2. deepseek's
`λ × (1−DC) × t` is **not** a rate — it yields a dimensionless expected-failure count — and its own
worked example visibly breaks down mid-calculation, containing the literal strings *"Wait:"* and
*"Actually"* before arriving at 10 FIT by an unexplained route. ❌ **Does not close; discredits
deepseek's PMHF entry.**

| Model | PMHF example | Verdict |
|---|---|---|
| chatgpt | (2e-9)(4e-9)(1e4) = 8e-14; + 3e-9 = 3.00008e-9 /h | ✅ |
| gemini | (80e-9)(700e-9)(15000) = 8.4e-10; + 2.0e-8 | ✅ |
| yuanbao | (3×15×100000)/1e9 = 0.0045 FIT; 11 + 0.0045 = 11.0045 FIT | ✅ |
| minimax 2.7 | 2+3+4 = 9 FIT < 10 FIT → ASIL D pass | ✅ (trivial but closes) |
| **deepseek** | self-contradicting mid-example | ❌ |

### ASIL target values — NEEDS-RETRIEVAL, and the scoping doc says why

Model consensus (10 of 11 agree exactly):

| | ASIL B | ASIL C | ASIL D |
|---|---|---|---|
| SPFM | ≥ 90% | ≥ 97% | ≥ 99% |
| LFM | ≥ 60% | ≥ 80% | ≥ 90% |
| PMHF | < 100 FIT (10⁻⁷/h) | < 100 FIT | < 10 FIT (10⁻⁸/h) |

**Cross-check against `../HW-ASSURANCE-SCOPING-2026-08-31.md` §1:** the scoping doc reaches the same
numbers from named secondary sources **and records that two public sources disagree on the ASIL B
SPFM target — 90% versus 97%** — with the normative value paywalled in ISO 26262-5 Table 5. Ten
models agreeing on 90% is *not* evidence: it is ten draws from the same secondary literature, and the
corpus has already demonstrated (twice, on POWER4 coherence) that multi-model agreement tracks a
shared prior rather than truth.

**Status: NEEDS-RETRIEVAL. The open `TODO(alice)` in the scoping doc stands unchanged.** Every other
number in the table inherits the same status; none was independently verifiable here.

**Clause locators:** most models returned `null` as instructed. Those that guessed offered
"Table 4/Table 5" or "Clause 8/Clause 9" — the scoping doc's quoted ISO preview confirms Clause 8
covers the architectural metrics and Clause 9 the PMHF/EEC methods, so the *clause* attribution is
sound while the *table* number is not verifiable.

---

## Family 2 — JEDEC FIT-rate math

### Chi-square point and confidence-bound estimate — clean consensus

```
λ_CL  =  χ²(2r+2, CL) × 10⁹ / ( 2 × ss × t × AF )      [FIT, upper bound at confidence CL]
λ_point =  r × 10⁹ / ( ss × t × AF )                    [FIT, point estimate]
```

with `r` = failures, `ss` = sample size, `t` = test hours, `AF` = acceleration factor. Nine models
agree, including the factor of 2 in the denominator and the `2r+2` degrees of freedom.

**Best single contribution — gemini states the χ² identity for the zero-failure case:**
`χ²(2, CL) = −2·ln(1 − CL)`, giving 1.832581 at 60%. **Recomputed: −2·ln(0.40) = 1.8325815 ✅.** This
matters because it removes the need for a lookup table in the degenerate case a qualification report
most often reports.

| Model | Example | Verdict |
|---|---|---|
| chatgpt | r=15, t=2000, ss=500, AF=78.6 → point 15e9/7.86e7 = 190.84 FIT | ✅ |
| chatgpt | 60% CL: χ²=33.4 → 33.4e9/1.572e8 = 212.47 FIT; 90%: 42.6 → 270.99 FIT | ✅ |
| gemini | r=0, CL=0.60, N=100, t=1000, AF=77.645 → 1.832581e9 / 1.5529e7 | ✅ |
| yuanbao | ss=231, t=1000, r=0, AF=77.6 → denom 3.58512e7; 1.8326e9/3.58512e7 = 51.1 FIT | ✅ |
| deepseek | N=77, H=1000, r=0, AF=100 → 1.832e9/1.54e7 = 118.96 FIT | ✅ |
| **grok** | ss=231, t=1000, r=0, AF=27.5 → states λ = 1.442e-10, "FIT ≈ 0.144" | ❌ **off by 10³** — 1.8326/(2×231×1000×27.5) = 1.4424e-7 /h = **144 FIT**, not 0.144. The entry then trails into a self-correcting parenthetical without fixing the number. Discredits grok's FIT entry. |

### Arrhenius acceleration factor — clean consensus

```
AF = exp[ (E_a / k) × ( 1/T_use − 1/T_stress ) ]     T in kelvin, k = 8.617×10⁻⁵ eV/K
```

Unanimous. The canonical 55 °C / 125 °C, E_a = 0.7 eV case recomputes consistently across five models
at **AF ≈ 77–78.6**, the spread being entirely due to whether 273 or 273.15 is used for the kelvin
conversion and whether k is 8.6e-5 or 8.617333262e-5:

| Model | Constants | AF | Verdict |
|---|---|---|---|
| chatgpt | k=8.6e-5, T=328/398 | 78.6 | ✅ (exponent 4.3645) |
| gemini | k=8.617333262e-5, T=328.15/398.15 | 77.6 | ✅ (exponent 4.3524) |
| deepseek | k=8.617e-5 | 77.1 | ✅ |
| yuanbao | k=8.617e-5 | 77.6 | ✅ |

**This spread is itself a finding for a calculator spec:** the same physical case yields 77.0–78.6
depending on constant choices, ~2%. A deterministic calculator must pin k and the kelvin offset, and
a fixture suite must state them.

**E_a values.** Consensus default 0.7 eV for an unknown mechanism; several models add 1.0 eV for the
no-failure case, matching the scoping doc's JEP122 note. Every model that offered a value attached an
applicability caveat, which the prompt asked for and which they delivered.

---

## Family 3 — EAR ECCN 3A090

### TPP — unanimous, and it matches the regulation

```
TPP = 2 × MacTOPS × bit_length          summed over all processing units on the IC
```

All 10 models. The scoping doc quotes the regulation's Technical Note 2 verbatim in the same form,
including the rationale for the factor of 2 (*"one multiply-accumulate computation … as 2
operations"*). **This is the single best-attested formula in the S slice.**

```
Performance density = TPP / applicable die area (mm²)
```

Also unanimous.

| Model | Example | Verdict |
|---|---|---|
| chatgpt | 300 MacTOPS @16-bit → 2×300×16 = 9600; aggregate 9600+2400 = 12,000 | ✅ |
| gemini | 250 MacTOPS @8-bit → 2×250×8 = 4000 | ✅ |
| yuanbao | 50@16 → 1600; 25@8 → 400; total 2000; PD = 2000/400 = 5.0 | ✅ |
| deepseek | 100 units × (2×5×8) = 8000; PD = 8000/800 = 10.0 | ✅ |

### Threshold values and the classification rule — NEEDS-RETRIEVAL, and two models get the rule wrong

Scoping doc, quoting 90 FR 5298 / the 2025-02-14 correction:

- **3A090.a** — TPP ≥ 4800 **and** performance density ≥ 5.92
- **3A090.b.1** — TPP 2400–4800 **and** PD 1.6–5.92
- **3A090.b.2** — TPP ≥ 1600 **and** PD 3.2–5.92
- **3A090.c** — HBM memory-bandwidth density > 2 GB/s/mm²

| Model | Classification logic | Verdict |
|---|---|---|
| **yuanbao** | evaluates .a, then .b first branch, then `TPP≥1600 AND PD≥3.2 AND PD<5.92 → 3A090.b` | ⚠→✅ **matches the regulation as the scoping doc quotes it** — the only model to get the banded structure right |
| **gemini** | states 3A090.a as `(TPP≥4800) OR (TPP≥1600 AND PD≥5.92)` | ⚠ **arithmetic closes, rule is wrong** — .a requires TPP ≥ 4800 **and** PD ≥ 5.92; the OR-branch conflates .a with .b |
| **grok** | *"TPP = 1600 and performance density = 5.92 meets the a.2 threshold exactly"* | ⚠ **wrong on both counts** — there is no "a.2"; at PD exactly 5.92 the b.2 band (PD < 5.92) does not apply, and TPP 1600 is far below .a |

**This is the most important lesson in the S slice: arithmetic closing does not mean the entry is
usable.** gemini and grok compute TPP flawlessly and then classify against a rule they have
misremembered. A calculator built from their entries would return the right number and the wrong
answer.

**Volatility flag inherited from the scoping doc:** these parameters changed four times in three years
(Oct 2022, Oct 2023, Dec 2024, Jan 2025). Any calculator must pin a rule date. **Status:
NEEDS-RETRIEVAL against the current eCFR text regardless of model agreement.**

---

## Family 4 — CHIPS Act §48D

### The calculation is trivial; the rate is the whole question

```
Credit = rate × qualified investment basis
Primary-purpose test: semiconductor-related output share > 50%
```

| Model | Rate used | Verdict |
|---|---|---|
| chatgpt, grok, yuanbao, sonnet, kimi | **35%** | ✅ arithmetic; matches scoping doc's current-law reading |
| gemini | 25% for property placed in service 2024, 35% for 2027 | ✅ **and the most careful answer** — it treats the rate as time-dependent rather than fixed |
| minimax 2.7 | flat **25%** on a $500 M basis → $125 M | ⚠ arithmetic closes; **rate is stale** |

Recomputations: 0.35 × $100 M = $35 M ✅; 0.35 × $1 B = $350 M ✅; 0.25 × $500 M = $125 M ✅
(arithmetically).

**Cross-check against the scoping doc §3:** 26 U.S.C. §48D(a) currently reads **35 percent**;
the original CHIPS Act of 2022 set **25 percent**, and **Pub. L. 119-21 substituted 35 for 25 in
2025**. So both rates are real, and the correct answer depends on an as-of date — exactly as
gemini/meta modelled it and as the scoping doc's volatility flag warns.

**Primary-purpose threshold.** Models offering a number said **>50%**, matching the scoping doc's
quotation of T.D. 10009 (*"more than 50% of the facility's potential output"*). One model's worked
example — 80% of revenue → qualifies — recomputes ✅ and cites `Treas. Reg. § 1.48D-2`, a locator the
scoping doc does not quote. **NEEDS-RETRIEVAL on the locator; the threshold itself is corroborated.**

**Other statutory thresholds** the models raised and the scoping doc confirms: construction must begin
on or before **2026-12-31**; property placed in service after **2022-12-31**; §50(a)(3)(A) **100%
recapture** on an applicable transaction within 10 years. None was independently verified here.

---

## Cross-family summary

| Family | Formula consensus | Worked-example arithmetic | Threshold status |
|---|---|---|---|
| ISO SPFM | strong (1 structural dissent) | ✅ 6/6 recompute | **NEEDS-RETRIEVAL** (ASIL B SPFM disputed 90 vs 97 in the public literature) |
| ISO LFM | strong | ✅ 6/6 | NEEDS-RETRIEVAL |
| ISO PMHF | **none — 6 forms** | ❌ 1 of 5 fails | NEEDS-RETRIEVAL |
| JEDEC FIT | strong | ❌ 1 of 6 fails (grok, 10³) | n/a — formula-only |
| Arrhenius | unanimous | ✅ 4/4, with a 2% constant-choice spread | n/a |
| EAR TPP | unanimous | ✅ 4/4 | **NEEDS-RETRIEVAL**; 2 of 3 classification rules wrong |
| CHIPS §48D | trivial | ✅ 3/3 | rate is date-dependent; both 25% and 35% are real |

**Three observations that matter more than the merge itself:**

1. **Consensus on a formula is worth something; consensus on a threshold is worth nothing.** Ten
   models agree the ASIL B SPFM target is 90%. The scoping doc shows the public sources disagree and
   the normative value is paywalled. Same pattern as POWER4 coherence, third occurrence.
2. **Arithmetic correctness and rule correctness are independent failure modes.** gemini and grok both
   compute TPP perfectly and then classify against a misremembered regulation. A recomputation gate
   catches ❌ but never catches ⚠.
3. **Two models carry stable structural defects** — mistral's inverted SPFM, reproduced identically in
   its T vectors, and deepseek's dimensionally-wrong PMHF that visibly collapses mid-example. Both are
   model-level, not incidental, and both are screenable.

`TODO(alice): every NEEDS-RETRIEVAL above, and the PMHF form, need the primary text. The ASIL B SPFM
question (90% vs 97%) is unchanged from the scoping doc and is still the highest-value single
retrieval in this space.`
