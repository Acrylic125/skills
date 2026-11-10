# FYP finder

Find NTU final-year projects that match your experience and goals.

## Use the skill

1. From the repository root, copy the skill into your skills directory:

   ```sh
   mkdir -p ~/.agents/skills
   cp -R fyp-finder ~/.agents/skills/
   ```

2. Start a new agent session and invoke `$fyp-finder`.
3. Confirm where to save findings. The macOS default is `~/fyp-finder`.
4. Log in to NTU when prompted. The skill uses your active browser and brings the login page to the foreground.
5. Provide your resume or links to your work, then choose your goal.

Read the recommendations directly in chat. The skill returns 15 project recommendations, groups related variants, and lists self-suggested projects separately. A separate professor sentiment table cites r/NTU posts and comments.

Your profile guides project matching:

| Input | How the skill uses it |
| --- | --- |
| Resume and work links | Records each project's or experience's problem domain, what you did, and how you did it. |
| Your goal | Matches project descriptions to familiar work, new skills, or a different field. |

Professor ratings summarize opinions in r/NTU posts and comments. Justifications cite sources and distinguish supervision feedback from teaching feedback.

| Sentiment | Evidence |
| --- | --- |
| Good | Positive remarks. |
| Bad | Negative remarks. |
| Ok | Neutral mentions. |
| N/A | Missing or inconclusive information. |

The skill requires computer-use tools, web search, and Python 3. Its scripts use only the Python standard library.

See [SKILL.md](SKILL.md) for the workflow.

## Restart from a checkpoint

On repeat runs, choose a step to restart. The skill recreates that step's artifacts and all downstream artifacts, preserving earlier findings and your source material.

| Checkpoint | Artifacts recreated |
| --- | --- |
| Find projects | Project and statistics pages, project index, and project headers. |
| Profiling | `profile.json` and your selected goal. |
| Analyse and suggest | `analysis.json` and fresh recommendation and professor sentiment tables in chat. |

`checkpoints.json` records completed steps and artifact paths in your findings directory.

## Output

Results appear in chat as three tables:

- Project recommendations, ordered by compatibility with your profile. Relevant description text is bold. Related parts or variants share a row.
- Self-suggested projects, listed separately without a ranking. These do not count toward the 15 recommendations.
- Professor sentiment, labelled **Good**, **Ok**, **Bad**, or **N/A**, with explanations and links to r/NTU posts or comments.

The Bids column sums selections across choices 1–15. The score is that total divided by the highest total across all projects.

| Label | Score |
| --- | --- |
| Uncontested | 0. |
| Contested | Above 0 and below 0.5. |
| Competitive | 0.5 or higher. |

Cells show the label and raw count, such as `Competitive, 6 bids (1-15)`. Each grouped variant keeps its own count. Missing statistics show **N/A**. These labels describe relative popularity, not allocation odds.

### Sample

This shortened example uses fictional projects and professors, with a dataset maximum of 12 bids. The example profile includes Python data pipelines and a goal of learning machine learning.

#### Project recommendations

| ID + Title | Prof | Bids | Description + Keywords | Rationale |
| --- | --- | --- | --- | --- |
| DEMO-001: Traffic prediction, part A; DEMO-002: Traffic prediction, part B | Dr Example | DEMO-001: Contested, 3 bids (1-15); DEMO-002: Competitive, 6 bids (1-15) | Build **Python data pipelines** and forecasting models. Part A covers data preparation. Part B covers prediction. Keywords: Data Analytics, Machine Learning | Builds on your pipeline experience. Part B adds machine learning to match your learning goal. |

#### Self-suggested projects

| ID + Title | Prof | Bids | Description + Keywords | Rationale |
| --- | --- | --- | --- | --- |
| DEMO-003: Self-suggested data project | Dr Sample | Uncontested, 0 bids (1-15) | Propose a project using **data engineering**. Keywords: Data Analytics | Lets you define a problem around your existing experience. |

#### Professor sentiment

| Prof | Sentiment | Justification |
| --- | --- | --- |
| Dr Example | N/A | No relevant r/NTU mentions found. |
| Dr Sample | N/A | Not enough information to classify sentiment. |
