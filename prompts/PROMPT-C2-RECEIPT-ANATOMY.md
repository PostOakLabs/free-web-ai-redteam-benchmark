This task is about the **RISC Zero zkVM receipt format** — the structure a verifier must understand to check a risc0 receipt, especially the groth16-wrapped form (STARK succinct receipt compressed to a Groth16 proof over BN254).

From your knowledge of the risc0 proof system (v1.x-3.x era), document the receipt anatomy **field by field**, as a bare JSON object:

{"receipt_kinds": [the receipt variants — composite/succinct/groth16 — and when each is produced],
"groth16_receipt_fields": [{"field", "type_shape", "meaning", "verifier_must_check": what a correct verifier does with this field, "failure_if_skipped": what forgery becomes possible if a verifier ignores it}],
"claim_structure": the ReceiptClaim's components (image id, journal digest, exit code, input/output digests — as precisely as you know) and how the claim digest is computed from them,
"binding_chain": step by step, what binds journal bytes → claim digest → groth16 public inputs → seal, and where the control root / verifying key enter,
"version_coupling": which parts are circuit-version-dependent (verifying key, control root/control IDs) and what breaks when a verifier uses the wrong version's parameters,
"common_verifier_bugs": [3-6 known or plausible verifier implementation errors, each with the check that catches it],
"certainty_notes": per-section honesty — which parts you know from the actual risc0 design vs general zk-receipt reasoning}

**Hard rules:** this will be checked against real risc0 receipts and the risc0 source/docs — precision beats coverage; the `certainty_notes` section is mandatory and per-section; where field names may have changed across versions, say so rather than asserting one; `failure_if_skipped` entries must name a concrete forgery/confusion, not "security issue." No prose outside the JSON.

[prompt-version: C2-RECEIPT-v1 2026-08-31]
