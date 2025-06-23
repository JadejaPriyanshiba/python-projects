from .basics import getValue
import requests
import google.generativeai as genai

def callAPIModel(prompt):
    token = getValue("TOKEN")
    apiUrl = getValue("API_URL")
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "inputs" : prompt
    }
    response = requests.post(apiUrl, headers=headers, json=payload)
    if(response.status_code!=200):
        raise Exception("something went wrong couldn't load response")
    print(str(response))
    return response.json()[0]['generated_text']

def callLocalModel(prompt):
    url = "http://localhost:1234/v1/completions"
    full_prompt = f"{prompt}"
    payload = {
        "prompt": full_prompt,
        "temperature": 0.7,
        "max_tokens": 1024,
        # "stop": ["Title:"],
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        return response.json()['choices'][0]['text'].strip()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")
    
def connectGemini2Flash(prompt, model='gemini-2.5-flash'):
    # Step 1: Configure with your API key1
    apiKey = getValue("GEMINI_TOKEN")
    genai.configure(api_key=apiKey)  # Replace with your key

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        print(response.text)
        return response.text
    except Exception as e:
        print("Error occurred:", e)