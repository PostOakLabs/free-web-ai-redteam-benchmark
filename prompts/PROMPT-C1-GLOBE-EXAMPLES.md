This task is about the OECD's officially published **GloBE Model Rules (Pillar Two) Illustrative Examples** document (originally March 2022, revised through May 2025 with Administrative Guidance examples).

From your knowledge of THAT SPECIFIC DOCUMENT, reproduce up to 5 of its worked examples touching: top-up tax computation, the Substance-Based Income Exclusion (payroll/tangible-asset carve-outs and their transitional rates), deferred-tax / transition rules (Article 9.1), or the de minimis exclusion.

**Output: a single bare JSON array** of:

{"example_id": the document's own example number/label as best you recall (e.g. "Example 5.3-1") else null, "article": the Model Rules article it illustrates, "fact_pattern": the inputs with values and units, "computation": the arithmetic STEP BY STEP with intermediate values, "result": the example's stated outcome, "doc_vs_general": exactly one of "confident-this-example-is-in-the-document" | "probably-in-the-document" | "constructed-from-rule-knowledge-not-a-published-example", "weakest_point": the single detail most likely wrong}

**Hard rules:** step-by-step arithmetic will be recomputed mechanically — an example whose steps don't reproduce its result is discarded; REVERSING a rule's direction (e.g. which entity the top-up allocates to, whether a rate glides down or holds) is the worst failure — if unsure of a direction, say so in weakest_point; a constructed example honestly labeled is acceptable and still useful, a constructed example labeled as published is the failure this format exists to catch. Fewer honest entries beat five vague ones. No prose outside the JSON.

[prompt-version: C1-GLOBE-v1 2026-08-31]
