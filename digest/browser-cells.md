# Browser Constraint Matrix — Prompt B cells merged, and checked against the first real measurements

**Status: model claims, with a measured ground truth for part of the matrix.** The B outputs are
research claims made by models against live web search. As of 2026-08-31 the zkprof project has its
**first real browser measurements**, which means several of these cells no longer need a model's
opinion. Where a measurement exists, **the measurement wins and the model claims are graded against
it.**

**Corpus:** 77 B-cell entries across 7 model-runs (kimi R1+R2, sonnet R1+R2, glm 5.3 R1+R2,
meta R1, opus 5 R1, opus R2, tencent yunbao R1). Heavy overlap — kimi and sonnet resubmitted
identical cell sets in both runs, so the effective independent sample is ~5 models.

**Measured ground truth used below** — read read-only from the zkprof repo's
`browser-run-1/measurements` branch, `measurements/2026-08-31-chrome/`:

> **Chrome 151.0.7922.175, `--headless=new`, Windows 11, i9-10850K (20 logical), RTX 3080.**
> Two server modes: isolated (`COOP: same-origin` / `COEP: require-corp`) and `--no-isolation`.
> Single machine, single sample. The repo's own README states this explicitly: *"These are
> single-machine, single-session, single-sample measurements. Not a benchmark."* Every use below
> respects that — these are used to **falsify categorical claims** ("feature X is not available"),
> which one sample can legitimately do, and never to establish a performance fact.

---

## Cell 1 — SharedArrayBuffer + cross-origin isolation (COOP/COEP)

**Model consensus (7/7, no dissent):** COOP `same-origin` + COEP `require-corp` (or `credentialless`,
Chromium-only) on the top-level document; SharedArrayBuffer gated on the resulting
`crossOriginIsolated` state; Chrome desktop 92+/Android 88+, Edge 92+, Firefox 79+. No 2026 change
found by anyone. Two models add that `Permissions-Policy: cross-origin-isolated` can additionally
gate child frames (meta, tencent yunbao).

**Measured:** ✅ **confirmed, and refined.** Isolated mode → `crossOriginIsolated: true`,
`threads.shared_array_buffer: true`, 20 logical processors reported. No-isolation mode →
`crossOriginIsolated: false`, `shared_array_buffer: false`.

