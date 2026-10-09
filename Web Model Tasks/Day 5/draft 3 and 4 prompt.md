## Draft #3 — Seal-integrity re-test
`DELIVERY\HY4-DISPATCH-SEAL-INTEGRITY-RETEST-2026-09-08.md`

- **Self-deriving procedure**: the prior artifact's exact script lives on the Omen, so instead of replaying it, the dispatch makes Hy4 **derive the verification procedure from the repo itself** (find how `compute_proof` digests are computed — naming the tool used — and re-derive every sealed kernel's digest from current file bytes). Guessing a hash procedure is explicitly forbidden; UNVERIFIABLE beats stalling.
- **A18 ratchet + guest registration #1782**: a dedicated step identifies what those changes touched in the sealing/registration path and re-tests *specifically around them* — do pre-change proofs still verify, do new seals verify?
- **The mutation path is exercised**: the repo's own deliberate-tamper fixture (`mutate-seal-art-01.case.json`) is applied in a scratch copy, and the dispatch requires proof that detection **still fires** — the strongest possible seal check.
- Population drift is a finding (640 sealed at baseline vs whatever current main says).

## Draft #4 — Adversarial re-audit of #1
`DELIVERY\HY4-DISPATCH-ADVERSARIAL-RE-AUDIT-2026-09-08.md`

- **Genuinely different method**, per the every-third rule: #1 was static inspection; this one is **dynamic adversarial execution** — import each real kernel module and attack its numeric helpers with boundary vectors (empty/1-element arrays, p at every boundary, unsorted, duplicates, NaN/±Inf, tie stress, n=2→1000, nearest-rank adversarial cases where `floor(p*n)` and `ceil(p*n)-1` disagree).
- **Independent references written from the declared definitions** (A&S, A-3, R-6, R-7) — never by copying kernel code; a missing declared convention is itself a finding ("no declared convention" → UNDETERMINED).
- **Adjudicates #1's three divergence claims with execution evidence** — especially F1 (`floor(pA*n)`): is it a defect, or does the kernel's shard declare a convention that makes floor correct? That's exactly what the PARTIAL grade contested.
- New divergences the static pass couldn't see are the point of the dispatch (item 7).

Both follow the house conventions (READ-ONLY clone, incremental .md landing, no npm/network/installs, UNDETERMINED beats stalling, machine-readable companions).

**On your confirmation**: Tim commits both to `workbuddy\` and updates QUEUE.md — then dispatch is the same simplified pattern as the clause-fidelity one (open the file, execute the fenced block). Say the word on any edits and I'll revise before they go to the bus.
---

# Review verdict — Opus verifier seat B (Omen), 2026-09-09

**Both dispatches are approved after edits. Both files were modified in place; the fenced blocks are the parts that changed.** The design of both is sound — self-deriving procedure in #3, method-change enforcement in #4 — and every fix below came from checking the repo, not from re-reading the drafts.

## Blocking defect, #4 only — the core instruction could not have run

Step 3 told the session to *"import the actual kernel module and execute its numeric helper."* **The helpers are module-private.** At `origin/main`, `sim-01-lcr-nsfr-liquidity-stress-test.kernel.mjs` exports exactly `meta` (line 1563), `compute` (1639) and `buildArtifact` (1732), while its `percentileAt` is a bare `function` at line 1632; `mms-03-app-fraud-graph.kernel.mjs` has the identical shape with `quantile` at line 102. The import returns `undefined` for all 22 helpers and the dispatch fails at step 3 with nothing delivered.

Rewritten to drive the exported `compute(pp)` with policy_parameters constructed so the helper's behaviour shows in the output. **This is also the better experiment**: it answers reachability, which is exactly what F2 and F3 ask and what a private-helper unit test structurally cannot answer — a helper can be wrong in code no input reaches, and that ambiguity is what earned #1 its PARTIAL. Added `UNREACHABLE-FROM-PUBLIC-INPUT` as a verdict, and an explicit ban on the tempting fallback of copying helper source into the harness, which would be #1's static method in costume.

## Defects in both

**The push instruction contradicted itself inside one fenced block.** #3 said "commit and push NOTHING" at step 8 and "Commit and push BOTH … in the same push" at step 9; #4 the same at steps 9 and 10. The intent was obvious to a human and ambiguous to a runner. Now stated once: farm bus YES, ainumbers source clone NEVER.

**No positive control.** Three censuses on this estate published a clean zero today that turned out to be a broken instrument, most starkly `VERDICT-REACHABILITY-EXEC-CENSUS-1` reporting 0 of 1097 verdicts reached across 943 executions when the fixtures it executed visibly contain those values. #3 had the positive half and lacked the negative; #4 had neither. Both now require the control to fire before any count is reportable, and both are told to stop and report the instrument if it does not.

**Provenance was a header note, not a first step.** Both now open with STEP 0 and a shared-clone warning: `C:\dev\ainumbers-farm\repos\ainumbers` is shared, so a run that finds HEAD moving must pin its sha and say so rather than pull again.

## Corrections of fact

**"A18 ratchet" is not a name this estate uses.** `git log --grep="A18 ratchet"` returns nothing; the commits say §18, e.g. `ff3d57c0 prove(art-663): first §18 GPU prove …`. A session searching for A18 finds nothing and either stalls or invents a target. Renamed throughout, and #3 now says to report failure to locate the change rather than substitute a guess.

**#3 used one tamper fixture where six exist.** `chaingraph/vm/twin/fixtures/` carries `mutate-seal-art-01`, `mutate-imageid-art-01`, `mutate-journal-art-01`, `probe-keyreorder-art-01`, `probe-unicode-art-01`, plus `real-art-01` and `real-art-106`. Three tampers make a far stronger detection test, the two probes exercise canonicalisation, and **the untampered cases are a free negative control** — without them, "detection fired" is indistinguishable from "the checker rejects everything."

**#3's 640 sealed-kernel baseline** is now marked as a claim to re-derive rather than a given.

## Verified correct, left alone

`HY4-HELPER-IDENTITY-SWEEP-2026-09-07-REPORT.md` is where #4 says it is (`C:\dev\ainumbers-farm\outbox\`, 13,602 bytes). `mutate-seal-art-01.case.json` is where #3 says it is. #4's instruction not to inherit #1's dead-code call on F3 is exactly right and was strengthened rather than changed.

## One scheduling note

#4's 2–3 h estimate may exceed the lane timeout. Incremental landing was already required; added an explicit PARTIAL contract and an order of work that puts F1/F2/F3 first, so a cut-off run still delivers the adjudication the dispatch exists for.
