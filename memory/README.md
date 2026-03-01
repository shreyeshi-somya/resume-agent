# memory/

Source-of-truth files that describe the candidate's experience, skills, and education. The agent reads these when generating match reports and tailored resumes.

## What to upload

These files must be populated with your own information before using the agent:

| File | Required? | Description |
|------|-----------|-------------|
| `projects.md` | Yes | Detailed project descriptions with tools used, skills demonstrated, and quantified results. Each role should have bullet points the agent can select from. |
| `skills.md` | Yes | Master skills inventory organized by category (programming, pipelines, visualization, analytics, etc.) with proficiency levels. |
| `education.md` | Yes | Education history, certifications, degrees, and relevant coursework. |
| `personal_projects.md` | No | Personal/side projects hosted on GitHub with descriptions and tech stacks. If you don't have personal projects to showcase, simply don't create this file — the agent will skip the Projects section on the resume. |

## How the agent uses these

- **Match reports** compare JD requirements against `projects.md` and `skills.md` to find the strongest matches.
- **Resume generation** pulls specific bullets from `projects.md` and rewrites them to align with JD keywords.
- **Education and projects sections** are populated from `education.md` and `personal_projects.md`.

## Examples

### projects.md

```markdown
## COMPANY NAME, Location (Year - Year)
Role Title

- [Action verb] [what you built/did] using [tools/tech], resulting in [quantified impact]
- [Action verb] [what you built/did], enabling [outcome for team/stakeholders]
- [Action verb] [process/system], reducing/improving [metric] by [X]%
- ...add as many bullets as you have per role — the agent picks the best ones

## ANOTHER COMPANY, Location (Year - Year)
Role Title

- [Action verb] [what you built/did] using [tools/tech], [quantified result]
- [Action verb] [what you built/did], supporting [team/function]
```

### skills.md

```markdown
## Category 1 (e.g., Programming)
- Skill: Proficiency — brief context on what you've done with it
- Skill: Proficiency — context

## Category 2 (e.g., Tools & Platforms)
- Skill: Proficiency — context
- Skill: Proficiency — context

## Category 3 (e.g., Analytics)
- Skill: Proficiency — context
```

Proficiency levels: Expert, Advanced, Intermediate, Beginner

### education.md

```markdown
## UNIVERSITY NAME, Country (Graduation Date)
Degree in Specialization
Relevant coursework: Course 1, Course 2, Course 3
```

### personal_projects.md (optional)

```markdown
## Project Title
One-line description of what the project does.

- Built [what] using [tech stack], achieving [result or scale]
- Extended with [feature], enabling [outcome]
- github.com/yourusername/project-repo
```
