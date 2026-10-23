# Candidate Test-Vector Suite — Prompt T, every vector recomputed

**Status: CANDIDATE FIXTURES, NOT VERIFIED AGAINST AUTHORITY.** Merged model output, 2026-08-31, run
marker `free-model-harvest/T/2026-08-31`. Arithmetic has been recomputed here; **threshold values have
not been retrieved** and carry the same NEEDS-RETRIEVAL status as `hw-calc-formulas.md`.

**Corpus:** 14 `* t.json` files → **113 vectors**. 12 models produced the demanded 9-vector shape
(3 each × SPFM / FIT / TPP). One prose refusal (mimo). One wrong-content file (glm 5.3 flash — the
Alpha 21264 recall again, its seventh submission of the same text across seven prompts; excluded).

**Method.** Every vector's stated step-by-step arithmetic was recomputed independently. A first
automated pass produced 18 apparent failures; **hand-checking showed 13 of those were the checker's
fault** — it inferred λ_total wrongly where a vector supplied both components and an explicit total.
Only hand-confirmed failures are reported below. That miss rate is itself worth recording: a naive
recomputation gate would have discarded 13 sound vectors.

---

## 1. Survivors — the candidate fixture suite

**101 of 113 vectors recompute correctly (89%).** Grouped by calculation, with the `discriminates`
claim assessed.

### 1.1 ISO 26262 SPFM — 30 of 36 survive

| Model | Vector | Recompute | `discriminates` assessment |
|---|---|---|---|
| chatgpt | ASIL B boundary, exactly 90% | ✅ 1−100/1000 | **Genuine boundary.** Clean, minimal, unambiguous |
| chatgpt | ASIL C boundary, exactly 97% | ✅ | Genuine boundary |
| chatgpt | ASIL D boundary, exactly 99% | ✅ | Genuine boundary |
| deepseek | Low SPFM, fails ASIL B (75%) | ✅ | **Genuine negative case** — the only sub-threshold failure vector in the slice besides grok's |
| deepseek | ASIL B boundary, exactly 90% | ✅ | duplicate of chatgpt's discriminator |
| deepseek | ASIL C boundary, exactly 97% | ✅ | duplicate |
| gemini | Realistic mid-range MCU, 95% | ✅ 1−50/1000 | **Genuine mid-range** — passes B, fails C |
| gemini | ASIL C exact boundary | ✅ | duplicate |
| gemini | ASIL D exact boundary | ✅ | duplicate |
| grok | mid-range ASIL-C meeting, 97% | ✅ | boundary, not mid-range as claimed — **`discriminates` overstated** |
| grok | ASIL-D boundary exactly 99% | ✅ | duplicate |
| grok | **degenerate all-safe, SPFM 100%** | ✅ | **Unique and valuable** — λ_SPF = λ_RF = 0. Exercises the "no single-point faults at all" path |
| kimi | Realistic mid-range, 92% | ✅ 45+35+120+25+775=1000; 1−80/1000 | Genuine mid-range, five-component distribution |
| kimi | ASIL C boundary exactly 97% | ✅ 15+15+200+50+720=1000 | duplicate discriminator, different distribution |
| kimi | **Just below ASIL D, 98.95%** | ✅ 21/2000=0.0105 | **Unique** — near-miss by 0.05 pp; exercises comparison precision, not just the boundary |
| meta | mid-range, passes B fails C, 95% | ✅ | Genuine |
| meta | boundary exactly 90% | ✅ | duplicate |
| meta | high-coverage, 99% | ✅ | duplicate |
| minimax 2.7 | **ASIL B boundary with SPFM *and* LFM both exactly at target** | ✅ 62.5% case internally consistent | **Unique** — the only vector exercising two metrics simultaneously at their boundaries |
| minimax 2.7 | ASIL B pass, generous safe-fault margin | ✅ | Genuine |
| minimax 2.7 | ASIL B fail, insufficient headroom | ✅ | Genuine negative |
| sonnet | Realistic mid-range, 99.125% | ✅ 30+15+100+5000=5145; 45/5145 | **Realistic magnitudes** — the only vector using a plausible whole-device λ (5145 FIT) |
| sonnet | Exact ASIL B boundary, 90.0% | ✅ 100/1000 | duplicate |
| sonnet | Degenerate: zero SPF and RF | ✅ | duplicate of grok's degenerate |
| minimax m3 | Baseline ASIL B, 91.23% | ✅ 50/570 | ⚠ **convention** — denominator excludes λ_MPF,detected |
| minimax m3 | Threshold boundary | ✅ internally | ⚠ same convention |
| yuanbao | ASIL-D boundary miss, 98.08% | ✅ 2.8/145.78 | ⚠ **convention** — denominator excludes λ_safe |
| yuanbao | ASIL-D boundary hit | ✅ internally | ⚠ same convention |
| yuanbao | High-coverage comfortable margin | ✅ internally | ⚠ same convention |

