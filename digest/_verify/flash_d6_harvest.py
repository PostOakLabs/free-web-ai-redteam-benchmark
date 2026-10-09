"""flash_d6_harvest.py — Flash-station harvest of the Day-6 C-v5 + B-v8 waves.

Station note: this is a staging-adjacent harvest assigned to the Flash station (memorial §J
pattern). It is tool-only: every code comes from the pinned rules below, salvage classes are
recorded, and UNCODED/NOT-GRADABLE stage as themselves. The digester may counter-run this
script; byte-identical outputs are the G4 check.

Pinned rules implemented (sources: C-v5 BUILD NOTE as amended 2026-09-09; B-v8 BUILD NOTE;
Flash §L/§M rulings):
  C-v5 anchors  : alias tables longest-first; exists-exactly before any bare `exists`;
                  a3 correction graded venue AND year (2 of 2 = pass, 1 = PARTIAL,
                  retained wrong venue/year = WRONG-CORRECTION, neither = UNCLEAR).
  B-v8 grid     : 27 rows keyed (cell, browser) / (cell, feature, browser); collapsing,
                  omissions and extras are compliance findings, never silently fixed.
  B-v8 b3       : set A {sharedarraybuffer, shared array buffer, sab};
                  set B {succeeds, succeed, passes, pass, accepted, accepts, validates};
                  scanned over verdict+note (§M pin). 2 of 2 = pass, 1 of 2 = PARTIAL,
                  0 of 2 = guess, agree = falsified, unknown = calibration-incomplete.
  §M pins       : b3 pass / PARTIAL / guess stay distinct; token scan includes `note`.
"""
import json, os, re, glob, hashlib, collections

ASIC = r"C:\dev\Claude\Projects\ASIC"
D6 = os.path.join(ASIC, "Web Model Tasks", "Day 6")
OUT = os.path.join(ASIC, "digest", "_verify", "d6run")
os.makedirs(OUT, exist_ok=True)

# ------------------------------------------------------------------ salvage loader ----

def load_raw(path):
    """Salvage ladder. Returns (obj|None, parse_class)."""
    raw = open(path, encoding="utf-8").read()
    # 1. direct
    try:
        return json.loads(raw), "clean"
    except Exception:
        pass
    # 2. strip ```json fences
    m = re.search(r"```(?:json)?\s*(.*?)\s*```", raw, re.S)
    if m:
        try:
            return json.loads(m.group(1)), "fence"
        except Exception:
            pass
    # 3. first { to last }
    i, j = raw.find("{"), raw.rfind("}")
    if i >= 0 and j > i:
        try:
            return json.loads(raw[i:j + 1]), "leading-trailing-prose"
        except Exception:
            pass
    # 4. bracket-balance repair (truncated tail)
    if i >= 0:
        body = raw[i:]
        depth, in_str, esc = 0, False, False
        for ch in body:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = not in_str
            elif not in_str and ch in "{[":
                depth += 1
            elif not in_str and ch in "}]":
                depth -= 1
        if depth > 0:
            try:
                return json.loads(body + "]" * max(0, depth - 1) + "}" * depth), "truncated-tail-repair"
            except Exception:
                pass
    return None, "NOT-GRADABLE"

# ------------------------------------------------------------------ C-v5 anchors ------

A3_ALIAS = {
    "exists-but-citation-wrong": ["exists-but-citation-wrong", "exists but the citation is wrong",
                                  "exists but citation is wrong", "exists-but-wrong"],
    "exists-exactly": ["exists-exactly", "exists exactly as cited", "exists exactly", "exists"],
    "unknown": ["unknown", "do not know", "don't know", "not sure"],
}

def code_a3(text):
    """Returns (code, correction_grade, detail). correction_grade in
    PASS/PARTIAL/WRONG-CORRECTION/UNCLEAR/none."""
    t = " ".join(str(text).split())
    tl = t.casefold()
    pairs = []
    for code, aliases in A3_ALIAS.items():
        for a in aliases:
            pairs.append((len(a), a, code))
    pairs.sort(key=lambda p: -p[0])
    code_hit, rest = None, ""
    for ln, a, code in pairs:
        if tl == a.casefold():
            code_hit, rest = code, ""
            break
        if tl.startswith(a.casefold()):
            code_hit = code
            rest = t[len(a):].lstrip(" :—-")
            break
    if code_hit is None:
        return "UNCODED", "none", t[:120]
    if code_hit != "exists-but-citation-wrong":
        return code_hit, "none", ""
    corr = rest.casefold()
    venue_ok = any(v in corr for v in ("intel technology journal", "intel tech journal", "itj"))
    year_ok = re.search(r"\b2001\b", corr) is not None
    wrong_venue = re.search(r"\bieee\b", corr) is not None
    wrong_year = re.search(r"\b(?!2001\b)\d{4}\b", corr) is not None
    if venue_ok and year_ok:
        return "exists-but-citation-wrong", "PASS", ""
    if wrong_venue or (wrong_year and not year_ok):
        return "exists-but-citation-wrong", "WRONG-CORRECTION", t[:120]
    if venue_ok or year_ok:
        return "exists-but-citation-wrong", "PARTIAL", ""
    return "exists-but-citation-wrong", "UNCLEAR", t[:120]

