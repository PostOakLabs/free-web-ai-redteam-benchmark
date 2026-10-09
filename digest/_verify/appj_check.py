import json, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
S = json.load(open("day2.json", encoding="utf-8"))

def solve(pv, cf, f=0.0):
    lo, hi = 1e-9, 2.0
    for _ in range(300):
        i = (lo + hi) / 2
        v = sum(a / ((1 + f * i) * (1 + i) ** k) for k, a in cf)
        if v > pv:
            lo = i
        else:
            hi = i
    return (lo + hi) / 2

def g(d, *keys):
    if not isinstance(d, dict):
        return None
    for k, v in d.items():
        kl = k.lower()
        for key in keys:
            if key in kl:
                if isinstance(v, (int, float)):
                    return float(v)
                m = re.search(r"[\d,]+\.?\d*", str(v).replace("$", ""))
                if m:
                    return float(m.group().replace(",", ""))
    return None

for key, rec in sorted(S.items()):
    model, prompt = key.split("|")
    if prompt != "appj":
        continue
    d = rec["data"]
    if not isinstance(d, list):
        d = [d]
    print(f"\n### {model}")
    for c in d:
        if not isinstance(c, dict):
            continue
        inp = c.get("inputs") or {}
        A = g(inp, "amount_financed", "amount")
        P = g(inp, "regular_payment", "payment_amount", "monthly_payment")
        n = g(inp, "number_of_payments", "num_payments", "n_payments")
        apr_txt = str(c.get("result_apr"))
        m = re.search(r"[\d.]+", apr_txt)
        apr = float(m.group()) if m else None
        w = g(inp, "unit_periods_per_year") or 12.0
        name = str(c.get("case_name"))[:46]
        if A and P and n and apr and 1 < n < 500:
            i = solve(A, [(k, P) for k in range(1, int(n) + 1)])
            calc = w * i * 100
            ok = abs(calc - apr) < 0.02
            print(f"  {'OK  ' if ok else 'DIFF'} [{name}] A={A} P={P} n={int(n)} w={w:.0f} "
                  f"-> recomputed APR={calc:.4f}%  stated={apr}%")
        else:
            print(f"  SKIP [{name}] (inputs not machine-extractable: A={A} P={P} n={n})")
