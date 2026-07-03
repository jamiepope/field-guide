# Deploying the Paris Field Guide

This project builds a static website from Markdown source files.

Markdown is the source of truth. The generated site is written to `docs/`, which is the Cloudflare Pages publish directory.

## Prerequisites

- Python 3.11 or newer
- `pip`
- A Cloudflare account
- A Cloudflare Pages project connected to this repository

## Local Build

From the repository root:

```bash
./build.sh
```

This command:

- creates `.venv/` if needed
- installs `requirements.txt`
- runs the Python static site generator
- copies source assets from `assets/` to `docs/assets/`
- writes the generated site to `docs/`

## Local Preview

After building:

```bash
python3 -m http.server 8000 --directory docs
```

Open:

```text
http://localhost:8000
```

Stop the preview server with `Ctrl+C`.

## Local Checks

After building, run:

```bash
.venv/bin/python scripts/check_site.py
```

This verifies generated internal links, generated asset references, and local-only path leaks.

## Cloudflare Pages Setup

Create or configure a Cloudflare Pages project with these settings:

| Setting | Value |
| --- | --- |
| Framework preset | None |
| Build command | `./build.sh` |
| Build output directory | `docs` |
| Root directory | repository root |
| Node.js | Not required |

Python should be available in the Cloudflare Pages build environment. If Cloudflare requires an explicit Python version later, add the supported runtime setting in the Cloudflare project configuration.

## Redeploying After Content Changes

1. Edit Markdown source files.
2. Run `./build.sh` locally.
3. Preview with `python3 -m http.server 8000 --directory docs`.
4. Commit the Markdown, generator/template/asset changes if any.
5. Push to the branch connected to Cloudflare Pages.

Cloudflare Pages will run `./build.sh` and publish `docs/`.

## Deployment Checklist

- [ ] Build succeeds with `./build.sh`.
- [ ] Generated-site check succeeds with `.venv/bin/python scripts/check_site.py`.
- [ ] `docs/index.html` exists.
- [ ] `docs/days/*.html` exists for every trip day intended for publication.
- [ ] `docs/assets/css/style.css` exists and loads in the browser.
- [ ] All internal links resolve.
- [ ] Bottom navigation works.
- [ ] Previous/Next day navigation works.
- [ ] Mobile viewport works well around 390-430px wide.
- [ ] Offline/static assets load correctly from `docs/`.
- [ ] No broken images.
- [ ] No missing pages.
- [ ] No localhost URLs, absolute filesystem paths, or runtime-only dependencies appear in generated files.

## Before First Public Deployment

- Review [docs/index.html](docs/index.html) on a phone-sized viewport.
- Review the empty or mismatched [days/2026-07-05.md](days/2026-07-05.md) source before publishing.
- Confirm the ticket list is safe to publish publicly.
- Confirm trip logistics do not expose private information.
- Confirm all intended day pages are present in `docs/days/`.
- Decide whether `docs/` should be committed as generated output or built only by Cloudflare.
