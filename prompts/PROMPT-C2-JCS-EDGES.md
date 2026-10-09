This task is about **RFC 8785 — JSON Canonicalization Scheme (JCS)** — the exact canonical serialization rules, targeting the edge cases where implementations diverge.

Produce up to 12 edge-case test vectors, each a concrete input with its EXACT canonical output per RFC 8785. Cover at least: number serialization (integers vs floats, -0, values at and beyond 2^53, exponent forms like 1e21 boundaries, tiny decimals), string escaping (which characters escape, unicode normalization NON-behavior, surrogate pairs, the solidus), key ordering (UTF-16 code-unit ordering — include a case where UTF-16 ordering differs from code-point ordering, e.g. keys with characters above U+FFFF vs U+E000-U+FFFF), and structural cases (empty object/array, nesting, duplicate-key illegality).

**Output: a single bare JSON array** of:

{"vector_name", "input_json": the input as a JSON string (escaped), "canonical_output": the exact JCS serialization as a string, "rule": which RFC 8785 section/rule produces this behavior, "divergence_trap": what a naive implementation (e.g. plain JSON.stringify with sorted keys) produces instead, if different, "certainty": "rfc-exact" | "probable" | "unsure-flagged"}

**Hard rules:** every vector will be executed against a reference JCS implementation — a wrong canonical_output discards the vector, but a correctly-identified divergence_trap is the prize (those become gate tests); the UTF-16 ordering case and the number-formatting cases (ES6 serialization of doubles) are the highest-value and hardest — attempt them with honest certainty labels; fewer exact vectors beat twelve approximate ones. No prose outside the JSON.

[prompt-version: C2-JCS-v1 2026-08-31]
