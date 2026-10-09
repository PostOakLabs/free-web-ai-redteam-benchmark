"""d4grade.py — four-tier recall grading against the pagemarked papers
(DIGEST-COMMISSION-DAY4-1 sections 2.2 / 2.3 / 2.4, addendum).

Tiers:
  T1 verbatim              normalised quote is a substring of the normalised source
  T2 paraphrase-consistent high content-word overlap with a located source window
  T3 contradicts-paper     located, but a numeric/directional token disagrees   [CANDIDATE]
  T4 not-found-in-paper    no window clears the overlap floor after normalisation

NORMALISATION (commission 2.2, addendum: verified estate policy, proven on RUNSHEET-42's
18 quotes): strip hyphenation at line wraps, THEN collapse all whitespace, THEN casefold.
The paper reads `deliver best-of-<wrap>breed`; a raw grep for `best-of-breed` returns 0 and
would emit a false T4 on a real quote. T4 is only assertable after this normalisation.

T3 is emitted as a CANDIDATE only. Commission section 4 keeps the rule that failures are
reported when hand-confirmed; the checker proposes, the digest author adjudicates.

Usage:  python d4grade.py    -> d4run/grade-*.txt, d4run/d4grades.json
"""
import json, os, re, sys, unicodedata, difflib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ASIC = r"C:\dev\Claude\Projects\ASIC"
OUT = os.path.join(ASIC, "digest", "_verify", "d4run")
SRC = os.path.join(ASIC, "sources")

T2_FLOOR = 0.60          # content-word overlap to call a window "located"
WINDOW = 400             # chars of source window scored around a candidate anchor

STOP = set("""a an the and or of to in for on with by is are was were be been that this it its as at
from into than then so such not no nor but if we our their they he she his her which who whom whose
can could may might must shall should will would do does did done have has had having more most
other some any each both few all every one two three""".split())


def denorm(t):
    """Wrap-and-hyphen collapse + whitespace collapse + casefold."""
    t = unicodedata.normalize("NFKC", t)
    t = t.replace("\u00ad", "")                     # soft hyphen
    t = re.sub(r"[\u2010-\u2015]", "-", t)          # unicode dashes -> ascii hyphen
    t = re.sub(r"-[ \t]*[\r\n]+[ \t]*", "", t)      # hyphen AT a line wrap: join the word
    t = re.sub(r"[\r\n\t]+", " ", t)                # remaining line breaks -> space
    t = re.sub(r"[^\S\n]+", " ", t)                 # collapse runs of spaces
    t = re.sub(r"\s+", " ", t)
    return t.strip().casefold()


def words(t):
    return [w for w in re.findall(r"[a-z0-9]+(?:\.[0-9]+)?", t) if w not in STOP and len(w) > 1]


def nums(t):
    return re.findall(r"\d+(?:\.\d+)?\s*(?:%|percent|ghz|mhz|kb|mb|gb|w|mm|nm|ns|ps)?", t)


def dehyphen(t):
    """Remove ALL hyphens, not only wrap hyphens. Used ONLY as a rescue pass after a
    primary miss, never as the primary comparison, so it cannot manufacture matches
    between genuinely different words.
    Price: the Pentium 4 paper writes `8k-byte`; a model wrote `8Kbyte`. Wrap-hyphen
    collapse alone left that a false T3/T4 -- the same false-negative class the
    commission's 2.2 exists to prevent, one level in from `best-of-<wrap>breed`."""
    return re.sub(r"-", "", t)


def load_source(fn):
    raw = open(os.path.join(SRC, fn), encoding="utf-8", errors="replace").read()
    pages = []
    for m in re.finditer(r"===PDF PAGE (\d+)===", raw):
        pages.append((int(m.group(1)), m.start()))
    n = denorm(raw)
    return raw, n, pages, dehyphen(n)


def page_of(raw, pos_in_norm, norm, pages):
    """Approximate the PDF page for a normalised offset by proportional mapping."""
    if not pages or not norm:
        return None
    frac = pos_in_norm / max(1, len(norm))
    target = frac * len(raw)
    best = pages[0][0]
    for pg, off in pages:
        if off <= target:
            best = pg
        else:
            break
    return best


