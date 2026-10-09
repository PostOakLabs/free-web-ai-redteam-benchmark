"""Re-render RUNSHEET-34.md against prompts/J-ISSUE-REDTEAM-V1.md.

Only the FRAMING changes:
  - PAPER: <url>            -> RECORD: <proj> issue #<n>, <owner/repo> (GitHub issue thread).
  - *Schema note:* ...      -> removed (it documents a mismatch against the 9-key PAPER schema,
                               which is not JI-v1's target schema; under JI-v1 the issue shape
                               IS the expected shape, and the note reads as "your input is broken")
  - header loop instruction -> points at J-ISSUE-REDTEAM-V1.md

The embedded JSON objects are NOT touched. Verified by hashing every block's JSON
before and after and requiring all 34 digests to match.
"""
import re, sys, json, hashlib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SRC = r"C:\dev\Claude\Projects\ASIC\redteam\RUNSHEET-34.md"

raw = open(SRC, encoding="utf-8").read()

# --- record the invariant BEFORE ---------------------------------------------
def json_digests(text):
    out = []
    for m in re.finditer(r"```json\n(.*?)\n```", text, re.S):
        out.append(hashlib.sha256(m.group(1).encode("utf-8")).hexdigest()[:16])
    return out

before = json_digests(raw)

# --- project short-name per repo (matches JI-v1's own RECORD line format) -----
PROJ = {
    "The-OpenROAD-Project/OpenROAD": "OpenROAD",
    "The-OpenROAD-Project/OpenROAD-flow-scripts": "OpenROAD-flow-scripts",
    "librelane/librelane": "LibreLane",
}

converted = []
def paper_to_record(m):
    url = m.group(1)
    g = re.match(r"https://github\.com/([^/]+/[^/]+)/(issues|pull)/(\d+)", url)
    if not g:
        raise SystemExit(f"unrecognised PAPER url, refusing to guess: {url}")
    repo, kind, num = g.group(1), g.group(2), g.group(3)
    if repo not in PROJ:
        raise SystemExit(f"unmapped repo, refusing to guess a short name: {repo}")
    noun = "issue" if kind == "issues" else "pull request"
    line = f"RECORD: {PROJ[repo]} {noun} #{num}, {repo} (GitHub {noun} thread)."
    converted.append(line)
    return line

out = re.sub(r"^PAPER: (\S+)$", paper_to_record, raw, flags=re.M)

# --- drop the schema-mismatch footnotes --------------------------------------
out, n_notes = re.subn(r"\n\*Schema note:\*[^\n]*\n", "\n", out)

# --- header ------------------------------------------------------------------
OLD_HDR = (
    "# RUNSHEET-34 — 34 red-team paste blocks (2026-09-04)\n"
    "\n"
    "Loop: paste ONE block together with the `prompts/J-EPISODE-REDTEAM-V2.md` prompt text into the free AI; record the verdict in `TALLY-34.md`.\n"
    "Blocks render extraction-file objects VERBATIM (no rewording, no enrichment).\n"
)
NEW_HDR = """# RUNSHEET-34 — 34 red-team paste blocks (re-rendered 2026-09-08 for JI-v1)

**Loop:** paste ONE block together with the text of `prompts/J-ISSUE-REDTEAM-V1.md` into the free
AI; record the verdict in `TALLY-34.md`. Paste the prompt down to (not including) the `---` rule —
everything below that rule is a BUILD NOTE and is not part of the paste.

Blocks render extraction-file objects **VERBATIM** (no rewording, no enrichment). Sources:
`extractions/issue-episodes.json` and `extractions/issue-episodes-batch2.json`.

**Why this file was re-rendered.** It previously paired these blocks with
`prompts/J-EPISODE-REDTEAM-V2.md`, whose schema was verified against the five *paper*-episode
files only. All 34 blocks here are *issue* episodes: they carry
`prior_state`/`observation`/`hypothesis`/`candidates_considered`/`chosen_intervention`/`post_state`
and have no `decision`, `alternatives_or_rejected`, `rationale` or `outcome`. J-v2 asks the reviewer
to attack the decision DIRECTION and to judge a quote against a recalled paper, so on every one of
these blocks both of its pre-screens collapsed to its own `cannot-judge-without-the-paper` escape.
JI-v1 replaces those with `mechanism_check` / `evidence_check` / `attribution_check`, which are
answerable from the pasted record alone. See `SESSION-MEMORIAL-2026-09-08-REDTEAM.md` §1.

**Operator notes — not part of any paste:**
- The old per-block `*Schema note:*` footnotes are gone. They flagged these objects as deviating
  from the 9-key paper schema; under JI-v1 this shape IS the expected shape, and leaving the note in
  told the reviewer their input was malformed.
- **Blocks 04, 05 and 06 carry no `direct_quote` and no `section_or_page_locator`.** That is a real
  property of those records, not a rendering fault. It is deliberately NOT flagged in the block —
  detecting it is what `attribution_check` is for. The prompt's field-level escape
  (`not-determinable-from-this-record`) is the correct answer there.
- Every block is a GitHub issue thread: 31 in `The-OpenROAD-Project/OpenROAD`, 1 in
  `The-OpenROAD-Project/OpenROAD-flow-scripts`, 2 in `librelane/librelane`.
- Block 01 is the exemplar baked into JI-v1 itself. Running it is a **calibration check**, not new
  evidence: the prompt's BUILD NOTE states the expected shape of a competent review (unmeasured
  `post_state` under `evidence_check`, plus the #5971 deferral). A model that returns bare SOUND on
  Block 01 is miscalibrated and its other 33 verdicts should be read with that in mind.
"""
if OLD_HDR not in out:
    raise SystemExit("header not found verbatim — refusing to guess at a replacement")
out = out.replace(OLD_HDR, NEW_HDR, 1)

# --- verify the invariant AFTER ----------------------------------------------
after = json_digests(out)
if before != after:
    raise SystemExit(f"ABORT: embedded JSON changed ({sum(a!=b for a,b in zip(before,after))} blocks)")

open(SRC, "w", encoding="utf-8", newline="").write(out)

print(f"blocks converted PAPER->RECORD : {len(converted)}")
print(f"schema-note footnotes removed  : {n_notes}")
print(f"embedded JSON digests unchanged: {len(before)}/{len(after)}  ALL MATCH")
print(f"PAPER: lines remaining         : {len(re.findall(r'^PAPER: ', out, re.M))}")
print(f"RECORD: lines                  : {len(re.findall(r'^RECORD: ', out, re.M))}")
print(f"size {len(raw)} -> {len(out)} chars")
print("\nsample RECORD lines:")
for c in converted[:3] + converted[-2:]:
    print("   ", c)
