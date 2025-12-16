import os
import json
import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(".env")

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

RECIPE_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "recipes": {
            "type": "array",
            "description": "A list of creative recipe suggestions generated from the ingredients.",
            "items": {
                "type": "object",
                "properties": {
                    "dish_name": {
                        "type": "string",
                        "description": "The creative and descriptive name of the suggested dish.",
                    },
                    "cuisine": {
                        "type": "string",
                        "description": "The style of cuisine, e.g., 'Italian', 'Thai', 'Mexican', 'Fusion'.",
                    },
                    "estimated_time_minutes": {
                        "type": "integer",
                        "description": "The total estimated preparation and cooking time, in minutes.",
                    },
                    "difficulty": {
                        "type": "string",
                        "enum": ["Easy", "Medium", "Hard"],
                        "description": "The complexity of the recipe.",
                    },
                    "recipe_steps": {
                        "type": "array",
                        "description": "A list of concise step-by-step instructions for the recipe.",
                        "items": {"type": "string"},
                    },
                },
                "required": [
                    "dish_name",
                    "cuisine",
                    "estimated_time_minutes",
                    "difficulty",
                    "recipe_steps",
                ],
            },
        },
        "identified_ingredients": {
            "type": "array",
            "description": "A list of all unique ingredients confidently identified in the input image.",
            "items": {"type": "string"},
        },
    },
    "required": ["recipes", "identified_ingredients"],
}


def generate_structured_recipes(image_url: str) -> dict:
    print(f"Fetching image from: {image_url}...")
    try:
        image_bytes = requests.get(image_url).content
        image_part = types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
    except requests.exceptions.RequestException as e:
        return {"error": f"Could not fetch image from {image_url}."}

    prompt_text = (
        "Act as a professional culinary AI assistant. "
        "1. VISUAL ANALYSIS: Strictly analyze the image to identify all edible ingredients, "
        "ignoring brand names, packaging labels, or background clutter. "
        "Also determine the amount of each ingredient that the image contains, "
        "using that information to inform your generation of recepies. "
        "2. ASSUMPTIONS: You may assume the user has basic pantry staples (oil, salt, pepper, water). "
        "3. GENERATION: Generate distinct, creative, and practical recipe suggestions. "
        "Ensure variety in cuisine types (e.g., don't make all the recipes pasta). "
        "Ensure the generation of 2-3 easy meals, 2-3 medium meals, and 1-2 hard meals. "
        "4. FORMATTING: Your output must be raw, valid JSON strictly adhering to the provided schema. "
        "Do not include markdown formatting (like ```json) or conversational filler."
    )

    config = types.GenerateContentConfig(
        response_mime_type="application/json", response_schema=RECIPE_JSON_SCHEMA
    )

    print("Sending structured recipe request to Gemini API...")

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=[prompt_text, image_part], config=config
    )

    recipe_data = json.loads(response.text)

    return recipe_data


if __name__ == "__main__":
    generate_structured_recipes()
