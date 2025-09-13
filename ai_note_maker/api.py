import random
import re
import requests
from config import connect as con
from services import generate_pdf_from_plain as genPDF
from validations import user_validations as uvd
import sys


isDebug = True
getInstantProgressPDF = False
recommendTopics = False
getQuestions = True
getNotes = True
startIndex = 0

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
        return preDefineTopics.replace("\n","").split(",,")

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

def makeQuestions(topic, chapter, subject, otherTopics, complexity, maturity, addMCQs = True, addTruFalse = False, addOneWord = False, addFIBs = False, questions = 10, lastQuestionNumber = 0, model = "local"):
    startNum = lastQuestionNumber + 1
    topicList = ", ".join(otherTopics)

    prompt = f"""
You are an experienced educator and professional exam paper setter.

Generate {questions} high-quality, diverse, and original exam-style questions for the topic: "{topic}" in the chapter: "{chapter}" under the subject: "{subject}".

Other related topics to consider for depth and relevance: {topicList}

Guidelines:
1. Difficulty: {complexity.capitalize()}
2. Student Maturity Level: {maturity}
3. Start numbering from question number {startNum}
4. Use plain text only - no markdown, no *, #, or formatting symbols.
5. Follow standard exam paper formatting:
   - Numbered questions.
   - Proper punctuation and spacing.
   - Leave a blank line between questions.
   - Do NOT include answers with the questions.

Structure:
{ 'Section: Multiple Choice Questions\n- Provide 4 options (a)-(d) for each MCQ.' if addMCQs else '' }
{ 'Section: True or False\n- Provide clear factual statements.' if addTruFalse else '' }
{ 'Section: One Word Answer Questions\n- Each question must have a single-word answer.' if addOneWord else '' }
{ 'Section: Fill in the Blanks\n- Use grammatically correct sentences with blanks.' if addFIBs else '' }
Note: don't include any other format / structure other than these...

After all questions, write an "Answer Key" section formatted like this:

Answer Key:
1. (b)
2. True
3. Inertia
...

Only output the questions followed by the answer key. No extra explanations.
"""

    if model == "gemini":
        prompt += "\nEnsure this is all plain text. No formatting symbols like *, #, etc."

    response = callModel(prompt, model=model)

    if response is None:
        raise Exception("Invalid response from model")

    raw_output = response.strip()

    # Split into questions and answers
    if "Answer Key:" in raw_output:
        question_part, answer_part = raw_output.split("Answer Key:", 1)
    else:
        raise Exception("Answer key not found in the output")

    # Extract each question line (ignore empty lines)
    question_lines = [line.strip() for line in question_part.strip().split("\n") if line.strip()]
    
    # Extract answers from answer part
    # Supports formats like "1. (b)" or "2. True" or "3. Gravity"
    answer_lines = [line.strip() for line in answer_part.strip().split("\n") if re.match(r"^\d+\.\s", line.strip())]

    # Parse into clean lists
    questions = question_lines
    answers = []
    for line in answer_lines:
        match = re.match(r"^(\d+)\.\s+(.*)", line)
        if match:
            q_num = int(match.group(1))
            ans = match.group(2).strip()
            answers.append({"q_no": q_num, "answer": ans})

    return {
        "questions": questions,
        "answers": answers
    }

