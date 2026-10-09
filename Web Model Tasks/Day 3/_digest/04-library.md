# Digest — family `library`

**Prompt:** `..\..\prompts\F-DIAGNOSIS-LIBRARY.md` (prompt-version `F-v2 2026-09-04`) — ordered
differential-diagnosis trees for exactly 10 named ASIC physical-design symptoms.
**Files:** 15 — the largest family, and the only one with a `longcat` and a `sonnet` and a `mistral`
response together.
**Nature of the family:** recalled practice, explicitly not data. The prompt makes that structural:
every frequency label carries its own `recall_confidence`, and the value is asserted to live in the
`discriminating_experiments`. **Nothing here is checkable against a document; what is checkable is
schema conformance, calibration shape, and cross-model convergence on the discriminators.**

---

## 1. Parse status and coverage

| Model | Parse | Symptoms | Canonical order? |
|---|---|---|---|
| chatgpt, deepseek, gemini, grok, meta, mistral, qwen, sonnet, yuanbao | clean | 10 | ✔ 1→10 |
| glm 5.3 flash, kimi, mimo, minimax 2.7 | clean after fence strip | 10 | ✔ 1→10 |
| **longcat** | **truncated** — file ends mid-string inside a `discriminating_experiments` entry, no closing bracket | **4 recovered** | ✔ 1→4 |
| **minimax m3** | **truncated** — file ends mid-string inside a `common_root_causes` entry, no closing bracket | **5 recovered** | ✔ 1→5 |

**13 of 15 files emit all ten canonical symptoms in the prompt's exact order.** The two exceptions
are truncated files, not short answers — see §6. Because the truncation is at the file level, **it is
unknown whether longcat and minimax m3 produced ten symptoms**; this digest records 4 and 5
*recovered*, never as their answer length.

---

## 2. Schema — the most conformant family in the corpus

All twelve required paths are present in **15 of 15** files, including the nested ones:

```
symptom                                        15/15
first_checks[].check                           15/15
first_checks[].why_first                       15/15
first_checks[].check_cost                      15/15
discriminating_experiments[].experiment        15/15
discriminating_experiments[].rules_in          15/15
discriminating_experiments[].rules_out         15/15
common_root_causes[].cause                     15/15
common_root_causes[].recalled_frequency        15/15
common_root_causes[].recall_confidence         15/15
classic_trap                                   15/15
node_era_note                                  15/15
```

**Cardinality.** The prompt asks for 2–4 first checks, 2–4 experiments, 3–5 root causes.
**Every count in every file is in range** — first_checks 3–4, experiments 2–4, causes 3–5. No model
padded or under-filled.

**Enum conformance.** `recalled_frequency` uses only `common` / `occasional` / `rare` in all 15 files
— zero off-enum values across 611 root-cause entries. `check_cost` uses only `minutes` / `hours` /
`days` in 14 files; **one off-enum value corpus-wide**: `minimax 2.7` writes `"minutes to hours"`
once (its other 39 checks are in-enum). Corpus tally: `minutes` 378, `hours` 112, `days` 1
(yuanbao), `minutes to hours` 1.

### Two schema contaminations — see `00-corpus-and-harness.md` §6

| File | Extra fields not in `F-DIAGNOSIS-LIBRARY.md` | Extent |
|---|---|---|
| `mimo library.json` | `not_in_paper`, `paper_vs_general`, `weakest_point` | **10/10 items**. Every `paper_vs_general` is the literal POWER4-recall enum string `"from-general-POWER4-knowledge-not-necessarily-this-paper"` (first at char 3,840) |
| `glm 5.3 flash library.json` | `not_in_paper` | **10/10 items**, all `false` (first at char 3,741) |

