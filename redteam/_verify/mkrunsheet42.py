"""Build RUNSHEET-42.md + TALLY-42.md for prompts/J-EPISODE-REDTEAM-V3.md.

Renders all 42 paper-episode objects from extractions/*.episodes.json VERBATIM, one
block per episode, in V3's own PAPER:-line format.

Invariants enforced by this script, not asserted by its author:
  * every block's JSON is re-parsed and compared key-sorted against the source
    extraction object; any difference aborts the build
  * every episode must carry exactly V3's 9 keys; a missing or extra key aborts
  * citations are read from prompts/D2-*-RECALL.md, never retyped from memory
"""
import json, os, re, sys, hashlib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ASIC = r"C:\dev\Claude\Projects\ASIC"
OUT_RUN = os.path.join(ASIC, "redteam", "RUNSHEET-42.md")
OUT_TAL = os.path.join(ASIC, "redteam", "TALLY-42.md")

V3KEYS = ["title", "section_or_page_locator", "decision", "alternatives_or_rejected",
          "rationale", "outcome", "direct_quote", "gaps", "confidence"]

# extraction file -> (prompt file carrying the citation, short paper label)
POOLS = [
    ("Alpha21264",                      "D2-ALPHA21264-RECALL",        "Alpha 21264"),
    ("Niagara",                         "D2-NIAGARA-RECALL",           "Niagara"),
    ("Pentium4",                        "D2-PENTIUM4-RECALL",          "Pentium 4"),
    ("POWER4-circuit-physical-design",  "D2-POWER4-PHYSICAL-RECALL",   "POWER4 circuit/physical"),
    ("POWER4-d2true",                   "D2-POWER4-RECALL",            "POWER4 system (d2true pool)"),
    ("POWER4-system-microarchitecture", "D2-POWER4-RECALL",            "POWER4 system"),
]


def citation(prompt_stem):
    """Lift the bibliographic record from the D2 prompt's first line and restyle it to
    J-v3's own PAPER-line form: Authors, "Title," Journal, vol. N, no. N, pp. X-Y, Date.
    Verified below by requiring the Niagara result to equal V3's line byte-for-byte."""
    line = open(os.path.join(ASIC, "prompts", prompt_stem + ".md"),
                encoding="utf-8").readline()
    m = re.search(r'\*\*"(.+?)"\s+—\s+(.+?)\s+—\s+(.+?)\.?\*\*', line)
    if not m:
        raise SystemExit(f"citation not parseable from {prompt_stem}: {line[:120]}")
    title, authors, venue = m.group(1), m.group(2), m.group(3).rstrip(".")
    v = re.search(r'^(.*?),\s*Vol\.\s*(\d+),\s*No\.\s*(\d+),\s*(.+?),\s*pp\.\s*(\S+)$', venue)
    if v:
        journal, vol, no, date = v.group(1), v.group(2), v.group(3), v.group(4)
        pages = v.group(5).replace("–", "-")
        date = date.replace("–", "-")
        venue = f"{journal}, vol. {vol}, no. {no}, pp. {pages}, {date}"
    return f'{authors}, "{title}," {venue}.'


def collapse_wrap(q):
    """Collapse PDF line-wrap whitespace inside a direct_quote, exactly as J-v3 did to
    its own exemplar ("these were collapsed to single spaces so quote_plausibility judges
    prose rather than line-wrap artifacts. No words changed.").
    Words are NOT altered — asserted by the word-sequence check in the caller."""
    return re.sub(r"[ \t]*[\r\n]+[ \t]*", " ", q)


def episodes(stem):
    d = json.load(open(os.path.join(ASIC, "extractions", stem + ".episodes.json"),
                       encoding="utf-8"))
    return d["episodes"] if isinstance(d, dict) and "episodes" in d else d


_v3 = open(os.path.join(ASIC, "prompts", "J-EPISODE-REDTEAM-V3.md"), encoding="utf-8").read()
_v3cite = re.search(r"^PAPER: (.+)$", _v3, re.M).group(1)
if citation("D2-NIAGARA-RECALL") != _v3cite:
    raise SystemExit("ABORT: restyled citation != J-v3's own PAPER line\n"
                     f"  built: {citation('D2-NIAGARA-RECALL')}\n  V3   : {_v3cite}")

blocks, rows, n = [], [], 0
unwrapped, ctrl = [], []
exemplar_block = None
EX = episodes("Niagara")[0]                       # the object baked into V3

