# JidoSeal tier requirements — OKF v0.2, plus fields that evidence ISO 9001 §7.5.2 and ISO 30401

This is the complete, exact rubric `jidoseal` and `jidoseal-mcp` apply. It describes what the
free local scan checks; it does not describe any private service. Everything here is
reproducible: pick a folder, scan it, and compare against the table.

Independent of Google and of ISO. OKF is an open specification from Google Cloud. JidoSeal is
not affiliated with, sponsored by, or endorsed by Google or ISO.

ISO names no fields. ISO 9001 §7.5.2 asks for appropriate identification and description of
documented information and gives examples ("a title, date, author, or reference number"), not a
fixed list; Silver's four fields are one reasonable way to evidence it. ISO 30401 asks that
knowledge be kept current under defined governance and sets no review interval; Gold's status
and stated review policy, with real review dates, are how you evidence it. The mapping is
JidoSeal's own, and a JidoSeal tier is not an ISO certification.

## The rule, in one line

`tier(file) = gold if Silver ∧ status ∧ review_policy ∧ reviewed_at ∧ next_review_at; silver if Bronze ∧ title ∧ description ∧ timestamp ∧ owner; bronze if type; else none`
`tier(corpus) = the lowest tier of any file in it.`

## Fields

| Field | Tier | What it evidences | Accepted spellings |
|---|---|---|---|
| `type` | Bronze | OKF v0.2 (the one required field) | `type` |
| `title` | Silver | ISO 9001 §7.5.2 — identification (e.g. a title) | `title` |
| `description` | Silver | ISO 9001 §7.5.2 — description | `description`, `desc` |
| `timestamp` | Silver | ISO 9001 §7.5.2 — identification (e.g. a date) | `timestamp`, `updated`, `created`, `date`, or `generated.at` |
| `owner` | Silver | ISO 9001 §7.5.2 — identification (e.g. an author) | `owner`, `author`, or `generated.by` |
| `status` | Gold | ISO 30401 kept-current governance — lifecycle status | `status` |
| `review_policy` | Gold | ISO 30401 kept-current governance — the review cadence you choose (ISO 30401 sets no interval) | `review_policy` |
| `reviewed_at` | Gold | ISO 30401 kept-current governance — last review | `reviewed_at` |
| `next_review_at` | Gold | ISO 30401 kept-current governance — next review due | `next_review_at` |

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

Coverage for a tier is the percentage of files that reach **at least** that tier. The 0–100
`score` is the mean of the Bronze, Silver and Gold coverages, rounded half-up. A corpus is
eligible for certification once every file reaches Bronze (100% Bronze coverage).

## The gap list

For every file below a tier, the scan says which fields are missing and how each could be closed:

- `AUTO` — a value can be proposed mechanically (for example `status: stable`, or a title taken from the file's first heading or its file name).
- `NEEDS-CLIENT` — only the owner can answer it (`owner`, `review_policy`, `reviewed_at`, `next_review_at`); the scan offers a default (`yearly`, today, one year out) but never fills it in for you.

See [`examples/tiers/`](../examples/tiers/) for one folder per tier and a mixed one.
