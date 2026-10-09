"""tallycodes.py — the pinned coding scheme for TALLY-34 and TALLY-42.

WHY THIS EXISTS
    Flash §H: the rules "existed as intent and never as an executable specification."
    TALLY-34/42 defined Mech/Evid/Attr, Dir/Quote, verdict, severity and the calibration
    classes in PROSE. 76 blocks of verdicts were about to land against unpinned intent.
    This module is the executable specification. The prose tables in the two TALLY files
    are now documentation of this file, not the other way round.

DESIGN RULES, each traceable to a defect this estate actually paid for

    1. EXACT ENUM, LONGEST-FIRST.  `"SOUND-WITH-RESERVATIONS".startswith("SOUND")` is
       true. A shortest-first scan collapsed every reserved verdict into SOUND and
       inverted a whole published table (Day-5 Track D). Matching is longest-alias-first,
       always.

    2. UNCODED IS A VALUE, NOT A ZERO.  Anything the codebook cannot place returns
       UNCODED with the raw text preserved. It is never silently dropped, never coerced
       to a neighbouring code, and never counted as a pass. `UNCODED` in a tally column
       means "the codebook did not cover this", which is a finding about the codebook.

    3. ESCAPES ARE PASSES.  N-D (record-side) and N-J (paper-side) are the prompts' own
       sanctioned field-level escapes. They are codes in good standing, not gaps.

    4. NO SUBSTRING CREDIT.  Codes match on normalised whole tokens or on explicit
       phrase aliases, never on "the code appears somewhere in the sentence".

    5. A NEGATED POSITIVE EARNS NO CODE.  Rule 4's negation variant, found by the Flash
       G6.6(c) vet: `"not sound"` coded SOUND, `"not measured"` coded MEAS while its
       synonym `"unmeasured"` coded ASSERT, and `"does not match the paper"` coded
       MATCHES -- while `"does not match -- reads like a transplant"` coded TRANSPLANT
       by longest-alias luck, so one semantic coded two ways. A positive alias with a
       negator in the 3 tokens before it is SKIPPED and scanning continues. Where the
       negated form has a real code the table carries it as an explicit alias (mech
       `"does not hold"` -> BREAKS, evid `"not measured"` -> ASSERT); an alias that
       contains its own negator is matched whole and is never tripped by this rule.
       Everything else falls to UNCODED, which is rule 2's safe direction -- a finding
       about the codebook beats a confident wrong code.

    6. NO SILENT DEFAULT ON block_class.  `calibration()` normalises, then RAISES on
       anything outside its three-value contract. The vet found `"Known-Sound"` and
       `None` returning `consistent`. That does not produce a wrong finding -- it MASKS
       a real one, silently, in the one function whose whole job is to find it.

Public API
    code_verdict(text, sheet)   -> (code, basis)
    code_field(field, text)     -> (code, basis)      field in mech|evid|attr|dir|quote
    code_severity(objections)   -> {"fatal": n, "major": n, "minor": n, "uncoded": n}
    calibration(verdict, n_obj, block_class) -> (code, why)
    selftest()                  -> runs G6.1 fixtures; raises on any failure

Run `python tallycodes.py` to execute the fixture suite (G6.1) and print the differential
sample stub required by G6.6(c).
"""
import re, sys, unicodedata

# ---------------------------------------------------------------- normalisation ----


