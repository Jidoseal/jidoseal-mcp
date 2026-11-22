# JidoSeal OKF check (Claude Code plugin)

A free skill plus the local `jidoseal-mcp` server. Pick a folder of Markdown docs, scan it, and the assistant fills in the missing frontmatter fields the scan lists (asking you for the ones only you can answer, such as `owner`), then rescans to confirm the tier. The scan runs on your machine and writes only `<folder>/.jidoseal/`; see the [main README](../../README.md#side-effects-and-data-in-brief) for what it reads, writes and sends.

```
/plugin marketplace add Jidoseal/jidoseal-mcp
/plugin install jidoseal@jidoseal
```

Then ask: "Use the okf-check skill on ~/notes and get it to Bronze."

- Needs [`uv`](https://docs.astral.sh/uv/) (the plugin starts the server with `uvx jidoseal-mcp`). Without uv: `pip install jidoseal-mcp`, and change the command in `.mcp.json` to `jidoseal-mcp`.
- The same skill works in other tools that read Agent Skills or MCP; see the [main README](../../README.md) for Copilot, Cursor, Codex, Gemini CLI, Zed, Cline, Continue, JetBrains and local models.
- The scan is free and local. The server also offers certificates through `jidoseal_certification_offer`: OKF Certified is free, and Bronze, Silver and Gold are paid. The skill mentions it once, after a scan, and only starts a request or a purchase if you explicitly ask (the server requires `confirm: true` for both calls).

Open Knowledge Format (OKF) v0.2 is an open specification in Google's GoogleCloudPlatform/open-knowledge-format repository, under the Apache-2.0 licence. JidoSeal checks a folder against the three conformance rules in OKF §11 and reports the result. Bronze and Silver add document fields. Gold adds AI-provenance fields. A JidoSeal certificate is not an ISO certification. JidoSeal is independent of Google and of ISO, and is not affiliated with, sponsored by, or endorsed by either.

Apache-2.0.
