# Profiling

This checkpoint produces `profile.json` and records the selected goal in `checkpoints.json`. When restarted, initialize `profile.json` as `{"work": []}` before calling `add_work()` so previous records are replaced rather than appended. Preserve the user's resume and source links.

## Instructions
1. Call `get_keywords()` and `get_categories()` from the separate scripts in this implementer directory's `scripts/` folder.
2. Ask the user to provide their resume and/or links to their work.
3. Analyse their work. A work is a singular project or experience. For each piece of work:
   - Label it with keywords and a category using the available values from (1).
   - Answer "What is the problem domain?"
   - Answer "What was done?"
   - Answer "How was it done?"
4. For each work, call `add_work(Work)` from `scripts/add_work.py`. It creates `profile.json` if absent and appends the work; use it to persist records rather than writing the file manually. Its docstring defines the work fields. Base each record on the provided material; ask for missing details rather than inventing them.
5. Finally, ask a multiple-choice question: **What do you want out of this internship?**
   1. "I want to skive, give me projects similar to my past work."
   2. "I want to learn something new, give me projects that is similar to my past work"
   3. "I want to explore, give me projects thats totally different from what I have already done"
6. Before handing off to analysis, read `profile.json` and check that every work identified from the user's materials has been added, using its name and references to match it. Add any missing work with `add_work()` without duplicating saved records.

Wait for the answer, record it in `checkpoints.json`, and pass it alongside `profile.json` to the analysis and suggest step. Helpers default to `~/fyp-finder`; pass `directory=<working-directory>` for another confirmed directory.

## Output

`add_work()` saves `profile.json` in the confirmed working directory with this structure. References are resume file paths and/or links to the source work. Keep keyword/category labels in the profiling discussion; the file contains only these fields:

```json
{
  "work": [
    {
      "references": ["string"],
      "name": "string",
      "problemDomain": "string",
      "what": "string",
      "how": "string"
    }
  ]
}
```
