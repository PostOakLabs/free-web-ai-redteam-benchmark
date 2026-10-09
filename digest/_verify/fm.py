"""Confirm the FRTB and MICA numeric anchors model-by-model, for the scorecard."""
import json, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
S = json.load(open("day2b.json", encoding="utf-8"))

# Reference values (normal ES): ES_a = phi(z_a)/(1-a)
ANCH = {
    "phi(1.96)=0.05844": r"0\.0584\d*",
    "phi(2.3263)=0.02665": r"0\.0266\d*",
    "ES97.5 mult 2.3378": r"2\.33[67]\d*",
    "ES99 mult 2.6652": r"2\.66[45]\d*",
    "sqrt(20/10)=1.41421": r"1\.414\d*",
    "z97.5=1.95996": r"1\.9599\d*",
    "z99=2.32635": r"2\.3263\d*",
}
BAD = {"VaR-as-ES 1.95996 used as multiplier": r"multiplier[^.\n]{0,30}1\.9599",
       "ES=VaR conflation phrase": r"(?i)expected shortfall\s*(?:=|is|equals)\s*va[r_]"}

print("FRTB anchors present per model")
for key in sorted(S):
    m, p = key.split("|")
    if p != "frtb":
        continue
    blob = json.dumps(S[key]["data"], ensure_ascii=False)
    hits = [k for k, r in ANCH.items() if re.search(r, blob)]
    bad = [k for k, r in BAD.items() if re.search(r, blob)]
    print(f"  {m:16} {len(hits)}/7  {sorted(hits)}")
    if bad:
        print(f"      !! {bad}")

print("\n\nMICA: tail_convention presence + stress arithmetic closure")
for key in sorted(S):
    m, p = key.split("|")
    if p != "mica":
        continue
    d = S[key]["data"]
    objs = d if isinstance(d, list) else [d]
    objs = [o for o in objs if isinstance(o, dict)]
    tc = sum(1 for o in objs if any("tail" in k.lower() for k in o))
    blob = json.dumps(d, ensure_ascii=False)
    unk = len(re.findall(r"UNKNOWN[-_ ]?CURRENT[-_ ]?VALUE|UNKNOWN", blob))
    eur = sorted(set(re.findall(r"350[,.]?000|EUR\s?350", blob)))
    two = len(re.findall(r"\b2\s?%|\b0\.02\b", blob))
    print(f"  {m:16} cases={len(objs):2} tail_convention={tc:2} UNKNOWN-flags={unk:2} "
          f"own-funds-350k={'Y' if eur else 'n'} two-pct-refs={two}")
