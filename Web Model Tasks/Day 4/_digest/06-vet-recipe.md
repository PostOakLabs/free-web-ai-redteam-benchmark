# Vet recipe — Day 4 digest

**Written last (G5), after every file was written and every move was done. Every expected value below
was produced by running the command in this session, at `2026-09-09T01:55:50Z`, and re-derived after
the digest documents were complete — not recalled from earlier in the run.**

Hand this to the Flash re-audit session. Self-audit is weaker than independent audit; that is why
this file exists rather than a self-assessment.

---

## 0. Confirm you have the bytes that produced the digest

```bash
cd "C:/dev/Claude/Projects/ASIC/digest/_verify"
sha256sum -c MANIFEST-D4.sha256
```

**Expected, verified 01:55Z:**

```
d4load.py: OK
d4grade.py: OK
d4xcheck.py: OK
```

If any line says FAILED, the tool changed after the digest was written and nothing below is binding.

## 1. G1 — census gate

```bash
cd "C:/dev/Claude/Projects/ASIC"
ls "Web Model Tasks/Day 4"/*.json > /tmp/day4-census.txt
wc -l < /tmp/day4-census.txt
python digest/_verify/d4load.py > /tmp/d4load.txt 2>&1; echo "EXIT=$?"
grep "G1 CENSUS ASSERT" /tmp/d4load.txt
```

| expected | value |
|---|---|
| census line count | **73** |
| `d4load.py` exit | **0** |
| assert line | `G1 CENSUS ASSERT: census=73 loaded=73 skipped=0 halted=0  -> PASS` |

**Do not pipe the loader through `head`, `tail` or `sed -n`.** Redirect to a file and grep the file.
That rule is G2 and it exists because this estate has broken it twice, once reading `head`'s exit
code as a gate result and once cutting 73 skip warnings out of a Day-3 run.

**Adversarial check:** temporarily add a file with an unknown family suffix to `Day 4/` and re-run.
The loader must exit **3** with `G1 STOP — unrecognised family`. It must not skip. Remove the file
afterwards.

## 2. Grading tiers

```bash
python digest/_verify/d4grade.py > /tmp/d4grade.txt 2>&1; echo "EXIT=$?"
cat digest/_verify/d4run/grade-summary.txt
```

| tier | expected count |
|---|---|
| T0-absent | 1 |
| T0-declined | 189 |
| **T1-verbatim** | **49** |
| T1-verbatim-hyphen-variant | 5 |
| T2-paraphrase-consistent | 11 |
| **T3-contradicts-CANDIDATE** | **1** |
| **T4-not-found** | **16** |
| TOTAL | **272** |

## 3. G4 — determinism

```bash
cd digest/_verify/d4run
sha256sum d4corpus.json d4grades.json d4permodel.json
```

| file | expected sha256 (first 8) |
|---|---|
| `d4corpus.json` | `83b177f9` |
| `d4grades.json` | `9d662355` |
| `d4permodel.json` | `403c020a` |

Re-run all three scripts and hash again. All three must be unchanged.

## 4. The three hand-confirmed findings — check these, they are the substance

Everything else in the digest is a count. These are claims about models.

**4a. deepseek `pphysical` entry 2 contradicts the paper.**

```bash
python -c "
import sys; sys.path.insert(0,'digest/_verify')
from d4grade import denorm
import re
t=denorm(open('sources/POWER4-cpd-pagemarked.txt',encoding='utf-8',errors='replace').read())
print('1.5 ghz :', len(re.findall(r'1\.5 ?ghz',t)))
print('1.3 ghz :', len(re.findall(r'1\.3 ?ghz',t)))
print('15200   :', len(re.findall(r'15,?200',t)))
print('1.5 v   :', len(re.findall(r'1\.5 ?v\b',t)))"
```

**Expected, run at 01:56Z:** `1.5 ghz` **0** · `1.3 ghz` **4** · `15200` **2** · `1.5 v` **1**.
The quote's pin count and single-PLL claim verify; its frequency does not, and `1.5` is present in
the paper only as a voltage.

*(This line first read `1.3 ghz ≥5`, written from memory of an earlier probe. Running it gave 4. The
value above is the run value. That substitution is the exact defect G5 exists to prevent, caught
here because the recipe was executed before being handed over rather than after.)*

**4b and 4c. Two whole-file fabrication sets.** `glm 5.3 flash pphysical.json` and `longcat p4.json`
return T4 on all five entries each. Verify by taking any quote from either file and searching the
normalised source for its **first 25 characters**. Expect zero hits. Then take a quote from
`grok p4.json` and do the same — expect a hit. The contrast is the check.

## 5. Where the digest could still be wrong

Give these your time before re-checking the counts.

1. **T2 versus T4 rests on one tunable.** `T2_FLOOR = 0.60` content-word overlap in `d4grade.py`.
   Nothing validates that number. Move it to 0.5 and 0.7 and see which claims cross the line; any
   that move are weakly graded and the digest does not say so.
2. **T3 detection is numeric-only.** A quote that inverts a *direction* — "chose X over Y" where the
   paper chose Y — is not detected by anything here and would grade T2. The single T3 found was
   numeric. **A direction reversal would pass this digest silently**, and that is the failure class
   the D2 prompts call worst.
3. **The 189 declines are ungraded by construction.** Declining is the prompt's sanctioned escape and
   is scored as a pass. Nine models declined every entry of every paper. The digest therefore says
   nothing about their knowledge, and a reader could mistake "no findings against them" for "clean".
4. **`page_of()` is proportional, not exact.** It maps a normalised offset to a PDF page by linear
   interpolation over page-marker positions. Near a page boundary it can be off by one, which the
   ±2 tolerance absorbs but does not fix.
5. **Four checker defects were found *during* this run** (`00-corpus-and-harness.md` §5), each of
   which had produced a false finding. That rate suggests more remain. The four found were caught by
   hand-checking a suspicious result, not by any gate.

## 6. Coverage as-of stamp

| count | value | as-of |
|---|---|---|
| Day 4 response files | 73 | 2026-09-09T01:55:50Z |
| loaded / skipped | 73 / 0 | same |
| families | 5 | same |
| quarantine gate coverage | **10 of 10** families (Day 3 + Day 4) | same |
| entries graded | 272 quotes across 4 paper families | same |
| digest documents | 8 (`00`–`06` + this) | same |

Counts on this page drift when other sessions add files. Re-run §1 before relying on any of them.
