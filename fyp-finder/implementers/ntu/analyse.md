# Analyse and Suggest

Read `profile.json` from the confirmed working directory as the user's profile. Its `work` array records each experience's references, name, problem domain, what was done, and how. Use it together with the user's selected goal from profiling.

## Instructions
1. Query the project headers, keywords, and categories using `get_headers()`, `get_keywords()` and `get_categories()` from `scripts` in this implementer directory.
2. Using the information gathered in (1), find a set of keywords, categories, and other possible useful search terms to filter down the projects by, to match projects by the **user's profile**. Write a temporary python script to do this filtering.
3. Out of this filtered subset, use `get_project(projectCode)` to read the full detail of each filtered project.
4. Produce 15 distinct main-table recommendations based on the **user's profile**, ordered by compatibility. Apply the grouping rules below before counting: each group counts as one recommendation. Self-suggested projects are additional, unranked entries and do not count toward the 15. If fewer than 15 candidates remain, scope down the restrictive search criteria by relaxing filters and querying again. Each such adjustment and re-query is a **revision turn**. Read the full details of newly included candidates before evaluating their compatibility. Continue until there are 15 recommendations or all available projects have been considered; report any shortfall.

5. Do one additional web-search pass for every distinct professor in the recommendations, including self-suggested projects and grouped variants. Follow the professor sentiment instructions below, then report the recommendations.

## Professor sentiment

Search for each professor's name and common name variants on Reddit's **r/NTU** (for example, `site:reddit.com/r/NTU "<professor name>"`). Read relevant posts and comments, confirm they refer to the same professor, and classify the sentiment:

- **N/A** — not enough information, including no relevant mentions or inaccessible evidence.
- **Bad** — the professor was mentioned with negative remarks.
- **Ok** — the professor was mentioned without positive or negative remarks.
- **Good** — the professor was mentioned with positive remarks.

For mixed remarks, briefly describe both sides and choose the label best supported overall; use **N/A** if the evidence does not support a clear classification. **Ok** means neutral mentions, not missing evidence. Distinguish FYP supervision experiences from teaching feedback and include post/comment dates for context. Describe remarks as Reddit users' opinions, not established facts about the professor.

After the project recommendation tables, report professor ratings directly in chat as a separate table with one row per distinct professor:

```md
| Prof | Sentiment | Justification |
| --- | --- | --- |
| <professor name> | <N/A, Bad, Ok, or Good> | <brief explanation with dates and direct links to supporting r/NTU posts/comments> |
```

For **N/A**, state the information gap rather than inventing a source. Keep only professor names in the project tables' **Prof** column.

## Output format

Report the results directly in chat as tables, rather than creating a Markdown report file. Order main-table rows by compatibility without a Rank column or numbered entries. Keep self-suggested projects outside this ordering. Use the project ID, title, and keywords from its header and the supervisor and description from its full details. Bold the parts of the description relevant to the user's profile. In the rationale, explain the match to specific past work and the user's selected goal.

- Put projects explicitly marked **Self suggested** in a separate **Self-suggested projects** table, using the same columns. Recognize capitalization and hyphenation variations. Keep this table unranked and separate from the main recommendations; omit it when there are no self-suggested recommendations.
- Group multiple parts or variants of the same project into one row within the appropriate table. Confirm the relationship from their titles and full descriptions; a shared topic alone is insufficient. List every included ID and its part/variant title in **ID + Title**, preserve supervisor associations, and summarize meaningful differences in **Description + Keywords**. Explain which part or variant best matches the profile in **Rationale**.
- Grouping is for presentation only: keep each project's original ID and individual source record.

```md
| ID + Title | Prof | Description + Keywords | Rationale |
| --- | --- | --- | --- |
| <project ID> — <title> | <prof> | <description with relevant parts bolded>; Keywords: <keywords> | <profile compatibility and goal fit> |
```

Each helper is in its own matching `.py` script. Functions default to `~/fyp-finder`; pass `directory=<working-directory>` for another confirmed directory. Scripts accept `--directory` and print JSON to stdout; `get_project.py` also requires a project code.
