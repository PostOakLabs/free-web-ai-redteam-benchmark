# Digest — family `alpha`

**Prompt:** `prompts/D2-ALPHA21264-RECALL.md` — Kessler, *The Alpha 21264 Microprocessor*,
IEEE Micro 19(2):24–36, 1999.
**Ground truth:** `sources/Alpha21264-pagemarked.txt`. **15 files, 70 entries, 15 of 15 parse.**
As-of 2026-09-09T01:41:45Z.

## Model set — 15, and the 15th is misfiled

chatgpt · deepseek · gemini · glm 5.3 flash · grok · kimi · longcat · meta · mimo · minimax 2.7 ·
minimax m3 · mistral · qwen · sonnet · **yuanbao (as `yuanbao power.json`)**.

yuanbao is not missing. Its answer arrived under a truncated filename and is digested here with
provenance intact and the file unrenamed (`00-corpus-and-harness.md` §2).

`minimax m3 alpha.json` recovered **4 of ~5** entries by forward harvest after a delimiter break at
char 2863; element 0 destroyed, later elements intact. Recorded, not repaired.

## Quote grading

| tier | count |
|---|---|
| T1 verbatim (incl. hyphen-variant) | **17** |
| T2 paraphrase-consistent | 3 |
| T3 contradicts-paper | **0** |
| T4 not-found | **0** |
| T0 declined | 50 |
| entries | 70 |

**Alpha is the cleanest family in Day 4.** Of 20 quotes actually asserted, 17 are verbatim, 3 are
paraphrase-consistent, and **not one is fabricated or contradicted**.

Four models assert; eleven decline on every entry.

| model | verbatim | paraphrase | page guesses within ±2 |
|---|---|---|---|
| grok | 5/5 | 0 | **5/5** |
| meta | 5/5 | 0 | **5/5** |
| kimi | 4/5 | 1 | **5/5** |
| chatgpt | 3/5 | 2 | **5/5** |
| 11 others | — | — | declined |

Page guesses are journal pages; the offset (PDF = journal − 23) comes from the extraction file's own
`_locator_note`. All four asserting models locate every episode to within two pages.

## Convergent numerics, checked against the paper

| claim | models | verdict |
|---|---|---|
| 64 kb | 5/15 | IN-PAPER (4 hits) |
| 600 mhz | 5/15 | IN-PAPER (4 hits) |
| 80 entries | 3/15 | IN-PAPER — paper writes `80-entry register file` |

Zero unsupported convergent claims. The third was a **false NOT-FOUND on the first pass** because
the matcher required the plural; see `00-corpus-and-harness.md` §5.

## The corrected-sentence cross-check

This family is where memorial-3's two corrections live. Neither pre-correction value appears
anywhere in these 15 files; meta recalls `90% to 100%` and chatgpt and meta recall `85% to 100%`,
both matching the paper. Detail and the honest limits: `06-crosscheck.md` §1.

## Honesty fields

`not_in_paper` is **false in all 70 entries** — the escape was never used in this family.
`paper_vs_general`: 38 `confident-this-is-in-the-paper`, 24 `probably-in-the-paper`, 8
`from-general-Alpha-knowledge-not-necessarily-this-paper`. Confidence spans 0.25–0.99, mean 0.729.

**Confidence does not separate the quoters from the decliners**, and the 8 general-knowledge labels
are the honest ones — they mark claims the model is not attributing to the paper at all.
