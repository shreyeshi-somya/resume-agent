#!/usr/bin/env python3
"""Convert a resume markdown file to a clean, ATS-friendly PDF using WeasyPrint."""

import ctypes.util
import os
import sys
import re
from pathlib import Path

# WeasyPrint needs Homebrew's native libs (pango, gobject, etc.) on macOS.
# The system Python can't find them automatically, so we patch the lookup.
_brew_lib = "/opt/homebrew/lib"
if os.path.isdir(_brew_lib):
    _orig_find = ctypes.util.find_library

    def _patched_find_library(name):
        result = _orig_find(name)
        if result:
            return result
        # Try Homebrew lib directory directly
        for suffix in (".dylib",):
            for candidate in (
                os.path.join(_brew_lib, f"lib{name}{suffix}"),
                os.path.join(_brew_lib, f"{name}{suffix}"),
            ):
                if os.path.isfile(candidate):
                    return candidate
        return None

    ctypes.util.find_library = _patched_find_library

import markdown
from weasyprint import HTML


CSS = """
@page {
    size: Letter;
    margin: 0.2in;
}

body {
    font-family: Calibri, Arial, Helvetica, sans-serif;
    font-size: 10.5pt;
    line-height: 1.3;
    color: #000;
    margin: 0;
    padding: 0;
}

/* ── Header / Contact ── */
.header {
    text-align: center;
    margin-bottom: 6pt;
}

.header h1 {
    font-size: 20pt;
    font-weight: bold;
    margin: 0 0 2pt 0;
    letter-spacing: 1pt;
}

.header p {
    font-size: 10pt;
    margin: 0;
    color: #333;
}

.header a {
    color: #1a0dab;
    text-decoration: none;
}

/* ── Section Headers ── */
h2 {
    font-size: 11pt;
    font-weight: bold;
    text-transform: uppercase;
    border-bottom: 1.2pt solid #000;
    padding-bottom: 2pt;
    margin: 10pt 0 6pt 0;
    letter-spacing: 0.5pt;
}

/* ── Experience blocks ── */
.company-line {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin: 6pt 0 0 0;
    font-size: 10.5pt;
}

.company-line .company {
    font-weight: bold;
}

.company-line .dates {
    font-weight: normal;
    white-space: nowrap;
}

.role-title {
    font-style: italic;
    margin: 0 0 2pt 0;
    font-size: 10.5pt;
}

/* ── Education blocks ── */
.edu-line {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin: 6pt 0 0 0;
    font-size: 10.5pt;
}

.edu-line .school {
    font-weight: bold;
}

.edu-line .dates {
    font-weight: normal;
    white-space: nowrap;
}

.degree {
    font-style: italic;
    margin: 0;
    font-size: 10.5pt;
}

.coursework {
    margin: 0 0 2pt 0;
    font-size: 10pt;
    color: #333;
}

/* ── Project blocks ── */
.project-title {
    font-weight: bold;
    margin: 6pt 0 1pt 0;
    font-size: 10.5pt;
}

.project-title span {
    font-weight: normal;
}

/* ── Bullet lists ── */
ul {
    margin: 1pt 0 2pt 0;
    padding-left: 16pt;
}

li {
    margin: 1pt 0;
    line-height: 1.3;
    font-size: 10.5pt;
}

/* ── Skills section ── */
.skills-section ul {
    list-style: none;
    padding-left: 0;
    margin: 2pt 0;
}

.skills-section li {
    margin: 1pt 0;
}

/* ── Summary paragraph ── */
.summary {
    margin: 4pt 0 2pt 0;
    text-align: justify;
    font-size: 10.5pt;
    line-height: 1.35;
}

/* ── Links ── */
a {
    color: #1a0dab;
    text-decoration: none;
}

/* ── Bold keywords ── */
strong {
    font-weight: bold;
}

/* ── Misc ── */
p {
    margin: 2pt 0;
}

hr {
    display: none;
}
"""


