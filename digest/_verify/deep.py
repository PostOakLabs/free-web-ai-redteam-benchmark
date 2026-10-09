"""Nested-key inventory + the specific anomalies flagged by schema.py."""
import json, sys, collections, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
C = json.load(open("corpus.json", encoding="utf-8"))


def items_of(d):
    if d is None:
        return [], {}
    if isinstance(d, dict):
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


def paths(o, pre=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from paths(v, f"{pre}.{k}" if pre else k)
    elif isinstance(o, list):
        for v in o:
            yield from paths(v, pre + "[]")
    else:
        yield pre


for fam in ("library", "patterns", "power4"):
    ks = sorted(k for k in C if C[k]["family"] == fam)
    print("=" * 96)
    print("NESTED PATH INVENTORY —", fam)
    print("=" * 96)
    freq = collections.Counter()
    per = {}
    for k in ks:
        its, _ = items_of(C[k].get("data"))
        s = set()
        for it in its:
            s |= {p for p in paths(it)}
        per[C[k]["model"]] = s
        freq.update(s)
    for p, n in freq.most_common(40):
        if n == len(ks):
            print(f"  {n:3}/{len(ks)}  {p}")
        else:
            miss = sorted(m for m in per if p not in per[m])
            print(f"  {n:3}/{len(ks)}  {p:52} ABSENT: {', '.join(miss)}")
    print()

print("=" * 96)
print("ANOMALY 1 — minimax 2.7 power4: schema")
print("=" * 96)
d = C["minimax 2.7|power4"]["data"]
print(json.dumps(d, ensure_ascii=False)[:1800])

print("\n" + "=" * 96)
print("ANOMALY 2 — library node_era key spelling variants")
print("=" * 96)
for k in sorted(x for x in C if C[x]["family"] == "library"):
    its, _ = items_of(C[k].get("data"))
    odd = set()
    for it in its:
        if isinstance(it, dict):
            odd |= {kk for kk in it if "era" in kk.lower() and kk != "node_era_note"}
    if odd:
        print(f"  {C[k]['model']:16} odd keys: {sorted(odd)}")

print("\n" + "=" * 96)
print("ANOMALY 3 — cross-family field leakage into library")
print("=" * 96)
for k in sorted(x for x in C if C[x]["family"] == "library"):
    its, _ = items_of(C[k].get("data"))
    leak = set()
    for it in its:
        if isinstance(it, dict):
            leak |= {kk for kk in it if kk in ("not_in_paper", "paper_vs_general",
                                               "weakest_point", "page_guess",
                                               "quote_as_recalled")}
    if leak:
        print(f"  {C[k]['model']:16} carries: {sorted(leak)}")

print("\n" + "=" * 96)
print("ANOMALY 4 — power4: which paper? page_guess ranges + where_in_paper")
print("=" * 96)
for k in sorted(x for x in C if C[x]["family"] == "power4"):
    its, _ = items_of(C[k].get("data"))
    pg = [it.get("page_guess") for it in its if isinstance(it, dict)]
    pgn = [p for p in pg if isinstance(p, (int, float))]
    where = [str(it.get("where_in_paper"))[:40] for it in its if isinstance(it, dict)]
    rng = f"{min(pgn)}-{max(pgn)}" if pgn else "none-numeric"
    print(f"  {C[k]['model']:16} page_guess={pg}  range={rng}")
    print(f"       where: {where}")
