# Task: produce exact RFC 8785 (JCS) canonical serializations

For each JSON document below, output BOTH byte strings: (a) compact insertion-order serialization (keys as given, no whitespace, UTF-8) and (b) the RFC 8785/JCS canonical serialization. Every transformation you apply (key sort order, number formatting, escape handling) must be named per case. These strings are diffed byte-for-byte against a reference canonicalizer — no hashes, the strings themselves.

1. `{"b": 1, "a": 2, "C": 3}` — note: mixed case keys; state the JCS sort principle you applied (code-unit order, not locale).
2. `{"outer": {"z": true, "a": [ {"y": 1, "x": 2}, {"k": null} ]}}` — objects nested inside arrays.
3. `{"n1": 1e21, "n2": 1e-7, "n3": 0.000001, "n4": 100000000000000000000, "n5": -0, "n6": 333333333.33333329}` — JCS number serialization rules per value, each stated.
4. `{"€": "euro", "$": "dollar", "ü": "umlaut", "aa": "double"}` — key ordering under UTF-16 code-unit comparison; show the resulting order and why.
5. `{"s1": "line\nbreak", "s2": "tab\there", "s3": "quote\"inside", "s4": "unicode é", "s5": "control "}` — exact escape forms JCS mandates per string.

**Output:** bare JSON only: `[{"case": N, "compact": "<exact string>", "jcs": "<exact string>", "rules_applied": ["..."]}]` plus `{"weakest_point": "<the case you are least sure is byte-exact and the specific rule in doubt>"}`.