def parse_resume_md(md_text: str) -> str:
    """Parse the resume markdown into structured HTML with semantic classes."""

    lines = md_text.strip().split("\n")
    html_parts: list[str] = []
    i = 0

    # ── Header: parse <center> block ──
    if lines[i].strip() == "<center>":
        i += 1
        # skip blank lines
        while i < len(lines) and not lines[i].strip():
            i += 1
        # name line
        name = lines[i].strip()
        i += 1
        # skip blank lines
        while i < len(lines) and not lines[i].strip():
            i += 1
        # contact line
        contact = lines[i].strip()
        i += 1
        # skip to </center>
        while i < len(lines) and lines[i].strip() != "</center>":
            i += 1
        i += 1  # skip </center>

        # convert markdown links in contact line to HTML
        contact_html = markdown.markdown(contact).replace("<p>", "").replace("</p>", "")

        html_parts.append(
            f'<div class="header">'
            f"<h1>{name}</h1>"
            f"<p>{contact_html}</p>"
            f"</div>"
        )

    # skip blank lines after header
    while i < len(lines) and not lines[i].strip():
        i += 1

    # ── Summary paragraph (text before first ##) ──
    summary_lines: list[str] = []
    while i < len(lines) and not lines[i].startswith("## "):
        if lines[i].strip():
            summary_lines.append(lines[i].strip())
        i += 1

    if summary_lines:
        summary_md = " ".join(summary_lines)
        summary_html = markdown.markdown(summary_md)
        html_parts.append(f'<div class="summary">{summary_html}</div>')

    # ── Sections ──
    while i < len(lines):
        line = lines[i]

        # Section header
        if line.startswith("## "):
            section_name = line[3:].strip()
            html_parts.append(f"<h2>{section_name}</h2>")
            i += 1

            if "SKILL" in section_name.upper():
                html_parts.append(_parse_skills(lines, i))
                i = _skip_section(lines, i)

            elif "EXPERIENCE" in section_name.upper():
                exp_html, i = _parse_experience(lines, i)
                html_parts.append(exp_html)

            elif "EDUCATION" in section_name.upper():
                edu_html, i = _parse_education(lines, i)
                html_parts.append(edu_html)

            elif "PROJECT" in section_name.upper():
                proj_html, i = _parse_projects(lines, i)
                html_parts.append(proj_html)

            else:
                # Generic section: just render as markdown
                section_lines: list[str] = []
                while i < len(lines) and not lines[i].startswith("## "):
                    section_lines.append(lines[i])
                    i += 1
                html_parts.append(markdown.markdown("\n".join(section_lines)))
        else:
            i += 1

    return "\n".join(html_parts)


def _skip_section(lines: list[str], i: int) -> int:
    """Advance index past the current section."""
    while i < len(lines) and not lines[i].startswith("## "):
        i += 1
    return i


def _parse_skills(lines: list[str], i: int) -> str:
    """Parse skills section into a clean list."""
    items: list[str] = []
    while i < len(lines) and not lines[i].startswith("## "):
        line = lines[i].strip()
        if line.startswith("- "):
            item_html = markdown.markdown(line[2:]).replace("<p>", "").replace("</p>", "")
            items.append(f"<li>{item_html}</li>")
        i += 1
    return f'<div class="skills-section"><ul>{"".join(items)}</ul></div>'


def _parse_experience(lines: list[str], start: int) -> tuple[str, int]:
    """Parse experience section with company/date alignment."""
    html_parts: list[str] = []
    i = start

    while i < len(lines) and not lines[i].startswith("## "):
        line = lines[i].strip()

        # Company line: **COMPANY**, Location  <spaces>  dates
        company_match = re.match(
            r"^\*\*(.+?)\*\*,\s*(.+?)\s{2,}(\S.*\S)\s*$", line
        )
        if company_match:
            company = company_match.group(1)
            location = company_match.group(2).strip()
            dates = company_match.group(3).strip()
            html_parts.append(
                f'<div class="company-line">'
                f'<span class="left"><span class="company">{company}</span>, {location}</span>'
                f'<span class="dates">{dates}</span>'
                f"</div>"
            )
            i += 1
            # Next non-blank line is the role title
            while i < len(lines) and not lines[i].strip():
                i += 1
            if i < len(lines) and not lines[i].startswith("## ") and not lines[i].startswith("- ") and not re.match(r"^\*\*", lines[i].strip()):
                html_parts.append(f'<div class="role-title">{lines[i].strip()}</div>')
                i += 1
            continue

        # Bullet point
        if line.startswith("- "):
            bullets: list[str] = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                bullet_text = lines[i].strip()[2:]
                bullet_html = markdown.markdown(bullet_text).replace("<p>", "").replace("</p>", "")
                bullets.append(f"<li>{bullet_html}</li>")
                i += 1
            html_parts.append(f'<ul>{"".join(bullets)}</ul>')
            continue

        i += 1

    return "\n".join(html_parts), i


