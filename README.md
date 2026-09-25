<!-- mcp-name: com.jidoseal/jidoseal-mcp -->
# jidoseal-mcp

[![Listed on mcpservers.org](https://mcpservers.org/badge.svg)](https://mcpservers.org/servers/jidoseal/jidoseal-mcp)

**Check a folder of markdown notes against Open Knowledge Format (OKF) v0.2 — from inside Claude Code, Claude Desktop, Cursor, GitHub Copilot, OpenAI Codex, Gemini CLI, Zed, Cline, Continue, JetBrains AI Assistant or a local model, on your own machine.**

Pick a folder, scan it. `jidoseal-mcp` is a local [Model Context Protocol](https://modelcontextprotocol.io) server that reads the YAML frontmatter of every `*.md` file under a folder, reports which **tier** the knowledge base reaches (Bronze / Silver / Gold), and lists — per file — the exact frontmatter fields missing for the next tier. Nothing leaves your machine: no file, no file name, no file content.

```bash
pip install jidoseal-mcp
claude mcp add jidoseal -- jidoseal-mcp     # Claude Code; every other tool is below
```

Then ask your assistant: *"Scan ~/notes with JidoSeal and tell me what's missing for Silver."*

> **Independent.** OKF is an open specification from Google Cloud. JidoSeal is not affiliated with, sponsored by, or endorsed by Google or ISO. ISO names no fields: the Silver and Gold fields below are JidoSeal's way of evidencing the ISO clauses, and a JidoSeal certificate is not an ISO certification.

---

## What it checks

The scan is deterministic — presence of populated frontmatter fields, no model calls, no scoring by opinion. A field counts only if it has real content (`title:` with nothing after it earns nothing).

| Tier | A file must have (populated) | What it evidences |
|---|---|---|
| **Bronze** | `type` | OKF v0.2 as written — `type` is its one required field |
| **Silver** | Bronze + `title`, `description`, `timestamp`, `owner` | ISO 9001 §7.5.2, which asks for appropriate identification and description of a document and gives examples ("a title, date, author, or reference number"). These four fields are one reasonable way to evidence it. |
| **Gold** | Silver + `status`, `review_policy`, `reviewed_at`, `next_review_at` | ISO 30401's kept-current knowledge governance. The standard sets no review interval; a stated review policy with real review dates is how you evidence it, and the cadence is yours to choose. |

A corpus's tier is the tier of its **weakest file**. Coverage is the share of files that reach each tier. The full field reference — accepted aliases, what counts as "populated", what is excluded — is in [docs/tiers.md](docs/tiers.md).

A minimal Gold-tier file:

```markdown
---
type: policy
title: Leave policy
description: How leave accrues and how to request it.
timestamp: 2026-09-01
owner: dept:people-ops
status: stable
review_policy: yearly
reviewed_at: 2026-09-01
next_review_at: 2027-09-01
---
```

Worked examples for each tier, and a mixed folder, are in [`examples/tiers/`](examples/tiers/).

## Tools

| Tool | What it does | Network |
|---|---|---|
| `jidoseal_scan` | The free Self-Check over a folder on this machine: corpus tier, per-file missing fields for the next tier (each marked `AUTO` — a value JidoSeal can propose — or `NEEDS-CLIENT` — only the owner can answer), coverage per tier, a 0–100 score, and a Merkle root of the corpus. | none |
| `jidoseal_certification_offer` | What optional certification would cost for this corpus, why, what it includes, and exactly which facts a purchase would send. Computes locally; starts nothing. | none |
| `jidoseal_start_checkout` | Only on your explicit go-ahead: asks jidoseal.com to create a Stripe Checkout session and returns the link for you to open. Takes no payment. | jidoseal.com only |

Example `jidoseal_scan` result for [`examples/tiers/mixed`](examples/tiers/mixed) (three files, one Gold, one Bronze, one with no frontmatter):

```jsonc
{
  "corpus": { "file_count": 3, "tier": "none",
              "coverage": { "bronze": 66.7, "silver": 33.3, "gold": 33.3 } },
  "score": 44,
  "certified_eligible": false,
  "files": [
    { "name": "expenses.md", "tier": "bronze",
      "missing": { "silver": [ { "field": "description", "fix": "AUTO" },
                               { "field": "timestamp",   "fix": "AUTO" },
                               { "field": "owner",       "fix": "NEEDS-CLIENT" } ] } }
    // …
  ]
}
```

`frontmatter_ok: false` on a file means its frontmatter block exists but does not parse; no field write can close its gaps until it is fixed by hand.

## Install and wire it into your tool

Requires Python 3.9+. `pip install jidoseal-mcp` also installs [`jidoseal`](https://pypi.org/project/jidoseal/) (the scan engine and CLI) and puts a `jidoseal-mcp` command on your PATH. No account and no API key. The scan itself needs no network — it runs the same offline.

Every tool below launches the same local command, `jidoseal-mcp`, over stdio. Only the place you write it down differs.

<details open><summary><b>Claude Code</b></summary>

```bash
claude mcp add jidoseal -- jidoseal-mcp
```
or commit a project-scoped `.mcp.json`:
```json
{ "mcpServers": { "jidoseal": { "command": "jidoseal-mcp" } } }
```
</details>

<details><summary><b>Claude Desktop</b></summary>

Settings → Developer → Edit Config opens `claude_desktop_config.json`. Add:
```json
{ "mcpServers": { "jidoseal": { "command": "jidoseal-mcp", "args": [] } } }
```
Restart Claude Desktop afterwards.
</details>

<details><summary><b>Cursor</b></summary>

`~/.cursor/mcp.json` (or `.cursor/mcp.json` in a project):
```json
{ "mcpServers": { "jidoseal": { "type": "stdio", "command": "jidoseal-mcp", "args": [] } } }
```
</details>

<details><summary><b>GitHub Copilot (VS Code agent mode, and Visual Studio, JetBrains, Eclipse, Xcode)</b></summary>

Copilot Chat uses MCP tools in **Agent** mode. In VS Code, add `.vscode/mcp.json` to the project (or run **MCP: Open User Configuration** for every project):
```json
{ "servers": { "jidoseal": { "type": "stdio", "command": "jidoseal-mcp" } } }
```
Copilot in Visual Studio, JetBrains IDEs, Eclipse and Xcode takes the same `servers` entry in its own MCP settings. On a Copilot Business or Enterprise seat, your organization must have the "MCP servers in Copilot" policy turned on; it is off by default.
</details>

<details><summary><b>OpenAI Codex (CLI, IDE extension and app)</b></summary>

```bash
codex mcp add jidoseal -- jidoseal-mcp
```
or in `~/.codex/config.toml`:
```toml
[mcp_servers.jidoseal]
command = "jidoseal-mcp"
```
</details>

<details><summary><b>Gemini CLI</b></summary>

```bash
gemini mcp add -s user jidoseal jidoseal-mcp
```
or in `~/.gemini/settings.json` (or `.gemini/settings.json` in a project):
```json
{ "mcpServers": { "jidoseal": { "command": "jidoseal-mcp" } } }
```
</details>

<details><summary><b>Zed</b></summary>

In Zed's `settings.json` (or Settings → AI → MCP Servers → Add Local Server):
```json
{ "context_servers": { "jidoseal": { "command": "jidoseal-mcp", "args": [], "env": {} } } }
```
</details>

<details><summary><b>Cline</b></summary>

MCP Servers → Configure → Configure MCP Servers, then add:
```json
{ "mcpServers": { "jidoseal": { "type": "stdio", "command": "jidoseal-mcp", "args": [], "disabled": false } } }
```
</details>

<details><summary><b>Continue</b></summary>

`.continue/mcpServers/jidoseal.yaml` in your workspace (MCP tools run in Continue's agent mode):
```yaml
name: JidoSeal
version: 0.0.1
schema: v1
mcpServers:
  - name: jidoseal
    type: stdio
    command: jidoseal-mcp
```
</details>

<details><summary><b>JetBrains AI Assistant</b></summary>

Settings → Tools → AI Assistant → Model Context Protocol (MCP) → Add → STDIO, and paste:
```json
{ "mcpServers": { "jidoseal": { "command": "jidoseal-mcp", "args": [] } } }
```
</details>

<details><summary><b>A local model</b></summary>

Any MCP client that can launch a stdio server and sits in front of a local model takes the same two facts — a name and a command:
```json
{ "mcpServers": { "jidoseal": { "command": "jidoseal-mcp", "args": [], "env": {} } } }
```
</details>

<details><summary><b>No AI tool at all — just the command line</b></summary>

```bash
pipx install jidoseal && jidoseal --root ~/notes
```
Same scan, same verdict, from a terminal. See the [`jidoseal` CLI on PyPI](https://pypi.org/project/jidoseal/).
</details>

If your host uses a different Python than the one you installed into, point it at the module: `"command": "/path/to/python", "args": ["-m", "jidoseal_mcp"]`.

Check the wiring by hand, without any host:

```bash
printf '%s\n' \
 '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"x","version":"0"}}}' \
 '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
 | jidoseal-mcp
```
You should see an `initialize` result naming `jidoseal`, then the three tools.

## Run it in CI

The CLI writes `.jidoseal/manifest.json`; a few lines turn it into a gate. See [docs/ci.md](docs/ci.md) for a GitHub Actions workflow that fails the build when any file falls below Silver.

## What leaves your machine

**A scan: nothing.** Not the files, not their names, not their contents. That is a property of the import graph, not a promise about which branches run: `jidoseal_mcp.py`, `scan_result.py` and `offer.py` import no socket, no `urllib`, no HTTP client, and neither does anything they pull in. `checkout_client.py` is the one module that can reach the network, and it is imported only inside the checkout handler.

**A purchase**, only if you choose one: the company, name and email you typed, the tier, a 0–100 score, the corpus's Merkle root, the local scan's id, and which Bronze price applies. No file contents, no file names, no per-file hashes, no paths. The Merkle root is a one-way digest.

Verify it yourself:

```bash
strace -f -o /tmp/trace.txt -e trace=network jidoseal-mcp < your-jsonrpc-input   # no network syscalls during a scan
bwrap --unshare-net --dev-bind / / jidoseal-mcp < your-jsonrpc-input             # the scan works with no network at all
```

The scan writes its own records — `manifest.json` and an appended `progress.ndjson` — under `<folder>/.jidoseal/` and nowhere else. It never modifies your notes.

## Optional certification

Scanning is free and unlimited, and so are the fixes. If you want a dated certificate for the grade your folder reached, bound to the Merkle root of your corpus, with a public verification page and a listing in the public registry, that is a paid step on [jidoseal.com](https://jidoseal.com); current prices are published there, one flat price per grade however many files. A person at JidoSeal signs it off from the grade, the score and that fingerprint only, never from your file contents.

## Links

- Website: <https://jidoseal.com>
- Public registry of certified knowledge bases: <https://jidoseal.com/registry>
- PyPI: [`jidoseal-mcp`](https://pypi.org/project/jidoseal-mcp/) · [`jidoseal`](https://pypi.org/project/jidoseal/)
- MCP Registry: `com.jidoseal/jidoseal-mcp`
- OKF specification (Google Cloud, Apache-2.0): <https://github.com/GoogleCloudPlatform/open-knowledge-format>
- Contact: support@jidoseal.com

## About this repository

This repository holds the source of the `jidoseal-mcp` package: an MCP server implemented on the Python standard library alone (no MCP SDK), speaking JSON-RPC 2.0 over stdio. It depends on the separately published [`jidoseal`](https://pypi.org/project/jidoseal/) package for the scan engine, which is **not** part of this repository. Issues are welcome; there is no test suite in this repository, so please include the `jidoseal-mcp` and `jidoseal` versions and the smallest folder that reproduces a problem.

## License

Apache-2.0 for the code in this repository — see [LICENSE](LICENSE). The `jidoseal` engine it depends on is distributed separately under its own terms.
