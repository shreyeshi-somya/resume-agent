# Resume Agent

An AI-powered resume tailoring agent built with [Claude Code](https://claude.ai/claude-code). Drop in a job description, and the agent generates a targeted, ATS-optimized resume matched to the role.

## How it works

1. **Drop a JD** into `job.md` at the project root
2. **Run a command** like `match` or `full`
3. The agent **parses the JD**, extracts required skills and keywords
4. **Generates a match report** comparing the JD against your experience
5. **Builds a tailored resume** selecting the strongest bullets for that specific role
6. **Produces a PDF** ready to submit

The agent stops for your approval after the match report and after the resume draft, so you stay in control of the final output.

## Setup

### 1. Install dependencies

```bash
brew install pango          # system library required by WeasyPrint
pip3 install -r requirements.txt
```

### 2. Create your `.env` file

Create a `.env` file at the project root with your personal information:

```
NAME=Your Name
EMAIL=your@email.com
PHONE=(123) 456-7890
LOCATION=City, State
LINKEDIN_URL=https://www.linkedin.com/in/yourprofile/
GITHUB_URL=https://github.com/yourusername
```

### 3. Populate your memory files

Add your experience to the files in `memory/`:

- `projects.md` — Detailed bullet points for each role
- `skills.md` — Skills inventory with proficiency levels
- `education.md` — Degrees, certifications, coursework
- `personal_projects.md` — GitHub projects to showcase

See `memory/README.md` for details on format and content.

### 4. Run with Claude Code

```bash
claude
```

Then use shortcut commands:

| Command | What it does |
|---------|-------------|
| `parse` | Intake JD, create folder, parse requirements |
| `match` | Parse + generate match report |
| `build` | Parse + match + generate resume markdown |
| `full` | Full pipeline with approval pauses |
| `finalize <Company-Role>` | Generate final markdown with PII + PDF |
| `pdf <Company-Role>` | Regenerate PDF from existing `resume.md` |
| `delete <Company-Role>` | Remove a job application folder |

## Project structure

```
resume-agent/
├── CLAUDE.md                 # Agent instructions
├── .env                      # Your PII (not committed)
├── job.md                    # Drop a JD here to start
├── memory/                   # Your experience (skills, projects, education)
├── templates/                # Resume formatting templates
├── jobs/                     # Generated output per application
│   └── <Company>-<RoleAbbrev>/
│       ├── jd.md             # Original JD
│       ├── jd-parsed.md      # Parsed requirements
│       ├── match-report.md   # Skill match analysis
│       ├── resume.md         # Tailored resume
│       └── <Name>.pdf        # Final PDF (named from .env FULL_NAME)
└── scripts/
    └── generate_pdf.py       # Markdown to PDF converter
```

## Resume output

- ATS-friendly: no tables, columns, or graphics
- Standard fonts (Calibri/Arial)
- Bold keywords for emphasis
- Clickable LinkedIn and GitHub links
- Two pages maximum

## Customization

All agent behavior is controlled by two files — no code changes needed.

### CLAUDE.md — Agent rules

Edit `CLAUDE.md` to change how the agent builds resumes. Common tweaks:

| What to change | Where in CLAUDE.md | Default |
|---|---|---|
| Page limit | `Resume Rules > Content Rules` | 2 pages |
| Bullets per role | `Step 3` and `Content Rules` | 4-7 per role, min 3, max 9 |
| Resume sections | `Step 3` (items 6-8) | Skills, Experience, Education, Projects |
| Section order | `Step 3` | Skills > Experience > Education > Projects |
| Action verb style | `Resume Rules > Content Rules` | Built, Developed, Architected, Led, etc. |
| Keyword strategy | `Resume Rules > Keyword Rules` | Mirror JD phrasing exactly |
| Folder naming | `Folder Naming Convention` | `<Company>-<RoleAbbrev>` |

For example, to make a one-page resume, change `TWO PAGES maximum` to `ONE PAGE maximum` in Content Rules and reduce the bullet limits in Step 3.

To remove the Projects section, delete item 8 from Step 3 and remove the Projects section from the template.

### templates/resume_template.md — Resume layout

Edit the template to change the structure, section headers, or formatting conventions the agent follows. The template controls:

- Which sections appear and in what order
- Header format and PII placeholders
- Bullet count guidelines per role
- Tone and style rules

### scripts/generate_pdf.py — PDF styling

Edit the CSS in `generate_pdf.py` to change fonts, margins, font sizes, spacing, or other visual styling of the PDF output.
