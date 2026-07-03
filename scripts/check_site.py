from __future__ import annotations

import re
import sys
from pathlib import Path


LINK_RE = re.compile(r"""(?:href|src)=["']([^"']+)["']""")
BAD_RE = re.compile(r"""(?:/Users/|localhost|127\.0\.0\.1|file://)""")


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    docs = root / "docs"
    failures: list[str] = []

    if not docs.exists():
        failures.append("docs/ does not exist. Run ./build.sh first.")
        return _finish(failures)

    html_files = sorted(docs.rglob("*.html"))
    if not html_files:
        failures.append("No HTML files found under docs/.")

    for path in html_files:
        text = path.read_text(encoding="utf-8")
        if BAD_RE.search(text):
            failures.append(f"{path.relative_to(root)} contains a local-only URL or path.")

        for raw_target in LINK_RE.findall(text):
            if _is_external_or_fragment(raw_target):
                continue

            target_path = raw_target.split("#", 1)[0]
            if not target_path:
                continue

            resolved = (path.parent / target_path).resolve()
            try:
                resolved.relative_to(docs.resolve())
            except ValueError:
                failures.append(f"{path.relative_to(root)} links outside docs/: {raw_target}")
                continue

            if not resolved.exists():
                failures.append(f"{path.relative_to(root)} has missing link: {raw_target}")

    return _finish(failures)


def _is_external_or_fragment(target: str) -> bool:
    return (
        target.startswith("#")
        or target.startswith("mailto:")
        or target.startswith("tel:")
        or "://" in target
    )


def _finish(failures: list[str]) -> int:
    if failures:
        for failure in failures:
            print(f"ERROR: {failure}", file=sys.stderr)
        return 1

    print("Generated site checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
