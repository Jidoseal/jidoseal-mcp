# ai-contribution-policies (jrjsmrtn)

Repository: <https://github.com/jrjsmrtn/ai-contribution-policies>
Checked at commit `e397de49fa87` (2026-10-09T23:53:22+02:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `knowledge/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 61 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | 2026-08-15 text |
| Trust and lifecycle fields used | `sources` (61), `generated` (61), `verified` (61), `status` (61), `stale_after` (61) |
| Trust tiers (§5.3) | machine-confirmed 61 |
| JidoSeal checker | score 67, tier silver |

## What to change

### Values that follow the 2026-08-15 text (61)

These are valid under the text of 2026-08-15. To follow the current text (2026-08-21), write each as a datetime with a UTC offset, for example `2026-12-31` becomes `2026-12-31T00:00:00Z`. Both texts call themselves `okf_version: "0.2"`.

- `overview.md: stale_after = '2026-11-05'`
- `distributions/ctan.md: stale_after = '2026-11-10'`
- `distributions/debian.md: stale_after = '2027-02-28'`
- `distributions/fedora.md: stale_after = '2027-03-14'`
- `distributions/freebsd.md: stale_after = '2027-02-04'`
- `distributions/gentoo.md: stale_after = '2027-02-04'`
- `distributions/netbsd.md: stale_after = '2027-02-04'`
- `distributions/tex-live.md: stale_after = '2027-02-10'`
- `foundations/apache-software-foundation.md: stale_after = '2027-02-04'`
- `foundations/linux-foundation.md: stale_after = '2027-02-04'`
- `foundations/openinfra.md: stale_after = '2027-02-04'`
- `foundations/owasp.md: stale_after = '2027-03-07'`
- `mechanisms/agent-file-pointers.md: stale_after = '2027-03-08'`
- `mechanisms/assisted-by-trailer.md: stale_after = '2027-03-08'`
- `mechanisms/certifying-origin.md: stale_after = '2027-03-10'`
- … and 46 more

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
