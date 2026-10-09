import json, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
S = json.load(open("day2b.json", encoding="utf-8"))

PROBES = {
    "n_public_inputs": r'(\b(?:one|two|three|four|five|1|2|3|4|5)\b[^.\n]{0,40}public input)',
    "split_128": r'(128[- ]bit|two halves|hi/lo|lo/hi|split[^.\n]{0,40}(?:field element|half))',
    "imageid_is_pre": r'(image[_ ]?id[^.\n]{0,80}pre[- ]?state|pre[- ]?state[^.\n]{0,60}image[_ ]?id)',
    "tagged_hash": r'(tagged|domain separat|risc0\.[A-Za-z]+|struct hash)',
    "bn254_control": r'(bn254[_ ]?control|control[_ ]?root|control[_ ]?id)',
    "selector": r'(selector|first 4 bytes|4-byte)',
    "assumptions": r'(assumption)',
}
for key, rec in sorted(S.items()):
    m, p = key.split("|")
    if p != "receipt":
        continue
    blob = json.dumps(rec["data"], ensure_ascii=False)
    print(f"\n### {m}  [{rec.get('parse','clean')}]")
    for name, pat in PROBES.items():
        hits = re.findall(pat, blob, re.I)
        uniq = sorted({(h if isinstance(h, str) else h[0]).strip().lower() for h in hits})[:4]
        print(f"   {name:16} {len(hits):3}  {uniq}")