for stem, prompt_stem, label in POOLS:
    cite = citation(prompt_stem)
    for i, ep in enumerate(episodes(stem)):
        missing = [k for k in V3KEYS if k not in ep]
        extra = [k for k in ep if k not in V3KEYS]
        if missing or extra:
            raise SystemExit(f"ABORT {stem}[{i}] schema: missing={missing} extra={extra}")
        n += 1
        tag = ""
        if stem == "Niagara" and i == 0:
            tag = "  ⚠ CALIBRATION — this is the exemplar baked into J-v3 itself"
            exemplar_block = n
        ep = dict(ep)
        q0 = ep.get("direct_quote") or ""
        if isinstance(q0, str) and any(c in q0 for c in "\r\n"):
            q1 = collapse_wrap(q0)
            if q0.split() != q1.split():
                raise SystemExit(f"ABORT {stem}[{i}]: wrap-collapse changed words")
            ep["direct_quote"] = q1
            unwrapped.append((stem, i))
        if isinstance(ep.get("direct_quote"), str) and \
           any(ord(c) < 0x20 for c in ep["direct_quote"]):
            ctrl.append((stem, i, n))
        body = json.dumps(ep, ensure_ascii=False, indent=2)
        blocks.append(
            f"## Block {n:02d} — {ep['title']} [{stem}.episodes.json ep{i:02d}]{tag}\n\n"
            f"PAPER: {cite}\n\n```json\n{body}\n```\n")
        rows.append((n, ep["title"], label, stem, i))

# --- locate the cross-pool duplicate decision, do not hardcode its number ------
# De-hyphenate before matching: d2true writes "binary-compatibility", sys writes
# "binary compatibility". A literal-space search finds only one of the two.
dup = [num for num, title, label, stem, i in rows
       if "binary compat" in title.lower().replace("-", " ")]
if len(dup) != 2:
    raise SystemExit(f"ABORT: expected exactly 2 binary-compatibility blocks, found {dup}")
DUP_A, DUP_B = dup

# --- verify every rendered block against its source object ---------------------
rendered = "\n".join(blocks)
checked = 0
for m in re.finditer(r"```json\n(.*?)\n```", rendered, re.S):
    checked += 1
src_all = []
for stem, _, _ in POOLS:
    src_all.extend(episodes(stem))
for idx, m in enumerate(re.finditer(r"```json\n(.*?)\n```", rendered, re.S)):
    got = json.loads(m.group(1))
    raw = src_all[idx]
    want = dict(raw)
    if isinstance(want.get("direct_quote"), str):
        want["direct_quote"] = collapse_wrap(want["direct_quote"])
    if json.dumps(got, sort_keys=True, ensure_ascii=False) != \
       json.dumps(want, sort_keys=True, ensure_ascii=False):
        raise SystemExit(f"ABORT: block {idx+1} does not match its source object")
    for k, v in raw.items():
        if k != "direct_quote" and got[k] != v:
            raise SystemExit(f"ABORT: block {idx+1} field {k} altered")
    if str(raw.get("direct_quote", "")).split() != str(got.get("direct_quote", "")).split():
        raise SystemExit(f"ABORT: block {idx+1} quote words changed")

