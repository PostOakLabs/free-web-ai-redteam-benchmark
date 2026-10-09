# Day 4 corpus — provenance, gates, and coverage

**73 of 73 files across 5 families; 0 skipped.**

```
ls "Web Model Tasks/Day 4"/*.json > census.txt   ->  73          as-of 2026-09-09T01:41:45Z
python digest/_verify/d4load.py                  ->  exit 0
G1 CENSUS ASSERT: census=73 loaded=73 skipped=0 halted=0  -> PASS
```

No exclusions. Every file is digested; two carry parse anomalies recorded in §3 and neither is
silently dropped. Commissioned by `digest/DIGEST-COMMISSION-DAY4-1.md` (2026-09-08) with its
same-day addendum.

---

## 1. Gate results

| gate | requirement | result |
|---|---|---|
| **G1** census | `loaded + skipped == 73`, `skipped == 0`, unknown family halts | **PASS** — 73/73/0/0. The loader's default is inverted from Day 3's: an unrecognised family raises `SystemExit(3)`, it cannot skip |
| **G2** no verdict through a pipe | full output to file, status `grep -c`'d from the file, `$?` captured before any filter | **HELD** — every verdict in this digest was read from `_verify/d4run/*.txt`; no `head`/`tail`/`sed -n` sits between a command and a recorded result |
| **G3** tooling preserved first | `d4*.py` + `MANIFEST.sha256` generated **before** the run | **PASS** — `digest/_verify/MANIFEST-D4.sha256`, regenerated on each tool change so the hash always matches the bytes that produced this digest |
| **G4** determinism | derived JSONs regenerate byte-identically | **PASS** — full chain re-run, all 3 identical: `d4corpus.json` `83b177f9…`, `d4grades.json` `9d662355…`, `d4permodel.json` `403c020a…` |
| **G5** vet recipe last | written after all moves, every value produced in-session, as-of stamped | see `06-vet-recipe.md`, written last |

## 2. Families, prompts, ground truth

| family | files | prompt | ground truth |
|---|---|---|---|
| `alpha` | **15** | `prompts/D2-ALPHA21264-RECALL.md` | `sources/Alpha21264-pagemarked.txt` |
| `niagara` | 14 | `prompts/D2-NIAGARA-RECALL.md` | `sources/Niagara-pagemarked.txt` |
| `p4` | 15 | `prompts/D2-PENTIUM4-RECALL.md` | `sources/Pentium4-pagemarked.txt` |
| `pphysical` | 14 | `prompts/D2-POWER4-PHYSICAL-RECALL.md` | `sources/POWER4-cpd-pagemarked.txt` |
| `lvs` | 15 | `prompts/F-LVS-MISMATCH-CLASSES.md` | **none — no paper.** Graded on schema and convergence only, and this digest says so rather than implying otherwise |

**This is the asymmetry the commission named (§2.1).** Four of five families have local ground truth,
so recall claims are *graded*, not parked. `NEEDS-RETRIEVAL` appears nowhere in the four paper
families.

### `alpha` is 15 files, and the 15th is misfiled

`Web Model Tasks/Day 4/yuanbao power.json` is yuanbao's Alpha 21264 answer under a truncated
filename. It is digested **as `alpha`**, and it was **not renamed** — the as-collected name is the
evidence of the collection defect (commission §2.5). The loader carries the provenance on the record
itself:

```
family_as_collected : "power"
family              : "alpha"
misfile_provenance  : "yuanbao's Alpha 21264 answer under a truncated filename; page_guess values
                       fall in Alpha's 24-36 journal range and content is Alpha (Ebox, clustered
                       integer execution, integer issue queue). File NOT renamed…"
```

Without it, yuanbao reads as a non-responder on `alpha` and a phantom `power` family appears.
**Model-set completeness is recorded, never absorbed:** yuanbao answered; the collection step
mislabelled it.

## 3. Parse results — 73 files, 71 clean

