# from reportlab.lib.pagesizes import A4
# from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.enums import TA_CENTER
# from reportlab.lib.units import inch

# # ***** HELPERS
# styles = getSampleStyleSheet()

# # Custom Styles
# styles.add(ParagraphStyle(name='Centered', alignment=TA_CENTER, fontSize=11))
# styles.add(ParagraphStyle(name='Equation', alignment=TA_CENTER, fontSize=11, spaceBefore=6, spaceAfter=6))
# styles.add(ParagraphStyle(name='Subheading', fontSize=13, textColor="#003366", spaceAfter=6))
# styles.add(ParagraphStyle(name='Example', fontSize=11, leftIndent=20, textColor="#333333"))
# styles.add(ParagraphStyle(name='Note', fontSize=10, textColor="#666666", italic=True))


# def add_title(story, title):
#     story.append(Paragraph(f"<font size=22 color='#003399'><b>{title}</b></font>", styles['Title']))
#     story.append(Spacer(1, 0.3 * inch))

# def add_section(story, section_title):
#     story.append(Paragraph(f"<font size=16 color='#FF5733'><b>{section_title}</b></font>", styles['Heading2']))
#     story.append(Spacer(1, 0.2 * inch))

# def add_subheading(story, text):
#     story.append(Paragraph(f"<b>{text}</b>", styles['Subheading']))

# def add_paragraph(story, text):
#     text = text.replace('\n', '<br/>')
#     story.append(Paragraph(text, styles['CustomBodyText']))
#     story.append(Spacer(1, 0.1 * inch))

# def add_equation(story, equation_text):
#     # Simple LaTeX-style notation – not rendered as math but looks centered
#     story.append(Paragraph(f"<font face='Courier'>{equation_text}</font>", styles['Equation']))

# def add_example(story, example_text):
#     example_text = example_text.replace('\n', '<br/>')
#     story.append(Paragraph(f"<b>Example:</b> {example_text}", styles['Example']))
#     story.append(Spacer(1, 0.1 * inch))

# def add_note(story, note_text):
#     story.append(Paragraph(f"<i>{note_text}</i>", styles['Note']))
#     story.append(Spacer(1, 0.1 * inch))

# def generatePDF(topics, answers, title):
#     pdf_file = f"{title.lower().replace(' ', '_')}.pdf"
#     doc = SimpleDocTemplate(pdf_file, pagesize=A4,
#                             rightMargin=40, leftMargin=40,
#                             topMargin=60, bottomMargin=40)

#     story = []
#     add_title(story, f"Notes on: {title}")

#     for i, topic in enumerate(topics):
#         add_section(story, f"{i+1}.) {topic}")
#         # Assume answer is a structured string — parse if needed
#         formatted = answers[i]

#         # For demo: use dummy parser logic (can replace with real one)
#         for line in formatted.split("\n"):
#             line = line.strip()
#             if not line:
#                 continue
#             if line.startswith("####"):
#                 add_subheading(story, line[4:].strip())
#             elif line.startswith("**Example:**"):
#                 add_example(story, line.replace("**Example:**", "").strip())
#             elif line.startswith("**Note:**"):
#                 add_note(story, line.replace("**Note:**", "").strip())
#             elif "$" in line:  # crude check for equation
#                 add_equation(story, line)
#             else:
#                 add_paragraph(story, line)

#         story.append(Spacer(1, 0.2 * inch))

#     doc.build(story)
#     print(f"PDF generated: {pdf_file}")



###############################################################################################
############## ************** last acceptable version starts here ************** ##############
###############################################################################################

# from reportlab.lib.pagesizes import A4
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.enums import TA_CENTER
# from reportlab.lib.units import inch
# import re

# styles = getSampleStyleSheet()

