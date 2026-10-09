"""Load-bearing cell extraction for aprc / power4 / library / patterns."""
import json, sys, re, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
C = json.load(open("corpus.json", encoding="utf-8"))


def lst(k):
    d = C[k].get("data")
    if d is None:
        return []
    if isinstance(d, dict):
        for v in d.values():
            if isinstance(v, list) and len(v) > 1:
                return v
        return [d]
    if len(d) == 1 and isinstance(d[0], list):      # double-wrapped (minimax 2.7 power4)
        return d[0]
    return [x for x in d if isinstance(x, dict) and "weakest_point" not in (set(x) - {"weakest_point"}) or len(x) > 1]


print("#" * 100)
print("# APRC — aprc_pct per case")
print("#" * 100)
tab = {}
for k in sorted(x for x in C if C[x]["family"] == "aprc"):
    m = C[k]["model"]
    row = {}
    for it in lst(k):
        if isinstance(it, dict) and "case" in it:
            row[it["case"]] = it.get("aprc_pct", "<<KEY ABSENT>>")
    tab[m] = row
allcases = sorted({c for r in tab.values() for c in r if isinstance(c, int)})
print(f"{'model':16}" + "".join(f"{'case '+str(c):>16}" for c in allcases))
for m in sorted(tab):
    print(f"{m:16}" + "".join(f"{str(tab[m].get(c,'ROW ABSENT')):>16}" for c in allcases))
print("\nper-case spread:")
for c in allcases:
    vals = [(m, tab[m][c]) for m in tab if c in tab[m]]
    nums = [(m, float(v)) for m, v in vals if isinstance(v, (int, float))]
    nonnum = [(m, v) for m, v in vals if not isinstance(v, (int, float))]
    if nums:
        lo = min(nums, key=lambda x: x[1]); hi = max(nums, key=lambda x: x[1])
        cnt = collections.Counter(round(v, 1) for _, v in nums)
        print(f"  case {c}: n={len(nums)}  min={lo[1]} ({lo[0]})  max={hi[1]} ({hi[0]})  "
              f"modal={cnt.most_common(3)}")
    if nonnum:
        print(f"           non-numeric: {nonnum}")

print("\n" + "#" * 100)
print("# POWER4 — honesty-field distributions")
print("#" * 100)
print(f"{'model':16}{'n':>3}  {'paper_vs_general tally':52} {'not_in_paper':14} "
      f"{'cannot-reproduce-verbatim':6} {'not-stated-in-paper':6}")
for k in sorted(x for x in C if C[x]["family"] == "power4"):
    its = lst(k)
    pv = collections.Counter(str(i.get("paper_vs_general", "ABSENT"))[:34] for i in its if isinstance(i, dict))
    nip = collections.Counter(str(i.get("not_in_paper", "ABSENT")) for i in its if isinstance(i, dict))
    q = sum(1 for i in its if isinstance(i, dict) and
            str(i.get("quote_as_recalled", i.get("quote_as_recall_verbatim", ""))).strip()
            == "cannot-reproduce-verbatim")
    a = sum(1 for i in its if isinstance(i, dict) and
            str(i.get("alternatives_or_rejected", "")).strip() == "not-stated-in-paper")
    conf = [i.get("confidence") for i in its if isinstance(i, dict)]
    print(f"{C[k]['model']:16}{len(its):>3}  {str(dict(pv)):52} {str(dict(nip)):14} "
          f"{q:^6} {a:^6}  conf={conf}")

print("\n" + "#" * 100)
print("# LIBRARY — recalled_frequency vocabulary + recall_confidence range")
print("#" * 100)
for k in sorted(x for x in C if C[x]["family"] == "library"):
    its = lst(k)
    freqs, confs, off = collections.Counter(), [], []
    for it in its:
        for rc in (it.get("common_root_causes") or []):
            if isinstance(rc, dict):
                freqs[str(rc.get("recalled_frequency", "ABSENT"))] += 1
                c = rc.get("recall_confidence")
                if isinstance(c, (int, float)):
                    confs.append(c)
                else:
                    off.append(c)
    rng = f"{min(confs):.2f}-{max(confs):.2f}" if confs else "-"
    mean = f"{sum(confs)/len(confs):.3f}" if confs else "-"
    bad = [f for f in freqs if f not in ("common", "occasional", "rare")]
    print(f"  {C[k]['model']:16} items={len(its):2} causes={sum(freqs.values()):3} "
          f"conf[{rng}] mean={mean}  freq={dict(freqs)}"
          + (f"  OFF-ENUM:{bad}" if bad else ""))

print("\n" + "#" * 100)
print("# PATTERNS — provenance enum + recall_confidence")
print("#" * 100)
ENUM = {"recalled-from-practice", "textbook-standard", "tool-default-idiom"}
for k in sorted(x for x in C if C[x]["family"] == "patterns"):
    its = lst(k)
    if not its:
        print(f"  {C[k]['model']:16} NO PARSED ITEMS (parse={C[k]['parse']})")
        continue
    prov = collections.Counter(str(i.get("provenance", "ABSENT")) for i in its if isinstance(i, dict))
    confs = [i.get("recall_confidence") for i in its if isinstance(i, dict)]
    nums = [c for c in confs if isinstance(c, (int, float))]
    off = [p for p in prov if p not in ENUM]
    rng = f"{min(nums):.2f}-{max(nums):.2f}" if nums else "-"
    print(f"  {C[k]['model']:16} items={len(its):2} conf[{rng}] {dict(prov)}"
          + (f"  OFF-ENUM:{off}" if off else ""))
