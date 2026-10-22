# State of OKF, October 2026

**What this is:** a check of every public bundle listed on [BundleDex](https://bundledex.net) against the Open Knowledge Format (OKF) v0.2 specification, with the method stated below so anyone can repeat it. **Data:** BundleDex's full list as published at 2026-10-21T19:02:06Z; every repository fetched and checked on 2026-10-22 (UTC), at the commit recorded for it in [data.json](data.json). **By:** JidoSeal. OKF is an open specification from Google Cloud; JidoSeal is not affiliated with Google.

The leaderboard is in [leaderboard.md](leaderboard.md). Each bundle has its own page under [bundles/](bundles/), listing the exact files and values behind its result and what to change.

## The numbers

| | |
|---|---|
| Entries on BundleDex | 900 (873 distinct repositories; 27 are listed twice) |
| Repositories fetched | 829 (44 could not be fetched: removed, renamed or private) |
| Repositories with an OKF bundle in them | 528. The other 301 hold no `.md` file with an OKF `type`; many of them are OKF tools, skills or converters rather than bundles |
| Concept files checked | 107,983 (median bundle: 11 files) |
| Bundles that meet OKF v0.2 conformance (§11, items 1 and 2) | **282 of 528 (53%)** |
| Bundles not yet conformant that are one or two files away | 91 of 246 |
| Bundles that declare `okf_version` in an `index.md` | 304: 214 say `"0.2"`, 90 say `"0.1"` |
| Bundles whose timestamps follow the 2026-08-15 text of v0.2 / the 2026-08-21 text / fit both | 49 / 35 / 78 |
| Bundles with a timestamp value that neither text allows | 33 |
| Bundles that record a `verified` entry on any file | 110 |

## Which 0.2?

OKF v0.2 changed on 2026-08-21 without a version bump ([pull 6](https://github.com/GoogleCloudPlatform/open-knowledge-format/pull/6), merge commit `ad30107`; the question is raised in issue [#24](https://github.com/GoogleCloudPlatform/open-knowledge-format/issues/24)). Both texts say `okf_version: "0.2"`:

| Field | Text of 2026-08-15 (commit `25461db`) | Text of 2026-08-21 (current) |
|---|---|---|
| `stale_after`, `sources[].last_modified`, `usage_window.from` / `.to` | bare date, `2026-12-31` | ISO 8601 datetime with a UTC offset, `2026-12-31T00:00:00Z` |
| `generated.at`, `verified[].at` | ISO 8601 datetime | ISO 8601 datetime with a UTC offset |

So a bundle's own timestamps are the only way to tell which text it follows. (BundleDex lists all 900 entries as `okf_version` `"0.1"`, so its column cannot tell them apart either.) Of the 528 bundles:

| Timestamps | Bundles | Of which declare `"0.2"` |
|---|---|---|
| No timestamp fields at all | 333 | 65 |
| Fit both texts (only `generated.at` / `verified[].at`, all with an offset) | 78 | 62 |
| Follow the 2026-08-21 text | 35 | 30 |
| Follow the 2026-08-15 text | 49 | 33 |
| Mix the two texts | 0 | 0 |
| Include a value neither text allows | 33 | 24 |

Across all files, 5,309 timestamp values are written the 2026-08-15 way. They are valid under that text; to follow the current one, `2026-12-31` becomes `2026-12-31T00:00:00Z`. A bare date names a different instant in each timezone, which is the reason pull 6 gives for the change.

The 33 bundles with a value neither text allows fall into two groups: 18 have template placeholders left in place (`YYYY-MM-DD`, `<ISO timestamp>`, `{{date}}`), and 15 write `generated.at` or `verified[].at` as a bare date, which both texts call a datetime. (5 have other values, such as `soon` or a relative period.)

## Conformance

OKF v0.2 §11 calls a bundle conformant when (1) every non-reserved `.md` file has a parseable YAML frontmatter block and (2) every block has a non-empty `type`. This report checks those two items; it does not check item 3 (the structure of `index.md` and `log.md`).

- 282 of 528 bundles meet both. Where the bundle declares its own root with an `index.md` carrying `okf_version`, 222 of 304 do; where the root had to be inferred, 60 of 224.
- Of the 246 that do not yet, 91 are one or two files away, and 159 have a `README.md` without frontmatter inside the bundle folder (typically because the bundle is the repository root). Moving the bundle into its own folder, or adding frontmatter to that file, is usually the whole change.
- By file: 2,288 files have no frontmatter block, 1,055 have frontmatter but no `type`, and 285 have a block that does not parse as YAML.

**Compared with BundleDex's own flag.** BundleDex marks each entry `okf_conformant` true or false, and does not publish its rule. On the 528 bundles, the two agree on 266 (112 yes, 154 no) and differ on 262 (170 that this check finds conformant and BundleDex does not, 92 the other way). Most differences come from where the bundle is taken to start: BundleDex gives only the repository. This report states its rule below, and each bundle page names the folder it used.

## Trust and lifecycle fields

OKF v0.2 added optional fields that say where a document came from, who confirmed it, and whether it is still current (§5). How many of the 528 bundles use each on at least one file:

| Field | Bundles |
|---|---|
| `status` | 258 |
| `generated` | 193 |
| `sources` | 186 |
| `verified` | 110 |
| `stale_after` | 83 |
| v0.1 `timestamp` (superseded by `generated.at`, §13.1) | 190, of which 163 have no `generated` on any file |
| v0.1 `# Citations` body heading (superseded by `sources`) | 92 |

- **Trust tiers (§5.3), by file:** 885 files are human-reviewed, 369 machine-confirmed, and the rest unverified. (One bundle holds 49,729 of the 107,983 files, so per-bundle counts above say more than file shares.)
- **Past `stale_after`** on 2026-10-22: 60 files in 21 bundles.
- **Changed after their last verification** (`generated.at` later than the newest `verified[].at`): 123 files in 13 bundles. §5.2 keeps the two fields independent, so a reader has to compare them to notice.

## The top 20

Bundles that meet conformance, ordered as in the [leaderboard](leaderboard.md): by the JidoSeal checker's score, then by how many of the five v0.2 trust and lifecycle fields they use, then by size.

| # | Bundle | Files | Timestamps | Trust and lifecycle fields used |
|---|---|---|---|---|
<!-- top20 -->
| 1 | [software-supply-chain-landscape](bundles/software-supply-chain-landscape.md) (jrjsmrtn) | 73 | has values neither text allows | `sources`, `generated`, `verified`, `status`, `stale_after` |
| 2 | [ai-contribution-policies](bundles/ai-contribution-policies.md) (jrjsmrtn) | 61 | 2026-08-15 text | `sources`, `generated`, `verified`, `status`, `stale_after` |
| 3 | [guide_okf](bundles/guide-okf.md) (demouv-projects) | 44 | 2026-08-15 text | `sources`, `generated`, `verified`, `status`, `stale_after` |
| 4 | [memory](bundles/memory.md) (Aeryx-ai) | 20 | 2026-08-21 text | `sources`, `generated`, `verified`, `status`, `stale_after` |
| 5 | [okf-federation](bundles/okf-federation.md) (manaty) | 16 | 2026-08-15 text | `sources`, `generated`, `verified`, `status`, `stale_after` |
| 6 | [ai-brain-starter](bundles/ai-brain-starter.md) (david-wulf) | 15 | has values neither text allows | `sources`, `generated`, `verified`, `status`, `stale_after` |
| 7 | [okf-job-sheet](bundles/okf-job-sheet.md) (muhaj) | 13 | 2026-08-15 text | `sources`, `generated`, `verified`, `status`, `stale_after` |
| 8 | [opengeo-spec](bundles/opengeo-spec.md) (cangqiaoGEO) | 12 | has values neither text allows | `sources`, `generated`, `verified`, `status`, `stale_after` |
| 9 | [okf-bundle](bundles/okf-bundle.md) (BlackBox-ai-lab) | 10 | 2026-08-15 text | `sources`, `generated`, `verified`, `status`, `stale_after` |
| 10 | [okf-skills](bundles/okf-skills.md) (scaccogatto) | 8 | 2026-08-15 text | `sources`, `generated`, `verified`, `status`, `stale_after` |
| 11 | [acme-context-demo](bundles/acme-context-demo.md) (GDG-PVD) | 6 | 2026-08-15 text | `sources`, `generated`, `verified`, `status`, `stale_after` |
| 12 | [okf-seedling](bundles/okf-seedling.md) (watanabe3tipapa) | 6 | 2026-08-15 text | `sources`, `generated`, `verified`, `status`, `stale_after` |
| 13 | [seal-okf](bundles/seal-okf.md) (playidea-lab) | 5 | 2026-08-15 text | `sources`, `generated`, `verified`, `status`, `stale_after` |
| 14 | [okf4net](bundles/okf4net.md) (jchable) | 2 | 2026-08-21 text | `sources`, `generated`, `verified`, `status`, `stale_after` |
| 15 | [okf-bundle-template](bundles/okf-bundle-template.md) (Movida) | 1 | 2026-08-21 text | `sources`, `generated`, `verified`, `status`, `stale_after` |
| 16 | [CRA-knowledge-base](bundles/cra-knowledge-base.md) (JonasLundin) | 336 | 2026-08-21 text | `sources`, `generated`, `status`, `stale_after` |
| 17 | [okf-planning](bundles/okf-planning.md) (chris-page-gov) | 230 | 2026-08-15 text | `sources`, `generated`, `status`, `stale_after` |
| 18 | [AI-Act-knowledge-base](bundles/ai-act-knowledge-base.md) (JonasLundin) | 219 | 2026-08-21 text | `sources`, `generated`, `status`, `stale_after` |
| 19 | [NIST-CSF-knowledge-base](bundles/nist-csf-knowledge-base.md) (JonasLundin) | 157 | 2026-08-21 text | `sources`, `generated`, `status`, `stale_after` |
| 20 | [NIS2-knowledge-base](bundles/nis2-knowledge-base.md) (JonasLundin) | 121 | 2026-08-21 text | `sources`, `generated`, `status`, `stale_after` |
<!-- /top20 -->

## Method

1. **List.** BundleDex's full dataset (`bundledex.net/api/bundles.json`, 900 entries; the fields used are saved here as [bundledex-2026-10-21.json](bundledex-2026-10-21.json), with the sha256 of the full download), reduced to 873 distinct repositories.
2. **Fetch.** One shallow clone per repository with a sparse checkout of `*.md` only, so no code or binary was downloaded or run ([method/fetch.py](../method/fetch.py)).
3. **Find the bundle.** BundleDex gives only the repository, so ([method/analyze.py](../method/analyze.py)):
   - if an `index.md` declares `okf_version` in its frontmatter (§12), the bundle is the folder of the shallowest such file;
   - otherwise, among folders holding `.md` files with a non-empty `type`, the bundle is the folder whose subtree holds the most of them while at least half of its concept files have one (ties: the shallower folder, then the first by name);
   - if no `.md` file has a `type`, no bundle is identified (301 repositories).

   Concept files are the `.md` files under that folder except `index.md` and `log.md` (§3.1), anything under a folder whose name starts with `.` or is `node_modules`, and paths listed in a `.okfignore` at the bundle folder (a BundleDex convention, not part of the specification).
4. **Check each file.** Frontmatter is read with YAML's timestamp conversion turned off, so every value is checked as the author wrote it. The rules (conformance, trust tier, staleness, which text each timestamp follows) are in [src/okf_trust.py](../../../src/okf_trust.py), the same module the `jidoseal_trust` tool uses.
5. **Score.** The JidoSeal checker (`jidoseal` engine 0.1.4, the free local scan behind `jidoseal-mcp`) was run on each bundle folder. Its 0–100 score is the mean of three coverage figures; its Bronze / Silver / Gold tiers are defined by JidoSeal, not by OKF (Bronze is OKF's own rule: every file has a `type`). It did not complete on one bundle, because of a date it could not parse; that is a defect in the checker, and the bundle's other results stand.
6. **Publish.** [method/build.py](../method/build.py) writes the leaderboard, the bundle pages and [data.json](data.json).

**Limits.** BundleDex is not every OKF bundle (GitHub's `okf` topic lists others). The bundle-root rule can pick the wrong folder for a repository that holds several bundles, or a bundle mixed with other Markdown; if it did for yours, say so and it will be corrected. Each result is for the commit recorded, and later commits are not reflected. Hidden folders were not read.

**Who is named.** Bundles that meet conformance are named, in the leaderboard and on their pages. Every other bundle has a page under an id instead of its name, so its result is public but it is not listed by name anywhere in this report.

## Find your bundle

- If it meets conformance, it is in the [leaderboard](leaderboard.md) by name.
- Otherwise its page is `bundles/<id>.md`, where `<id>` is the first 12 characters of the sha256 of `github.com/<owner>/<repo>` in lower case:

  ```bash
  printf '%s' 'github.com/owner/repo' | tr 'A-Z' 'a-z' | sha256sum | cut -c1-12
  ```

  The same id is the `anon_id` of its row in [data.json](data.json); rows for repositories with no bundle found, or that could not be fetched, are there too.
- Wrong folder, a result you think is mistaken, or a page you would rather have under your bundle's name? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).

## Run it on your own folder

The per-file checks in this report are the `jidoseal_trust` tool of `jidoseal-mcp`, free and local. Pick a folder, check it, from Claude Code, Claude Desktop, Cursor, GitHub Copilot, OpenAI Codex, Gemini CLI, Zed, Cline or a local model:

```bash
claude mcp add jidoseal -- uvx jidoseal-mcp     # Claude Code; the other tools are in the main README
```

Then ask: *"Run jidoseal_trust on this folder. Which files are not conformant, which are stale, and which v0.2 text do the timestamps follow?"* The tool reads the files on your machine and writes nothing.

---

*State of OKF is planned as a dated, repeatable report. Corrections are welcome by [issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).*
