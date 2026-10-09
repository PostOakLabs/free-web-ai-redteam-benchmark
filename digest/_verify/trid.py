import json, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
S = json.load(open("day2.json", encoding="utf-8"))

def num(v):
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        m = re.search(r"-?[\d,]+\.?\d*", v.replace("$", ""))
        if m:
            return float(m.group().replace(",", ""))
    return None

def bucket(b):
    b = (b or "").lower()
    if "zero" in b:
        return "zero"
    if "ten" in b or "10" in b:
        return "ten"
    return "nolimit"

for key, rec in sorted(S.items()):
    model, prompt = key.split("|")
    if prompt != "trid":
        continue
    d = rec["data"]
    if not isinstance(d, list):
        d = [d]
    print(f"\n{'='*95}\n### {model}   ({len(d)} cases)")
    for c in d:
        if not isinstance(c, dict):
            continue
        fees = c.get("fees") or []
        zle = zcd = tle = tcd = 0.0
        zviol = []
        for f in fees:
            if not isinstance(f, dict):
                continue
            b = bucket(f.get("bucket"))
            le = num(f.get("le_amount"))
            cd = num(f.get("cd_amount"))
            if le is None or cd is None:
                continue
            if b == "zero":
                zle += le; zcd += cd
                if cd > le + 1e-9:
                    zviol.append((f.get("name"), round(cd - le, 2)))
            elif b == "ten":
                tle += le; tcd += cd
        thr = tle * 0.10
        allowed = tle + thr
        ten_excess = round(tcd - allowed, 2)
        zcure = round(sum(x[1] for x in zviol), 2)
        name = str(c.get("case_name"))[:52]
        print(f"\n  [{name}]")
        print(f"    ZERO : Σle={zle:.2f} Σcd={zcd:.2f} | per-fee overages={zviol} cure={zcure:.2f}")
        print(f"    TEN  : Σle={tle:.2f} Σcd={tcd:.2f} thr(10%)={thr:.2f} allowed={allowed:.2f} "
              f"-> {'VIOLATION cure=' + format(ten_excess, '.2f') if ten_excess > 0.005 else 'no violation'}")
        # sum-of-increases trap
        inc = sum(max(0.0, num(f.get('cd_amount')) - num(f.get('le_amount')))
                  for f in fees if isinstance(f, dict) and bucket(f.get('bucket')) == 'ten'
                  and num(f.get('le_amount')) is not None and num(f.get('cd_amount')) is not None)
        if abs(inc - (tcd - tle)) > 0.005:
            print(f"    TRAP : sum-of-increases={inc:.2f} vs aggregate-delta={tcd-tle:.2f} (mixed-direction case)")
        v = c.get("violations")
        print(f"    MODEL SAYS: {str(v)[:300]}")
