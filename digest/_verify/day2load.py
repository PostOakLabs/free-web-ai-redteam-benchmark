"""day2load.py — rebuild the Day-2 corpora the adjudications were computed from.

WHY THIS EXISTS: during the original session `day2.json` (batch 1) and `day2b.json`
(batch 2) were built by inline shell-python that was never saved. Every other analyser
in this directory reads one of those two files, so without this script the Day-2
results are not reproducible from the preserved tooling. This script closes that gap.
It was written AFTER the fact and is verified by reproducing the counts and headline
numbers quoted in digest/day2-c1-adjudication.md and digest/day2-c1b-c2-adjudication.md.

Salvage ladder is identical in behaviour to the one described in those documents:
  1 clean parse
  2 markdown fence strip
  3 invalid-escape repair          (a stray \\ldots broke a whole file)
  4 raw-newline escape             (literal LF inside a string value)
  5 unescaped inner-quote repair   (chatgpt jcs: "{"n":-0}")
  6 pair-in-array repair           (a "k": "v" pair sitting inside an array)
  7 trailing-content tolerance     (raw_decode from the first bracket; meta's "[2]")
  8 element-wise truncation        (keep the elements that completed)

CONTENT IS NEVER REPAIRED. A file that will not yield structure is recorded FAILED.

Usage:
    python day2load.py              # writes day2.json + day2b.json next to this file
    python day2load.py --report     # also prints the per-file parse table
"""
import json, os, re, sys, glob

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = r"C:\dev\Claude\Projects\ASIC\Web Model Tasks\Day 2"
OUT = os.path.dirname(os.path.abspath(__file__))
DEC = json.JSONDecoder()

BATCH1 = ("globe", "appj", "trid", "ofac")
BATCH2 = ("irb", "frtb", "mica", "ccd2", "receipt", "jcs")


def strip_fence(raw):
    s = re.sub(r"^\s*```(?:json|JSON)?\s*", "", raw)
    return re.sub(r"\s*```\s*$", "", s.strip())


def fix_bad_escapes(raw):
    return re.sub(r'\\(?![\\"/bfnrtu])', r"\\\\", raw)


def escape_raw_newlines(raw):
    out, in_str, esc = [], False, False
    for ch in raw:
        if esc:
            out.append(ch); esc = False; continue
        if ch == chr(92) and in_str:
            out.append(ch); esc = True; continue
        if ch == '"':
            in_str = not in_str; out.append(ch); continue
        if in_str and ch in "\n\r":
            out.append(chr(92) + ("n" if ch == "\n" else "r")); continue
        out.append(ch)
    return "".join(out)


def inner_quote_repair(raw):
    BS = chr(92)
    out = []
    for ln in raw.split("\n"):
        m = re.match(r'^(\s*"[A-Za-z_0-9]+"\s*:\s*")(.*)("\s*,?\s*)$', ln)
        if m and '"' in m.group(2):
            h, v, t = m.groups()
            out.append(h + v.replace(BS, BS + BS).replace('"', BS + '"') + t)
        else:
            out.append(ln)
    return "\n".join(out)


def pair_in_array(raw):
    for _ in range(20):
        try:
            DEC.raw_decode(raw); return raw
        except json.JSONDecodeError as e:
            p = e.pos
            while p < len(raw) and raw[p] in " \t":
                p += 1
            if p >= len(raw) or raw[p] != ":":
                return raw
            q = raw.rfind('"', 0, e.pos)
            q = raw.rfind('"', 0, q)
            if q < 0:
                return raw
            raw = raw[:q] + raw[p + 1:].lstrip(" ")
    return raw


def elementwise(body):
    if not body.lstrip().startswith("["):
        return None
    s = body.lstrip()[1:]
    items, pos = [], 0
    while True:
        tail = s[pos:].lstrip()
        if not tail or tail[0] == "]":
            break
        try:
            o, e = DEC.raw_decode(tail)
        except json.JSONDecodeError:
            break
        items.append(o)
        pos += (len(s[pos:]) - len(s[pos:].lstrip())) + e
        nxt = s[pos:].lstrip()
        if nxt.startswith(","):
            pos += (len(s[pos:]) - len(s[pos:].lstrip())) + 1
        else:
            break
    return items or None


def harvest(text):
    """Forward scan: pull every decodable top-level-ish object out of the text.

    Needed when the defect sits INSIDE element 0, which kills elementwise() before it
    starts. Three real instances in Day 2, each a different corruption inside element 0:
      grok frtb.json        `"ES_multiplier": 0.05844 / 0.025,`  -- an unevaluated
                            arithmetic EXPRESSION where a JSON number belongs
      minimax m3 frtb.json  `"ES_unit_sigma_value": 2. "ES_to_VaR..."` -- token dropout,
                            value truncated and the separating comma lost
      minimax m3 mica.json  `"supply_value": 1000000.0,\\n 1020000.0,` -- a dropped KEY,
                            leaving a bare value inside an object
    Element 0 is UNRECOVERABLE in all three and is NOT reconstructed. The later elements
    are intact and are harvested. Same strategy as parse2.py's harvest_objects().
    """
    out, i, n = [], 0, len(text)
    while i < n:
        if text[i] not in "[{":
            i += 1
            continue
        try:
            val, end = DEC.raw_decode(text, i)
        except json.JSONDecodeError:
            i += 1
            continue
        if isinstance(val, dict) and val:
            out.append(val)
            i = end
        elif isinstance(val, list) and val:
            out.extend(x for x in val if isinstance(x, dict))
            i = end
        else:
            i += 1
    return out or None


