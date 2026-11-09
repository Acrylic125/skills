#!/usr/bin/env python3
"""Retrieve project headers from saved NTU projects.html for analysis.

find_headers(html) returns one object per project with projNumber: str,
title: str, category: list[str], keywords: list[str]. Array values are
deduplicated in source order. Output defaults to projects.headers.json.
"""

import argparse
import json
import re
from pathlib import Path

from index_projects import ProjectRows, decode_html


def find_headers(html):
    parser = ProjectRows()
    parser.feed(html)
    parser.close()
    projects = []
    current = None
    fields = {"project title": "title", "category": "category", "keywords": "keywords"}
    for cells in parser.rows:
        if len(cells) != 2:
            continue
        label, value = cells
        label = " ".join(label.lower().split()).rstrip(":")
        if re.fullmatch(r"(?:\d+\)\s*)?proj\s+no\.?", label):
            current = {"projNumber": value}
            projects.append(current)
        elif current is not None and label in fields:
            field = fields[label]
            if field in current:
                raise ValueError(f"Duplicate field {field} for {current['projNumber']}")
            current[field] = value
    if not projects:
        raise ValueError("No project headers found; check for a login or error page")

    headers = []
    seen = set()
    for project in projects:
        number = project["projNumber"]
        missing = {"title", "category", "keywords"} - project.keys()
        if missing:
            raise ValueError(f"Project {number}: missing fields {', '.join(sorted(missing))}")
        if not number or number in seen:
            raise ValueError(f"Empty or duplicate project number: {number!r}")
        seen.add(number)
        title = " ".join(project["title"].split())
        if not title:
            raise ValueError(f"Project {number}: empty title")
        header = {
            "projNumber": number, "title": title, "category": [], "keywords": []
        }
        for field in ("category", "keywords"):
            for value in project[field].splitlines():
                if value and value not in header[field]:
                    header[field].append(value)
        headers.append(header)
    return headers


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path, default=Path.home() / "fyp-finder" / "projects.html", help="Saved NTU projects.html; default: ~/fyp-finder/projects.html")
    parser.add_argument("--output", type=Path, help="Default: projects.headers.json beside input")
    args = parser.parse_args()
    output = args.output or args.input.with_name("projects.headers.json")
    try:
        if output.resolve() == args.input.resolve():
            raise ValueError("Output must differ from the input HTML file")
        headers = find_headers(decode_html(args.input.read_bytes()))
        output.write_text(json.dumps(headers, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError, LookupError) as exc:
        parser.exit(1, f"Error: {exc}\n")
    print(f"Retrieved {len(headers)} project headers: {output}")


if __name__ == "__main__":
    main()
