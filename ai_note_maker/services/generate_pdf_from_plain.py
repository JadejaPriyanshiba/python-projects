import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from PyPDF2 import PdfMerger
def format_text(text):

    # Escape special HTML characters
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    # Bold for "quoted text"
    text = re.sub(r'"(.*?)"', r'<b>\1</b>', text)

    # Gray color for `code-like text`
    text = re.sub(r'`(.*?)`', r'<font color="#666666">\1</font>', text)

    # Handle bullet points starting with -
    lines = text.split('\n')
    formatted_lines = []
    for line in lines:
        if line.strip().startswith("-"):
            bullet = "&bull;"  # Unicode bullet
            content = line.strip()[1:].strip()
            formatted_line = f"&nbsp;&nbsp;&nbsp;&nbsp;{bullet} {content}"
        else:
            formatted_line = line
        formatted_lines.append(formatted_line)

    return "<br/>".join(formatted_lines)


def generatePDF(topics, answers, title):
    title = str(title)
    pdf_file = f"{title.lower().replace(' ', '_')}_notes.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=A4,
                            rightMargin=40, leftMargin=40,
                            topMargin=60, bottomMargin=40)

    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph(f"<font size=22 color='#003399'><b>Notes on: {title}</b></font>", styles['Title']))
    story.append(Spacer(1, 0.3 * inch))

    for i, topic in enumerate(topics):
        # Subtopic title
        story.append(Paragraph(f"<font size=16 color='#FF5733'><b>{i+1}.) {topic}</b></font>", styles['Heading2']))
        story.append(Spacer(1, 0.1 * inch))

        # Format and add content
        formatted_answer = format_text(answers[i])
        story.append(Paragraph(f"<font size=11>{formatted_answer}</font>", styles['BodyText']))
        story.append(Spacer(1, 0.3 * inch))

    doc.build(story)
    print(f"PDF generated: {pdf_file}")


# Utility to generate topic-wise questions PDF

def generate_topicwise_questions_pdf(title, questions, answers, topic):
    from uuid import uuid4
    styles = getSampleStyleSheet()

    filename = f"{title.lower().replace(' ', '_')}_topicwise_questions.pdf"
    temp_filename = f"temp_{uuid4().hex}.pdf"  # Temporary file to hold new content

    story = []

    # Add topic heading
    story.append(Paragraph(f"<font size=16 color='#003399'><b>Topic: {topic}</b></font>", styles["Heading2"]))
    story.append(Spacer(1, 0.2 * inch))

    for q in questions:
        story.append(Paragraph(f"<font size=11>{q.strip()}</font>", styles["BodyText"]))
        story.append(Spacer(1, 0.2 * inch))
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph(f"<font size=11>Answers</font>", styles["BodyText"]))
    story.append(Spacer(1, 0.2 * inch))
    for a in answers:
        q = a["q_no"]
        ans = a["answer"]
        story.append(Paragraph(f"<font size=11>{q}. {ans}</font>", styles["BodyText"]))
        story.append(Spacer(1, 0.2 * inch))

    # Generate new content into a temp PDF
    doc = SimpleDocTemplate(temp_filename, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=60, bottomMargin=40)
    doc.build(story)

    if os.path.exists(filename):
        # Merge existing file with new temp content
        merger = PdfMerger()
        merger.append(filename)         # Old content
        merger.append(temp_filename)    # New content
        merger.write(filename)          # Overwrite with merged content
        merger.close()
        os.remove(temp_filename)        # Clean up temp file
    else:
        # If file doesn't exist, just rename the temp file as final
        os.rename(temp_filename, filename)

    return filename


# Utility to generate final question paper with optional answer key
def generate_final_questionpaper_pdf(title, final_paper, answer_key=None):
    filename = f"{title.lower().replace(' ', '_')}_final_question_paper.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=60, bottomMargin=40)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>FINAL QUESTION PAPER</b>", styles['Title']))
    story.append(Spacer(1, 0.3 * inch))

    for i, q in enumerate(final_paper):
        story.append(Paragraph(q, styles["BodyText"]))
        story.append(Spacer(1, 0.2 * inch))

    if answer_key:
        story.append(PageBreak())
        story.append(Paragraph("<b>ANSWER KEY</b>", styles['Title']))
        story.append(Spacer(1, 0.3 * inch))
        for ans in answer_key:
            story.append(Paragraph(ans, styles["BodyText"]))
            story.append(Spacer(1, 0.1 * inch))

    doc.build(story)
    return filename
