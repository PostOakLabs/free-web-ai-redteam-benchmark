"""Per-family schema inventory: shape, item counts, key frequency, ABSENT map."""
import json, sys, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
C = json.load(open("corpus.json", encoding="utf-8"))
FAMS = ["aprc", "boundary", "power4", "library", "patterns"]


def items_of(d):
    """Normalise a response to a list of case/entry objects + a trailer dict."""
    if d is None:
        return [], {}
    if isinstance(d, dict):
        # a wrapper object: find the single list value if there is one
        lists = [(k, v) for k, v in d.items() if isinstance(v, list)]
        if len(lists) == 1 and len(lists[0][1]) > 1:
            return lists[0][1], {k: v for k, v in d.items() if k != lists[0][0]}
        return [d], {}
    out, trail = [], {}
    for x in d:
        if isinstance(x, dict) and set(x) <= {"weakest_point", "note", "notes"}:
            trail.update(x)
        else:
            out.append(x)
    return out, trail


for fam in FAMS:
    keys = [k for k in C if C[k]["family"] == fam]
    print("=" * 100)
    print(f"FAMILY: {fam}   files: {len(keys)}")
    print("=" * 100)
    keyfreq = collections.Counter()
    shapes = {}
    for k in sorted(keys):
        r = C[k]
        d = r.get("data")
        its, trail = items_of(d)
        top = ("dict:" + ",".join(list(d)[:6])) if isinstance(d, dict) else \
              ("list" if isinstance(d, list) else "NONE")
        ks = set()
        for it in its:
            if isinstance(it, dict):
                ks |= set(it)
        keyfreq.update(ks)
        shapes[r["model"]] = (len(its), ks, trail, top, r["parse"])
        print(f"  {r['model']:16} parse={r['parse']:22} items={len(its):3} "
              f"top={top[:44]:46} trailer={list(trail) if trail else '-'}")
    print(f"\n  ITEM-KEY FREQUENCY across {len(keys)} files:")
    for kk, n in keyfreq.most_common():
        holders = sorted(m for m, (c, ks, t, tp, p) in shapes.items() if kk in ks)
        miss = sorted(m for m in shapes if kk not in shapes[m][1])
        line = f"    {n:3}/{len(keys)}  {kk:34}"
        if n < len(keys):
            line += "  ABSENT in: " + ", ".join(miss)
        print(line)
    print()
