# Digest — family `aprc`

**Prompt:** `..\..\prompts\C1-CCD2-APRC.md` — APRC computation under the EU Consumer Credit
Directive assumptions, four scenarios, bare JSON.
**Files:** 14 on disk. **Usable: 13.** See §1.
**Nature of the family:** every load-bearing cell is a number produced by a stated equation, so
divergences reduce to identifiable modelling choices rather than to opinion. This is the most
mechanically gradable family in the Day 3 corpus.

---

## 1. Files and parse status

| Model | Parse | Cases recovered | Note |
|---|---|---|---|
| chatgpt, deepseek, gemini, glm 5.3 flash, grok, minimax 2.7, qwen, yuanbao | clean | 4 | |
| kimi, mistral, sonnet | clean after fence strip | 4 | sonnet's list has 6 elements: 4 case objects, then a standalone `{"financed_vs_cash_fee_note": …}` and a standalone `{"weakest_point": …}` |
| mimo | clean array; prose outside | 4 | see §5 |
| minimax m3 | **element-wise recovery** | **1 of 4** | cases 2–4 unrecoverable |
| **meta** | parses, but **wrong content** | **0** | byte-identical to `Day 2\meta receipt.json` — see `00-corpus-and-harness.md` §5 |

**All statistics below use n = 13 (meta excluded), and n = 12 for cases 2–4 (minimax m3 also
excluded).** meta's row is reported as ROW ABSENT throughout, never as a value.

---

## 2. Schema

Prompt's specified item schema: `{"case", "assumptions_invoked", "equation", "iterations", "aprc_pct"}`
plus a trailing `{"weakest_point"}`.

| Field | Present | ABSENT in |
|---|---|---|
| `case` | 13/13 | meta (no APRC content) |
| `assumptions_invoked` | 13/13 | meta |
| `equation` | 13/13 | meta |
| `iterations` | 13/13 | meta |
| `aprc_pct` | 13/13 | meta |
| `weakest_point` (top level) | **8/13** | deepseek, meta, mimo¹, minimax 2.7, minimax m3 |

¹ mimo's `weakest_point` **is present in the file's bytes** — in a second fenced block after the
array, ending `"…the single assumption most likely to diverge across member-state implementations."`
— but it is outside the parsed JSON value. Downstream schema validation will report it ABSENT unless
the loader reads trailing fences.

Two models added an unrequested field for the case-4 question: `sonnet.financed_vs_cash_fee_note`
and `yuanbao.financed_fee_note`. No other model emitted a dedicated field for it. See §4.

---

## 3. Load-bearing cell: `aprc_pct`

| model | case 1 | case 2 | case 3 | case 4 |
|---|---|---|---|---|
| chatgpt | 8.8 | **39.4** | 19.6 | 12.3 |
| deepseek | 8.9 | 24.4 | 19.6 | 8.0 |
| gemini | 7.7 | 22.6 | 19.6 | 12.3 |
| glm 5.3 flash | 8.8 | 24.4 | 19.6 | 8.0 |
| grok | 8.0 | 28.0 | 21.8 | 12.0 |
| kimi | 8.8 | 24.4 | 19.6 | 12.3 |
| mimo | 8.8 | 24.3 | 19.6 | 12.3 |
| minimax 2.7 | 6.5 | 32.7 | 18.0 | 7.7 |
| minimax m3 | 6.1 | ROW ABSENT | ROW ABSENT | ROW ABSENT |
| mistral | 6.7 | 24.0 | 18.0 | 8.0 |
| qwen | 8.8 | 24.4 | 19.6 | 12.3 |
| sonnet | 8.8 | 24.3 | 19.6 | 12.3 |
| yuanbao | 8.8 | 24.0 | 19.6 | 8.0 |
| **meta** | ROW ABSENT | ROW ABSENT | ROW ABSENT | ROW ABSENT |

| case | n | modal value | modal count | spread |
|---|---|---|---|---|
| 1 | 13 | **8.8** | 7 | 6.1 – 8.9 |
| 2 | 12 | **24.4** | 4 (24.3 ×2, 24.0 ×2 adjacent → 8 within 24.0–24.4) | 22.6 – 39.4 |
| 3 | 12 | **19.6** | 9 | 18.0 – 21.8 |
| 4 | 12 | **12.3** / **8.0** — bimodal | 6 / 4 | 7.7 – 12.3 |

