from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

from markdown_it import MarkdownIt


@dataclass(frozen=True)
class MarkdownPage:
    source_path: Path
    title: str
    body_markdown: str
    html: str
    front_matter: dict[str, Any]


def parse_front_matter(text: str) -> tuple[dict[str, Any], str]:
    """Parse simple YAML-like front matter without adding a YAML dependency."""
    if not text.startswith("---\n"):
        return {}, text

    end_marker = text.find("\n---", 4)
    if end_marker == -1:
        return {}, text

    raw_front_matter = text[4:end_marker]
    body_start = end_marker + len("\n---")
    if text[body_start:body_start + 1] == "\n":
        body_start += 1

    return _parse_simple_yaml(raw_front_matter), text[body_start:]


def render_markdown(markdown: str) -> str:
    parser = MarkdownIt("commonmark", {"html": True, "linkify": False})
    parser.enable("table")
    return _add_external_link_attrs(parser.render(markdown))


def load_markdown_page(path: Path) -> MarkdownPage:
    raw_text = path.read_text(encoding="utf-8")
    front_matter, body_markdown = parse_front_matter(raw_text)
    html = render_markdown(body_markdown)
    title = _title_for_page(path, body_markdown, front_matter)

    return MarkdownPage(
        source_path=path,
        title=title,
        body_markdown=body_markdown,
        html=html,
        front_matter=front_matter,
    )


def _title_for_page(path: Path, markdown: str, front_matter: dict[str, Any]) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()

    title = front_matter.get("title")
    if isinstance(title, str) and title.strip():
        return title.strip()

    return path.stem.replace("-", " ").title()


def _parse_simple_yaml(raw_front_matter: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_list_key: str | None = None

    for line in raw_front_matter.splitlines():
        stripped = line.strip()
        if not stripped:
            continue

        if stripped.startswith("- ") and current_list_key:
            value = stripped[2:].strip()
            if not isinstance(data.get(current_list_key), list):
                data[current_list_key] = []
            data[current_list_key].append(value)
            continue

        current_list_key = None
        if ":" not in stripped:
            continue

        key, raw_value = stripped.split(":", 1)
        key = key.strip()
        value = raw_value.strip()

        if not value:
            data[key] = None
            current_list_key = key
            continue

        data[key] = _parse_scalar(value)

    return data


def _parse_scalar(value: str) -> Any:
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value in {"null", "Null", "~"}:
        return None
    return value.strip("\"'")


EXTERNAL_LINK_RE = re.compile(r'<a href="(https?://[^"]+)"(?![^>]*\btarget=)([^>]*)>')
MAP_HOSTS = (
    "https://www.google.com/maps/",
    "https://maps.apple.com/",
    "https://citymapper.com/",
)


def _add_external_link_attrs(html: str) -> str:
    def replace(match: re.Match[str]) -> str:
        href = match.group(1)
        rest = match.group(2)
        if href.startswith(MAP_HOSTS):
            return match.group(0)
        return f'<a href="{href}" target="_blank" rel="noopener noreferrer"{rest}>'

    return EXTERNAL_LINK_RE.sub(replace, html)
