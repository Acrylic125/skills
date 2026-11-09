#!/usr/bin/env python3
"""Retrieve an NTU project's full indexed details by project code."""

from project_data import DEFAULT_DIRECTORY, load_artifact, run_cli


def get_project(projectCode, directory=DEFAULT_DIRECTORY):
    """Return the full projects.index.json record matching projectCode."""
    for project in load_artifact("projects.index.json", directory):
        if project["projNumber"] == projectCode:
            return project
    raise ValueError(f"Project not found: {projectCode}")


if __name__ == "__main__":
    run_cli(get_project, project=True)
