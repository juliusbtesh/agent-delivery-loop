# Lens: security

An attacker's-view review, separate from correctness: what could a curious or hostile caller reach, read or change that the product rules say they must not? Trace it in code. Passing tests and working controls do not establish that an access rule is enforced everywhere.

Stay read-only. Never print, copy or commit secrets. Do not exercise live systems with real credentials, change server data or attempt exploitation unless the user explicitly asks for that.

## Depth

Choose the depth for the change and say which ran. Running the full pass on a change that does not warrant it is a cost with no benefit; running the baseline on a change that needs the full pass is a miss.

- **Baseline** (the change touches a trust boundary or handles sensitive data, but adds no new surface): for each boundary touched, check authentication; authorization on every entry point, including the symmetric entry points the change did not touch; object-level access (can a caller reach another user's or tenant's record by supplying an id); what is returned and what is logged; and what fails open or closed on error. Where the change handles sensitive data, follow that data from where it is read to everywhere it goes: who can now see it that could not before, whether it reaches a log, an error message, an analytics or third-party call, a cache, an export or a test fixture, whether it is stored and for how long, and whether the least data needed is what is fetched and returned.
- **Full** (a whole feature, or any change that adds an endpoint, a token, a data flow, an embedded surface or a model integration): run the workstreams below that apply, over the entire feature and not only the latest diff. Skip a workstream that has nothing to examine, and say that it was skipped.

## Workstreams for the full pass

1. **Access control and tokens.** Every endpoint and server route: who can call it, which policy or guard applies, and whether the same rule holds on every sibling route and at both the issue and the use of a token. Object-level access and id guessing. Role and permission gates, per-user blocks and kill switches, their bypass paths, their fail-open behaviour and the window between a change and its effect. Session and token design: signing, scope and type enforcement, lifetime, refresh, replay, revocation, claims that leak. Rate, usage and cost limits, including how the client key is derived and whether it can be spoofed. Anonymous or public surfaces: origin handling, input limits, abuse paths.
2. **Data exposure and visibility.** Every path by which restricted data could reach another audience: responses, lists and pickers, review and admin screens, search results, error messages, events, stored transcripts and logs. Apply the repository's visibility rules at the source of each read, not only in the interface. What is sent to third parties, what is stored and whether it is protected at rest, retention and deletion, who can read it and whether that is audited, and whether real personal data is committed in fixtures, documents or reports.
3. **Browser and embedded surface.** Messaging between windows in both directions (origin and source checks, allow-list matching bugs, target origin, which messages trigger actions or carry secrets), framing controls, tokens in URLs and storage, rendering of untrusted text (raw HTML, link and image schemes, markdown pipelines), navigation and redirect validation, debug or development routes left reachable, public configuration that must not hold secrets, and new or changed dependencies and install scripts.
4. **Model and service-to-service risk.** Injection from documents, notes, names and search results that reach a model as data: what stops them steering tools to other records, revealing instructions or exfiltrating data through links. Whether tools always run as the signed-in user with a per-call access check, argument validation and size and time limits. How services authenticate to each other and how the receiver validates issuer, audience and scope; token lifetimes and over-broad roles; any unauthenticated route. Server-side fetches of URLs a user or admin can influence (allow-list bypasses, redirects, lookalike hosts, internal addresses), file parsing limits, editable content that becomes prompt text, cost and availability abuse, and secrets in code, configuration, documents, fixtures, reports or logs.

## Rules

- Ground every finding in code with file and line: the attacker, the input, the result and the impact.
- Check the symmetric cases: the same rule on every sibling endpoint, the old and new version of a contract, and the paths a deletion or rename leaves behind.
- When the repository forbids exposing an identity or internal text to an audience, treat a leak as blocking and look beyond the obvious field: aliases and short names, structured values, dynamic data, old and new serialization, and alternate response paths. Require a fix at the source and a behaviour test, not hiding in the interface.
- Record the controls you verified as sound, and state what could not be verified: production settings and data, deployed versions, behaviour visible only at runtime.
