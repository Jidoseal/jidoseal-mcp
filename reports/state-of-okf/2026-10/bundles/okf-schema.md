# okf-schema (gsemet)

Repository: <https://github.com/gsemet/okf-schema>
Checked at commit `4732e941a1ef` (2026-10-19T22:16:10+02:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `examples/ai-llm-knowledge-base/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.1 |
| Concept files | 10 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | has values neither text allows |
| Trust and lifecycle fields used | `generated` (10) |
| Trust tiers (§5.3) | unverified 10 |
| JidoSeal checker | score 67, tier silver |

## What to change

### Timestamp values neither v0.2 text allows (10)

`generated.at` and `verified[].at` are datetimes in both texts (`2026-06-30T14:00:00Z`); `stale_after`, `sources[].last_modified` and `usage_window` are bare dates in the 2026-08-15 text and datetimes with an offset in the 2026-08-21 text. Placeholders such as `YYYY-MM-DD` left in a template are counted here too.

- `concepts/function-calling.md: generated.at = '2026-06-29'`
- `concepts/rag.md: generated.at = '2026-06-29'`
- `concepts/react-pattern.md: generated.at = '2026-06-29'`
- `papers/attention-is-all-you-need.md: generated.at = '2026-06-29'`
- `papers/chain-of-thought-paper.md: generated.at = '2026-06-29'`
- `papers/toolformer.md: generated.at = '2026-06-29'`
- `some/concept.md: generated.at = '2026-06-29'`
- `tools/langchain.md: generated.at = '2026-06-29'`
- `tools/ollama.md: generated.at = '2026-06-29'`
- `tools/pytest.md: generated.at = '2026-06-29'`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
