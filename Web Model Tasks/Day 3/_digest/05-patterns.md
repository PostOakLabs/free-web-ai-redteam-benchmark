# Digest — family `patterns`

**Prompt:** `..\..\prompts\G-SDC-PATTERNS.md` (prompt-version `G-v2 2026-09-04`) — up to 10 SDC
constraint-derivation patterns, each with a `wrong_way`, a `signoff_risk` in both directions, a
`provenance` enum, a `recall_confidence`, and a per-number confidence wherever arithmetic appears.
**Files:** 14. **13 parse. One does not.**
**Nature of the family:** like `library`, unverifiable against any document. Unlike `library`, this
prompt names a *labelling* failure as its worst output — *"mislabeling textbook material as practice
judgment is the worst possible output — worse than omitting the pattern"* — which makes the
`provenance` field, not the content, the load-bearing cell. §5.

---

## 1. Parse status

| Model | Parse | Patterns |
|---|---|---|
| chatgpt, deepseek, meta, mistral, sonnet, yuanbao, grok, gemini, qwen | clean | 10 / 10 / 8 / 10 / 7 / 8 / 8 / 6 / 8 |
| glm 5.3 flash, kimi, mimo, minimax 2.7 | clean after fence strip | 8 / 10 / 8 / 10 |
| **minimax m3** | **WILL NOT PARSE** | **0** |

### `minimax m3 patterns.json` — the one hard failure in the Day 3 corpus

```
json.loads → Expecting ':' delimiter at char 2161 (line 9, col 49)

seam at char 2051:
  …r block now must absorb the leftover; at system integration the path fails
  ew/jitter/OCV) ≈ 10–15% of T (confidence 0.5)",
  "K (margin) ≈ 5–10% of T (confidence 0.5)",
  "L:I:C split 1:1:1 is a starting heuristic…
```

This is **not truncation**. A string literal is cut mid-word (`the path fails` → `ew/jitter/OCV)`)
and content belonging to a later array element is spliced onto it, destroying the closing quote of
the first. The file's last non-space character is `]`, so the outer array is closed, and an
object-boundary scan finds **8 complete top-level objects after the seam** — but element 0 is
unrecoverable and the file cannot be loaded as JSON.

**Reported as unparseable and excluded from every statistic below. Not repaired, not partially
salvaged into the counts.** It belongs to the same two-model damage cluster described in
`04-library.md` §6: at 17,436 bytes it sits within 92 bytes of `minimax m3 library.json` (17,528) and
`longcat library.json` (17,520), all three damaged, while undamaged files from other models run to
54,686 bytes. **Treat as a collection-surface defect, not a model output.**

---

## 2. Schema

Prompt's nine-field item schema, present in **13 of 13 parsed files**:
`pattern_name`, `situation`, `derivation`, `wrong_way`, `defense`, `signoff_risk`, `provenance`,
`recall_confidence`, `node_era_note`. **ABSENT in: `minimax m3` (file unparseable).**

Pattern counts: 10 (chatgpt, deepseek, kimi, minimax 2.7, mistral), 8 (glm 5.3 flash, grok, meta,
mimo, qwen, yuanbao), 7 (sonnet), 6 (gemini). The prompt says *"up to 10"* and *"fewer sharp patterns
beat ten padded ones"*, so every count is compliant.

**Enum conformance: perfect.** All 111 `provenance` values across 13 files are one of
`recalled-from-practice` / `textbook-standard` / `tool-default-idiom`. Zero off-enum values.

### The per-number confidence requirement is met four different ways

The prompt asks for *"a per-number confidence wherever arithmetic appears … e.g. 'assumes 15% margin
(confidence 0.6)'"*. It does not specify a field. Models chose:

| mechanism | models | count |
|---|---|---|
| **inline in prose**, matching the prompt's example form | meta (43 occurrences), mimo (16), qwen (13), yuanbao (10), chatgpt (8), glm 5.3 flash (7), kimi (3), sonnet (3), grok (2), mistral (2), gemini (1) | 11 |
| **dedicated object** `arithmetic_confidences` keyed by the value | **deepseek** — keys are literal numbers: `period=5ns`, `input_delay=2.8ns`, `output_delay=1.8ns`, `margin=15%`, `T_final=10ns`, `divide_by=2`, `alpha=0.6`, `A_budget=4.7ns`, `B_budget=2.3ns`, `ICG_setup=0.5ns`, `ICG_hold=0.3ns`, … | 1 |
| **dedicated object** `arithmetic_confidence` keyed by concept | **mimo** — `split_55_45`, `interconnect_400ps`, `margin_10_15_pct`, `early_margin_25_30_pct`, `setup_50ps`, `period_2000ps`, `degradation_200_400ps`, `depth_greater_than_2x_ratio` | 1 |
| **dedicated field** `_numeric_confidence_notes` | **sonnet** | 1 |
| **none found** | **minimax 2.7** — 10 patterns, zero inline `(confidence 0.x)` markers and no confidence sub-object, despite `derivation` fields averaging 359 characters with arithmetic | 1 |

