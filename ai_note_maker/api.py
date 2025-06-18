import requests
from config import connect as con
from services import generate_pdf as genPDF


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

def getTopics(title):
    prompt = f"""
You are an expert academic assistant.

Given the main topic: "{title}", list all the important topics or subtopics that should be covered to learn completly basic and meduim and general detailed learning.
accordingly to a student in 12th Grade
List topics in bullet points starting eith '-',
Do not add extra explanation — just give the clean short few words list.
Topics:
"""
    response = callModel(prompt)
    topics = convertIntoArray(response)
    print(response)
    for item in topics:
        print(str(topics.index(item))+".) "+item)
    return topics

def getExplanation(topic):
    prompt = f"""
Explain the topic: "{topic}" in a clear, structured, and beginner-friendly way.

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

    topics = getTopics(title)
    answers = []
    for topic in topics:
        answer = getExplanation(topic)
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

