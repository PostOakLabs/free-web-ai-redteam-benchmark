# Decline table and model-set completeness

Commission §3.5: the decline table is first-class, so that **"no findings against a model" is never
readable as "that model was clean."** As-of 2026-09-09T14:11:04Z.

---

## 1. Day 5 has no decliners

**This is the first day in the corpus where no model declined anything.** All 16 models answered all
5 families: 80 of 80 cells filled.

Day 4's contrast, for calibration: **9 of 16 models declined every quote of every paper**, including
the strongest Day-2 arithmetic performer. On Day 4 the decline table was the difference between
"clean" and "silent". Here it is empty, and that is a fact about Day 5, not a compliment to the
models — every Day-5 prompt asks for computation or review, and none offers a
`cannot-reproduce-verbatim` style escape.

## 2. Full coverage grid

`regz` = exact values matched of 9 · `strings` = JCS cases correct of 4 (case 5 ungradable) ·
`e-shape` = formula shapes OK · `red1`/`red3` = review verdict.

| model | regz /9 | strings /4 | e-shape | red1 | red3 |
|---|---|---|---|---|---|
| chatgpt | **9** | NOT GRADABLE | 6 | S-W-RES | S-W-RES |
| deepseek | **9** | 3 | 4 | S-W-RES | S-W-RES |
| gemini | **9** | 2 | 6 | S-W-RES | **SOUND (bare)** |
| glm 5.3 flash | **9** | 3 | 8 | S-W-RES | S-W-RES |
| grok | **9** | **4** | 7 | S-W-RES | **SOUND (bare)** |
| kimi | **9** | **4** | 4 | S-W-RES | S-W-RES |
| longcat | **9** | 3 | 7 | SUSPECT | SOUND +2 obj |
| meta | **9** | **4** | 6 | S-W-RES | **SOUND (bare)** |
| mimo | **9** | 2 | 4 | S-W-RES | S-W-RES |
| minara | **9** | **4** | 6 | S-W-RES | S-W-RES |
| minimax 2.7 | 5 | 2 | 4 | S-W-RES, 0 obj | **SOUND (bare)** |
| mistral | 2 | 1 | 3 | S-W-RES | S-W-RES |
| qwen | **9** | 2 | 6 | S-W-RES | **SOUND (bare)** |
| solar | NOT GRADABLE | 3 | 6 | S-W-RES | NOT GRADABLE |
| sonnet | **9** | **4** | 8 | S-W-RES | S-W-RES |
| yuanbao | **9** | 3 | **9** | S-W-RES | S-W-RES |

## 3. The three NOT-GRADABLE cells — none is a model decline

Every gap in the grid is a delivery or format defect, recorded as such:

| cell | cause |
|---|---|
| `chatgpt` × `strings` | salvage recovered no case-shaped records. The file's escaping is inconsistent within a single string (`\"€\":\"euro","$":"dollar"` — escaped and unescaped in the same value), so no repair rung produces case objects. Content exists; structure does not |
| `solar` × `regz` | **PROSE-NOT-JSON** — answered in English with markdown tables |
| `solar` × `red3` | element-wise recovery returned 3 objects, none carrying a `verdict` |

**None of these is a refusal.** All three models produced substantive content that this digest could
not grade mechanically. Reading them as non-answers would be wrong.

## 4. Model-set completeness

**16 of 16 models filed all 5 families.** No absences to record — the first such day.

The 15 legacy models plus `minara`, the new arrival, which filed under **two spellings**
(`minara` on e/red1/regz, `minaria` on red3/strings). Merged to one model, files unrenamed, dual
spelling carried in `d5permodel.json` as `spellings_as_collected`. The operator confirms the canonical name
at checkoff.

Had the merge not been applied, this page would report 17 models with two partial ghosts, and every
per-model denominator in the digest would be wrong.
