"""Boundary family: extract the load-bearing cells (inclusivity + 3 verdicts x 8 rules)
and build the agreement/divergence map. No grading — normalisation only."""
import json, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
C = json.load(open("corpus.json", encoding="utf-8"))

POS = re.compile(r'\b(fires?|fired|firing|yes|true|trigger(?:s|ed)?|pass(?:es|ed)?|'
                 r'blocked|met|satisfied|qualif|exceeds|above|applies|in\b)', re.I)
NEG = re.compile(r'\b(does not|no\b|not\b|fail(?:s|ed)?|false|below|excluded|'
                 r'ineligible|disqualif)', re.I)


def norm(v):
    """Map a free-text verdict to FIRE / NO-FIRE / OTHER, keeping the raw text."""
    if v is None:
        return "ABSENT", None
    s = str(v).strip()
    low = s.lower()
    neg = bool(re.match(r'^\s*(no|does not|not|fail|false)\b', low)) or \
          bool(re.search(r'\b(does not (fire|trigger|apply|exceed)|no[t]? (fire|trigger)|'
                         r'not (triggered|met|satisfied)|fails?\b|no-fire|no\b)', low))
    pos = bool(re.match(r'^\s*(yes|fire|trigger|pass|true|qualif|blocked)', low))
    if pos and not re.match(r'^\s*(no|not)\b', low):
        return "FIRE/PASS", s
    if neg:
        return "NO", s
    if re.search(r'\b(fires|triggered|applies|exceeds|passes|qualifies|meets)\b', low):
        return "FIRE/PASS", s
    return "OTHER", s


rows = {}
incl = {}
for k in sorted(x for x in C if C[x]["family"] == "boundary"):
    r = C[k]
    m = r["model"]
    d = r["data"]
    lst = d["rules"] if isinstance(d, dict) and "rules" in d else d
    if not isinstance(lst, list):
        continue
    for it in lst:
        if not isinstance(it, dict) or "rule" not in it:
            continue
        n = it.get("rule")
        try:
            n = int(n)
        except (TypeError, ValueError):
            continue
        v = it.get("verdicts") or {}
        cells = {}
        for slot in ("below", "at", "above"):
            cells[slot] = norm(v.get(slot) if isinstance(v, dict) else None)
        rows[(m, n)] = cells
        incl[(m, n)] = it.get("phrase_inclusivity", "ABSENT")

models = sorted({m for m, _ in rows})
print(f"models with parsed boundary rows: {len(models)}\n")

for n in range(1, 9):
    print("=" * 100)
    print(f"RULE {n}")
    print("=" * 100)
    ci = collections.Counter()
    tri = collections.Counter()
    for m in models:
        c = rows.get((m, n))
        if c is None:
            print(f"  {m:16} ROW ABSENT")
            continue
        pat = (c["below"][0], c["at"][0], c["above"][0])
        tri[pat] += 1
        ci[str(incl.get((m, n)))] += 1
        print(f"  {m:16} incl={str(incl.get((m,n))):10} "
              f"below={c['below'][0]:10} at={c['at'][0]:10} above={c['above'][0]:10}")
    print(f"  --> inclusivity tally: {dict(ci)}")
    print(f"  --> verdict-triple tally: {dict(tri)}")
    print()

print("\n\nRAW 'at' CELL TEXT (the load-bearing cell) per rule/model")
for n in range(1, 9):
    print(f"\n### rule {n}")
    for m in models:
        c = rows.get((m, n))
        if c:
            print(f"  {m:16} {str(c['at'][1])[:118]}")
