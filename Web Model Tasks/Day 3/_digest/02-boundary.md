# Digest — family `boundary`

**Prompt:** `..\..\prompts\C1-BOUNDARY-VERDICTS.md`, delivered verbatim as `_payload.txt` /
`_payload.b64`. Eight regulatory comparators, three inputs each (below / at / above the boundary),
plus a per-rule `phrase_inclusivity` label and a one-sentence `reasoning`.
**Files:** 13. **All 13 parse.** `sonnet boundary.json` is ABSENT from disk (see
`00-corpus-and-harness.md` §1).
**Nature of the family:** 312 verdict cells (13 models × 8 rules × 3 slots) that the prompt intends
to be graded mechanically. **The single most important finding is that they cannot be, as written —
the verdict vocabulary is unnormalised and polarity-inverted between models.** See §3.

---

## 1. Parse and shape

| Model | Parse | Rules | Top-level shape |
|---|---|---|---|
| chatgpt | clean (+ trailing reference-link footer `[1]: https://www.consumerfinance.gov/rul…`) | 8 | list |
| deepseek | clean | 8 | **object** `{"rules": [...], "weakest_point": ...}` |
| gemini, minimax 2.7, mimo, mistral | clean after fence strip | 8 / 8 / 8 / 9 | list |
| glm 5.3 flash, grok, kimi, meta, qwen, yuanbao | clean | 8 | list |
| minimax m3 | recovered — a `"key": "value"` pair sitting inside an array | 8 | **object** `{"rules": [...], "weakest_point": ...}` |

`mistral` emits 9 items for 8 rules: its 9th is a `{"weakest_point": …, "reason": …}` object folded
into the rules list rather than kept separate (§2).

**Two container shapes.** Eleven files are a bare list; `deepseek` and `minimax m3` wrap the rules in
`{"rules": [...]}`. A loader keyed to a list will read those two as zero rules.

---

## 2. Schema

