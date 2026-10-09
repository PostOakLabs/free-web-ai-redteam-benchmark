"""Byte-level extraction of the specific anomalies, so each digest claim can cite an offset."""
import json, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BASE = r"C:\dev\Claude\Projects\ASIC\Web Model Tasks\Day 3"


def show(fname, pattern, n=3, w=150):
    raw = open(rf"{BASE}\{fname}", encoding="utf-8-sig").read()
    print(f"\n--- {fname}  ({len(raw)} chars) : /{pattern}/ ---")
    hits = list(re.finditer(pattern, raw))
    print(f"    {len(hits)} match(es)")
    for m in hits[:n]:
        s = max(0, m.start() - w)
        print(f"    @char {m.start()}: ...{raw[s:m.end()+w]}...")


print("=" * 96)
print("A. chatgpt library.json — node_era escape emitted as a KEY, three spellings")
print("=" * 96)
show("chatgpt library.json", r'"no[-_]era[-_]difference[-_]recalled"\s*:', n=4, w=90)

print()
print("=" * 96)
print("B. minimax 2.7 power4.json — double-wrapped array")
print("=" * 96)
raw = open(rf"{BASE}\minimax 2.7 power4.json", encoding="utf-8-sig").read()
print("    first 20 chars:", repr(raw[:20]))
print("    last  20 chars:", repr(raw[-20:]))
d = json.loads(raw)
print(f"    outer list len={len(d)}  inner type={type(d[0]).__name__} len={len(d[0])}")
print(f"    inner[0] keys: {sorted(d[0][0])}")
print(f"    NOTE: field name is {'quote_as_recall_verbatim' if 'quote_as_recall_verbatim' in d[0][0] else 'quote_as_recalled'}")

print()
print("=" * 96)
print("C. meta aprc.json — content identity check vs Day 2 meta receipt.json")
print("=" * 96)
a = open(rf"{BASE}\meta aprc.json", encoding="utf-8-sig").read()
b = open(r"C:\dev\Claude\Projects\ASIC\Web Model Tasks\Day 2\meta receipt.json",
         encoding="utf-8-sig").read()
print(f"    Day3 'meta aprc.json'      : {len(a)} chars, first 90: {a[:90]!r}")
print(f"    Day2 'meta receipt.json'   : {len(b)} chars, first 90: {b[:90]!r}")
print(f"    byte-identical: {a == b}")
print(f"    identical after whitespace-strip: {''.join(a.split()) == ''.join(b.split())}")
print(f"    Day3 tail 20: {a[-20:]!r}   Day2 tail 20: {b[-20:]!r}")
print(f"    top-level keys (Day3 aprc file): {sorted(json.loads(a[:a.rfind('}')+1]))}")

print()
print("=" * 96)
print("D. minimax m3 patterns.json — the splice, exact offsets")
print("=" * 96)
raw = open(rf"{BASE}\minimax m3 patterns.json", encoding="utf-8-sig").read()
try:
    json.loads(raw)
except json.JSONDecodeError as e:
    print(f"    json.loads: {e.msg} at char {e.pos} (line {e.lineno} col {e.colno})")
m = re.search(r'the path fails', raw)
print(f"    splice seam at char {m.start()}:")
print("    " + repr(raw[m.start() - 60:m.start() + 160]))
# how many complete objects survive after the seam?
objs = 0
dec = json.JSONDecoder()
for mm in re.finditer(r'\n  \{', raw):
    try:
        dec.raw_decode(raw[mm.start() + 3:])
        objs += 1
    except json.JSONDecodeError:
        pass
print(f"    complete top-level objects recoverable by object-boundary scan: {objs}")
print(f"    file ends with a closing bracket: {raw.rstrip()[-1:]!r}")

print()
print("=" * 96)
print("E. mimo library.json — recall/paper fields leaking into the F-family schema")
print("=" * 96)
for pat in (r'"paper_vs_general"\s*:\s*"[^"]{0,60}',
            r'"not_in_paper"\s*:\s*[a-z]+',
            r'"weakest_point"\s*:\s*"[^"]{0,60}'):
    show("mimo library.json", pat, n=2, w=70)
show("glm 5.3 flash library.json", r'"not_in_paper"\s*:\s*[a-z]+', n=2, w=70)

print()
print("=" * 96)
print("F. mimo aprc.json — prose leading/trailing outside the JSON")
print("=" * 96)
raw = open(rf"{BASE}\mimo aprc.json", encoding="utf-8-sig").read()
print("    LEAD 300 chars:", repr(raw[:300]))
print("    ...")
print("    TAIL 320 chars:", repr(raw[-320:]))
