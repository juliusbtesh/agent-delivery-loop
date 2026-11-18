# Lens: product logic

Does the change deliver the intended product outcome across the whole affected workflow? Individually correct functions, passing tests and working controls do not establish that the product logic is complete. Do not treat the implementation as proof of the intended rule.

## Depth

- **Compact** (a small change to an existing rule): state the rule, check the one journey it affects and its obvious alternate, and stop. Omit scenarios that do not apply rather than manufacturing a checklist.
- **Full** (a new feature or a changed workflow): map each confirmed acceptance criterion to its entry points, its persistence and downstream effects, and the evidence that verifies it. Mark each criterion covered, gap found, or unverified. Do not create criteria from preference.

## What to check

- Establish the intended actor, the business rule, its prerequisites and the successful end state from the requirements, current product behaviour and authoritative documents.
- Trace the complete journey: entry point, defaults or imported and saved state, user choices, validation, submission, persistence, downstream consumers, and reopening or later actions. Follow relevant unchanged code beyond the diff to find missing connections.
- Check the meaningful combinations of role, scope, lifecycle stage and mode. Look for users who cannot complete an action they are allowed, actions offered that cannot succeed, and rules applied to the wrong entity or to only some entry points.
- For a configurable rule, trace the configuration to the code that actually consumes and enforces it. Check that defaults, existing selections, templates, imports, retries and context changes still honour it; disabling a control does not settle what happens to a value already selected.
- Check transitions and recovery. A change to an upstream input must reconcile dependent values, eligibility, summaries and saved state. Look for contradictory statuses, stranded workflows, missing next steps, and success messages shown before the promised outcome.
- Consider data that already exists, alternate roles, retries, duplicates, out-of-order events and partial failures where they are relevant.
- Challenge the rule with concrete scenarios: a normal success path and the relevant alternate or disallowed paths. Check whether the tests assert the business outcome; a mocked endpoint or an isolated helper can pass while the consumer workflow is broken.

## Reporting

Raise an evidence-backed omission or contradiction as a finding even when the code compiles and follows local conventions. State the expected rule, the triggering scenario, the actual behaviour and the consequence for the user or business. Report an unresolved product decision as an open question, not as a defect. Keep findings tied to behaviour the task introduced, changed or left incomplete.