| file | class | detail |
|---|---|---|
| 71 files | `clean` | — |
| `minimax m3 alpha.json` | `harvest-skip-broken-element` | 4 of ~5 entries recovered. Delimiter break at char 2863; element 0 destroyed, later elements intact |
| **`glm 5.3 flash p4.json`** | **`FAILED`** | **0 entries. Not repaired.** |

### The one unrecoverable file

`glm 5.3 flash p4.json` (1,934 chars) carries **dropped closing quotes** at four sites, not a stray
control character as the raw parser error suggests — the parser reaches a newline because the string
was never closed:

```
L7:  …scale frequency with the process technology of the time (0.18µm, later 0.13µm).
L12: "decision": " object fields
L13: …highest frequency, with 20-stage pipeline, double-pbroken ALUs basic as
L14: "decision": " began
```

`double-pbroken` and `" object fields` are spliced fragments; content is corrupt, not merely
truncated. Both recovery strategies return 0. **Recorded FAILED and excluded from `p4` denominators
(14 of 15 assessable). No content was reconstructed.**

### A recovery-ordering defect found in this session's own loader

The first build tried element-wise recovery, returned on its first success, and reported
`minimax m3 alpha.json` at **2** entries. The forward harvest recovers **4** — element-wise stops at
the first broken element while harvest skips it. The loader now runs **both** and keeps whichever
recovers more, recording the comparison on the record:

```
"recovery_compare": {"elementwise": 2, "harvest": 4}
```

Ordering, not capability, was costing two entries per affected file. `MANIFEST-D4.sha256` was
regenerated after the fix, before the run that produced this digest.

## 4. Grading method

Four tiers against the normalised paper text (commission §2.2, addendum: verified estate policy):

| tier | meaning |
|---|---|
| **T1 verbatim** | normalised quote is a substring of the normalised source |
| **T1 hyphen-variant** | matches only after in-word hyphens are removed — counted separately so the true byte-verbatim figure stays honest |
| **T2 paraphrase-consistent** | ≥0.60 content-word overlap with a located source window |
| **T3 contradicts-paper** | located, but a numeric token disagrees — **CANDIDATE only, hand-confirmed before reporting** |
| **T4 not-found** | no window clears the floor after normalisation |
| **T0** | declined (`cannot-reproduce-verbatim`), absent, or too short to grade |

Normalisation strips wrap hyphenation, collapses whitespace, and casefolds, before any search.
Tier 4 is only assertable after that (`best-of-⏎breed` in the POWER4 text returns 0 on a raw grep).

## 5. Checker defects found and fixed during this run

Every one would have produced a false finding. All were caught by hand-checking before publication,
per the commission's §4 rule that failures are reported only when hand-confirmed.

| defect | false result it produced | fix |
|---|---|---|
| wrap-hyphen collapse only | `8Kbyte` vs the paper's `8k-byte` → false T3 against **meta p4** | hyphen-insensitive rescue pass, recorded as its own tier |
| plural-only unit match | paper writes `20-stage`, `80-entry` → false NOT-FOUND on **6 of 15** and **3 of 15** model claims | singular/plural variants |
| numeral-only match | paper writes `four threads` → false NOT-FOUND on 3 of 14 | numeral↔spelled-out equivalence |
| PDF-vs-journal page units | every non-Pentium4 family scored **0** page guesses | documented offsets applied (Alpha −23, Niagara −20, POWER4-cpd −26) |

**The last one inverted a headline.** Before the fix, page guesses looked near-worthless corpus-wide.
After it, **chatgpt, grok, kimi and meta score 5/5 within ±2 pages on every paper they answered.**
That was a units bug in the checker, not model behaviour.

## 6. Files

| deliverable | path |
|---|---|
| this note | `_digest/00-corpus-and-harness.md` |
| per-family digests | `_digest/01-alpha.md` … `05-lvs.md` |
| corpus-recall cross-check (commission §2.4) | `_digest/06-crosscheck.md` |
| vet recipe (G5, written last) | `_digest/06-vet-recipe.md` |
| tooling + hashes | `digest/_verify/d4{load,grade,xcheck}.py`, `MANIFEST-D4.sha256` |
| raw run outputs | `digest/_verify/d4run/*.txt`, `*.json` |