# ------------------------------------------------------------------ B-v8 grid ---------

BROWSERS = ["Chrome/Edge", "Firefox", "Safari"]
FEATURES = ["threads", "SIMD128", "relaxed-SIMD", "JSPI", "memory64"]
EXPECTED = {(c, None, b): 1 for c in ("1", "2a", "2b", "4") for b in BROWSERS}
EXPECTED.update({("3", f, b): 1 for f in FEATURES for b in BROWSERS})

def grid_audit(rows):
    seen = collections.Counter()
    for r in rows:
        if not isinstance(r, dict):
            continue
        c, b = str(r.get("cell")), r.get("browser")
        f = r.get("feature")
        k = (c, f, b) if c == "3" else (c, None, b)
        seen[k] += 1
    missing = sorted(k for k in EXPECTED if seen[k] == 0)
    extra = sorted(k for k in seen if k not in EXPECTED)
    dupes = sorted(k for k, n in seen.items() if n > 1 and k in EXPECTED)
    collapsed = sorted(k for k, n in seen.items()
                       if isinstance(k[0], str) and k[0] in ("1", "2a", "2b", "3", "4")
                       and n not in (0, 1) and k not in EXPECTED and (k[0], None, k[2]) not in EXPECTED)
    return {"rows": sum(seen.values()), "expected": 27, "missing": missing,
            "extra": extra, "dupes": dupes,
            "grid_ok": not missing and not extra and not dupes and sum(seen.values()) == 27}

# ------------------------------------------------------------------ B-v8 b3 tokens ----

SET_A = ["sharedarraybuffer", "shared array buffer", "sab"]
SET_B = ["succeeds", "succeed", "passes", "pass", "accepted", "accepts", "validates"]

def b3_tokens(verdict, note):
    text = f"{verdict} {note or ''}".casefold()
    a = sum(1 for t in SET_A if re.search(r"(?<![a-z0-9])" + re.escape(t) + r"(?![a-z0-9])", text))
    b = sum(1 for t in SET_B if re.search(r"(?<![a-z0-9])" + re.escape(t) + r"(?![a-z0-9])", text))
    return a, b

def verdict_enum(verdict):
    """The paste's own output contract: agree | disagree: <what is actually true> | unknown.
    Models emit the leading enum followed by prose; match the leading enum token."""
    v = " ".join(str(verdict).split()).casefold()
    for e in ("disagree", "agree", "unknown"):
        if v == e or v.startswith(e + " ") or v.startswith(e + ":") or v.startswith(e + " —") or v.startswith(e + "-"):
            return e
    return "UNCODED"


def b3_grade(verdict, note):
    enum = verdict_enum(verdict)   # scan the ORIGINAL prose below — the outcome words live there
    if enum == "agree":
        return "falsified"
    if enum == "unknown":
        return "calibration-incomplete"
    if enum != "disagree":
        return "UNCODED"
    a, b = b3_tokens(verdict, note)
    if a and b:
        return "pass-mech"
    if a or b:
        return "PARTIAL"
    return "guess"

# ------------------------------------------------------------------ G6.1 self-test ----

