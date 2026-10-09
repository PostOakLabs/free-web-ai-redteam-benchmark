"""d5grade_regz.py — Track A: exact recomputation of C1-REGZ-FACTOR (commission section 2A).

Zero heuristics, no overlap tunables. A model is right or wrong at 6 decimals.
Reference values are computed here with Decimal, never transcribed.

Q-names per commission section 3.1 (the T-names collide with the harvest rubric).

Usage: python d5grade_regz.py -> d5run/regz-detail.txt, regz-summary.txt, d5regz.json
"""
import json, os, re, sys
from decimal import Decimal as D

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ASIC = r"C:\dev\Claude\Projects\ASIC"
OUT = os.path.join(ASIC, "digest", "_verify", "d5run")

T23 = {"A": 124331, "B": 3730, "C": 24866, "D": 1243}
T24 = {"A": 130461, "B": 3914, "C": 26092, "D": 1305}
OFFICIAL_2025_A = 134841

# ---- reference, computed not transcribed -------------------------------------
FACTORS = {k: (D(T24[k]) / D(T23[k])).quantize(D("0.000001")) for k in "ABCD"}
PROJ = {k: int((D(T24[k]) * D("1.034")).to_integral_value(rounding="ROUND_HALF_UP"))
        for k in "ABCD"}
IMPLIED_A = (D(OFFICIAL_2025_A) / D(T24["A"])).quantize(D("0.000001"))
BP_GAP = ((IMPLIED_A - D("1.034")) * 10000).quantize(D("0.01"))
PROJ_GAP = OFFICIAL_2025_A - PROJ["A"]


def txt(entry):
    return " ".join(str(entry.get(k, "")) for k in ("steps", "answer", "note", "reasoning"))


def has(t, *forms):
    """VALUE comparison, not substring comparison.

    Every numeric token in the text is read as a number and compared to the reference
    at the reference's own precision. This is the only rule that gets all three cases
    right at once:

      1.033573251776393  -> CORRECT   (full precision; rounds to the 6dp reference)
      1.033573           -> CORRECT   (stated at reference precision)
      1.033574           -> WRONG     (deepseek's stated 6dp answer; the true value is
                                       1.03357325..., so this rounds the wrong way)

    Plain substring matching credited deepseek, because "1.033573" occurs inside its
    working value "1.0335735". Naive \\b anchoring then broke the six models that wrote
    the full-precision value. Neither is a text problem.
    """
    toks = re.findall(r"\d+(?:\.\d+)?", t.replace(",", ""))
    for f in forms:
        s = str(f)
        if "." in s:
            dp = len(s.split(".")[1])
            ref = D(s)
            for tok in toks:
                if "." not in tok:
                    continue
                try:
                    if D(tok).quantize(ref) == ref:
                        return True
                except Exception:
                    continue
        else:
            if any(tok == s for tok in toks):
                return True
    return False


def main():
    C = json.load(open(os.path.join(OUT, "d5corpus.json"), encoding="utf-8"))
    rows, detail = {}, []
    detail.append("REFERENCE (computed by this script, not transcribed)")
    detail.append(f"  task1 factors 6dp : " +
                  ", ".join(f"{k}={FACTORS[k]}" for k in "ABCD"))
    detail.append(f"  task2 proj x1.034 : " +
                  ", ".join(f"{k}={PROJ[k]}" for k in "ABCD"))
    detail.append(f"  task3 implied A   : {IMPLIED_A}  gap vs 1.034 = {BP_GAP} bp; "
                  f"projection {PROJ['A']} vs official {OFFICIAL_2025_A} = {PROJ_GAP}")
    detail.append("")

    for key in sorted(C):
        r = C[key]
        if r["family"] != "regz":
            continue
        model = r["model"]
        d = r.get("data")
        if not isinstance(d, list):
            rows[model] = {"parse": r["parse"], "gradable": False,
                           "t1": None, "t2": None, "t3_factor": None, "t3_bp": None,
                           "score": None,
                           "note": "PROSE-NOT-JSON" if r["parse"] == "FAILED" else r["parse"]}
            detail.append(f"### {model:16} NOT GRADABLE ({r['parse']})")
            continue
        blob = " ".join(txt(e) for e in d if isinstance(e, dict))
        blob = blob.replace(",", "")            # strip thousands separators once
        t1 = sum(1 for k in "ABCD" if has(blob, FACTORS[k]))
        t2 = sum(1 for k in "ABCD" if has(blob, PROJ[k]))
        t3f = has(blob, IMPLIED_A)
        t3b = has(blob, abs(BP_GAP), str(abs(BP_GAP)).rstrip("0").rstrip("."),
                  int(abs(BP_GAP)))
        score = t1 + t2 + (1 if t3f else 0)
        rows[model] = {"parse": r["parse"], "gradable": True, "t1": t1, "t2": t2,
                       "t3_factor": bool(t3f), "t3_bp": bool(t3b), "score": score,
                       "max": 9}
        detail.append(f"### {model:16} t1={t1}/4  t2={t2}/4  t3factor={'Y' if t3f else 'n'}"
                      f"  t3bp={'Y' if t3b else 'n'}  score={score}/9  [{r['parse']}]")
        miss1 = [k for k in "ABCD" if not has(blob, FACTORS[k])]
        miss2 = [k for k in "ABCD" if not has(blob, PROJ[k])]
        if miss1:
            detail.append(f"      task1 missing tiers: {miss1} (expected "
                          + ", ".join(f'{k}={FACTORS[k]}' for k in miss1) + ")")
        if miss2:
            detail.append(f"      task2 missing tiers: {miss2} (expected "
                          + ", ".join(f'{k}={PROJ[k]}' for k in miss2) + ")")

    open(os.path.join(OUT, "regz-detail.txt"), "w", encoding="utf-8").write(
        "\n".join(detail))
    json.dump(rows, open(os.path.join(OUT, "d5regz.json"), "w", encoding="utf-8"),
              ensure_ascii=False, sort_keys=True, indent=1)

    grad = {m: v for m, v in rows.items() if v["gradable"]}
    S = ["TRACK A — regz exact recomputation (C1-REGZ-FACTOR)",
         f"  models: {len(rows)}   gradable: {len(grad)}   not gradable: {len(rows)-len(grad)}",
         "",
         f"  {'model':16}{'t1/4':>6}{'t2/4':>6}{'t3f':>5}{'t3bp':>6}{'score/9':>9}  parse",
         ]
    for m in sorted(grad, key=lambda x: -grad[x]["score"]):
        v = grad[m]
        S.append(f"  {m:16}{v['t1']:>6}{v['t2']:>6}{'Y' if v['t3_factor'] else 'n':>5}"
                 f"{'Y' if v['t3_bp'] else 'n':>6}{v['score']:>9}  {v['parse']}")
    for m in sorted(rows):
        if not rows[m]["gradable"]:
            S.append(f"  {m:16}{'—':>6}{'—':>6}{'—':>5}{'—':>6}{'NOT GRADABLE':>9}  "
                     f"{rows[m]['note']}")
    perfect = [m for m, v in grad.items() if v["score"] == 9]
    S += ["", f"  exact on all 9 checked values: {len(perfect)} — {sorted(perfect)}",
          "",
          "  NOTE: this track is pure arithmetic. No overlap floor, no tunable, no",
          "  paraphrase tier — a value is present at 6dp or it is not."]
    s = "\n".join(S)
    open(os.path.join(OUT, "regz-summary.txt"), "w", encoding="utf-8").write(s)
    print(s)


if __name__ == "__main__":
    main()
