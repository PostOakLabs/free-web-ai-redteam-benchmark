# DIGEST COMMISSION — DAY 4 — 73 files, 5 families — with the failure modes of Days 1–3 priced in

Commissioned by the Flash re-audit session (`SESSION-MEMORIAL-2026-09-08-FLASH-REAUDIT-1.md`) on
the operator's instruction, 2026-09-08, before the Opus digest session begins Day 4. Everything asserted
below cites a file on disk or a command that reproduces it. §1 gates are stop-the-run violations,
not style preferences — each one exists because a prior day tripped over it.

**The corpus (verified 2026-09-08):** `Web Model Tasks/Day 4/` holds **73 response files** —
`alpha` 14 (+1 misfiled, §2.5), `niagara` 14, `p4` 15, `pphysical` 14, `lvs` 15. Prompts on disk:
`prompts/D2-ALPHA21264-RECALL.md`, `D2-NIAGARA-RECALL.md`, `D2-PENTIUM4-RECALL.md`,
`D2-POWER4-PHYSICAL-RECALL.md`, `F-LVS-MISMATCH-CLASSES.md`.

---

## 1. Hard gates — each priced by a specific prior failure

**G1. Census gate.** `ls "Web Model Tasks/Day 4"/*.json | wc -l` → **73**, run before loading
anything. The loader must assert `loaded + skipped == 73`, and `skipped` must be **0**. Any skip is
a STOP, not a note.
*Price:* `digest/_verify/load.py`'s hard-coded family allow-list silently skipped **73 of 143**
Day-3 files on the defining run (memorial-4 §2). Invert the default: unknown family ⇒ digest it or
halt, never skip.

**G2. No verdict through a pipe.** Full output goes to a file; status classes are `grep -c`'d from
that file; the true `$?` is captured before any filter (use `run.cmd > out.txt 2>&1; EXIT=$?`).
Never `| head`, `| tail`, `| sed -n '1,Np'` between a command and a verdict you will record.
*Price:* twice in one session — `--check | head` (read head's exit 0, true exit 1; audit file §5)
and `load.py 2>&1 | sed -n '1,60p'` (cut 73 SKIP warnings above the table; memorial-4 §2).

**G3. Tooling preserved before the run.** Loader + analysers land in `digest/_verify/` (prefix
`d4` to avoid Day-3 name collisions), `MANIFEST.sha256` generated, and the digest is produced by
those exact files. No post-hoc reconstruction.
*Price:* `day2load.py` was rebuilt after the fact and validated only against its own reported
figures — the audit file's own §6 says this is the weakest link in its chain. Don't re-earn that.

**G4. Determinism gate at the end.** Re-run the full chain; derived JSONs must regenerate
byte-identically (hash before/after). The standard is achievable: Day 3's `corpus.json` /
`day2.json` / `day2b.json` all reproduced byte-identically under the 09-08 re-audit.

**G5. No placeholders, no stale recipes.** The "how to vet this" section is written **last**,
after any file move, with every expected value produced by a command run in the same session, and
each count **as-of stamped**.
*Price:* memorial-4 §3's recipe (`SKIP count` → expect 73) was broken by its own §4 move (now
returns 0) and §4 itself is an empty stub; audit file §3 promised `grep -c 'Schema note'` → 0
(actual 1) and §10 named a `best-ofbreed` token that exists nowhere. All four defects were checks
written from memory instead of run.

## 2. What Day 4 must do that Days 1–3 didn't

**2.1 The asymmetry that upgrades the grading.** Day 3's `library`/`patterns` slices were
schema-and-convergence only, and RECEIPT went unadjudicated for lack of embedded ground truth
(`TODO(alice)`, `day2-c1b-c2-adjudication.md:672`). **Day 4 has local ground truth on disk.** Bind
each family and grade against it:

| family | prompt | ground truth |
|---|---|---|
| `alpha` | `prompts/D2-ALPHA21264-RECALL.md` | `sources/Alpha21264-pagemarked.txt` |
| `niagara` | `prompts/D2-NIAGARA-RECALL.md` | `sources/Niagara-pagemarked.txt` |
| `p4` | `prompts/D2-PENTIUM4-RECALL.md` | `sources/Pentium4-pagemarked.txt` |
| `pphysical` | `prompts/D2-POWER4-PHYSICAL-RECALL.md` | `sources/POWER4-cpd-pagemarked.txt` |
| `lvs` | `prompts/F-LVS-MISMATCH-CLASSES.md` | the prompt's own class definitions (no paper — say so) |

**2.2 Four-tier grading of numeric/quote claims** against the normalised source text:
**verbatim / paraphrase-consistent / contradicts-paper / not-found-in-paper.** Normalisation MUST
strip hyphenation at line-wraps **and** collapse whitespace before any substring search.
*Price:* the paper text is `deliver best-of-⏎breed` (`sources/POWER4-sys-pagemarked.txt:121–122`);
a raw `best-of-breed` grep returns 0 and a false NOT-IN-PAPER on a real quote is the known failure.
Tier-4 "not found" is only assertable after the normalised search.

