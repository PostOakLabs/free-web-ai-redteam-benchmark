# Day 3 corpus — shared provenance note

> ## ⛔ SCOPE CORRECTION — 2026-09-08, by the session that wrote this digest
>
> **These digests cover 70 of 143 Day-3 response files, and 5 of 10 prompt families. Everything
> below about those 5 families stands and was verified; the corpus statements are wrong.**
>
> The brief that commissioned this work named five families (`aprc`, `boundary`, `power4`,
> `library`, `patterns`). Five more were already on disk, dated **2026-09-04 14:39–14:42**, a day
> before this digest ran:
>
> | family | files | prompt on disk |
> |---|---|---|
> | `alpha` | 14 (+1 misfiled, see below) | `prompts/D2-ALPHA21264-RECALL.md` |
> | `niagara` | 14 | `prompts/D2-NIAGARA-RECALL.md` |
> | `p4` | 15 | `prompts/D2-PENTIUM4-RECALL.md` |
> | `pphysical` | 14 | `prompts/D2-POWER4-PHYSICAL-RECALL.md` |
> | `lvs` | 15 | `prompts/F-LVS-MISMATCH-CLASSES.md` |
>
> **How it was missed:** `digest/_verify/load.py` printed `SKIP unrecognised family:` **73 times**.
> The output was read through `sed -n '1,60p'`, which cut the warnings. The tool reported the
> problem; the operator truncated the report. Same failure class as AINumbers SO #56, committed on
> the run that defined this corpus.
>
> **Consequences for what follows:**
> - "70 files", "5 prompt families", and the per-family counts are **scoped to the brief, not to the
>   corpus**. Read them as "the five commissioned families".
> - The staleness claim about `RUN-MANIFEST.tsv` understated the gap. The manifest has since been
>   regenerated to 444 rows, which was this digest's predicted target; the true target is
>   **444 + 73 = 517**. See the correction in `DAY3-FOLD-NORMALIZE-1.md`.
> - **`03-power4.md` has an unexamined sibling.** It flags `minimax m3` entry 0 as
>   clock-distribution content belonging to "the companion paper". That companion paper's own
>   family — `pphysical`, 14 files — was sitting in the same directory, unread.
> - **`Web Model Tasks/Day 4/yuanbao power.json` is misfiled.** Its `page_guess` values (24, 28, 30)
>   fall in Alpha 21264's 24–36 range, its content is Alpha (Ebox, clustered integer execution,
>   20-entry integer issue queue), and yuanbao is the only model with no `alpha.json`. It is
>   yuanbao's **alpha** answer under a truncated name. The alpha family is 15 models, not 14.
>
> Nothing in these six digest files was re-derived for this correction; the five families they do
> cover were verified and reproduce (see `SESSION-AUDIT-2026-09-05-to-09-08.md` §2). The remaining
> five families are **undigested**, not digested-and-clean.

Read this before any per-family digest. It records what the harness files say about how the
responses were collected, and the parse status of all 70 response files. Every claim below is
traceable to a named file; where a fact is not in the bytes, it is marked **ABSENT**, never inferred.

---

## 1. Files present

