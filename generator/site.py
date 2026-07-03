from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from generator.assets import STYLE_CSS
from generator.markdown import MarkdownPage, load_markdown_page
from generator.templates import create_environment


ROOT_PAGES = [
    "README.md",
    "itinerary.md",
    "logistics.md",
    "tickets.md",
    "transit-ledger.md",
]


@dataclass(frozen=True)
class SitePaths:
    root: Path
    docs: Path
    days: Path
    templates: Path
    assets: Path


@dataclass(frozen=True)
class DayPage:
    page: MarkdownPage
    output_name: str
    href: str
    previous: "DayPage | None" = None
    next: "DayPage | None" = None


def build_site(root: Path) -> None:
    paths = SitePaths(
        root=root,
        docs=root / "docs",
        days=root / "days",
        templates=root / "templates",
        assets=root / "docs" / "assets",
    )

    paths.docs.mkdir(exist_ok=True)
    (paths.docs / "days").mkdir(parents=True, exist_ok=True)
    paths.assets.mkdir(parents=True, exist_ok=True)

    environment = create_environment(paths.templates)
    root_pages = [load_markdown_page(paths.root / name) for name in ROOT_PAGES]
    day_pages = _load_day_pages(paths.days)

    _write_static_assets(paths)
    _write_index(paths, environment, root_pages, day_pages)
    _write_days(paths, environment, day_pages)


def main() -> None:
    build_site(Path.cwd())


def _load_day_pages(days_dir: Path) -> list[DayPage]:
    loaded = [
        DayPage(
            page=load_markdown_page(path),
            output_name=f"{path.stem}.html",
            href=f"days/{path.stem}.html",
        )
        for path in sorted(days_dir.glob("*.md"))
    ]

    return [
        DayPage(
            page=day.page,
            output_name=day.output_name,
            href=day.href,
            previous=loaded[index - 1] if index > 0 else None,
            next=loaded[index + 1] if index + 1 < len(loaded) else None,
        )
        for index, day in enumerate(loaded)
    ]


def _write_index(
    paths: SitePaths,
    environment,
    root_pages: list[MarkdownPage],
    day_pages: list[DayPage],
) -> None:
    template = environment.get_template("index.html")
    html = template.render(
        title="Paris Field Guide",
        root_pages=root_pages,
        day_pages=day_pages,
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
    (paths.assets / "style.css").write_text(STYLE_CSS, encoding="utf-8")


if __name__ == "__main__":
    main()
