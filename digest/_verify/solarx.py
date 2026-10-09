"""Cross-add: recompute solar trid + solar ofac against the rules adjudicated
in day2-c1-adjudication.md (aggregate 10% test; full-attribution fixpoint)."""
import json, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
S = json.load(open("day2b.json", encoding="utf-8"))

print("=" * 78)
print("SOLAR TRID — zero-tolerance per-item, 10% AGGREGATE bucket")
print("=" * 78)
for c in S["solar|trid"]["data"]:
    fees = c["fees"]
    zt = [f for f in fees if f["bucket"] == "zero_tolerance"]
    tp = [f for f in fees if f["bucket"] == "ten_pct_aggregate"]
    zcure = sum(max(0.0, f["cd_amount"] - f["le_amount"]) for f in zt)
    le = sum(f["le_amount"] for f in tp)
    cd = sum(f["cd_amount"] for f in tp)
    thr = le * 0.10
    excess = max(0.0, (cd - le) - thr)
    sum_inc = sum(max(0.0, f["cd_amount"] - f["le_amount"]) for f in tp)
    print(f"\n{c['case_name'][:74]}")
    print(f"  zero-tol cure   = {zcure:.2f}")
    print(f"  10% SigmaLE={le:.2f}  SigmaCD={cd:.2f}  delta={cd-le:+.2f}  thr={thr:.2f}"
          f"  excess-cure={excess:.2f}   (sum-of-increases would be {sum_inc:.2f})")
    txt = (c.get("computation") or "") + " " + str(c.get("violations", "")) + " " + \
          str(c.get("cure_amounts", "")) + " " + json.dumps(c, ensure_ascii=False)
    for label, val in (("SigmaLE", le), ("SigmaCD", cd), ("thr", thr),
                       ("excess", excess), ("zcure", zcure)):
        s = f"{val:,.2f}"
        print(f"     {label:8} {s:>12}  stated-in-file: {'YES' if s in txt else 'no'}")

print("\n" + "=" * 78)
print("SOLAR OFAC — full-attribution fixpoint vs multiplicative")
print("=" * 78)


def fixpoint(ents, edges):
    blocked = {e["id"] for e in ents if e.get("blocked")}
    while True:
        grew = False
        for e in ents:
            t = e["id"]
            if t in blocked:
                continue
            agg = sum(x["pct"] for x in edges if x["to"] == t and x["from"] in blocked)
            if agg >= 50:
                blocked.add(t)
                grew = True
        if not grew:
            return blocked


def agg_for(t, blocked, edges):
    return sum(x["pct"] for x in edges if x["to"] == t and x["from"] in blocked)


for c in S["solar|ofac"]["data"]:
    ents, edges = c["entities"], c["edges"]
    b = fixpoint(ents, edges)
    seeds = {e["id"] for e in ents if e.get("blocked")}
    derived = sorted(b - seeds)
    print(f"\n{c['case_name'][:74]}")
    print(f"  seeds={sorted(seeds)}  derived-blocked={derived}")
    for e in ents:
        t = e["id"]
        if t in seeds:
            continue
        print(f"    {t}: aggregate blocked ownership = {agg_for(t, b, edges)}%"
              f"  -> {'BLOCKED' if t in b else 'not blocked'}")
    print(f"  stated: {str(c.get('blocked_verdicts'))[:150]}")
