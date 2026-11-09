#!/usr/bin/env python3
"""Append one analysed project/experience to profile.json.

Profile schema: {"work": [{"references": list[str], "name": str,
"problemDomain": str, "what": str, "how": str}]}.
Each record represents a single work. References identify its source material.
add_work(work, directory=~/fyp-finder) creates profile.json if absent,
including its parent directory, and appends to the work array.
CLI: --input <work.json>, or omit --input to read a work object from stdin.
"""

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

from project_data import DEFAULT_DIRECTORY


def validate_work(work):
    if not isinstance(work, dict):
        raise ValueError("Work must be an object")
    if set(work) != {"references", "name", "problemDomain", "what", "how"}:
        raise ValueError("Work fields must be references, name, problemDomain, what, how")
    for field in ("name", "problemDomain", "what", "how"):
        if not isinstance(work.get(field), str) or not work[field].strip():
            raise ValueError(f"Work.{field} must be a nonempty string")
    references = work.get("references")
    if not isinstance(references, list) or any(
        not isinstance(value, str) or not value.strip() for value in references
    ):
        raise ValueError("Work.references must be an array of nonempty strings")


def add_work(work, directory=DEFAULT_DIRECTORY):
    """Validate and append a Work object; return the updated profile."""
    validate_work(work)
    path = Path(directory).expanduser() / "profile.json"
    profile = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"work": []}
    if not isinstance(profile, dict) or set(profile) != {"work"} or not isinstance(profile["work"], list):
        raise ValueError("profile.json must be an object containing only a work array")
    for existing in profile["work"]:
        validate_work(existing)
    profile["work"].append(work)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         delete=False) as output:
            temporary = Path(output.name)
            output.write(json.dumps(profile, ensure_ascii=False, indent=2) + "\n")
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return profile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="Work JSON file; default: stdin")
    parser.add_argument("--directory", type=Path, default=DEFAULT_DIRECTORY,
                        help="Profile directory; default: ~/fyp-finder")
    args = parser.parse_args()
    try:
        work = json.loads(args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read())
        profile = add_work(work, args.directory)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Error: {exc}\n")
    print(json.dumps(profile, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
