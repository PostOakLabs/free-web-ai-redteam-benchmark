# BOUNDARY-GRADING-1 — Report (2026-09-04)

Commission: `BOUNDARY-GRADING-1.md`. Method: day2-c1 vocabulary
(VERIFIED / WRONG-INPUT / SELF-INCONSISTENT / WRONG-RULE / INDETERMINATE);
at-cell decisive; phrase-mismatch rule enforced; fence-strip/raw_decode/
salvage per the day2 parse note (recorded, content never repaired).

## 1. Ground-truth table (all retrieval-level, 2026-09-04, zero memory-level)

| R | Operative phrase (verified) | Inclusivity | below/at/above | Evidence |
|---|---|---|---|---|
| 1 | "more than 2 percent" §1026.32(a)(1)(iii) | strict | NO/NO/**YES** | law.cornell 1026.32 |
| 2 | "more than 36 months" (same clause) | strict | NO/NO/**YES** | same |
| 3 | "By 1.5 or more" §1026.35(a)(1)(i) | inclusive | NO/**YES**/YES | law.cornell 1026.35 |
| 4 | "does not exceed … by 2.25 or more" §1026.43(e)(2)(vi) | exclusion-inclusive (2.25 FAILS) | PASS/**FAIL**/FAIL | CFPB + interp-43 + FR 2025-22773 |
| 5 | "less than €10m AND less than €1m" (Art 5.5 / EU Art 30) | strict/strict | (9.9,.9)YES; cap-pairs NO | OECD/EU multi-source |
| 6 | "equal to or greater than" + **PREMISE FLAG: 16%-for-2026 is wrong; actual 17%** (15/16/17 for 2023-24/25/26, 3 sources) | inclusive as stated | NO/**YES**/YES + flag | oecdpillars/BEPS/Tiberghien |
| 7 | "at least one half of the SCR" Art 82(1)(a) DR 2015/35 | inclusive | NO/**YES**/YES | EIOPA rulebook + legislation.gov.uk |
| 8 | **INDETERMINATE all models** — no users-leg phrase exists; thresholds are sector-specific (IR 2024/2690: MSP 30min/5%/1M, trust 20min/1%/200k…), Art 23(3) is qualitative | — | — | springlex/nis2insights/Art 23(3) |

R6 graded against the stated phrase (direction skill is the transferable
signal); the rate-premise error is a prompt defect, flagged globally.

## 2. Verdict matrix (R1–R7; R8 INDET ×13) — V=VERIFIED, W=WRONG-RULE, S=SELF-INCONSISTENT

| Model | 1 | 2 | 3 | 4 | 5 | 6 | 7 | Score |
|---|---|---|---|---|---|---|---|---|
| deepseek | V | V | V | V | V | V | V | **7** |
| glm 5.3 flash | V | V | V | V | V | V | V | **7** |
| grok | V | V | V | V | V | V | V | **7** |
| meta | V | V | V | V | V | V | V | **7** |
| mimo [fence] | V | V | V | V | V | V | V | **7** |
| qwen | V | V | V | V | V | V | V | **7** |
| minimax 2.7 [fence] | V | V | V | V+S(lbl) | V | V | V | 6+S |
| kimi | V | V | V | V+S(lbl) | V | V | V | 6+S |
| yuanbao | V | V | V | V+S(lbl) | V | V | V | 6+S |
| chatgpt [raw_decode] | V | V | V | W(AT) | V | V★ | V | 6 |
| gemini [fence] | V | V | V | W(AT) | V | V | V | 6 |
| mistral [fence] | V | V | V | W(AT) | S(vocab) | V | V | 5+S |
| minimax m3 [salvage] | V | V | INDET | W(AT) | V | V | V | 5+I |

Notes: S(lbl) = verdicts right, `strict` label contradicts the "or more"
phrase (kimi/yuanbao/m2.7 R4). S(vocab) = mistral R5 FIRE means
opposite things in R1 vs R5. m3 R3 lost to file damage (delimiter break
ch.671); R1/2/4–8 salvaged as complete objects. PASS-as-negative reading
(chatgpt/deepseek/mistral R1–R3, deepseek R4/R6/R7) confirmed per-row
against each model's own reasoning — never assumed. R5 positional
mappings confirmed against reasoning (deepseek/mimo/m2.7 explicit;
kimi/qwen/yuanbao/gemini/chatgpt positional-consistent).

## 3. Leaderboard (boundary semantics)

Tier 1 (7/7): deepseek, glm 5.3 flash, grok, meta, mimo, qwen. Tier 2
(6 + label): minimax 2.7, kimi, yuanbao. Tier 3 (6, R4 at-miss):
chatgpt — with the standout judgment bonus: **only model to catch the
R6 rate-premise error** (reasoning + weakest_point, OECD-cited; minimax
2.7 hedged it) — gemini. Tier 4: mistral (5+S), minimax m3 (5+I, damaged
file). Hardest cell corpus-wide: **R4 at 2.25 FAILS QM** (4 at-misses);
R8 ungradeable by design.

## 4. Honest closer + quota

Quota-deferred: nothing — all rules resolved (R8 by premise ruling, not
retrieval failure); every ground-truth cell is retrieval-level with
URL+date above. Parse states recorded per model (4 fence-strips, 1
raw_decode, 1 salvage, 1 unrecoverable region). Vocabulary judgments
(PASS-as-negative, R4 labels, mistral R5) each cite the model's own
reasoning as evidence. Boundary discipline held: at-cells decided every
row; no "conservative direction" passes given.

---

## SHADOW-VERIFIER ADJUDICATION (draft) — 2026-09-04 ~14:2xZ (date -u) — CONFIRMED (CS-68), sampled at the decisive cells

**Independent reproductions (bytes + retrieval):** parse states byte-reproduce exactly — chatgpt needs raw_decode (trailing prose), gemini/mistral carry fences, and minimax m3's damage is at char 671 precisely as the report's "delimiter break ch.671" states. Verdict spot-checks at the decisive at-cells all match: chatgpt R4 `strict` + at PASS vs ground truth 2.25-FAILS → W(AT) ✓; gemini R4 at "passes" → W(AT) ✓; chatgpt R6's ★ claim byte-confirmed — its reasoning says verbatim "the current OECD text identifies 17% rather than 16% as the transition rate for fiscal years beginning in 2026 ([OECD][3])" and its weakest_point repeats it — the only model to catch the prompt's rate-premise error ✓; mistral R1 at PASS vs R5 at FIRE confirms the S(vocab) inversion claim ✓; deepseek R1 strict/PASS-as-negative matches both the file bytes and the estate's own art-234 calibration (THRESHOLD-BOUNDARY-SEMANTICS-2026-09-01) ✓. Ground-truth R1/R2 strict and R6's 15/16/17-by-FY correction are retrieval-level with sources named; R8's INDETERMINATE-by-premise ruling (no monolithic users-leg phrase exists; sector-specific thresholds) is the honest handling. Grading against the stated-but-wrong R6 rate while flagging the premise globally is the right call — direction skill is measurable, the prompt defect is quarantined.

**Coverage arithmetic:** 13/13 outputs graded (R1–R7 × 13 + R8 ruled), 4 verdicts independently re-derived to the byte, ground truth 8/8 resolved, quota-deferred: none. Sampled, not exhaustive — the R4 label-contradiction rows (kimi/yuanbao/m2.7) and the minimax-m3 salvage boundary were accepted at report level with the m3 ch.671 anchor byte-proven. Evidence level: bytes + retrieval for the sampled rows, session-level for the rest. Proposal pointer: CS-68.
