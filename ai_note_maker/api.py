import requests
from config import config as cg

def callModel(prompt):
    token = cg.getValue("TOKEN")
    apiurl = cg.getValue("API_URL")
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "inputs" : prompt
    }
    response = requests.post(apiurl, headers=headers, json=payload)
    if(response.status_code!=200):
        print("somthing went wrong coulbnt load response")
        return response
    
    return response.json()

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


from pathlib import Path

env_path = Path(__file__).parent.parent / '.env'
print("from 2 "+str(env_path))

title = input("For what topic do you want your notes?: ")

topics = getTopics(title)


with open("apiresults", "w") as f:
    f.write("-------------------- TOPICS -----------------\n")

    for item in topics:
        f.write(str(topics.index(item))+".) "+item)
        f.write("\n")