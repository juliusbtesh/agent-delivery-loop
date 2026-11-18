---
name: delivery-audit
description: Independently audit a repository implementation against its dispatch and actual diff as a senior maintainer would, at a depth weighed for the change, rerun relevant checks, and give an acceptance or precise remediation verdict. Use when a user asks to verify work produced through an agent handoff.
---

# Delivery Audit

The invocation argument is the dispatch slug. Audit in the feature-branch worktree recorded by the dispatch. Read that checkout's `AGENTS.md` and `AGENT_WORKFLOW.md` when present, then the task source, `.agent-delivery/dispatch/<slug>.md`, and the implementation summary if present. The dispatch carries the scope and checks when no workflow file exists. Treat the summary as a set of claims. Inspect the actual working tree, including untracked files; do not infer the result from the summary alone.

Review as a senior maintainer deciding whether this is ready to ship, not as a checker ticking the dispatch's list. Stay read-only until the verdict: do not fix what you find.

## Settle what the task really requires

The dispatch is the assignment, not the final word on what is correct. Before judging the work, build a short decision ledger: the task source and its acceptance criteria, the dispatch, the repository's own rules and invariants (`AGENTS.md`, `AGENT_WORKFLOW.md`, feature documents, any project skill that covers the changed surface), and later decisions by the owner that the dispatch records. Authority matters more than recency. When the dispatch contradicts a repository rule, omits one that plainly applies, or rests on an assumption the code disproves, that is a finding against the dispatch: name the contradiction and the behavior it affects, and do not accept work merely because it did what a mistaken dispatch asked. Keep unresolved product decisions separate from confirmed defects, and do not invent requirements from preference.

## Plan the audit

Weigh the change before reviewing it. Every audit runs the core steps below. Each lens is a deeper review kept in its own file under `references/`; open a lens only when the change calls for it, and at the depth it calls for. Applying every lens to every change wastes the audit and buries the findings that matter.

| Lens | Apply when the change… | File |
| --- | --- | --- |
| Product logic | alters a business rule, a workflow, a default, validation, or what a user can do or see | `references/product-logic.md` |
| Architecture, reuse and efficiency | adds a service, endpoint, helper, query, component, state store or loading path, or changes the work done per request or per item | `references/architecture-reuse-efficiency.md` |
| Security | touches a trust boundary (authentication, roles and permissions, tokens, input parsing, file or URL handling, messages between windows or services, configuration, a new dependency), or reads, stores, returns, logs, exports or sends onward sensitive data: personal, financial, health or confidential business data, credentials, or anything the project restricts to some audiences | `references/security.md` |
| Contract drift | changes something another repository, service or deployed client calls or consumes, or consumes something another repository is changing | `references/contract-drift.md` |

Start from the `Audit depth` the dispatch records, then read the diff and adjust. You may raise the depth or add a lens when the diff touches more than the dispatch expected, and must say so. You may lower or drop one only with a stated reason tied to the diff. A copy change, a style fix or a version bump usually needs the core steps only; a new endpoint or a change to who may do what usually needs most lenses. Write the plan down before reviewing: the lenses chosen, the depth of each, and the lenses skipped with the reason. The plan appears in the verdict.

## Core steps (every audit)

1. Compare the dispatch outcome, scope, non-goals, and current task state with `git status`, staged and unstaged diffs, untracked files, and the relevant source. Verify the recorded feature branch, worktree, parent branch, base commit, and pre-existing changes against the current tree. If the task was implemented in the repository's main checkout or on the integration branch instead of its own worktree and feature branch, report **cannot verify** with that reason rather than auditing or committing there. Review task changes against the branch-point `Base`, especially when this branch inherits a prior accepted feature; do not attribute inherited commits to the current task. If a path had prior edits and no reliable baseline exists, do not attribute its whole diff to the task; isolate the change or report the limit. Check for missing work and unrequested scope.
2. Follow the requested behavior through the affected entry point, state changes, outputs, and failure paths, reading the unchanged code the change depends on: immediate callers and callees, shared helpers, types and nearby tests. A passing unit test or plausible-looking UI does not establish that the whole flow works. Check the relevant correctness cases: null, empty and error states, boundaries, stale state, races, partial responses, and anything that fails open.
3. Check the change against the project's stated invariants and conventions, and search for every call site and symmetric case of a changed signature, enum, contract or state transition. Do not rely on compilation alone.
4. Test the tests. For each rule the task introduces or protects, confirm a test would fail if the rule were removed: make the smallest breaking edit, run the relevant tests, record which fail, and restore the file. A rule no test notices is a verification gap whatever the pass count says. Record content hashes of the task's files before the first experiment and confirm they match afterwards, so the tree you judge is the tree the implementer left.
5. Rerun the checks needed to substantiate the verdict, sized to the change's real blast radius. Start with the narrowest command that could disprove a suspected problem, then widen to everything the change can affect: a changed shared validator, type, default or transport helper reaches every caller and their tests, not only the tests named after the changed file. Before running a command, know what it does: read-only, local output, external calls, data changes, messages sent, or a deploy. A command called test, verify or dry-run is not thereby harmless. State which checks ran, which did not, and why. Compare claimed counts with observed results when counts matter.
6. For secret exposure, inspect changed content and use established repository scanners when available; a pattern search alone cannot prove a diff is secret-free.
7. Check that documentation and backlog status reflect what was actually verified.
8. Before the verdict, recheck the worktree against what you reviewed. If the content changed during the audit, review the difference or say what the verdict does and does not cover.

