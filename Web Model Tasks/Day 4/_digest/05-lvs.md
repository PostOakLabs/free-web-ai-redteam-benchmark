# Digest — family `lvs`

**Prompt:** `prompts/F-LVS-MISMATCH-CLASSES.md`. **15 files, 30 entries, 15 of 15 parse clean.**
As-of 2026-09-09T01:41:45Z.

## ⛔ No paper. Nothing on this page is graded against ground truth.

This is the one Day-4 family with no source document, and the commission names it explicitly (§2.1):
grade on the prompt's own class definitions and **say so** rather than implying paper-backing.

There is no quote-tier table, no page-guess column and no convergence-checked-against-source
section, because none of the three is possible here. **Absence of a defect finding on this page means
the check does not exist, not that the files are clean.** That distinction is the point of the page.

## Model set — 15, the only complete family in Day 4

chatgpt · deepseek · gemini · glm 5.3 flash · grok · kimi · longcat · meta · mimo · minimax 2.7 ·
mistral · qwen · solar · sonnet · yuanbao.

**No model is missing.** Every other Day-4 family has at least one absence: `niagara` lacks longcat
and minimax m3, `pphysical` lacks chatgpt, `alpha` needed a misfiled file to reach 15, and `p4` has
one unparseable file.

## Schema conformance — 30 of 30

Every entry carries all six F-family keys:

| key | present |
|---|---|
| `symptom` | 30/30 |
| `first_checks` | 30/30 |
| `discriminating_experiments` | 30/30 |
| `common_root_causes` | 30/30 |
| `classic_trap` | 30/30 |
| `node_era_note` | 30/30 |

Every model returned exactly **2** entries. Uniform, complete, structurally clean — matching Day 3's
`library` family, which was that corpus's schema-conformance benchmark.

## What can be said, and what cannot

**Can:** the family is schema-perfect and delivery-complete. Two of the five Day-4 families are
structurally flawless; this is one, and it is the only one with no model absent.

**Cannot:** whether any diagnostic tree, root-cause frequency or discriminating experiment is
*correct*. That needs a practitioner, not a document. Day 3's `library` digest reached the same
boundary; this family sits behind it.

## For a future pass

The natural next check is cross-model convergence on the discriminating experiments — the treatment
`Day 3/_digest/04-library.md` gave the diagnosis library, where 14 of 15 models converged
independently on a single `classic_trap` and one model dissented in a recorded direction. **That work
is not done here and is not implied by anything above.**