HDR = f"""# RUNSHEET-42 — 42 red-team paste blocks for `prompts/J-EPISODE-REDTEAM-V3.md` (2026-09-08)

Every paper-episode object in the corpus, rendered from `extractions/*.episodes.json`. No rewording,
no enrichment. **One disclosed normalisation, described below; every other byte is verbatim.**

## The one normalisation — `direct_quote` line-wrap, 18 of 42 blocks

Stored quotes carry the PDF's `\\r\\n` line breaks, often mid-word. **18 of the 42 are affected, and
two whole pools are affected entirely** (Niagara 6/6, POWER4-circuit-physical 8/8). Left in, they
make `quote_plausibility` judge PDF extraction artifacts rather than prose on 43% of the run.

J-v3 already resolved this for the one block it controls — its BUILD NOTE records collapsing the
exemplar's wrap points to single spaces *"so quote_plausibility judges prose rather than line-wrap
artifacts. No words changed."* **The same collapse is applied here to all 18, and to nothing else.**
The builder asserts it: the whitespace-split word sequence of every quote must be identical before
and after, and every other field must compare byte-equal to its source object, or the build aborts.

**Consequence, verified:** substituting Block {exemplar_block} reproduces the unmodified J-v3 prompt exactly —
same JSON object, same `PAPER:` line. Before this normalisation it did not, which is how the issue
was found.

**One quote is degenerate and was NOT repaired.** Block {ctrl[0][2] if ctrl else '-'} (`POWER4-d2true` ep05) reads `"Eight-way, 128-byte line \\x011.5 MB"` — a stray control character
from the PDF layer survives the wrap collapse. Repairing it would be a content edit. Treat
`quote_plausibility` on that block as uninformative rather than as a fabrication signal.

## ⛔ How to paste — READ THIS, the obvious method is wrong

J-v3 is a **standalone** prompt: it already contains a worked exemplar under the heading
*"The draft under review:"*. Appending a block after it gives the model **two** drafts and no
statement of which to review.

**For each block: paste J-v3 with the block SUBSTITUTED IN, not appended.** Replace the prompt's
`PAPER:` line and the JSON fence that follows it with the block's `PAPER:` line and JSON fence.
Everything else in the prompt — the review schema, the hard rules, the version tag — stays byte
identical. Stop at the `---` rule; the BUILD NOTE below it is not part of the paste.

*(The same ambiguity exists in the `RUNSHEET-34.md` / `J-ISSUE-REDTEAM-V1.md` pairing, which says
"paste ONE block together with the prompt". Substitution is the correct reading there too.)*

## Contents — {n} blocks, 5 papers, 6 extraction files

| blocks | paper | extraction file |
|---|---|---|
| 01–07 | Alpha 21264 | `Alpha21264.episodes.json` |
| 08–13 | Niagara | `Niagara.episodes.json` |
| 14–20 | Pentium 4 | `Pentium4.episodes.json` |
| 21–28 | POWER4 circuit/physical | `POWER4-circuit-physical-design.episodes.json` |
| 29–34 | POWER4 system — d2true pool | `POWER4-d2true.episodes.json` |
| 35–42 | POWER4 system | `POWER4-system-microarchitecture.episodes.json` |

**Schema pre-check passed:** all 42 episodes carry exactly J-v3's nine keys — `title`,
`section_or_page_locator`, `decision`, `alternatives_or_rejected`, `rationale`, `outcome`,
`direct_quote`, `gaps`, `confidence` — with no extras and none missing. This check is the one that
was never run for J-v2 against the issue-episode set, which is why that pairing collapsed to its own
escape clause on all 34 blocks (`SESSION-MEMORIAL-2026-09-08-REDTEAM.md` §1). J-v3 genuinely fits
this pool.

**Operator notes — not part of any paste:**

- **Block {exemplar_block} is the exemplar baked into J-v3 itself.** Run it as a **calibration check**: J-v3's BUILD NOTE calls this a
  known-**sound** episode, so a reviewer returning many fatal objections here is miscalibrated, and
  its other 41 verdicts should be read in that light. It is not new evidence.
- **Two POWER4 pools describe the same paper** (IBM JRD 46(1) pp. 5–25). `POWER4-d2true` was
  authored 2026-09-04 from verified claims in `digest/episode-draft-bank.md`;
  `POWER4-system-microarchitecture` is the direct extraction. No two titles are identical, but
  **Block {DUP_A} (d2true, "Absolute binary-compatibility requirement...") and Block {DUP_B} (sys,
  "Maintain binary compatibility with prior PowerPC systems") are the same decision extracted twice.** A
  reviewer should reach compatible verdicts on both; divergence is a finding about the reviewer or
  about one of the two extractions.
- **Alpha 21264 blocks carry two 2026-09-08 corrections.** `SESSION-MEMORIAL-2026-09-08-REDTEAM-3.md`
  fixed `outcome` percentages in ep00 (`5%`→`90%`) and ep06 (`95%`→`85%`) against
  `sources/Alpha21264-pagemarked.txt`. These blocks render the corrected values. A reviewer
  objecting to either number is objecting to the source text.
- **Quote-completeness differs sharply by pool and will skew `quote_plausibility`.** J-v3's BUILD
  NOTE measured it: Alpha, Pentium 4 and POWER4-system stored quotes are 37–58-character
  **mid-phrase fragments**; POWER4-circuit and Niagara quotes are complete sentences. A fragment is
  a property of the extraction, **not** evidence the quote is fabricated. Expect
  `quote_plausibility` to be least reliable on blocks 01–07, 14–20 and 35–42.
- **`direction_check` can be graded against each model's own prior recall.** All 13 panel models
  answered PROMPT-L/M/N/O/P on 2026-08-31 (Day 1) and the five D2-* prompts (Day 4) on the same five
  papers. A model contradicting its own recall is a stronger signal than one contradicting an
  unaided judgment.

---

"""

