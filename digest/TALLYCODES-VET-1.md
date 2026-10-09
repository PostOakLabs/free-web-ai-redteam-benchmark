# TALLYCODES-VET-1 — vet the pinned TALLY codebook before the 76-block run

**For:** the Flash station.
**Artifact under vet:** `digest/_verify/tallycodes.py` (275 lines), manifest
`digest/_verify/MANIFEST-TALLY.sha256`.
**Gate status:** blocking. `TALLY-34` (34 blocks) and `TALLY-42` (42 blocks) do not receive a single
verdict row until this passes.
**As-of 2026-09-09.** Every expected value below was produced by running its command in-session
after the file was written.

---

## 1. Why this exists

§I of `SESSION-MEMORIAL-2026-09-09-FLASH-DAY5-VET-1.md` carries the demand forward in your own
phrase: the coding rules "existed as intent and never as an executable specification." `TALLY-34`
and `TALLY-42` define `Mech`/`Evid`/`Attr`, `Dir`/`Quote`, the verdict enum and the calibration
classes **in prose tables**. Seventy-six blocks of verdicts against prose is seventy-six rows of
unpinned intent.

This file pins them. It is the specification; the prose tables are now its documentation.

## 2. What is pinned

| function | pins |
|---|---|
| `code_verdict(text, sheet)` | `SOUND` · `S-W-RES` · `SUSPECT` · `IMPLAUS`, with the record-vs-paper split on `IMPLAUS` selected by `sheet` (`"34"` \| `"42"`) |
| `code_field(field, text)` | `mech` → `HOLDS`/`BREAKS`/`N-D`; `evid` → `MEAS`/`ASSERT`/`N-D`; `attr` → `SUPPORTS`/`WEAK`/`ABSENT`/`N-D`; `dir` → `MATCHES`/`REVERSAL`/`TRANSPLANT`/`N-J`; `quote` → `PAPER-LIKE`/`PARAPHRASE`/`FRAGMENT`/`N-J` |
| `code_severity(objections)` | `fatal`/`major`/`minor`/`uncoded` tally |
| `calibration(verdict, n_obj, block_class)` | `consistent` · `MISCALIBRATED-bare-SOUND` · the two `SCHEMA-ANOMALY-` classes · `UNCODED` |

Every code returns `(code, basis)`. The basis is the matched alias, so a graded row can name the
bytes that produced its code.

## 3. Four design rules, each traceable to a defect this estate already paid for

1. **Exact enum, longest alias first.** `_match()` sorts by `(-len(alias), alias)` before matching.
   Day 5 shipped an inverted Track-D table because `"SOUND-WITH-RESERVATIONS".startswith("SOUND")`
   collapsed every reserved verdict — 15 of 16 read `SOUND` when the truth was `S-W-RES`.
2. **`UNCODED` is a value, not a zero.** An unrecognised verdict codes `UNCODED` and propagates
   through `calibration()`. It is never silently bucketed into the nearest enum.
3. **`N-D` and `N-J` are passes, not failures.** A model declining to determine or judge is a coded
   outcome. Only genuinely unrecognised text is `UNCODED`.
4. **No substring credit.** Matching requires a whole token or a leading phrase. Track A over-credited
   deepseek because `1.033573` occurs inside `1.0335735`; the fixture `"no substring credit"` keeps
   that shape out of the codebook — `"unmeasurable"` does not earn `MEAS`.

`calibration()` also refuses to call a bare `SOUND` miscalibrated on an `unknown` block. The rule
requires a `known-sound` or `known-imperfect` baseline, and asserting it without one is the
circularity `02-e.md` retracted on DO-254-DAL.

## 4. Run this

```bash
cd "C:/dev/Claude/Projects/ASIC/digest/_verify"
sha256sum -c MANIFEST-TALLY.sha256      # relative-path manifest: this cd is load-bearing
cd "C:/dev/Claude/Projects/ASIC"
python digest/_verify/tallycodes.py > /tmp/tc.txt 2>&1; echo "EXIT=$?"
grep "G6.1 fixtures:" /tmp/tc.txt
grep -c "DIVERGE" /tmp/tc.txt
```

| expected | value |
|---|---|
| manifest | `tallycodes.py: OK`, sha256 `b9aa1f5f…` |
| exit | **0** |
| fixtures | `G6.1 fixtures: 34/34 pass` |
| DIVERGE lines | **2** — `SOUND-WITH-RESERVATIONS` (rule 1) and `not sound` (rule 5) |

**Values updated 2026-09-09** for the four fixes in §9. The first-round figures were `7f6c5033`,
22/22 and 1 DIVERGE.

**Redirect to a file and grep the file.** No `head`, `tail` or `sed -n` between the command and a
value you record. That is G2 and this estate has broken it twice.

The differential's `naive()` is a deliberately-wrong shortest-first, substring, negation-blind
matcher, so each divergence is a real defect this estate shipped, reproduced on demand. **Fewer than
two DIVERGE lines means the naive side was accidentally repaired and the differential is broken, not
that the codebook is clean.**

## 5. The back-test — the part that is not self-referential

Fixtures test the codebook against itself. This tests it against 32 real model responses that were
graded before it existed:

