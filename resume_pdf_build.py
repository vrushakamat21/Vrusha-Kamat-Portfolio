from html import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


OUTPUT_PATH = "assets/resume.pdf"
TEAL = colors.HexColor("#17695f")
NAVY = colors.HexColor("#173e55")
TEXT = colors.HexColor("#27343a")
MUTED = colors.HexColor("#586970")
RULE = colors.HexColor("#a9c2bf")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="ResumeName", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=21, leading=23, textColor=NAVY, alignment=TA_CENTER, spaceAfter=2,
))
styles.add(ParagraphStyle(
    name="ResumeRole", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=9, leading=11, textColor=TEAL, alignment=TA_CENTER, spaceAfter=5,
))
styles.add(ParagraphStyle(
    name="ResumeContact", parent=styles["Normal"], fontName="Helvetica",
    fontSize=7, leading=9, textColor=MUTED, alignment=TA_CENTER,
))
styles.add(ParagraphStyle(
    name="ResumeSection", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=8.2, leading=9.5, textColor=TEAL, spaceBefore=4, spaceAfter=2,
))
styles.add(ParagraphStyle(
    name="ResumeBody", parent=styles["Normal"], fontName="Helvetica",
    fontSize=7.8, leading=9.4, textColor=TEXT, spaceAfter=1,
))
styles.add(ParagraphStyle(
    name="ResumeSmall", parent=styles["Normal"], fontName="Helvetica",
    fontSize=7.3, leading=8.8, textColor=TEXT, spaceAfter=0.5,
))
styles.add(ParagraphStyle(
    name="ResumeDate", parent=styles["Normal"], fontName="Helvetica",
    fontSize=7.3, leading=8.8, textColor=MUTED, alignment=2,
))


def paragraph(text, style="ResumeBody"):
    return Paragraph(text, styles[style])


def section(title, contents):
    return [
        paragraph(escape(title.upper()), "ResumeSection"),
        HRFlowable(width="100%", thickness=0.55, color=RULE, spaceBefore=0, spaceAfter=3),
        *contents,
    ]


def education_entry(title, years, detail):
    row = Table(
        [[paragraph(f"<b>{escape(title)}</b>", "ResumeBody"), paragraph(escape(years), "ResumeDate")]],
        colWidths=[143 * mm, 27 * mm],
    )
    row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return [row, paragraph(escape(detail), "ResumeSmall")]


story = [
    paragraph("Vrusha Kamat", "ResumeName"),
    paragraph("B.E. Computer Science &amp; Engineering Student · Aspiring Developer", "ResumeRole"),
    paragraph(
        '<link href="mailto:vrushakamat06@gmail.com">vrushakamat06@gmail.com</link> '
        '· +91 9535421486 · '
        '<link href="https://linkedin.com/in/vrusha-kamat-525253396">LinkedIn</link> · '
        '<link href="https://github.com/vrushakamat21">GitHub</link> · Mangalore, India',
        "ResumeContact",
    ),
    HRFlowable(width="100%", thickness=1.3, color=TEAL, spaceBefore=5, spaceAfter=3),
]

story += section("Profile", [paragraph(
    "Computer Science &amp; Engineering student at Canara Engineering College developing practical skills through a Synent Technologies internship, coursework, and hands-on projects. Interested in web development and AI/ML.",
    "ResumeSmall",
)])

story += section("Education", [
    *education_entry("B.E. Computer Science & Engineering · Canara Engineering College", "2024–2028", "Current SGPA: 8.5"),
    *education_entry("Pre-University Course (Science) · Creative PU College", "2022–2024", "93%"),
    *education_entry("School Education (CBSE) · Kendriya Vidyalaya", "2012–2022", "89%"),
])

skill_rows = [
    [paragraph("<b>Programming:</b> Java 65%, Python 55%, C 55%", "ResumeSmall"), paragraph("<b>Frontend:</b> HTML 80%, CSS 75%, JavaScript 60%", "ResumeSmall")],
    [paragraph("<b>Backend:</b> Python, Flask, Java", "ResumeSmall"), paragraph("<b>Databases:</b> MySQL / SQL 65%, MongoDB 45%", "ResumeSmall")],
    [paragraph("<b>Tools:</b> Git &amp; GitHub 65%, VS Code 80%, Linux CLI 45%", "ResumeSmall"), paragraph("<b>AI/ML:</b> Machine Learning 45%, Computer Vision / YOLO 40%, NumPy / Pandas 40%", "ResumeSmall")],
]
skill_table = Table(skill_rows, colWidths=[85 * mm, 85 * mm])
skill_table.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ("TOPPADDING", (0, 0), (-1, -1), 1),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
]))
story += section("Skills", [skill_table])

story += section("Projects · Synent Technologies", [
    paragraph('<b>APIverse:</b> Integrated live weather and forecasts with GitHub profile search and daily quotes using APIs.', "ResumeSmall"),
    paragraph('<b>Velora:</b> Responsive fragrance storefront with browsable collections, category filters, and scent customization.', "ResumeSmall"),
    paragraph('<b>TaskFlow:</b> Task organizer with categories, priority highlights, due reminders, completion tracking, and quick notes.', "ResumeSmall"),
])

story += section("Experience & Achievements", [
    paragraph('<b>Internship · Synent Technologies:</b> Completed three hands-on projects spanning API integration, responsive web design, and task management.', "ResumeSmall"),
    paragraph('<b>Buildathon 2025:</b> Participated and received a certificate from the Canara Student Open Source Community.', "ResumeSmall"),
    paragraph('<b>ElectroHack 4.0:</b> Participated in a 24-hour national-level software and hardware hackathon at KS Institute of Technology, 25–26 September 2026.', "ResumeSmall"),
    paragraph('Continuously developing technical skills through projects, experimentation, and hands-on learning.', "ResumeSmall"),
])

story += section("MongoDB Certificates", [paragraph(
    "MongoDB Basics for Students · AI Data Strategy with MongoDB · RAG with MongoDB · Vector Search Fundamentals · AI Agents with MongoDB",
    "ResumeSmall",
)])

document = SimpleDocTemplate(
    OUTPUT_PATH,
    pagesize=A4,
    rightMargin=20 * mm,
    leftMargin=20 * mm,
    topMargin=12 * mm,
    bottomMargin=12 * mm,
    title="Vrusha Kamat - Resume",
    author="Vrusha Kamat",
)
document.build(story)