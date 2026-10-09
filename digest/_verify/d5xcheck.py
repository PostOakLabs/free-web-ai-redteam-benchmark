"""d5xcheck.py - Track D: red-team verdict harvest, calibration wave, cross-model matrix
(commission section 2D and section 3.5/3.6).

Verified block identities (commission 2D):
  red1 = every model reviewing RUNSHEET-34 Block 01 (BoomTile) - the exemplar baked
         into J-ISSUE-REDTEAM-V1 itself
  red3 = every model reviewing RUNSHEET-42 Block 08 (Niagara thread-rich) - the
         exemplar baked into J-EPISODE-REDTEAM-V3, the block marked CALIBRATION

Both are CALIBRATION waves on a single block, not surveys. Consequences, stated on
every page that uses them:
  * `direction_check` is OUT OF SCOPE - one block gives no direction spread to compare.
  * J-v3's BUILD NOTE declares Block 08 known-SOUND-with-known-gaps, so a bare SOUND
    with zero objections is MISCALIBRATED by the prompt's own definition. J-v1 says the
    same of Block 01 (known-imperfect: unmeasured post_state, the #5971 deferral).

Emits d5permodel.json - the per-model x per-track calibration feed (commission 3.6).

Usage: python d5xcheck.py -> d5run/redteam-*.txt, d5permodel.json
"""
import json, os, re, sys, collections

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ASIC = r"C:\dev\Claude\Projects\ASIC"
OUT = os.path.join(ASIC, "digest", "_verify", "d5run")

VERDICTS = ["SOUND", "SOUND-WITH-RESERVATIONS", "SUSPECT",
            "IMPLAUSIBLE-FOR-THIS-RECORD", "IMPLAUSIBLE-FOR-THIS-PAPER"]
SHORT = {"SOUND": "SOUND", "SOUND-WITH-RESERVATIONS": "S-W-RES", "SUSPECT": "SUSPECT",
         "IMPLAUSIBLE-FOR-THIS-RECORD": "IMPLAUS", "IMPLAUSIBLE-FOR-THIS-PAPER": "IMPLAUS"}
# fields each prompt's review schema carries
FIELDS = {"red1": ["mechanism_check", "evidence_check", "attribution_check",
                   "missing_from_story", "most_defensible_part"],
          "red3": ["direction_check", "quote_plausibility",
                   "missing_from_story", "most_defensible_part"]}
BLOCK = {"red1": "RUNSHEET-34 Block 01 (BoomTile) - J-v1's own exemplar, known-imperfect",
         "red3": "RUNSHEET-42 Block 08 (Niagara) - J-v3's own exemplar, known-SOUND"}


def one(d):
    """A review is a single object. Salvage may hand back a list; take the first
    element that carries a verdict, and record if more than one was present."""
    if isinstance(d, dict):
        return d, 1
    if isinstance(d, list):
        cands = [x for x in d if isinstance(x, dict) and "verdict" in x]
        if cands:
            return cands[0], len(cands)
        if d and isinstance(d[0], dict):
            return d[0], len(d)
    return None, 0


def norm_verdict(v):
    """Match LONGEST enum first. 'SOUND-WITH-RESERVATIONS'.startswith('SOUND') is true,
    so a shortest-first scan silently collapses every reserved verdict into SOUND and
    invents a corpus-wide bare-SOUND miscalibration that is not there."""
    if not isinstance(v, str):
        return None
    u = v.strip().upper().replace("_", "-")
    for k in sorted(VERDICTS, key=len, reverse=True):
        if u.startswith(k):
            return k
    return u[:40] or None


