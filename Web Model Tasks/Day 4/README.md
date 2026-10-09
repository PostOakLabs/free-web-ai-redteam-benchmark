# Day 4 — UNDIGESTED model responses (moved from Day 3, 2026-09-08)

> ## ⛔ NOTHING IN THIS FOLDER HAS BEEN DIGESTED, PARSED, GRADED, OR CHECKED.
>
> These 73 files were moved here **as-collected**. No file was opened, edited, renamed, repaired, or
> analysed during the move. Absence of a defect note here means **nobody looked**, not that the file
> is clean.

## Why these files are here

They sat in `Day 3/` alongside the five families that were digested on 2026-09-05, and were missed:
the digest loader carried a family allow-list and printed `SKIP unrecognised family:` 73 times into
output that was read through a pager. Full account:
`../../SESSION-MEMORIAL-2026-09-08-REDTEAM-4.md` §2.

They are **not** late arrivals. Every file is dated **2026-09-04 14:39–14:42**, a day before the
digest ran.

## Contents

| family | files | prompt | paper / subject |
|---|---|---|---|
| `alpha` | 14 | `prompts/D2-ALPHA21264-RECALL.md` | Kessler, *The Alpha 21264 Microprocessor*, IEEE Micro 19(2):24–36, 1999 |
| `niagara` | 14 | `prompts/D2-NIAGARA-RECALL.md` | Kongetira et al., *Niagara: A 32-Way Multithreaded SPARC Processor*, IEEE Micro 25(2), 2005 |
| `p4` | 15 | `prompts/D2-PENTIUM4-RECALL.md` | Hinton et al., *The Microarchitecture of the Pentium 4 Processor*, Intel Tech. Journal Q1 2001 |
| `pphysical` | 14 | `prompts/D2-POWER4-PHYSICAL-RECALL.md` | Warnock et al., *The circuit and physical design of the POWER4 microprocessor*, IBM JRD 46(1):27–52, 2002 |
| `lvs` | 15 | `prompts/F-LVS-MISMATCH-CLASSES.md` | LVS mismatch classes (not a paper-recall prompt) |
| `power` | 1 | — | **misfiled, see below** |

**73 files. Four of the five families are paper-recall; `lvs` is not.**

## `yuanbao power.json` — misfiled, deliberately not renamed

It is **yuanbao's `alpha` answer under a truncated filename**, diagnosed before the move:

- `page_guess` values 24, 28, 30 fall inside Alpha 21264's 24–36 page range.
- Content is Alpha: Ebox, clustered integer execution with duplicated integer register files, a
  20-entry integer issue queue.
- yuanbao is the only model in the corpus with no `alpha.json`.

**It was not renamed.** The as-collected filename is the evidence of the collection defect, and
renaming it would destroy that while a digest pass has not yet confirmed the diagnosis. Treat the
`alpha` family as **15 models**, and confirm or overturn this reading when the family is digested.

## Known context a digest pass should not re-derive

- **`pphysical` is the companion paper to Day 3's digested `power4` family.** `Day 3/_digest/03-power4.md`
  flags a `minimax m3` entry as clock-distribution content belonging to "the companion paper" and
  treats it as an anomaly. The companion's own 14 files are here.
- **These four paper-recall families are an untapped cross-check on the extraction corpus.** They
  answer against the same five papers that `SESSION-MEMORIAL-2026-09-08-REDTEAM-3.md`'s numerics
  sweep covered. That sweep used exactly one file from here (`meta alpha.json:27`) to corroborate a
  defect the panel had flagged on 2026-08-31 and nobody read for eight days.
- **`RUN-MANIFEST.tsv` does not know about these 73 files.** It stands at 444 rows; the corrected
  target is **517**. See the correction block in `../../DAY3-FOLD-NORMALIZE-1.md`.
- **No quarantine gate exists for this folder.** `Day 3/_digest/quarantine.json` covers the five
  digested families only and says so in its `_scope_correction_2026_09_08` key. Day 3's gate found
  a byte-identical duplicate, a hard parse failure, three collection-truncated files and three
  field-contaminated files in 70 files. Assume this folder has its own and has not been looked at.

## Move record

Moved `2026-09-08` from `Web Model Tasks/Day 3/`. Filenames unchanged. Mtimes preserved by `mv`.
Day 3 retains its 70 digested response files, its `_digest/` output, and the browser-dispatch harness
(`MECHANISM-NOTES.md`, `_inject.js`, `_payload.*`, `dispatch-state.json`), which documents the
`boundary` run only and stays with it.
