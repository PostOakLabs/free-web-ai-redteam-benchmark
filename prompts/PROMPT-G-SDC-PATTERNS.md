You are cataloging timing-constraint derivation patterns — the reasoning senior engineers use to WRITE and BUDGET SDC constraints, which is almost never written down publicly.

**List up to 10 distinct patterns**, drawing from situations like: deriving a block-boundary input/output delay budget; deciding a false path vs a multicycle path (and defending it); constraining a clock-domain crossing; budgeting between two blocks that haven't been implemented yet; over-constraining strategy during early implementation and when to relax; virtual clocks for IO; handling a generated/divided clock; constraining an asynchronous interface.

**Each pattern is one object:**

{"pattern_name", "situation": when this arises, "derivation": step-by-step how the constraint value or exception is actually derived (with the arithmetic shape if there is one — e.g. how a boundary budget splits available period between launch block, interconnect, and capture block), "wrong_way": the common incorrect derivation and what silently breaks downstream, "defense": how the engineer justifies this constraint in review — what evidence backs it, "signoff_risk": what happens at signoff if this constraint is wrong in each direction (too tight vs too loose), "confidence": 0.0–1.0}

**Hard rules:** the `wrong_way` and `signoff_risk` fields carry the real value — a pattern without a failure mode is a textbook entry, not engineering judgment. Arithmetic must be self-consistent. No invented chip or company names. Fewer sharp patterns beat ten shallow ones. **Output: a single bare JSON array and NOTHING else.**

[prompt-version: G-v1 2026-08-31]
