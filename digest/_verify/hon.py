import json, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
S = json.load(open("day2b.json", encoding="utf-8"))
PROMPTS = ["irb", "frtb", "mica", "ccd2", "receipt", "jcs"]
MODELS = sorted({k.split("|")[0] for k in S})

HON = ["weakest_point", "certainty", "certainty_notes", "known_uncertainty",
       "tail_convention", "article_basis", "known_benchmark", "source_basis",
       "confidence", "provenance_note", "rule", "divergence_trap"]

print("GRID (cases per model x prompt; '-' = file absent)")
hdr = f"{'model':16}" + "".join(f"{p:>9}" for p in PROMPTS)
print(hdr)
absent = []
for m in MODELS:
    row = f"{m:16}"
    for p in PROMPTS:
        k = f"{m}|{p}"
        if k not in S:
            row += f"{'-':>9}"
            absent.append((m, p))
            continue
        d = S[k]["data"]
        n = len(d) if isinstance(d, list) else (len(d) if isinstance(d, dict) else 1)
        row += f"{n:>9}"
    print(row)
print(f"\nABSENT files ({len(absent)}): " + ", ".join(f"{m}/{p}" for m, p in absent))

print("\n\nHONESTY FIELD PRESENCE (share of cases carrying the field)")
print(f"{'model':16}" + "".join(f"{p:>9}" for p in PROMPTS))
for m in MODELS:
    row = f"{m:16}"
    for p in PROMPTS:
        k = f"{m}|{p}"
        if k not in S:
            row += f"{'-':>9}"
            continue
        d = S[k]["data"]
        objs = d if isinstance(d, list) else [d]
        objs = [o for o in objs if isinstance(o, dict)]
        if p in ("receipt",):
            blob = json.dumps(S[k]["data"], ensure_ascii=False)
            row += f"{('cert' if 'certainty' in blob else 'NONE'):>9}"
            continue
        hit = sum(1 for o in objs if any(h in o for h in HON))
        row += f"{hit}/{len(objs):<7}"
    print(row)

print("\n\nWEAKEST_POINT / uncertainty text length (median chars, C1 prompts)")
for m in MODELS:
    out = []
    for p in ("irb", "frtb", "mica", "ccd2"):
        k = f"{m}|{p}"
        if k not in S:
            out.append(f"{p}:-")
            continue
        objs = S[k]["data"] if isinstance(S[k]["data"], list) else [S[k]["data"]]
        L = []
        for o in objs:
            if not isinstance(o, dict):
                continue
            t = " ".join(str(o.get(h, "")) for h in HON)
            L.append(len(t.strip()))
        L.sort()
        out.append(f"{p}:{L[len(L)//2] if L else 0}")
    print(f"  {m:16} " + "  ".join(out))
