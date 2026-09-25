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
2. Read the current task, relevant source and tests, repository instructions, and status documents. Check prerequisites against the current tree and environment. Do not dispatch work whose required prerequisite is missing. Identify the project's integration branch from its workflow or Git configuration; ask if multiple plausible branches remain. For an independent task, branch from the integration branch. For a task that depends on unmerged accepted work, branch from that prerequisite feature branch's accepted commit, or from the integration branch if it already contains that commit. Sequence alone is not proof of dependency; resolve ambiguity from the task source or with the user. Do not silently merge or rebase multiple unmerged prerequisites.
3. Create or reuse a task-specific feature branch from that exact base. Follow the project's naming convention, or use `feature/<slug>` when none exists. Reuse an existing branch only after verifying it belongs to the same task and has the expected ancestry; never reset another branch to fit. Use a separate worktree when another agent occupies the checkout, the checkout has unrelated changes, or the branch is already checked out elsewhere. Otherwise a clean checkout may switch branches. Record pre-existing changes before branch or worktree creation; keep them out of the task tree. Give each agent the target worktree path.
4. Write `.agent-delivery/dispatch/<slug>.md` in the chosen worktree with the template below. Keep this directory ignored by Git. If an older active dispatch lacks branch or worktree fields, establish its actual checkout and baseline before adding them; do not move an in-progress task to a new branch or overwrite its summary blindly.
5. Show the user the task scope, branch, base, worktree, and handoff path. Dispatching does not implement, commit, push, or deploy the task.

```md
# Dispatch: <slug> — Round 1
Status: READY FOR IMPLEMENTATION
Integration branch: <project's integration branch>
Parent branch: <integration branch or accepted prerequisite feature branch>
Base: <exact branch-point commit SHA>
Feature branch: <task-specific branch>
Worktree: <absolute checkout path containing this dispatch>
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

## Handoff
Implementer writes `.agent-delivery/dispatch/<slug>.summary.md` and leaves the code ready for audit.
```

If the task would edit a path that already has user changes, isolate the task in a worktree or establish an explicit baseline before dispatch. A commit SHA alone cannot identify changes already present in a dirty working tree. The ignored dispatch directory is local to each worktree, so write or copy the handoff into the worktree the agents will use. Use a short, durable task description in the backlog; keep the detailed implementation prompt in the temporary dispatch. If the user requests a different branch or handoff method, follow that choice.
