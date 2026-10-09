"""Day 3 corpus loader. Records EXACTLY how each file parses:
   clean | salvaged:<technique> | FAILED, with byte offset of the break.
No inference: a file that will not parse is reported, never guessed at."""
import json, re, os, sys, glob
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = r"C:\dev\Claude\Projects\ASIC\Web Model Tasks\Day 3"
FAMS = ["aprc", "boundary", "power4", "library", "patterns"]
DEC = json.JSONDecoder()


def strip_fence(raw):
    s = re.sub(r'^\s*```(?:json|JSON)?\s*', '', raw)
    return re.sub(r'\s*```\s*$', '', s.strip())


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


def fix_bad_escapes(raw):
    """Repair invalid JSON escapes like \\ldots, \\. , \\a  -> escape the backslash."""
    return re.sub(r'\\(?![\\"/bfnrtu])', r'\\\\', raw)


def unescaped_inner_quotes(raw):
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
    """Truncated array: re-parse element by element, keep what completes."""
    if not body.lstrip().startswith("["):
        return None
    s = body.lstrip()[1:]
    items, pos = [], 0
    while True:
        s2 = s[pos:].lstrip()
        if not s2 or s2[0] in "]":
            break
        try:
            o, e = DEC.raw_decode(s[pos:].lstrip())
        except json.JSONDecodeError:
            break
        items.append(o)
        pos = pos + (len(s[pos:]) - len(s[pos:].lstrip())) + e
        s3 = s[pos:].lstrip()
        if s3.startswith(","):
            pos = pos + (len(s[pos:]) - len(s[pos:].lstrip())) + 1
        else:
            break
    return items or None


TECHNIQUES = [
    ("clean", lambda s: s),
    ("fence-strip", strip_fence),
    ("bad-escape-repair", lambda s: fix_bad_escapes(strip_fence(s))),
    ("raw-newline-escape", lambda s: escape_raw_newlines(strip_fence(s))),
    ("inner-quote-repair", lambda s: unescaped_inner_quotes(strip_fence(s))),
    ("pair-in-array", lambda s: pair_in_array(strip_fence(s))),
    ("combined", lambda s: pair_in_array(escape_raw_newlines(fix_bad_escapes(strip_fence(s))))),
]


def load(path):
    raw = open(path, encoding="utf-8-sig").read()
    rec = {"bytes": len(raw.encode("utf-8")), "chars": len(raw)}
    for name, fix in TECHNIQUES:
        try:
            body = fix(raw)
        except Exception:
            continue
        idx = [x for x in (body.find("{"), body.find("[")) if x >= 0]
        if not idx:
            continue
        i = min(idx)
        try:
            obj, end = DEC.raw_decode(body[i:])
        except json.JSONDecodeError:
            continue
        trail = body[i + end:].strip()
        rec.update({"parse": name, "data": obj, "trailing": trail,
                    "leading": body[:i].strip()})
        return rec
    # last resort: element-wise on a truncated array
    body = fix_bad_escapes(strip_fence(raw))
    i = body.find("[")
    if i >= 0:
        items = elementwise(body[i:])
        if items:
            rec.update({"parse": "elementwise-truncation", "data": items,
                        "trailing": "", "leading": body[:i].strip()})
            return rec
    try:
        json.loads(raw)
    except json.JSONDecodeError as e:
        rec.update({"parse": "FAILED", "error": f"{e.msg} at line {e.lineno} col {e.colno} (char {e.pos})",
                    "context": raw[max(0, e.pos - 90):e.pos + 60], "data": None})
    return rec


if __name__ == "__main__":
    corpus = {}
    for p in sorted(glob.glob(os.path.join(BASE, "*.json"))):
        base = os.path.basename(p)
        if base.startswith("_") or base == "dispatch-state.json":
            continue
        stem = base[:-5]
        fam = stem.rsplit(" ", 1)[-1]
        model = stem[: -(len(fam) + 1)]
        if fam not in FAMS:
            print("SKIP unrecognised family:", base); continue
        rec = load(p)
        rec["file"] = base
        rec["model"] = model
        rec["family"] = fam
        corpus[f"{model}|{fam}"] = rec
    print(f"{'file':34}{'family':10}{'parse':26}{'bytes':>8}  trailing/leading")
    for k in sorted(corpus, key=lambda x: (corpus[x]["family"], corpus[x]["model"])):
        r = corpus[k]
        extra = ""
        if r["parse"] == "FAILED":
            extra = "  ERROR: " + r["error"]
        else:
            if r.get("leading"):
                extra += f"  LEAD:{r['leading'][:40]!r}"
            if r.get("trailing"):
                extra += f"  TRAIL:{r['trailing'][:40]!r}"
        print(f"{r['file']:34}{r['family']:10}{r['parse']:26}{r['bytes']:>8}{extra}")
    json.dump({k: {kk: vv for kk, vv in v.items()} for k, v in corpus.items()},
              open("corpus.json", "w", encoding="utf-8"), ensure_ascii=False)
    print("\nloaded", len(corpus), "files")
