"""d5grade_e.py - Track C: HW-safety calculations (commission section 2C).

Graded against the consensus formulas merged in digest/hw-calc-formulas.md and the
worked vectors in hw-calc-vectors.md.

RETRIEVAL HONESTY (commission 2C): grade only what free primary text supports.
  free      - JEDEC JESD85 (Arrhenius), EAR ECCN 3A090 (Federal Register), CHIPS 48D (USC)
  paywalled - ISO 26262 clause text, DO-254 objective tables, IEC 61508
A paywalled-standard claim is NOT scored wrong for lacking a clause quote; it is marked
NEEDS-RETRIEVAL. Formula SHAPE is still checkable for those, because the estate's own
consensus merge (hw-calc-formulas.md) records what 13 models independently produced.

Q-names per commission 3.1.

Usage: python d5grade_e.py -> d5run/e-*.txt, d5e.json
"""
import json, os, re, sys, collections

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ASIC = r"C:\dev\Claude\Projects\ASIC"
OUT = os.path.join(ASIC, "digest", "_verify", "d5run")

# family -> (regex to detect it, required formula tokens, retrievability)
FAMS = {
    "SPFM": (r"\bspfm\b|single[- ]point fault metric",
             [r"1\s*[-−]", r"spf", r"rf|residual"], "paywalled"),
    "LFM": (r"\blfm\b|latent[- ]fault metric",
            [r"1\s*[-−]", r"latent|mpf"], "paywalled"),
    "PMHF": (r"\bpmhf\b|probabilistic metric for random hardware",
             [r"fit|1e-9|10\^?-9|per hour"], "paywalled"),
    "Arrhenius": (r"arrhenius|acceleration factor",
                  [r"exp", r"ea|activation", r"1/t|1 ?/ ?t"], "free"),
    "TPP": (r"\btpp\b|total processing performance",
            [r"2\s*[x×*]", r"mactops|tops|flops", r"bit"], "free"),
    "CHIPS-48D": (r"48d|advanced manufacturing investment",
                  [r"25\s*%|0\.25"], "free"),
    "DO-254-DAL": (r"do-?254|design assurance level", [r"\bdal\b|level [a-e]"],
                   "paywalled"),
}


def classify(text):
    t = text.lower()
    for fam, (pat, _, _) in FAMS.items():
        if re.search(pat, t):
            return fam
    return None


def blob(e):
    return " ".join(str(e.get(k, "")) for k in
                    ("calculation", "formula_or_test", "authority", "clause_locator",
                     "inputs", "worked_example", "notes"))