| Field | Present | ABSENT in |
|---|---|---|
| `rule` | 13/13 | — |
| `phrase_inclusivity` | 13/13 | — |
| `verdicts` (with `below`/`at`/`above`) | 13/13 | — |
| `reasoning` | 13/13 | — (on rule items; mistral's 9th item uses `reason` instead) |
| `weakest_point` | 13/13 | — (see placement note below) |

**Two shape notes on `mistral boundary.json`.** Its `weakest_point` is **present**, but as the 9th
element of the rules list rather than a separate trailing object:
`{"weakest_point": "Rule 5 (GloBE de-minimis)", "reason": "The phrasing of the dual conditions ('le…"}`
— it pairs the flag with a `reason` key where every other model would use `reasoning`. A loader that
iterates rule items will try to read it as a rule. Separately, **mistral's `rule` values are JSON
strings** (`"1"`, `"2"`, …) where all twelve other files use integers; a numeric key join drops the
whole file.

One cell is missing inside an otherwise complete object: **`minimax m3` rule 3 has no `at` key** —
`verdicts` carries `below` and `above` only. Reported here as **ABSENT**, not inferred from its
neighbours.

---

## 3. The load-bearing problem: the verdict vocabulary is not normalised

Rule 1 (HOEPA prepayment penalty, *"can exceed … more than 2 percent"*). **All 13 models label the
phrase `strict`, and all 13 agree substantively**: no trigger at 1.99% or 2.00%, trigger at 2.01%.
They express the identical "does not fire" verdict in **seven different tokens**:

| model | `verdicts.below` (all mean *the trigger does not fire*) |
|---|---|
| chatgpt, deepseek, mistral | `PASS` |
| mimo | `PASS — 1.99% is not 'more than' 2%; trigger does not fire.` |
| glm 5.3 flash, kimi | `NO FIRE` |
| minimax 2.7 | `NO FIRE (1.99% ≤ 2.00%, not more than)` |
| minimax m3 | `NO FIRE` |
| grok, qwen | `NO` |
| meta | `NO_FIRE at 1.99%` |
| gemini | `does not fire` |
| **yuanbao** | **`FAIL`** |

**`PASS` and `FAIL` are used by different models to express the same verdict.** chatgpt writes
`PASS` for "the loan passes — no HOEPA trigger"; yuanbao writes `FAIL` for "the test fails to fire".
A grader doing string comparison scores these as opposite. Rule 2 reproduces the pattern exactly.

**This inverts again between rules.** In rules 6 and 7 (safe-harbour and Tier-1 floor, both framed as
tests to be *met*), chatgpt/kimi/meta/qwen/yuanbao use `PASS` for the satisfied case at the
boundary — while `deepseek` and `mistral` write `FIRE` for the same satisfied case, and
`minimax m3` writes domain words (`SAFE HARBOUR`, `COMPLIANCE`, `NO COMPLIANCE`).

**Pipeline consequence: no cell in this family is machine-gradable without a per-model, per-rule
token map.** Four models make their rows self-describing by inlining the input value or the semantic
outcome with the verdict — `meta` (`NO_FIRE at 1.99%`), `mimo`, `minimax 2.7`, and `minimax m3`
(domain words). Those rows survive normalisation; the bare `PASS`/`FAIL`/`NO` rows do not.

---

## 4. Rules 1, 2, 3, 6, 7, 8 — substantive agreement

Once vocabulary is set aside, six of eight rules are unanimous or near-unanimous, and the
`phrase_inclusivity` label is unanimous on all six:

| Rule | inclusivity (13/13 agree) | at-boundary outcome | dissent |
|---|---|---|---|
| 1 — HOEPA prepay *"more than 2 percent"* | `strict` | does not fire at 2.00% | none |
| 2 — HOEPA duration *"more than 36 months"* | `strict` | does not fire at 36 | none |
| 3 — HPCT *"1.5 or more percentage points"* | `inclusive` | fires at 1.50 | `minimax m3` — **`at` key ABSENT** |
| 6 — CbCR simplified ETR *"equal to or greater than"* 16% | `inclusive` | satisfied at 16.00% | none |
| 7 — Solvency II Tier 1 *"at least equal to"* 50% | `inclusive` | satisfied at 50.00% | none |
| 8 — NIS2 users leg *"equal to or greater than"* | `inclusive` | satisfied at threshold | none |

**Rule 3 has one internal inconsistency worth flagging**: `minimax 2.7` labels the phrase
`inclusive` and writes `below: NO (1.49 pp < 1.50 pp, below the threshold)` then
`at: PASS (1.50 pp = 1.50 pp, exactly at the threshold)` — using `PASS` where its own rule-1 row
used `NO FIRE`/`FIRE`. Same file, opposite polarity convention between rules.

---

## 5. Rule 4 — the genuine divergence

General QM price limit. The prompt states the **pass** condition: APR *"does not exceed APOR … by
2.25 or more percentage points"*. This is the only rule in the set framed as a pass condition rather
than a trigger, and it is the only rule where models disagree on both the label and the outcome.

**`phrase_inclusivity` splits 4 / 8 / 1:**

- `strict`: chatgpt, kimi, mistral, yuanbao
- `inclusive`: deepseek, gemini, glm 5.3 flash, grok, meta, mimo, minimax m3, qwen
- `strict (for the pass condition)`: minimax 2.7 — the only hedged value in 104 inclusivity cells

**The label does not predict the verdict.** chatgpt says `strict` → `at: PASS`. kimi says `strict` →
`at: FAIL`. **The same label attached to opposite outcomes in the same rule.**

**Verdicts at the 2.25 boundary, grouped by meaning rather than token:**

| Meaning at 2.25 | models | tokens used |
|---|---|---|
| **does not qualify as General QM** (9) | glm 5.3 flash, grok, kimi, meta, qwen, yuanbao | `FAIL`, `NO`, `FAIL at 2.25` |
| | deepseek, mimo | `FIRE` — trigger-polarity for the same meaning |
| | minimax 2.7 | `FAIL (2.25 pp = 2.25 pp, does exceed by 2.25 or more — not a passing spread)` |
| **does qualify** (3) | chatgpt, gemini, minimax m3 | `PASS`, `passes`, `PASS` |
| **internally mixed** (1) | mistral | `below: PASS`, `at: PASS`, `above: FIRE` — pass-polarity in two slots, trigger-polarity in the third, within one row |

**Two models independently name the same premise risk on this rule**, and it is the risk that would
flip it:

> `kimi.weakest_point`: *"Rule 4 (General QM price limit): the actual regulatory text may use 'more
> than 2.25 percentage points' rather than '2.25 or more,' which would flip th…"*

> `mimo.weakest_point`: *"Rule 4 (General QM price limit): Regulation Z §1026.43(e)(2)(vi) likely
> reads 'by more than 2.25 percentage points' (strict — excluding the boundary)…"*

`qwen.weakest_point` names the same rule for a different reason — *"the phrasing 'does not exceed …
by 2.25 or more' combines a negative condition with an inclusive threshold"*. **One verbatim check of
§1026.43(e)(2)(vi) settles rule 4 for all 13 models.**

---

## 6. Rule 5 — a slot-assignment ambiguity in the prompt, not a model divergence

GloBE de-minimis: revenue *"less than EUR 10 million"* AND income *"less than EUR 1 million"*, with
pairs `(10.0M, 0.9M)`, `(9.9M, 1.0M)`, `(9.9M, 0.9M)`. These pairs are **not ordered
below/at/above** — two fail and one qualifies, in prompt order.

Models assigned them to the three slots in two opposite orders:

| slot mapping | models | resulting row |
|---|---|---|
| prompt order (pair1→below, pair3→above) | chatgpt, deepseek, gemini, grok, mimo, minimax 2.7, minimax m3 | fail, fail, qualify |
| reversed (qualifying pair→below) | kimi, meta, mistral, qwen, yuanbao | qualify, fail, fail |
| explicit refusal to map | **glm 5.3 flash** | `below: "(9.9M, 0.9M): FIRE"`, `at: "(10.0M, 0.9M): NO FIRE on the revenue…"`, `above: "n/a — no listed pair exceeds a cap, an…"` |

**`phrase_inclusivity` is `strict` in all 13 files** — the substantive reading is unanimous. The
disagreement is entirely about which pair goes in which slot.

**Six of thirteen models identified this themselves in `weakest_point`** — deepseek (*"the provided
inputs are not a simple below/at/above series, making the assignmen…"*), grok (*"the exact pairing of
the three listed (revenue, income) combinations to the below/at/above slots"*), minimax 2.7,
minimax m3, mistral, yuanbao. **Rule 5 should be regraded on the pair-level verdicts, not the slot
labels**; the four models that inline the pair with the verdict (glm 5.3 flash, meta, mimo,
minimax 2.7) are the only ones gradable without reconstructing their mapping.

---

## 7. `weakest_point` — where each model located its own risk

All thirteen files carry it (mistral's is inside its 9th list item — §2). Every one names a specific
rule.

| Rule flagged | models |
|---|---|
| **Rule 5** (GloBE) | deepseek, grok, minimax 2.7, minimax m3, mistral*, yuanbao — 6 |
| **Rule 8** (NIS2) | gemini, glm 5.3 flash, meta — 3 |
| **Rule 4** (General QM) | kimi, mimo, qwen — 3 |
| **Rule 6** (CbCR) | chatgpt — 1 |

\* mistral's `weakest_point` value is the bare string `"Rule 5 (GloBE de-minimis)"`; its explanation
is in a sibling `reason` key (*"The phrasing of the dual conditions ('le…"*) rather than in the
`weakest_point` string itself, and the pair sits inside a 9th list item rather than a top-level
object.

**Two of these challenge the prompt's own premise rather than the model's recall** — a distinct and
more useful category:

> `chatgpt`: *"Rule 6 is the weakest point because the supplied premise says the 2026 transition rate
> is 16%, whereas current OECD material states that the Transitio…"*

> `glm 5.3 flash`: *"Rule 8: the final NIS2 Directive (EU) 2022/2555 defines 'significant incident'
> qualitatively (severe operational disruption, financial loss, or consid…"* — i.e. the prompt's
> *"framed as 'equal to or greater than' the minimum"* may not correspond to operative text at all.

`gemini` and `meta` make the same NIS2 point independently, meta adding that national transposition
varies between *"exceeds"*, *"more than"*, and *"equal to"*.

**The flags land on the two rules that actually diverged (4 and 5) plus the two whose premises are
contested (6 and 8). No model flagged rules 1, 2, 3 or 7 — the four that were unanimous.**

---

## 8. Citation posture

The prompt does not ask for citations. Four files nonetheless anchor to a named instrument, in
`reasoning` or `weakest_point`:

| model | anchor as written |
|---|---|
| mimo | *"Regulation Z §1026.43(e)(2)(vi)"* |
| glm 5.3 flash | *"the final NIS2 Directive (EU) 2022/2555"* |
| gemini | *"NIS2 primary text (Article 23)"* |
| chatgpt | a trailing link footer outside the JSON: `[1]: https://www.consumerfinance.gov/rul…` |

The remaining nine reason from the phrase quoted in the prompt itself without naming a source. **For
rules 1–3 and 6–8 that is sufficient — the prompt supplies the operative phrase — so absence of a
citation is not a gap here. It is a gap for rules 4 and 5, where the disagreement is precisely about
whether the prompt's phrase is the operative one.**

---

## 9. Consensus / outlier map

**Consensus on all six unanimous rules, with self-describing verdict tokens** (the rows that survive
normalisation unchanged): `meta`, `mimo`, `minimax 2.7`.

**Consensus on substance, bare tokens** (need a per-model map before grading): `chatgpt`, `deepseek`,
`gemini`, `glm 5.3 flash`, `grok`, `kimi`, `qwen`, `yuanbao`.

**Outliers, each with the byte-level reason:**

| model | where | what the bytes show |
|---|---|---|
| mistral | rule 4 | polarity mixed within one row (`PASS`, `PASS`, `FIRE`); 9 items for 8 rules; `rule` as string not integer; `reason` vs `reasoning` |
| minimax m3 | rule 3 | `verdicts.at` key **ABSENT**; domain-word vocabulary elsewhere (`SAFE HARBOUR`, `COMPLIANCE`) |
| chatgpt, gemini | rule 4 | the 3-model minority reading at the 2.25 boundary |
| minimax 2.7 | rule 3 vs rule 1 | opposite polarity conventions inside one file |
| yuanbao | rules 1, 2 | `FAIL` for "does not fire" — the token most likely to be misgraded |
| glm 5.3 flash | rule 5 | the only file to refuse the slot mapping and write `n/a` with a stated reason |

---

## 10. Flags for the pipeline

1. **Do not grade this family by string match.** Build a per-model token map first; `PASS` and `FAIL`
   both appear as "does not fire" and as "satisfied", in different files and in different rules of
   the same file.
2. **Three loader traps.** `deepseek` and `minimax m3` nest the rules under `"rules"` — a list-keyed
   loader reads them as empty. `mistral` types `rule` as a string, so a numeric join drops it, and
   folds its `weakest_point` into the rules list where a rule iterator will hit it.
3. **`minimax m3` rule 3 `at` is ABSENT** — 1 of 312 cells genuinely missing. Do not fill it.
4. **Regrade rule 5 on pair-level verdicts, not slot labels.** The slot ambiguity is in the prompt;
   six models said so unprompted.
5. **Three single retrievals settle everything that is actually disputed:**
   §1026.43(e)(2)(vi) verbatim (rule 4, 13 rows); the GloBE de-minimis pair semantics (rule 5, 13
   rows); whether NIS2 states a numeric users threshold at all (rule 8 premise, flagged by 3 models).
6. **`sonnet boundary.json` is ABSENT**, corroborated by `dispatch-state.json` `SKIPPED-NOTAB`.
   Record as no-data, not as a failure.
