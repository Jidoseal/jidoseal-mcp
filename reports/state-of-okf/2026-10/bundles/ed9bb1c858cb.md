# Bundle ed9bb1c858cb

Checked at commit `9d21aa0caceb` (2026-06-21T16:49:46+02:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `(repository root)/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.1 |
| Concept files | 5677 |
| OKF v0.2 conformance (§11, items 1–2) | not yet: 557 file(s) to change |
| Timestamps follow | no timestamp fields |
| Trust and lifecycle fields used | none |
| Trust tiers (§5.3) | unverified 5676 |
| JidoSeal checker | score 30, tier none |

5120 file(s) use the v0.1 `timestamp` key, which v0.2 supersedes with `generated: {by, at}` (§13.1); consumers may still fall back to it.

## What to change

### Files with no frontmatter block (1)

OKF v0.2 §11 asks every `.md` file other than `index.md` and `log.md` to start with a YAML frontmatter block holding a non-empty `type`. The smallest change is:

```yaml
---
type: Note
---
```

If these files are not meant to be part of the bundle (a README, a changelog), moving the bundle into its own folder keeps them out.

- `README.md`

### Files with frontmatter but no `type` (556)

`type` is the one key OKF v0.2 always requires (§4.1). Any short descriptive string works, for example `type: Reference`.

- `references/10-minute-demo-collect-human-feedback-databricks-on-aws-3f033604.md`
- `references/10-minute-demo-evaluate-a-genai-app-databricks-on-aws-c90f1438.md`
- `references/abac-grant-policies-for-models-beta-databricks-on-aws-49466796.md`
- `references/access-control-in-unity-catalog-databricks-on-aws-817d7ad8.md`
- `references/access-control-legacy-databricks-on-aws-0be88992.md`
- `references/access-data-shared-with-you-using-opensharing-for-recipients-databricks-on-aws-7bb360b8.md`
- `references/access-trace-data-databricks-on-aws-0c458734.md`
- `references/adapt-single-node-pytorch-to-distributed-deep-learning-databricks-on-aws-7a436585.md`
- `references/add-an-instance-profile-to-a-model-serving-endpoint-databricks-on-aws-6124b720.md`
- `references/add-an-mlflow-experiment-resource-to-a-databricks-app-databricks-on-aws-2dc6c6e2.md`
- `references/add-context-to-traces-databricks-on-aws-1d18f107.md`
- `references/add-traces-to-applications-automatic-and-manual-tracing-databricks-on-aws-91d388aa.md`
- `references/admin-privileges-in-unity-catalog-databricks-on-aws-a7ab7fd7.md`
- `references/advanced-usage-of-databricks-connect-databricks-on-aws-e72df911.md`
- `references/ai-governance-databricks-on-aws-e6fd4910.md`
- … and 541 more

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
