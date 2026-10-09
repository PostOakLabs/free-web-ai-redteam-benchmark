import json, os, re, glob
from collections import Counter

ROOT = r"C:\dev\Claude\Projects\ASIC\Web Model Tasks"
OUT = os.path.dirname(os.path.abspath(__file__))
DEC = json.JSONDecoder()

def strip_fences(t):
    t = re.sub(r"```[a-zA-Z0-9_-]*\n", "\n", t)
    return t.replace("```", "\n")

def harvest_objects(text):
    """Walk the text pulling every top-level-ish JSON object/array we can decode.
    Handles truncation: an unparseable tail is simply skipped, earlier elements kept."""
    out = []
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch not in "[{":
            i += 1
            continue
        try:
            val, end = DEC.raw_decode(text, i)
            out.append(val)
            i = end
            continue
        except Exception:
            pass
        if ch == "[":
            # truncated array: decode its elements one by one
            j = i + 1
            got = 0
            while j < n:
                while j < n and text[j] in " \t\r\n,":
                    j += 1
                if j >= n or text[j] == "]":
                    break
                try:
                    val, end = DEC.raw_decode(text, j)
                    out.append(val)
                    got += 1
                    j = end
                except Exception:
                    break
            if got:
                i = j
                continue
        i += 1
    return out

def flatten(vals):
    items = []
    for v in vals:
        if isinstance(v, list):
            items.extend(x for x in v if isinstance(x, dict))
        elif isinstance(v, dict):
            pulled = False
            for k, vv in v.items():
                if isinstance(vv, list) and vv and isinstance(vv[0], dict):
                    for x in vv:
                        if isinstance(x, dict):
                            x = dict(x); x["_wrapper_key"] = k
                            items.append(x)
                    pulled = True
            if not pulled:
                items.append(v)
    seen, uniq = set(), []
    for it in items:
        k = json.dumps(it, sort_keys=True, ensure_ascii=False)[:6000]
        if k in seen: continue
        seen.add(k); uniq.append(it)
    return uniq

def slice_of(fn):
    f = fn.lower()
    if " d2." in f: return "D2"
    if f.endswith(" f.json"): return "F"
    if f.endswith(" g.json"): return "G"
    if f.endswith(" h.json"): return "H"
    if f.endswith(" i.json"): return "I"
    if f.endswith(" j.json"): return "J"
    if f.endswith(" k.json"): return "K"
    if f.endswith(" l.json"): return "L"
    if f.endswith(" m.json"): return "M"
    if f.endswith(" n.json"): return "N"
    if f.endswith(" o.json"): return "O"
    if f.endswith(" p.json"): return "P"
    if f.endswith(" q.json"): return "Q"
    if f.endswith(" s.json"): return "S"
    if f.endswith(" t.json"): return "T"
    if "prompt 2" in f: return "R2"
    if "prompt 3" in f: return "D1"
    if "prompt 4" in f: return "E"
    if "august" in f: return "R1"
    if "deep-research-report" in f or f.startswith("qwen deconstructing"): return "D1"
    return "OTHER"

def model_of(fn):
    b = re.sub(r"\.(json|md)$", "", os.path.basename(fn), flags=re.I)
    for suf in [" d2"," f"," g"," h"," i"," j"," k"," l"," m"," n"," o"," p"," q"," s"," t"," prompt 2"," prompt 3"," prompt 4",
                " free asic task august"," instant free asic task august",
                " free asic august"," asic free task august"," asic august",
                " json august"]:
        if b.lower().endswith(suf):
            return b[:len(b)-len(suf)].strip()
    if b.lower().startswith("qwen "): return "qwen"
    if b.lower().startswith("deep-research-report"): return "deep-research-report"
    return b.strip()

report, store = [], {}
for path in sorted(glob.glob(os.path.join(ROOT, "*"))):
    fn = os.path.basename(path)
    if fn.lower().startswith("log-"): continue
    raw = open(path, encoding="utf-8", errors="replace").read()
    txt = strip_fences(raw)
    vals = harvest_objects(txt)
    items = flatten(vals)
    covered = sum(len(json.dumps(v, ensure_ascii=False)) for v in vals)
    sl, md = slice_of(fn), model_of(fn)
    store.setdefault(sl, []).append({"file": fn, "model": md, "items": items})
    report.append({"file": fn, "slice": sl, "model": md, "bytes": len(raw),
                   "items": len(items), "json_cover_pct": round(100*covered/max(1,len(raw))),
                   "status": "OK" if items else "PROSE-ONLY"})

json.dump(store, open(os.path.join(OUT,"store.json"),"w",encoding="utf-8"), indent=1, ensure_ascii=False)
json.dump(report, open(os.path.join(OUT,"report.json"),"w",encoding="utf-8"), indent=1, ensure_ascii=False)
for r in sorted(report, key=lambda x:(x["slice"],x["model"])):
    print(f"{r['slice']:5} {r['model']:22} {r['items']:4} items cover={r['json_cover_pct']:3}% {r['status']:10} {r['file']}")
c, n = Counter(), Counter()
for r in report: c[r["slice"]]+=1; n[r["slice"]]+=r["items"]
print("\nBY SLICE:", {k:(c[k],n[k]) for k in sorted(c)})
print("TOTAL files", len(report), "items", sum(n.values()))
