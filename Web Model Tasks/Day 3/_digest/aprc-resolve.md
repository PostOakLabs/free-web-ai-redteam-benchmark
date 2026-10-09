# Day 3 APRC re-solve (DAY3-FOLD-NORMALIZE-1, step 4)

Method: each model's own `equation` string parsed and solved numerically by
bisection on the stated present-value form `LHS = Σ cf·(1+X)^(-m/12)`.
Monthly-`i` forms (sonnet, minimax 2.7, minimax m3 case 4) are solved in
monthly space and converted by the model's OWN stated conversion
(`APRC=(1+i)^12-1` effective vs `APRC=12·i` nominal); the conversion is part
of the measurement. **Zero regulatory retrieval.** Deltas are arithmetic
measurements, not verdicts.

Parse result: **50/50 cells machine-parseable, 0 non-parseable.** Annuity
`Σ`/`sum` shorthands were expanded to explicit monthly terms; `...`
ellipses expanded over the stated range; single-period equations solved
closed-form. `mimo` case 4 was cut at the explicitly labeled `Cash-fee
alternative for comparison:` (a different scenario stated for comparison,
not the case equation). `minimax m3` contributes cases 1 and 4 only (cases
2+3 fused, see loader log).

## Re-solve table (stated vs own-equation solve, pp delta = solve − stated)

| model | c1 stated/solve/Δ | c2 stated/solve/Δ | c3 stated/solve/Δ | c4 stated/solve/Δ |
|---|---|---|---|---|
| chatgpt | 8.8 / 8.84 / +0.04 | **39.4 / 30.05 / −9.35** | 19.6 / 19.56 / −0.04 | 12.3 / 12.32 / +0.02 |
| deepseek | 8.9 / 8.84 / −0.06 | 24.4 / 24.36 / −0.04 | 19.6 / 19.56 / −0.04 | 8.0 / 8.00 / −0.00 |
| gemini | 7.7 / 8.84 / **+1.14** | **22.6 / 24.36 / +1.76** | 19.6 / 19.56 / −0.04 | 12.3 / 12.32 / +0.02 |
| glm 5.3 flash | 8.8 / 8.84 / +0.04 | 24.4 / 24.36 / −0.04 | 19.6 / 19.56 / −0.04 | 8.0 / 8.00 / −0.00 |
| grok | 8.0 / 8.84 / **+0.84** | **28.0 / 24.36 / −3.64** | **21.8 / 19.56 / −2.24** | 12.0 / 12.00 / +0.00 |
| kimi | 8.8 / 8.84 / +0.04 | 24.4 / 24.36 / −0.04 | 19.6 / 19.56 / −0.04 | 12.3 / 12.32 / +0.02 |
| mimo | 8.8 / 8.84 / +0.04 | 24.3 / 24.36 / +0.06 | 19.6 / 19.56 / −0.04 | 12.3 / 12.32 / +0.02 |
| minimax 2.7 | 6.5 / 6.52 / +0.02¹ | 32.7 / 32.71 / +0.01¹ | 18.0 / 18.00 / +0.00¹ | 7.7 / 7.72 / +0.02¹ |
| minimax m3 | 6.1 / 8.84 / **+2.74**² | ABSENT (fused) | ABSENT (fused) | 8.0 / 8.00 / −0.00 |
| mistral | 6.7 / 6.72 / +0.02³ | 24.0 / 24.02 / +0.02 | **18.0 / 0.00 / −18.00**⁴ | 8.0 / 8.00 / −0.00 |
| qwen | 8.8 / 8.84 / +0.04 | 24.4 / 24.36 / −0.04 | 19.6 / 19.56 / −0.04 | 12.3 / 12.32 / +0.02 |
| sonnet | 8.8 / 8.84 / +0.04⁵ | 24.3 / 24.24 / −0.06⁵ | 19.6 / 19.56 / −0.04⁵ | 12.3 / 12.32 / +0.02 |
| yuanbao | 8.8 / 8.84 / +0.04 | 24.0 / 24.02 / +0.02 | 19.6 / 19.56 / −0.04 | 8.0 / 8.00 / −0.00 |

¹ Solved with the model's STATED nominal conversion `APRC = 12·i_monthly`
(the equation-level difference; arithmetic itself checks out to ≤0.02pp).
² Solved from the readable `9900 = Σ 450·(1+X)^(-k/12)` form embedded in the
equation string after `equation reads:`; the string also invokes a monthly
method-A form, so the +2.74pp gap is equation-form ambiguity plus arithmetic.
³ Solved from the stated `10100 = Σ 450…` form (LHS 10100, not 9900).
⁴ The stated equation `1500 = Σ 125/(1+X)^(t/12), t=1..12` sums to the
principal and solves to **0.00%**; the stated 18.0% is unsupported by the
equation as written.
⁵ Solved in the stated monthly-`i` form with the stated effective conversion
`(1+i)^12−1` (case 2 final flow `3000·1.01³+25 = 3115.90` as stated).

Reference solves of the shared forms: 9900-vs-450×24 → **8.84%**; modal
case-2 form (3055 final) → **24.36%**; 1500-vs-137.52×12 → **19.56%**;
5000-vs-5616 → **12.32%**; 5200-vs-5616 → **8.00%**; mistral single-term
3165.90/3000 → **24.02%**.

## Digest flags: confirm / refute

- `gemini` case 2 (equation matches modal group, answer 22.6 vs 24.4):
  **CONFIRMED wrong arithmetic.** Own equation solves to 24.36 (Δ +1.76pp).
  Same defect, smaller, in gemini case 1 (7.7 vs 8.84, Δ +1.14pp).
- `grok` case 2 (28.0 on a 3055 equation): **CONFIRMED wrong arithmetic.**
  Own equation solves to 24.36 (Δ −3.64pp). grok case 1 (8.0 vs 8.84) and
  case 3 (21.8 vs 19.56, Δ −2.24pp) are further arithmetic gaps on standard
  equations.
- `chatgpt` case 2 (`3090` final term where nine models write `3055`):
  equation-level difference **CONFIRMED**, but the digest's claim that 39.4
  "follows from that term" is **REFUTED**: the 3090 equation solves to
  **30.05%** (Δ −9.35pp). Its `iterations` (e.g. `f(0.25)=81.34`) do not match
  direct evaluation of the stated equation either (true f(0.25)≈+29).
  ChatGPT case 2 carries BOTH defects: different equation AND wrong solve.

## Separation achieved (no regulation needed)

- Wrong arithmetic on shared equations: gemini (c1, c2), grok (c1, c2, c3),
  chatgpt (c2), mistral (c3).
- Equation-level differences with correct arithmetic: minimax 2.7 throughout
  (nominal `12·i` conversion, LHS 10100 in c1, annuity-1055 in c2),
  mistral c1 (LHS 10100), mistral c2 / yuanbao c2 (single-term 3165.90 form),
  sonnet c2 (monthly structure, 3115.90 final), grok c4 (`5200+400` interest
  base), camp A/B split on case 4 (all arithmetic checks out on both sides).
- No equation string in the 50 solved cells required hand-transcription into
  a preferred form; every solve above names the parsed form it used.