**Refinement the models did not make.** In *both* modes the probe reports
`wasm-threads: TESTED — "threads: engine accepts the module"`. That is, **WebAssembly threads
module validation succeeds without cross-origin isolation; it is the `SharedArrayBuffer` constructor
that is gated, not the wasm feature.** Several models collapse these ("WASM threads silently fail or
fall back to single-threaded" — mimo; "Threads: supported… with cross-origin isolation" — kimi).
The distinction matters operationally: a feature-detection routine that tests wasm-threads module
validation will report threads available on a non-isolated page where they cannot actually be used.

**Honesty note.** Every model marked its "nothing changed in 2026" half as weak — glm ("no
2026-specific browser-release confirmation retrieved"), opus ("absence of evidence, not
verification"). That was the right call and the measurement does not resolve it either; a single
Chrome build cannot show that nothing changed anywhere.

**Status: MEASURED (Chrome 151 only). Firefox / Safari remain model-claim only.**

---

## Cell 2a — WebGPU compute-shader availability

**Model claims:** Chrome/Edge 113+; Firefox 141 (Windows) / 145–147 (macOS), Linux+Android
incomplete; Safari 26 (macOS Tahoe 26 / iOS 26 / iPadOS 26 / visionOS 26). opus R2 fetched the
authoritative gpuweb Implementation-Status wiki directly and confirmed the per-platform granularity,
including that Chrome on Windows ARM64 still needs `--enable-unsafe-webgpu` and that Firefox
Linux/Android are Nightly-only.

**Measured:** ✅ `webgpu.adapter_available: true` on Chrome 151 headless — including under
`--headless=new`, which several of the H-slice pitfalls predicted would fail (see §4).

**Status: MEASURED for Chrome. Firefox/Safari = high-confidence model claim from an authoritative
vendor page (highest-quality unmeasured cell in the matrix).**

---

## Cell 2b — is `timestamp-query` exposed to web content by default?

**This is the cell the pipeline flagged twice as "measure, don't research". It has now been
measured, and the models were split.**

| Model | Claim | Verdict against measurement |
|---|---|---|
| sonnet (R1+R2, "verified from current authoritative page") | "timestamp-query is **NOT exposed by default** to ordinary web content in Chrome; full-precision access requires the WebGPU Developer Features flag" | ❌ **falsified on availability** |
| tencent yunbao (conf high) | "Chrome/Edge **enabled by default since Chrome 121**, quantized to 100 µs" | ✅ availability confirmed |
| glm 5.3 ("verified from a current authoritative page for Chrome") | "Chrome shipped timestamp-query by default; it remains spec-optional — apps must check `adapter.features.has()`" | ✅ confirmed |
| kimi | "optional adapter feature… values quantized to 100 µs by default; `enable-webgpu-developer-features` needed for unquantized precision" | ✅ on availability; quantization **not measured** |
| meta | "optional WebGPU feature, must be requested via `requiredFeatures`, not enabled by default" | ✅ as a spec statement; ambiguous as an availability claim |
| opus (R1 and R2) | `UNVERIFIED` — and in R2, after fetching the authoritative page, reported it as a *verified gap*: the gpuweb status page does not mention timestamp-query at all | correct process, no answer |

**Measured:** `webgpu.timestamp_query: **true**` in **both** isolated and non-isolated modes,
Chrome 151 headless, no flags beyond `--headless=new`.

**Resolution.** The feature **is** exposed to ordinary web content by default in Chrome 151, and its
exposure does **not** depend on cross-origin isolation. sonnet's flat "not exposed by default" is
wrong; the models that framed it as "exposed but spec-optional and quantized" (yunbao, glm, kimi)
are right on the part that was measured.

**Still open, and it is the part that matters:** the **100 µs quantization** claim. Three models
assert it independently; the probe records only a boolean. A quantized timestamp-query is nearly
useless for the sub-100 µs kernels a proving workload cares about, so *availability without
resolution is not an answer*. **Recommend extending the probe to measure timestamp-query
granularity, not just presence** — that is the residual "measure, don't research" item for this cell.

---

## Cell 3 — WASM feature status (threads, SIMD128, relaxed-SIMD, JSPI, memory64)

**This cell produced the sharpest model-vs-measurement conflict in the matrix.**

| Feature | Model claims | Measured (Chrome 151, both modes) |
|---|---|---|
| baseline | — | **TESTED** |
| threads | "all four browsers with COI" (kimi, sonnet, meta) | **TESTED** — module accepted in both modes (see cell 1 refinement) |
| SIMD128 | "Chrome 91+, Edge 91+, Firefox 89+, Safari 16.4+" (kimi) | **TESTED** ✅ |
| **relaxed-SIMD** | kimi, "verified from current authoritative page": "Chrome 114+, Firefox 120+, Safari 18.4+; **webassembly.org lists Full Support for all four browsers**". glm/sonnet: "part of the standardized Wasm 3.0 set, shipping in current versions" | ❌ **UNAVAILABLE** — *"relaxed-simd: engine did not accept the module (unsupported or not compiled in)"* |
| **memory64** | kimi: "Chrome 133+ (Feb 2025), Edge 133+, Firefox 134+; Safari does NOT support". meta/glm: standardized in Wasm 3.0 | ❌ **UNAVAILABLE** — *"memory64: engine did not accept the module"* |
| JSPI | kimi: "Chrome 137+ stable since May 2025; Firefox Nightly-only; Safari 27 beta". meta: "Chrome 137+, Firefox 153+, Node 25+, Safari TP 238+" | **TESTED** — *"WebAssembly.promising / Suspending present"* ✅ |

**Reading the conflict honestly.** A model claiming "verified from an authoritative page" that
relaxed-SIMD and memory64 are broadly shipped is contradicted by a real Chrome 151 refusing both
modules. Two readings, and they are not equally likely but both must be stated:

1. **The features are genuinely not enabled in this build/configuration.** Most likely. Headless
   Chrome, a specific build, and possibly flag-gated features would all produce exactly this.
2. **The probe's test modules are wrong.** Not dismissible: `ENVIRONMENT.md` records that *"the first
   browser run of the probe found and fixed a real bug (it read an empty env instead of the browser
   globals)"*. A freshly-debugged instrument's negative results deserve one confirmation pass.

**Recommended resolution, cheap:** validate the probe's relaxed-SIMD and memory64 test modules
against a known-good reference (e.g. `wasm-tools` or a second engine) before treating the negative
as a fact about Chrome. Until then this cell is **CONTESTED**, not resolved — and that is already
more than it was, because previously it was a stack of mutually-inconsistent blog citations with no
ground truth at all. opus's R2 entry (`UNVERIFIED`, because `webassembly.org/features` renders its
table client-side and a text fetch returns *"Loading table, please wait…"*) turns out to have been
the correctly humble answer.

---

## Cell 4 — cross-origin iframe: isolation and WebGPU (the wallet-embedding cell)

**Model claims, and they conflict on the substance:**

- **glm, opus:** an embedded cross-origin document *can* participate in an isolated context;
  Chromium provides `COEP: credentialless` (Chrome 96+) and the `credentialless` iframe attribute
  (default from Chrome 110); Chrome supports `allow="cross-origin-isolated"` delegation.
  WebGPU-in-iframe: explicitly `UNVERIFIED`.
- **tencent yunbao (conf high):** the iframe inherits the COI browsing-context group but
  `window.crossOriginIsolated` stays false **unless the parent delegates the `cross-origin-isolated`
  Permissions-Policy feature**; and therefore *"WebGPU (which requires cross-origin isolation) is NOT
  available in a cross-origin iframe by default."*
- **meta:** the WebGPU Permissions-Policy defaults to `self`, so cross-origin and sandboxed iframes
  are blocked from `navigator.gpu` unless the parent sets `allow="webgpu"`.

**Measured (partially decisive):** WebGPU adapter was available in the **non-isolated** server mode
(`crossOriginIsolated: false`, `adapter_available: true`). **This falsifies yunbao's premise that
WebGPU requires cross-origin isolation.** Whatever governs WebGPU in an iframe, it is not COI — so
yunbao's conclusion, even if it happens to be right, is right for the wrong reason. meta's
Permissions-Policy account is the one consistent with the measurement and is the hypothesis to test.

**Not measured:** the iframe case itself. Every model that addressed WebGPU-in-a-cross-origin-iframe
either marked it UNVERIFIED (glm, opus, both runs) or reasoned from the falsified premise.

**Status: still "measure, don't research" — and now with a specific, cheap experiment.** Serve the
existing probe page inside a cross-origin iframe under three conditions (no `allow`, `allow="webgpu"`,
`allow="cross-origin-isolated; webgpu"`) and record the probe's own capability matrix each time. The
instrument already exists; only the harness page is missing. This is the highest-value unbuilt
measurement in the matrix, because it is the cell an embedded-wallet deployment actually depends on.

---

## Cell 5 — published 2026 in-browser proving measurements with a reproducible harness

**Model claims:** All models converge on the same two 2025 leads and none produces a 2026 one.

- **FibRace** — "a large-scale benchmark of client-side proving on mobile devices", attributed to
  KKRT Labs (Cairo M) and Hyli, September 2025, arXiv 2510.14693; the attributed result is that
  in-browser p256 ECDSA proving was largely impractical, with only Noir reaching limited usability.
  (kimi, glm, opus; sonnet cites "the paper's own reported methodology and stated numbers".)
- **StarkWare Stwo / S-two + WebGPU** — 5× on constraint-polynomial evaluation, 2× on the overall
  pipeline; sourced only to a community news post, with neither hardware nor harness identified.
  Every model that cites it flags the source as weak.
- **ZKProphet** (arXiv 2509.22684) — GPU proving, not in-browser; correctly excluded by the models
  that mention it.
- meta rates its own cell-5 answer **0.35**, the lowest confidence anywhere in the B corpus. That is
  the correct posture.

**Measured — and this is the useful part:** the project now has its own numbers, which do not settle
the literature question but do change what the cell is *for*.

| Measurement (groth16-bn254-merkle-poseidon-d64, one sample each) | isolated | no-isolation |
|---|---|---|
| total, scalar | 3101.1 ms | 4584.8 ms |
| total, `+simd128` | 2970.3 ms | 2951.2 ms |
| MSM share of total (isolated scalar) | 2589.1 ms = **83.5%** | — |
| witness_gen / ntt_fft / field_arith (isolated scalar) | 338.4 / 164.5 / 1.6 ms | — |
| timer resolution | **4.999995 µs** | **99.999994 µs** |

Two things follow directly:

1. **`+simd128` buys ~4% on this workload** (3101 → 2970 ms, isolated). The corpus-wide H-slice
   pitfall *"SIMD128 exists but the field-arithmetic hot loop remains effectively scalar"* (asserted
   by 9 of 11 H models) is **consistent with this measurement**. It is one sample and MSM dominates
   at 83.5%, so the honest statement is "the measured delta is small and the pitfall's prediction is
   not contradicted", not "the pitfall is confirmed".
2. **Do not read the isolated-vs-non-isolated totals as an isolation effect.** The repo's README
   says so explicitly: the scalar pair (3101 vs 4585 ms) *"differ by ~1.5× for the same profile,
   which is normal run-to-run / machine-state variance, not evidence of anything"* — and the simd
   pair (2970 vs 2951) shows essentially no difference, which is what makes the scalar pair's spread
   obviously noise.

**Status: cell 5 remains UNVERIFIED as a literature question** (no model produced a 2026 measurement
with a reproducible harness; the strongest lead, FibRace/arXiv 2510.14693, is 2025 and mobile-focused
and nobody opened the paper). But the project no longer *needs* the literature to have a browser
number of its own.

---

## Cell 6 (new) — timer resolution, which no B cell asked about but every H pitfall depends on

**Measured:** isolated **5.0 µs**, non-isolated **100.0 µs** — a clean 20× difference, exactly the
`crossOriginIsolated` clock-coarsening the H-slice pitfalls describe.

This is worth promoting to a matrix cell because it is the number that decides whether any
measurement in a non-isolated context means anything. And it lets one specific model claim be
graded: **minimax m3's H-pitfall says "performance.now() clamped at 5 ms for non-isolated contexts"**
— that is wrong by 50× (it is 100 µs), and it appears to have swapped in the *isolated* figure's
magnitude with the wrong unit. kimi, chatgpt, gemini, grok, meta, mistral, qwen and yuanbao all
describe the mechanism correctly without committing to a number, which is the safer form.

---

## 4. The H slice — 119 proving pitfalls, a corpus the commission's map does not list

Twelve `* h.json` files (chatgpt, deepseek, gemini, grok, kimi, meta, minimax 2.7, minimax m3,
mistral, qwen, yuanbao — plus one mimo prose refusal) contain **119 recovered pitfall objects** from
Prompt H (`prompts/PROMPT-H-PROVING-PITFALLS.md`, H-v1). This is the single largest unlisted slice in
the collection folder and it is directly relevant to this deliverable, so it is classified here.

**Shape:** `{pitfall_name, what_happens, why, how_discovered, mitigation, affects, confidence}`,
where `affects ∈ {correctness, performance, measurement-validity, deployment}`. Format compliance
was near-perfect — 11 of 12 models produced clean bare arrays.

**Convergence is extreme.** Eleven distinct pitfalls account for most of the 119, and nine of them
appear in 9+ of the 11 models: JS↔WASM marshalling copies; SharedArrayBuffer/COOP/COEP deployment;
wasm32 4 GiB ceiling; SIMD not vectorizing field arithmetic; WebGPU readback stalls counted as
compute; timestamp-query availability/quantization; timer clamping; JIT warmup and tiering; GC pauses
attributed to the workload; mobile memory kills; Safari divergences; iframe restrictions.

**The `measurement-validity` subset is the valuable part** (the prompt said so, and the models
complied — 48 of 119 entries are tagged `measurement-validity`). Cross-checked against the real run:

| Pitfall | Models | Status against the 2026-08-31 Chrome run |
|---|---|---|
| Timer clamping without COI distorts microbenchmarks | 9 | ✅ **confirmed and quantified** — 5 µs vs 100 µs |
| WebGPU readback/`mapAsync` stall counted as GPU compute | 10 | not tested — the harness measures wasm phases, no GPU path exercised |
| JIT warmup / tiering (Liftoff→TurboFan) contaminating early runs | 10 | **untested and unmitigated in the current harness** — the reports are single-sample with no warm-up discipline recorded. This is the pitfall most likely to be *actively affecting* the numbers in cell 5 |
| GC pauses attributed to the proving kernel | 6 | not tested |
| timestamp-query unavailable/quantized | 9 | ⚠ availability **falsified** (it is available); quantization untested |
| Marshalling dominates proving time | yuanbao (conf 0.92), and implied by 10 others | ❌ **falsified for this workload** — the marshalling bench shows the Poseidon batch rows at **0.95%–2.45%** marshalling share; the 100% rows are the pure-copy control workloads, not real proving |

**Two findings worth carrying out of this slice:**

1. **The single most-agreed pitfall in the corpus (marshalling overhead) does not hold for the
   project's actual workload.** Ten models independently warn that JS↔WASM copying dominates; the
   measured share on batch workloads is under 2.5%. The pitfall is real in general and irrelevant
   here, because MSM is 83.5% of the time. This is a good illustration of why a consensus pitfall
   list is not a priority list.
2. **The one pitfall that is probably biting right now is the one nobody has checked.** JIT
   tiering — 10 models, confidences 0.85–0.99 — and the current measurement methodology is
   single-sample with no recorded warm-up. Before any of the cell-5 numbers are used for anything,
   run the harness N times per configuration and report the distribution. That is a cheap change to
   an instrument that already exists.

**Recommendation:** keep the H slice as its own artefact (it is a genuinely useful practitioner
checklist for the zkprof work) and add `pitfall → measured/untested/falsified` as a standing column,
refreshed after each browser run. It is the only part of this collection effort that has a real
feedback loop attached.

---

## 5. Matrix status summary

| Cell | Status | Next action |
|---|---|---|
| 1 SAB + COI | **MEASURED** (Chrome 151); models unanimous and correct | Measure Firefox/Safari, or accept the model claim |
| 2a WebGPU availability | **MEASURED** (Chrome); vendor status page read directly for the rest | none — best-sourced cell in the matrix |
| 2b timestamp-query exposure | **MEASURED — sonnet falsified**; availability yes | **measure quantization granularity**, which is the part that matters |
| 3 WASM features | **CONTESTED** — relaxed-SIMD and memory64 measured UNAVAILABLE against confident model claims of broad support | validate the probe's test modules, then re-measure |
| 4 iframe isolation + WebGPU | **PARTIAL; yunbao's premise falsified** | run the probe inside a cross-origin iframe under three `allow` conditions — highest-value unbuilt measurement |
| 5 published 2026 measurements | **UNVERIFIED** as a literature question; project has its own numbers now | open arXiv 2510.14693 (FibRace) and extract its harness, or drop the cell |
| 6 timer resolution *(new)* | **MEASURED** — 5 µs / 100 µs | promote to a standing cell; it gates every other measurement |

**Cells where every model said UNVERIFIED and a measurement has since answered it: 2b.** That is one
confirmed win for the "measure, don't research" rule, and it cost one probe page.
