import json, re, sys, math
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
store = json.load(open("store.json", encoding="utf-8"))

def num(v):
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, dict):
        for k in ("value", "val"):
            if k in v:
                return num(v[k])
    if isinstance(v, str):
        m = re.search(r"-?\d[\d,]*\.?\d*(?:[eE][-+]?\d+)?", v.replace(",", ""))
        if m:
            return float(m.group())
    return None

def find(inp, *keys):
    if not isinstance(inp, dict):
        return None
    for k, v in inp.items():
        kl = k.lower().replace("λ", "lambda").replace("_", "").replace(" ", "")
        for key in keys:
            if key in kl:
                n = num(v)
                if n is not None:
                    return n
    return None

rows = []
for f in store["T"]:
    for it in f["items"]:
        calc = str(it.get("calculation") or "").lower()
        inp = it.get("inputs") or {}
        out = it.get("expected_output") or {}
        name = str(it.get("vector_name"))[:60]
        verdict, detail = "SKIP", ""
        if "spfm" in calc:
            spf = find(inp, "lambdaspf", "spf")
            rf = find(inp, "lambdarf", "residual", "rf")
            tot = find(inp, "total", "lambdatotal")
            if tot is None:
                mpf = find(inp, "mpflatent", "latent", "mpf")
                safe = find(inp, "safe", "lambdas")
                det = find(inp, "mpfdet", "detected")
                parts = [x for x in (spf, rf, mpf, safe, det) if x is not None]
                tot = sum(parts) if len(parts) >= 3 else None
            claimed = find(out, "spfm")
            if None not in (spf, rf, tot) and tot:
                calcv = (1 - (spf + rf) / tot) * 100
                if claimed is not None:
                    cl = claimed * 100 if claimed <= 1.0001 else claimed
                    ok = abs(calcv - cl) < 0.15
                    verdict = "OK" if ok else "FAIL"
                    detail = f"recomputed {calcv:.4f}% vs claimed {cl:.4f}%"
                else:
                    verdict, detail = "NOCLAIM", f"recomputed {calcv:.4f}%"
        elif "tpp" in calc:
            claimed = find(out, "tpp")
            txt = json.dumps(inp, ensure_ascii=False)
            pairs = re.findall(r"(\d[\d,]*\.?\d*)\s*(?:mac)?tops[^0-9]{0,40}?(\d+)\s*[- ]?bit", txt, re.I)
            if pairs:
                tot = sum(2 * float(a.replace(",", "")) * float(b) for a, b in pairs)
                if claimed:
                    ok = abs(tot - claimed) / max(1, claimed) < 0.02
                    verdict = "OK" if ok else "FAIL"
                    detail = f"recomputed {tot:.0f} vs claimed {claimed:.0f}"
        rows.append((f["model"], calc[:22], name, verdict, detail))

from collections import Counter
c = Counter(r[3] for r in rows)
print("VERDICTS:", dict(c), "total", len(rows))
for r in rows:
    if r[3] in ("FAIL", "OK", "NOCLAIM"):
        print(f"{r[3]:8} {r[0]:14} {r[1]:22} {r[2][:44]:46} {r[4]}")