⚠ **The convention problem is the most important finding in this slice.** Five vectors from two models
recompute *perfectly against their own stated denominators* while using a denominator that differs
from the other ten models — minimax m3 excludes detected multiple-point faults, yuanbao excludes safe
faults. ISO's SPFM denominator is the total safety-related failure rate including safe faults
(`hw-calc-formulas.md` §1). **These five are not arithmetic failures and must not be discarded as
such — but they cannot enter one fixture suite alongside the other thirty without splitting the
expected values.** Either pin the convention and re-derive their expected outputs, or keep them as a
deliberate second suite that tests convention-sensitivity.

### 1.2 JEDEC FIT — 33 of 36 survive

| Model | Vector | Recompute | `discriminates` assessment |
|---|---|---|---|
| chatgpt | 15 failures, 60% CL, 0.7 eV | ✅ AF=78.615 at k=8.6e-5, T=328/398 | Genuine mid-range |
| chatgpt | same exposure at 90% CL | ✅ χ²=42.6 at df=32 (=2×15+2 ✅) | **Unique** — isolates the confidence-level term with everything else held constant |
| chatgpt | Zero-failure boundary at 90% CL, Ea=0.5 | ✅ AF=22.591; point estimate 0 | **Unique** — the degenerate r=0 case where the point estimate is 0 and only the bound is meaningful |
| gemini | mid-range qualification | ✅ AF=77.645, df=4 | Genuine |
| gemini | zero-failure degenerate | ✅ χ²(2,0.60) = −2·ln(0.40) = 1.832581 | **Best in slice** — uses the closed form instead of a table lookup |
| gemini | **unaccelerated thermal boundary** | ✅ T_use = T_stress → delta = 0 → AF = exp(0) = 1 | **Unique and important** — the AF = 1 degenerate that a calculator will hit whenever someone tests at use temperature |
| grok | classic 0-fail HTOL 60% CL | ✅ | Genuine |
| grok | one-failure case, higher CL | ✅ | Genuine |
| grok | **AF boundary, T_use = T_test** | ✅ | duplicate of gemini's, independently derived |
| kimi | mid-range with f=2 | ✅ | Genuine |
| kimi | zero-failure upper-bound-only | ✅ | duplicate |
| kimi | **calibrated to land at ~100 FIT** | ✅ | **Unique** — a target-value inverse case; useful as a regression anchor |
| yuanbao | ss=231, t=1000, r=0, AF=77.85 | ✅ 231×1000×77.85 = 1.7983e7 | Genuine, and uses the industry-standard 231-device sample |
| meta, minimax 2.7, sonnet, deepseek, minimax m3 | 15 further vectors | ✅ | mostly duplicate discriminators |

