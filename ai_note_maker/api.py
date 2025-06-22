import requests
from config import connect as con
from services import generate_pdf as genPDF
from validations import user_validations as uvd

def callModel(prompt):
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

    if preDefineTopics !="":
        prompt += f"""
The user already has a predefined list of topics:
{preDefineTopics}

Please:
- Review the predefined topics
- Suggest improvements or additional recommended topics
- Then print a clean, updated list starting with '-'
"""

    prompt += "\nTopics:\n"


    response = callModel(prompt)
    tempTopics = convertIntoArray(response)
    topics = uvd.ValidateTopics(tempTopics)
    topics.validateTopics()    
    return topics.topicsByAI

def getExplanation(topic, length, subject, maturity, complexity, extraNotes):
    prompt = f"""
Explain the topic: "{topic}" in a clear, structured, and beginner-friendly way.
approx length of the explanations should be {length}
Subject: "{subject}",
Target learner level: "{maturity}",
complexity of the content: "{complexity}"
"{extraNotes}"
- Break it down into key subtopics or components.
- For each subtopic, provide a brief explanation and, where useful, an example or analogy.
- Use bullet points or headings.
- Avoid repeating instructions or filler text.
- End with a summary of key points.

Start directly:
"""
    response = callModel(prompt)
    
    if response is None:
        raise Exception("Invalid response from model")

    answer = response
    print(f"Explanation for {topic}:\n{answer}\n")
    return answer

if __name__ == "__main__":
    title = input("For what topic do you want your notes?: ")
    subject = input("Subject: ").strip()
    length = input("Length of the subtopics explanations (eg. 100 lines, 200 words): ").strip()
    maturity = input("Maturity of notes (enter human age, or grade or other) (eg: 12 years old, 12th grade med student, PHD student): ").strip()
    complexity = input("How much complexity do you want (basic, simple. medium, in depth, complex): ")
    extraNotes = input("any extra notes?: ")
    preDefineTopics = input("Do you have any predefined list of topics? if no then press 'Enter' or 'Return' yes then enter them separated with commas, (topic1, new topic 2): ").strip()
    topics = getTopics(title, subject, maturity, preDefineTopics, complexity, extraNotes)
    
    answers = []
    for topic in topics:
        answer = getExplanation(topic, length, subject, maturity, complexity, extraNotes)
        answers.append(answer)

    genPDF.generatePDF(topics, answers, title)
    
    with open("apiresults.txt", "w") as f:
        f.write("-------------------- TOPICS -----------------\n")
        
        for item in topics:
            f.write(str(topics.index(item))+".) "+item)
            f.write("\n")
        
        for item in topics:
            f.write(str(topics.index(item))+".) "+item)
            f.write("\n")
            f.write(answers[topics.index(item)])
            f.write("\n\n\n")

