You are cataloging the practical pitfalls of running cryptographic proving workloads in the browser (WebAssembly and WebGPU) — the footguns practitioners hit that never make it into documentation.

**List up to 12 pitfalls** across areas like: JS↔WASM data marshalling and copying; SharedArrayBuffer/cross-origin-isolation deployment; wasm memory growth and 32-bit address-space limits; WASM threads and worker pools; SIMD codegen not actually vectorizing field arithmetic; WebGPU buffer mapping and readback stalls; GPU timestamp-query availability and quantization; browser timer resolution and measurement distortion; iframe/embedded-context restrictions; mobile browser memory kills; JIT warmup and tiering distorting benchmarks; Safari-specific divergences.

**Each pitfall is one object:**

{"pitfall_name", "what_happens": the observable failure or silent distortion, "why": the underlying mechanism, "how_discovered": the symptom that usually reveals it (and how long it typically wastes before diagnosis), "mitigation": what actually works, "affects": "correctness" | "performance" | "measurement-validity" | "deployment", "confidence": 0.0–1.0}

**Hard rules:** "measurement-validity" pitfalls are the most valuable — things that make benchmark numbers LIE (timer clamping, JIT tiering mid-run, GC pauses attributed to the workload, readback synchronization counted as compute). Be specific about mechanism; a pitfall without a "why" is a rumor. Only include browser/runtime behaviors you genuinely know; mark browser-specific claims with the browser and a confidence reflecting how current your knowledge is. Fewer sharp entries beat twelve vague ones. **Output: a single bare JSON array and NOTHING else.**

[prompt-version: H-v1 2026-08-31]