**2.3 Convergence AND check.** Publish the cross-model table per family — then actually check the
contested sentences against the paper. Day 3 could only flag "9 of 13 assert it, retrieved by
none" (NEEDS-RETRIEVAL). Here the corpus's agreement is *checkable*, so "13 of 15 recall X" must be
followed by "and the paper says X at line N" or "the paper says ≠X — majority wrong".

**2.4 Run the paid-for defect detector.** Memorial-3's sweep fixed ep00 `5%→90%` and ep06
`95%→85%` (corroborated verbatim at `Day 4/meta alpha.json:27`) and declared a blind spot of 48
lenient-matched tokens dominated by powers of two. The Day-4 corpus independently recalls those
same sentences 14–15 more times per family. Grade the whole corpus's recall of each flagged
sentence and the lenient tokens explicitly. This is the cheapest defect detection the estate owns.

**2.5 Model-set completeness is a finding, not a gap.** Enumerate each family's model set in the
digest. A missing model is recorded, never absorbed. Live example: yuanbao has no `alpha.json`
because its alpha answer is misfiled as `Day 4/yuanbao power.json` (diagnosed: `page_guess`
24/26/28/30 in Alpha's range; Ebox / integer-issue-queue content). **Digest it as `alpha`, 15th
file, with the misfile provenance preserved. Do not rename it** — the as-collected filename is the
evidence of the collection defect.

**2.6 NEEDS-RETRIEVAL narrows.** Day 3 parked claims because ground truth wasn't embedded. On Day
4, paper-backed claims are checkable — grade them, don't park them. The marker survives only for
post-paper developments and whatever the LVS prompt genuinely leaves undefined.

## 3. Digest-document requirements

1. **Coverage statement in the first screen:** "73 of 73 files across 5 families; 0 skipped," with
   the census command and as-of timestamp. Any exclusion gets an explicit NOT-DIGESTED table with a
   reason. *Price:* the Day-3 digest printed "70 files / 5 families" flat, no denominator, and 73
   files went undigested for three days.
2. **Every number is a command output.** Quote said-vs-computed in the digest or a `_verify`
   companion (extend `irb.py`'s `said X vs computed Y` pattern to text claims).
3. **Quarantine gate extended to 10 of 10 families**; keep the `_scope_correction_2026_09_08` key
   intact. Today it covers 5.
4. **Corrections prepend, never absorb** (the Day-3 convention done right: the scope block atop
   `00-corpus-and-harness.md`, original text retained).
5. **As-of stamp every drift-capable count.** *Price:* the audit file's §8 quoted 293 flat-md /
   44 dangling / 429 entries as current; live is 306 / 45 / 448 — thirteen files of drift from
   other sessions in three days.

## 4. Keep — regressions here cost more than the improvements above

Byte-identity gates on any re-render; salvage with recorded parse classes; failures reported only
when hand-confirmed (the checker false-positive log is the method's honesty); anchored substring
edits gated on occurrence-count (memorial-3's discipline that prevented the `5%`-inside-`95%`
corruption); machine-readable gates; `TODO(alice)`-style candour about anything genuinely
unadjudicable.

## 5. Deliverables

1. `Web Model Tasks/Day 4/_digest/00-corpus-and-harness.md` + one digest per family (Day-3 layout).
2. `digest/_verify/d4*.py` + `MANIFEST.sha256`, generated before the digest run (G3).
3. Quarantine extension to 10 families (§3.3).
4. The corpus-recall cross-check section (§2.4) — this is the deliverable the estate most wants.
5. A vet recipe written last (G5), then handed to the Flash re-audit session for independent
   verification — self-audit is weaker than independent audit, as memorial-4 itself put it.

---

## Addendum — 2026-09-08, after RUNSHEET-42 verification (Flash session)

`redteam/RUNSHEET-42.md` + `TALLY-42.md` were built and Flash-verified the same day: mkrunsheet42.py
regenerates byte-identically; 42/42 episodes carry exactly J-v3's nine keys; Block 08 reproduces
J-v3 byte-for-byte; Blocks 32/36 are the same POWER4 binary-compatibility decision (byte-identical
`direct_quote`); 18 of 42 quotes carry the one disclosed wrap-collapse, words unchanged.

Consequences for THIS commission:

- **§2.2's normalisation is no longer advisory — it is the verified estate policy.** Grade recall
  quotes with the identical wrap-and-hyphen collapse (J-v3's rule, proven on 18 quotes at RUNSHEET-42;
  one control character survives at Block 34 and is disclosed, not repaired — do the same if Day-4
  grading meets one).
- **Record per-model recall so TALLY-42 can use it.** RUNSHEET-42's operator notes call for grading
  `direction_check` against each model's own prior recall of the same five papers — which is exactly
  what this digest produces. Emit per-model, per-paper recall verdicts in the digest (not only
  per-family aggregates) so a future TALLY-42 run can be cross-graded against them without re-parsing.
- **The redteam track is unblocked and does not gate this digest.** The J-v2 pairing failure (all 34
  blocks escaping) is fixed at the source: the schema pre-check this digest must also run (G1's
  census + the nine-key assertion) is the same check that made J-v3 fit.
