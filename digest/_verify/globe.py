import json, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
S = json.load(open("day2.json", encoding="utf-8"))

NUM = re.compile(r"-?[\d,]+(?:\.\d+)?")

def nums(s):
    return [float(x.replace(",", "")) for x in NUM.findall(str(s))]

for key, rec in sorted(S.items()):
    model, prompt = key.split("|")
    if prompt != "globe":
        continue
    d = rec["data"]
    if not isinstance(d, list):
        d = [d]
    print(f"\n{'='*95}\n### {model}   ({len(d)} examples)")
    for c in d:
        if not isinstance(c, dict):
            continue
        print(f"\n  [{str(c.get('example_id'))} | {str(c.get('article'))[:40]}] "
              f"doc_vs_general={str(c.get('doc_vs_general'))[:48]}")
        print(f"    FACTS: {str(c.get('fact_pattern'))[:340]}")
        print(f"    COMP : {str(c.get('computation'))[:900]}")
        print(f"    RESULT: {str(c.get('result'))[:220]}")
        print(f"    WEAK : {str(c.get('weakest_point'))[:170]}")
