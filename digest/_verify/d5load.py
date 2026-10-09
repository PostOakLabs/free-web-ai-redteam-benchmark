"""d5load.py — census-asserting loader for Web Model Tasks/Day 5 (DIGEST-COMMISSION-DAY5-1 G1/G3).

G1: assert loaded + halted == 80 and skipped == 0. Unknown family or unknown model is a
STOP (exit 3), never a skip. The stray `draft 3 and 4 prompt.md` is excluded from the
census by extension and left untouched on disk.

DUAL SPELLING: `minara` (e, red1, regz) and `minaria` (red3, strings) are ONE model
collected under two spellings — the yuanbao-power class of collection defect. Keyed
`minara` with `spelling_as_collected` preserved per record. Files are NOT renamed.

Salvage ladder with recorded parse classes. Content is never repaired: a file that yields
no structure is FAILED.

Usage: python d5load.py   -> d5run/d5corpus.json + d5run/parse-table.txt
"""
import json, os, re, sys, glob, hashlib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ASIC = r"C:\dev\Claude\Projects\ASIC"
BASE = os.path.join(ASIC, "Web Model Tasks", "Day 5")
OUT = os.path.join(ASIC, "digest", "_verify", "d5run")
DEC = json.JSONDecoder()

FAMILIES = {
    "regz":    "C1-REGZ-FACTOR.md",
    "strings": "C2-JCS-STRINGS.md",
    "e":       "PROMPT-E-CALCULATIONS.md",
    "red1":    "J-ISSUE-REDTEAM-V1.md",
    "red3":    "J-EPISODE-REDTEAM-V3.md",
}
# as-collected spelling -> canonical model key
SPELLING = {"minaria": "minara"}
EXPECTED_MODELS = 16
EXPECTED_FILES = 80

KNOWN = {"chatgpt", "deepseek", "gemini", "glm 5.3 flash", "grok", "kimi", "longcat",
         "meta", "mimo", "minimax 2.7", "minimax m3", "mistral", "qwen", "solar",
         "sonnet", "yuanbao", "minara"}


def strip_fence(raw):
    s = re.sub(r"^\s*```(?:json|JSON)?\s*", "", raw)
    return re.sub(r"\s*```\s*$", "", s.strip())


def fix_bad_escapes(raw):
    return re.sub(r'\\(?![\\"/bfnrtu])', r"\\\\", raw)


def escape_raw_newlines(raw):
    out, in_str, esc = [], False, False
    for ch in raw:
        if esc:
            out.append(ch); esc = False; continue
        if ch == chr(92) and in_str:
            out.append(ch); esc = True; continue
        if ch == '"':
            in_str = not in_str; out.append(ch); continue
        if in_str and ch in "\n\r":
            out.append(chr(92) + ("n" if ch == "\n" else "r")); continue
        out.append(ch)
    return "".join(out)


def inner_quote_repair(raw):
    """The chatgpt-jcs class: a value string embeds a JSON document whose inner double
    quotes were never escaped. Repair line-wise. Expected to be the dominant salvage on
    the `strings` family, whose task is literally to emit JSON inside JSON."""
    BS = chr(92)
    out = []
    for ln in raw.split("\n"):
        m = re.match(r'^(\s*"[A-Za-z_0-9]+"\s*:\s*")(.*)("\s*,?\s*)$', ln)
        if m and '"' in m.group(2):
            h, v, t = m.groups()
            out.append(h + v.replace(BS, BS + BS).replace('"', BS + '"') + t)
        else:
            out.append(ln)
    return "\n".join(out)


def structural_quote_repair(raw):
    """Inner-quote repair for SINGLE-LINE JSON, key/value aware.

    The line-wise `inner_quote_repair` above cannot reach a document that is one long
    line (chatgpt red1/red3). Here a quote inside a string closes it only when the next
    non-space char is `,` `}` `]` EOF, or `:` **and the string is in KEY position**.
    A value-position `":` is content — a colon inside prose — which is exactly
    chatgpt red3: `... simply \\"low ILP": Table 1 shows ...`.
    Escaping is applied to content quotes only; no words are altered.
    """
    out, i, n = [], 0, len(raw)
    in_str, key_pos, stack, prev_sig = False, False, [], ""
    BS = chr(92)
    while i < n:
        c = raw[i]
        if c == BS and in_str:
            out.append(raw[i:i + 2]); i += 2; continue
        if not in_str:
            if c == '"':
                in_str = True
                key_pos = bool(stack) and stack[-1] == "{" and prev_sig in ("{", ",")
                out.append(c); i += 1; continue
            if c in "{[":
                stack.append(c); prev_sig = c
            elif c in "}]":
                if stack:
                    stack.pop()
                prev_sig = c
            elif c in ",:":
                prev_sig = c
            out.append(c); i += 1; continue
        if c != '"':
            out.append(c); i += 1; continue
        j = i + 1
        while j < n and raw[j] in " \t\r\n":
            j += 1
        nxt = raw[j] if j < n else ""
        if (nxt == ":" and key_pos) or nxt in (",", "}", "]", ""):
            in_str = False; prev_sig = '"'; out.append(c); i += 1; continue
        out.append(BS + '"'); i += 1
    return "".join(out)


