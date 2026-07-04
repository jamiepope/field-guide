from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil

from generator.markdown import MarkdownPage, load_markdown_page
from generator.templates import create_environment


@dataclass(frozen=True)
class SitePaths:
    root: Path
    docs: Path
    days: Path
    templates: Path
    source_assets: Path
    generated_assets: Path


@dataclass(frozen=True)
class DayPage:
    page: MarkdownPage
    output_name: str
    href: str
    display_date: str
    display_title: str
    previous: "DayPage | None" = None
    next: "DayPage | None" = None


@dataclass(frozen=True)
class TicketItem:
    item: str
    date: str
    time: str
    status: str
    notes: str


def build_site(root: Path) -> None:
    paths = SitePaths(
        root=root,
        docs=root / "docs",
        days=root / "days",
        templates=root / "templates",
        source_assets=root / "assets",
        generated_assets=root / "docs" / "assets",
    )

    paths.docs.mkdir(exist_ok=True)
    (paths.docs / "days").mkdir(parents=True, exist_ok=True)

    environment = create_environment(paths.templates)
    day_pages = _load_day_pages(paths.days)
    ticket_items = _parse_ticket_items(paths.root / "tickets.md")

    _write_static_assets(paths)
    _write_index(paths, environment, day_pages, ticket_items)
    _write_days(paths, environment, day_pages)


def main() -> None:
    build_site(Path.cwd())


def _load_day_pages(days_dir: Path) -> list[DayPage]:
    loaded: list[DayPage] = []
    for path in sorted(days_dir.glob("*.md")):
        if path.stem == "2026-07-14":
            continue

        page = load_markdown_page(path)
        loaded.append(
            DayPage(
                page=page,
                output_name=f"{path.stem}.html",
                href=f"days/{path.stem}.html",
                display_date=path.stem,
                display_title=_day_display_title(path, page),
            )
        )

    return [
        DayPage(
            page=day.page,
            output_name=day.output_name,
            href=day.href,
            display_date=day.display_date,
            display_title=day.display_title,
            previous=loaded[index - 1] if index > 0 else None,
            next=loaded[index + 1] if index + 1 < len(loaded) else None,
        )
        for index, day in enumerate(loaded)
    ]


def _write_index(
    paths: SitePaths,
    environment,
    day_pages: list[DayPage],
    ticket_items: list[TicketItem],
) -> None:
    template = environment.get_template("index.html")
    html = template.render(
        title="Paris Field Guide",
        day_pages=day_pages,
        primary_day=day_pages[0] if day_pages else None,
        ticket_items=ticket_items,
        is_home=True,
    )
    (paths.docs / "index.html").write_text(html, encoding="utf-8")


def _write_days(paths: SitePaths, environment, day_pages: list[DayPage]) -> None:
    template = environment.get_template("day.html")
    for day in day_pages:
        html = template.render(
            title=day.page.title,
            day=day,
            day_pages=day_pages,
            is_home=False,
        )
        (paths.docs / "days" / day.output_name).write_text(html, encoding="utf-8")


def _write_static_assets(paths: SitePaths) -> None:
    if paths.generated_assets.exists():
        shutil.rmtree(paths.generated_assets)
    shutil.copytree(
        paths.source_assets,
        paths.generated_assets,
        ignore=shutil.ignore_patterns(".gitkeep"),
    )


def _day_display_title(path: Path, page: MarkdownPage) -> str:
    front_matter_date = page.front_matter.get("date")
    has_body = bool(page.body_markdown.strip())
    if front_matter_date and str(front_matter_date) != path.stem and not has_body:
        return path.stem
    return page.title


def _parse_ticket_items(path: Path) -> list[TicketItem]:
    page = load_markdown_page(path)
    rows: list[TicketItem] = []

    for line in page.body_markdown.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or "---" in stripped:
            continue

        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if cells == ["Item", "Date", "Time", "Status", "Notes"]:
            continue
        if len(cells) != 5:
            continue

        rows.append(
            TicketItem(
                item=cells[0],
                date=cells[1],
                time=cells[2],
                status=cells[3],
                notes=cells[4],
            )
        )

    return rows


if __name__ == "__main__":
    main()
