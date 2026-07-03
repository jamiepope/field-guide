# Paris Field Guide

This repository is a Markdown-first source of truth for a Paris family trip.
It stores researched facts, human-readable day plans, logistics, tickets, and transit notes as plain Markdown and generates a static site into `docs/`.

> **Status:** In Progress

## Current Sprint

**Goal**

Complete a fully verified Paris Field Guide before departure.

### Remaining Work

- [ ] Complete attraction research
- [ ] Complete logistics research
- [ ] Finalize transit strategy
- [ ] Add restaurants and cafés
- [x] Build static website
- [ ] Generate daily email brief

## Principles

- Markdown is canonical.
- Research files hold verified facts.
- Day files stay concise and usable on a phone.
- Logistics, tickets, and transit records stay separate from day narratives.
- Detailed facts should live in research files, not duplicated into day files.
- Factual sections remain `TODO` until sourced.
- No travel facts should be invented.
- No attraction hours, prices, policies, transport rules, or recommendations should be added unless they are explicitly present in existing Markdown sources.

## Repo Layout

| Path | Purpose |
| --- | --- |
| `days/` | Daily guide pages for the trip. |
| `research/` | Verified research notes, split by topic. |
| `research/attractions/` | Attraction-specific research files. |
| `research/logistics/` | Arrival and transit research files. |
| `assets/css/` | Source stylesheets copied into the generated site. |
| `assets/js/` | Source JavaScript, if needed later. |
| `assets/images/` | Source image assets, if needed later. |
| `logistics.md` | Trip logistics that do not belong to a single day. |
| `tickets.md` | Ticket tracking and confirmation notes. |
| `transit-ledger.md` | Transit planning and movement ledger. |
| `itinerary.md` | High-level trip outline. |
| `templates/` | Jinja HTML templates and Markdown templates for new content. |
| `generator/` | Python static-site generator modules. |
| `scripts/` | Build and validation entry points. |
| `docs/` | Generated static site output only; this is the Cloudflare Pages publish directory. |

## Research Rules

Each research file should use these sections:

- `Official Facts`
- `Observations`
- `Recommendations`
- `Sources`

Keep `Official Facts` empty or marked `TODO` until backed by a source in the same file.
Use `Observations` for notes from the guide-building process.
Use `Recommendations` only when a recommendation is explicitly supported by existing Markdown content.
Use `Sources` for source names, URLs, access dates, and any verification notes.

Day files should link to relevant research files instead of copying detailed facts into the daily guide.
They should focus on the practical shape of the day: plan, notes, logistics, and open questions.

## Templates

Use the files in `templates/` when adding new Markdown content:

- `templates/day.md`
- `templates/research.md`
- `templates/logistics.md`
- `templates/ticket.md`
- `templates/transit-ledger.md`

## Static Site

Build the static site with:

```bash
./build.sh
```

The build process:

- creates `.venv/` if needed
- installs `requirements.txt`
- renders Markdown through the Python generator
- copies source assets from `assets/` to `docs/assets/`
- writes generated HTML and copied assets into `docs/`

Preview the generated site locally with:

```bash
./serve.sh start
./serve.sh status
./serve.sh stop
```

Check generated links and asset references with:

```bash
.venv/bin/python scripts/check_site.py
```

Review screenshots should be written to `tmp/screenshots/` and cleaned with `./scripts/clean-screenshots.sh`.

## Cloudflare Pages

Use these Cloudflare Pages settings:

| Setting | Value |
| --- | --- |
| Framework preset | None |
| Build command | `./build.sh` |
| Output directory | `docs` |

See [DEPLOY.md](DEPLOY.md) for deployment setup and checklist.

Do not create a React app.