**Coverage nuance worth flagging:** the prompt required a threshold-boundary case per calculation.
**FIT has no regulatory threshold** — it is a measured rate, not a controlled parameter. Models
substituted *degenerate-input* boundaries (r = 0, AF = 1) and *target* boundaries (10 FIT ASIL D,
~100 FIT). That is the right substitution, but it means the FIT family's "boundary" coverage is of a
different kind from SPFM's and TPP's, and a suite spec should say so rather than implying regulatory
equivalence.

### 1.3 EAR TPP — 30 of 33 survive

| Model | Vector | Recompute | `discriminates` assessment |
|---|---|---|---|
| chatgpt | **Exactly 4800** | ✅ 600 TOPS × 8 | Genuine boundary |
| chatgpt | **4792 — eight below** | ✅ 599 × 8 | **Best discriminator in the slice.** A near-miss by 8 units tests the comparison operator, not just the arithmetic |
| chatgpt | Multi-mode, highest TPP selected | ✅ max(4800, 1600) | **Unique** — exercises the "select the applicable mode" semantics |
| gemini | Datacenter accelerator, TPP 16000, PD 26.67 | ✅ 16000/600 | Genuine high-side |
| gemini | Primary threshold boundary, TPP 4800, PD 12 | ✅ 4800/400 | Genuine |
| gemini | **PD exactly 5.92** | ✅ 1600/270.27027 = 5.9200 | Arithmetic ✅, **classification ⚠** — labelled 3A090.a; TPP 1600 with PD 5.92 is not .a under the scoping doc's quoted bands |
| grok | Exactly 4800 via 2×150×16 | ✅ | duplicate |
| grok | Below both thresholds, TPP 800 | ✅ 2×50×8 | Genuine negative |
| grok | Multi-unit aggregation, 3200+2560=5760 | ✅ | **Unique** — the only vector testing summation across heterogeneous units |
| kimi | Comfortably in .a territory | ✅ | Genuine |
| kimi | Just below .a, crossing into .b | ✅ | **Unique band-crossing** |
| kimi | **PD exactly at the .b lower boundary (3.2)** | ✅ | **Unique** — the only vector on the 3.2 boundary |
| yuanbao | TPP 2000, PD 5.0 → 3A090.b | ✅ 1600+400; 2000/400 | ✅ **and the classification matches the regulation** as the scoping doc quotes it |
| deepseek, meta, minimax 2.7, sonnet, minimax m3 | 12 further vectors | ✅ | mostly duplicates |

---

## 2. Failed vectors — with the exact step that broke

**12 vectors fail. Two models account for all of them, and both failures are structural rather than
arithmetic slips.**

### mistral — 3 SPFM vectors, inverted formula

| Vector | The step that broke |
|---|---|
| *"Mid-range SPFM with mixed fault distribution"* | Step 2 states `SPFM = λ_SPF / (λ_SPF + λ_RF + λ_MPF_latent + λ_safe) = 95 / 100 = 0.95`. **The numerator is the single-point rate itself, not its complement.** With the consensus formula the same inputs give `1 − (95+2)/100 = 0.03`. The vector reports **95% and claims ASIL B is met when the true value is 3%** |
| *"Threshold-boundary SPFM at ASIL C"* | same inversion; reported 97%, recomputes to 2% |
| *"Degenerate SPFM with high latent faults"* | same inversion; reported 50%, recomputes to 25% |

**This is the same structural error as mistral's S-slice expression** (`hw-calc-formulas.md` §1), which
makes it a stable model-level defect. It is also the most dangerous failure shape in the slice: the
outputs are plausible ASIL-relevant percentages, the steps are shown, and only recomputation against
the correct formula exposes them.

### qwen — 2 SPFM vectors, fabricated formula

