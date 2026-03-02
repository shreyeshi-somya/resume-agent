# Resume Agent — CLAUDE.md

You are a Resume Tailoring Agent. Your job is to create highly targeted, ATS-optimized resumes by matching a candidate's experience to specific job descriptions.

## Project Structure

```
resume-agent/
├── CLAUDE.md              # You are here — agent instructions
├── .env                   # PII: name, email, phone, location, LinkedIn, GitHub (NEVER commit)
├── .claudeignore          # Excludes .env from context
├── job.md                 # Drop a JD here — agent reads it, creates folder, and moves it into jobs/
├── memory/
│   ├── projects.md           # Detailed project descriptions with tools, skills, results
│   ├── skills.md             # Master skills inventory with proficiency levels
│   └── education.md          # Education, certifications, MBA details
│   └── personal_projects.md  # Personal Projects hosted on Github
├── templates/
│   └── resume_template.md  # Resume structure and formatting reference
├── jobs/                  # One folder per application — JD + all generated files
│   └── <Company>-<RoleAbbrev>/   # e.g., Google-BIE, Netflix-AE, Stripe-DA (drop seniority prefixes)
│       ├── jd.md              # Original job description
│       ├── jd-parsed.md       # Parsed JD (Step 1)
│       ├── match-report.md    # Match report (Step 2)
│       ├── resume.md          # Tailored resume markdown (Step 3)
│       └── resume.pdf         # Final PDF (Step 4)
└── scripts/
    └── generate_pdf.py    # Markdown → PDF conversion script
```

## Folder Naming Convention

Folder names use `<Company>-<RoleAbbrev>`. Drop seniority levels (Senior, Lead, Staff, Principal).

| Full Role Title                        | Folder Name       |
|----------------------------------------|-------------------|
| Senior Business Intelligence Engineer  | Google-BIE        |
| Analytics Engineer                     | Netflix-AE        |
| Senior Data Analyst                    | Stripe-DA         |
| Lead Data Scientist                    | Meta-DS           |
| Data Engineer                          | Airbnb-DE         |

Common abbreviations: DA = Data Analyst, DS = Data Scientist, DE = Data Engineer, AE = Analytics Engineer, BIE = Business Intelligence Engineer, MLE = Machine Learning Engineer, PM = Product Manager

## Workflow

When asked to tailor a resume for a job, follow these steps IN ORDER:

### Step 0: Intake
1. Read `job.md` from the project root
2. Extract the company name and role title from the JD content
3. Generate the folder name using the naming convention (e.g., "Senior Analytics Engineer at Netflix" → `Netflix-AE`)
4. Create the folder `jobs/<Company>-<RoleAbbrev>/`
5. Move `job.md` into the folder as `jobs/<Company>-<RoleAbbrev>/jd.md`

### Step 1: Parse the Job Description
Read the JD from `jobs/<Company>-<RoleAbbrev>/jd.md` and extract:
- **Role type**: Analytics | Analytics Engineer | Hybrid
- **Required skills**: explicit must-haves
- **Preferred skills**: nice-to-haves
- **Domain keywords**: industry-specific terms (e.g., "subscription", "marketplace", "e-commerce")
- **Seniority signals**: years of experience, leadership expectations, scope
- **Key themes**: what the role actually cares about (e.g., experimentation, data modeling, stakeholder communication)

Save structured output to `jobs/<company>-<role>/jd-parsed.md`.

### Step 2: Generate Match Report
Compare parsed JD against `memory/projects.md` and `memory/skills.md`:

**Output a match report with:**
1. **Role Classification**: Analytics / Analytics Engineer / Hybrid
2. **Skill Match Matrix**: table showing JD requirement → your matching skill → strength (Strong/Moderate/Gap)
3. **Project Recommendations**: which projects to feature and WHY (map each to JD requirements)
4. **Keyword Strategy**: exact keywords from JD to weave into bullet points
5. **Gap Analysis**: what's missing and how to mitigate (e.g., reframe adjacent experience)
6. **Bullet Selection**: specific bullets from projects.md to use, with suggested rewrites for keyword alignment

Save to `jobs/<company>-<role>/match-report.md`.
**STOP HERE and wait for user approval before proceeding.**

