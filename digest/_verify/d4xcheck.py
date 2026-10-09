"""d4xcheck.py — commission DAY4-1 sections 2.3 / 2.4 and the addendum's per-model emission.

A. Section 2.4 "run the paid-for defect detector": grade the whole Day-4 corpus's recall
   of the two sentences memorial-3 corrected in extractions/Alpha21264.episodes.json,
   and of the numeric tokens its sweep could only match leniently.
B. Section 2.3 "convergence AND check": tally numeric claims per family across models,
   then check each against the paper instead of stopping at "N of M assert it".
C. Addendum: emit per-model, per-paper verdicts so a later TALLY-42 run can grade
   direction_check against each model's own prior recall without re-parsing.

Usage: python d4xcheck.py  -> d4run/xcheck-*.txt, d4run/d4permodel.json
"""
import json, os, re, sys, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from d4grade import denorm, dehyphen

ASIC = r"C:\dev\Claude\Projects\ASIC"
OUT = os.path.join(ASIC, "digest", "_verify", "d4run")
SRC = os.path.join(ASIC, "sources")

GT = {"alpha": "Alpha21264-pagemarked.txt", "niagara": "Niagara-pagemarked.txt",
      "p4": "Pentium4-pagemarked.txt", "pphysical": "POWER4-cpd-pagemarked.txt"}

# memorial-3's two corrected sentences: (label, paper-true value, the wrong value it held)
M3 = [("branch-predictor success rate", r"90%?\s*to\s*100%", r"\b5%\s*to\s*100%",
       "Alpha ep00 outcome, corrected 5% -> 90% on 2026-09-08"),
      ("line/way prediction accuracy", r"85%?\s*to\s*100%", r"\b95%\s*to\s*100%",
       "Alpha ep06 outcome, corrected 95% -> 85% on 2026-09-08")]

_c = {}
def src(fam):
    f = GT[fam]
    if f not in _c:
        n = denorm(open(os.path.join(SRC, f), encoding="utf-8", errors="replace").read())
        _c[f] = (n, dehyphen(n))
    return _c[f]


WORDNUM = {"1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six",
           "7": "seven", "8": "eight", "9": "nine", "10": "ten", "12": "twelve",
           "16": "sixteen", "20": "twenty", "32": "thirty-?two", "64": "sixty-?four"}


def unit_variants(u):
    """Singular/plural variants. Measured price of not having this: the Pentium 4 paper
    writes `20-stage`, Alpha writes `80-entry`, and a plural-only match returned a false
    NOT-FOUND on claims 6 of 15 and 3 of 15 models made correctly."""
    v = {u}
    if u.endswith("ies"):
        v.add(u[:-3] + "y")
    if u.endswith("es"):
        v.add(u[:-2])
    if u.endswith("s"):
        v.add(u[:-1])
    else:
        v.add(u + "s")
        v.add(u + "es")
    return sorted(v)


def paper_has(n, nh, val, unit):
    """Return (hits, how). Tries numeral and spelled-out forms, singular and plural,
    hyphenated and not. Every widening is recorded in `how` so a reader can see which
    match rescued the claim rather than trusting a bare boolean."""
    forms = [(re.escape(val), "numeral")]
    if val in WORDNUM:
        forms.append((WORDNUM[val], "spelled-out"))
    for uv in unit_variants(unit):
        for vpat, vhow in forms:
            pat = rf"{vpat}\s*-?\s*{re.escape(uv)}"
            h = len(re.findall(pat, n))
            if h:
                return h, f"{vhow}+'{uv}'"
            h = len(re.findall(pat, nh))
            if h:
                return h, f"{vhow}+'{uv}'+dehyphen"
    return 0, "none of numeral/spelled-out x singular/plural x dehyphen"


def blob(entry):
    return " ".join(str(entry.get(k, "")) for k in
                    ("decision", "rationale", "outcome", "quote_as_recalled", "title"))


