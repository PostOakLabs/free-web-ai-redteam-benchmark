# Vet recipe — Day 5

**Written last (G5), after every document was written and the manifest was backfilled. Every
expected value below was produced by running its command in this session at
`2026-09-09T14:28:51Z`, after the writes — not recalled from earlier in the run.**

Hand to the Flash re-audit session. Self-audit is weaker than independent audit.

---

## 0. Confirm you have the bytes that produced the digest

```bash
cd "C:/dev/Claude/Projects/ASIC/digest/_verify"
sha256sum -c MANIFEST-D5.sha256
```

Expect six `OK` lines: `d5load.py`, `d5grade_regz.py`, `d5grade_strings.py`, `d5grade_e.py`,
`d5xcheck.py`, `d5tally.py`. Any `FAILED` line voids everything below.

## 1. G1 census

```bash
cd "C:/dev/Claude/Projects/ASIC"
ls "Web Model Tasks/Day 5"/*.json > /tmp/d5census.txt; wc -l < /tmp/d5census.txt
python digest/_verify/d5load.py > /tmp/d5load.txt 2>&1; echo "EXIT=$?"
grep "G1 CENSUS ASSERT" /tmp/d5load.txt
```

| expected | value |
|---|---|
| census | **80** |
| exit | **0** |
| assert | `census=80 loaded=80 skipped=0 halted=0 models=16  -> PASS` |

**Redirect to a file and grep the file.** Do not put `head`, `tail` or `sed -n` between a command
and a value you will record — that is G2, and this estate has broken it twice.

## 2. Adversarial census — run it, it is not decorative

```bash
echo '{}' > "Web Model Tasks/Day 5/zzz badfamily.json"
python digest/_verify/d5load.py > /tmp/adv.txt 2>&1; echo "EXIT=$?"    # expect 3
grep "G1 STOP" /tmp/adv.txt                                            # expect the halt
rm "Web Model Tasks/Day 5/zzz badfamily.json"
python digest/_verify/d5load.py > /tmp/d5load.txt 2>&1; echo "EXIT=$?" # expect 0
```

**Verified in-session at 14:28Z: exit 3 with the planted file, `G1 STOP — halted, not skipped`,
then exit 0 and `census=80 … PASS` after removal.** The loader must halt, never skip — that is the
inversion of the Day-3 defect where a family allow-list silently dropped 73 of 143 files.

## 3. Track values

```bash
for s in d5grade_regz d5grade_strings d5grade_e d5xcheck; do
  python digest/_verify/$s.py > /tmp/$s.txt 2>&1; echo "$s EXIT=$?"
done
cat digest/_verify/d5run/{regz,strings,e,redteam}-summary.txt
```

| track | expected |
|---|---|
| A regz | **12** models exact on all 9; `deepseek` 8, `minimax 2.7` 5, `mistral` 2, `solar` NOT GRADABLE |
| B strings | **44 of 60** correct on cases 1–4; case 5 UNGRADABLE; **14 of 15** correct on the s1–s4 prefix |
| C e | **65** NEEDS-RETRIEVAL, **73** free-primary-text; TPP **11/27** is the weak family |
| D red1 | **0** bare-SOUND; 1 schema anomaly (`minimax 2.7`, reservations without objections) |
| D red3 | **5** bare-SOUND (`gemini`, `grok`, `meta`, `minimax 2.7`, `qwen`); 1 schema anomaly (`longcat`) |

## 4. G4 determinism

```bash
cd "C:/dev/Claude/Projects/ASIC/digest/_verify/d5run"
sha256sum d5corpus.json d5regz.json d5strings.json d5e.json d5redteam.json d5permodel.json
```

| file | expected sha256 (first 8) |
|---|---|
| `d5corpus.json` | `b6430c7f` |
| `d5regz.json` | `50480289` |
| `d5strings.json` | `df152546` |
| `d5e.json` | `df0e7761` |
| `d5redteam.json` | `ff646c6a` |
| `d5permodel.json` | `db30addd` |

Re-run the chain and hash again; all six must be unchanged.

## 5. Floor sweep — there is no floor to sweep

