---
name: canon-performance
description: Measure performance and resource use when optimizing hot paths, caching, batching, changing representations, or executing metered workloads.
---

# Performance

Identify the actual expensive operation and the required behavior before optimizing. Inspect the implementation, input sizes, runtime, and frequency. Do not infer costs from a pattern name, an asymptotic label alone, or a benchmark of a different representation.

If one response already establishes that both categories are empty, do not query each category again. If several consumers need the same layout derivation, compute it at the appropriate owner and define when it becomes stale. Construction governs ownership and shared state. Recompute when inputs change; a cached wrong result is not an optimization.

For a speed or memory claim, compare equivalent behavior on representative inputs. Record implementation/runtime versions, sizes, warmup where relevant, repetitions, timing or memory method, and variability. Include boundary sizes and the actual deployed constraints. Separate build time from runtime, latency from throughput, and peak memory from allocation count. Report measurements and limitations; do not promise gains from unmeasured code.

Example: a request succeeds with 50 IDs but a production proxy rejects larger query strings. Batch based on measured/known limits and preserve complete results, ordering if required, retries, and failure visibility. A tiny staging dataset does not prove production capacity. Avoid turning one observed batch size into a universal constant.

For metered generation or external jobs, distinguish account balance, per-key limits, rate limits, and delayed usage reporting. Run a bounded pilot, persist completed units, and resume without paying for them again. Choose concurrency from observed throughput and limits. If the user knowingly authorizes removing a reserve or cap, follow that authorization and record the resulting risk; do not silently reinstate it or later misclassify the authorized choice as an agent mistake.

Do not run expensive benchmarks or regenerate data for unrelated cosmetic work. Automate repeated measurement or resumable batch work when that saves demonstrated effort. A small direct fix may need a request-count or boundary check rather than a benchmark suite.
