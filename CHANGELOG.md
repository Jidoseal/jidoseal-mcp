# Changelog

## 0.3.2 — 2026-11-23
- Fix: `jidoseal_start_checkout` now also sends `fileCount` (how many files the scan read) and `criteriaVersion` (the rules the scan ran under, `1.0.0`). jidoseal.com's `/api/checkout` now requires both: it refuses a paid certificate for fewer than 25 files, and refuses a scan under any rules but OKF Folder Criteria v1.0.0. Versions 0.3.0 and 0.3.1 don't send these fields, so their paid checkouts are refused with a 400 that says to run `pip install -U jidoseal-mcp`. The paid request now carries twelve fields; the README and the offer text say so. Nothing else changed: same engine pin (`jidoseal==0.2.0`), same criteria (v1.0.0), no new network use.

## 0.3.1 — 2026-11-22
- Fix: `jidoseal_start_checkout` now sends `filesBelowBronze`, `filesBelowSilver` and `filesBelowGold` (counts of files below each tier, from the scan's new `filesBelow`). jidoseal.com's `/api/checkout` requires them and refused every paid checkout from 0.3.0 with a 400 ("missing its per-file tier counts"). The paid request now carries ten fields; the README and the offer text say so. Nothing else changed: same engine pin (`jidoseal==0.2.0`), same criteria (v1.0.0), no new network use.

## 0.3.0 — 2026-11-21
- OKF Folder Criteria v1.0.0 ladder (OKF Certified free, Bronze $349, Silver $599, Gold $999), engine `jidoseal==0.2.0`, free OKF Certified request via `/api/certify-free`.
