from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.units import inch

def generatePDF(topics, answers, title):
    pdf_file = "ai_generated_notes.pdf"
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

        # Explanation content
        formatted_answer = answers[i].replace('\n', '<br/>')
        story.append(Paragraph(f"<font size=11>{formatted_answer}</font>", styles['BodyText']))
        story.append(Spacer(1, 0.3 * inch))

    doc.build(story)
    print(f"PDF generated: {pdf_file}")