def norm(t):
    """Casefold, collapse whitespace, unify dashes. NOT hyphen-stripping: `S-W-RES` and
    `SWRES` are different tokens and conflating them is how alias tables rot."""
    if not isinstance(t, str):
        return ""
    t = unicodedata.normalize("NFKC", t)
    t = re.sub(r"[‐-―]", "-", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip().casefold()


NEGATORS = ("not", "never", "no", "nor", "cannot", "neither")
_NEG_WINDOW = 3


def _negated(n, start):
    """True if a negator sits in the `_NEG_WINDOW` tokens before position `start` -- rule 5.

    The window is deliberately generous. Over-rejecting yields UNCODED, which rule 2
    treats as a finding about the codebook; under-rejecting yields a confident wrong
    code, which is the defect being fixed. The asymmetry is the whole point.
    """
    toks = re.findall(r"[a-z0-9'-]+", n[:start])
    return any(t in NEGATORS or t.endswith("n't") for t in toks[-_NEG_WINDOW:])


def _match(text, table):
    """Longest-alias-first whole-token match. Returns (code, alias) or (None, None).

    Aliases are sorted by length descending BEFORE matching -- rule 1. A tie in length
    is resolved by the alias string, so the scan order is total and deterministic and
    does not depend on dict insertion order.

    The boundary lookarounds are rule 4: `unmeasurable` never earns MEAS. The negation
    skip is rule 5: a matched alias with a negator in front of it is passed over and the
    scan continues, so `"does not match -- reads like a transplant"` reaches TRANSPLANT
    by rule rather than by luck.
    """
    n = norm(text)
    if not n:
        return None, None
    pairs = [(a, c) for c, aliases in table.items() for a in aliases]
    pairs.sort(key=lambda p: (-len(p[0]), p[0]))
    for alias, code in pairs:
        a = norm(alias)
        m = re.search(r"(?<![a-z0-9-])" + re.escape(a) + r"(?![a-z0-9-])", n)
        if not m or _negated(n, m.start()):
            continue
        return code, alias
    return None, None


UNCODED = "UNCODED"

# ---------------------------------------------------------------- verdicts --------
# TALLY-34 (JI-v1, record-side) and TALLY-42 (J-v3, paper-side) share three codes and
# differ in the fourth. Kept as separate tables so a paper-side IMPLAUS can never be
# recorded on a record-side sheet.
_VERDICT_COMMON = {
    "S-W-RES": ["sound-with-reservations", "sound with reservations", "s-w-res"],
    "SOUND": ["sound"],
    "SUSPECT": ["suspect"],
}
VERDICT = {
    "34": dict(_VERDICT_COMMON, **{
        "IMPLAUS": ["implausible-for-this-record", "implausible for this record", "implaus"]}),
    "42": dict(_VERDICT_COMMON, **{
        "IMPLAUS": ["implausible-for-this-paper", "implausible for this paper", "implaus"]}),
}

# ---------------------------------------------------------------- field codes -----
FIELD = {
    "mech": {
        "HOLDS": ["holds", "causal chain closes", "chain closes", "plausibly produces"],
        "BREAKS": ["breaks", "does not hold", "chain breaks", "does not produce"],
        "N-D": ["not-determinable-from-this-record", "not determinable", "n-d"],
    },
    "evid": {
        "MEAS": ["measured", "meas", "re-measured", "quantified"],
        # "not measured" and "not quantified" are explicit negated aliases (rule 5): the
        # negated form of MEAS has a real code, and its synonym "unmeasured" already
        # carried it. Without these the two synonyms coded to opposite values.
        "ASSERT": ["asserted", "assert", "merely asserted", "claimed", "unmeasured",
                   "not measured", "not quantified", "not re-measured"],
        "N-D": ["not-determinable-from-this-record", "not determinable", "n-d"],
    },
    "attr": {
        "SUPPORTS": ["supports", "supported", "named + dated + locator"],
        "WEAK": ["weak", "does not carry", "does not support the claim"],
        "ABSENT": ["absent", "no quote", "no direct_quote", "none"],
        "N-D": ["not-determinable-from-this-record", "not determinable", "n-d"],
    },
    "dir": {
        "MATCHES": ["matches", "match", "consistent with the paper"],
        "REVERSAL": ["reversal", "reversed", "opposite direction"],
        "TRANSPLANT": ["transplant", "general knowledge", "general-knowledge transplant"],
        "N-J": ["cannot-judge-without-the-paper", "cannot judge", "n-j"],
    },
    "quote": {
        "PAPER-LIKE": ["paper-like", "paper like", "reads like the paper"],
        "PARAPHRASE": ["paraphrase", "dressed as a quote", "paraphrased"],
        "FRAGMENT": ["fragment", "mid-phrase", "judgment withheld"],
        "N-J": ["cannot-judge-without-the-paper", "cannot judge", "n-j"],
    },
}

SEVERITY = {"fatal": ["fatal"], "major": ["major"], "minor": ["minor"]}

# ---------------------------------------------------------------- API -------------


def code_verdict(text, sheet):
    if sheet not in VERDICT:
        raise ValueError(f"sheet must be '34' or '42', got {sheet!r}")
    c, a = _match(text, VERDICT[sheet])
    return (c, a) if c else (UNCODED, str(text)[:80])


def code_field(field, text):
    if field not in FIELD:
        raise ValueError(f"unknown field {field!r}")
    c, a = _match(text, FIELD[field])
    return (c, a) if c else (UNCODED, str(text)[:80])


def code_severity(objections):
    out = {"fatal": 0, "major": 0, "minor": 0, "uncoded": 0}
    for o in objections or []:
        if not isinstance(o, dict):
            out["uncoded"] += 1
            continue
        c, _ = _match(o.get("severity", ""), SEVERITY)
        out[c if c else "uncoded"] += 1
    return out


BLOCK_CLASSES = ("known-sound", "known-imperfect", "unknown")


def calibration(verdict, n_obj, block_class):
    """block_class: 'known-sound' | 'known-imperfect' | 'unknown'. Normalised, then
    RAISED on anything else -- rule 6.

    Bare SOUND is miscalibrated ONLY on a block whose prompt declares its gaps. On an
    unknown block a bare SOUND is an ordinary verdict and this function says so rather
    than inventing a finding.

    `unknown` must be passed deliberately. A typo, a capitalisation, or a None cannot
    reach it: those raise. The failure mode this closes is not a wrong finding, it is a
    silent `consistent` that hides every MISCALIBRATED-bare-SOUND on the sheet -- and a
    caller who does not know the block's class is exactly the caller who must be stopped.
    """
    bc = norm(block_class)
    if bc not in BLOCK_CLASSES:
        raise ValueError(
            f"block_class must be one of {BLOCK_CLASSES}, got {block_class!r}. "
            "Refusing to default: a silent 'consistent' here masks every "
            "MISCALIBRATED-bare-SOUND on the sheet.")
    block_class = bc
    if verdict == UNCODED:
        return UNCODED, "verdict not codeable"
    if verdict == "SOUND" and n_obj == 0:
        if block_class in ("known-sound", "known-imperfect"):
            return "MISCALIBRATED-bare-SOUND", f"bare SOUND on a {block_class} block"
        return "consistent", "bare SOUND on an unclassified block is not a finding"
    if verdict == "SOUND" and n_obj > 0:
        return "SCHEMA-ANOMALY-SOUND-with-objections", "verdict contradicts its own list"
    if verdict == "S-W-RES" and n_obj == 0:
        return "SCHEMA-ANOMALY-reservations-without-objections", "reserved, list empty"
    return "consistent", ""


# ---------------------------------------------------------------- G6.1 fixtures ---


def _raises(fn):
    """Fixture helper: returns the exception class name, or NO-RAISE. A rule-6 fixture
    that asserts a raise must fail loudly when the raise is removed."""
    try:
        fn()
    except Exception as e:
        return type(e).__name__
    return "NO-RAISE"


# Each fixture is (callable, args, expected). Every one is a defect this estate paid
# for, or its nearest neighbour. A fixture that has never failed has never been tested,
# so the NEGATIVE cases are the point.
FIXTURES = [
    # rule 1 -- the collision that inverted a published table
    ("verdict longest-first", lambda: code_verdict("SOUND-WITH-RESERVATIONS", "34")[0], "S-W-RES"),
    ("verdict plain sound", lambda: code_verdict("SOUND", "34")[0], "SOUND"),
    ("verdict spaced alias", lambda: code_verdict("Sound With Reservations", "42")[0], "S-W-RES"),
    ("verdict prefixed prose", lambda: code_verdict("SOUND-WITH-RESERVATIONS: the record holds", "34")[0], "S-W-RES"),
    # sheet separation -- a paper verdict must not code on a record sheet's enum
    ("record sheet implaus", lambda: code_verdict("IMPLAUSIBLE-FOR-THIS-RECORD", "34")[0], "IMPLAUS"),
    ("paper sheet implaus", lambda: code_verdict("IMPLAUSIBLE-FOR-THIS-PAPER", "42")[0], "IMPLAUS"),
    # rule 2 -- UNCODED, never coerced
    ("unknown verdict is UNCODED", lambda: code_verdict("MOSTLY FINE", "34")[0], UNCODED),
    ("empty verdict is UNCODED", lambda: code_verdict("", "42")[0], UNCODED),
    ("None verdict is UNCODED", lambda: code_verdict(None, "34")[0], UNCODED),
    # rule 3 -- escapes are codes in good standing
    ("N-D codes", lambda: code_field("mech", "not-determinable-from-this-record")[0], "N-D"),
    ("N-J codes", lambda: code_field("dir", "cannot-judge-without-the-paper")[0], "N-J"),
    # rule 4 -- no substring credit
    ("no substring credit", lambda: code_field("evid", "unmeasurable")[0], UNCODED),
    ("hyphen token not split", lambda: code_field("quote", "paper-like prose")[0], "PAPER-LIKE"),
    # field codes
    ("attr absent", lambda: code_field("attr", "ABSENT — no quote in the record")[0], "ABSENT"),
    ("attr supports", lambda: code_field("attr", "supports the claim")[0], "SUPPORTS"),
    ("dir reversal", lambda: code_field("dir", "REVERSAL")[0], "REVERSAL"),
    # severity
    ("severity tally", lambda: code_severity(
        [{"severity": "fatal"}, {"severity": "Major"}, {"severity": "x"}, "junk"]),
     {"fatal": 1, "major": 1, "minor": 0, "uncoded": 2}),
    # calibration -- bare SOUND is a finding only on a declared block
    ("bare SOUND on known-sound", lambda: calibration("SOUND", 0, "known-sound")[0],
     "MISCALIBRATED-bare-SOUND"),
    ("bare SOUND on unknown block", lambda: calibration("SOUND", 0, "unknown")[0], "consistent"),
    ("SOUND with objections", lambda: calibration("SOUND", 2, "known-sound")[0],
     "SCHEMA-ANOMALY-SOUND-with-objections"),
    ("reserved, empty list", lambda: calibration("S-W-RES", 0, "known-imperfect")[0],
     "SCHEMA-ANOMALY-reservations-without-objections"),
    ("uncoded verdict propagates", lambda: calibration(UNCODED, 0, "known-sound")[0], UNCODED),
    # ---- rule 5: the negation class. Four probes below are VERBATIM from the Flash
    # G6.6(c) vet's named list; each returned a confident wrong code before this fix.
    ("neg: not sound", lambda: code_verdict("not sound", "34")[0], UNCODED),
    ("neg: not measured", lambda: code_field("evid", "not measured")[0], "ASSERT"),
    ("neg: does not match paper", lambda: code_field("dir", "does not match the paper")[0], UNCODED),
    ("neg: synonym parity", lambda: code_field("evid", "unmeasured")[0], "ASSERT"),
    # the same semantic must not code two ways: negation skips MATCHES, TRANSPLANT stands
    ("neg: skip then match", lambda: code_field("dir", "does not match — reads like a transplant")[0],
     "TRANSPLANT"),
    # an alias containing its own negator is matched whole, never tripped by rule 5
    ("neg: self-negating alias", lambda: code_field("mech", "does not hold")[0], "BREAKS"),
    ("neg: window not global", lambda: code_field("mech", "not determinable for part one; chain closes for part two")[0],
     "N-D"),
    ("neg: positive still codes", lambda: code_field("evid", "measured on the bench")[0], "MEAS"),
    # ---- rule 6: block_class normalises, then refuses. Probes verbatim from the vet.
    ("bc: mixed case", lambda: calibration("SOUND", 0, "Known-Sound")[0], "MISCALIBRATED-bare-SOUND"),
    ("bc: upper + padded", lambda: calibration("SOUND", 0, "  KNOWN-SOUND ")[0], "MISCALIBRATED-bare-SOUND"),
    ("bc: None raises", lambda: _raises(lambda: calibration("SOUND", 0, None)), "ValueError"),
    ("bc: typo raises", lambda: _raises(lambda: calibration("SOUND", 0, "know-sound")), "ValueError"),
]


def selftest(verbose=True):
    fails = []
    for name, fn, want in FIXTURES:
        try:
            got = fn()
        except Exception as e:
            got = f"EXCEPTION {e}"
        ok = got == want
        if not ok:
            fails.append((name, want, got))
        if verbose:
            print(f"  {'ok  ' if ok else 'FAIL'} {name:34} -> {got!r}")
    if verbose:
        print(f"\n  G6.1 fixtures: {len(FIXTURES) - len(fails)}/{len(FIXTURES)} pass")
    if fails:
        raise SystemExit(f"G6.1 FIXTURE FAILURE: {fails}")
    return True


def differential_sample():
    """G6.6(c): the auditor reimplements the coding rule and both run on the same input.

    Divergence does NOT void the auditor -- it voids BOTH until adjudicated against the
    primary (the TALLY prose tables and the prompts' own enums). This mirrors the
    settled amendment: differential applies to rule-reimplementation, never to
    value-recomputation from primary.
    """
    # Two cases are known-divergent by construction, one per pinned rule: the prefix
    # collision (rule 1) and the negated positive (rule 5). Both are real defects this
    # estate shipped. A run reporting fewer than two DIVERGE lines means the naive side
    # has been accidentally repaired, i.e. the differential is broken -- not that the
    # codebook is clean.
    cases = ["SOUND-WITH-RESERVATIONS", "not sound", "SOUND", "SUSPECT",
             "IMPLAUSIBLE-FOR-THIS-RECORD", "MOSTLY FINE", ""]

    def naive(t):
        # deliberately the WRONG shape: shortest-first, substring, negation-blind.
        # Present so the differential has something to disagree with on known cases.
        u = norm(t)
        for c in ("SOUND", "S-W-RES", "SUSPECT", "IMPLAUS"):
            if norm(c) in u:
                return c
        return UNCODED

    rows = []
    for c in cases:
        a = code_verdict(c, "34")[0]
        b = naive(c)
        rows.append((c, a, b, "AGREE" if a == b else "DIVERGE -> adjudicate vs primary"))
    return rows


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("G6.1 FIXTURE SUITE — tallycodes.py")
    selftest()
    print("\nG6.6(c) DIFFERENTIAL SAMPLE (pinned rule vs a naive reimplementation)")
    print(f"  {'input':32}{'pinned':10}{'naive':10}outcome")
    for inp, a, b, o in differential_sample():
        print(f"  {inp!r:32}{a:10}{b:10}{o}")
    print("\n  Divergence voids BOTH sides until adjudicated against the primary "
          "(the TALLY prose tables and the prompts' enums) — never the auditor by default.")
