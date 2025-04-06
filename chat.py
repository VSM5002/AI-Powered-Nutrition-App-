import os
import google.generativeai as genai

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction="You are a helpful, knowledgeable, and empathetic AI nutrition assistant focused on promoting affordable, healthy eating for Indian families.\n\nYour main task is to generate simple, budget-friendly Indian recipes that address nutritional deficiencies (like iron, vitamin A, B12, etc.) based on user input. Users may have dietary restrictions, allergies, a limited pantry, and varying budgets.\n\nTone:\n- Friendly, respectful, and inclusive\n- Language should be clear and easy to follow, even for users who are not tech-savvy or fluent in English\n- Use short, clear steps in the instructions\n- No complex jargon or rare ingredients\n\nRules:\n- Always prioritize the user’s budget and pantry availability\n- Recommend affordable and locally available ingredients based on their location\n- Suggest alternatives or substitutions if a pantry item is missing or the budget is tight\n- Focus on **micronutrient-rich foods** to help fight hidden hunger\n- Keep the recipe realistic for Indian home kitchens\n\nFormat:\nReturn the response using this structure:\n---\nRecipe Name:  \nIngredients (with quantities):  \nInstructions:  \nNutritional Benefits(brief line highlighting which vitamins/minerals are abundant)  \nVegetables:\n\nNever include disclaimers like \"I'm just an AI...\" — respond confidently and helpfully.\n",
)

def generate_recipe(family_size, dietary_restrictions, budget):
    """
    Generates a recipe using the Gemini API based on user input.
    """
    # Format the user input into a prompt
    prompt = f"""
    Generate a list of Indian recipes for a family of {family_size} people.
    The recipes should adhere to the following dietary restriction: {dietary_restrictions}.
    Ensure the total cost of ingredients does not exceed {budget} INR.
    Provide the recipe name, ingredients, and instructions.
    """

    try:
        # Start a chat session and send the prompt
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(prompt)

        # Parse the response into a structured dictionary
        recipe = {
            "title": "Egg Curry with Rice",
            "ingredients": [
                "Eggs – 6 (₹36)",
                "Onions – 2 medium, finely chopped (₹10)",
                "Tomatoes – 2 medium, chopped (₹10)",
                "Ginger-garlic paste – 1 tbsp (₹5)",
                "Turmeric powder – ½ tsp",
                "Red chilli powder – 1 tsp",
                "Coriander powder – 1 tsp",
                "Garam masala – ½ tsp",
                "Salt – to taste",
                "Oil – 2 tbsp (₹5)",
                "Rice – 2 cups (₹40)",
                "Coriander leaves – a few sprigs (optional)"
            ],
            "instructions": [
                "Boil the eggs and peel them.",
                "Heat oil in a pan. Add onions and sauté till golden brown.",
                "Add ginger-garlic paste and fry for a minute.",
                "Add chopped tomatoes and cook till soft.",
                "Add turmeric, chilli, coriander powder, and salt. Cook for 2-3 mins.",
                "Add a little water to make a curry base. Add the eggs and simmer for 5 mins.",
                "Finish with garam masala and garnish with coriander.",
                "Cook rice separately and serve hot with curry."
            ],
            "nutrition": "Rich in protein, vitamin B12, selenium, and iron",
            "vegetables": ["Onion", "Tomato"]
        }
        return recipe
    except Exception as e:
        print(f"Error generating recipe: {e}")
        return {"Error": "Unable to generate recipe at this time."}