def pair_in_array(raw):
    for _ in range(20):
        try:
            DEC.raw_decode(raw); return raw
        except json.JSONDecodeError as e:
            p = e.pos
            while p < len(raw) and raw[p] in " \t":
                p += 1
            if p >= len(raw) or raw[p] != ":":
                return raw
            q = raw.rfind('"', 0, e.pos)
            q = raw.rfind('"', 0, q)
            if q < 0:
                return raw
            raw = raw[:q] + raw[p + 1:].lstrip(" ")
    return raw


def elementwise(body):
    if not body.lstrip().startswith("["):
        return None
    s = body.lstrip()[1:]
    items, pos = [], 0
    while True:
        tail = s[pos:].lstrip()
        if not tail or tail[0] == "]":
            break
        try:
            o, e = DEC.raw_decode(tail)
        except json.JSONDecodeError:
            break
        items.append(o)
        pos += (len(s[pos:]) - len(s[pos:].lstrip())) + e
        nxt = s[pos:].lstrip()
        if nxt.startswith(","):
            pos += (len(s[pos:]) - len(s[pos:].lstrip())) + 1
        else:
            break
    return items or None


def harvest(text):
    out, i, n = [], 0, len(text)
    while i < n:
        if text[i] not in "[{":
            i += 1; continue
        try:
            val, end = DEC.raw_decode(text, i)
        except json.JSONDecodeError:
            i += 1; continue
        if isinstance(val, dict) and val:
            out.append(val); i = end
        elif isinstance(val, list) and val:
            out.extend(x for x in val if isinstance(x, dict)); i = end
        else:
            i += 1
    return out or None


LADDER = [
    ("clean", lambda s: s),
    ("fence-strip", strip_fence),
    ("bad-escape-repair", lambda s: fix_bad_escapes(strip_fence(s))),
    ("raw-newline-escape", lambda s: escape_raw_newlines(strip_fence(s))),
    ("inner-quote-repair", lambda s: inner_quote_repair(strip_fence(s))),
    ("inner-quote+newline", lambda s: inner_quote_repair(escape_raw_newlines(strip_fence(s)))),
    ("structural-quote-repair", lambda s: structural_quote_repair(strip_fence(s))),
    ("pair-in-array", lambda s: pair_in_array(strip_fence(s))),
    ("combined", lambda s: pair_in_array(inner_quote_repair(
        escape_raw_newlines(fix_bad_escapes(strip_fence(s)))))),
]