def grade_quote(q, raw, norm, pages, nohy):
    """Return (tier, evidence dict)."""
    if not isinstance(q, str) or not q.strip():
        return "T0-absent", {}
    if q.strip() == "cannot-reproduce-verbatim":
        return "T0-declined", {}
    nq = denorm(q)
    if len(nq) < 12:
        return "T0-too-short", {"norm": nq}
    idx = norm.find(nq)
    if idx >= 0:
        return "T1-verbatim", {"page": page_of(raw, idx, norm, pages), "norm": nq}
    # rescue pass: hyphen-insensitive. Recorded as its own tier so the count of
    # true byte-verbatim matches stays honest.
    idx2 = nohy.find(dehyphen(nq))
    if idx2 >= 0:
        return "T1-verbatim-hyphen-variant", {
            "page": page_of(raw, idx2, nohy, pages), "norm": nq,
            "note": "matches source only after removing in-word hyphens"}
    qw = words(nq)
    if not qw:
        return "T4-not-found", {"norm": nq, "reason": "no content words"}
    # locate the best window by content-word density
    best = (0.0, -1)
    step = 120
    for s in range(0, max(1, len(norm) - WINDOW), step):
        w = norm[s:s + WINDOW]
        ww = set(words(w))
        if not ww:
            continue
        ov = sum(1 for x in qw if x in ww) / len(qw)
        if ov > best[0]:
            best = (ov, s)
    ov, s = best
    if ov < T2_FLOOR:
        return "T4-not-found", {"norm": nq, "best_overlap": round(ov, 3)}
    win = norm[s:s + WINDOW]
    qn, wn = nums(nq), nums(win)
    missing_nums = [x for x in qn if x.replace(" ", "") not in
                    [y.replace(" ", "") for y in wn]]
    ev = {"page": page_of(raw, s, norm, pages), "overlap": round(ov, 3),
          "window": win[:300], "norm": nq}
    if missing_nums:
        ev["numeric_tokens_not_in_window"] = missing_nums
        return "T3-contradicts-CANDIDATE", ev
    return "T2-paraphrase-consistent", ev


def main():
    C = json.load(open(os.path.join(OUT, "d4corpus.json"), encoding="utf-8"))
    srcs, grades = {}, {}
    tally = {}
    lines = []
    for key in sorted(C):
        r = C[key]
        gt = r.get("ground_truth")
        if not gt or not isinstance(r.get("data"), list):
            continue
        if gt not in srcs:
            srcs[gt] = load_source(gt)
        raw, norm, pages, nohy = srcs[gt]
        fam, model = r["family"], r["model"]
        lines.append(f"\n### {model} | {fam}  ({r['file']}, parse={r['parse']})")
        per = []
        for i, e in enumerate(r["data"]):
            if not isinstance(e, dict):
                continue
            q = e.get("quote_as_recalled", e.get("quote_as_recall_verbatim"))
            tier, ev = grade_quote(q, raw, norm, pages, nohy)
            pg = e.get("page_guess")
            per.append({"i": i, "title": str(e.get("title"))[:70], "tier": tier,
                        "page_guess": pg, "page_found": ev.get("page"),
                        "overlap": ev.get("overlap"), "confidence": e.get("confidence"),
                        "paper_vs_general": e.get("paper_vs_general"),
                        "not_in_paper": e.get("not_in_paper"),
                        "numeric_flags": ev.get("numeric_tokens_not_in_window")})
            tally[tier] = tally.get(tier, 0) + 1
            pgs = f"guess={pg} found={ev.get('page')}" if ev.get("page") else f"guess={pg}"
            lines.append(f"   [{i}] {tier:26} {pgs:22} {str(e.get('title'))[:56]}")
            if tier.startswith("T3"):
                lines.append(f"        numeric not in window: {ev['numeric_tokens_not_in_window']}")
                lines.append(f"        quote : {ev['norm'][:150]}")
                lines.append(f"        window: {ev['window'][:150]}")
        grades[key] = {"model": model, "family": fam, "file": r["file"],
                       "ground_truth": gt, "entries": per}
    txt = "\n".join(lines)
    open(os.path.join(OUT, "grade-detail.txt"), "w", encoding="utf-8").write(txt)
    json.dump(grades, open(os.path.join(OUT, "d4grades.json"), "w", encoding="utf-8"),
              ensure_ascii=False, sort_keys=True, indent=1)
    summ = ["TIER TALLY (quote_as_recalled, all paper families)"]
    for t in sorted(tally):
        summ.append(f"  {t:28} {tally[t]}")
    summ.append(f"  {'TOTAL':28} {sum(tally.values())}")
    s = "\n".join(summ)
    open(os.path.join(OUT, "grade-summary.txt"), "w", encoding="utf-8").write(s)
    print(s)


if __name__ == "__main__":
    main()
