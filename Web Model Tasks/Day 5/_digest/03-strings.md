# Track B — `strings`, JCS conformance

**Prompt:** `prompts/C2-JCS-STRINGS.md` — exact RFC 8785 canonical serializations.
**Reference:** `digest/_verify/jcs.py`, 12 of 12 RFC 8785 self-asserts pass.
**16 files, 15 gradable, cases 1–4 graded.** As-of 2026-09-09T14:11:04Z.

---

## ⛔ Case 5 is UNGRADABLE, and the reason is transport, not the models

The prompt's case-5 input embeds a **raw U+0007 (BEL)** inside `"control …"`. That is illegal in
JSON, so *the prompt's own case does not parse*. Worse, chat surfaces strip or substitute invisible
control characters on paste: **every one of the 15 responding models rendered `s5` as a plain space
or U+00A0.** None of them ever received the character.

Grading case 5 against a `` reference would have recorded **a transmission loss as 15 model
failures.** It is scored UNGRADABLE instead.

**The part that did survive was answered well: 14 of 15 models produced the correct canonical form
for `s1`–`s4`.** The first version of that sub-check reported *0 of 15* because it compared the
models' full output against a reference with `s5` removed. That was my defect and it is fixed.

**Action for the prompt:** case 5 needs its control character written as an escape (``) in the
source markdown, or the case cannot be run at all.

## Results — cases 1–4

| model | correct /4 | note |
|---|---|---|
| grok · kimi · meta · minara · sonnet | **4** | |
| deepseek · glm 5.3 flash · longcat · solar · yuanbao | 3 | longcat: case 1 right answer, rule not stated |
| gemini · mimo · minimax 2.7 · qwen | 2 | |
| mistral | 1 | |
| chatgpt | NOT GRADABLE | see below |

**44 of 60 graded cases correct.** Five models are perfect on the gradable set.

## Difficulty by case

| case | correct | what it tests |
|---|---|---|
| 1 | **14/14** | mixed-case key sort, UTF-16 code units |
| 2 | 11/14 | objects nested inside arrays, recursive sort |
| 4 | 9/14 | `€ $ ü aa` — UTF-16 ordering on non-ASCII keys |
| 3 | **7/14** | ES6 number serialization: `1e21`, `1e-7`, `-0`, `2^53` boundary, `333333333.33333329` |

**Case 3 is the discriminator**, exactly as the Day-2 JCS-edges slice predicted. Number
serialization halves the field.

## Right answer, wrong rule — the separate score

Commission §2B: a correct canonical string produced alongside a rule statement that does not name
the governing rule is a **finding, not a pass**. One instance: **longcat, case 1** — correct output,
but its `rules_applied` does not name UTF-16 code-unit ordering.

That the count is 1 is itself informative: models that got these right generally knew why.

## `chatgpt` — content without structure

`chatgpt strings.json` escaping is inconsistent *within a single value*:

```
{\"€\":\"euro","$":"dollar","ü":"umlaut","aa":"double"}
```

Escaped and unescaped quotes in the same string. No repair rung yields case-shaped records; the
forward harvest returns the embedded canonical fragments themselves (`{C,a,b}`, `{outer}`), which
are not review records. Marked NOT GRADABLE and its harvest output **rejected rather than counted** —
an earlier pass scored it 0 of 0, which read as a zero.

This is the same class as the Day-2 `chatgpt jcs.json` defect, where a quoting repair turned an
apparent 0/33 into a top-quartile 10/11. **chatgpt's Track-B content has not been assessed**, and
that is a delivery finding, not a capability one.