subject = "Physics"
title = "Wave motion, optics and acoustics"
length = "150 lines"
maturity = "11th grade student"
extraNotes = "cover from simple to in depth knowledge, adding real world knowledge, add extra knowledge and fun facts too. Make the structure more point vise shorter but knowledgeable and to the point simple statements."
complexity = "from the basics and essential complexity for MCQ based exam (india)"
wantGemini = True
preDefineTopics = """Introduction and basics,,
Types of waves, (progressive, stationary, mechanical, non-mechanical, transverse, longitudinal),,
Frequency, wavelength, periodic time and their relations,,
Properties and applications of electromagnetic waves (ordinary light, LASER) and sound waves (ultrasonic wave, audible wave),,
Amplitude, intensity, phase and wave equations,,
Reflection, refraction, Snell's law, absolute refractive index, relative refractive index, total internal reflection, critical angle, optical fiber (construction, properties and applications),,
Reverberation, Reverberation time, Sabine's formula, echo, absorption coefficient,,
Summary (quick revision)"""
if __name__ == "__main__":

    if(not isDebug):
        title = input("For what topic do you want your notes?: ")
        subject = input("Subject: ").strip()
        length = input("Length of the subtopics explanations (eg. 100 lines, 200 words): ").strip()
        maturity = input("Maturity of notes (enter human age, or grade or other) (eg: 12 years old, 12th grade med student, PHD student): ").strip()
        complexity = input("How much complexity do you want (basic, simple. medium, in depth, complex): ")
        extraNotes = input("any extra notes?: ")
        preDefineTopics = input("Do you have any predefined list of topics? if no then press 'Enter' or 'Return' yes then enter them separated with commas(,,), (topic1,, new topic 2): ").strip()
        wantGemini = True if int(input("do you want gemini? (1/0): ")) == 1 else False
    topics = getTopics(title, subject, maturity, preDefineTopics, complexity, extraNotes)
    
    with open(f"{title.lower().replace(" ","_")}.txt", "a") as f:
            f.write("-------------------- TOPICS -----------------\n")
            
            for item in topics:
                f.write(str(topics.index(item))+".) "+item)
                f.write("\n")
    
    answers = []
    final_paper = []
    answer_key = []

    questions_filename = f"{title.lower().replace(' ', '_')}_questions.txt"
    all_questions = []

    proceed = (input(f"Topic to start with is: {topics[startIndex::][0]} (1/0): ").strip()) == "1"
    if not proceed :
        sys.exit()

    for i, topic in enumerate(topics[startIndex::]):
        
        if getNotes:
            answer = getExplanation(topic, length, subject, maturity, complexity, extraNotes, title, topics[:i], topics[i+1:], model= "gemini" if wantGemini else "local")
            answers.append(answer)

            # Save as .txt
            with open(f"{title.lower().replace(' ', '_')}.txt", "a") as f:
                f.write(f"{i+1}.) {topic}\n")
                f.write(answer)
                f.write("\n\n\n")

            # Only pass topics/answers up to current index
            genPDF.generatePDF(topics[startIndex:i+1], answers[:i+1], title+f"_from_{startIndex}")
        
        if getQuestions:
            questions_filename = f"{title.lower().replace(' ', '_')}_questions.txt"
            all_answers = []

            with open(questions_filename, "a") as f:
                print(f"Generating questions for topic: {topic}")

                result = makeQuestions(
                    topic=topic,
                    chapter=title,
                    subject=subject,
                    otherTopics=topics[:i] + topics[i+1:],
                    complexity=complexity,
                    maturity=maturity,
                    addMCQs=True,
                    addTruFalse=False,
                    addOneWord=False,
                    addFIBs=False,
                    questions=15,
                    lastQuestionNumber=len(all_questions),
                    model="gemini" if wantGemini else "local"
                )

                f.write(f"Topic: {topic}\n\n")
                for q in result["questions"]:
                    f.write(q + "\n")
                f.write("\n\n")

                # Parse and store questions
                question_block = []
                current_q_number = None

                for q_text in result["questions"]:
                    q_text = q_text.strip()

                    # Start of a new question
                    match = re.match(r"^(\d+)\.\s+(.*)", q_text)
                    if match:
                        if question_block and current_q_number is not None:
                            # Store the previous full question block
                            full_question_text = "\n".join(question_block)
                            answer_obj = next((a for a in result["answers"] if a["q_no"] == current_q_number), None)
                            answer_text = answer_obj["answer"] if answer_obj else "N/A"
                            all_questions.append({
                                "original_q_no": current_q_number,
                                "text": full_question_text,
                                "answer": answer_text,
                                "topic": topic
                            })

                        # Start a new question block
                        current_q_number = int(match.group(1))
                        question_block = [q_text]

                    else:
                        # Continuation of options or explanation
                        if current_q_number is not None:
                            question_block.append(q_text)

                # Save the last question block
                if question_block and current_q_number is not None:
                    full_question_text = "\n".join(question_block)
                    answer_obj = next((a for a in result["answers"] if a["q_no"] == current_q_number), None)
                    answer_text = answer_obj["answer"] if answer_obj else "N/A"
                    all_questions.append({
                        "original_q_no": current_q_number,
                        "text": full_question_text,
                        "answer": answer_text,
                        "topic": topic
                    })

                print("generating topic vise question paper")
                # generating topic vise PDF
                ans = genPDF.generate_topicwise_questions_pdf(title, result["questions"], result["answers"], topic)

        # Step 3: Build Final Question Paper (Random)
        # random.shuffle(all_questions)
        # final_paper = []
        # answer_key = []

        # for i, q in enumerate(all_questions):
        #     q_number = i + 1
        #     final_paper.append(f"{q_number}. {q['text']}")
        #     answer_key.append(f"{q_number}. {q['answer']}")

        # final_filename = f"{title.lower().replace(' ', '_')}_final_paper.txt"
        # with open(final_filename, "w") as f:
        #     f.write("FINAL QUESTION PAPER\n\n")
        #     for q in final_paper:
        #         f.write(q + "\n\n")

        #     f.write("\nANSWER KEY\n\n")
        #     for a in answer_key:
        #         f.write(a + "\n")



    if getQuestions:
        print("generating final question paper")
        # genPDF.generatePDF(topics, answers, title)
        random.shuffle(all_questions)
        final_paper = []
        answer_key = []

        for i, q in enumerate(all_questions):
            q_number = i + 1
            final_paper.append(f"{q_number}. {q['text']}")
            answer_key.append(f"{q_number}. {q['answer']}")

        # Save final paper
        final_filename = f"{title.lower().replace(' ', '_')}_final_paper.txt"
        with open(final_filename, "w") as f:
            f.write("FINAL QUESTION PAPER\n\n")
            for i, q in enumerate(all_questions):
                f.write(f"{i+1}. {q['text']}\n\n")   # Already includes options
            f.write("\nANSWER KEY\n\n")
            for i, a in enumerate(all_questions):
                f.write(f"{i+1}. {a['answer']}\n")

        # save final paper pdf 
        ans = genPDF.generate_final_questionpaper_pdf(title=title, final_paper=final_paper, answer_key=answer_key)



