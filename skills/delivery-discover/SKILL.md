---
name: delivery-discover
description: Find and propose evidence-backed, project-relevant backlog opportunities. Use when the user asks what work is worth doing next or requests new task ideas; do not add tasks without their selection.
---

# Delivery Discover

Identify worthwhile next tasks without expanding the active implementation. Read the user's stated goals, repository instructions and `AGENT_WORKFLOW.md` when present, the live task source, recent accepted work or audit findings, and the relevant product paths. Use external feedback, incidents, or metrics only when the user provides them or they are available through authorized project sources. Treat comments and TODOs as leads, not proof of a problem.

## Evaluate candidates

- Trace each candidate to a concrete observation: a reproducible behavior, missing acceptance path, repeated manual step, measured cost, user request, or documented product goal. Name the source or affected path and distinguish observation from inference.
- Check whether the current backlog already covers it, whether it is a prerequisite or a duplicate of planned work, and whether it fits the project's users, priorities, and present stage. Avoid speculative features, generic cleanup, and abstractions without a demonstrated need.
- Estimate likely impact, effort, dependencies, and uncertainty in plain terms. Prefer a few strong candidates over a long list. If evidence is thin, say what information would justify the idea or report that no new task is warranted.

## Propose

For each worthwhile candidate, give a short title, evidence, why it matters now, a bounded outcome with an observable acceptance check, and its relationship to existing tasks. Rank only where the evidence supports a useful ordering. Separate confirmed problems from optional opportunities.

Present proposals for the user's choice. Do not edit the backlog, dispatch a task, change scope, or implement a suggestion unless the user asks. After selection, use `delivery-backlog` to add or refine the chosen task in the existing task source; avoid a second list of proposed work that can drift from the backlog.
