import requests
from config import connect as con
from services import generate_pdf_from_plain as genPDF
from validations import user_validations as uvd


isDebug = True
getInstantProgressPDF = False
recommendTopics = False

def callModel(prompt, model = "local"):
    # token = cg.getValue("TOKEN")
    # apiurl = cg.getValue("API_URL")
    # headers = {"Authorization": f"Bearer {token}"}

    # payload = {
    #     "inputs" : prompt
    # }
    # response = requests.post(apiurl, headers=headers, json=payload)
    # # if(response.status_code!=200):
    # #     print("somthing went wrong coulbnt load response")
    # #     return response
    # print(str(response))
    # return response.json()
    model = model.lower()
    if(model=="gemini"):
        return con.connectGemini2Flash(prompt)
    else:
        return con.callLocalModel(prompt)

def convertIntoArray(data):
    lines = data.split('\n')
    items = []
    for line in lines:
        line = line.strip()
        if line.startswith("-"):
            item = line[1:].strip()
            if item:
                items.append(item)
    return items

def getTopics(title, subject, maturity, preDefineTopics, complexity, extraNotes ):
    if recommendTopics:
        prompt = f"""
You are an expert academic assistant.

Given the main topic: "{title}",
Subject: "{subject}",
Target learner level: "{maturity}",
complexity of the content: "{complexity}"
"{extraNotes}"
List all the essential subtopics required to fully understand this topic at a basic to medium level of depth.

Please:
- List topics in bullet points starting with '-'
- Keep them short (a few words), no extra explanation
"""

        if recommendTopics and preDefineTopics !="":
            prompt += f"""
The user already has a predefined list of topics:
{preDefineTopics}

Please:
- Review the predefined topics
- Suggest improvements or additional recommended topics
- Then print a clean, updated list starting with '-'
"""

        prompt += "\nTopics:\n"


        response = callModel(prompt, model="gemini")
        tempTopics = convertIntoArray(response)
        topics = uvd.ValidateTopics(tempTopics)
        topics.validateTopics()    
        return topics.topicsByAI
    else:
        preDefineTopics = str(preDefineTopics)
        return preDefineTopics.replace("\n","").split(",")

def getExplanation(topic, length, subject, maturity, complexity, extraNotes, title, topicsAlreadyCovered, otherTopicsLeft, model = "local"):
    topicsAlreadyCovered = list(topicsAlreadyCovered)
    otherTopicsLeft = list(otherTopicsLeft)

    prompt = f"""
Explain the topic: "{topic}" in a clear, structured, and beginner-friendly way.
approx length of the explanations should be {length}
Subject: "{subject}",
The main parent topic is: "{title}", write content relating to this
Target learner level: "{maturity}",
complexity of the content: "{complexity}"
and the topics already covered are : {",".join(topicsAlreadyCovered)}, so don't include these topics (you can short recap things if they are referenced for current topic)
and the topics for future are : {",".join(otherTopicsLeft)}, so don't include content of these (you can provide a context to further reference if needed)

"{extraNotes}"
- Break it down into key subtopics or components.
- For each subtopic, provide a brief explanation and, where useful, an example or analogy.
- Use bullet points or headings.
- Avoid repeating instructions or filler text.
- End with a summary of key points.

Start directly:
"""
    if(model=="gemini"):
        prompt += "make it a plain text only , no formatting, no #, *, for formatting for anything, bulleting you can use numbers or '-', nothing else... "
    response = callModel(prompt, model=model)
    
    if response is None:
        raise Exception("Invalid response from model")

    answer = response
    print(f"Explanation for {topic}:\n{answer}\n")
    return answer

