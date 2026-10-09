# `prompts/_paste/` — dispatch-ready pastes, hash-identical to the vetted bytes

Generated 2026-09-10. **Paste from these files. Do not paste from the source prompts.**

| file | prompt | sha256 | status |
|---|---|---|---|
| `PROMPT-B-BROWSER.paste.md` | **B-v8** | `e9fba3a8…` | dispatch-clear (Flash §N) |
| `PROMPT-C-SOURCES.paste.md` | **C-v5** | `173f0282…` | dispatch-clear (memorial §13.2) |

## Why these exist

The source prompts carry a BUILD NOTE below a `---` rule: answer keys, grading rules, demotions.
**A dispatcher who selects the whole file pastes the answer key to the model**, which destroys every
anchor in one move — the anchors are the calibration instrument and they only work unseen.

Flash §L found the related hazard from the other side: B-v6's own ⛔ DISPATCH BLOCKED marker sat
*below* the rule, where a dispatcher pasting "everything above the rule" would never see it. A file
that has to be read correctly to be used correctly is a defect waiting on a tired evening.

These files remove the judgment call. There is nothing below the rule because there is no rule.

## The hashes are the point

Each file is **byte-identical** to the stream both stations vetted:

```bash
cd "C:/dev/Claude/Projects/ASIC"
sed '/\*\*BUILD NOTE/,$d' prompts/PROMPT-B-BROWSER.md | sha256sum   # e9fba3a8…
sha256sum prompts/_paste/PROMPT-B-BROWSER.paste.md                  # e9fba3a8…
```

Same for C-v5 at `173f0282…`. **Verified MATCH on both at generation time**, and re-checkable any
time with `sha256sum -c MANIFEST-PASTE.sha256` from this directory.

An earlier generation attempt trimmed trailing blank lines and produced `09b0a553…` / `12cb9f0f…`.
Prettier, and **not the vetted bytes** — which is the whole failure mode this directory exists to
prevent. These files are the raw `sed` stream, unpolished on purpose.

## Regenerating

```bash
cd "C:/dev/Claude/Projects/ASIC"
for f in PROMPT-B-BROWSER PROMPT-C-SOURCES; do
  sed '/\*\*BUILD NOTE/,$d' "prompts/$f.md" > "prompts/_paste/$f.paste.md"
done
cd prompts/_paste && sha256sum -c MANIFEST-PASTE.sha256
```

**No reformatting, no trimming, no editor round-trip.** If `sha256sum -c` fails after a regeneration,
the source prompt's paste moved — which means its version must bump and it needs a re-vet before
anything is dispatched. It does not mean the manifest is stale.

## Collection

One model per chat, fresh chat. Save verbatim as
`<model-self-name-as-declared-in-the-header> b2.json` and `… c2.json` — the header's self-declared
name is the canonical spelling, which is the fence against a second minara/minaria split. Neither
suffix has ever been collected (checked 2026-09-09).

Grading keys stay in the source prompts' BUILD NOTEs and are never copied here.
