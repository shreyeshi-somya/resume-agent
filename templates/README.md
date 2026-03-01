# templates/

Resume formatting templates that define the structure, section order, and styling rules for generated resumes.

## What to upload

| File | Description |
|------|-------------|
| `resume_template.md` | Defines the resume layout: section order, bullet count per role, header format, and tone guidelines. The agent uses this as the formatting reference when generating tailored resumes. |

## How the agent uses these

- **Step 3 (Resume Generation)** reads the template to determine section order (Summary, Skills, Experience, Education, Projects), bullet limits per role, and formatting conventions.
- The template uses PII placeholders (`{NAME}`, `{EMAIL}`, etc.) that get replaced with real values from `.env` in the final step.
