# Expert-Interview Elicitation Guide — merged from Prompt Q

> # ⏸ PARKED
>
> **This is soft, qualitative material and it is not on the deterministic north star.** Nothing here
> can be verified by recomputation, checked against a clause, or falsified by a measurement — the
> three things the rest of this digest relies on. It is retained on the explicit condition that it
> becomes useful only **if a human expert ever engages**, at which point a tested elicitation protocol
> would be worth having ready. Until then it consumes no further pipeline time and should not be
> iterated on.
>
> Filed here rather than discarded because the cost of keeping it is a file, and the cost of
> regenerating it later is another collection run.

**Status: DRAFT SCAFFOLDING, NOT EXPERT DATA.** Merged model output, 2026-08-31, run marker
`free-model-harvest/Q/2026-08-31`.

**Corpus:** 14 `* q.json` files → **212 items**, the largest per-file yield of any slice. 13 models
produced usable structure; `mimo q.json` is a prose refusal (its 13th). `glm 5.3 flash q.json` is —
again — the Alpha 21264 recall, its eighth submission of the same text; excluded.

**Section coverage across the merged corpus:** 80 decompression questions, 44 anti-patterns, 20
rejected-path questions, 15 number-elicitation, 15 verification, 6 opening, 4 closing.

**Named techniques, unprompted:** Critical Decision Method (7 entries), cognitive interviewing (6),
timeline reconstruction (5). The prompt asked models to name the technique when they used one, and
they did — the material is at least grounded in real elicitation literature rather than invented
wholesale.

---

## 1. Opening — surfacing a story worth telling

The consensus move is to select for *felt stakes* rather than asking for a case study. The sharpest
version:

> *"Think about the last time you looked at a timing report or a DRC report and felt your stomach
> drop — a point where you knew your weekend was gone. Walk me back: what design stage were you in?"*

Others in the same family: ask for the failure the interviewee *still argues about*; ask for the one
they would warn a new hire about; ask for a block that taped out late and why. All avoid the phrase
"case study", which several models flag as producing success theatre.

`models: chatgpt, deepseek, grok, kimi, minimax 2.7, yuanbao`

---

## 2. Decompression — one question per record field

80 questions merged; the union maps cleanly onto the target record shape. Best-phrased per field:

| Record field | Question | `leading_risk` and the neutral fix |
|---|---|---|
| **prior_state** | *"Before you spotted the problem, what was the state of your design? Give me the exact milestone — post-CTS? post-route? — and the key numbers you were tracking."* | Naming a number leads: *"Was your utilization over 80%?"* forces it. Neutral: *"What was the utilization at that stage?"* |
| **observation** | *"What did you actually see first — which report, which line, which number?"* | Asking "what went wrong" invites a diagnosis where you want an observation |
| **hypothesis** | *"At that moment, before you'd checked anything, what did you *think* was happening?"* | The past-tense framing matters; present tense recruits hindsight |
| **candidates_considered** | see §3 — this is the hard one | |
| **chosen_intervention** | *"Walk me through exactly what you changed, in the order you changed it."* | *"So you fixed it by re-placing?"* supplies the answer |
| **post_state** | *"What did the same reports say after?"* | Asking "did it work?" gets a yes |
| **lessons** | *"What would you do differently on the next block — and what wouldn't you change?"* | The second clause prevents a manufactured regret |

**The `leading_risk` field was the prompt's best design decision.** 135 of the 212 items carry one,
and they are specific rather than generic — the *"Did you try X?" vs "What did you try?"* distinction
appears in five independent models with the same reasoning: naming an intervention contaminates the
alternatives list, and the contamination is invisible in the finished record.

---

## 3. Rejected paths — the hardest material, and where the guide earns its keep

Every model agrees this is the part experts do not volunteer, and the memory-jogging techniques are
the most differentiated content in the slice:

- **Timeline-then-branch (CDM).** *"Draw a mental timeline: at the moment you saw the problem, what
  were your top three options, and in what order did you eliminate them?"* Ordering the eliminations
  recovers paths that a flat "what else did you consider?" misses.
- **The meeting probe.** *"Who disagreed with you, and what did they want to do instead?"* Recovers
  alternatives through social memory rather than technical memory — the one technique here that feels
  like it came from having done it.
