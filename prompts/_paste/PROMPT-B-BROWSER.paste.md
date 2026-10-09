I am filling a deployment-constraint matrix for running cryptographic proving workloads
(WebAssembly + WebGPU) inside web browsers. Answer the cells below for the CURRENT state of
Chrome/Edge, Firefox, and Safari. Two access tiers — pick honestly:

- **Live web access:** cite a URL and retrieval date for every claim — no URL, no claim.
- **No live web access:** do NOT stop and do NOT skip rows. Answer from training knowledge; set
  knowledge_basis to "training-recall" on every claim, give your best as_of month for that
  knowledge, and omit url. A labeled training-recall answer is useful data; an invented URL is not;
  an empty file is neither.

ANCHOR CHECK (calibration; answer all three, each with knowledge_basis, confidence, and note):

  b1: "SharedArrayBuffer is available to a page only under cross-origin isolation (COOP/COEP)."
  b2: "WebGPU timestamp-query is exposed to ordinary web content by default in current Chrome."
  b3: "WebAssembly threads module validation fails without cross-origin isolation in current Chrome."

**Output: a single bare JSON object and nothing else:**

{"prompt":"B-v8","model":"<your exact model name, as you state it>","date":"<today YYYY-MM-DD>",
 "web_access":true,
 "anchors":{"b1":{"verdict":"agree | disagree: <what is actually true> | unknown",
                  "knowledge_basis":"live-web","confidence":0.0,"note":"<refinement, or empty>"},
            "b2":{"…same four keys…"},"b3":{"…same four keys…"}},
 "rows":[{"cell":"1","browser":"Chrome/Edge","feature":null,"claim":"…",
          "url":null,"retrieved":null,"as_of":"2026-09","changed_since_2026_03_01":null,
          "knowledge_basis":"live-web","confidence":0.0,"verifier_hint":"…","notes":"…"}],
 "bonus":[{"ref":"…","what_was_measured":"…","hardware":"…","url":null,"retrieved":null,
           "knowledge_basis":"training-recall","confidence":0.0,"notes":"…"}]}

**THE ROW GRID — 27 rows, no more and no fewer.** `browser` is exactly one of `"Chrome/Edge"`,
`"Firefox"`, `"Safari"`. Every row is uniquely keyed by (cell, browser) — and for cell 3, by
(cell, feature, browser). Emit one row per key even when your answer is identical across browsers;
do NOT collapse uniform claims into a single row.

| cell | question | feature | rows |
|---|---|---|---|
| 1 | `SharedArrayBuffer` + cross-origin isolation (COOP/COEP): current requirements | null | 3 |
| 2a | WebGPU compute-shader availability | null | 3 |
| 2b | Is `timestamp-query` exposed to ordinary web content by default? | null | 3 |
| 3 | WASM feature status | one row per feature × browser: `threads`, `SIMD128`, `relaxed-SIMD`, `JSPI`, `memory64` | 15 |
| 4 | Inside a cross-origin iframe: can an embedded page obtain cross-origin isolation / WebGPU access? | null | 3 |

**`bonus` is a separate array and is NOT part of the 27.** It holds published 2025–2026 measurements
of in-browser proving (any proof system) with a reproducible test setup — repo or paper, what was
measured, on what hardware. An empty `bonus` array is fine and costs you nothing.

- **A row is never omitted.** If you cannot answer one, emit it with `claim:"NO-ANSWER"` and say why
  in `notes`. Under live web access, a row you cannot source is `claim:"UNVERIFIED"` — and never an
  invented URL. Under training-recall, answer the row from knowledge and label it; use `NO-ANSWER`
  only where you have no knowledge at all.
- `url` and `retrieved` are REQUIRED on a live-web row **that carries a claim**, and forbidden on
  training-recall and inference rows. On an `UNVERIFIED` or `NO-ANSWER` row they stay `null` even
  under live web access — that is the one case where a live-web row legitimately has no URL, and it
  is never a reason to invent one or to relabel knowledge_basis.
- knowledge_basis: "live-web" | "training-recall" | "inference".
- **Date formats are exact.** `retrieved` = `YYYY-MM-DD`, the day you fetched the page. `as_of` =
  `YYYY-MM`, the month your knowledge is good to. Not prose, not a season, not "current".
- `changed_since_2026_03_01` = did the underlying behaviour change **on or after 2026-03-01**?
  `true` | `false` | `"unknown"`. This is an absolute window; do not compute it from today's date.
- `verifier_hint` = the page that would settle the claim (e.g., webgpureport.org, a chromestatus.com
  feature entry, MDN).
- `confidence` (0.0–1.0) on every row and every anchor = your confidence the claim is correct.
- `note` on an anchor = any refinement the verdict alone cannot carry. Use it when the statement is
  true as worded but the mechanism is more specific than it implies.
- If two sources disagree, report both. Distinguish "verified from a current authoritative page"
  from "widely believed, weaker source" via confidence. No prose outside the JSON.

[prompt-version: B-v8 2026-09-10 — over B-v7: the url/retrieved rule no longer fires on an
UNVERIFIED or NO-ANSWER row, which under B-v7 left a live-web model unable to obey both that rule
and the never-omit-a-row rule. Over B-v6: the UNVERIFIED rule scoped to live-web and a
training-recall NO-ANSWER escape added (B-v6's two rules cancelled each other and blocked dispatch);
fixed 27-row grid keyed (cell, browser) and (cell, feature, browser), replacing model-chosen row
collapsing; cell 2 split into 2a/2b; bonus cell 5 moved to its own array; anchors gain note and
confidence; exact date formats; changed_recently replaced by the absolute
changed_since_2026_03_01; b3 sharpened to a falsifiable form. Supersedes B-v6 and B-v7, neither of
which dispatched.]

---

