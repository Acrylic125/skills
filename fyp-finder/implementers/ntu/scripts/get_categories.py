#!/usr/bin/env python3
"""Retrieve the distinct NTU project categories."""

from get_headers import get_headers
from project_data import DEFAULT_DIRECTORY, run_cli


def get_categories(directory=DEFAULT_DIRECTORY):
    """Return sorted, distinct categories from the saved project headers."""
    return sorted({value for header in get_headers(directory) for value in header["category"]})


if __name__ == "__main__":
    run_cli(get_categories)
