#!/usr/bin/env python3
"""Retrieve saved NTU project headers."""

from project_data import DEFAULT_DIRECTORY, load_artifact, run_cli


def get_headers(directory=DEFAULT_DIRECTORY):
    """Return project headers from projects.headers.json."""
    return load_artifact("projects.headers.json", directory)


if __name__ == "__main__":
    run_cli(get_headers)
