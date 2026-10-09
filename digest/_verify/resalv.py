"""Re-salvage the three receipt files the main loader left unparsed, and patch
them into day2b.json so rec.py grades them.

Salvage shapes needed here:
  meta    - trailing content after the closing brace  ("[2]")          [technique 4]
  sonnet  - markdown fence + a "key": "value" PAIR sitting inside an   [technique 7]
            ARRAY of strings (mixed array/object)
  yuanbao - raw literal newlines inside string values                  [technique 8]
"""
import json, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BASE = r"C:\dev\Claude\Projects\ASIC\Web Model Tasks\Day 2"
DEC = json.JSONDecoder()


def strip_fence(raw):
    raw = re.sub(r'^\s*```(?:json)?\s*', '', raw)
    return re.sub(r'\s*```\s*$', '', raw.strip())


def escape_raw_newlines(raw):
    """Escape literal LF/CR that appear INSIDE a JSON string literal."""
    out, in_str, esc = [], False, False
    for ch in raw:
        if esc:
            out.append(ch)
            esc = False
            continue
        if ch == chr(92) and in_str:
            out.append(ch)
            esc = True
            continue
        if ch == '"':
            in_str = not in_str
            out.append(ch)
            continue
        if in_str and ch in "\n\r":
            out.append(chr(92) + ("n" if ch == "\n" else "r"))
            continue
        out.append(ch)
    return "".join(out)


def pair_in_array(raw):
    """Error-driven repair: a stray `"key": "value"` PAIR sitting inside an ARRAY.
    The decoder stops on the ':' that cannot follow an array element, so at that
    position we delete the preceding key literal and the colon, keeping the value."""
    for _ in range(12):
        try:
            DEC.raw_decode(raw)
            return raw
        except json.JSONDecodeError as e:
            p = e.pos
            while p < len(raw) and raw[p] in " \t":
                p += 1
            if p >= len(raw) or raw[p] != ":":
                return raw                       # not this shape; give up
            q = raw.rfind('"', 0, e.pos)         # closing quote of the key
            q = raw.rfind('"', 0, q)             # opening quote of the key
            if q < 0:
                return raw
            raw = raw[:q] + raw[p + 1:].lstrip(" ")
    return raw


def salvage(path):
    raw = strip_fence(open(path, encoding="utf-8-sig").read())
    i = min(x for x in (raw.find("{"), raw.find("[")) if x >= 0)
    body = raw[i:]
    for fix, label in ((lambda s: s, "clean"),
                       (escape_raw_newlines, "raw-newline escape"),
                       (pair_in_array, "pair-in-array"),
                       (lambda s: pair_in_array(escape_raw_newlines(s)), "both")):
        try:
            obj, end = DEC.raw_decode(fix(body))
            return obj, fix(body)[end:].strip(), label
        except json.JSONDecodeError:
            continue
    raise SystemExit(f"unsalvageable: {path}")


S = json.load(open("day2b.json", encoding="utf-8"))
for m in ("meta", "sonnet", "yuanbao"):
    obj, trail, how = salvage(rf"{BASE}\{m} receipt.json")
    S[f"{m}|receipt"] = {"data": obj, "parse": f"salvaged:{how}", "trailing": trail}
    print(f"{m:8} salvage={how:20} keys={len(obj) if isinstance(obj, dict) else '?'} "
          f"trailing={trail[:20]!r}")
json.dump(S, open("day2b.json", "w", encoding="utf-8"), ensure_ascii=False)
