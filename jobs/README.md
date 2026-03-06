# jobs/

Generated output folder. Each job application gets its own subfolder named `<Company>-<RoleAbbrev>` (e.g., `Google-BIE`, `Netflix-AE`).

## What goes here

Nothing needs to be uploaded manually. The agent automatically creates a subfolder for each application and populates it with:

| File | Description |
|------|-------------|
| `jd.md` | Original job description (moved from `job.md` at the root) |
| `jd-parsed.md` | Parsed JD with extracted skills, keywords, and themes |
| `match-report.md` | Skill match matrix and bullet selection strategy |
| `resume.md` | Tailored resume in markdown (final version with PII) |
| `<Name>.pdf` | PDF version of the resume, named using `FULL_NAME` from `.env` (e.g., `John_Doe.pdf`) |

## Folder naming convention

Drop seniority prefixes (Senior, Lead, Staff, Principal) and abbreviate the role:

- DA = Data Analyst, DS = Data Scientist, DE = Data Engineer
- AE = Analytics Engineer, BIE = Business Intelligence Engineer
- MLE = Machine Learning Engineer, PM = Product Manager

Examples: `Stripe-DA`, `Meta-DS`, `Airbnb-DE`