Required fields are present in both — this is addition, not substitution. mimo's `weakest_point`
values are nonetheless on-topic for this family (e.g. *"Frequency labels and discrimination logic are
from general practice, not any single documented case"*), so the contamination is at the field-name
level, not the content level.

### One field-naming anomaly

`chatgpt library.json` emits the node-era escape token as a **key** in addition to a real prose
`node_era_note`, and spells that key three different ways across ten items:

```
@char  3204 : …than it was at 28nm.","no_era_difference_recalled":"no-era-difference-recalled"}
@char  6395 : …older-node designs.","no_era_difference_recalled":"no-era-difference-recalled"}
@char  9287 : …hold closure.","no-era-difference_recalled":"no-era-difference-recalled"}
@char 12329 : …prominent than at 28nm.","no-era-difference-recalled":"no-era-difference-recalled"}
```

Ten occurrences, three spellings (`no_era_difference_recalled`, `no-era-difference_recalled`,
`no-era-difference-recalled`). Each sits beside a populated `node_era_note` containing real prose, so
**the escape and its negation are asserted in the same object.** A schema validator will see three
unknown keys; a semantic reader should ignore them.

---

## 3. `node_era_note` — the escape is almost never used

Of 139 recovered items, **two** carry the escape token, both in `grok library.json`. The other 137
carry substantive 28nm-vs-7nm prose. Sample first-item values:

```
meta      "At 28nm congestion correlated with cell density; at 7nm-and-below congestion occ…"
mistral   "7nm-and-below: more routing layers reduce congestion severity, but power grid de…"
gemini    "At 7nm and below, unidirectional routing rules and extreme pin-access track offs…"
```

**Note the substantive divergence inside this near-unanimity:** for symptom 1, thirteen models say
7nm makes congestion *worse* or *less correlated with density*; `mistral` says *"more routing layers
reduce congestion severity"*. That is an opposite-direction claim on the same cell, and it is the
only one in the field.

---

## 4. Convergence on the load-bearing cell — `classic_trap`

The prompt states the value is in discrimination, not description. `classic_trap` for symptom 1
(congestion DRCs with clean placement density) shows **14 of 15 models converging on one answer, in
independent wording**: *the engineer blames global placement density and re-spreads cells, when the
real cause is local pin access, macro channels, blockages or power straps.*

```
chatgpt      "Treating clean average utilization as proof of routability and immediately spreading
              the whole block, when the actual problem is often …"
minimax 2.7  "Assuming cell density is the proxy for routability — the real bottleneck is pin
              density, which most density reports do not surface by d…"
kimi         "Blaming placement density when the issue is actually macro pin access or orientation"
sonnet       "Assuming overall placement density is the culprit and globally spreading cells, which
              wastes area/timing without fixing a localized pin…"
meta         "Spreading placement to lower density, which increases wirelength and makes congestion
              and routing DRCs worse instead of fixing pin/bloc…"
```

The one file outside the cluster is `minimax m3` — *"Trusting the placer's reported utilization as a
true picture of the placed design without checking the actual routing congestion heatma…"* — which
names the same underlying error but locates it in tool reporting rather than in the engineer's
response.

**For the episode pipeline this is the useful shape: fifteen independent phrasings of one
discriminator.** The convergent core is corpus-supported without any external document; the
divergent tails (mistral's 7nm claim in §3, minimax m3's framing here) are the items a practitioner
reviewer should be shown.

---

## 5. Calibration — `recall_confidence` spreads nearly 2× across models

Per file, over all `common_root_causes[].recall_confidence` values:

| model | causes | conf range | mean | frequency mix (common / occasional / rare) |
|---|---|---|---|---|
| gemini | 30 | 0.80–0.95 | **0.872** | 13 / 17 / **0** |
| chatgpt | 50 | 0.68–0.94 | 0.821 | 24 / 22 / 4 |
| mistral | 41 | 0.50–0.90 | 0.746 | 19 / 12 / 10 |
| longcat | 16 | 0.60–0.90 | 0.728 | 8 / 4 / 4 |
| deepseek | 41 | 0.50–0.85 | 0.707 | 20 / 19 / 2 |
| grok | 40 | 0.55–0.85 | 0.696 | 19 / 20 / 1 |
| minimax 2.7 | 49 | 0.55–0.80 | 0.691 | 20 / 19 / 10 |
| kimi | 40 | 0.40–0.90 | 0.688 | 19 / 19 / 2 |
| yuanbao | 39 | 0.50–0.85 | 0.681 | 20 / 14 / 5 |
| mimo | 44 | 0.50–0.90 | 0.674 | 14 / 26 / 4 |
| meta | 50 | 0.45–0.85 | 0.669 | 21 / 20 / 9 |
| qwen | 50 | 0.50–0.75 | 0.627 | 24 / 23 / 3 |
| minimax m3 | 25 | 0.40–0.80 | 0.604 | 10 / 10 / 5 |
| glm 5.3 flash | 46 | 0.35–0.75 | 0.572 | 22 / 19 / 5 |
| **sonnet** | 50 | **0.30–0.60** | **0.451** | 19 / 19 / **12** |

Two ends worth the verifier's attention, stated as observations not judgements:

- **`gemini` never labels any cause `rare`** — 30 causes, all `common` or `occasional` — and carries
  the highest mean confidence (0.872) with the narrowest band (0.80–0.95). It also emits the fewest
  causes per symptom (3 everywhere) and exactly 2 experiments everywhere. Its file is uniformly
  minimum-cardinality and maximum-confidence.
- **`sonnet` is the inverse**: 50 causes, 12 labelled `rare`, mean 0.451, ceiling 0.60. No confidence
  in its file exceeds 0.60.

**The prompt states that *"a low-confidence frequency beats a confident-sounding invention."* This
table is the raw material for testing whether that instruction changed behaviour; the digest does not
score it.**

---

## 6. Truncation cluster — a transport signature, not a model behaviour

Four files in the Day 3 corpus are damaged. **All four belong to exactly two models**, and three
terminate within 92 bytes of each other:

| file | bytes | damage |
|---|---|---|
| `minimax m3 library.json` | 17,528 | truncated mid-string |
| `longcat library.json` | 17,520 | truncated mid-string |
| `minimax m3 patterns.json` | 17,436 | mid-string splice (see `05-patterns.md`) |
| `minimax m3 aprc.json` | 9,575 | two case objects fused, no `},{` |

Files from other models far exceed this length without damage — `minimax 2.7 library.json` 54,686
bytes, `mimo library.json` 46,983, `glm 5.3 flash library.json` 39,660, `qwen library.json` 36,112 —
so **there is no corpus-wide cap; the ~17.4–17.5 KB ceiling is specific to the longcat and
minimax m3 collection surfaces.** `dispatch-state.json` records `minimax-m3 (gmi)` as a raw-API
control at `console.gmicloud.ai` (`temp 0.5 top_p 0.9`); `longcat` appears nowhere in that file.

**Consequence for grading: longcat's and minimax m3's short library answers must not be read as
sparse recall.** The truncation is upstream of the model's output length.

---

## 7. Consensus / outlier map

**Full-conformance core** (10 symptoms, canonical order, all cardinalities and enums in range, no
extra fields): `deepseek`, `grok`, `kimi`, `meta`, `minimax 2.7`¹, `mistral`, `qwen`, `sonnet`,
`yuanbao`, `gemini`².
¹ one off-enum `check_cost`. ² minimum cardinality throughout, see §5.

| model | outlier axis | evidence |
|---|---|---|
| chatgpt | field naming | 10 stray escape-token keys, 3 spellings (§2) |
| mimo | schema contamination | POWER4-recall fields on 10/10 items (§2) |
| glm 5.3 flash | schema contamination | `not_in_paper` on 10/10 items; lowest-but-one confidence mean |
| gemini | calibration shape | zero `rare` labels; highest mean confidence; minimum cardinality everywhere |
| sonnet | calibration shape | confidence ceiling 0.60; 12 `rare` labels, the most in the family |
| mistral | one substantive reversal | symptom-1 `node_era_note` claims 7nm *reduces* congestion severity where 13 models claim the opposite (§3) |
| longcat, minimax m3 | transport damage | truncated at ~17.5 KB (§6) |

---

## 8. Flags for the pipeline

1. **This family is the corpus's schema-conformance benchmark** — 15/15 on all twelve required
   paths, all cardinalities in range, one off-enum value in 492 `check_cost` entries. Any validator
   built here should be reused on the other four families, which are markedly less conformant.
2. **Strip, do not reject, the contaminating fields** in `mimo` and `glm 5.3 flash`. The required
   content is intact.
3. **Ignore chatgpt's three stray key spellings**; its `node_era_note` prose is the real value.
4. **Do not treat longcat (4) and minimax m3 (5) as short answers** — flag as truncated at
   collection and re-collect if those two models matter to the sample.
5. **Nothing in this family is document-checkable.** The gradable surface is (a) schema, (b)
   calibration shape, (c) whether a discriminator actually discriminates. For (c), the symptom-1
   `classic_trap` cluster (§4) is fifteen independent statements of one claim and is the natural
   first candidate for practitioner review.
6. **One substantive contradiction is worth adjudicating**: mistral's 7nm-reduces-congestion claim
   against thirteen contrary files (§3). It is a single cell and a single question.