# # Additional Styles
# styles.add(ParagraphStyle(name='Centered', alignment=TA_CENTER, fontSize=11))
# styles.add(ParagraphStyle(name='Equation', alignment=TA_CENTER, fontSize=11, spaceBefore=6, spaceAfter=6))
# styles.add(ParagraphStyle(name='Subheading', fontSize=13, textColor="#003366", spaceAfter=6))
# styles.add(ParagraphStyle(name='CustomBullet', fontSize=11, leftIndent=15))
# styles.add(ParagraphStyle(name='BodyIndented', fontSize=11, leftIndent=20))
# styles.add(ParagraphStyle(
#     name='Statement',
#     fontSize=10.5,
#     textColor="#333333",
#     leftIndent=10,
#     spaceBefore=6,
#     spaceAfter=6,
#     leading=14,
#     italic=True
# ))
# def parse_and_add_content(story, content):
#     lines = content.strip().split("\n")
#     buffer = ""
#     bullet_buffer = ""
#     in_bullet = False
#     latex_to_unicode = {
#         r"\theta": "θ",
#         r"\pi": "π",
#         r"\infty": "∞",
#         r"\le": "≤",
#         r"\ge": "≥",
#         r"\cdot": "·",
#         r"\sin": "sin",
#         r"\cos": "cos",
#         r"\tan": "tan",
#         r"\cot": "cot",
#         r"\csc": "csc",
#         r"\sec": "sec",
#     }

#     def flush_paragraph():
#         nonlocal buffer
#         if buffer.strip():
#             story.append(Paragraph(buffer.strip(), styles['CustomBodyText']))
#             story.append(Spacer(1, 0.1 * inch))
#             buffer = ""

#     def flush_bullet():
#         nonlocal bullet_buffer
#         if bullet_buffer.strip():
#             text = bullet_buffer.strip()

#             # Replace LaTeX-style text
#             for latex, uni in latex_to_unicode.items():
#                 text = text.replace(latex, uni)

#             lines = text.split("\n")
#             base_line = lines[0].strip()
#             example_lines = [l.strip() for l in lines[1:] if l.strip()]

#             # Handle title:** or **title:** bolding
#             match1 = re.match(r"^(.*?)\s*:\s*\*\*\s*(.+)", base_line)
#             match2 = re.match(r"^(.*?)\*\*\s*:\s*(.+)", base_line)
#             if match1:
#                 title = match1.group(1).strip()
#                 body = match1.group(2).strip()
#                 final = f"<b>{title}:</b> {body}"
#             elif match2:
#                 title = match2.group(1).strip()
#                 body = match2.group(2).strip()
#                 final = f"<b>{title}:</b> {body}"
#             else:
#                 final = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", base_line)

#             # Append indented examples
#             for ex in example_lines:
#                 if ex.lower().startswith(("example:", "eg:", "e.g.")):
#                     ex = re.sub(r"^[•*-]?\s*(Example|e\.g\.|eg)[:\*]?\s*", "", ex, flags=re.IGNORECASE)
#                     final += f"<br/><font size=10>&nbsp;&nbsp;&nbsp;&nbsp;Example: {ex.strip()}</font>"
#                 else:
#                     final += f"<br/><font size=10>&nbsp;&nbsp;&nbsp;&nbsp;{ex.strip()}</font>"

#             story.append(Paragraph(f"• {final}", styles['CustomBullet']))
#             story.append(Spacer(1, 0.05 * inch))
#             bullet_buffer = ""



#     for line in lines:
#         stripped = line.strip()
#         for k, v in latex_to_unicode.items():
#             line = line.replace(k, v)
#         # Headings
#         if stripped.startswith("#### "):
#             flush_paragraph()
#             flush_bullet()
#             story.append(Paragraph(f"<b>{stripped[5:]}</b>", styles['Subheading']))
#             story.append(Spacer(1, 0.15 * inch))

#         elif stripped.startswith("### "):
#             flush_paragraph()
#             flush_bullet()
#             story.append(Paragraph(f"<b>{stripped[4:]}</b>", styles['Subheading']))
#             story.append(Spacer(1, 0.15 * inch))

#         elif stripped.startswith("## "):
#             flush_paragraph()
#             flush_bullet()
#             story.append(Paragraph(f"<b>{stripped[3:]}</b>", styles['Heading2']))
#             story.append(Spacer(1, 0.15 * inch))
        
#         # Special case: math or statement line with $...$ pattern (and not a bullet or heading)
#         elif '$' in stripped and not in_bullet and not stripped.startswith("#"):
#             flush_paragraph()
#             flush_bullet()

