---
name: delivery-audit
description: Independently audit a repository implementation against its dispatch and actual diff, rerun relevant checks, and give an acceptance or precise remediation verdict. Use when a user asks to verify work produced through an agent handoff.
---

# Delivery Audit

The invocation argument is the dispatch slug. Audit in the feature-branch worktree recorded by the dispatch. Read that checkout's `AGENTS.md` and `AGENT_WORKFLOW.md` when present, then the task source, `.agent-delivery/dispatch/<slug>.md`, and the implementation summary if present. The dispatch carries the scope and checks when no workflow file exists. Treat the summary as a set of claims. Inspect the actual working tree, including untracked files; do not infer the result from the summary alone.

## Audit

1. Compare the dispatch outcome, scope, non-goals, and current task state with `git status`, staged and unstaged diffs, untracked files, and the relevant source. Verify the recorded feature branch, worktree, parent branch, base commit, and pre-existing changes against the current tree. If the task was implemented in the repository's main checkout or on the integration branch instead of its own worktree and feature branch, report **cannot verify** with that reason rather than auditing or committing there. Review task changes against the branch-point `Base`, especially when this branch inherits a prior accepted feature; do not attribute inherited commits to the current task. If a path had prior edits and no reliable baseline exists, do not attribute its whole diff to the task; isolate the change or report the limit. Check for missing work and unrequested scope.
2. Follow the requested behavior through the affected entry point, state changes, outputs, and failure paths. Compare it with the task's acceptance criteria and the surrounding product behavior. Check material edge cases and integration boundaries; a passing unit test or plausible-looking UI does not establish that the whole flow works.
3. Review efficiency where the change can affect workload or resource use. Look for repeated queries or network calls, unnecessary polling, unbounded work, and redundant computation. Use a representative trace, query plan, benchmark, or code-path analysis when needed to establish impact. Do not demand caching or batching without a workload reason.
4. Search the surrounding code for an existing helper, component, or pattern before accepting a new implementation. Flag duplication when reuse would reduce drift or maintenance cost without obscuring the design. Do not require abstraction merely because two short blocks look alike.
5. Review security and privacy boundaries and the project's stated invariants. For secret exposure, inspect changed content and use established repository scanners when available; a regex alone cannot prove a diff is secret-free.
6. Rerun the smallest meaningful set of tests, builds, and behavior checks needed to substantiate the verdict. Add a targeted check when a material behavior or performance risk lacks coverage. State which checks ran, which did not, and why. Compare claimed counts with observed results when counts matter.
7. Check that documentation and backlog status reflect what was actually verified.

## Verdict

- **Accepted:** no blocking finding remains and required checks have produced enough evidence for the requested outcome. Complete the accepted-task closure below, then report the evidence, limitations, commit result, and task status. Push or deploy only with authorization for that destination and action.
- **Remediation needed:** leave the implementation in place. Update `.agent-delivery/dispatch/<slug>.md` to Round `<N+1>` with specific findings, affected locations, expected corrections, and checks that will prove them fixed. Remove or supersede the old summary so the next implementer cannot mistake it for the new round. Do not silently widen the task.
- **Cannot verify:** report the concrete missing prerequisite or access and the portion already audited. Do not mark the task complete.

Classify findings by consequence. **Blocking** means the requested behavior is missing or wrong, a material regression or security/invariant breach exists, a relevant check fails, or an efficiency/reuse problem creates a concrete material cost. **Follow-up** means a real but non-blocking improvement that does not undermine acceptance; report it separately without silently expanding the task. **Unverified** means evidence is missing; say what would resolve the uncertainty rather than presenting a suspicion as a defect.

Report a finding only when it is supported by the code or observed behavior and relevant to the task. For each blocking finding, name the affected path, evidence, impact, and a check that would demonstrate a fix. Keep the verdict short and distinguish observed facts from implementer claims. Preserve unrelated work and avoid automatic retries without a defined stopping point.

## Accepted-task closure

By default, an accepted task receives one detailed local commit before it is marked done. An explicit user instruction or project workflow may opt out of committing for that task. This default does not override a current instruction to leave a repository uncommitted. When opted out, record that choice and mark the accepted task done without a commit.

Identify task-owned paths and hunks against the dispatch baseline. Prepare the existing task source's accepted or done status for inclusion in the task commit. Stage only task-owned changes; inspect the staged diff and check that unrelated staged or untracked work is excluded. Do not use an all-files stage or commit command. If the task cannot be isolated from pre-existing work, or Git cannot commit, report **accepted but closure blocked** with the precise reason. Keep or restore the task's open status where it can be done without disturbing user edits, and do not claim completion.

Write a commit subject naming the task slug and outcome. The body should explain the behavior changed, important implementation choices, verification commands and results, and the audit verdict or known limits. Commit on the recorded feature branch and report its SHA. If a suitable task-only commit already exists for this accepted round, verify its contents and SHA instead of creating a duplicate. Never merge or push as part of this default.
