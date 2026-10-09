import json, math, re, sys
from statistics import NormalDist
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
N = NormalDist()
S = json.load(open("day2b.json", encoding="utf-8"))

def K_of(pd, lgd, M):
    R = 0.12 * (1 - math.exp(-50 * pd)) / (1 - math.exp(-50)) \
        + 0.24 * (1 - (1 - math.exp(-50 * pd)) / (1 - math.exp(-50)))
    b = (0.11852 - 0.05478 * math.log(pd)) ** 2
    inner = N.inv_cdf(pd) / math.sqrt(1 - R) + math.sqrt(R / (1 - R)) * N.inv_cdf(0.999)
    cond = N.cdf(inner)
    k_nomat = lgd * cond - pd * lgd
    mat = (1 + (M - 2.5) * b) / (1 - 1.5 * b)
    return R, b, N.inv_cdf(pd), inner, cond, k_nomat, k_nomat * mat

print(f"REFERENCE TABLE (LGD 45pct, M 2.5) Phi_inv(0.999)={N.inv_cdf(0.999):.4f}")
for pd in (0.005, 0.01, 0.03, 0.10):
    R, b, ip, inner, cond, k0, k = K_of(pd, 0.45, 2.5)
    print(f"  PD={pd:6.3%}  R={R:.6f} b={b:.6f} Phi_inv(PD)={ip:.4f} inner={inner:.4f} "
          f"Phi(inner)={cond:.6f}  K={k*100:.4f}%  RW={k*12.5*100:.3f}%  RW*1.06={k*12.5*1.06*100:.3f}%")

def num(v):
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        m = re.search(r"-?[\d.]+", v.replace(",", ""))
        if m:
            return float(m.group())
    return None

def get(d, *keys):
    if not isinstance(d, dict):
        return None
    for k, v in d.items():
        kl = k.lower().replace("_", "").replace(" ", "")
        for key in keys:
            if key in kl:
                n = num(v)
                if n is not None:
                    return n
    return None

print("\n" + "=" * 100)
for key, rec in sorted(S.items()):
    model, prompt = key.split("|")
    if prompt != "irb":
        continue
    d = rec["data"]
    d = d if isinstance(d, list) else [d]
    print(f"\n### {model} ({len(d)})")
    for c in d:
        if not isinstance(c, dict):
            continue
        inp = c.get("inputs") or {}
        pd = get(inp, "pd") ; lgd = get(inp, "lgd") ; M = get(inp, "maturity", "m_years")
        if M is None: M = get(inp, "m")
        if pd is not None and pd > 1: pd /= 100.0
        if pd is not None and pd > 0.5: pd = None
        if lgd is not None and lgd > 1: lgd /= 100.0
        if M is not None and not (0.5 <= M <= 10): M = None
        res = c.get("result") or {}
        kp = get(res, "kpct", "k_pct", "k") ; rw = get(res, "riskweight", "rw")
        if pd is None or lgd is None:
            print(f"  SKIP [{str(c.get('case_name'))[:44]}] inputs not extractable")
            continue
        M = M if M else 2.5
        R, b, ip, inner, cond, k0, k = K_of(pd, lgd, M)
        exp_k = k * 100 ; exp_rw = k * 12.5 * 100
        okk = kp is not None and abs(kp - exp_k) < 0.06
        okr = rw is not None and (abs(rw - exp_rw) < 0.8 or abs(rw - exp_rw * 1.06) < 0.8)
        flag = "OK  " if (okk and okr) else "DIFF"
        print(f"  {flag} [{str(c.get('case_name'))[:40]}] PD={pd:.4%} LGD={lgd:.0%} M={M} | "
              f"K: said {kp} vs {exp_k:.4f} | RW: said {rw} vs {exp_rw:.3f} (x1.06={exp_rw*1.06:.3f})")
