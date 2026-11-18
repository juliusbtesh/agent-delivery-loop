# Agent Delivery Loop

Seven portable [Agent Skills](https://agentskills.io/specification) for setting up a repository workflow, discovering worthwhile work, and moving a task from backlog to implementation to independent audit. An optional coordinator runs the handoff loop across separate agents.

```
setup → discover → backlog → dispatch → implement → audit → remediation or acceptance

delivery-loop coordinates dispatch → implement → audit → remediation or acceptance,
then, on your go-ahead, integrates accepted work and hands off to promotion

delivery-promote moves integrated work along the branch chain (optional, per project)

backlog → implement → audit → integrate → promote, with a deliberate stop between stages
```

The skills preserve a small handoff protocol. The backlog and repository are the durable sources of truth. Dispatch and implementation summaries are temporary files in `.agent-delivery/dispatch/` so separate agent sessions can coordinate without copying a prompt through chat.

## Skills

| Skill | Job |
| --- | --- |
| [`delivery-setup`](skills/delivery-setup/SKILL.md) | Reconcile an existing project's workflow, or define a fresh project's first tasks, then create its configuration and local skill. |
| [`delivery-discover`](skills/delivery-discover/SKILL.md) | Propose relevant, evidence-backed tasks for the user's selection without changing the backlog. |
| [`delivery-backlog`](skills/delivery-backlog/SKILL.md) | Read the live backlog, add or update a task when requested, and prepare a scoped dispatch. |
| [`delivery-implement`](skills/delivery-implement/SKILL.md) | Implement a dispatch, run the relevant checks, and write an evidence-based handoff. |
| [`delivery-audit`](skills/delivery-audit/SKILL.md) | Review the work as a senior maintainer would: question the dispatch against the project's rules, weigh which deeper reviews the change warrants (product logic; architecture, reuse and efficiency; security; contract drift), prove the tests would catch a regression, then commit accepted work locally by default or write a precise remediation round. |
| [`delivery-loop`](skills/delivery-loop/SKILL.md) | Coordinate separate implementation and audit agents through bounded remediation rounds, then verify accepted-task closure. |
| [`delivery-promote`](skills/delivery-promote/SKILL.md) | Promote integrated work along the project's recorded branch chain, one step at a time, with a drift check and a go-ahead for each step. Applies only where the workflow records a chain. |

These are instruction-based skills: they use the agent's existing repository and shell tools. They do not require a particular model, vendor, language, or issue tracker. An agent must support the Agent Skills `SKILL.md` convention to discover them automatically; otherwise, point it at the relevant file explicitly.

## Familiar commands

In Claude Code, the skill directory name becomes its slash command. After installing the seven skills, use their full names; the three shorter commands are optional personal aliases:

```text
/delivery-setup
/delivery-discover
/delivery-backlog <new task description>
/delivery-backlog prompt <slug>
/delivery-implement <slug>
/delivery-audit <slug>
/delivery-loop <slug>
/delivery-promote
```

Install the seven reusable skills for each local agent, then use `/delivery-setup` to prepare a project's own workflow. The [Claude Code skills documentation](https://code.claude.com/docs/en/skills) confirms that symlinked skill folders are supported and that slash command names come from directory names. To keep this package agent-neutral, the repository holds the reusable skills in `skills/` and no agent-specific discovery folder. The installer creates personal links for supported local agents. Project-specific discovery links belong in each adopting project.

Codex invokes the core skills as `$delivery-setup`, `$delivery-discover`, `$delivery-backlog`, `$delivery-implement`, `$delivery-audit`, and `$delivery-loop`, or through a natural-language request. The slash command spelling is a Claude Code interface; the workflow and handoff files are shared.

## Use in a repository

1. Obtain a local copy of this repository and keep it in place: the personal skill links point to it. From the `agent-delivery-loop` repository root, check the seven links for Codex and Claude Code, then install missing ones:

   ```sh
   python3 scripts/install.py
   python3 scripts/install.py --install
   ```

   Run `python3 scripts/install.py` again to verify all fourteen links. The check exits nonzero for missing or conflicting entries. Installation creates only missing links in `~/.agents/skills/` (Codex) and `~/.claude/skills/` (Claude Code); it never replaces an existing file, directory, or link. On Windows, where creating a symbolic link needs elevated rights or Developer Mode, the installer falls back to a directory junction and reports `INSTALLED (junction)`; the check accepts either. Use `--agent codex` or `--agent claude` to target one agent. Inspect any reported conflict before changing it. The personal Claude commands use their full names, such as `/delivery-backlog` and `/delivery-loop`. For another agent, use that agent's documented skills directory or supply the seven `SKILL.md` paths directly.

   To use the familiar `/backlog`, `/implement`, and `/audit` commands in Claude Code, install optional personal aliases. The installer checks for conflicts and never replaces an existing command:

   ```sh
   python3 scripts/install.py --agent claude --claude-aliases --install
   ```
2. Start a new agent session if its skill inventory is loaded at startup. In Codex, check for the seven `delivery-*` skills; in Claude Code, check for the seven `/delivery-*` commands. The shorter `/backlog`, `/implement`, and `/audit` names require the optional aliases above. If discovery fails, point the agent at the relevant `skills/<name>/SKILL.md` file and check the installation path. Claude Code's personal skills apply to local projects on that machine; Claude cloud sessions do not load files from `~/.claude/skills`.
3. Run `$delivery-setup` (or `/delivery-setup` in Claude Code) in the target folder. In an existing project, it inspects workflow documents, agent rules, skills, commands, and checks; it merges compatible rules and asks you to resolve material conflicts. In an empty folder, it asks what you want to build and turns the first agreed outcomes into specific tasks in `BACKLOG.md`. In either case, it creates or refreshes `AGENT_WORKFLOW.md`, one thin project-local `skills/project-delivery/SKILL.md`, relative links at `.agents/skills/project-delivery` and `.claude/skills/project-delivery`, and the `.agent-delivery/dispatch/` ignore rule. It also checks that both agents can find the seven reusable skills. These relative project links can be committed and work after cloning; personal links to this checkout are machine-specific. The task skills still work without these project files: each dispatch carries scope and checks.
4. Follow the quick start below for individual handoffs or a coordinated loop. Setup and backlog editing can begin in an empty folder; dispatch needs a Git repository with an initial commit for a reliable feature-branch base.

The skills respect repository instructions such as `AGENTS.md` and the user's current request. `AGENT_WORKFLOW.md` is the canonical project configuration; the project-local skill points to it. The project-local skill links serve Codex and Claude Code; other agents need their own documented discovery path or the skill file supplied explicitly. A successful audit authorizes the local task commit by default, but setup alone does not. Pushes, deployments, publication, and access changes remain separate actions.

## Quick start after installation

Run these in the **project you want to work on**, not in this skillset repository. Replace `<slug>` with a task ID from that project's backlog.

| Goal | Codex | Claude Code |
| --- | --- | --- |
| Set up or reconcile the project workflow | `$delivery-setup` | `/delivery-setup` |
| Propose relevant next tasks without adding them | `$delivery-discover` | `/delivery-discover` |
| View the current backlog | `$delivery-backlog` | `/delivery-backlog` |
| Add a task | `$delivery-backlog add <description>` | `/delivery-backlog add <description>` |
| Prepare a task dispatch and feature branch | `$delivery-backlog prompt <slug>` | `/delivery-backlog prompt <slug>` |
| Implement the dispatch | `$delivery-implement <slug>` | `/delivery-implement <slug>` |
| Independently verify and close accepted work | `$delivery-audit <slug>` | `/delivery-audit <slug>` |
| Coordinate dispatch, implementation, and audit | `$delivery-loop <slug>` | `/delivery-loop <slug>` |
| Promote integrated work to the next branch in the chain | `$delivery-promote` | `/delivery-promote` |

The audit is weighed, not uniform. Every audit runs a short set of core steps. The deeper reviews live in separate files under `skills/delivery-audit/references/` and are opened only when the change calls for them, at compact or full depth: the dispatch records the expected depth, and the auditor may raise it when the diff touches more than expected. The verdict states which reviews ran and which were skipped and why.

For manual handoffs, give the implementation and audit steps to separate agents or sessions. `delivery-implement` writes a summary; `delivery-audit` checks the actual work and either requests a bounded remediation round or accepts it. On acceptance, audit marks the task done and makes a detailed **local** commit on its feature branch by default. You can opt out of that commit. Merging and pushing are separate actions.

For an ordered chain, ask: “Use `$delivery-loop` for `<first-slug>`, then `<second-slug>`. The second task depends on the first. Report both when finished.” Say when tasks are independent; order alone does not make the second branch depend on the first. The loop waits for independent audit, starts the next task only after closing the first, and reports the whole chain. You can specify implementation and audit models if the agent launcher supports them. Automated coordination needs an environment that can launch and await separate agents; use the individual skills when it cannot.

If you installed the optional Claude aliases, `/backlog`, `/implement`, and `/audit` work in place of their full `/delivery-*` names. `delivery-discover` only proposes tasks; choose one before adding it to the backlog.

## Handoff files

Every task gets its own feature branch in its own new worktree; the main checkout is never switched or used as the task tree. The integration branch is `development` unless the project's workflow names another. For a task slug `<slug>`, the backlog skill creates that branch and worktree (or reuses the task's existing ones) and writes `.agent-delivery/dispatch/<slug>.md` in the worktree. It records the integration branch, parent branch, exact base commit, feature branch, worktree path, and any pre-existing changes. Independent tasks branch from the integration branch; a task depending on unmerged accepted work branches from its prerequisite feature tip. The implementer writes `.agent-delivery/dispatch/<slug>.summary.md`. A remediation round updates the dispatch and replaces the old summary. Both files stay local and ignored in that worktree; accepted code, tests, and backlog/status updates become the durable record on the feature branch. The backlog skill also prepares the worktree so the project's checks can run there (dependencies installed, ignored local configuration copied) and records that on the dispatch. In a project that never ran setup, the handoff folder is hidden through the repository's local `.git/info/exclude`. Accepted work stays on its feature branch until you give the go-ahead to integrate. The loop then merges the accepted branches into the integration branch in dependency order by the project's method, runs the project's checks on the merged result, removes each merged task's worktree and local branch, and, where the project has a promotion chain, reports what is integrated but not yet promoted. It never promotes on its own.

## Origin

This workflow is adapted from the backlog, implement, and audit commands used to develop Pulse and Pulse Trade. The public version removes product-specific file paths, model names, deployment assumptions, and security controls so each adopting project can state its own requirements.

## License

MIT. See [LICENSE](LICENSE).
