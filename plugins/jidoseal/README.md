# JidoSeal OKF check (Claude Code plugin)

A free skill plus the local `jidoseal-mcp` server. Pick a folder of Markdown docs, scan it, and the assistant fills in the missing frontmatter fields the scan lists (asking you for the ones only you can answer, such as `owner`), then rescans to confirm the tier. Nothing leaves your machine.

```
/plugin marketplace add Jidoseal/jidoseal-mcp
/plugin install jidoseal@jidoseal
```

Then ask: "Use the okf-check skill on ~/notes and get it to Silver."

- Needs [`uv`](https://docs.astral.sh/uv/) (the plugin starts the server with `uvx jidoseal-mcp`). Without uv: `pip install jidoseal-mcp`, and change the command in `.mcp.json` to `jidoseal-mcp`.
- The same skill works in other tools that read Agent Skills or MCP; see the [main README](../../README.md) for Copilot, Cursor, Codex, Gemini CLI, Zed, Cline, Continue, JetBrains and local models.
- The scan is free and local. The server also offers an optional paid certificate through `jidoseal_certification_offer`; the skill mentions it once, after a scan, and only starts a purchase if you explicitly ask.

OKF is an open specification published by Google Cloud under Apache-2.0. JidoSeal is independent and is not affiliated with, sponsored by or endorsed by Google or ISO. A JidoSeal grade is evidence you can show; it isn't ISO certification.

Apache-2.0.
