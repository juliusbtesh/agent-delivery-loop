---
name: delivery-backlog
description: Maintain a repository task backlog and prepare a current, scoped dispatch for implementation. Use when a user asks to view, add, prioritize, or dispatch project work through an agent handoff.
---

# Delivery Backlog

Use the project's existing task source. Read `AGENTS.md` and `AGENT_WORKFLOW.md` when present; the latter may identify the backlog, verification commands, and project invariants. If no workflow file exists, locate the actual backlog before editing it. Do not invent a second source of truth. If the project has no task source and the user asks to add a task, create a simple `BACKLOG.md` after checking for an existing tracker; a view request alone does not create one.

## Invocation

- No arguments: show the live backlog.
- `prompt <slug>`: prepare the named open task for implementation.
- `add <description>` or a clear new-task description: add the task to the backlog; do not dispatch it yet.
- An existing slug, category, or short keyword: show matching tasks. If it is unclear whether the user means a new task or a lookup, clarify before editing.

## View or edit

- For a view request, summarize the live backlog by status and identify actionable task handles. Do not alter task state.
- Add, reprioritize, or change status only when requested. Preserve the backlog's format and existing decisions. Give each dispatchable task a stable, unique slug or issue ID.
- Capture enough context for a later agent to act: desired outcome, scope, prerequisites, reuse opportunities, non-goals, and observable acceptance checks. Flag missing prerequisites without silently filling them in.

## Dispatch

When asked to prepare a task for implementation:

1. Select the requested open task by exact slug or ID before trying a title match. If ambiguous, identify the candidates. Dispatch requires a Git repository with an initial commit; without one, explain that prerequisite and do not invent a branch base or commit the user's setup files without authorization.
2. Read the current task, relevant source and tests, repository instructions, and status documents. Check prerequisites against the current tree and environment. Do not dispatch work whose required prerequisite is missing. Identify the project's integration branch from its workflow file. When the workflow does not name one, default to `development` if that branch exists; only if it does not exist, ask. For an independent task, branch from the integration branch. For a task that depends on unmerged accepted work, branch from that prerequisite feature branch's accepted commit, or from the integration branch if it already contains that commit. Sequence alone is not proof of dependency; resolve ambiguity from the task source or with the user. Do not silently merge or rebase multiple unmerged prerequisites. Check too that everything the task consumes from outside the repository exists in usable form, not only on a branch. When it does not, tell the user before dispatching: the task waits, or, when both sides have agreed the contract, it is built against that contract and the proof against the real thing is recorded as owed.
3. Create or reuse a task-specific feature branch from that exact base. Follow the project's naming convention, or use `feature/<slug>` when none exists. Reuse an existing branch only after verifying it belongs to the same task and has the expected ancestry; never reset another branch to fit. Always give the task its own new worktree for that feature branch (`git worktree add`), next to the main checkout unless the project's workflow names another location. Never switch branches in the main checkout or reuse it as the task tree, even when it is clean: other agents and the user work there. Reuse an existing worktree only when it already belongs to this task. Record pre-existing changes in the main checkout before creating the worktree; they stay there and out of the task tree. Give each agent the target worktree path.
   A new worktree holds only tracked files. Before handing it to an agent, make it able to run the project's checks: install dependencies the way the project does, and copy the untracked local configuration the checks need from the main checkout (for example a registry config or a local environment file). Copy such files only into paths Git ignores, never print their contents, and never add them to a commit. Record what was installed and copied on the dispatch's `Worktree setup` line. If the checks cannot be made to run in the worktree, say so in the dispatch instead of leaving the agent to discover it.
4. Decide how deeply this task should be audited and record it in the dispatch's `Audit depth` section. `delivery-audit` always runs its core steps; name which of its lenses the task warrants (product logic; architecture, reuse and efficiency; security; contract drift), at compact or full depth, and give the reason for each in a phrase. Base it on what the task touches, not on its size: a one-line change to who may do something warrants the security lens, and a large copy edit warrants none. Name the lenses that do not apply as well, so the auditor can tell a decision from an omission. When the task changes something another repository calls or consumes, say which repository and where its working copy is, so the contract can be checked from both sides. Say in the dispatch's `Tests` section what tests the task warrants and why, judged by the rules and boundaries it touches, not its size. The project's own testing rules take precedence, whether stricter or narrower.
5. Write `.agent-delivery/dispatch/<slug>.md` in the chosen worktree with the template below. Keep this directory ignored by Git: when the project's `.gitignore` does not already ignore `.agent-delivery/dispatch/` (a project that never ran `delivery-setup`), add it to the repository's local `.git/info/exclude` instead of editing the project's `.gitignore`. If an older active dispatch lacks branch or worktree fields, establish its actual checkout and baseline before adding them; do not move an in-progress task to a new branch or overwrite its summary blindly.
6. Show the user the task scope, branch, base, worktree, audit depth, and handoff path. Dispatching does not implement, commit, push, or deploy the task.

```md
# Dispatch: <slug> — Round 1
Status: READY FOR IMPLEMENTATION
Integration branch: <project's integration branch>
Parent branch: <integration branch or accepted prerequisite feature branch>
Base: <exact branch-point commit SHA>
Feature branch: <task-specific branch>
Worktree: <absolute path of this task's own worktree; never the main checkout>
Worktree setup: <dependencies installed and ignored local files copied, or "none needed">
Pre-existing changes: <"none" or paths/statuses from git status before dispatch>
Task source: <path and task identifier>

## Outcome
<What must work when done>

## Scope and context
<Relevant files, behavior, and constraints verified in the current tree>

## Prerequisites
<What was checked and its result>

## Reuse and non-goals
<Existing code to build on; boundaries to preserve>

## Verification
<Commands and observable acceptance checks; identify checks needing external access>

## Tests
<What tests this task warrants and why, or "none" with the reason; the project's own testing rules take precedence>

## Audit depth
<For each audit lens: compact, full, or not applicable, with the reason. Name any other repository whose contract this task touches and where to read it>

## Handoff
Implementer writes `.agent-delivery/dispatch/<slug>.summary.md` and leaves the code ready for audit.
```

If the task would edit a path that already has user changes, isolate the task in a worktree or establish an explicit baseline before dispatch. A commit SHA alone cannot identify changes already present in a dirty working tree. The ignored dispatch directory is local to each worktree, so write or copy the handoff into the worktree the agents will use. Use a short, durable task description in the backlog; keep the detailed implementation prompt in the temporary dispatch. If the user requests a different branch or handoff method, follow that choice.
