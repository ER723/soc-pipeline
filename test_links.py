"""
Verifies every relative markdown link in this repo's docs actually
points to a file that exists. This repo has had real broken-link
issues before (a self-referential link, stale pre-rename URLs) —
this test exists specifically to catch that class of mistake
automatically, going forward.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent
MARKDOWN_FILES = list(REPO_ROOT.glob("*.md")) + list(REPO_ROOT.glob("docs/*.md"))

LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def get_relative_links(file_path):
    """Return every relative (non-http) link target found in a markdown file."""
    text = file_path.read_text(encoding="utf-8")
    links = []
    for match in LINK_PATTERN.finditer(text):
        target = match.group(2)
        if target.startswith(("http://", "https://", "#")):
            continue
        links.append(target)
    return links


def test_all_relative_links_resolve():
    broken = []
    for md_file in MARKDOWN_FILES:
        for link in get_relative_links(md_file):
            resolved = (md_file.parent / link).resolve()
            if not resolved.exists():
                broken.append(f"{md_file.relative_to(REPO_ROOT)} -> {link} (resolved to {resolved}, does not exist)")

    assert not broken, "Broken relative links found:\n" + "\n".join(broken)


if __name__ == "__main__":
    test_all_relative_links_resolve()
    print(f"Checked {len(MARKDOWN_FILES)} markdown files — all relative links resolve correctly.")