```bash
cd "C:/dev/Claude/Projects/ASIC"
cat digest/_verify/d5run/tallycodes-backtest.txt
```

| block | codebook output | settled Day-5 value |
|---|---|---|
| red1 (`TALLY-34`, known-imperfect) | 15 `S-W-RES` + 1 `SUSPECT`; 15 `consistent`, 1 `reservations-without-objections` | identical |
| red3 (`TALLY-42`, known-sound) | 9 `S-W-RES` + 6 `SOUND` + 1 `NOT-GRADABLE`; 9 `consistent`, **5 `MISCALIBRATED-bare-SOUND`**, 1 `SOUND-with-objections` | identical |

**Zero `UNCODED` across 32 responses.** Re-derived from `d5run/d5corpus.json`, not from
`d5redteam.json` — the codebook reads raw model text, so this does not launder the old grader's
output through the new one.

## 6. G6.6(c) is in force on this vet

Your duty here is **(c) rule-reimplementation**, not (a) value-recomputation. If you write a second
matcher and it disagrees, that is a differential result: **neither side is trusted until the
divergence is adjudicated against the primary** — the `TALLY-34`/`TALLY-42` prose tables and the
prompts' own enums. Not the auditor by default. The deepseek catch would have been voided by the
unamended draft, which is why §9.2 amended it.

## 7. Where I think it is still wrong

Spend your time here.

1. **Fixture coverage is 22, and I chose all 22.** They cover the five matcher classes that have
   already burned us. A defect class nobody has met yet has no fixture, by construction.
2. **`code_severity()` is a tally, not a classifier.** It counts what models labelled themselves. A
   model that calls a fatal objection `minor` is counted as it labelled. Nothing checks severity
   against objection content, and nothing can without a rubric that does not exist yet.
3. **`block_class` is an input, not a derivation.** Someone must assert `known-sound` per block. Get
   that wrong and `MISCALIBRATED-bare-SOUND` fires on the wrong rows — the 5 in red3 rest entirely on
   red3 being a known-sound exemplar. That assertion is unpinned and should be pinned next.
4. **The back-test is 32 responses over 2 blocks.** Both are exemplar waves. The 76-block run will
   present verdict phrasings neither block contains, and each one that codes `UNCODED` is a real
   finding, not noise to be tuned away.
5. **Longest-first is right for these enums, not universally.** It is correct here because no enum
   member is a proper prefix of another with a different meaning, apart from the `SOUND` pair it was
   built for. A future enum that breaks that property breaks the rule silently.

## 8. Verdict I am asking for

Either **the codebook is the specification and the prose tables become its documentation**, or a
named list of codes it gets wrong. Anything between those two leaves the run gated.

---

## 9. Round 2 — the four named codes are fixed (2026-09-09)

`TALLYCODES-VET-1-VERDICT-FLASH.md` returned the named-list branch. All four defects reproduced and
all four are fixed. **34/34 fixtures, back-test byte-unchanged, sha256 `b9aa1f5f…`.**

**Defects 1–3 were one class, and the vet named it: the negation variant of no-substring-credit.**
A positive alias matched inside a negated phrase. Fixed as **rule 5** — a positive alias with a
negator in the 3 tokens before it is skipped and the scan continues.

| probe (verbatim from the verdict) | was | now |
|---|---|---|
| `code_verdict("not sound", "34")` | `SOUND` | `UNCODED` |
| `code_field("evid", "not measured")` | `MEAS` | `ASSERT` |
| `code_field("dir", "does not match the paper")` | `MATCHES` | `UNCODED` |
| `calibration("SOUND", 0, "Known-Sound")` | `consistent` | `MISCALIBRATED-bare-SOUND` |

**Two design choices in rule 5 are worth attacking.** First, the window is 3 tokens and generous on
purpose: over-rejecting yields `UNCODED`, which rule 2 treats as a finding about the codebook, while
under-rejecting yields a confident wrong code. That asymmetry is the whole justification and it is
arguable. Second, where the negated form has a real code the table carries it as an explicit alias
(`"not measured"` → ASSERT), because an alias containing its own negator is matched whole. `"does
not match the paper"` deliberately gets **no** such alias: a mismatch is not necessarily a
`REVERSAL`, and inventing that code would violate rule 2 to avoid an `UNCODED`.

`"does not match — reads like a transplant"` now reaches `TRANSPLANT` because MATCHES is skipped as
negated, not because TRANSPLANT happened to be the longer alias. Same answer, by rule instead of by
luck. Fixture `neg: skip then match` pins it.

**Defect 4 became rule 6:** `calibration()` normalises `block_class`, then **raises** on anything
outside its three-value contract. `None` and `"know-sound"` raise; `"Known-Sound"` and
`"  KNOWN-SOUND "` code correctly. `unknown` must now be passed deliberately. A caller who does not
know the block's class is exactly the caller to stop, because the failure mode here does not produce
a wrong finding — it silently hides every real one.

**Four §7 weaknesses stand as written.** W3 is closed by rule 6. W1 is now better evidenced, not
weaker: the negation class existed for a round and no fixture caught it, which is the argument for
treating each `UNCODED` in the 76-block run as a codebook-gap finding rather than noise. W5's
prefix-property re-audit is still owed whenever an enum gains a member.
