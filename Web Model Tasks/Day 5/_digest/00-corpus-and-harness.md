# Day 5 corpus — census, gates, and parse

**80 of 80 responses across 5 families and 16 models; 0 skipped. 1 stray excluded and left
untouched.**

```
ls "Web Model Tasks/Day 5"/*.json > census.txt   ->  80        as-of 2026-09-09T14:11:04Z
python digest/_verify/d5load.py                  ->  exit 0
G1 CENSUS ASSERT: census=80 loaded=80 skipped=0 halted=0 models=16  -> PASS
```

Commissioned by `digest/DIGEST-COMMISSION-DAY5-1.md` (2026-09-09).

---

## 1. Gate results

| gate | result |
|---|---|
| **G1** census | **PASS** — 80/80/0/0, 16 models. Unknown family *or unknown model* exits 3; the loader cannot skip |
| **G2** no verdict through a pipe | **HELD** — every verdict in these documents was read from `_verify/d5run/*.txt` |
| **G3** tooling first | **PASS** — `MANIFEST-D5.sha256` regenerated before every run, so the hash always matches the bytes that produced the digest |
| **G4** determinism | **PASS** — two full clean chain runs, all 6 derived JSONs byte-identical (`d5corpus b6430c7f`, `d5regz 06a3c1b4`, `d5strings df152546`, `d5e df0e7761`, `d5redteam ff646c6a`, `d5permodel 27cc86b2`) |
| **G5** vet recipe last | see `07-vet-recipe.md`, written after every other file, values re-derived in-session |

**Document numbers are unique** (`00`–`07`). Day 4 shipped two files numbered `06`; not repeated.

**Q-names, not T-names.** All tiered output here uses `Q1`/`Q2`/… The Day-4 `T0–T4` quote tiers
collided with the harvest rubric's T1/T2/T3 (keeper/salvage/discard) and with survey triage.

## 2. Families and tracks

| family | files | prompt | track | ground truth |
|---|---|---|---|---|
| `regz` | 16 | `C1-REGZ-FACTOR.md` | **A** | exact arithmetic, recomputed here |
| `strings` | 16 | `C2-JCS-STRINGS.md` | **B** | `digest/_verify/jcs.py`, 12/12 RFC 8785 self-asserts |
| `e` | 16 | `PROMPT-E-CALCULATIONS.md` | **C** | `digest/hw-calc-formulas.md` consensus merge |
| `red1` | 16 | `J-ISSUE-REDTEAM-V1.md` | **D** | calibration wave, RUNSHEET-34 Block 01 |
| `red3` | 16 | `J-EPISODE-REDTEAM-V3.md` | **D** | calibration wave, RUNSHEET-42 Block 08 |

Three of five tracks have deterministic ground truth. Track A has **no tunable at all**.

### The dual-spelled model

`minara` (e, red1, regz) and `minaria` (red3, strings) are **one model collected under two
spellings** — the `yuanbao power.json` class of collection defect. Merged to the key `minara`,
with `spelling_as_collected` preserved on every record. **Files were not renamed.** The operator confirms
the canonical name at checkoff.

Without the merge the corpus reads as 17 models with two 3-file and 2-file ghosts.

### The stray

`draft 3 and 4 prompt.md` (Hy4 seal-retest dispatch drafts) is **not Day-5 content**. Excluded from
the census by extension, **left in place untouched**, flagged for relocation.

## 3. Parse results

| class | files |
|---|---|
| `clean` | 44 |
| `clean+fence-close+fenced` | 15 |
| `clean+trailing-content` | 10 |
| `clean+fenced+trailing-content` | 3 |
| `structural-quote-repair` | 2 |
| `raw-newline-escape` | 2 |
| `elementwise-truncation` | 2 |
| `harvest-skip-broken-element` | 1 |
| **`FAILED`** | **1** |

**A labelling fix made during this run.** `raw_decode` starts at the first bracket, so a file
wrapped in a ```` ```json ```` fence would otherwise be reported `clean`. The loader now says what was
actually outside the parsed value — hence the `clean+fenced` and `clean+trailing-content` classes.
28 files carry something outside the JSON; none of it was silently absorbed.

### The three commission-predicted failures — all salvaged

`chatgpt red1`, `chatgpt red3` and `solar red3` were flagged going in. All three now parse:

- **`chatgpt red1` / `chatgpt red3`** — the Day-2 chatgpt-jcs class: a value string embeds prose
  containing unescaped double quotes, on a document that is effectively one long line, so the
  existing line-wise repair could not reach it. A new **key/value-aware structural repair** was
  added: a quote inside a string closes it only when the next non-space character is `,` `}` `]`
  EOF, **or `:` and the string is in key position**. A value-position `":` is content — a colon
  inside prose — which is exactly `chatgpt red3`'s break at `… simply \"low ILP": Table 1 shows …`.
  Both recover their full review objects (S-W-RES with 4 and 7 objections).
- **`solar red3`** — element-wise recovery, 3 objects.

### The one unrecoverable file, and it is not a parse defect

**`solar regz.json` is prose, not JSON.** It opens *"Here is the answer in English, with each task
shown step by step."* and answers in markdown tables. There is no JSON to salvage. Recorded
`PROSE-NOT-JSON` and excluded from Track A denominators (15 of 16 gradable). Its content was not
transcribed into a score.

## 4. Findings about the instruments, not the models

Four defects were found in this session's own tooling or in the prompts, each caught before it
reached a published number.

| defect | false result it would have produced | disposition |
|---|---|---|
| **Verdict prefix collision** — `"SOUND-WITH-RESERVATIONS".startswith("SOUND")` matched first | **every reserved verdict collapsed to SOUND**, inventing a corpus-wide bare-SOUND miscalibration. The first Track-D table showed 15/16 "SOUND" on red1; the true figure is 15/16 **S-W-RES** | longest-enum-first matching |
| **`C2-JCS-STRINGS` case 5 is malformed** — embeds a raw U+0007 (BEL), illegal in JSON | 15 models scored wrong on a case whose input never reached them | case 5 **UNGRADABLE**, see `03-strings.md` |
| **case-5 sub-score compared unlike things** | reported "0 of 15" correct on the surviving prefix | fixed; true figure **14 of 15** |
| **`strings` wrapper + non-case salvage** | deepseek scored NOT GRADABLE while holding a valid `{"cases": […]}` wrapper | unwrap; chatgpt's harvest output correctly rejected as non-case-shaped |

## 5. Documents

| file | contents |
|---|---|
| `00-corpus-and-harness.md` | this note |
| `01-regz.md` | Track A — exact recomputation |
| `02-e.md` | Track C — HW-safety calculations |
| `03-strings.md` | Track B — JCS conformance |
| `04-redteam-calibration.md` | Track D — calibration wave + cross-model matrix |
| `05-decline-and-coverage.md` | decline table, model-set completeness |
| `06-crossmodel-calibration.md` | the per-model feed and how to consume it |
| `07-vet-recipe.md` | written last, in-session values |