Commission §3.2 requires any overlap-graded output to publish its 0.5/0.6/0.7 tier tally inline.
**Day 5 has no overlap-graded track.** Track A is exact arithmetic, Track B is byte comparison
against a reference canonicalizer, Track D is enum harvest. Track C's shape check is token presence,
not overlap.

**There is therefore no floor-band table, and this section exists to say so rather than to leave the
requirement silently unmet.** Day 4's 13-of-272 floor sensitivity has no analogue here. If a future
day adds an overlap-graded track, the requirement reactivates.

## 6. Manifest backfill

```bash
wc -l < "Web Model Tasks/RUN-MANIFEST.tsv"      # expect 598 (597 rows + header)
grep -c "minaria" "Web Model Tasks/RUN-MANIFEST.tsv"   # expect 2
```

**444 → 597 rows**, 153 appended: Day 4 (73) and Day 5 (80). The dual spelling is recorded **as
collected** — `minara e/red1/regz`, `minaria red3/strings` — because the manifest indexes filenames,
while `d5permodel.json` carries the merge.

## 7. Where this digest could still be wrong

Spend your time here, not on re-counting.

1. **Track C's shape check is token-based.** An inverted metric with the right terms passes. The
   estate has one on record (mistral's SPFM inversion in `hw-calc-formulas.md`) and **this checker
   would not catch it**. Track C is not a correctness audit.
2. **Track A scores value presence, not reasoning.** A model that printed the right figures beside
   wrong prose scores 9. The consistency judgment task 1 actually asks for is unscored.
3. **`solar regz.json` is prose and was not hand-graded.** Its arithmetic may be entirely correct.
   The digest records NOT GRADABLE and does not guess — but that is a gap, not a neutral outcome.
4. **`chatgpt strings.json` was never assessed.** Same class as the Day-2 chatgpt-jcs file that went
   from apparent 0/33 to 10/11 once repaired. A better repair may exist.
5. **`mistral` regz tier B is a truncate-vs-round convention difference**, scored as a miss. The
   prompt does not name the convention. That single cell is arguably the model's, arguably the
   prompt's.
6. **Four instrument defects were found during this run** (`00-corpus-and-harness.md` §4), one of
   which inverted an entire table. All four were caught by hand-checking a suspicious result, not by
   any gate. **That rate is the reason to assume more remain.**
7. **`minara`/`minaria` is provisional.** If they are two models, every per-model figure that
   mentions minara is wrong.

## 8. As-of stamp

| count | value | as-of |
|---|---|---|
| Day 5 responses | 80 | 2026-09-09T14:28:51Z |
| loaded / skipped / halted | 80 / 0 / 0 | same |
| models | 16 (15 legacy + minara) | same |
| stray excluded, untouched | 1 (`draft 3 and 4 prompt.md`) | same |
| RUN-MANIFEST rows | 597 | same |
| digest documents | 8 (`00`–`07`, unique numbers) | same |

Re-run §1 before relying on any count; other sessions add files.

9. **CORRECTIONS APPLIED 2026-09-09, after the Flash vet passed.** An audit pass found defects the
   vet did not, because the vet reproduced my numbers and confirmed my self-criticisms rather than
   testing the rules that produced them:
   - **Track A said 13 exact; the true figure is 12.** The matcher compared substrings, so
     `1.033573` matched inside deepseek's `1.0335735` while its stated 6dp answer `1.033574` is
     wrong. Now compares values at the reference's precision. `d5regz.json` and `d5permodel.json`
     hashes changed accordingly (`50480289`, `db30addd`).
   - **Track C: three of seven families have a 1-token shape check** (`max(1, len-1)`), and
     DO-254-DAL's token is nearly implied by its own detector, so its 11/11 is an artifact.
   - **A Track C inference was retracted** — the LFM-vs-SPFM gap is explained by unequal test
     difficulty (1-of-2 vs 2-of-3), not by model behaviour.
   - **`classify()` is order-dependent**: 9 of 168 entries match multiple families.
   - **The manifest backfill dates are wrong for the majority of rows.** Day 4 holds 30 files dated
     09-04 and 43 dated 09-08; Day 5 holds 32 dated 09-08 and 48 dated 09-09. I stamped one date
     per day. The commission asked for rows "dated honestly"; these are not.
