# Bundle dec95f7c7fc8

Checked at commit `a321cc7ed2cd` (2026-08-22T00:19:33Z), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `sample-knowledge/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 8 |
| OKF v0.2 conformance (§11, items 1–2) | not yet: 8 file(s) to change |
| Timestamps follow | no timestamp fields |
| Trust and lifecycle fields used | none |
| Trust tiers (§5.3) | n/a |
| JidoSeal checker | score 0, tier none |

## What to change

### Files whose frontmatter does not parse (8)

The block between the `---` lines must be valid YAML that reads as a mapping. The parser's first message is shown for each file.

- `account-plans/northstar-plan.md: frontmatter is not valid YAML: mapping values are not allowed here`
- `clients/northstar-client.md: frontmatter is not valid YAML: mapping values are not allowed here`
- `commitments/northstar-commitment.md: frontmatter is not valid YAML: mapping values are not allowed here`
- `contacts/northstar-contact.md: frontmatter is not valid YAML: mapping values are not allowed here`
- `deliverables/northstar-deliverable.md: frontmatter is not valid YAML: mapping values are not allowed here`
- `issues/northstar-issue.md: frontmatter is not valid YAML: mapping values are not allowed here`
- `renewal-dates/northstar-renewal.md: frontmatter is not valid YAML: mapping values are not allowed here`
- `stakeholders/northstar-stakeholder.md: frontmatter is not valid YAML: mapping values are not allowed here`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
