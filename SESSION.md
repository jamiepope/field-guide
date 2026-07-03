# Session Handoff

Last Updated: 2026-07-02

Branch: main

Last Commit:
Build initial static site generator and mobile UI

---

# Current Goal

Finish the Paris Field Guide and deploy a polished, mobile-first static website before departure.

---

# Current Status

## Repository

- ✅ Repository structure complete.
- ✅ Daily itinerary framework complete.
- ✅ Research framework created.
- ✅ Logistics complete.
- ✅ Tickets complete.
- ✅ Transit ledger started.
- ✅ Static site generator implemented.
- ✅ Initial mobile-first website generated.

## Website

Status:

Version 1 renders successfully.

Current focus:

Improve UX, not architecture.

Deployment target:

Cloudflare Pages.

Architecture:

Markdown
→ Python Generator
→ HTML
→ Cloudflare Pages

---

# Current Design Decisions

- Markdown is canonical.
- Research files are the source of truth.
- Day files summarize and link to research.
- Static site only.
- Python generator.
- No React.
- Mobile-first.
- Dark-first.
- Shared design system across future projects.
- Ship usable first. Polish second.

---

# Design System

Repository:

~/Code/design-system

Current palette:

Background: #101418
Surface: #171D23
Surface Elevated: #202832

Text: #F7F8FA
Secondary: #BAC3CF
Muted: #758293

Accent: #7DB7FF
Success: #8EE6B5
Warning: #FFC978
Error: #F26D6D

Current font:

Inter

Status:

Still evolving.

---

# Workflow

1. Research
2. Improve Markdown
3. Generate website
4. Test on phone
5. Commit

---

# Working Rules

- One thing at a time.
- Keep momentum.
- Ship usable first.
- Polish second.
- Mobile-first.
- Facts come from official sources whenever accuracy matters.
- Codex writes repetitive implementation.
- ChatGPT researches, reviews, designs, and makes architectural decisions.
- Do not redesign architecture unless explicitly requested.
- If modifying more than a few lines, always provide the entire file.
- Small edits (a few lines) may be provided as patches.
- Never leave ambiguity about where content belongs.

---

# Immediate Next Tasks

1. Review the generated mobile website.
2. Improve the homepage so it answers "What do I need today?"
3. Continue official attraction research.
4. Enrich each day's guide.
5. Deploy to Cloudflare Pages.
6. Test on an actual iPhone.
7. Continue refining the shared design system as a separate project.

---

# Open Questions

- Final transit strategy.
- Weekly Navigo pass vs pay-as-you-go.
- Restaurant recommendations.
- Laundry timing.
- Cloudflare deployment workflow.
- Final homepage UX.

---

# Future Ideas (Do Not Work Yet)

- Daily email briefing.
- Packing checklist.
- Weather integration.
- "I'm Done Here" navigation.
- After Action Reviews.
- Reusable Field Guide framework.

---

# Notes for Future ChatGPT

The repository structure is complete.

Do not redesign the architecture.

Do not suggest new frameworks.

Assume the current structure is intentional.

Work one task at a time.

Use Codex for repetitive implementation whenever appropriate.

ChatGPT should focus on:

- UX
- Research
- Design decisions
- Code review
- Product direction

Current priority:

Ship a polished Version 1 before departure.

---

# Session Summary

Today's accomplishments:

- Created the Paris Field Guide repository.
- Created the shared Design System repository.
- Completed the itinerary framework for every day of the trip.
- Created the research structure.
- Created logistics, tickets, itinerary, and transit documents.
- Established the shared workflow with Codex.
- Built the first Python static site generator.
- Generated the first mobile-first website.
- Tested successfully in the iOS Simulator.
- Established the design direction for both the Field Guide and future projects.

This project is now in the refinement phase rather than the planning phase.