---
name: delivery-promote
description: Report where a project's branches stand along its recorded promotion chain, and promote already-integrated work one step at a time (for example development to staging to production). Use when the user asks what is or is not released, or asks to promote, release, or move a branch forward, and the project's workflow records a promotion chain; not for implementing or merging individual tasks.
---

# Delivery Promote

Move work that is already on one branch of the project's promotion chain onto the next branch in that chain, or report where the chain stands. This skill does not implement, audit, or merge task branches; `delivery-loop` and the task skills end at the integration branch, and promotion starts there.

## When it applies

Read `AGENTS.md` and `AGENT_WORKFLOW.md`. The workflow must record a promotion chain: an ordered list of branches starting at the integration branch. If it records none, or the project has a single long-lived branch, say that promotion does not apply here and stop; offer `delivery-setup` to record a chain if the user wants one. Do not infer a chain from branch names.

A chain is whatever the project records, of any length and with any branch names: two branches (integration and production, or integration and a staging branch that is the end of the line), the common three, or several intermediate stages before production. Nothing here assumes three stages or the names `development`, `staging` and `production`. Work the chain exactly as written: every recorded branch is a step, in order, and a stage the project does not have is not a step.

How much of this skill applies is the project's decision, recorded in its workflow, and it differs between projects:

- which steps of the chain an agent may carry out, and which the owner or a release pipeline always does;
- how a step is made: a pull request, or a merge and push;
- what must be true first: required checks, approvals, release notes, a version bump, a deploy window;
- whether other repositories must be released before or after this one.

Follow what is recorded; it takes precedence over the defaults below. Where the workflow says a step belongs to the owner or a pipeline, do not perform it: prepare and report only. Where it is silent on a point, use the default here and say that you did.

## Report the chain (no changes)

Asked what is released, or whether everything is in production, answer without changing anything. Fetch, then for each neighbouring pair of branches in the chain report: what the earlier branch has that the later one lacks, what the later branch has that the earlier one lacks, and whether the required checks passed on each tip. Say plainly which work is integrated but not yet promoted and how far each piece has travelled. Identify work by content as well as by commit, since a change copied between branches as a new commit is present even though its commit id is not. This report is the safe default when the request is ambiguous.

## Before each step

Promote one step at a time, from a branch to the branch immediately after it. Never skip a branch. For the step from `source` to `target`:

1. Fetch, then compare the two branches. List what `source` has that `target` lacks: this is what the step will promote. If it is empty, report that there is nothing to promote and stop.
2. Check that `target` has nothing `source` lacks. A commit that exists only on `target` (a hotfix, a direct commit, a change copied by hand) means the chain has drifted. Stop and show those commits; the user decides whether to bring them back to `source` first. Compare by content as well as by commit, and say which of the differing commits are already present under another id and which are truly missing.
3. Check that the project's required checks have passed on the exact `source` commit being promoted, using the project's CI where it exists and its recorded verification commands otherwise. A failing or missing required check stops the step.
4. Check release order. When the workflow records that another repository must be released first, or the work being promoted calls or consumes something in another repository that changed alongside it, confirm the other side is already at or beyond `target`'s stage. A consumer promoted ahead of the provider it depends on reaches users who then meet errors; a provider change that removes something must wait until no released consumer uses it. If the order is not satisfied, stop and name what has to be promoted first and where.
5. Show the user the step: source and target, the commits and a short summary of what they change, the check results, the release-order result, any open tasks recording verification still owed on the work being promoted, and how the project promotes. Ask for a go-ahead for this step. Approval for one step is not approval for the next.

## Promote

Use the method the workflow records. When it records none, open a pull request from `source` into `target` where the host supports it, and otherwise merge with a merge commit; do not squash or rebase a promotion, because the next comparison depends on shared history. Do the work in a new worktree for `target`, never in the main checkout. Never force-push. Push or merge only after the user's go-ahead for this step and this destination.

After the step, verify it: `target` contains every commit of `source`, the project's post-merge checks or deployment for `target` succeeded where the project has them, and nothing unexpected changed. Report what was promoted, the resulting commit, the checks, and anything not verified, such as behavior that only a signed-in person can confirm. Remove the worktree created for the step.

To continue along the chain, start again at "Before each step" for the next pair of branches, with a fresh comparison and a fresh go-ahead.

## Hotfixes

When the user needs a fix on a later branch immediately, they may commit it there directly; that is their call, not this skill's. Afterwards the fix must also reach every earlier branch in the chain, or the next promotion will either stop on drift or silently undo it. When asked to reconcile, bring the fix back toward the integration branch one step at a time, with the same comparison and go-ahead as a promotion.