`C:\dev\Claude\Projects\ASIC\Web Model Tasks\Day 3\`

| Kind | Files |
|---|---|
| Harness | `MECHANISM-NOTES.md`, `_inject.js`, `_payload.txt`, `_payload.b64`, `dispatch-state.json` |
| Responses | 70 `.json` files — `<model> <family>.json` |

Per-family response counts: **aprc 14 · boundary 13 · power4 14 · library 15 · patterns 14.**

Sixteen distinct model labels appear across the corpus. No model has all five families:

| model | aprc | boundary | power4 | library | patterns |
|---|---|---|---|---|---|
| chatgpt · deepseek · gemini · glm 5.3 flash · grok · kimi · mimo · minimax 2.7 · minimax m3 · qwen · yuanbao | ✔ | ✔ | ✔ | ✔ | ✔ |
| meta | ✔ (see §5) | ✔ | ✔ | ✔ | ✔ |
| mistral | ✔ | ✔ | **ABSENT** | ✔ | ✔ |
| sonnet | ✔ | **ABSENT** | ✔ | ✔ | ✔ |
| longcat | **ABSENT** | **ABSENT** | ✔ | ✔ | **ABSENT** |

`sonnet boundary.json` is absent from disk, and `dispatch-state.json` independently records
`{"model": "sonnet", "status": "SKIPPED-NOTAB", "note": "no claude.ai tab in group; the operator ruled run-9-without"}`.
Those two facts are consistent. No comparable dispatch record exists for the other absences.

---

## 2. What the harness files establish — and what they do not

`MECHANISM-NOTES.md` (2,005 bytes, dated 2026-09-03, headed "first supervised run") documents five
properties of the Claude-in-Chrome MCP, not of any model:

1. The extension addresses only its own tab group; tabs outside are invisible.
2. Closing the group's blank anchor tab destroyed group `1549947802` and ejected 13 tabs.
3. `ctrl+v` cannot reach the system clipboard — the clipboard route is unusable.
4. **`type` silently no-ops on background tabs**: every keystroke action against a non-foregrounded
   tab returned success while the composer stayed empty. The note states the consequence directly:
   *"11 manifest lines would have been written against 11 empty composers. Reported-success is not
   evidence of delivery."*
5. Standing rule adopted: verify the composer's actual text before every send.

The adopted method is a `javascript_tool` DOM write with pre-send verification. `dispatch-state.json`
carries that verification per model as `verified_composer_len` (2,131–2,153) and
`verified_occurrences: 1`.

**Scope limit that matters for the pipeline.** `dispatch-state.json` has
`"prompt_id": "C1-BOUNDARY-VERDICTS"` and describes **one run on one family**. It records six models
as `DISPATCHED` (meta, grok, yuanbao, kimi, qwen, deepseek), five as `PENDING`
(chatgpt, gemini, mistral, minimax 2.7, minimax-m3), and three as skipped (sonnet, glm 5.3 flash,
mimo). Yet **13 `* boundary.json` files exist on disk, including files for four of the five PENDING
models and for two of the three SKIPPED models** (`glm 5.3 flash boundary.json`,
`mimo boundary.json`). The state file therefore does **not** account for the collection route of
most boundary responses, and accounts for none of the other four families at all. **Treat
`dispatch-state.json` as a partial log of one family's browser run, not as corpus provenance.** For
70 files, delivery evidence exists for 6.

Two guardrail notes in that file are worth carrying forward because they are contradicted by the
files on disk: glm 5.3 flash is recorded `SKIPPED-SUSPENDED` and mimo `SKIPPED-DROPPED`, with
*"guardrail forbids dispatch"* — and both have complete response files for all five families
(glm 5.3 flash: 5 of 5; mimo: 5 of 5). Whatever route produced them was outside the logged run.

`_payload.txt` (2,156 bytes) and `_payload.b64` (2,876 bytes) hold the same content; the base64
decodes to the plain text. That content is the **boundary** prompt only.

---

## 3. Prompt binding — which prompt each family answers

`_payload.txt` binds `boundary` directly (verbatim match). The other four are bound by matching the
response field-set to a prompt file in `..\..\prompts\`; each binding is stated with its evidence and
none is assumed.

| Family | Prompt file | Binding evidence |
|---|---|---|
| `boundary` | `prompts/C1-BOUNDARY-VERDICTS.md` | `_payload.txt` is this task verbatim; `dispatch-state.json` `prompt_id: C1-BOUNDARY-VERDICTS` |
| `aprc` | `prompts/C1-CCD2-APRC.md` | responses carry exactly `case`, `assumptions_invoked`, `equation`, `iterations`, `aprc_pct` — the prompt's output schema — and four cases matching its four scenarios |
| `power4` | `prompts/D2-POWER4-RECALL.md` (microarchitecture, pp. 5–25) | 13 of 14 files carry the full D2-v5 field set; **every numeric `page_guess` in the corpus falls in 5–21**, inside the 5–25 range this prompt specifies and outside the 27–52 range of the companion physical-design prompt. See the one content exception in the power4 digest §6 |
| `library` | `prompts/F-DIAGNOSIS-LIBRARY.md` | all 15 files carry `symptom`/`first_checks`/`discriminating_experiments`/`common_root_causes`/`classic_trap`/`node_era_note`, and 13 of 15 emit exactly the prompt's 10 canonical symptoms |
| `patterns` | `prompts/G-SDC-PATTERNS.md` | responses carry `pattern_name`/`situation`/`derivation`/`wrong_way`/`defense`/`signoff_risk`/`provenance`/`recall_confidence`/`node_era_note` |

---

## 4. Parse status — all 70 files

**One file will not parse. Three parse only under element-wise recovery. Sixty-six parse.**

| File | Status | Detail |
|---|---|---|
| `minimax m3 patterns.json` | **WILL NOT PARSE** | `json.loads`: *Expecting ':' delimiter* at char 2161 (line 9, col 49). Not truncation — a **mid-string splice** at char 2051: `…at system integration the path fails` runs straight into `ew/jitter/OCV) ≈ 10–15% of T (confidence 0.5)",`. A string literal is cut mid-word and content from a later array element is joined to it. The file's last non-space character is `]`, so the outer array is closed; an object-boundary scan finds **8 complete top-level objects** after the seam, but the first element is destroyed. **Flagged for re-collection, not repair.** |
| `minimax m3 aprc.json` | element-wise recovery | 1 of 4 cases recovered |
| `minimax m3 library.json` | element-wise recovery | 5 of 10 symptoms recovered |
| `longcat library.json` | element-wise recovery | 4 of 10 symptoms recovered |
| `minimax m3 boundary.json` | recovered | a `"key": "value"` pair sitting inside an array; 8 rules recovered |
| 20 files | fence-wrapped | content preceded by ` ```json ` and/or followed by ` ``` ` — parses after fence strip |
| 44 files | clean | — |