#             # Convert LaTeX-like math to Unicode
#             text = stripped
#             for latex, uni in latex_to_unicode.items():
#                 text = text.replace(latex, uni)

#             # Remove $ delimiters and style math parts
#             text = re.sub(r"\$(.+?)\$", r"<b>\1</b>", text)
#             text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)

#             story.append(Paragraph(f"<i>{text.strip()}</i>", styles['Statement']))
#             story.append(Spacer(1, 0.05 * inch))

#         # Bullet point or continued bullet
#         elif stripped.startswith("•") or stripped.startswith("* "):
#             flush_paragraph()
#             flush_bullet()
#             bullet_buffer = stripped.lstrip("•* ")
#             in_bullet = True
#         elif in_bullet and stripped:
#             # Likely continuation of a bullet
#             bullet_buffer += " " + stripped
#         elif not stripped:
#             # Empty line = end of paragraph or bullet
#             flush_paragraph()
#             flush_bullet()
#             in_bullet = False

#         elif stripped.startswith("##### "):
#             flush_paragraph()
#             flush_bullet()
#             story.append(Paragraph(f"<b>{stripped[6:]}</b>", styles['CustomBodyText']))
#             story.append(Spacer(1, 0.1 * inch))

#         elif stripped.startswith("###### "):
#             flush_paragraph()
#             flush_bullet()
#             story.append(Paragraph(f"<b>{stripped[7:]}</b>", styles['BodyIndented']))
#             story.append(Spacer(1, 0.1 * inch))
#         elif re.match(r"^[•*-]\s*", stripped):
#             flush_paragraph()

#             # If it's an example/child line and we're in a bullet — append it
#             if re.match(r"^[•*-]\s*(Example|e\.g\.|eg)[:\*]?", stripped, re.IGNORECASE) and in_bullet:
#                 bullet_buffer += "\n" + stripped
#             else:
#                 flush_bullet()
#                 bullet_buffer = stripped.lstrip("•*- ")
#                 in_bullet = True
#         else:
#             flush_bullet()
#             # Handle inline bold and equations
#             line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", stripped)
#             # line = line.replace("$", "")  # optional: remove math tags if not rendering
#             buffer += line + " "

#     flush_paragraph()
#     flush_bullet()

# def generatePDF(topics, answers, title):
#     pdf_file = f"{title.lower().replace(' ', '_')}.pdf"
#     doc = SimpleDocTemplate(pdf_file, pagesize=A4,
#                             rightMargin=40, leftMargin=40,
#                             topMargin=60, bottomMargin=40)

#     story = []
#     story.append(Paragraph(f"<font size=22 color='#003399'><b>Notes on: {title}</b></font>", styles['Title']))
#     story.append(Spacer(1, 0.3 * inch))

#     for i, topic in enumerate(topics):
#         story.append(Paragraph(f"<font size=16 color='#FF5733'><b>{i+1}.) {topic}</b></font>", styles['Heading2']))
#         story.append(Spacer(1, 0.2 * inch))
#         parse_and_add_content(story, answers[i])
#         story.append(Spacer(1, 0.2 * inch))

#     doc.build(story)
#     print(f"PDF generated: {pdf_file}")
###############################################################################################
############## ************** last acceptable version ends here ************** ################
###############################################################################################

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
import re

styles = getSampleStyleSheet()

# Additional Styles
styles.add(ParagraphStyle(name='Centered', alignment=TA_CENTER, fontSize=11))
styles.add(ParagraphStyle(name='Equation', alignment=TA_CENTER, fontSize=11, spaceBefore=6, spaceAfter=6))
styles.add(ParagraphStyle(name='Subheading', fontSize=13, textColor="#003366", spaceAfter=6))
styles.add(ParagraphStyle(name='CustomBullet', fontSize=11, leftIndent=15))
styles.add(ParagraphStyle(name='BodyIndented', fontSize=11, leftIndent=20))
styles.add(ParagraphStyle(
    name='Statement',
    fontSize=10.5,
    textColor="#333333",
    leftIndent=10,
    spaceBefore=6,
    spaceAfter=6,
    leading=14,
    italic=True
))

