---
name: delivery-implement
description: Implement a scoped repository dispatch and produce a verifiable handoff for an independent audit. Use when a user asks an agent to build a task prepared by delivery-backlog or to address an audit remediation round.
---

# Delivery Implement

The invocation argument is the dispatch slug. Work in the feature branch and worktree recorded by the dispatch. Read that checkout's `AGENTS.md` and `AGENT_WORKFLOW.md` when present, then read `.agent-delivery/dispatch/<slug>.md` there. The dispatch must provide the task scope and verification even when the optional workflow file is absent. If the dispatch is absent, ask for the task source or have `delivery-backlog` prepare it; do not guess the assignment.

## Before editing

- Read the dispatch round, outcome, scope, non-goals, and verification. Compare its `Base`, `Parent branch`, `Feature branch`, `Worktree`, and `Pre-existing changes` with the current repository state. Reconcile changes since dispatch before editing. Do not work on the integration branch or in another agent's checkout. If the dispatch's `Worktree` is the repository's main checkout (its `.git` is a directory, not a file pointing at a worktree), or the checkout is on the integration branch, stop and report it: the task must be re-dispatched into its own worktree. If a task path already contained user changes, isolate the task or establish an explicit baseline; never treat the whole file diff as your work.
- Read the relevant source and tests. Recheck any prerequisite that could have changed since dispatch.
- In a remediation round, inspect the existing work and address the named findings in place. Preserve portions the audit accepted.

## Implement and verify

- Make the smallest coherent change that satisfies the outcome. Use existing project patterns and follow the user's scope.
- Run the affected tests, lint/build checks, and observable checks in the dispatch or `AGENT_WORKFLOW.md`. Do not claim a check passed unless it ran and produced that result.
- Update the project's backlog or status files when the task requires it. Keep the task in progress until an independent audit accepts it; record outstanding deployment or device checks honestly.
- Do not commit, push, publish, or deploy as part of this handoff unless the user explicitly asks for that action. Leave unrelated changes untouched.

## Handoff

Write `.agent-delivery/dispatch/<slug>.summary.md` with:

```md
# Implementation summary: <slug> — Round <N>
Base: <branch-point commit SHA used>
Branch: <feature branch used>
Worktree: <checkout path used>

## Worktree changes
<Task-owned changed and untracked paths; pre-existing changes left untouched or reconciled>

## Changed
<Files and behavior, with reasons>

## Verification
<Exact commands, results, and meaningful counts; note anything not run>

## Invariants and limitations
<Project-specific boundaries checked, deviations, remaining work>
```

Summarize the result to the user and point to `delivery-audit`. The summary is evidence to inspect, not proof that the implementation is correct.
