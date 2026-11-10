---
name: fyp-finder
description: Used when the user needs to find which FYP projects best match their needs.
---

# FYP Finder

## Workflow

1. Choose an implementer from the directories under `implementers/`. If there is only one, select it automatically. If there is more than one, ask the user which to use and wait for their answer.
2. Confirm the working directory as described below and select a restart checkpoint if this is a repeat run. Find projects using `implementers/{implementer}/finder.md` ([NTU finder](implementers/ntu/finder.md)).
3. Profile using `implementers/{implementer}/profile.md` ([NTU profile](implementers/ntu/profile.md)).
4. Analyse and suggest using `implementers/{implementer}/analyse.md` ([NTU analysis](implementers/ntu/analyse.md)).

Read each phase's instructions when reaching it. Pass the confirmed working directory and previous findings to the next phase. If a phase is marked as not yet implemented, report the completed artifacts and stop there.

## Checkpoints

Treat **Find projects**, **Profiling**, and **Analyse and suggest** as artifact checkpoints. After each completes, record its artifact paths and completion status in `checkpoints.json`, alongside the implementer and selected profiling goal.

On retrigger, inspect the checkpoints and existing artifacts, then ask a multiple-choice question: **Which step should restart?** Offer **Find projects**, **Profiling**, and **Analyse and suggest**, showing which artifacts each recreates. Wait for the answer.

Restart means recreating the selected step's artifacts and all downstream artifacts. Preserve and validate earlier checkpoints, skip their steps, and mark the selected and downstream checkpoints incomplete until regenerated. The selection authorizes those replacements without further reuse prompts. Preserve user-provided source material. If an earlier prerequisite is missing or invalid, offer restart choices from that step or earlier. A first run without artifacts starts at Find projects.

## Working directory

Before starting, ask which directory to work in and ask the user to confirm it. Explain that this directory stores findings. Suggest the platform default:

- macOS: `~/fyp-finder`
- Windows: `%UserProfile%\Desktop`

Wait for confirmation before collecting findings. Create the confirmed directory if needed, and save the files below there.
