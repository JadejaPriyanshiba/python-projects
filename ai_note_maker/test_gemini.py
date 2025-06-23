import google.generativeai as genai
from ai_note_maker.config import basics as cg

#### model selection
## gemini-2.5-pro
# Use it when:
# You really need better reasoning, code accuracy, math, or multi-turn depth.
# You’re okay with slower output or fewer calls/day (~50–100).

# Use gemini-2.5-flash for:
# - Bulk text generation
# - Note-taking
# - Summarizing articles, transcripts, etc.

# Use gemini-2.5-pro for:
# - Deep insights
# - Reasoning, logic
# - Code analysis or factual precision

def listGeminiModel():
    models = genai.list_models()
    for model in models:
        print(f"Name: {model.name}")
        print(f"Supported methods: {model.supported_generation_methods}")
        print("-" * 50)