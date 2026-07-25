

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(
    filename,
    ats_score,
    matched_skills,
    missing_skills,
    cover_letter,
    linkedin_summary,
    ai_insights,
    candidate_email=None,
):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("AI Resume Analysis Report", styles["Title"]))
    story.append(Spacer(1, 12))

    story.append(
        Paragraph(f"<b>ATS Score:</b> {ats_score}/100", styles["Normal"])
    )
    story.append(Spacer(1, 12))

    if candidate_email:
        story.append(
            Paragraph(
                f"<b>Candidate Email:</b> {candidate_email}",
                styles["Normal"]
            )
        )
    story.append(Spacer(1, 12))


    matched = (
            ", ".join(matched_skills)
            if isinstance(matched_skills, list)
            else str(matched_skills)
        )

    story.append(
            Paragraph(
                f"<b>Matched Skills:</b> {matched}",
                styles["Normal"],
            )
        )
    
    story.append(Spacer(1, 12))

    missing = (
    ", ".join(missing_skills)
    if isinstance(missing_skills, list)
    else str(missing_skills)
    )

    story.append(
    Paragraph(
        f"<b>Missing Skills:</b> {missing}",
        styles["Normal"],
        )
    )
    story.append(Spacer(1, 12))

    story.append(
        Paragraph("<b>Cover Letter</b>", styles["Heading2"])
    )
    story.append(
        Paragraph(
            cover_letter.replace("\n", "<br/>"),
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 12))

    story.append(
        Paragraph("<b>LinkedIn Summary</b>", styles["Heading2"])
    )
    story.append(
        Paragraph(
            linkedin_summary.replace("\n", "<br/>"),
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 12))

    story.append(
        Paragraph("<b>AI Insights</b>", styles["Heading2"])
    )
    story.append(
        Paragraph(
            ai_insights.replace("\n", "<br/>"),
            styles["Normal"],
        )
    )

    doc.build(story)