subject = "Fundamentals of Artificial Intelligence"
title = "Introduction To Artificial Intelligence"
length = "150 lines"
maturity = "3rd year computer engineering student"
extraNotes = "Form it simple to understand, not lengthy, to the points, but more of knowledge with real life examples. Add extra fun facts and extra knowledge spots."
complexity = "from the basics to in depth real coding knowledge and concepts"
wantGemini = True
preDefineTopics = """What is Artificial Intelligence?,
History and Evolution of AI,
AI vs. Machine Learning vs. Deep Learning,
Types of AI (Narrow. General. Super),
Intelligent Agents and Environments,
Simply overview of steps to create a AI model,
AI Ethics, Bias, and Fairness,
AI Societal Impact and Future,
AI Development Frameworks (Python and other Libraries),
The AI problem,
The underlying Assumptions,
AI techniques,
The level of model,
Criteria for success,
Real-world AI Applications and Case Studies
"""
# preDefineTopics = """Angles and Angle Measurement (Degrees, Radians)
# ,Right Triangle Trigonometry (SOH CAH TOA)
# ,Pythagorean Theorem Applications
# ,The Unit Circle and Reference Angles
# ,Trigonometric Functions of Any Angle
# ,Fundamental Trigonometric Identities (Reciprocal, Quotient, Pythagorean)
# ,Sum and Difference Identities
# ,Double and Half-Angle Identities
# ,Product-to-Sum and Sum-to-Product Identities
# ,Law of Sines
# ,Law of Cosines
# ,Area of Triangles using Trigonometry
# ,Solving Trigonometric Equations
# ,Periods of Trigonometric functions
# ,Allied & Compound Angles, Multiple-Submultiples angles
# ,Sum and factor formula
# ,Summary"""
# preDefineTopics = """Introduction,
# Electric Charge: Fundamental Concepts,
# Definition of Electric Current,
# Conventional Current vs. Electron Flow,
# Drift Velocity of Electrons,
# Electric Potential and Potential Difference (Voltage),
# Electromotive Force (EMF),
# Electrical Resistance and Resistivity,
# Factors Affecting Resistance,
# Ohm's Law,
# Electrical Conductivity,
# Direct Current (DC) vs. Alternating Current (AC),
# Simple Electric Circuits,
# Series and Parallel Combinations of Resistors,
# Kirchhoff's Current Law (KCL),
# Kirchhoff's Voltage Law (KVL),
# Electric field, electric potential, electric flux,
# Capacitance and capacitors,
# parallel plate capacitors,
# series and parallel combination of capacitors,
# Electrical Power,
# Electrical Energy,
# Joule Heating Effect,
# Summary, formula sheet, tips and tricks
# """

if __name__ == "__main__":

    if(not isDebug):
        title = input("For what topic do you want your notes?: ")
        subject = input("Subject: ").strip()
        length = input("Length of the subtopics explanations (eg. 100 lines, 200 words): ").strip()
        maturity = input("Maturity of notes (enter human age, or grade or other) (eg: 12 years old, 12th grade med student, PHD student): ").strip()
        complexity = input("How much complexity do you want (basic, simple. medium, in depth, complex): ")
        extraNotes = input("any extra notes?: ")
        preDefineTopics = input("Do you have any predefined list of topics? if no then press 'Enter' or 'Return' yes then enter them separated with commas, (topic1, new topic 2): ").strip()
        wantGemini = True if int(input("do you want gemini? (1/0): ")) == 1 else False
    topics = getTopics(title, subject, maturity, preDefineTopics, complexity, extraNotes)
    
    with open(f"{title.lower().replace(" ","_")}.txt", "a") as f:
            f.write("-------------------- TOPICS -----------------\n")
            
            for item in topics:
                f.write(str(topics.index(item))+".) "+item)
                f.write("\n")
    
    answers = []

    for i, topic in enumerate(topics):
        answer = getExplanation(topic, length, subject, maturity, complexity, extraNotes, title, topics[:i], topics[i+1:], model= "gemini" if wantGemini else "local")
        answers.append(answer)

        # Save as .txt
        with open(f"{title.lower().replace(' ', '_')}.txt", "a") as f:
            f.write(f"{i+1}.) {topic}\n")
            f.write(answer)
            f.write("\n\n\n")

        # Only pass topics/answers up to current index
        genPDF.generatePDF(topics[:i+1], answers[:i+1], title)

    # genPDF.generatePDF(topics, answers, title)

