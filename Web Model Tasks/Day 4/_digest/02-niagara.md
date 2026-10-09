# Digest — family `niagara`

**Prompt:** `prompts/D2-NIAGARA-RECALL.md` — Kongetira, Aingaran, Olukotun, *Niagara: A 32-Way
Multithreaded SPARC Processor*, IEEE Micro 25(2):21–29, 2005.
**Ground truth:** `sources/Niagara-pagemarked.txt`. **14 files, 69 entries, 14 of 14 parse clean.**
As-of 2026-09-09T01:41:45Z.

## Model set — 14

chatgpt · deepseek · gemini · glm 5.3 flash · grok · kimi · meta · mimo · minimax 2.7 · mistral ·
qwen · **solar** · sonnet · yuanbao.

**longcat and minimax m3 are ABSENT** from this family — recorded, not absorbed. solar appears here
and in `pphysical` but in no other Day-4 family.

## Quote grading

| tier | count |
|---|---|
| T1 verbatim | **10** |
| T2 paraphrase-consistent | 4 |
| T3 contradicts-paper | 0 |
| **T4 not-found** | **5** |
| T0 declined | 50 |
| entries | 69 |

| model | result |
|---|---|
| chatgpt | 5/5 verbatim, 5/5 page guesses within ±2 |
| grok | 5/5 verbatim, 5/5 page guesses within ±2 |
| glm 5.3 flash | 0 verbatim, 2 paraphrase, **3 T4** |
| deepseek | 0 verbatim, 2 paraphrase, **2 T4** |
| 10 others | declined every entry |

Page guesses are journal pages; offset PDF = journal − 20, from the extraction file's own
`_locator_note`.

## Convergent numerics, checked against the paper

| claim | models | verdict |
|---|---|---|
| 32 threads | **9/14** | IN-PAPER (5 hits) |
| 4 threads | 3/14 | IN-PAPER — paper writes `four threads`, spelled out |
| 16 kb · 8 kb · 3 mb | 3/14 each | IN-PAPER (1 hit each) |

Zero unsupported. The 32-thread claim is the strongest convergence in Day 4 and the paper states it
plainly. `4 threads` was a **false NOT-FOUND on the first pass** — the matcher tried only the
numeral form.

## Honesty fields

`not_in_paper` false in all 69. `paper_vs_general`: 44 confident, 20 probably, 5
general-knowledge. Confidence 0.25–0.98, mean **0.748** — the second-highest mean in Day 4, in a
family carrying 5 fabricated quotes. **Confidence does not track correctness here.**