def main():
    C = json.load(open(os.path.join(OUT, "d4corpus.json"), encoding="utf-8"))
    G = json.load(open(os.path.join(OUT, "d4grades.json"), encoding="utf-8"))
    out = []

    # ---------- A. memorial-3 sentences ----------
    out.append("=" * 78)
    out.append("A. SECTION 2.4 — corpus recall of the two sentences memorial-3 corrected")
    out.append("=" * 78)
    for label, right_pat, wrong_pat, prov in M3:
        n, _ = src("alpha")
        in_paper_right = len(re.findall(right_pat, n))
        in_paper_wrong = len(re.findall(wrong_pat, n))
        out.append(f"\n--- {label} ---")
        out.append(f"    provenance      : {prov}")
        out.append(f"    paper (normalised) matches /{right_pat}/ : {in_paper_right}")
        out.append(f"    paper (normalised) matches /{wrong_pat}/ : {in_paper_wrong}")
        say_right, say_wrong, silent = [], [], []
        for k, r in sorted(C.items()):
            if r["family"] != "alpha" or not isinstance(r.get("data"), list):
                continue
            t = denorm(" ".join(blob(e) for e in r["data"] if isinstance(e, dict)))
            if re.search(right_pat, t):
                say_right.append(r["model"])
            elif re.search(wrong_pat, t):
                say_wrong.append(r["model"])
            else:
                silent.append(r["model"])
        out.append(f"    corpus recalls PAPER-TRUE value : {len(say_right)} {sorted(say_right)}")
        out.append(f"    corpus recalls the WRONG value  : {len(say_wrong)} {sorted(say_wrong)}")
        out.append(f"    corpus silent on this sentence  : {len(silent)}")

    # ---------- B. convergence AND check ----------
    out.append("\n" + "=" * 78)
    out.append("B. SECTION 2.3 — numeric convergence, then checked against the paper")
    out.append("=" * 78)
    NUM = re.compile(r"\b(\d+(?:\.\d+)?)\s*(ghz|mhz|kb|kbyte|mbyte|mb|gb|w|nm|"
                     r"stage|stages|thread|threads|way|entry|entries|bit|bits|%)\b")
    for fam in ("alpha", "niagara", "p4", "pphysical"):
        n, nh = src(fam)
        claims = collections.defaultdict(set)
        for k, r in sorted(C.items()):
            if r["family"] != fam or not isinstance(r.get("data"), list):
                continue
            t = denorm(" ".join(blob(e) for e in r["data"] if isinstance(e, dict)))
            for m in NUM.finditer(t):
                claims[f"{m.group(1)} {m.group(2)}"].add(r["model"])
        nmodels = len({r["model"] for r in C.values() if r["family"] == fam})
        out.append(f"\n--- {fam}  ({nmodels} models, ground truth {GT[fam]}) ---")
        rows = sorted(claims.items(), key=lambda kv: -len(kv[1]))[:14]
        for claim, models in rows:
            if len(models) < 3:
                continue
            v, u = claim.split(" ", 1)
            hits, how = paper_has(n, nh, v, u)
            verdict = "IN-PAPER" if hits else "NOT-FOUND-IN-PAPER"
            out.append(f"    {len(models):2}/{nmodels} models say {claim:16} -> {verdict}"
                       f"  (hits {hits} via {how})")

    # ---------- C. per-model per-paper verdicts ----------
    out.append("\n" + "=" * 78)
    out.append("C. ADDENDUM — per-model per-paper recall verdicts (for TALLY-42 cross-grading)")
    out.append("=" * 78)
    perm = {}
    for key, g in sorted(G.items()):
        tiers = collections.Counter(e["tier"] for e in g["entries"])
        assertable = sum(v for t, v in tiers.items() if not t.startswith("T0"))
        verb = tiers.get("T1-verbatim", 0) + tiers.get("T1-verbatim-hyphen-variant", 0)
        # page_guess is a JOURNAL page (the D2 prompts ask for one and give the range);
        # page_found is a PDF page. Each extraction file's _locator_note states the offset.
        # Without it every non-Pentium4 family scores 0 and reads as a model failure when
        # it is a units mismatch in the checker.
        OFFSET = {"alpha": 23, "niagara": 20, "pphysical": 26, "p4": 0}
        off = OFFSET.get(g["family"], 0)
        pg = [(e["page_guess"], e["page_found"]) for e in g["entries"]
              if isinstance(e.get("page_guess"), (int, float)) and e.get("page_found")]
        near = sum(1 for a, b in pg if abs((a - off) - b) <= 2)
        perm[key] = {"model": g["model"], "paper": g["family"], "file": g["file"],
                     "entries": len(g["entries"]), "assertable_quotes": assertable,
                     "verbatim": verb, "paraphrase": tiers.get("T2-paraphrase-consistent", 0),
                     "contradicts_candidate": tiers.get("T3-contradicts-CANDIDATE", 0),
                     "not_found": tiers.get("T4-not-found", 0),
                     "declined": tiers.get("T0-declined", 0),
                     "page_guesses_scored": len(pg), "page_within_2": near}
    hdr = (f"{'model':16}{'paper':11}{'ent':>4}{'assert':>7}{'verb':>5}"
           f"{'para':>5}{'T3':>4}{'T4':>4}{'decl':>6}{'pg±2':>7}")
    out.append("\n" + hdr)
    for k in sorted(perm, key=lambda x: (perm[x]["paper"], perm[x]["model"])):
        p = perm[k]
        out.append(f"{p['model']:16}{p['paper']:11}{p['entries']:>4}{p['assertable_quotes']:>7}"
                   f"{p['verbatim']:>5}{p['paraphrase']:>5}{p['contradicts_candidate']:>4}"
                   f"{p['not_found']:>4}{p['declined']:>6}"
                   f"{str(p['page_within_2'])+'/'+str(p['page_guesses_scored']):>7}")
    json.dump(perm, open(os.path.join(OUT, "d4permodel.json"), "w", encoding="utf-8"),
              ensure_ascii=False, sort_keys=True, indent=1)

    txt = "\n".join(out)
    open(os.path.join(OUT, "xcheck.txt"), "w", encoding="utf-8").write(txt)
    print(txt)


if __name__ == "__main__":
    main()
