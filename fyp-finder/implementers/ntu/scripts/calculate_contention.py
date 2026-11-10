#!/usr/bin/env python3
"""Calculate relative project popularity across the complete statistics dataset.

Sum choices 1-15, excluding the source Total column. Score = bids / maximum
bids across all projects (0 when all totals are zero). Labels: Uncontested
for 0, Contested for 0 < score < 0.5, Competitive for score >= 0.5.
Counts are selections, not necessarily unique students or allocation odds.

Default input: ~/fyp-finder/stats.json, otherwise stats.html in that directory.
JSON accepts a project-code-to-HTML-row mapping (19 cells: serial, code, title,
choices 1-15, Total), or an array of {projNumber, selections: [15 counts]}.
--input overrides the source. Output is JSON on stdout.
"""

import argparse
import json
from pathlib import Path

from index_projects import ProjectRows, decode_html
from project_data import DEFAULT_DIRECTORY


def calculate_contention(directory=DEFAULT_DIRECTORY, *, input_path=None):
    """Return per-project bids, normalized score, label, and display text."""
    directory = Path(directory).expanduser()
    path = Path(input_path).expanduser() if input_path else directory / "stats.json"
    if input_path is None and not path.exists():
        path = directory / "stats.html"
    if path.suffix.lower() == ".html":
        parser = ProjectRows()
        parser.feed(decode_html(path.read_bytes()))
        parser.close()
        rows = [row for row in parser.rows if row and row[0].isdigit()]
        records = []
        for row in rows:
            if len(row) != 19:
                raise ValueError("Expected 19 statistics cells per project")
            records.append((row[1], row[3:18]))
    else:
        data = json.loads(path.read_text(encoding="utf-8"))
        records = []
        if isinstance(data, dict):
            for code, row in data.items():
                if not isinstance(row, list) or len(row) != 19 or row[1] != code:
                    raise ValueError(f"Expected a 19-cell statistics row for {code}")
                records.append((code, row[3:18]))
        elif isinstance(data, list):
            for row in data:
                if not isinstance(row, dict):
                    raise ValueError("Expected project statistics objects")
                records.append((row.get("projNumber"), row.get("selections")))
        else:
            raise ValueError("Expected a statistics array or project-code mapping")

    if not records:
        raise ValueError("No project statistics found")
    totals = {}
    for code, counts in records:
        if not isinstance(code, str) or not code or code in totals:
            raise ValueError(f"Missing or duplicate project code: {code!r}")
        if not isinstance(counts, list) or len(counts) != 15:
            raise ValueError(f"Expected 15 selection quantities for {code}")
        values = []
        for count in counts:
            if type(count) is int and count >= 0:
                values.append(count)
            elif isinstance(count, str) and count.strip().isascii() and count.strip().isdigit():
                values.append(int(count))
            else:
                raise ValueError(f"Invalid selection quantity for {code}: {count!r}")
        totals[code] = sum(values)

    headers = directory / "projects.headers.json"
    if headers.exists():
        expected = {row["projNumber"] for row in json.loads(headers.read_text(encoding="utf-8"))}
        if expected - totals.keys():
            raise ValueError("Statistics omit listed projects; use the complete dataset, not a shortlist")
    maximum = max(totals.values())
    result = []
    for code, bids in totals.items():
        score = bids / maximum if maximum else 0.0
        label = "Uncontested" if bids == 0 else "Competitive" if score >= 0.5 else "Contested"
        result.append({"projNumber": code, "bids": bids, "score": score,
                       "label": label, "display": f"{label}, {bids} bids (1-15)"})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=DEFAULT_DIRECTORY)
    parser.add_argument("--input", type=Path, help="Full statistics JSON or HTML")
    args = parser.parse_args()
    try:
        result = calculate_contention(args.directory, input_path=args.input)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f"Error: {exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
