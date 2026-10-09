"""Re-grade JCS with adjudication classes:
   OK          - byte-identical to reference canonicalizer
   DUP         - duplicate-key vector: RFC 8785 3.1 forbids it, not counted either way
   FORM        - substance right, output escaped instead of literal UTF-8 (or vice versa)
   WRONG       - substantive divergence (number serialization, key order, escaping rule)
   INPUTBAD    - the model's own input_json is not valid JSON (vector unusable)
"""
import json, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from jcs import canon

BS = chr(92)
S = json.load(open("day2b.json", encoding="utf-8"))

# chatgpt needs the quote-repair salvage
raw = open(r"C:\dev\Claude\Projects\ASIC\Web Model Tasks\Day 2\chatgpt jcs.json",
           encoding="utf-8").read()
out = []
for ln in raw.split("\n"):
    m = re.match(r'^(\s*"[A-Za-z_]+"\s*:\s*")(.*)("\s*,?\s*)$', ln)
    if m:
        h, v, t = m.groups()
        out.append(h + v.replace(BS, BS + BS).replace('"', BS + '"') + t)
    else:
        out.append(ln)
CG = json.loads("\n".join(out))


def unescape_only(a, b):
    """True if a and b differ only by \\uXXXX escaping of non-control characters."""
    def norm(s):
        return re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), s)
    def fix(s):
        s = norm(s)
        o = []
        i = 0
        while i < len(s):
            c = s[i]
            if 0xD800 <= ord(c) < 0xDC00 and i + 1 < len(s) and 0xDC00 <= ord(s[i+1]) < 0xE000:
                o.append(chr(0x10000 + ((ord(c) - 0xD800) << 10) + (ord(s[i+1]) - 0xDC00)))
                i += 2
                continue
            o.append(c)
            i += 1
        return "".join(o)
    return fix(a) == fix(b)


rows = {}
for key, rec in sorted(S.items()):
    m, p = key.split("|")
    if p != "jcs":
        continue
    d = CG if m == "chatgpt" else (rec["data"] if isinstance(rec["data"], list) else [rec["data"]])
    tally = {"OK": 0, "FORM": 0, "WRONG": 0, "DUP": 0, "INPUTBAD": 0}
    notes = []
    for c in d:
        if not isinstance(c, dict) or "input_json" not in c:
            tally["INPUTBAD"] += 1
            continue
        nm = str(c.get("vector_name"))[:44]
        th = c.get("canonical_output")
        if "dup" in nm.lower():
            tally["DUP"] += 1
            notes.append(f"DUP  [{nm}] answered: {str(th)[:48]!r}")
            continue
        try:
            v = json.loads(c["input_json"])
        except Exception as e:
            tally["INPUTBAD"] += 1
            notes.append(f"INPUTBAD [{nm}] {e}")
            continue
        mine = canon(v)
        if not isinstance(th, str):
            tally["WRONG"] += 1
            notes.append(f"WRONG [{nm}] non-string output {th!r}")
        elif mine == th:
            tally["OK"] += 1
        elif unescape_only(mine, th):
            tally["FORM"] += 1
            notes.append(f"FORM [{nm}] escaped-not-literal")
        else:
            tally["WRONG"] += 1
            notes.append(f"WRONG [{nm}]\n       in     {c['input_json'][:88]}"
                         f"\n       theirs {th[:88]}\n       mine   {mine[:88]}")
    rows[m] = (tally, notes)

print(f"{'model':16}{'OK':>4}{'FORM':>6}{'WRONG':>7}{'DUP':>5}{'BAD':>5}   gradable  score")
for m, (t, n) in sorted(rows.items(), key=lambda x: (-x[1][0]["OK"], x[1][0]["WRONG"])):
    g = t["OK"] + t["FORM"] + t["WRONG"]
    sc = f"{t['OK']}/{g}" if g else "-"
    print(f"{m:16}{t['OK']:>4}{t['FORM']:>6}{t['WRONG']:>7}{t['DUP']:>5}{t['INPUTBAD']:>5}   {g:>7}  {sc}")
print()
for m, (t, n) in sorted(rows.items()):
    if n:
        print(f"\n### {m}")
        for x in n:
            print("  " + x)
