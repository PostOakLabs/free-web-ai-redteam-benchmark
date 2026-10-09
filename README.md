# Free web AI red-team benchmark

Over eight collection days, from 31 August to 17 September 2026, structured prompts were pasted by hand into the free web chat interface of 16 AI services. Every reply was saved verbatim. Nothing was automated and nothing was paid for.

The replies were then graded. Most were graded by mechanical recomputation. The paper-recall answers were checked against the papers themselves.

## Read the results

Open `digest/report/days/index.html` in a browser. There is an overview page plus one page per day. The pages are self-contained; only Google Fonts load from the network.

## What is in this repository

| Path | Contents |
|---|---|
| `digest/report/days/` | The report pages |
| `digest/report/build_days.py`, `_day_scenes.py`, `_staircase_kit.py` | The page generator. Run `python digest/report/build_days.py` to rebuild the pages. |
| `Web Model Tasks/Day 1/` to `Day 8/` | The replies as collected |
| `Web Model Tasks/RUN-MANIFEST.tsv` | The run manifest |
| `prompts/` | The prompts as sent |
| `digest/` | The grading reports and verification scripts the pages cite |
| `redteam/` and the root-level `.md` files | Other files the pages cite as sources |

Every file a page cites as a source is included at the path the page gives.

## Licence

- **Code** (the page generator and the verification scripts): MIT. See [`LICENSE`](LICENSE).
- **Written content** (the pages, reports and prompts): CC BY 4.0. See [`LICENSE-content.md`](LICENSE-content.md).
- **Model replies** under `Web Model Tasks/`: third-party output, reproduced as collected. No rights are claimed in them.