LADDER = [
    ("clean", lambda s: s),
    ("fence-strip", strip_fence),
    ("bad-escape-repair", lambda s: fix_bad_escapes(strip_fence(s))),
    ("raw-newline-escape", lambda s: escape_raw_newlines(strip_fence(s))),
    ("inner-quote-repair", lambda s: inner_quote_repair(strip_fence(s))),
    ("pair-in-array", lambda s: pair_in_array(strip_fence(s))),
    ("combined", lambda s: pair_in_array(escape_raw_newlines(fix_bad_escapes(strip_fence(s))))),
]


def load_one(path):
    raw = open(path, encoding="utf-8-sig").read()
    for name, fix in LADDER:
        try:
            body = fix(raw)
        except Exception:
            continue
        idx = [x for x in (body.find("{"), body.find("[")) if x >= 0]
        if not idx:
            continue
        try:
            obj, end = DEC.raw_decode(body[idx[0]:] if len(idx) == 1 else body[min(idx):])
        except json.JSONDecodeError:
            continue
        i = min(idx)
        return {"data": obj, "parse": name, "trailing": body[i + end:].strip(),
                "leading": body[:i].strip(), "chars": len(raw)}
    body = fix_bad_escapes(strip_fence(raw))
    i = body.find("[")
    if i >= 0:
        items = elementwise(body[i:])
        if items:
            return {"data": items, "parse": "elementwise-truncation",
                    "trailing": "", "leading": body[:i].strip(), "chars": len(raw)}
    items = harvest(body)
    if items:
        return {"data": items, "parse": "harvest-skip-broken-element",
                "trailing": "", "leading": "", "chars": len(raw)}
    try:
        json.loads(raw)
    except json.JSONDecodeError as e:
        return {"data": None, "parse": "FAILED", "chars": len(raw),
                "error": f"{e.msg} at line {e.lineno} col {e.colno} (char {e.pos})"}
    return {"data": None, "parse": "FAILED", "chars": len(raw), "error": "unknown"}


def build(families):
    store = {}
    for p in sorted(glob.glob(os.path.join(BASE, "*.json"))):
        stem = os.path.basename(p)[:-5]
        fam = stem.rsplit(" ", 1)[-1]
        if fam not in families:
            continue
        model = stem[: -(len(fam) + 1)]
        rec = load_one(p)
        rec["file"] = os.path.basename(p)
        rec["model"] = model
        rec["prompt"] = fam
        store[f"{model}|{fam}"] = rec
    return store


if __name__ == "__main__":
    report = "--report" in sys.argv
    for fname, fams in (("day2.json", BATCH1), ("day2b.json", BATCH2)):
        st = build(fams)
        if fname == "day2b.json":
            # The batch-2 store also carried solar's TRID and OFAC files: those two
            # prompts belong to batch 1 by name, but solar answered them late and they
            # were cross-added to the batch-1 adjudication from inside the batch-2 pass
            # (day2-c1b-c2-adjudication.md section 8). solarx.py reads them from here,
            # so the rebuild reproduces that store rather than a tidier one.
            st.update({k: v for k, v in build(("trid", "ofac")).items()
                       if k.startswith("solar|")})
        json.dump(st, open(os.path.join(OUT, fname), "w", encoding="utf-8"),
                  ensure_ascii=False)
        clean = sum(1 for v in st.values() if v["parse"] == "clean")
        failed = [k for k, v in st.items() if v["parse"] == "FAILED"]
        salv = [(k, v["parse"]) for k, v in st.items()
                if v["parse"] not in ("clean", "FAILED")]
        print(f"{fname}: {len(st)} files  clean={clean}  salvaged={len(salv)}  FAILED={len(failed)}")
        if report:
            for k, v in sorted(st.items()):
                extra = ""
                if v.get("leading"):
                    extra += f"  LEAD:{v['leading'][:28]!r}"
                if v.get("trailing"):
                    extra += f"  TRAIL:{v['trailing'][:28]!r}"
                if v["parse"] == "FAILED":
                    extra = "  " + v.get("error", "")
                print(f"   {v['file']:34} {v['parse']:24}{extra}")
        elif salv or failed:
            for k, p in salv:
                print(f"   salvaged: {k}  [{p}]")
            for k in failed:
                print(f"   FAILED  : {k}")
    print("\nNOTE: resalv.py then patches day2b.json for the three receipt files that")
    print("      need trailing-content / pair-in-array / raw-newline salvage. Run it next:")
    print("      python resalv.py")
