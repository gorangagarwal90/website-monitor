# GemsNY Image Audit — Live Progress

This is an isolated live-progress version of the GemsNY product image auditor. It does not replace the existing website-monitor project in this repository.

## What it checks
- All eligible GemsNY product/category URLs discovered from the public sitemap
- Numeric pagination across category grids
- Loose gemstone product cards
- Jewelry/preset product cards
- Original/source image dimensions
- Minimum requirement: 500 x 500 pixels

## Live progress
Open **Actions → GemsNY Image Audit - Live Progress**. Each shard streams lines like:

`PROGRESS | shard=3 | category=Sapphire | page=42 | pages_checked=42 | images_checked=1008 | categories_completed=0/8 | elapsed_seconds=...`

This lets you see pages and product images being checked while the audit is still running.

## Final output
After all 16 shards finish, GitHub automatically builds the final Excel report and uploads the artifact:

`FINAL-GemsNY-Image-Audit-Live-Progress`

The workflow runs 16 shards concurrently.
