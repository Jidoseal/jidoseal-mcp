<!-- mcp-name: com.jidoseal/jidoseal-mcp -->
# jidoseal-mcp

[![Listed on mcpservers.org](https://mcpservers.org/badge.svg)](https://mcpservers.org/servers/jidoseal/jidoseal-mcp)

**Check a folder of markdown notes against Open Knowledge Format (OKF) v0.2 — from inside Claude Code, Claude Desktop, Cursor, GitHub Copilot, OpenAI Codex, Gemini CLI, Zed, Cline, Continue, JetBrains AI Assistant or a local model, on your own machine.**

Pick a folder, scan it. `jidoseal-mcp` is a local [Model Context Protocol](https://modelcontextprotocol.io) server that reads the YAML frontmatter of every `*.md` file under a folder, reports which **tier** the knowledge base reaches (OKF Certified / Bronze / Silver / Gold), and lists — per file — the exact frontmatter fields missing for the next tier. The scan sends nothing over the network: no file, no file name, no file content. That is JidoSeal's own claim about its engine; [below](#what-leaves-your-machine) is how to check it.

```bash
pip install jidoseal-mcp
claude mcp add jidoseal -- jidoseal-mcp     # Claude Code; every other tool is below
```

Then ask your assistant: *"Scan ~/notes with JidoSeal and tell me what's missing for Bronze."*

> **New: [State of OKF, October 2026](https://github.com/Jidoseal/jidoseal-mcp/blob/main/reports/state-of-okf/2026-10/README.md).** All 900 bundles listed on BundleDex, checked against OKF v0.2 on 2026-10-22: conformance, which of the two v0.2 texts each bundle's timestamps follow, trust fields, and a [leaderboard](https://github.com/Jidoseal/jidoseal-mcp/blob/main/reports/state-of-okf/2026-10/leaderboard.md), with the method and a page per bundle.

### Try it in 60 seconds

Free and local; the scan engine is proprietary; JidoSeal also sells optional certificates.

Pick a folder, scan it. Watch the 76-second run first: [Check an OKF v0.2 folder in 60 seconds (free, local)](https://youtu.be/useMCASUHQ0). To try it on the three-file sample in this repository:

```bash
git clone --depth 1 https://github.com/Jidoseal/jidoseal-mcp && cd jidoseal-mcp/examples/tiers/mixed
pip install jidoseal-mcp
claude mcp add jidoseal -- jidoseal-mcp     # Claude Code; Cursor, Copilot, Codex, Gemini CLI, Zed and local models are below
claude
```

(`claude mcp add` registers the server for the folder you run it in, so run it there, or add `-s user`.) Then ask: *"Scan this folder with JidoSeal. Which tier does it reach, and what does each file need for Bronze?"*

The `jidoseal_scan` result it gets back, from a real run of `jidoseal-mcp` 0.3.0 (engine 0.2.0, OKF Folder Criteria v1.0.0) on that folder on 2026-11-21 (UTC), trimmed to the summary and the Bronze gaps:

```jsonc
{
  "corpus": { "file_count": 3, "tier": "none", "criteria_version": "1.0.0",
              "coverage": { "okf-certified": 66.7, "bronze": 33.3, "silver": 33.3, "gold": 0.0 } },
  "files": [
    { "name": "expenses.md", "tier": "okf-certified", "present": [ "type", "title" ],
      "missing": { "bronze": [ { "field": "description", "fix": "AUTO" },
                               { "field": "timestamp",   "fix": "AUTO" },
                               { "field": "owner",       "fix": "NEEDS-CLIENT" } ] } },  // silver gaps trimmed
    { "name": "leave-policy.md", "tier": "silver",
      "missing": { "bronze": [], "silver": [] } },
    { "name": "notes.md", "tier": "none", "present": [],
      "missing": { "okf-certified": [ { "field": "type", "fix": "AUTO", "value": "note", "confidence": "MEDIUM", "inferred": true } ],
                   "bronze": [ { "field": "title",       "fix": "AUTO" },
                               { "field": "description", "fix": "AUTO" },
                               { "field": "timestamp",   "fix": "AUTO" },
                               { "field": "owner",       "fix": "NEEDS-CLIENT" } ] } }  // silver gaps trimmed
  ],
  "skipped": [],
  "certified_eligible": false,
  "okf11Result": "1/3",
  "score": 33
  // … plus audit id, rubric, file hashes, Merkle root and the paths of the two files written under .jidoseal/
}
```

The folder reaches no tier yet because `notes.md` has no frontmatter: a corpus's tier is that of its weakest file. Each list under `missing` names the gaps that block that tier, so `bronze` holds what a file still needs for Bronze. `AUTO` marks a value JidoSeal can propose; `NEEDS-CLIENT` marks one only you can answer (here, `owner`).

> **Independent.** Open Knowledge Format (OKF) v0.2 is an open specification in Google's GoogleCloudPlatform/open-knowledge-format repository, under the Apache-2.0 licence. JidoSeal checks a folder against the three conformance rules in OKF §11 and reports the result. Bronze and Silver add document fields. Gold adds AI-provenance fields. A JidoSeal certificate is not an ISO certification. JidoSeal is independent of Google and of ISO, and is not affiliated with, sponsored by, or endorsed by either.

### Side effects and data, in brief

- **Reads:** the `*.md` files under the folder you give it (hidden files and folders are skipped), plus `<folder>/.jidoseal/config.yaml` if present. The server refuses a folder that contains a symlink to a directory or to a file outside the folder.
- **Writes:** `<folder>/.jidoseal/manifest.json` (replaced on each scan) and `<folder>/.jidoseal/progress.ndjson` (appended to). Nothing else; your notes are not modified.
- **Trust and changes tools:** `jidoseal_trust` and `jidoseal_changes` read only and write nothing. `jidoseal_changes` runs the local `git` program, with transports disabled, to read the folder's history.
- **Network, scan and offer:** none, by JidoSeal's own claim about its proprietary engine, not independently audited. The tests below check it on every change.
- **Network, checkout (optional, paid):** `jidoseal_start_checkout` runs only with `confirm: true`. It sends twelve fields to jidoseal.com: company, name and email as typed, the tier (Bronze, Silver or Gold), a 0–100 score, the corpus's Merkle root, three counts of files below Bronze, Silver and Gold, the number of files scanned, the criteria version the scan ran under, and the local scan's id. jidoseal.com copies them into the Stripe Checkout session it creates (the email as the session's customer email, all twelve as session metadata), when the session is created, before any payment. No file contents, file names, per-file hashes or paths. No card data passes through this server.
- **Network, free OKF Certified certificate (optional):** `jidoseal_request_free_certificate` runs only with `confirm: true`, for a folder where every file passes the three OKF v0.2 §11 rules and with 25 or more files. It sends eight fields to jidoseal.com: company, name and email as typed, a 0–100 score, the corpus's Merkle root, the text `3/3`, the number of files, and one digest of the folder's own `.jidoseal/config.yaml` (or the text `absent:no-config-file`). jidoseal.com emails a confirmation link that expires in 72 hours. No file contents, file names, per-file hashes or paths. Nothing is charged.
- **Engine:** the scan engine is the separate `jidoseal` package, under a proprietary licence. It ships as plain Python source and is pinned here to one version (0.2.0), with its sha256 in [`ENGINE-SHA256SUMS`](ENGINE-SHA256SUMS) and an SBOM in [`sbom.cdx.json`](sbom.cdx.json). So "nothing leaves your machine" is JidoSeal's own claim: you can check it with the commands under [What leaves your machine](#what-leaves-your-machine) and the tests in [`tests/`](tests/), but it has not been independently audited.

---

## What it checks

The scan is deterministic — presence of populated frontmatter fields, no model calls, no scoring by opinion. A field counts only if it has real content (`title:` with nothing after it earns nothing).

| Tier | A file must have (populated) |
|---|---|
| **OKF Certified** (free) | A frontmatter block with `type`: every file passes the three OKF v0.2 §11 conformance rules |
| **Bronze** | OKF Certified + `title`, `description`, `timestamp`, `owner` |
| **Silver** | Bronze + `status`, `review_policy`, `reviewed_at`, `next_review_at` |
| **Gold** | Silver + AI-provenance fields: `sources`, `ai_involvement` and `license` (a human `verified` entry is needed only when `ai_involvement` is `assisted` or `generated`) |

Bronze checks fields that help evidence identification of documented information, of the kind ISO 9001 clause 7.5 describes. Silver adds review and change fields. Neither shows conformity with ISO 9001 or with ISO 30401. Gold checks that provenance and AI-involvement fields exist, are well-formed and agree with each other. It does not check that the fields are true. It is not ISO/IEC 42001 certification, an AI Act conformity assessment, or legal advice.

These are OKF Folder Criteria v1.0.0, which engine 0.2.0 grades against by default. Criteria v0.9.2 named the tiers differently (its Silver is today's Bronze, and its Gold is today's Silver); certificates issued under v0.9.2 keep their name.

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
ai_involvement: none
sources: []
license: proprietary
---
```

Worked examples for each tier, and a mixed folder, are in [`examples/tiers/`](examples/tiers/).

## Tools

| Tool | What it does | Network |
|---|---|---|
| `jidoseal_scan` | The free Self-Check over a folder on this machine, graded against OKF Folder Criteria v1.0.0: corpus tier, per-file missing fields for the next tier (each marked `AUTO` — a value JidoSeal can propose — or `NEEDS-CLIENT` — only the owner can answer), coverage per tier, a 0–100 score, and a Merkle root of the corpus. | none (JidoSeal's claim; see [below](#what-leaves-your-machine)) |
| `jidoseal_certification_offer` | What certification would cost for this corpus (OKF Certified is free; Bronze $349, Silver $599, Gold $999), why, what it includes, and exactly which facts a request or purchase would send. Computes locally; starts nothing. | none (same claim) |
| `jidoseal_start_checkout` | For a Bronze, Silver or Gold folder, only on your explicit go-ahead, passed as `confirm: true` (without it, nothing is sent): asks jidoseal.com to create a Stripe Checkout session and returns the link for you to open. Takes no payment. | jidoseal.com, which passes the fields to Stripe |
| `jidoseal_request_free_certificate` | For an OKF Certified folder with 25 or more files, only on your explicit go-ahead, passed as `confirm: true` (without it, nothing is sent): asks jidoseal.com for the free OKF Certified certificate. jidoseal.com emails you a confirmation link that expires in 72 hours. Nothing is charged. | jidoseal.com |
| `jidoseal_trust` | Before an agent relies on a document: `stale`, `unverified` or `ok`, with the reasons, from its OKF v0.2 trust and lifecycle fields (`stale_after`, `status`, `verified`, `generated`). Also its trust tier (§5.3), whether it meets OKF v0.2 conformance, and which text of v0.2 its timestamps follow. One file, or every `*.md` in a folder. Reads only. Plain Python in this package; does not use the scan engine. | none |
| `jidoseal_changes` | After an edit: every `*.md` that differs from a git commit (default `HEAD`, so the uncommitted edits and new files), what changed in its frontmatter and body, and what that did to its trust: a verified document whose text changed while `verified` did not, `verified` or `type` removed, `generated.at` not updated, `status` or `stale_after` changed. Reads only. Runs the local `git` with `protocol.allow=never` and no lazy fetch. | none |

Example `jidoseal_scan` result for [`examples/tiers/mixed`](examples/tiers/mixed) (three files, one Silver, one OKF Certified, one with no frontmatter):

```jsonc
{
  "corpus": { "file_count": 3, "tier": "none", "criteria_version": "1.0.0",
              "coverage": { "okf-certified": 66.7, "bronze": 33.3, "silver": 33.3, "gold": 0.0 } },
  "score": 33,
  "okf11Result": "1/3",
  "certified_eligible": false,
  "files": [
    { "name": "expenses.md", "tier": "okf-certified",
      "missing": { "bronze": [ { "field": "description", "fix": "AUTO" },
                               { "field": "timestamp",   "fix": "AUTO" },
                               { "field": "owner",       "fix": "NEEDS-CLIENT" } ] } }
    // …
  ]
}
```

`frontmatter_ok: false` on a file means its frontmatter block exists but does not parse; no field write can close its gaps until it is fixed by hand.

### Trust before you rely on a document

Ask: *"Before you use ~/notes/policies/leave.md, check it with jidoseal_trust."* or, after an agent has edited your notes, *"Run jidoseal_changes on ~/notes: what did you change, and which verified documents did it leave unconfirmed?"* A `jidoseal_trust` answer for one file:

```jsonc
{
  "verdict": "unverified",
  "reasons": [ "content changed at 2026-10-01T00:00:00Z, after its latest verification at 2026-06-25T09:00:00Z" ],
  "okf_conformant": true,
  "trust_tier": "human-reviewed",
  "status": "stable",
  "stale": false,
  "which_0_2": "2026-08-21"
  // … plus each timestamp as written and which v0.2 text it follows
}
```

OKF v0.2 changed on 2026-08-21 without a version bump: `stale_after`, `sources[].last_modified` and `usage_window` went from bare dates to datetimes with a UTC offset. Both forms are accepted, and `which_0_2` says which one a document uses.

## Install and wire it into your tool

Requires Python 3.9+. `pip install jidoseal-mcp` also installs [`jidoseal`](https://pypi.org/project/jidoseal/) (the scan engine and CLI, pinned to the tested version) and puts a `jidoseal-mcp` command on your PATH. No account and no API key. The scan itself needs no network — it runs the same offline.

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
You should see an `initialize` result naming `jidoseal`, then the six tools.

## Run it in CI

The CLI writes `.jidoseal/manifest.json`; a few lines turn it into a gate. See [docs/ci.md](docs/ci.md) for a GitHub Actions workflow that fails the build when any file falls below Bronze.

## What leaves your machine

**A scan:** JidoSeal's claim is that it sends nothing: not the files, not their names, not their contents. The engine that does the scan is proprietary, and nobody independent has audited this claim. It is built to be checkable: `jidoseal_mcp.py`, `scan_result.py` and `offer.py` import no socket, no `urllib`, no HTTP client, and neither does anything they pull in, including the twelve engine modules the pinned `jidoseal` wheel contains. `checkout_client.py` is the one module that can reach the network, and it is imported only inside the two handlers that talk to jidoseal.com (checkout and the free certificate request). `git_changes.py`, behind `jidoseal_changes`, is the one module that starts a program: the local `git`, with transports disabled (`protocol.allow=never`, `GIT_NO_LAZY_FETCH=1`), imported only inside its own handler.

**A purchase**, only if you choose one and the call carries `confirm: true`: the company, name and email you typed, the tier, a 0–100 score, the corpus's Merkle root, three counts of files below Bronze, Silver and Gold, the number of files scanned, the criteria version the scan ran under, and the local scan's id, sent to jidoseal.com. jidoseal.com copies them into the Stripe Checkout session it creates: the email as the session's customer email, and all twelve as session metadata. That happens when the session is created, before any payment. No file contents, no file names, no per-file hashes, no paths, and no card data through this server (Stripe hosts the payment page). The Merkle root is a one-way digest.

**A free OKF Certified request**, only if you choose one and the call carries `confirm: true`: the company, name and email you typed, a 0–100 score, the corpus's Merkle root, the text `3/3`, the number of files, and one digest of the folder's own `.jidoseal/config.yaml` (or `absent:no-config-file`), sent to jidoseal.com. jidoseal.com emails a confirmation link that expires in 72 hours. No file contents, no file names, no per-file hashes, no paths. Nothing is charged.

Verify it yourself:

```bash
strace -f -o /tmp/trace.txt -e trace=network jidoseal-mcp < your-jsonrpc-input   # no network syscalls during a scan
bwrap --unshare-net --dev-bind / / jidoseal-mcp < your-jsonrpc-input             # the scan works with no network at all
```

The scan writes its own records — `manifest.json` and an appended `progress.ndjson` — under `<folder>/.jidoseal/` and nowhere else. It never modifies your notes.

The test suite checks the same things on every change, against the pinned engine wheel after verifying its sha256 (see [`.github/workflows/tests.yml`](.github/workflows/tests.yml)):

| File | What it holds |
|---|---|
| [`tests/test_scan_isolation.py`](tests/test_scan_isolation.py) | The scan opens and lists nothing outside the folder; folders with symlinks that lead out of it, or to directories, or that redirect `.jidoseal/`, are refused before the engine runs; and the installed `jidoseal` CLI (engine 0.2.0) refuses links out on its own, writing nothing. |
| [`tests/test_write_boundary.py`](tests/test_write_boundary.py) | The only files created or changed are the two under `<folder>/.jidoseal/`; notes are byte-for-byte unchanged. |
| [`tests/test_network_boundary.py`](tests/test_network_boundary.py) | No socket, DNS lookup or child process during a scan — in-process with sockets blocked, and end to end over stdio in a process that exits on any socket event. |
| [`tests/test_checkout_confirmation.py`](tests/test_checkout_confirmation.py) | Checkout makes no request without `confirm: true`, and with it sends exactly the twelve fields above (HTTP mocked). [`tests/test_free_certificate.py`](tests/test_free_certificate.py) holds the same for the free request and its eight fields. |
| [`tests/test_import_graph.py`](tests/test_import_graph.py) | Static check of every module on the scan path, the engine's included. |
| [`tests/test_trust_and_changes.py`](tests/test_trust_and_changes.py) | `jidoseal_trust` and `jidoseal_changes`: verdicts, the two v0.2 timestamp texts, no writes, no socket, and `git` as the only program `jidoseal_changes` starts, always with transports disabled. |
| [`tests/test_packaging.py`](tests/test_packaging.py) | The engine pin, `ENGINE-SHA256SUMS`, the SBOM and the installed engine files all agree. No tool text or result shows the engine's unqualified no-egress line, and the checkout text names the Stripe step. |

The `jidoseal` command-line tool refuses such folders too, from engine 0.1.4 (0.2.0 is pinned here): a symlink to a file or directory outside the folder, or a symlinked `.jidoseal/`, stops the run before anything is read or written, and the command exits with status 2. It does not follow a symlinked directory inside the folder either, so each file is read once. This server is a little stricter: it refuses a symlinked directory even when it stays inside. The CLI's own no-network line is worded as JidoSeal's claim, like this server's. Engine 0.1.3 and earlier followed symlinks and printed an unqualified line, so use 0.1.4 or later.

## Optional certification

Scanning is free and unlimited, and so are the fixes. A folder where every file passes the three OKF v0.2 §11 rules, with 25 or more files, can get the OKF Certified certificate free. A dated certificate for a higher grade, bound to the Merkle root of your corpus, with a public verification page and a listing in the public registry, is a paid step on [jidoseal.com](https://jidoseal.com): Bronze $349 (renewal $200), Silver $599 ($300), Gold $999 ($450), one flat price per grade however many files. A person at JidoSeal signs it off from the grade, the score and that fingerprint only, never from your file contents.

- Agency 5-pack: five Bronze certificates, $1,299, use them within 12 months.
- Certified OKF tool: includes one 50%-off Bronze code.
- Refer a peer: they get 20% off a Bronze certificate.

## Links

- Website: <https://jidoseal.com>
- Public registry of certified knowledge bases: <https://jidoseal.com/registry>
- PyPI: [`jidoseal-mcp`](https://pypi.org/project/jidoseal-mcp/) · [`jidoseal`](https://pypi.org/project/jidoseal/)
- MCP Registry: `com.jidoseal/jidoseal-mcp`
- OKF specification (Google Cloud, Apache-2.0): <https://github.com/GoogleCloudPlatform/open-knowledge-format>
- Contact: support@jidoseal.com

## About this repository

This repository holds the source of the `jidoseal-mcp` package: an MCP server implemented on the Python standard library alone (no MCP SDK), speaking JSON-RPC 2.0 over stdio. It depends on the separately published [`jidoseal`](https://pypi.org/project/jidoseal/) package for the scan engine, which is **not** part of this repository and is pinned to one tested version. Run the tests with `pip install -e ".[test]" && pytest`. Issues are welcome; please include the `jidoseal-mcp` and `jidoseal` versions and the smallest folder that reproduces a problem.

## License

Apache-2.0 for the code in this repository — see [LICENSE](LICENSE). The `jidoseal` engine it depends on is distributed separately under its own terms.
