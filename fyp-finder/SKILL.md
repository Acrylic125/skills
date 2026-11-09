---
name: fyp-finder
description: Used when the user needs to find which FYP projects best match their needs.
---

# FYP Finder

## Workflow

1. Choose an implementer from the directories under `implementers/`. If there is only one, select it automatically. If there is more than one, ask the user which to use and wait for their answer.
2. Confirm the working directory as described below, then find projects using `implementers/{implementer}/finder.md` ([NTU finder](implementers/ntu/finder.md)).
3. Profile using `implementers/{implementer}/profile.md` ([NTU profile](implementers/ntu/profile.md)).
4. Analyse and suggest using `implementers/{implementer}/analyse.md` ([NTU analysis](implementers/ntu/analyse.md)).

Read each phase's instructions when reaching it. Pass the confirmed working directory and previous findings to the next phase. If a phase is marked as not yet implemented, report the completed artifacts and stop there.

## Existing artifacts

Before each step, check for existing artifacts. If found, show their paths and ask a multiple-choice question: **Reuse existing artifacts** or **Restart this step**. Wait for the answer; reuse skips completed work, while restart replaces that step's artifacts. Ask once per covered step.

## Working directory

Before starting, ask which directory to work in and ask the user to confirm it. Explain that this directory stores findings. Suggest the platform default:

- macOS: `~/fyp-finder`
- Windows: `%UserProfile%\Desktop`

Wait for confirmation before collecting findings. Create the confirmed directory if needed, and save the files below there.
