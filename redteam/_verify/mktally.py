"""Rebuild TALLY-34.md for JI-v1's field set. Titles are read from the re-rendered
RUNSHEET-34.md so the two files cannot drift; nothing is retyped."""
import re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RUN = r"C:\dev\Claude\Projects\ASIC\redteam\RUNSHEET-34.md"
OUT = r"C:\dev\Claude\Projects\ASIC\redteam\TALLY-34.md"

t = open(RUN, encoding="utf-8").read()
rows = re.findall(r"^## Block (\d+) — (.*?) \[([a-z0-9\-]+\.json)\]$", t, re.M)
if len(rows) != 34:
    raise SystemExit(f"expected 34 blocks, found {len(rows)}")

TRUNC = 62
head = """# TALLY-34 — red-team verdicts against `prompts/J-ISSUE-REDTEAM-V1.md`

Re-rendered 2026-09-08 alongside `RUNSHEET-34.md`. The previous version's columns were built for
`J-EPISODE-REDTEAM-V2.md`, whose `direction_check` / `quote_plausibility` fields do not exist in
JI-v1 output and were unanswerable on these records anyway (see
`SESSION-MEMORIAL-2026-09-08-REDTEAM.md` §1).

**One copy of the block table per model run.** Fill from the model's returned JSON object; every
column below maps to exactly one key in it. `Fatal` / `Major` are counts of `objections[].severity`.

## Column coding

JI-v1's three checks are free-text in the JSON. Code them here so the sheet is sortable, and keep
the model's own sentence in `Note` when it is doing real work.

| Column | From JSON key | Codes |
|---|---|---|
| `Verdict` | `verdict` | `SOUND` · `S-W-RES` (SOUND-WITH-RESERVATIONS) · `SUSPECT` · `IMPLAUS` (IMPLAUSIBLE-FOR-THIS-RECORD) |
| `Fatal` / `Major` | count of `objections[].severity` | integer |
| `Mech` | `mechanism_check` | `HOLDS` (causal chain closes) · `BREAKS` (states where it breaks) · `N-D` (not-determinable-from-this-record) |
| `Evid` | `evidence_check` | `MEAS` (post_state measured) · `ASSERT` (claimed, unmeasured) · `N-D` |
| `Attr` | `attribution_check` | `SUPPORTS` (named + dated + locator, and supports the claim) · `WEAK` (present but does not carry the claim) · `ABSENT` (no quote in the record) · `N-D` |

`N-D` is a **pass**, not a gap: JI-v1 instructs a field-level escape over a guessed objection.

**Expected on blocks 04, 05 and 06:** `Attr = ABSENT`. Those three records carry no `direct_quote`
and no `section_or_page_locator`. A model that reports `SUPPORTS` there has invented a quote — treat
that as a disqualifying result for the whole run, not as one bad row.

**Block 01 is a calibration check, not evidence.** It is the exemplar baked into JI-v1 itself, and
the prompt's BUILD NOTE states what a competent review finds: the unmeasured `post_state`
(`Evid = ASSERT`) and the macro-loop cause deferred to #5971. A model returning bare `SOUND` with
zero objections on Block 01 is miscalibrated; read its other 33 verdicts in that light and record it
in the per-model summary.

---

## Block table — model: ________________  date: __________

| # | Title | Verdict | Fatal | Major | Mech | Evid | Attr | Note |
|---|---|---|---|---|---|---|---|---|
"""

lines = []
for n, title, src in rows:
    ti = title if len(title) <= TRUNC else title[: TRUNC - 1].rstrip() + "…"
    ti = ti.replace("|", r"\|")
    lines.append(f"| {n} | {ti} |  |  |  |  |  |  |")

tail = """

## Per-model summary (one row per model run)

| Model | Date | SOUND | S-W-RES | SUSPECT | IMPLAUS | Blk01 calibration | Attr invented on 04/05/06 | Survivors first |
|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  | pass / miscalibrated | yes / no |  |

`Survivors first` = the block numbers this model left standing with no fatal objection, in the order
you would send them to expert review.

## Cross-model rollup (fill once several models are in)

| # | Runs | Worst verdict | Fatal count across models | Consensus defect | Ready for expert review? |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

A block only reaches expert review when no model returned a fatal objection on it. A block that
several models mark `Evid = ASSERT` is not thereby disqualified — under JI-v1 an unmeasured
resolution is an evidence defect and is explicitly **not** counted as a fatal objection.
"""

open(OUT, "w", encoding="utf-8", newline="").write(head + "\n".join(lines) + tail)
print(f"wrote {OUT}")
print(f"  block rows      : {len(lines)}")
print(f"  titles source   : RUNSHEET-34.md (not retyped)")
print(f"  bytes           : {len(head)+len('\\n'.join(lines))+len(tail)}")