Three files carry content **outside** the JSON value:

- `chatgpt boundary.json` — trailing `[1]: https://www.consumerfinance.gov/rul…` (a reference-link footer).
- `mimo aprc.json` — **leading prose** (`"Looking at each case, I need to set up the CCD Annex I present-value equation…"`, ~300 chars of worked summary) and a **second fenced block** after the array containing `{"weakest_point": …}`. The weakest_point is present in the file's bytes but is **not inside the parsed JSON value**; a naive parser reports it ABSENT.
- `meta aprc.json` — trailing `[2]`.

---

## 5. Corpus-integrity finding: `meta aprc.json` is a duplicate of a Day 2 file

`Day 3\meta aprc.json` is **byte-identical** to `Day 2\meta receipt.json`:

```
Day 3 'meta aprc.json'    : 23,651 chars, opens {"receipt_kinds": [{"kind": "Composite / Segment Receipt", …
Day 2 'meta receipt.json' : 23,651 chars, opens {"receipt_kinds": [{"kind": "Composite / Segment Receipt", …
byte-identical: True        both end: 'tion docs."\n  }\n}[2]'
```

Its top-level keys are `binding_chain`, `certainty_notes`, `claim_structure`, `common_verifier_bugs`,
`groth16_receipt_fields`, `receipt_kinds`, `version_coupling` — the risc0 receipt-anatomy schema. It
contains **zero APRC content**: no `case`, no `equation`, no `aprc_pct`.

This is a file-placement defect in the collection step, not a model output about APRC. **meta has no
APRC response in this corpus.** Every APRC statistic in the aprc digest uses n = 13, not 14.

---

## 6. Cross-family field contamination

Two library files carry fields belonging to the POWER4-recall schema. This is byte-verifiable and
affects schema validation downstream:

| File | Contaminating fields | Extent |
|---|---|---|
| `mimo library.json` | `not_in_paper`, `paper_vs_general`, `weakest_point` | **10 of 10 items**; every `paper_vs_general` value is the literal POWER4 enum string `"from-general-POWER4-knowledge-not-necessarily-this-paper"` (first at char 3,840) |
| `glm 5.3 flash library.json` | `not_in_paper` | **10 of 10 items**, all `false` (first at char 3,741) |

Neither field appears in `F-DIAGNOSIS-LIBRARY.md`. The required library fields are present in both
files as well — this is addition, not substitution.

---

## 7. Reading order

`01-aprc.md` · `02-boundary.md` · `03-power4.md` · `04-library.md` · `05-patterns.md`

Each digest states the family's schema, its agreement/divergence map on the load-bearing cells, the
citation-versus-assertion posture with byte evidence, and a consensus/outlier map. **No digest
renders a verdict on whether any model is correct.** Where a divergence reduces to a single decidable
question, that question is stated so a verifier can settle it once and grade many models at a time.
