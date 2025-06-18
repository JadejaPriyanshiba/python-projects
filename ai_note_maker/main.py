import requests
from config import connect as con

    
def generate_notes(title):
    
    get_topics = (
        f"""
You are an expert academic assistant.

Given the main topic: "{title}", list all the important sections or subtopics that should be covered to make a complete basic and meduim and general detailed learning.
List topics in bullet points,
Do not add extra explanation — just give the clean short few words list.
"""
    )
    get_explanation=(
        "Generate long, accurate, well-structured, and exam-ready notes with proper formatting, bullet points, and clear explanations.\n\n"
    )
    response = con.callLocalModel(get_topics)
    response = response
def parse_bullet_list_to_array(raw_output: str):
    lines = raw_output.strip().split('\n')
    items = []
    for line in lines:
        line = line.strip()
        if line.startswith("-"):
            item = line[1:].strip()
            if item:
                items.append(item)
    return items

# === Run ===
if __name__ == "__main__":
    title = input("Enter your topic title: ")
    topics = generate_notes(title)
    print("\n--- Generated Notes ---\n")
    topics = parse_bullet_list_to_array(topics)
    for i in topics :
        print(str(topics.index(i))+ ".) "+i) 