open(OUT_RUN, "w", encoding="utf-8", newline="").write(HDR + "\n".join(blocks))
print(f"RUNSHEET-42.md : {n} blocks, {checked} JSON fences, all verified against source")
print(f"                 citation style verified identical to J-v3's own PAPER line")
print(f"                 quotes wrap-collapsed: {len(unwrapped)} of {n} (words unchanged, checked)")
print(f"                 quotes still holding control chars: {ctrl or 'none'}")
print(f"                 {os.path.getsize(OUT_RUN)} bytes")

# ---------------------------------------------------------------- tally --------
T = f"""# TALLY-42 — red-team verdicts against `prompts/J-EPISODE-REDTEAM-V3.md`

Companion to `RUNSHEET-42.md` ({n} blocks). One copy of the block table per model run. Every column
maps to exactly one key in J-v3's returned JSON object.

## Column coding

| Column | From JSON key | Codes |
|---|---|---|
| `Verdict` | `verdict` | `SOUND` · `S-W-RES` (SOUND-WITH-RESERVATIONS) · `SUSPECT` · `IMPLAUS` (IMPLAUSIBLE-FOR-THIS-PAPER) |
| `Fatal` / `Major` | count of `objections[].severity` | integer |
| `Dir` | `direction_check` | `MATCHES` · `REVERSAL` · `TRANSPLANT` (reads as general knowledge, not this paper) · `N-J` (cannot-judge-without-the-paper) |
| `Quote` | `quote_plausibility` | `PAPER-LIKE` · `PARAPHRASE` (dressed as a quote) · `FRAGMENT` (mid-phrase, judgment withheld) · `N-J` |

`N-J` is a **pass**, not a gap: J-v3 instructs a field-level escape over a guessed objection, and
states plainly that the reviewer does not have the paper. Scoring `N-J` as a miss pushes models back
toward guessing, which is the behaviour the prompt suppresses.

**`REVERSAL` is the headline signal.** J-v3's parent prompt family calls a reversed decision
direction the single worst possible output. Any `Dir = REVERSAL` should be escalated to source
before anything else in the run is read.

**Expect `Quote = FRAGMENT` on blocks 01–07, 14–20, 35–42.** Those pools store 37–58-character
mid-phrase quotes. That is an extraction property, not a fabrication signal — a model reporting
`PARAPHRASE` across a whole pool is describing the extraction method, not a defect.

**Block {exemplar_block} is a calibration check, not evidence** — it is J-v3's own exemplar, declared
known-sound. Bare `SOUND` there is expected; many fatal objections there means miscalibrated.

---

## Block table — model: ________________  date: __________

| # | Paper | Title | Verdict | Fatal | Major | Dir | Quote | Note |
|---|---|---|---|---|---|---|---|---|
"""
TR = 54
lines = []
for num, title, label, stem, i in rows:
    t = title if len(title) <= TR else title[:TR - 1].rstrip() + "…"
    lines.append(f"| {num:02d} | {label} | {t.replace('|', chr(92)+'|')} |  |  |  |  |  |  |")

TAIL = f"""

## Per-model summary (one row per model run)

| Model | Date | SOUND | S-W-RES | SUSPECT | IMPLAUS | Blk {exemplar_block} calibration | REVERSAL blocks | Survivors first |
|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  | pass / miscalibrated |  |  |

`Survivors first` = blocks left standing with no fatal objection, in the order you would send them
to expert review.

## Cross-model rollup

| # | Runs | Worst verdict | Fatal across models | Consensus defect | Ready for expert review? |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

Two consistency checks this pool supports for free:

1. **Blocks {DUP_A} and {DUP_B} are the same decision** (POWER4 binary compatibility) extracted into two
   files. Verdicts should be compatible; divergence is a finding.
2. **`direction_check` vs the model's own prior recall.** Every panel model answered PROMPT-L/M/N/O/P
   (Day 1) and the D2-* recall prompts (Day 4) on these same five papers. A model whose
   `direction_check` here contradicts its own earlier recall is the sharpest available signal.
"""

open(OUT_TAL, "w", encoding="utf-8", newline="").write(T + "\n".join(lines) + TAIL)
print(f"TALLY-42.md    : {len(lines)} block rows, {os.path.getsize(OUT_TAL)} bytes")