---

## 4. Case 4 — the cleanest divergence in the corpus: one term, two camps

Case 4 is not noisy; it is a **binary modelling choice on the left-hand side of an otherwise
identical equation.** Ten of twelve models write the same right-hand side, `5616 = (5000 + 200) ×
1.08`, discounted one year. They differ only in what stands on the left.

**Camp A — LHS = 5000 (the cash the consumer receives) → 12.3%**
`chatgpt`, `gemini`, `kimi`, `mimo`, `qwen`, `sonnet` (6)

```
chatgpt.equation : "5000 = 5616/(1+X), where 5616 = 5200*1.08 = (5000+200)*1.08"
sonnet.equation  : "5000 = [(5000+200)*1.08] * (1+X)^-1 = 5616*(1+X)^-1"
qwen.equation    : "5000 = ((5000 + 200) * 1.08) / (1+X) = 5616/(1+X)"
```

**Camp B — LHS = 5200 (the balance created) → 8.0%**
`deepseek`, `glm 5.3 flash`, `mistral`, `yuanbao` (4)

```
deepseek.equation : "5200 = 5616 / (1+X)"
yuanbao.equation  : "5200(1+X)^0 = 5616(1+X)^(-1)"
```

**Two models sit outside both camps, each for a stated reason visible in `equation`:**

- `grok` → 12.0. LHS 5000 (camp A), but RHS `(5200 + 400)` — interest computed on 5,000, not on the
  5,200 balance. Its own note reads *"financed fee increases the repayment obligation; net amount
  received by consumer is still 5000"*.
- `minimax 2.7` → 7.7. LHS 5200 (camp B), but solves monthly and converts by
  `APRC = 12 * i_monthly` — a nominal conversion rather than the annual effective rate the other
  eleven report.

