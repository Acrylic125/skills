"""Shared local artifact loading and JSON CLI for NTU query helpers."""

import argparse
import json
from pathlib import Path


DEFAULT_DIRECTORY = Path.home() / "fyp-finder"


def load_artifact(filename, directory=DEFAULT_DIRECTORY):
    path = Path(directory).expanduser() / filename
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or any(not isinstance(item, dict) for item in data):
        raise ValueError(f"Expected a JSON array of objects in {path}")
    return data


def run_cli(function, *, project=False):
    parser = argparse.ArgumentParser(description=function.__doc__)
    parser.add_argument("--directory", type=Path, default=DEFAULT_DIRECTORY,
                        help="Artifact directory; default: ~/fyp-finder")
    if project:
        parser.add_argument("projectCode", help="Project number, e.g. CCDS26-0962")
    args = parser.parse_args()
    try:
        data = (function(args.projectCode, directory=args.directory) if project
                else function(directory=args.directory))
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f"Error: {exc}\n")
    print(json.dumps(data, ensure_ascii=False, indent=2))
