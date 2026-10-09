"""d4load.py — census-asserting loader for Web Model Tasks/Day 4 (DIGEST-COMMISSION-DAY4-1 G1/G3).

G1 INVERSION: an unrecognised family is a STOP, never a skip. Day-3's loader carried a
family allow-list and silently skipped 73 of 143 files; this one halts instead.
Asserts loaded + skipped == census and skipped == 0 before writing anything.

Salvage ladder with recorded parse classes (commission §4 "Keep"). CONTENT IS NEVER
REPAIRED: a file that yields no structure is recorded FAILED.

Family binding (commission §2.5): `power` is bound to the `alpha` family because
`yuanbao power.json` is yuanbao's Alpha 21264 answer under a truncated filename. The file
is NOT renamed; the misfile is carried as provenance on the record.

Usage:  python d4load.py            -> writes d4run/d4corpus.json + d4run/parse-table.txt
"""
import json, os, re, sys, glob, hashlib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ASIC = r"C:\dev\Claude\Projects\ASIC"
BASE = os.path.join(ASIC, "Web Model Tasks", "Day 4")
OUT = os.path.join(ASIC, "digest", "_verify", "d4run")
DEC = json.JSONDecoder()

# family -> (prompt file, pagemarked ground truth or None)
FAMILIES = {
    "alpha":     ("D2-ALPHA21264-RECALL.md",      "Alpha21264-pagemarked.txt"),
    "niagara":   ("D2-NIAGARA-RECALL.md",         "Niagara-pagemarked.txt"),
    "p4":        ("D2-PENTIUM4-RECALL.md",        "Pentium4-pagemarked.txt"),
    "pphysical": ("D2-POWER4-PHYSICAL-RECALL.md", "POWER4-cpd-pagemarked.txt"),
    "lvs":       ("F-LVS-MISMATCH-CLASSES.md",    None),
}
# as-collected filename family -> real family, with the reason carried onto the record
MISFILED = {
    "power": ("alpha",
              "yuanbao's Alpha 21264 answer under a truncated filename; page_guess values "
              "fall in Alpha's 24-36 journal range and content is Alpha (Ebox, clustered "
              "integer execution, integer issue queue). File NOT renamed: the as-collected "
              "name is the evidence of the collection defect. Commission DAY4-1 section 2.5."),
}

D2KEYS = ["title", "where_in_paper", "decision", "alternatives_or_rejected", "rationale",
          "outcome", "quote_as_recalled", "page_guess", "not_in_paper", "paper_vs_general",
          "weakest_point", "confidence"]


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
    """Forward scan; needed when the defect sits INSIDE element 0."""
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
    ("pair-in-array", lambda s: pair_in_array(strip_fence(s))),
    ("combined", lambda s: pair_in_array(escape_raw_newlines(fix_bad_escapes(strip_fence(s))))),
]


def load_one(path):
    raw = open(path, encoding="utf-8-sig").read()
    rec = {"chars": len(raw), "sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]}
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
        rec.update({"data": obj, "parse": name, "trailing": body[i + end:].strip()[:120],
                    "leading": body[:i].strip()[:120]})
        return rec
    # Partial recovery: run BOTH strategies and keep whichever recovers more.
    # Ordering matters and cost real entries: on `minimax m3 alpha.json` element-wise
    # stops at the first broken element and returns 2, while the forward harvest skips
    # the broken element and returns 4. Trying element-wise first and returning on
    # success silently under-reported that file by two entries.
    body = fix_bad_escapes(strip_fence(raw))
    i = body.find("[")
    ew = elementwise(body[i:]) if i >= 0 else None
    hv = harvest(body)
    cands = [(len(ew or []), "elementwise-truncation", ew),
             (len(hv or []), "harvest-skip-broken-element", hv)]
    cands.sort(key=lambda c: -c[0])
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
    files = sorted(glob.glob(os.path.join(BASE, "*.json")))
    census = len(files)
    store, skipped, halted = {}, [], []

    for p in files:
        stem = os.path.basename(p)[:-5]
        fam_raw = stem.rsplit(" ", 1)[-1]
        model = stem[: -(len(fam_raw) + 1)]
        misfile = None
        fam = fam_raw
        if fam_raw in MISFILED:
            fam, misfile = MISFILED[fam_raw]
        if fam not in FAMILIES:
            halted.append((os.path.basename(p), fam_raw))
            continue
        rec = load_one(p)
        rec.update({"file": os.path.basename(p), "model": model, "family": fam,
                    "family_as_collected": fam_raw, "misfile_provenance": misfile,
                    "prompt": FAMILIES[fam][0], "ground_truth": FAMILIES[fam][1]})
        store[f"{model}|{fam}"] = rec

    # ---- G1 assertions, before anything is written ----
    loaded = len(store)
    if halted:
        print("G1 STOP — unrecognised family, loader halts rather than skipping:")
        for f, fam in halted:
            print(f"   {f}  (family '{fam}')")
        sys.exit(3)
    if len(skipped) != 0:
        print(f"G1 STOP — {len(skipped)} files skipped; skipped must be 0")
        sys.exit(3)
    if loaded + len(skipped) != census:
        print(f"G1 STOP — loaded({loaded}) + skipped({len(skipped)}) != census({census})")
        sys.exit(3)

    json.dump(store, open(os.path.join(OUT, "d4corpus.json"), "w", encoding="utf-8"),
              ensure_ascii=False, sort_keys=True)

    lines = [f"G1 CENSUS ASSERT: census={census} loaded={loaded} skipped={len(skipped)} "
             f"halted={len(halted)}  -> PASS",
             ""]
    byfam = {}
    for k, v in sorted(store.items()):
        byfam.setdefault(v["family"], []).append(v)
    for fam in sorted(byfam):
        recs = byfam[fam]
        lines.append(f"[{fam}] {len(recs)} files  prompt={FAMILIES[fam][0]}  "
                     f"ground_truth={FAMILIES[fam][1] or 'NONE (no paper)'}")
        for r in recs:
            extra = ""
            if r["parse"] == "FAILED":
                extra = "  ERROR: " + r.get("error", "")
            elif r["parse"] != "clean":
                extra = f"  [{r['parse']}]"
            if r["misfile_provenance"]:
                extra += "  MISFILED-AS-COLLECTED"
            n = len(r["data"]) if isinstance(r.get("data"), list) else (
                1 if isinstance(r.get("data"), dict) else 0)
            lines.append(f"   {r['file']:34} items={n:3} {r['parse']:28}{extra}")
        lines.append("")
    pt = "\n".join(lines)
    open(os.path.join(OUT, "parse-table.txt"), "w", encoding="utf-8").write(pt)
    print(pt)


if __name__ == "__main__":
    main()