**deepseek and mimo produce machine-readable per-number confidences; the other eleven produce prose
that must be regex-mined.** deepseek's key naming (`period=5ns`) makes the assumed value and its
confidence a single addressable pair — the only form in the corpus that survives extraction without
parsing English.

---

## 3. Convergent pattern taxonomy

Eight topics recur across nearly every file, in near-identical order. Naming differs; substance does
not. **Coverage below is measured on `pattern_name` only** — a topic marked "no name match" may still
be discussed inside another item's `situation` or `derivation`, so these are name-level counts, not
claims that the content is absent:

| # | topic | files with a matching `pattern_name` |
|---|---|---|
| 1 | block-boundary input/output delay budget split | **13/13** |
| 2 | false path vs multicycle path (decision + defence) | **13/13** |
| 3 | clock-domain crossing / synchronizer constraint | **13/13** |
| 4 | early over-constraining and planned relaxation | **13/13** |
| 5 | virtual clock for IO | **13/13** |
| 6 | generated / divided clock constraint | 12/13 — no name match in `kimi` |
| 7 | asynchronous interface / handshake constraint | 12/13 — no name match in `kimi` |
| 8 | budgeting not-yet-implemented blocks | 11/13 — no name match in `gemini`, `mimo` |

Five topics are named by every parsed file. `kimi` covers topic 8 inside its topic-1 title
(*"Block boundary I/O delay budget for unimplemen[ted]…"*) and adds a second, *"RTL-complexity-based
timing budget for unimple[mented]…"*.

Distinct tails worth keeping: `kimi` adds *"Combinational feedthrough max_delay budgeting"*,
*"Post-CTS clock uncertainty update from actual skew"*, *"Mode-based case analysis for multiplexed
clocks"*; `glm 5.3 flash` adds *"Mode-scoped case analysis and per-mode exception sco…"* and
*"Asynchronous reset constraint: assertion async by co…"*; `deepseek` adds *"Clock-gating check
(enable path) timing constraint"*; `mistral` adds *"clock_latency_budgeting"* and
*"uncertainty_allocation_in_derived_clocks"*.

`mistral` is the only file using snake_case pattern names throughout
(`block_boundary_io_delay_budgeting`, `false_path_vs_multicycle_decision`, …); every other file uses
prose titles. Cosmetic, but it means name-based joins across files need normalisation.

---

## 4. `wrong_way` and `signoff_risk` — the fields the prompt calls load-bearing

The prompt: *"the `wrong_way` and `signoff_risk` fields carry the real value — a pattern without a
failure mode is a textbook entry, not engineering judgment"*, and `signoff_risk` must state *"what
happens at signoff if this constraint is wrong in each direction (too tight vs too loose)"*.

`wrong_way` is populated in **all 111 items across 13 files** — median length by model ranges from
**151 chars (mistral)** to **574 chars (mimo)**:

```
mistral 121/151   grok 157/199   chatgpt 164/220   yuanbao 173/234   kimi 183/240
glm 187/311       qwen 218/260   gemini 244/254    deepseek 168/263  meta 285/318
minimax 2.7 302/359   sonnet 381/436   mimo 399/574          (min / median)
```

**`signoff_risk` naming both directions explicitly** — the specific thing the prompt asked for:

| model | items naming both "too tight" and "too loose" |
|---|---|
| chatgpt, deepseek, kimi, minimax 2.7 | **10 / 10** |
| glm 5.3 flash, meta | **8 / 8** |
| qwen, yuanbao | 7 / 8 |
| sonnet | 6 / 7 |
| gemini | 5 / 6 |
| **mistral** | **4 / 10** |
| **mimo** | **1 / 8** |
| **grok** | **1 / 8** |

Eleven of thirteen files satisfy the two-direction requirement on nearly every item. **`grok` and
`mimo` state a single-direction risk on seven of eight items each** — notable in mimo's case because
its `wrong_way` fields are the longest in the family (median 574 chars). Length and requirement
coverage are independent here.

---

## 5. The load-bearing cell — `provenance`

The prompt makes a specific claim about failure: labelling textbook material as practice judgement is
worse than omitting the pattern. **The distribution of that label is therefore the family's primary
evidence, and it is sharply bimodal.**

| model | `recalled-from-practice` | `textbook-standard` | `tool-default-idiom` | practice share |
|---|---|---|---|---|
| **grok** | 8 | 0 | 0 | **100%** |
| **kimi** | 10 | 0 | 0 | **100%** |
| **minimax 2.7** | 10 | 0 | 0 | **100%** |
| **mistral** | 10 | 0 | 0 | **100%** |
| deepseek | 8 | 0 | 2 | 80% |
| glm 5.3 flash | 6 | 2 | 0 | 75% |
| meta | 6 | 2 | 0 | 75% |
| mimo | 6 | 2 | 0 | 75% |
| sonnet | 5 | 2 | 0 | 71% |
| chatgpt | 7 | 3 | 0 | 70% |
| gemini | 4 | 2 | 0 | 67% |
| yuanbao | 5 | 3 | 0 | 62% |
| **qwen** | 3 | **4** | 1 | **38%** |

