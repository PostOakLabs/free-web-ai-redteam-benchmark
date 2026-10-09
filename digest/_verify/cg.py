import json, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from jcs import canon

BS = chr(92)
raw = open(r"C:\dev\Claude\Projects\ASIC\Web Model Tasks\Day 2\chatgpt jcs.json",
           encoding="utf-8").read()

# SALVAGE technique 6: value strings carry UNESCAPED inner double quotes.
# Repair line-wise: re-escape backslashes then quotes inside each "key": "value" line.
out = []
for ln in raw.split("\n"):
    m = re.match(r'^(\s*"[A-Za-z_]+"\s*:\s*")(.*)("\s*,?\s*)$', ln)
    if m:
        head, val, tail = m.groups()
        val = val.replace(BS, BS + BS).replace('"', BS + '"')
        out.append(head + val + tail)
    else:
        out.append(ln)
d = json.loads("\n".join(out))
print("SALVAGED chatgpt jcs vectors:", len(d))

ok = fail = unp = 0
for c in d:
    nm = str(c.get("vector_name"))[:40]
    try:
        v = json.loads(c["input_json"])
    except Exception as e:
        print(f"  UNPARSE [{nm}] {e}")
        unp += 1
        continue
    mine = canon(v)
    th = c.get("canonical_output")
    if mine == th:
        ok += 1
    else:
        fail += 1
        print(f"  FAIL [{nm}] cert={c.get('certainty')}")
        print(f"     in     {c['input_json'][:95]}")
        print(f"     theirs {str(th)[:95]}")
        print(f"     mine   {mine[:95]}")
print(f"chatgpt OK={ok} FAIL={fail} UNPARSE={unp}")
