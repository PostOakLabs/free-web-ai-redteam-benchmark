# Wave 1: three-model red-team of ten incident drafts

We picked ten incident drafts from the OpenROAD issue tracker, wrote a prompt that
asks a model to attack each draft's claims and structure, and pasted the same ten
into three free web models. Each model saw each draft once. Thirty reviews came
back. Every one parsed as JSON on the first try, with no repair and no hand-holding.

## The ten drafts

We stratified by failure type rather than taking the first ten. The sheet
(`RUNSHEET-34.md`) holds 34 episode drafts mined from real OpenROAD and
OpenROAD-flow-scripts issues. We selected ten that between them cover:
unmeasured post-state (the most common defect in the set), resolution claimed
without any fix described, a tooling policy that hides errors, a crash on
degenerate input, measurement validity, nondeterminism, silent netlist
corruption, a repair that took 40000 seconds on one endpoint, a misattributed
root cause, and a bug closed without reproduction.

## The three models

kimi, sonnet, and deepseek. We picked these three because they had the cleanest
records on the truth-anchored instruments we ran earlier (arithmetic exact on
9/9 values, format conformance 4/4 on the reference canonicalizer, correct on
the citation anchor probes, correct on the measured browser-behavior anchors).
We also ran chatgpt on the first block as a format pilot. Its response was
schema-compliant, but we did not extend it to the other nine blocks.

## The prompt

JI-v1.2. It asks for a single JSON object with a verdict from a four-value enum,
a list of objections with severities, three field checks that must begin with a
leading code word (HOLDS, BREAKS, MEAS, ASSERT, SUPPORTS, WEAK, ABSENT or N-D),
a list of omissions, and one thing the reviewer would keep. The prompt forbids
browsing, forbids inventing content, and says a field-level escape beats a
guessed objection.

## What came back

Thirty reviews. Every one parsed as JSON with the full seven-key schema and no
extra or renamed keys. No model invented a quote. No model fabricated content.
No model returned bare SOUND on any block, including Block 01, which is known
to be imperfect.

Verdict distribution: 15 SUSPECT, 15 SOUND-WITH-RESERVATIONS. No SOUND, no
IMPLAUSIBLE. Zero fatal objections across all thirty reviews.

The pattern per block:

| block | deepseek | kimi | sonnet | reading |
|---|---|---|---|---|
| 01 | SUSPECT | S-W-RES | S-W-RES | deepseek strictest |
| 02 | SUSPECT | SUSPECT | SUSPECT | unanimous: the evidence-assert class |
| 03 | SUSPECT | SUSPECT | S-W-RES | strong concern |
| 04 | SUSPECT | S-W-RES | SUSPECT | split |
| 05 | SUSPECT | S-W-RES | S-W-RES | |
| 06 | SUSPECT | S-W-RES | SUSPECT | split |
| 07 | SUSPECT | S-W-RES | SUSPECT | split |
| 08 | SUSPECT | S-W-RES | S-W-RES | |
| 09 | S-W-RES | S-W-RES | S-W-RES | unanimous: strongest record |
| 10 | SUSPECT | S-W-RES | S-W-RES | deepseek strictest |

deepseek flagged SUSPECT on nine of ten blocks. kimi and sonnet leaned
SOUND-WITH-RESERVATIONS on most. Block 02, where the resolution is the sentence
"solved on the latest version" with no commit and no PR, drew unanimous SUSPECT.
Block 09, the best-evidenced record in the set, drew unanimous
SOUND-WITH-RESERVATIONS. The models agree on which records are strong and which
are thin.

## What we did not find

No fatal objections. No fabricated quotes. No invented tool or chip names. No
bare SOUND on any block. No model browsed the web. No model refused the task.
The format contract held on every response: first character `{`, last character
`}`, no prose outside the JSON.

## What this does not tell us

These are three models from the same generation of free web AIs. They share
training biases we cannot see. Thirty reviews of ten drafts is enough to
characterize how these three models respond to incident drafts, not enough to
characterize how all models respond to all drafts. The ten drafts are
first-generation mining and have not been reviewed by a human expert. If that
review changes the drafts, these verdicts describe the old drafts.

## What the review debt looks like

None of the thirty verdicts has been reviewed by a human expert. The dataset
card, when it ships, will say "expert review: not performed." The verdicts and
the full response JSON are on disk and hash-verified. Anyone who wants to check
our work can re-run the same prompt on the same block and compare.

## Files

Responses: `Web Model Tasks/Day 8/* red1-*.json` (30 files).
Harvest: `digest/_verify/flash_d6_harvest.py` → `d6run/d6harvest.json`.
Staged tally: `redteam/TALLY-34.md` (three block tables + per-model summary +
cross-model rollup).
Prompt: `prompts/J-ISSUE-REDTEAM-V1.md` (JI-v1.2).
Paste files: `prompts/_paste/redteam/red1-01.paste.md` through `red1-10.paste.md`.
