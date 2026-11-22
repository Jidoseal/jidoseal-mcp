# JidoSeal tier requirements: OKF Folder Criteria v1.0.0

This is the complete, exact rubric `jidoseal` (engine 0.2.0) and `jidoseal-mcp` (0.3.0) apply. It
describes what the free local scan checks; it does not describe any private service. Everything
here is reproducible: pick a folder, scan it, and compare against the table.

Open Knowledge Format (OKF) v0.2 is an open specification in Google's
GoogleCloudPlatform/open-knowledge-format repository, under the Apache-2.0 licence. JidoSeal
checks a folder against the three conformance rules in OKF §11 and reports the result. Bronze
and Silver add document fields. Gold adds AI-provenance fields. A JidoSeal certificate is not an
ISO certification. JidoSeal is independent of Google and of ISO, and is not affiliated with,
sponsored by, or endorsed by either.

Bronze checks fields that help evidence identification of documented information, of the kind
ISO 9001 clause 7.5 describes. Silver adds review and change fields. Neither shows conformity
with ISO 9001 or with ISO 30401. Gold checks that provenance and AI-involvement fields exist,
are well-formed and agree with each other. It does not check that the fields are true. It is not
ISO/IEC 42001 certification, an AI Act conformity assessment, or legal advice.

## The ladder

| Tier | Every file needs | Certificate |
|---|---|---|
| OKF Certified | A frontmatter block with `type`: the three OKF v0.2 §11 conformance rules | Free |
| Bronze | OKF Certified + a title, description, date and owner | $349 (renewal $200) |
| Silver | Bronze + a status, a review policy and the dates of its last and next review | $599 (renewal $300) |
| Gold | Silver + AI-provenance fields: sources, AI involvement and licence | $999 (renewal $450) |

`tier(file)` is the highest tier whose fields the file has, and each tier needs everything below
it. `tier(corpus)` is the lowest tier of any file in it, and is `none` if the third OKF §11 rule
fails or the folder has no in-scope file.

The scan and the fixes are free. The OKF Certified certificate is free for a folder with 25 or
more files (one per email address, per folder and per company domain). Agency 5-pack: five
Bronze certificates, $1,299, use them within 12 months. Certified OKF tool: includes one
50%-off Bronze code. Refer a peer: they get 20% off a Bronze certificate.

Criteria v0.9.2 named the tiers differently: its Silver is today's Bronze, and its Gold is
today's Silver. `jidoseal --criteria 0.9.2` still prints that older result. Certificates issued
under v0.9.2 keep their name.

## Fields

| Field | Tier | Accepted spellings |
|---|---|---|
| `type` | OKF Certified | `type` (the literal key, as OKF §11 reads it) |
| `title` | Bronze | `title` |
| `description` | Bronze | `description`, `desc` |
| `timestamp` | Bronze | `timestamp`, `updated`, `created`, `date`, or `generated.at` |
| `owner` | Bronze | `owner`, `author`, or `generated.by` |
| `status` | Silver | `status` |
| `review_policy` | Silver | `review_policy` (the review cadence you choose) |
| `reviewed_at` | Silver | `reviewed_at` (last review) |
| `next_review_at` | Silver | `next_review_at` (next review due) |
| `ai_involvement` | Gold | `ai_involvement`: `none`, `assisted` or `generated` |
| `sources` | Gold | `sources`: a list of sources, each with an `author` and a `resource`; an empty list only when `ai_involvement` is `none` |
| `license` | Gold | `license`: `proprietary`, `internal`, a `LicenseRef-` identifier or an SPDX identifier |

When `ai_involvement` is `assisted` or `generated`, Gold also needs `generated.by`,
`generated.at` and a `verified` entry by a human (`human:name`) dated between the two dates and
the scan date. The engine reports Gold gaps as a tier (a file that meets Silver but not Gold is
Silver); it does not list per-field Gold gaps.

`stale_after` is recognised and reported in the manifest but is not required by any tier.

## What "populated" means

A field counts only if it carries content. Missing, `null`, empty or whitespace-only strings,
and empty lists/maps do **not** count. Numbers, booleans and dates do. A bare `title:` earns
nothing.

## What is excluded

- `index.md` and `log.md` — OKF v0.2's two reserved filenames — are never scored as concept
  documents.
- Nothing else, by default. No folder name is special. A corpus can declare its own
  conventions (generated folders, sync mirrors, default owners) in `<root>/.jidoseal/config.yaml`;
  the config's digest is recorded on the manifest so a scan is tied to the corpus definition it ran under.

## What is tolerated when reading

- A UTF-8 byte-order mark before the opening `---`.
- Tab characters in frontmatter indentation.
- `---` appearing inside a value (only a line that is exactly `---` closes the block).
- Full-width colons and native-language field names for 12 locales (`en zh-CN zh-TW es ja de fr pt-BR pt-PT ko ru hi`), mapped back to the canonical English field — on the read side only.
- A frontmatter block that does not parse is reported (`frontmatter_ok: false`) rather than silently scored as empty.

## Coverage and score

Coverage for a tier is the percentage of files that reach **at least** that tier, reported for
OKF Certified, Bronze, Silver and Gold. The 0–100 `score` is the mean of the four coverages,
rounded half-up. A corpus is eligible for a certificate at the tier it reaches: OKF Certified
(free) once every file passes the three §11 rules, and a paid tier from Bronze up.

## The gap list

The gap lists in `jidoseal_scan` are keyed by the tier they block: `okf-certified` holds the `type` gap, `bronze` the title, description, timestamp and owner, `silver` the four review fields. For every file below a tier, the scan says which fields are missing and how each could be closed:

- `AUTO` — a value can be proposed mechanically (for example `status: stable`, or a title taken from the file's first heading or its file name).
- `NEEDS-CLIENT` — only the owner can answer it (`owner`, `review_policy`, `reviewed_at`, `next_review_at`); the scan offers a default (`yearly`, today, one year out) but never fills it in for you.

See [`examples/tiers/`](../examples/tiers/) for one folder per tier and a mixed one.
