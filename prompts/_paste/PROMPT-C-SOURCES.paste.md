You are helping build a verified source registry for ASIC physical-design failure-and-recovery
stories (design-closure war stories: congestion, timing closure, CTS, power-grid, silicon bring-up).
Two tasks, both required.

TASK 1 — ANCHOR CHECK (calibration; answer all three). For each citation, state whether it exists
exactly as cited, exists but the citation is wrong (give the correction), or you do not know:

  a1: R. E. Kessler, "The Alpha 21264 Microprocessor," IEEE Micro, vol. 19, no. 2, pp. 24-36, March-April 1999.
  a2: P. Kongetira, K. Aingaran, K. Olukotun, "Niagara: A 32-Way Multithreaded SPARC Processor," IEEE Micro, vol. 25, no. 2, pp. 21-29, March-April 2005.
  a3: G. Hinton, D. Sager, M. Upton, D. Boggs, D. Carmean, A. Kyker, P. Roussel, "The Microarchitecture of the Pentium 4 Processor," IEEE Micro, vol. 21, 2007.

TASK 2 — NEW SOURCES (the actual value). List up to 8 PUBLIC, nameable sources of real ASIC
physical-design failure-and-recovery stories or detailed design-closure war stories — conference
talks, journal/magazine papers, book chapters, engineering blog postmortems, or well-known
forum/mailing-list threads. We ALREADY OWN: the two IEEE Micro papers above in their correct
citations, Hinton et al.'s Pentium 4 paper (Intel Technology Journal, Q1 2001), and Tendler et
al.'s POWER4 system microarchitecture plus Warnock et al.'s POWER4 circuit/physical design (both
IBM Journal of Research and Development, vol. 46, no. 1, 2002). Naming those five, or trivial
variants of them, has zero value to us. At most 2 entries per source type. Only include sources
you can actually NAME; do not invent titles.

**Output: a single bare JSON object and nothing else:**

{"prompt":"C-v5","model":"<your exact model name, as you state it>","date":"<today YYYY-MM-DD>",
 "anchors":{"a1":"exists-exactly | exists-but-citation-wrong: <the correction> | unknown",
            "a2":"…same…","a3":"…same…"},
 "sources":[{"title":"…","venue_or_publication":"…","year":0,"what_it_covers":"…",
             "why_relevant":"…","confidence":0.0,"knowledge_basis":"training-recall",
             "verification_hint":"…","access_guess":"free"}]}

- confidence (0.0–1.0) = your confidence the source exists exactly as named.
- knowledge_basis: "training-recall" | "recalled-citation" | "guess" — how you actually know it.
- verification_hint = the exact search phrase or URL that would confirm existence.
- access_guess = "free" | "paywalled" | "unknown".
- Fewer honest entries beat eight invented ones; "sources":[] is acceptable. No prose outside the
  JSON.

[prompt-version: C-v5 2026-09-09 — over C-v4: self-identification header, three anchor probes,
novelty contract against the owned set, per-source knowledge_basis / verification_hint /
access_guess, strata caps, array→object output shape]

---