def main():
    C = json.load(open(os.path.join(OUT, "d5corpus.json"), encoding="utf-8"))
    harvest = {"red1": {}, "red3": {}}
    detail = []

    for key in sorted(C):
        r = C[key]
        fam = r["family"]
        if fam not in ("red1", "red3"):
            continue
        model = r["model"]
        obj, n_objs = one(r.get("data"))
        if obj is None:
            harvest[fam][model] = {"gradable": False, "parse": r["parse"]}
            detail.append(f"{fam} {model:16} NOT GRADABLE ({r['parse']})")
            continue
        verdict = norm_verdict(obj.get("verdict"))
        objections = obj.get("objections")
        objections = objections if isinstance(objections, list) else []
        sev = collections.Counter(
            str(o.get("severity", "")).lower() for o in objections if isinstance(o, dict))
        present = [f for f in FIELDS[fam] if f in obj]
        missing = [f for f in FIELDS[fam] if f not in obj]
        # calibration class, per the prompts' own BUILD NOTEs
        bare_sound = (verdict == "SOUND" and len(objections) == 0)
        sound_with_obj = (verdict == "SOUND" and len(objections) > 0)
        res_no_obj = (verdict == "SOUND-WITH-RESERVATIONS" and len(objections) == 0)
        cal = ("MISCALIBRATED-bare-SOUND" if bare_sound else
               "SCHEMA-ANOMALY-SOUND-with-objections" if sound_with_obj else
               "SCHEMA-ANOMALY-reservations-without-objections" if res_no_obj else
               "consistent")
        harvest[fam][model] = {
            "gradable": True, "parse": r["parse"], "verdict": verdict,
            "verdict_short": SHORT.get(verdict, verdict), "objections": len(objections),
            "fatal": sev.get("fatal", 0), "major": sev.get("major", 0),
            "minor": sev.get("minor", 0), "fields_present": present,
            "fields_missing": missing, "calibration": cal,
            "extra_review_objects": n_objs - 1,
            "claims_attacked": [str(o.get("claim_attacked", ""))[:70]
                                for o in objections if isinstance(o, dict)],
        }
        detail.append(f"{fam} {model:16} {SHORT.get(verdict,verdict):8} "
                      f"obj={len(objections)} f/m/n={sev.get('fatal',0)}/"
                      f"{sev.get('major',0)}/{sev.get('minor',0)}  {cal}"
                      + (f"  MISSING={missing}" if missing else ""))

    json.dump(harvest, open(os.path.join(OUT, "d5redteam.json"), "w", encoding="utf-8"),
              ensure_ascii=False, sort_keys=True, indent=1)
    open(os.path.join(OUT, "redteam-detail.txt"), "w", encoding="utf-8").write(
        "\n".join(detail))

    # ---------- summary + cross-model matrix ----------
    S = ["TRACK D - red-team calibration wave (red1 + red3)"]
    for fam in ("red1", "red3"):
        h = harvest[fam]
        g = {m: v for m, v in h.items() if v.get("gradable")}
        S += ["", f"=== {fam}: {BLOCK[fam]} ===",
              f"  models: {len(h)}   gradable: {len(g)}",
              "",
              f"  {'model':16}{'verdict':10}{'obj':>4}{'fatal':>6}{'major':>6}"
              f"{'minor':>6}  calibration"]
        for m in sorted(g, key=lambda x: (g[x]["verdict_short"], x)):
            v = g[m]
            S.append(f"  {m:16}{v['verdict_short']:10}{v['objections']:>4}"
                     f"{v['fatal']:>6}{v['major']:>6}{v['minor']:>6}  {v['calibration']}")
        for m in sorted(h):
            if not h[m].get("gradable"):
                S.append(f"  {m:16}{'NOT GRADABLE':10}{'':>22}  parse={h[m]['parse']}")
        vc = collections.Counter(v["verdict_short"] for v in g.values())
        S.append(f"  verdict spread: {dict(vc)}")
        bare = [m for m, v in g.items() if v["calibration"].startswith("MISCALIBRATED")]
        anom = [(m, v["calibration"]) for m, v in g.items()
                if v["calibration"].startswith("SCHEMA-ANOMALY")]
        S.append(f"  bare-SOUND (miscalibrated per the prompt's own BUILD NOTE): "
                 f"{len(bare)} {sorted(bare)}")
        S.append(f"  schema anomalies: {len(anom)} {sorted(anom)}")
        miss = {m: v["fields_missing"] for m, v in g.items() if v["fields_missing"]}
        S.append(f"  models omitting a required review field: {len(miss)} {miss}")
        # convergence: which claims did models attack
        words = collections.Counter()
        for v in g.values():
            for c in v["claims_attacked"]:
                for w in re.findall(r"[a-z_]{5,}", c.lower()):
                    words[w] += 1
        S.append(f"  most-attacked claim tokens: "
                 f"{[w for w, n in words.most_common(8) if n >= 3]}")

    S += ["", "=== SCOPE NOTES, on every page that uses this wave ===",
          "  * direction_check is OUT OF SCOPE on a single-block wave: one block gives no",
          "    direction spread to grade. The column is not left blank-and-unexplained.",
          "  * Both blocks are the prompts' OWN exemplars, so these waves measure reviewer",
          "    calibration, not corpus quality. They are not evidence about the episodes.",
          "  * The topic-anchor fabrication probe (commission 3.4) does not apply here:",
          "    these families carry no recalled quotes to test for fabrication.",
          "  * Contradiction detection elsewhere in this digest is numeric-only, so a",
          "    direction reversal would pass silently."]
    s = "\n".join(S)
    open(os.path.join(OUT, "redteam-summary.txt"), "w", encoding="utf-8").write(s)
    print(s)

    # ---------- per-model calibration feed (commission 3.6) ----------
    regz = json.load(open(os.path.join(OUT, "d5regz.json"), encoding="utf-8"))
    strings = json.load(open(os.path.join(OUT, "d5strings.json"), encoding="utf-8"))
    ecalc = json.load(open(os.path.join(OUT, "d5e.json"), encoding="utf-8"))
    models = sorted({v["model"] for v in C.values()})
    feed = {}
    for m in models:
        feed[m] = {
            "regz": regz.get(m), "strings": strings.get(m), "e": ecalc.get(m),
            "red1": harvest["red1"].get(m), "red3": harvest["red3"].get(m),
            "dual_spelled": any(v.get("dual_spelled") for v in C.values()
                                if v["model"] == m),
            "spellings_as_collected": sorted({v["spelling_as_collected"]
                                              for v in C.values() if v["model"] == m}),
        }
    json.dump(feed, open(os.path.join(OUT, "d5permodel.json"), "w", encoding="utf-8"),
              ensure_ascii=False, sort_keys=True, indent=1)
    print(f"\nwrote d5permodel.json: {len(feed)} models x 5 tracks")


if __name__ == "__main__":
    main()