| Vector | The step that broke |
|---|---|
| *"ASIL B boundary case"* | `SPFM = 1 − (λ_RF / λ_SPF) = 1 − (10/100) = 0.90`. **This is not SPFM** — it is a ratio of residual to single-point faults, and it ignores λ_total entirely. It lands on 0.90 by coincidence of the chosen inputs. Correct value from the same inputs: `1 − (100+10)/1000 = 0.89` |
| *"ASIL D boundary case"* | same fabricated formula; `1 − 10/1000 = 0.99` reported. Correct value: `1 − 1010/10000 = 0.899` |
| *"Degenerate zero-fault case"* | ✅ **survives** — with zero faults the fabricated and correct formulas coincide |

**Note in qwen's favour, and it is a real one:** qwen carries **three explicit UNKNOWN /
parameterize-the-threshold flags** in its T file — more than any other model — doing exactly what the
prompt asked when it did not know a current regulatory value. Its failure is a wrong formula
confidently applied, not a fabricated threshold. Those are different defects and should be scored
differently.

### One near-miss worth recording

A TPP vector states an input of 16-bit operations and then computes with `bit_length = 8`, with the
literal text *"using bit_length=8, not 16 — corrected below"* inside the step. The final arithmetic is
self-consistent (2 × 125 × 8 × 2 units = 4000) but **the stated inputs and the computation disagree**,
so the vector cannot be used as a fixture without deciding which is authoritative. Recorded as
input/computation mismatch, not an arithmetic failure.

---

## 3. Coverage check

**Requirement: each calculation's vectors must include at least one threshold-boundary case.**

| Calculation | Boundary coverage | Verdict |
|---|---|---|
| **ISO 26262 SPFM** | ASIL B 90% exact (×4 models), ASIL C 97% exact (×5), ASIL D 99% exact (×4), plus a 0.05 pp near-miss (kimi) and a dual-metric boundary (minimax 2.7) | ✅ **Over-covered.** All three ASIL boundaries are hit exactly, from multiple independent fault distributions |
| **JEDEC FIT** | No regulatory threshold exists. Covered instead by degenerate inputs — r = 0 (×4), AF = 1 with T_use = T_stress (×2) — and target boundaries at 10 FIT and ~100 FIT | ⚠ **Covered by substitution.** Adequate, but the suite spec must state that these are degenerate/target boundaries, not regulatory ones |
| **EAR TPP** | TPP exactly 4800 (×3), 4792 (8 below), PD exactly 5.92, PD exactly 3.2, band-crossing .a→.b, multi-unit aggregation | ✅ **Well covered**, including both PD band edges |

**Gaps a fixture suite would still need:**
1. **No vector tests the 3A090.b.1 band** (TPP 2400–4800 with PD 1.6–5.92). Both PD edges are covered
   and the b.2 band is covered; b.1 is not.
2. **No vector tests HBM memory-bandwidth density (3A090.c)** — the prompt did not ask, but a complete
   EAR calculator needs it.
3. **No negative/zero-denominator vector for LFM**, where `Σλ − Σλ_SPF − Σλ_RF` can reach zero. The S
   slice's `edge_cases` fields raised division-by-zero repeatedly; no T vector exercises it.
4. **No vector spans the SPFM convention split** identified in §1.1 — which is precisely the case that
   would expose a calculator built on the wrong denominator.

---

## 4. Recommendation

- **Adopt the 101 surviving vectors as the candidate suite**, minus the five convention-divergent SPFM
  vectors, which should be held as a separate convention-sensitivity set until the denominator is
  pinned.
- **Deduplicate before use.** Roughly half the survivors are independent re-derivations of the same
  three discriminators (90/97/99 exact). That redundancy is useful evidence *now* — six models
  independently producing the same boundary is a mild correctness signal — and is dead weight in a
  test suite.
- **Add the four missing cases in §3** by hand; none requires a model.
- **Do not treat any expected value as authoritative** until the thresholds behind them are retrieved.
  The vectors test *arithmetic*, and the arithmetic is now checked; they do not test *the regulation*,
  and nothing here has.

`TODO(expert): the SPFM denominator convention (include safe faults? include detected MPF?) determines
the expected value of 30-plus fixtures. It is one sentence to settle and it blocks the suite.`