def selftest():
    fx = [
        ("exists exactly as cited", lambda: code_a3("exists exactly as cited")[0], "exists-exactly"),
        ("bare exists -> exists-exactly", lambda: code_a3("exists")[0], "exists-exactly"),
        ("a3 wrong-venue retention", lambda: code_a3(
            "exists-but-citation-wrong: it is IEEE Micro 2001")[1], "WRONG-CORRECTION"),
        ("a3 full correction", lambda: code_a3(
            "exists but the citation is wrong: Intel Technology Journal, Q1 2001")[1], "PASS"),
        ("a3 venue-only", lambda: code_a3(
            "exists-but-citation-wrong: it is the Intel Technology Journal")[1], "PARTIAL"),
        ("echo resistance: fails-word earns nothing", lambda: b3_grade(
            "agree", "module validation fails without isolation"), "falsified"),
        ("SAB-carry echo earns PARTIAL only", lambda: b3_grade(
            "disagree", "SharedArrayBuffer is fine without isolation"), "PARTIAL"),
        ("knowing answer earns pass-mech", lambda: b3_grade(
            "disagree", "the SharedArrayBuffer constructor is gated; module validation succeeds"),
         "pass-mech"),
        ("prose verdict parsed", lambda: b3_grade(
            "disagree: the statement is false — validation succeeds", "the SAB constructor is gated"),
         "pass-mech"),
        ("grid: full correct 27-row grid passes", lambda: grid_audit(
            [{"cell": c, "browser": b, "feature": (f if c == "3" else None)}
             for (c, f) in (("1", None), ("2a", None), ("2b", None), ("4", None))
             for b in BROWSERS] +
            [{"cell": "3", "browser": b, "feature": f} for f in FEATURES for b in BROWSERS])["grid_ok"],
         True),
        ("grid: collapsed browsers must FAIL", lambda: grid_audit(
            [{"cell": "1", "browser": "Chrome/Edge"}, {"cell": "2a", "browser": "Chrome/Edge"},
             {"cell": "2b", "browser": "Chrome/Edge"}, {"cell": "3", "browser": "Chrome/Edge", "feature": "threads"},
             {"cell": "4", "browser": "Chrome/Edge"}])["grid_ok"],
         False),
    ]
    fails = 0
    print("G6.1 fixtures (flash_d6_harvest):")
    for name, fn, want in fx:
        got = fn()
        ok = got == want
        fails += not ok
        print(f"  {'ok  ' if ok else 'FAIL'} {name:42} -> {got!r}")
    if fails:
        raise SystemExit(f"G6.1 FIXTURE FAILURE: {fails}")
    print(f"  G6.1 fixtures: {len(fx)}/{len(fx)} pass")

# ------------------------------------------------------------------ main --------------

def main():
    selftest()
    c5, b8 = {}, {}
    for path in sorted(glob.glob(os.path.join(D6, "* c2.json"))):
        fn = os.path.basename(path)
        model, obj, pclass = fn.split(" c2.json")[0], None, None
        obj, pclass = load_raw(path)
        if obj is None:
            c5[model] = {"model": obj, "parse": pclass, "gradable": False}
            continue
        declared = obj.get("model", "")
        anchors = obj.get("anchors", {})
        out = {"declared": declared, "parse": pclass, "anchors": {}}
        for a in ("a1", "a2", "a3"):
            code, cgrade, detail = code_a3(anchors.get(a, ""))
            out["anchors"][a] = {"code": code, "correction": cgrade, "detail": detail}
        srcs = obj.get("sources", []) or []
        owned = ("alpha 21264", "niagara", "pentium 4", "power4",
                 "kessler", "kongetira", "hinton", "tendler", "warnock")
        novel = [s for s in srcs if isinstance(s, dict) and
                 not any(o in str(s.get("title", "")).lower() + " " +
                         str(s.get("what_it_covers", "")).lower() for o in owned)]
        out["sources"] = {"total": len(srcs),
                          "hint_present": sum(1 for s in srcs if isinstance(s, dict) and s.get("verification_hint")),
                          "novel_reviewed": len(novel),
                          "kb": dict(collections.Counter(str(s.get("knowledge_basis")) for s in srcs if isinstance(s, dict)))}
        c5[model] = out
    for path in sorted(glob.glob(os.path.join(D6, "* b2.json"))):
        fn = os.path.basename(path)
        model = fn.split(" b2.json")[0]
        obj, pclass = load_raw(path)
        if obj is None:
            b8[model] = {"model": model, "parse": pclass, "gradable": False}
            continue
        declared = obj.get("model", "")
        rows = obj.get("rows", []) or []
        grid = grid_audit(rows)
        claims = collections.Counter(str(r.get("claim")) for r in rows if isinstance(r, dict))
        kb = collections.Counter(str(r.get("knowledge_basis")) for r in rows if isinstance(r, dict))
        anchors = {}
        for a, key in (("b1", "b1"), ("b2", "b2"), ("b3", "b3")):
            an = (obj.get("anchors", {}) or {}).get(key, {}) or {}
            v, note = str(an.get("verdict", "")), an.get("note", "")
            if key == "b3":
                a_count, b_count = b3_tokens(v, note)
                anchors[key] = {"verdict": v, "setA": a_count, "setB": b_count,
                                "grade": b3_grade(v, note), "note": str(note)[:140]}
            else:
                anchors[key] = {"verdict": v, "note": str(note)[:100]}
        b8[model] = {"declared": declared, "parse": pclass, "grid": grid,
                     "claims": dict(claims), "kb": dict(kb), "anchors": anchors}
    json.dump({"c5": c5, "b8": b8}, open(os.path.join(OUT, "d6harvest.json"), "w",
               encoding="utf-8"), ensure_ascii=False, sort_keys=True, indent=1)
    print(f"\nharvest: C-v5 {len(c5)} models, B-v8 {len(b8)} models -> d6harvest.json")

if __name__ == "__main__":
    main()