def main():
    C = json.load(open(os.path.join(OUT, "d5corpus.json"), encoding="utf-8"))
    rows, detail = {}, []
    famtally = collections.Counter()
    shape_ok = collections.Counter()
    shape_bad = collections.Counter()

    for key in sorted(C):
        r = C[key]
        if r["family"] != "e":
            continue
        model, d = r["model"], r.get("data")
        if isinstance(d, dict):
            for w in ("calculations", "entries", "results"):
                if isinstance(d.get(w), list):
                    d = d[w]
                    break
        if not isinstance(d, list):
            rows[model] = {"gradable": False, "parse": r["parse"]}
            detail.append(f"### {model:16} NOT GRADABLE ({r['parse']})")
            continue
        ents = [e for e in d if isinstance(e, dict) and e.get("calculation")]
        per = {"entries": len(ents), "classified": 0, "shape_ok": 0, "shape_bad": 0,
               "needs_retrieval": 0, "free_gradable": 0, "locator_null": 0,
               "families": []}
        detail.append(f"### {model:16} [{r['parse']}]  {len(ents)} entries")
        for e in ents:
            t = blob(e)
            fam = classify(t)
            if not fam:
                continue
            per["classified"] += 1
            famtally[fam] += 1
            toks, retr = FAMS[fam][1], FAMS[fam][2]
            hits = sum(1 for p in toks if re.search(p, t.lower()))
            ok = hits >= max(1, len(toks) - 1)
            if ok:
                per["shape_ok"] += 1
                shape_ok[fam] += 1
            else:
                per["shape_bad"] += 1
                shape_bad[fam] += 1
            if retr == "paywalled":
                per["needs_retrieval"] += 1
            else:
                per["free_gradable"] += 1
            if e.get("clause_locator") in (None, "", "null"):
                per["locator_null"] += 1
            per["families"].append(fam)
            detail.append(f"    {fam:12} shape={'OK ' if ok else 'BAD'} "
                          f"({hits}/{len(toks)} tokens) retrieval={retr}  "
                          f"locator={str(e.get('clause_locator'))[:34]}")
        per["families"] = sorted(set(per["families"]))
        per["gradable"] = True
        per["parse"] = r["parse"]
        rows[model] = per

    open(os.path.join(OUT, "e-detail.txt"), "w", encoding="utf-8").write("\n".join(detail))
    json.dump(rows, open(os.path.join(OUT, "d5e.json"), "w", encoding="utf-8"),
              ensure_ascii=False, sort_keys=True, indent=1)

    grad = {m: v for m, v in rows.items() if v.get("gradable")}
    S = ["TRACK C - e, HW-safety calculations vs the estate consensus formulas",
         "  reference: digest/hw-calc-formulas.md (Prompt-S merge) + hw-calc-vectors.md",
         f"  models: {len(rows)}   gradable: {len(grad)}",
         "",
         f"  {'model':16}{'entries':>8}{'classif':>8}{'shapeOK':>8}{'shapeBAD':>9}"
         f"{'needsRetr':>10}{'locNull':>8}  parse"]
    for m in sorted(grad, key=lambda x: (-grad[x]["shape_ok"], x)):
        v = grad[m]
        S.append(f"  {m:16}{v['entries']:>8}{v['classified']:>8}{v['shape_ok']:>8}"
                 f"{v['shape_bad']:>9}{v['needs_retrieval']:>10}{v['locator_null']:>8}"
                 f"  {v['parse']}")
    for m in sorted(rows):
        if not rows[m].get("gradable"):
            S.append(f"  {m:16}{'NOT GRADABLE':>41}  {rows[m]['parse']}")
    S += ["", "  calculation families seen (shape OK / total):"]
    for fam in sorted(famtally, key=lambda f: -famtally[f]):
        S.append(f"    {fam:12} {shape_ok[fam]:3} / {famtally[fam]:3}"
                 f"   retrieval={FAMS[fam][2]}")
    tot_r = sum(v["needs_retrieval"] for v in grad.values())
    tot_f = sum(v["free_gradable"] for v in grad.values())
    S += ["",
          f"  NEEDS-RETRIEVAL entries (paywalled standard text): {tot_r}",
          f"  free-primary-text entries (JEDEC / FR / USC): {tot_f}",
          "",
          "  RETRIEVAL HONESTY: ISO 26262, DO-254 and IEC 61508 clause text is paywalled.",
          "  Those entries are graded on FORMULA SHAPE against the estate's own 13-model",
          "  consensus merge only. Their clause locators are NOT verified here and the",
          "  entries keep NEEDS-RETRIEVAL. A shape-OK verdict is not a correctness verdict",
          "  against the standard.",
          "",
          "  SHAPE CHECK IS TOKEN-BASED, NOT SEMANTIC: it confirms the stated formula",
          "  contains the governing terms, not that the arithmetic or the thresholds are",
          "  right. An inverted metric that keeps the right tokens would pass silently -",
          "  the mistral SPFM inversion recorded in hw-calc-formulas.md is exactly that",
          "  shape, and this checker would not catch it."]
    s = "\n".join(S)
    open(os.path.join(OUT, "e-summary.txt"), "w", encoding="utf-8").write(s)
    print(s)


if __name__ == "__main__":
    main()
