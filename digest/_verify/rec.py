import json, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
S = json.load(open("day2b.json", encoding="utf-8"))

SEC = ["receipt_kinds", "groth16_receipt_fields", "claim_structure", "binding_chain",
       "version_coupling", "common_verifier_bugs", "certainty_notes"]

fieldcount = collections.Counter()
owner = collections.defaultdict(list)
for key, rec in sorted(S.items()):
    m, p = key.split("|")
    if p != "receipt":
        continue
    d = rec["data"]
    objs = d if isinstance(d, list) else [d]
    o = {}
    for x in objs:
        if isinstance(x, dict):
            o.update(x)
    have = [s for s in SEC if s in o]
    miss = [s for s in SEC if s not in o]
    g16 = o.get("groth16_receipt_fields") or []
    names = []
    for f in (g16 if isinstance(g16, list) else []):
        if isinstance(f, dict):
            n = f.get("field") or f.get("name")
            if n:
                names.append(str(n))
        elif isinstance(f, str):
            names.append(f)
    for n in names:
        k = re.sub(r'[^a-z0-9]', '', str(n).lower())
        fieldcount[k] += 1
        owner[k].append(m)
    nb = len(o.get("common_verifier_bugs") or [])
    cn = o.get("certainty_notes")
    cn_kind = ("per-section dict" if isinstance(cn, dict) else
               f"list[{len(cn)}]" if isinstance(cn, list) else
               "string" if isinstance(cn, str) else "ABSENT")
    print(f"\n### {m}   sections {len(have)}/7  missing={miss or '-'}")
    print(f"    g16 fields ({len(names)}): {', '.join(names)}")
    print(f"    verifier_bugs={nb}  certainty_notes={cn_kind}")
    kinds = o.get("receipt_kinds")
    if isinstance(kinds, list):
        kn = [(k.get("kind") or k.get("name") or str(k)[:30]) if isinstance(k, dict) else str(k)[:30]
              for k in kinds]
        print(f"    kinds: {kn}")
    bc = o.get("binding_chain")
    n_bc = len(bc) if isinstance(bc, list) else ("prose" if isinstance(bc, str) else "?")
    print(f"    binding_chain steps: {n_bc}")

print("\n\n===== groth16 field-name frequency (15 files) =====")
for k, c in fieldcount.most_common():
    print(f"  {c:2}  {k:28} {sorted(set(owner[k])) if c <= 3 else ''}")
