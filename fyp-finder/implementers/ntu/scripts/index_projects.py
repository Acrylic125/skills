#!/usr/bin/env python3
"""Extract a saved NTU project listing into a JSON index; standard library only.

Output: projects.index.json, an array of objects with string fields projNumber,
supervisor, summary, category, type, and a keywords array of strings.
Preserve the full source summary and extract keywords from source entries.
"""

import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path


FIELDS = {
    "supervisor": "supervisor",
    "project summary": "summary",
    "category": "category",
    "type": "type",
    "keywords": "keywords",
}


def clean(text):
    return "\n".join(" ".join(line.split()) for line in text.splitlines()).strip()


class ProjectRows(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows = []
        self.cells = None
        self.parts = None
        self.ignored = 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.ignored += 1
        if tag == "tr":
            self.cells = []
        elif tag in {"td", "th"} and self.cells is not None:
            self.parts = []
        elif tag in {"br", "p", "div", "li"} and self.parts is not None:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in {"script", "style"}:
            self.ignored = max(0, self.ignored - 1)
        if tag in {"td", "th"} and self.parts is not None:
            self.cells.append(clean("".join(self.parts)))
            self.parts = None
        elif tag == "tr" and self.cells is not None:
            self.rows.append(self.cells)
            self.cells = None
        elif tag in {"p", "div", "li"} and self.parts is not None:
            self.parts.append("\n")

    def handle_data(self, data):
        if self.parts is not None and not self.ignored:
            # Source formatting whitespace is inline; HTML elements define breaks.
            self.parts.append(re.sub(r"\s+", " ", data))


def decode_html(raw):
    # Browser saves may be UTF-8 despite retaining the original charset tag.
    try:
        return raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        charset = re.search(br"charset\s*=\s*[\"']?([\w-]+)", raw[:4096], re.I)
        return raw.decode(charset[1].decode("ascii") if charset else "windows-1252")


def extract_projects(html):
    parser = ProjectRows()
    parser.feed(html)
    parser.close()
    projects = []
    current = None
    for cells in parser.rows:
        if len(cells) != 2:
            continue
        label, value = cells
        label = " ".join(label.lower().split()).rstrip(":")
        if re.fullmatch(r"(?:\d+\)\s*)?proj\s+no\.?", label):
            current = {"projNumber": value}
            projects.append(current)
        elif current is not None and label in FIELDS:
            field = FIELDS[label]
            if field in current:
                raise ValueError(f"Duplicate field {field} for {current['projNumber']}")
            current[field] = (
                [line.strip() for line in value.splitlines() if line.strip()]
                if field == "keywords" else value
            )
    if not projects:
        raise ValueError("No project records found; check for a login or error page")
    seen = set()
    required = {"projNumber", *FIELDS.values()}
    for project in projects:
        number = project["projNumber"]
        missing = required - project.keys()
        if missing:
            raise ValueError(f"Project {number}: missing fields {', '.join(sorted(missing))}")
        if not number or number in seen:
            raise ValueError(f"Empty or duplicate project number: {number!r}")
        seen.add(number)
    return projects


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path, default=Path.home() / "fyp-finder" / "projects.html", help="Saved NTU projects.html; default: ~/fyp-finder/projects.html")
    parser.add_argument("--output", type=Path, help="Default: projects.index.json beside input")
    args = parser.parse_args()
    output = args.output or args.input.with_name("projects.index.json")
    try:
        if output.resolve() == args.input.resolve():
            raise ValueError("Output must differ from the input HTML file")
        projects = extract_projects(decode_html(args.input.read_bytes()))
        output.write_text(json.dumps(projects, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError, LookupError) as exc:
        parser.exit(1, f"Error: {exc}\n")
    print(f"Indexed {len(projects)} projects: {output}")


if __name__ == "__main__":
    main()