# handling \frac{one}{two and something}
def latex_fraction_to_html(text):
    # Convert LaTeX superscripts inside \frac
    def repl(match):
        num = match.group(1)
        den = match.group(2)

        # Replace ^ with HTML superscripts
        num = re.sub(r"([a-zA-Z0-9]+)\^(\d+)", r"\1<sup>\2</sup>", num)
        den = re.sub(r"([a-zA-Z0-9]+)\^(\d+)", r"\1<sup>\2</sup>", den)

        return f"{num}⁄{den}"

    return re.sub(r"\\frac\{(.+?)\}\{(.+?)\}", repl, text)

# Replace $...$ with styled math
def highlight_math(text):
    return re.sub(
        r"\$(.+?)\$",
        lambda m: f"<font face='Courier' backColor='#f0f0f0'><b>{m.group(1)}</b></font>",
        text
    )

def parse_and_add_content(story, content):
    lines = content.strip().split("\n")
    buffer = ""
    bullet_buffer = ""
    in_bullet = False
    latex_to_unicode = {
        r"\theta": "θ",
        r"\pi": "π",
        r"\infty": "∞",
        r"\le": "≤",
        r"\ge": "≥",
        r"\cdot": "·",
        r"\sin": "sin",
        r"\cos": "cos",
        r"\tan": "tan",
        r"\cot": "cot",
        r"\csc": "csc",
        r"\sec": "sec",
        r"\omega":"Ω",
        r"\Delta":"Δ",
        r"\circ": "°",
    }

    def flush_paragraph():
        nonlocal buffer
        if buffer.strip():
            story.append(Paragraph(buffer.strip(), styles['CustomBodyText']))
            story.append(Spacer(1, 0.1 * inch))
            buffer = ""

    def flush_bullet():
        nonlocal bullet_buffer
        if not bullet_buffer.strip():
            return

        text = bullet_buffer.strip()

        # Replace LaTeX-style with Unicode
        for latex, uni in latex_to_unicode.items():
            text = text.replace(latex, uni)

        lines = [l.strip() for l in text.split("\n") if l.strip()]
        base_line = lines[0]
        sub_lines = lines[1:]

        # Clean any leftover stray **
        base_line = re.sub(r"\*\*", "", base_line).strip()
        base_line = re.sub(r"\*(.+?)\*", r"<i>\1</i>", base_line)
        base_line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", base_line)

        sub_lines = [
            re.sub(r"\*\*", "", s).strip() for s in sub_lines
        ]
        sub_lines = [
            re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s) for s in sub_lines
        ]
        sub_lines = [
            re.sub(r"\*(.+?)\*", r"<i>\1</i>", s) for s in sub_lines
        ]

        # Detect bullets like "Title: body"
        match_title = re.match(r"^(.*?):\s*(.+)", base_line)
        if match_title:
            title = match_title.group(1).strip()
            body = match_title.group(2).strip()
            para = f"<b>{title}:</b> {body}"
        else:
            para = base_line

        # Output parent bullet
        story.append(Paragraph(f"• {para}", styles['CustomBullet']))

        # Output sub-points (indented, under parent bullet)
        for sub in sub_lines:
            story.append(Paragraph(f"<font size=10>&nbsp;&nbsp;&nbsp;&nbsp;{sub}</font>", styles['BodyIndented']))

        story.append(Spacer(1, 0.05 * inch))
        bullet_buffer = ""


    for line in lines:
        stripped = line.strip()
        for k, v in latex_to_unicode.items():
            line = line.replace(k, v)
        # Headings
        if stripped.startswith("#### "):
            flush_paragraph()
            flush_bullet()
            story.append(Paragraph(f"<b>{stripped[5:]}</b>", styles['Subheading']))
            story.append(Spacer(1, 0.15 * inch))

        elif stripped.startswith("### "):
            flush_paragraph()
            flush_bullet()
            story.append(Paragraph(f"<b>{stripped[4:]}</b>", styles['Subheading']))
            story.append(Spacer(1, 0.15 * inch))

        elif stripped.startswith("## "):
            flush_paragraph()
            flush_bullet()
            story.append(Paragraph(f"<b>{stripped[3:]}</b>", styles['Heading2']))
            story.append(Spacer(1, 0.15 * inch))
        
        # Special case: math or statement line with $...$ pattern (and not a bullet or heading)
        elif ('$' in stripped or 'θ' in stripped or '=' in stripped) and not in_bullet and not stripped.startswith("#") and not re.match(r"^[•*-]", stripped):
            flush_paragraph()
            flush_bullet()

            # Convert LaTeX-like math to Unicode
            text = stripped
            for latex, uni in latex_to_unicode.items():
                text = text.replace(latex, uni)

            # Remove $ delimiters and style math parts
            text = re.sub(r"\$(.+?)\$", r"<b>\1</b>", text)
            text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
            # back quotes handling
            text = re.sub(r"`(.+?)`", r"<font face='Courier' backColor='#f0f0f0'>\1</font>", text)
            # super script handling
            text = re.sub(r'(\w+)\^(\d+)', r'\1<sup>\2</sup>', text)
            # handling /frac
            text = latex_fraction_to_html(text)
            # handling quations between $...$
            text = highlight_math(text) 
            
            text = re.sub(r"\$(.*?)\$", r"<font color='#003366'><b>\1</b></font>", text)
            text = re.sub(r"\^\{?\\?circ\}?", "°", text)
            text = text.replace("^°", "°")
            text = text.replace("^\circ", "°")
            story.append(Paragraph(f"<i>{text.strip()}</i>", styles['Statement']))
            story.append(Spacer(1, 0.05 * inch))

        elif stripped.startswith("* ") or stripped.startswith("• ") or stripped.startswith("- "):
            flush_paragraph()
            flush_bullet()
            bullet_buffer = stripped.lstrip("*•- ")
            in_bullet = True
        # Bullet point or continued bullet
        elif stripped.startswith("•") or stripped.startswith("* "):
            flush_paragraph()
            flush_bullet()
            bullet_buffer = stripped.lstrip("•* ")
            in_bullet = True
        elif in_bullet and stripped:
            # If line starts like a bullet but we're already in one, treat as child
            if re.match(r"^[•*-]\s+", stripped):
                flush_bullet()
                bullet_buffer = stripped.lstrip("•*- ")
            else:
                bullet_buffer += "\n" + stripped

        elif not stripped:
            # Empty line = end of paragraph or bullet
            flush_paragraph()
            flush_bullet()
            in_bullet = False

        elif stripped.startswith("##### "):
            flush_paragraph()
            flush_bullet()
            story.append(Paragraph(f"<b>{stripped[6:]}</b>", styles['CustomBodyText']))
            story.append(Spacer(1, 0.1 * inch))

        elif stripped.startswith("###### "):
            flush_paragraph()
            flush_bullet()
            story.append(Paragraph(f"<b>{stripped[7:]}</b>", styles['BodyIndented']))
            story.append(Spacer(1, 0.1 * inch))
        elif re.match(r"^[•*-]\s*", stripped):
            flush_paragraph()

            # If it's an example/child line and we're in a bullet — append it
            if re.match(r"^[•*-]\s*(Example|e\.g\.|eg)[:\*]?", stripped, re.IGNORECASE) and in_bullet:
                bullet_buffer += "\n" + stripped
            else:
                flush_bullet()
                bullet_buffer = stripped.lstrip("•*- ")
                in_bullet = True
        else:
            flush_bullet()
            # Handle inline bold and equations
            line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", stripped)
            # line = line.replace("$", "")  # optional: remove math tags if not rendering
            buffer += line + " "  


    flush_paragraph()
    flush_bullet()

def generatePDF(topics, answers, title):
    pdf_file = f"{title.lower().replace(' ', '_')}.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=A4,
                            rightMargin=40, leftMargin=40,
                            topMargin=60, bottomMargin=40)

    story = []
    story.append(Paragraph(f"<font size=22 color='#003399'><b>Notes on: {title}</b></font>", styles['Title']))
    story.append(Spacer(1, 0.3 * inch))

    for i, topic in enumerate(topics):
        story.append(Paragraph(f"<font size=16 color='#FF5733'><b>{i+1}.) {topic}</b></font>", styles['Heading2']))
        story.append(Spacer(1, 0.2 * inch))
        parse_and_add_content(story, answers[i])
        story.append(Spacer(1, 0.2 * inch))

    doc.build(story)
    print(f"PDF generated: {pdf_file}")