- **The counterfactual cost probe.** *"If the schedule had been twice as long, what would you have
  done instead?"* Surfaces the option that was rejected for schedule rather than merit — which is
  precisely the rejection class the episode schema most wants.
- **The forbidden-fix probe.** *"What was the fix everyone suggested that you knew wouldn't work?"*

`models: chatgpt, deepseek, gemini, grok, minimax 2.7, sonnet, yuanbao`

---

## 4. Numbers — recovering metrics without manufacturing precision

Consensus technique: **offer the imprecision first.**

> *"For the key numbers — WNS, TNS, overflow percentage, DRC count — give me your best recollection to
> the nearest order of magnitude. If you remember it was 'about 300 ps', that's fine. If you only
> remember it was 'hundreds of picoseconds', say that."*

Several models pair this with an explicit record convention — capture the stated precision alongside
the value, so a later reader can tell "≈300 ps" from "300 ps". That is a schema requirement disguised
as an interview technique, and it is the most directly actionable idea in the slice: **the episode
schema has no field for stated precision**, and every number in the corpus is therefore recorded as
though it were exact.

---

## 5. Verification — the polite version of "that number seems too good"

15 questions. The pattern is to challenge by asking for mechanism rather than by doubting:

> *"That's a big improvement — from 200k DRCs to just 300. How many re-route iterations did that take?
> And at each iteration, what percentage of the improvement came from the first pass versus the rest?"*

Worth noting: **that example is, almost exactly, the claim thirteen red-team models independently
attacked** in `episode-draft-bank.md` §4 — a 200k→300 DRC collapse. The model generating an interview
question and the models red-teaming an episode converged on the same implausibility from opposite
directions, without either seeing the other. That is mild evidence the effect size really is the
thing a practitioner would challenge first.

Other verification moves: ask for the same metric at two different stages and check consistency;
ask who else could confirm; ask what the number was *before* the fix a second time, later in the
conversation.

---

## 6. Anti-patterns — 44 entries, each with an observable symptom in the record

The most reusable section, because every entry is stated as *interviewer mistake → detectable trace in
the finished record*, which makes it a review checklist rather than advice:

| Interviewer mistake | Symptom in the record |
|---|---|
| Leading with a presumed root cause | Clean hypothesis-to-solution path with no evidence alternatives were weighed |
| *"Did you try X?"* instead of *"What did you try?"* | Record lists exactly the suggested X, with thin detail on why others were rejected |
| Demanding exact numbers | Metrics acquire suspicious precision with no measurement source |
| Asking for numbers before the narrative is set | Numbers that are too round; the engineer backtracks later |
| Probing detail before establishing the timeline | Events attributed to the wrong decision point |
| Treating retrospective explanation as contemporaneous knowledge | Post-hoc causal certainty where the expert was actually uncertain at the time |
| Accepting *"I fixed it quickly"* | No stepwise actions, no post-state metrics, generic feel |
| Letting the expert skip the failed first attempt | **No rejected paths — the episode reads as a straight line, which is almost never true** |

**The last one is the most useful line in the whole slice**, because it is checkable against the
existing corpus: an episode with no rejected paths, or with rejections that cite no concrete cost, is
suspect on its face. That is the same criterion the F/A grading rubric already uses, arrived at
independently from the interviewer's side.

---

## 7. Assessment

**What is genuinely good here:** the `leading_risk` discipline, the rejected-path memory-joggers
(especially the social and counterfactual probes), and the anti-pattern → symptom mapping. All three
are usable verbatim by a non-expert interviewer, which the prompt required and which most of the 212
items satisfy.

**What it cannot do:** none of this has been tested on a human. Elicitation guides fail in ways that
only contact with a real interviewee reveals — questions that read well and land badly, probes that
feel like interrogation, techniques that assume a rapport the interviewer does not have. The corpus
has no way to detect any of that.

**Why it is parked and not pursued:** the project's verifiable path runs through recomputation,
clause retrieval and measurement. This slice touches none of them. It becomes valuable the day a
human expert agrees to sit down — and on that day, having 44 pre-catalogued interviewer mistakes with
their record symptoms is worth more than the hour it would take to write them from scratch.

`TODO(alice/bob): unpark only when an interview is actually scheduled.`
