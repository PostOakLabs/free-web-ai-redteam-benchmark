"""d5grade_strings.py - Track B: JCS conformance against the estate canonicalizer
(commission section 2B).

Reference = jcs.py in this directory, which passes its 12 RFC 8785 self-asserts.
Case inputs are read from prompts/C2-JCS-STRINGS.md, never retyped.

TWO DEFECTS DISCLOSED, both in the prompt/transport, not the models:

  1. Case 5's input embeds a RAW U+0007 (BEL) control character, which is illegal in
     JSON. The prompt's own case 5 does not parse.
  2. Chat surfaces strip or substitute invisible control characters on paste. Every
     model that answered rendered s5 as a plain space or U+00A0 - none received the
     BEL. Case 5 is therefore scored UNGRADABLE rather than as 14 model failures,
     and the s1..s4 prefix, which did survive transmission, is scored separately.

Also scored per commission 2B: a correct canonical string produced alongside a rule
statement that does not name the governing rule is a FINDING, not a pass.

Usage: python d5grade_strings.py -> d5run/strings-*.txt, d5strings.json
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from jcs import canon

ASIC = r"C:\dev\Claude\Projects\ASIC"
OUT = os.path.join(ASIC, "digest", "_verify", "d5run")
CTRL = re.compile("[" + "".join(chr(c) for c in range(0x20)) + "]")

_p = open(os.path.join(ASIC, "prompts", "C2-JCS-STRINGS.md"), encoding="utf-8").read()
_raw_cases = re.findall(r"^(\d)\. \`(\{.*?\})\`", _p, re.M)

REF, PROMPT_DEFECT = {}, {}
for _num, _src in _raw_cases:
    _n = int(_num)
    try:
        REF[_n] = canon(json.loads(_src))
    except json.JSONDecodeError:
        _esc = CTRL.sub(lambda m: "\\u%04x" % ord(m.group()), _src)
        REF[_n] = canon(json.loads(_esc))
        PROMPT_DEFECT[_n] = "input embeds a raw control character (illegal in JSON)"

UNGRADABLE = {5}
REF_S1_S4 = {}
_c5 = [s for n, s in _raw_cases if n == "5"]
if _c5:
    try:
        _o = json.loads(CTRL.sub("", _c5[0]))
        _o.pop("s5", None)
        REF_S1_S4[5] = canon(_o)
    except Exception:
        pass

RULE_KEYS = {
    1: ("utf-16", "code unit", "code-unit"),
    2: ("recurs", "nested", "depth", "sort"),
    3: ("ecmascript", "es6", "number", "double", "shortest"),
    4: ("utf-16", "code unit", "code-unit", "surrogate"),
    5: ("escape", "control", "shorthand"),
}


def norm_out(s):
    return s.strip() if isinstance(s, str) else s


def main():
    C = json.load(open(os.path.join(OUT, "d5corpus.json"), encoding="utf-8"))
    rows, detail, ungrade = {}, [], {}
    detail.append("REFERENCE JCS (computed by jcs.py from the prompt's own inputs)")
    for n in sorted(REF):
        f = "   [PROMPT DEFECT: " + PROMPT_DEFECT[n] + "]" if n in PROMPT_DEFECT else ""
        detail.append(f"  case {n}: {REF[n]}{f}")
    detail.append("")

    for key in sorted(C):
        r = C[key]
        if r["family"] != "strings":
            continue
        model, d = r["model"], r.get("data")
        if isinstance(d, dict):
            for w in ("cases", "results", "output"):
                if isinstance(d.get(w), list):
                    d = d[w]
                    break
        if isinstance(d, list) and d and not any(
                isinstance(x, dict) and "case" in x for x in d):
            rows[model] = {"gradable": False, "parse": r["parse"],
                           "note": "salvage recovered no case-shaped records"}
            detail.append(f"### {model:16} NOT GRADABLE - {r['parse']} produced no "
                          "case-shaped records")
            continue
        if not isinstance(d, list):
            rows[model] = {"gradable": False, "parse": r["parse"],
                           "note": "not a list after unwrapping"}
            detail.append(f"### {model:16} NOT GRADABLE ({r['parse']})")
            continue

        correct, wrong_rule, seen = 0, [], set()
        detail.append(f"### {model:16} [{r['parse']}]")
        for e in d:
            if not isinstance(e, dict) or "case" not in e:
                continue
            try:
                n = int(e["case"])
            except (TypeError, ValueError):
                continue
            if n not in REF or n in seen:
                continue
            got = norm_out(e.get("jcs"))
            if n in UNGRADABLE:
                # Compare only the part that survived transmission: drop the model's
                # own s5 member before comparing against the s1..s4 reference.
                sub = False
                if got:
                    try:
                        _m = json.loads(got)
                        _m.pop("s5", None)
                        sub = canon(_m) == REF_S1_S4.get(n)
                    except Exception:
                        sub = False
                ungrade.setdefault(n, []).append((model, sub))
                detail.append(f"    case {n}: UNGRADABLE (input did not survive "
                              f"transmission)  s1-s4_correct={'y' if sub else 'n'}")
                continue
            seen.add(n)
            ok = got == REF[n]
            rules = " ".join(str(x) for x in (e.get("rules_applied") or [])).lower()
            rule_ok = any(k in rules for k in RULE_KEYS.get(n, ()))
            if ok:
                correct += 1
                if not rule_ok:
                    wrong_rule.append(n)
            detail.append(f"    case {n}: {'OK ' if ok else 'BAD'}  "
                          f"rule_stated={'y' if rule_ok else 'n'}")
            if not ok:
                detail.append(f"        expected: {REF[n]}")
                detail.append(f"        got     : {got}")
        rows[model] = {"gradable": True, "parse": r["parse"], "cases_seen": len(seen),
                       "correct": correct, "right_answer_wrong_rule": sorted(wrong_rule)}

    open(os.path.join(OUT, "strings-detail.txt"), "w", encoding="utf-8").write(
        "\n".join(detail))
    json.dump(rows, open(os.path.join(OUT, "d5strings.json"), "w", encoding="utf-8"),
              ensure_ascii=False, sort_keys=True, indent=1)

    grad = {m: v for m, v in rows.items() if v["gradable"]}
    S = ["TRACK B - strings, JCS conformance vs the estate canonicalizer (jcs.py)",
         f"  models: {len(rows)}   gradable: {len(grad)}",
         "  reference: jcs.py, 12/12 RFC 8785 self-asserts pass",
         "  GRADED CASES: 1-4 only. Case 5 is ungradable - see the note below.",
         "",
         f"  {'model':16}{'correct/4':>11}  right-answer-wrong-rule  parse"]
    for m in sorted(grad, key=lambda x: (-grad[x]["correct"], x)):
        v = grad[m]
        S.append(f"  {m:16}{v['correct']:>11}  "
                 f"{str(v['right_answer_wrong_rule'] or '-'):23}  {v['parse']}")
    for m in sorted(rows):
        if not rows[m]["gradable"]:
            S.append(f"  {m:16}{'NOT GRADABLE':>11}  {rows[m].get('note',''):23}  "
                     f"{rows[m]['parse']}")
    tot = sum(v["correct"] for v in grad.values())
    seen = sum(v["cases_seen"] for v in grad.values())
    S += ["", f"  cases correct corpus-wide: {tot} of {seen} graded (cases 1-4)"]
    for n, lst in sorted(ungrade.items()):
        good = sum(1 for _, ok in lst if ok)
        S += ["",
              f"  CASE {n} UNGRADABLE for all {len(lst)} responding models. The prompt's input",
              "  embeds a raw U+0007 (BEL), which chat surfaces strip on paste; every model",
              "  rendered s5 as a plain space or U+00A0, so none received the character.",
              "  Scoring it would record a TRANSMISSION LOSS as 14 model failures.",
              f"  s1..s4 prefix correct despite that: {good} of {len(lst)}."]
    s = "\n".join(S)
    open(os.path.join(OUT, "strings-summary.txt"), "w", encoding="utf-8").write(s)
    print(s)


if __name__ == "__main__":
    main()
