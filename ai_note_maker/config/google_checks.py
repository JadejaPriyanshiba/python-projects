# list_generative_models.py

from basics import getValue
import google.generativeai as genai

def list_available_models(api_key: str):
    """
    Lists all models available with the given Google Generative AI API key.
    Gracefully handles missing fields.
    
    Args:
        api_key (str): Your Google Generative AI API key.
    """
    try:
        # Configure with API key
        genai.configure(api_key=api_key)

        # Convert the generator to a list
        models = list(genai.list_models())

        if not models:
            print("No models available with the provided API key.")
            return

        print(f"\nFound {len(models)} models:\n" + "-" * 60)

        for model in models:
            name = getattr(model, "name", "")
            description = getattr(model, "description", "")
            input_token_limit = getattr(model, "input_token_limit", "")
            output_token_limit = getattr(model, "output_token_limit", "")
            supports_chat = getattr(model, "supports_chat", "")
            supports_embeddings = getattr(model, "supports_embeddings", "")

            print(f"Name:                {name}")
            print(f"Description:         {description}")
            print(f"Input Token Limit:   {input_token_limit}")
            print(f"Output Token Limit:  {output_token_limit}")
            print(f"Supports Chat:       {supports_chat}")
            print(f"Supports Embeddings: {supports_embeddings}")
            print("-" * 60)

    except Exception as e:
        print(f"Error: {e}")
        
if __name__ == "__main__":
    # Replace with your actual API key or prompt the user
    apiKey = getValue("GEMINI_TOKEN")
    list_available_models(apiKey)
