# Paris Field Guide

This repository is a Markdown-first source of truth for a Paris family trip.
It stores researched facts, human-readable day plans, logistics, tickets, and transit notes as plain Markdown so a static site can be generated later.

No app has been generated yet. The eventual static site should live in `docs/`.

> **Status:** In Progress

## Current Sprint

**Goal**

Complete a fully verified Paris Field Guide before departure.

### Remaining Work

- [ ] Complete attraction research
- [ ] Complete logistics research
- [ ] Finalize transit strategy
- [ ] Add restaurants and cafés
- [ ] Build static website
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
| `research/transport/` | Arrival and transit research files. |
| `logistics.md` | Trip logistics that do not belong to a single day. |
| `tickets.md` | Ticket tracking and confirmation notes. |
| `transit-ledger.md` | Transit planning and movement ledger. |
| `itinerary.md` | High-level trip outline. |
| `templates/` | Markdown templates for new content. |
| `docs/` | Future generated static site output. |
| `assets/` | Future static site assets. |
| `data/` | Future structured data, if needed. |
| `references/` | Supporting reference material. |
| `scripts/` | Future generation or validation scripts. |

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

Do not generate HTML yet.
Do not create a React app.
Do not add dependencies unless the project explicitly moves into a generation phase.
