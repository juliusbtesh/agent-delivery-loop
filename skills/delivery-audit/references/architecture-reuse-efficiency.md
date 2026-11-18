# Lens: architecture, reuse and efficiency

Does the change solve the need the way this codebase already solves it, without duplicating what exists or adding avoidable work? Matching names and local style is not enough: inspect representative implementations outside the diff and trace their producers and consumers.

## Depth

- **Compact** (a small addition in an established area): search for an existing helper, component, query or rule that already does this, and check the obvious cost of the changed path.
- **Full** (a new endpoint, service, data source, state store or loading path): do all of the sections below.

## Fit with existing architecture and data flows

- Find how the codebase handles the same or an analogous need, and anchor any claimed mismatch to that concrete location with its behavioural or maintenance consequence.
- For anything new, identify whether an established path already supplies, or could appropriately supply, the information: existing response contracts, bootstrap or settings data, shared queries, caches.
- Weigh both sufficiency and incremental cost: whether the data is available at the point of use, authorization and scope, freshness, the source of truth, request and query count, payload size, latency and request waterfalls, cache invalidation, loading and error states, and ongoing maintenance. Check whether old and new consumers can now disagree or apply different rules.
- Accept a justified departure. Flag an inconsistency when it introduces a concrete behaviour gap, avoidable overhead, a duplicated responsibility or a repository rule violation, and explain why the established path is a viable alternative and what it would cost. When intent or workload evidence is missing, state the uncertainty; novelty alone is not a defect.
- Check, where relevant: naming, error handling, authorization gates, persistence, migration and backfill, logging, feature flags, dependency registration, serialization, null handling and tests.

## Duplication and reuse

- Search for existing helpers, components, queries, validators and business rules that overlap the changed code, including a new method that repeats one that already exists. Look for semantic duplication as well as copy and paste: two implementations of one rule drift apart even when their syntax differs. Name the overlapping locations and the maintenance cost, inconsistency risk or repeated runtime work.
- Recommend reuse only when the implementations share the same contract and ownership. Similar-looking code with different meaning does not need a shared abstraction. Consider coupling, readability and migration cost before recommending consolidation.

## Efficiency

- Trace the cost of the affected workflow: request and query count, data volume, computation, memory, I/O and repeated work. Check for one-query-per-item patterns, scans or nested loops that scale poorly, unbounded reads, redundant network calls, independent operations run serially, unnecessary re-renders or subscriptions, and caching or batching that does not take effect.
- Ground a performance concern in a concrete trigger and a plausible workload, using query structure, call counts, complexity, existing limits or a targeted measurement. State estimates and unknowns; do not claim a measured gain without a measurement.
- Look for a simpler implementation or a better use of an existing capability that reduces work while preserving behaviour, authorization, ordering, error handling and freshness. Do not ask for speculative caching, concurrency or an architectural rewrite.

## Reporting

A material regression or a concrete maintainability gap is a finding. A worthwhile improvement that does not block acceptance goes in a short follow-up list with the affected locations, the expected benefit and a reasonable next step. Do not manufacture opportunities or widen the audit into unrelated cleanup.
