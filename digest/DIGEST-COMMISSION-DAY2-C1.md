# Digest commission — Day 2, Class-1 batch (GLOBE / APPJ / TRID / OFAC)

**Input:** `C:\dev\Claude\Projects\ASIC\Web Model Tasks\Day 2\` — 55 JSONs, 14 models × 4 deterministic-computation prompts (glm 5.3 flash is missing trid; note it, don't wait for it). These are Class-1 prompts: every answer was required to show step-by-step arithmetic, so adjudication is MECHANICAL, not judgment.
**Output:** `C:\dev\Claude\Projects\ASIC\digest\day2-c1-adjudication.md` (+ update `recall-scorecard.md` in place).

## Method — per prompt, in this order

1. **Recompute the arithmetic yourself, mechanically.** For each model's JSON, re-execute every shown computation step (scratch python/node fine). A model whose steps don't reproduce its own final answer gets verdict SELF-INCONSISTENT regardless of whether the final number is right. A model whose steps reproduce but start from a wrong constant gets WRONG-INPUT (name the constant). Correct steps + correct inputs + correct answer = VERIFIED.
2. **Cross-model consensus table** per prompt: final answer(s) per model, grouped. Consensus is EVIDENCE, not ground truth — the art-220 lesson applies verbatim: consistent-but-wrong passes convergence. Where a majority agrees, still spot-check the majority's inputs against the source values quoted in their own JSONs; where models split, the recomputation from step 1 decides, not the vote.
3. **Honesty-label audit:** every JSON was required to carry `weakest_point` + provenance labels. Score each: is the weakest_point the ACTUAL weakest point (compare against your recomputation findings), or boilerplate? Flag any missing/evasive labels.
4. **Anti-reversal check:** any model whose narrative contradicts its own computed number (the D2 19% failure shape).
5. **Scorecard update:** per-model row deltas on `recall-scorecard.md` — Class-1 arithmetic reliability is a NEW column (VERIFIED / WRONG-INPUT / SELF-INCONSISTENT / anti-reversal counts per model). Note: glm 5.3 flash is SUSPENDED-status running a re-trial — its Day 2 results decide whether suspension stands; call that verdict explicitly. minimax 2.7 / m3 / mimo were DROPPED but appear in the folder — score them anyway as re-trial data, same explicit verdict.
6. **Harvest the good:** any step-sequence that is VERIFIED and unusually clean is candidate fixture material for the corresponding kernel-adjacent episode corpus — list file + prompt + why, don't copy content.

## Register
Show your recomputation arithmetic for every disagreement you adjudicate; verdicts by named model per prompt; INDETERMINATE over a guess; no writes outside the two named output files.