**Four models label every pattern they emit as recalled practice. One model (`qwen`) labels the
plurality as textbook-standard** — the only file where `textbook-standard` outnumbers
`recalled-from-practice`. Only `deepseek` and `qwen` use `tool-default-idiom` at all (2 and 1).

**This digest does not judge whether any label is correct.** It records that the label is a
self-report, that the corpus contains both a 100%-practice pole and a 38%-practice pole on the same
eight-topic taxonomy (§3), and that **the same eight patterns are called practice by grok/kimi/
minimax 2.7/mistral and textbook by qwen.** That head-to-head on a shared taxonomy is the cheapest
available test of the prompt's stated failure mode, and it needs a practitioner, not a document.

---

## 6. `recall_confidence` — two separated bands

| band | models | range |
|---|---|---|
| **high** | chatgpt 0.84–0.96 · deepseek 0.85–0.95 · gemini 0.85–0.95 | 0.84–0.96 |
| **middle** | kimi 0.65–0.85 · meta 0.68–0.85 · mimo 0.65–0.80 · minimax 2.7 0.70–0.80 · grok 0.65–0.80 · mistral 0.75–0.90 · yuanbao 0.60–0.85 | 0.60–0.90 |
| **low** | glm 5.3 flash 0.50–0.75 · qwen 0.55–0.72 · sonnet 0.45–0.60 | 0.45–0.75 |

The bands do not track the provenance poles. `mistral` sits in the upper-middle band (0.75–0.90)
while labelling 100% of its patterns as practice **and** producing the shortest `wrong_way` fields in
the family (median 151 chars) and the weakest two-direction `signoff_risk` coverage among the
10-pattern files (4/10). `qwen` sits in the low band while making the most conservative provenance
claims. **Confidence and provenance are independent self-reports in this corpus; neither validates
the other.**

Cross-family note: the same three models occupy the low-confidence band in `library` — sonnet
(mean 0.451), glm 5.3 flash (0.572), qwen (0.627) — and the same models occupy the high band
(gemini 0.872, chatgpt 0.821). **Confidence banding appears to be a stable per-model trait rather
than a per-task judgement.** That is a hypothesis the two families jointly support and neither
proves.

---

## 7. Consensus / outlier map

**Full-conformance core** — nine fields on every item, both `signoff_risk` directions on nearly every
item, in-enum provenance, per-number confidences present: `chatgpt`, `deepseek`, `kimi`,
`minimax 2.7`, `glm 5.3 flash`, `meta`.

| model | outlier axis | evidence |
|---|---|---|
| **minimax m3** | **unparseable** | mid-string splice at char 2051 (§1) |
| qwen | provenance pole | the only file where `textbook-standard` (4) outnumbers `recalled-from-practice` (3) |
| grok, kimi, minimax 2.7, mistral | provenance pole | 100% `recalled-from-practice` |
| grok, mimo | requirement coverage | `signoff_risk` names one direction only on 7 of 8 items |
| minimax 2.7 | requirement coverage | no per-number confidence found by any mechanism (§2) |
| mistral | field depth | shortest `wrong_way` (median 151 chars); snake_case naming; 4/10 two-direction `signoff_risk` |
| mimo | field depth | longest `wrong_way` (median 574) yet 1/8 two-direction `signoff_risk` |
| deepseek | structure, favourably | the only machine-readable per-number confidence keyed by the value itself |
| gemini | coverage | 6 patterns, the fewest; no `pattern_name` for the not-yet-implemented-block budget (topic 8) |

---

## 8. Flags for the pipeline

1. **`minimax m3 patterns.json` must be re-collected, not repaired.** The splice is in element 0 and
   the recovered remainder cannot be attributed with confidence to the intended pattern boundaries.
2. **`provenance` is the gradable cell here** — the prompt defines the failure mode in terms of it.
   The 100%-practice files (grok, kimi, minimax 2.7, mistral) and the 38% file (qwen) describe the
   *same eight topics* (§3), so a reviewer can compare like with like on one shared taxonomy.
3. **Two models emit extractable per-number confidences** (deepseek `arithmetic_confidences`, mimo
   `arithmetic_confidence`); the other eleven require regex-mining `(confidence 0.x)` out of prose,
   and `minimax 2.7` supplies none at all. If per-number confidence matters downstream, prefer
   deepseek's key-value form as the target schema.
4. **`signoff_risk` two-direction coverage is a cheap conformance metric** and it separates the
   corpus 11-to-2. It is independent of `wrong_way` length — do not use verbosity as a proxy.
5. **Normalise `pattern_name` before any cross-file join** — mistral is snake_case, every other file
   is prose, and the same pattern appears under 13 different titles.
6. **The confidence-band observation spans this family and `library`** (§6). If that stability holds
   across more families it is a per-model calibration constant worth recording once, rather than a
   finding to re-derive per task.