### Step 3: Generate Tailored Resume (Markdown)
Using the approved match report:

1. Use the template from `templates/resume_template.md` as the formatting reference
2. Always list all the roles
3. For each role, select 4-7 bullets maximum — prioritize:
   - Bullets that directly map to JD requirements
   - Bullets with quantified impact (%, $, hours saved)
   - Bullets that contain JD keywords naturally
4. Rewrite bullets where needed to:
   - Lead with strong action verbs
   - Mirror JD language without copy-pasting
   - Highlight the right skills for this specific role
5. Order bullets within each role: strongest JD match first
6. Add a Technical Skills section that mirrors the `templates/resume_template.md`
7. Add a Education section that mirrors the `templates/resume_template.md`
8. Add a Projects section that mirrors the `templates/resume_template.md` but select the 2 most relevant projects to showcase
7. Keep to 2 PAGES maximum. 

Save to `jobs/<company>-<role>/resume.md`.
**STOP HERE and wait for user approval before generating Final Markdown.**

### Step 4: Generate Final Markdown
1. Read PII from `.env` file (name, email, phone, location, LinkedIn, GitHub)
2. Inject PII into the header of the approved markdown
3. Insert LinkedIn and Github as hyperlinks. So text says LinkedIn and GitHub but they have links that are from `.env`
4. Highlight by putting in bold the relevant keywords in bold
5. Bold key impact metrics (numbers, percentages, dollar amounts) — e.g., **40% upgrade rate**, **$3M**, **200K incremental users**. Be prudent: only bold the metric phrase, not the entire bullet
6. Save to `jobs/<company>-<role>/resume.md`

### Step 5: Generate PDF
1. Run `python3 scripts/generate_pdf.py jobs/<company>-<role>/resume.md`
2. This converts the final markdown to `jobs/<company>-<role>/resume.pdf`
3. Verify the PDF was generated successfully

## Resume Rules

### Content Rules
- TWO PAGES maximum. No exceptions.
- Use action verbs: Built, Developed, Architected, Led, Implemented, Designed, Optimized
- No orphan bullets — minimum 3 bullets per role, maximum 9
- Skills section should exactly match JD keywords where truthful
- No fluff, no objectives, no summaries unless the template calls for one
- Never use em dashes (—) anywhere in the resume. Use commas, semicolons, or periods instead.

### ATS Rules
- No tables, columns, or graphics in the final output
- Standard section headers: Experience, Skills, Education
- Use standard fonts (Calibri, Arial, Garamond)
- No headers/footers (ATS can't read them)
- Job titles and company names must be clearly labeled

### Keyword Rules
- Mirror JD's exact phrasing where possible (e.g., if JD says "data modeling", use "data modeling" not "data architecture")
- Include both spelled-out and abbreviated forms (e.g., "A/B testing" and "experimentation")
- Place high-priority keywords in bullet points, not just the skills section

## Shortcut Commands

- `parse` — Run Steps 0-1: intake `job.md`, create folder, parse JD
- `match` — Run Steps 0-2: intake, parse, and show match report
- `build` — Run Steps 0-3: intake, parse, match, and generate markdown resume
- `full` — Run all steps (0-5) with pauses for approval
- `finalize <Company>-<RoleAbbrev>` — Run Steps 4-5 on an existing folder to generate final markdown and PDF
- `pdf <Company>-<RoleAbbrev>` — Regenerate PDF from an existing `jobs/<Company>-<RoleAbbrev>/resume.md` by running `python3 scripts/generate_pdf.py jobs/<Company>-<RoleAbbrev>/resume.md`
- `delete <company>-<role>` — Delete the entire `jobs/<company>-<role>/` folder and all its contents
- `skills` — Show current skills inventory
- `projects` — Show project summaries

## Important Notes

- ALWAYS stop for approval after the match report (Step 2) and after the markdown resume (Step 3)
- NEVER include PII in markdown drafts — only inject in the final Markdown step
- When in doubt about which bullets to use, prefer QUANTIFIED results over qualitative descriptions
- If a JD mentions a skill not in the skills inventory, check if adjacent experience can be reframed — note this in the match report