**The decidable question.** The whole 4.3-point spread reduces to: *when a broker fee is financed
into the balance at t=0, is the drawdown term the €5,000 advanced or the €5,200 principal created?*
The prompt asked for exactly this (*"state how the financed fee enters the equation differently than
a t=0 cash fee"*), and **only three of twelve models answered it explicitly**: sonnet and yuanbao in
dedicated fields, mimo inline in `equation` (*"Cash-fee alternative for comparison: 5000 = 200 +
5400·(1+X)^(-1)"*). yuanbao's note states the mechanism directly:

> `yuanbao.financed_fee_note`: *"A t=0 cash fee reduces the net amount made available to the consumer
> (net drawdown = principal − fee), leaving the repayment stream unchanged - it raises the APRC
> because the consumer receiv…"*

One retrieval against Annex I settles all twelve rows.

---

## 5. Case 2 — identical equations, three different answers

Nine models write the same present-value equation:

```
3000 = 55/(1+X)^(1/12) + 55/(1+X)^(2/12) + 3055/(1+X)^(3/12)
        where 55 = 3000×0.01 + 25   and   3055 = 3000 + 30 + 25
```

Reported results from that identical equation: **24.4** (deepseek, glm 5.3 flash, kimi, qwen),
**24.3** (mimo, sonnet), **24.0** (mistral, yuanbao), **22.6** (`gemini`), **28.0** (`grok`).

gemini's `equation` string is character-for-character the same shape as the 24.4 group's
(`3000 = 55*(1+X)^(-1/12) + 55*(1+X)^(-2/12) + 3055*(1+X)^(-3/12)`) yet its `aprc_pct` is 22.6;
grok's final term is likewise `(3000 + 3000*0.01 + 25)` = 3055 yet its `aprc_pct` is 28.0. **In both
files the stated equation and the stated answer are separable artifacts — a solver can re-run the
equation and compare, without needing the Directive.**

`chatgpt` diverges in the equation itself, not the solve:

```
chatgpt.equation : "3000 = 55/(1+X)^(1/12) + 55/(1+X)^(2/12) + 3090/(1+X)^(3/12)"
                                                                ^^^^ 3090, not 3055
```

3090 = 3000 + 90, i.e. three months of interest loaded into the final payment while two months of
interest are also carried in the two €55 instalments. Its `aprc_pct` of **39.4** is the corpus
maximum and follows from that term. `minimax 2.7` (32.7) uses an annuity form
`3000 = 1055 * a(3|i)` and again converts by `APRC = 12 * i_monthly`.

---

## 6. Citation posture — what is grounded and what is asserted

The prompt asks for `assumptions_invoked`, not citations. Models split on whether they name a
provision. **Article/Annex citations appear in `assumptions_invoked` strings, and are the checkable
part of this family beyond the arithmetic.**

**Models citing a specific provision (quoted from their own bytes):**

| model | citation as written |
|---|---|
| deepseek | *"per Directive 2008/48/EC Annex I Part II point (c)"* (case 4); *"Annex I Part II point (d)"* (case 2) |
| glm 5.3 flash | *"Part II(a)/(f)(i) logic"* (case 4); *"Annex I/III Part II(d)"* (case 2) |
| grok | *"Part II (a): total amount of credit deemed drawn down immediately and in full"* |
| kimi | *"Article 19(3)"*; *"Assumption (a) Annex I Part II"*; *"Assumption (d) Annex I Part II"* |
| mimo | *"Annex I Part 2 §1"* |
| minimax 2.7 | *"EU CCD Art. 6.2"* (cases 2 and 4) |
| gemini | *"Article 17 / Annex I assumption"* |
| yuanbao | *"Annex I Part II assumption (a)"* |

**Models stating assumptions without a provision reference:** `chatgpt`, `mistral`, `sonnet`, `qwen`
(qwen names the mechanism — *"under the additional assumption the full EUR 5000 is deemed drawn
immediately at t=0"* — without an article number).

`mistral` is the shortest in the family (1,867 chars) and its case-4 `assumptions_invoked` is four
bare clauses: `['Full €5,000 drawn at t=0', 'Single repayment at 12 months', '8% nominal rate',
'€200 fee financed at t=0']` — no provision, no derivation.

**Note for the verifier: the citations disagree with each other.** For the same case-2 overdraft
assumption, deepseek cites Annex I Part II **point (d)**, kimi cites **assumptions (a) and (d)**,
minimax 2.7 cites **Article 6.2**, gemini cites **Article 17**. These are different provisions
asserted for the same assumption. Two of them at most can be the operative one. **No claim in this
digest resolves which — this is the retrieval the family needs.**

---

## 7. Consensus / outlier map

**Consensus core (all four cases within one modal cluster, equation and answer consistent):**
`kimi`, `qwen`, `sonnet`, `mimo` — 8.8 / 24.3–24.4 / 19.6 / 12.3.
`deepseek`, `glm 5.3 flash`, `yuanbao` match on cases 1–3 and sit in camp B on case 4.

**Outliers, each with the byte-level reason:**

| model | outlier cell | visible cause |
|---|---|---|
| chatgpt | case 2 = 39.4 (max) | `3090` in the final term where nine models write `3055` |
| minimax 2.7 | cases 1,2,4 all low/high extremes | `APRC = 12 * i_monthly` nominal conversion throughout |
| gemini | case 1 = 7.7, case 2 = 22.6 | equation matches the modal group; answer does not |
| grok | case 2 = 28.0, case 3 = 21.8 | equation matches the modal group; answer does not |
| mistral | cases 1 = 6.7, 3 = 18.0 | shortest file in family; no `iterations` detail to locate the divergence |
| minimax m3 | case 1 = 6.1 (min) | only 1 of 4 cases survives parsing; single-point evidence |

**Not scored:** `meta` (wrong-content file, §1).

---

## 8. Flags for the pipeline

1. **`meta aprc.json` must not enter the APRC pipeline.** It is a Day 2 receipt-anatomy file.
   Re-collect or record meta as no-data for this family.
2. **`mimo aprc.json` needs a loader that reads trailing fenced blocks**, or its `weakest_point` is
   lost. The field is in the bytes.
3. **`minimax m3 aprc.json` yields one case.** Report as 1-of-4, never as a complete row.
4. **Two decidable retrievals gate the whole family**: (a) the financed-fee drawdown term (§4),
   (b) which provision governs the overdraft duration assumption (§6). Both are single lookups that
   grade twelve rows at once.
5. **The `equation` and `aprc_pct` fields are independently checkable.** Four models (gemini, grok,
   and to a lesser degree mistral and minimax 2.7) show a gap between the two. A re-solver run over
   the `equation` strings alone will separate "wrong model" from "wrong arithmetic" without any
   regulatory text.
