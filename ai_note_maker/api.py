import requests
from config import config as cg
from services import generate_pdf as genPDF
from main import connectLocalModel
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
    connectLocalModel(prompt)
    

def convertIntoArray(data):
    lines = data.strip().split('\n')
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
    topics = convertIntoArray(response[0]['generated_text'])
    print(response[0]['generated_text'])
    for item in topics:
        print(str(topics.index(item))+".) "+item)
    return topics

def getExplanation(topic):
    prompt = f"""Explain the topic of {topic} in a clear and structured way. 
Break it down into key subtopics or components. 
For each subtopic, give a simple explanation, relevant examples, and, where appropriate, analogies or real-world applications to make the concept easier to understand. 
Use bullet points or headings to organize the information. 
Make sure the explanation is beginner-friendly and flows logically from one part to the next."""
    response = callModel(prompt)
    answer = response[0]['generated_text']
    print(answer)
    return answer

if __name__ == "__main__":
    title = input("For what topic do you want your notes?: ")

    topics = getTopics(title)
    answers = []
    for topic in topics:
        answer = getExplanation(topic)
        answers.append(answer)

    genPDF.generatePDF(topics, answers, title)
    
    # with open("apiresults", "w") as f:
    #     f.write("-------------------- TOPICS -----------------\n")

    #     for item in topics:
    #         f.write(str(topics.index(item))+".) "+item)
    #         f.write("\n")
    #         f.write(answers[topics.index(item)])
    #         f.write("\n\n\n")

