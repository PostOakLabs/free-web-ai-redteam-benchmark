import json, re, sys
from collections import defaultdict
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
S = json.load(open("day2.json", encoding="utf-8"))

def num(v):
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        m = re.search(r"[\d.]+", v)
        if m:
            return float(m.group())
    return None

def solve(entities, edges):
    """OFAC 50% Rule: blocked seeds; an entity becomes blocked when blocked owners
    hold >=50% in aggregate; a blocked entity's holdings are attributed IN FULL."""
    blocked = {e["id"] for e in entities if e.get("blocked")}
    out = defaultdict(list)
    for e in edges:
        out[e["from"]].append((e["to"], num(e["pct"])))
    changed = True
    agg = {}
    while changed:
        changed = False
        agg = defaultdict(float)
        for src, lst in out.items():
            if src in blocked:
                for dst, pct in lst:
                    if pct is not None:
                        agg[dst] += pct
        for node, tot in agg.items():
            if tot >= 50 - 1e-9 and node not in blocked:
                blocked.add(node)
                changed = True
    return blocked, dict(agg)

def solve_mult(entities, edges):
    """The WRONG-but-common treatment: multiply percentages along paths."""
    seeds = {e["id"] for e in entities if e.get("blocked")}
    out = defaultdict(list)
    nodes = {e["id"] for e in entities}
    for e in edges:
        out[e["from"]].append((e["to"], num(e["pct"])))
    res = defaultdict(float)
    def walk(cur, frac, seen, root):
        for dst, pct in out.get(cur, []):
            if pct is None or dst in seen:
                continue
            f = frac * pct / 100.0
            res[dst] += f * 100 if cur == root or True else 0
            walk(dst, f, seen | {dst}, root)
    for s in seeds:
        walk(s, 1.0, {s}, s)
    return dict(res)

for key, rec in sorted(S.items()):
    model, prompt = key.split("|")
    if prompt != "ofac":
        continue
    d = rec["data"]
    if not isinstance(d, list):
        d = [d]
    print(f"\n{'='*95}\n### {model}   ({len(d)} cases)")
    for c in d:
        if not isinstance(c, dict):
            continue
        ents, edges = c.get("entities") or [], c.get("edges") or []
        ents = [e for e in ents if isinstance(e, dict) and "id" in e]
        edges = [e for e in edges if isinstance(e, dict) and "from" in e and "to" in e]
        if not ents or not edges:
            print(f"\n  [{str(c.get('case_name'))[:50]}] -- unparseable graph")
            continue
        b, agg = solve(ents, edges)
        m = solve_mult(ents, edges)
        seeds = {e["id"] for e in ents if e.get("blocked")}
        derived = sorted(b - seeds)
        print(f"\n  [{str(c.get('case_name'))[:56]}]")
        print(f"    seeds={sorted(seeds)}  ATTRIBUTION-derived blocked={derived}")
        print(f"    aggregate% (attribution): { {k: round(v,2) for k,v in sorted(agg.items())} }")
        print(f"    aggregate% (multiplicative): { {k: round(v,2) for k,v in sorted(m.items())} }")
        print(f"    MODEL SAYS: {str(c.get('blocked_verdicts'))[:230]}")