## Lenses

Run the lenses in your plan, each from its file, at the planned depth. They are independent of one another; when separate agents are available and a full-depth audit selects several, they may run as parallel read-only reviews that report to you, and you reconcile their findings against the same tree and remove duplicates.

A lens finding must be anchored the same way as any other: the file and line, the triggering scenario, the consequence, and the smallest reasonable direction for correction. Do not report a hypothetical that reading the code or running a deterministic check resolves, and do not list generic best practices.

## Verdict

- **Accepted:** no blocking finding remains and required checks have produced enough evidence for the requested outcome. Complete the accepted-task closure below, then report the evidence, limitations, commit result, and task status. Push or deploy only with authorization for that destination and action.
- **Remediation needed:** leave the implementation in place. Update `.agent-delivery/dispatch/<slug>.md` to Round `<N+1>` with specific findings, affected locations, expected corrections, and checks that will prove them fixed. Remove or supersede the old summary so the next implementer cannot mistake it for the new round. Do not silently widen the task. When the fault is in the dispatch, say so in the round and correct the instruction, so the implementer is not asked to repeat it.
- **Cannot verify:** report the concrete missing prerequisite or access and the portion already audited. Do not mark the task complete.

Classify findings by consequence. **Blocking** means the requested behavior is missing or wrong, a material regression or security/invariant breach exists, a relevant check fails, a rule the task depends on has no test that would notice its removal, or an efficiency/reuse problem creates a concrete material cost. An exploitable exposure of one user's or audience's data to another, an authorization bypass, or a secret in the repository is blocking unless proven unreachable. **Follow-up** means a real but non-blocking improvement that does not undermine acceptance; report it separately without silently expanding the task. **Unverified** means evidence is missing; say what would resolve the uncertainty rather than presenting a suspicion as a defect.

Report a finding only when it is supported by the code or observed behavior and relevant to the task. For each blocking finding, name the affected path, evidence, impact, and a check that would demonstrate a fix. Identify pre-existing problems separately from what the task introduced. Preserve unrelated work and avoid automatic retries without a defined stopping point.

Keep the verdict short, and always include, even when there are no findings:

- the audit plan as run: lenses applied and their depth, lenses skipped and why, and any change from the dispatch's `Audit depth`;
- one line per applied lens saying what was checked and what was found or not found;
- the controls and behaviors you verified as sound, so the owner knows what was covered;
- what could not be verified from here (a real sign-in, deployed configuration, production data, runtime-only behavior) and the smallest next step that would settle it;
- which evidence you observed yourself and which is the implementer's claim. A passing build, a mocked test or a source read does not prove deployed behavior.

## Accepted-task closure

By default, an accepted task receives one detailed local commit before it is marked done. An explicit user instruction or project workflow may opt out of committing for that task. This default does not override a current instruction to leave a repository uncommitted. When opted out, record that choice and mark the accepted task done without a commit.

Identify task-owned paths and hunks against the dispatch baseline. Prepare the existing task source's accepted or done status for inclusion in the task commit. Stage only task-owned changes; inspect the staged diff and check that unrelated staged or untracked work is excluded. Do not use an all-files stage or commit command. If the task cannot be isolated from pre-existing work, or Git cannot commit, report **accepted but closure blocked** with the precise reason. Keep or restore the task's open status where it can be done without disturbing user edits, and do not claim completion.

Write a commit subject naming the task slug and outcome. The body should explain the behavior changed, important implementation choices, verification commands and results, and the audit verdict or known limits. Commit on the recorded feature branch and report its SHA. If a suitable task-only commit already exists for this accepted round, verify its contents and SHA instead of creating a duplicate. Never merge or push as part of this default.