def _parse_education(lines: list[str], start: int) -> tuple[str, int]:
    """Parse education section with school/date alignment."""
    html_parts: list[str] = []
    i = start

    while i < len(lines) and not lines[i].startswith("## "):
        line = lines[i].strip()

        # School line: **UNIVERSITY**, Location  <spaces>  date
        edu_match = re.match(
            r"^\*\*(.+?)\*\*,\s*(.+?)\s{2,}(\S.*\S)\s*$", line
        )
        if edu_match:
            school = edu_match.group(1)
            location = edu_match.group(2).strip()
            dates = edu_match.group(3).strip()
            html_parts.append(
                f'<div class="edu-line">'
                f'<span class="left"><span class="school">{school}</span>, {location}</span>'
                f'<span class="dates">{dates}</span>'
                f"</div>"
            )
            i += 1
            # Degree line
            while i < len(lines) and not lines[i].strip():
                i += 1
            if i < len(lines) and not lines[i].startswith("## ") and not lines[i].startswith("**"):
                degree_html = markdown.markdown(lines[i].strip()).replace("<p>", "").replace("</p>", "")
                html_parts.append(f'<div class="degree">{degree_html}</div>')
                i += 1
            # Coursework line
            while i < len(lines) and not lines[i].strip():
                i += 1
            if i < len(lines) and not lines[i].startswith("## ") and not lines[i].startswith("**"):
                html_parts.append(f'<div class="coursework">{lines[i].strip()}</div>')
                i += 1
            continue

        i += 1

    return "\n".join(html_parts), i


def _parse_projects(lines: list[str], start: int) -> tuple[str, int]:
    """Parse projects section."""
    html_parts: list[str] = []
    i = start

    while i < len(lines) and not lines[i].startswith("## "):
        line = lines[i].strip()

        # Project title: **Title** — Description
        proj_match = re.match(r"^\*\*(.+?)\*\*\s*[—–-]\s*(.+)$", line)
        if proj_match:
            title = proj_match.group(1)
            desc = proj_match.group(2)
            html_parts.append(
                f'<div class="project-title">{title} <span>— {desc}</span></div>'
            )
            i += 1
            # Bullets
            bullets: list[str] = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                bullet_text = lines[i].strip()[2:]
                # Check if it's a bare URL (github link)
                if re.match(r"^https?://", bullet_text) or re.match(r"^github\.com/", bullet_text):
                    url = bullet_text if bullet_text.startswith("http") else f"https://{bullet_text}"
                    bullets.append(f'<li><a href="{url}">{bullet_text}</a></li>')
                else:
                    bullet_html = markdown.markdown(bullet_text).replace("<p>", "").replace("</p>", "")
                    bullets.append(f"<li>{bullet_html}</li>")
                i += 1
            if bullets:
                html_parts.append(f'<ul>{"".join(bullets)}</ul>')
            continue

        i += 1

    return "\n".join(html_parts), i


def build_html(body: str) -> str:
    """Wrap parsed body HTML in a full document with CSS."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>{CSS}</style>
</head>
<body>
{body}
</body>
</html>"""


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/generate_pdf.py <path-to-resume.md>")
        sys.exit(1)

    md_path = Path(sys.argv[1])
    if not md_path.exists():
        print(f"Error: {md_path} not found")
        sys.exit(1)

    pdf_path = md_path.parent / "resume.pdf"

    md_text = md_path.read_text(encoding="utf-8")
    body_html = parse_resume_md(md_text)
    full_html = build_html(body_html)

    HTML(string=full_html).write_pdf(str(pdf_path))
    print(f"PDF generated: {pdf_path}")


if __name__ == "__main__":
    main()