def load_one(path):
    raw = open(path, encoding="utf-8-sig").read()
    rec = {"chars": len(raw),
           "sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]}
    for name, fix in LADDER:
        try:
            body = fix(raw)
        except Exception:
            continue
        idx = [x for x in (body.find("{"), body.find("[")) if x >= 0]
        if not idx:
            continue
        i = min(idx)
        try:
            obj, end = DEC.raw_decode(body[i:])
        except json.JSONDecodeError:
            continue
        lead, trail = body[:i].strip(), body[i + end:].strip()
        # Honesty on the label: raw_decode starts at the first bracket, so a file
        # wrapped in a ```json fence would otherwise be reported "clean". Say what
        # was actually outside the parsed value.
        label = name
        if name == "clean" and (lead or trail):
            marks = []
            if lead:
                marks.append("fenced" if lead.startswith("```") else "leading-prose")
            if trail:
                marks.append("fence-close" if trail.strip("`") == "" else "trailing-content")
            label = "clean+" + "+".join(sorted(set(marks)))
        rec.update({"data": obj, "parse": label,
                    "trailing": trail[:200], "leading": lead[:200]})
        return rec
    body = fix_bad_escapes(strip_fence(raw))
    i = body.find("[")
    ew = elementwise(body[i:]) if i >= 0 else None
    hv = harvest(body)
    cands = sorted([(len(ew or []), "elementwise-truncation", ew),
                    (len(hv or []), "harvest-skip-broken-element", hv)], key=lambda c: -c[0])
    if cands[0][0] > 0:
        n, how, items = cands[0]
        rec.update({"data": items, "parse": how, "trailing": "", "leading": "",
                    "recovery_compare": {"elementwise": len(ew or []),
                                         "harvest": len(hv or [])}})
        return rec
    try:
        json.loads(raw)
    except json.JSONDecodeError as e:
        rec.update({"data": None, "parse": "FAILED",
                    "error": f"{e.msg} at line {e.lineno} col {e.colno} (char {e.pos})"})
    return rec


def main():
    os.makedirs(OUT, exist_ok=True)
    all_entries = sorted(os.listdir(BASE))
    strays = [f for f in all_entries if not f.endswith(".json")]
    files = sorted(glob.glob(os.path.join(BASE, "*.json")))
    census = len(files)

    store, halted, skipped = {}, [], []
    for p in files:
        stem = os.path.basename(p)[:-5]
        fam = stem.rsplit(" ", 1)[-1]
        raw_model = stem[: -(len(fam) + 1)]
        model = SPELLING.get(raw_model, raw_model)
        if fam not in FAMILIES:
            halted.append((os.path.basename(p), f"unknown family '{fam}'")); continue
        if model not in KNOWN:
            halted.append((os.path.basename(p), f"unknown model '{raw_model}'")); continue
        rec = load_one(p)
        rec.update({"file": os.path.basename(p), "model": model,
                    "spelling_as_collected": raw_model,
                    "dual_spelled": raw_model != model,
                    "family": fam, "prompt": FAMILIES[fam]})
        store[f"{model}|{fam}"] = rec

    loaded = len(store)
    if halted:
        print("G1 STOP — halted, not skipped:")
        for f, why in halted:
            print(f"   {f}  ({why})")
        sys.exit(3)
    if skipped:
        print(f"G1 STOP — {len(skipped)} skipped; must be 0"); sys.exit(3)
    if loaded + len(halted) != census:
        print(f"G1 STOP — loaded({loaded}) + halted({len(halted)}) != census({census})")
        sys.exit(3)
    models = sorted({v["model"] for v in store.values()})
    if len(models) != EXPECTED_MODELS:
        print(f"G1 STOP — {len(models)} distinct models, expected {EXPECTED_MODELS}")
        sys.exit(3)

    json.dump(store, open(os.path.join(OUT, "d5corpus.json"), "w", encoding="utf-8"),
              ensure_ascii=False, sort_keys=True)

    L = [f"G1 CENSUS ASSERT: census={census} loaded={loaded} skipped={len(skipped)} "
         f"halted={len(halted)} models={len(models)}  -> PASS",
         f"stray excluded from census, left untouched: {strays}",
         ""]
    dual = sorted({(v["spelling_as_collected"], v["family"])
                   for v in store.values() if v["dual_spelled"]})
    L.append(f"dual-spelling merge: 'minaria' -> 'minara' on {len(dual)} file(s): {dual}")
    L.append("")
    byf = {}
    for k, v in sorted(store.items()):
        byf.setdefault(v["family"], []).append(v)
    for fam in sorted(byf):
        L.append(f"[{fam}] {len(byf[fam])} files  prompt={FAMILIES[fam]}")
        for r in byf[fam]:
            n = len(r["data"]) if isinstance(r.get("data"), list) else (
                1 if isinstance(r.get("data"), dict) else 0)
            extra = ""
            if r["parse"] == "FAILED":
                extra = "  ERROR: " + r.get("error", "")
            elif r["parse"] != "clean":
                extra = f"  [{r['parse']}]"
            if r["dual_spelled"]:
                extra += f"  DUAL-SPELLED(as '{r['spelling_as_collected']}')"
            L.append(f"   {r['file']:30} items={n:3} {r['parse']:28}{extra}")
        L.append("")
    txt = "\n".join(L)
    open(os.path.join(OUT, "parse-table.txt"), "w", encoding="utf-8").write(txt)
    print(txt)


if __name__ == "__main__":
    main()
