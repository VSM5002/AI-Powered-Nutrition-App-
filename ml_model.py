import pandas as pd
import requests

# Load datasets
food_data = pd.read_csv("C:/Users/Admin/OneDrive/IBM_DATATHON/Indian_food_data.csv", encoding='ISO-8859-1')
price_data = pd.read_csv("C:/Users/Admin/OneDrive/IBM_DATATHON/prices.csv")

# Nutritionix API credentials
app_id = '31dc42e1'
app_key = 'c97fb5fe86f066b3ff59aef4af97bf67'

# Function to call Nutritionix API for calorie and nutrient info
def get_nutrition_info(food_name):
    url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
    headers = {
        'x-app-id': app_id,
        'x-app-key': app_key,
        'Content-Type': 'application/json'
    }
    data = {
        "query": food_name,
        "timezone": "US/Eastern"
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to estimate price based on ingredients
def estimate_price(ingredients, price_data):
    ingredient_list = [ingredient.strip().lower() for ingredient in ingredients.split(",")]
    total_price = 0
    for ingredient in ingredient_list:
        matched_price = price_data[price_data['Commodity'].str.lower() == ingredient]
        if not matched_price.empty:
            total_price += matched_price['Modal_x0020_Price'].values[0]
    return total_price

# Function to process user input, filter food based on preferences, state, and budget
def process_user_input(budget, diet_preference, cuisine):
    budget = budget * 100  # Convert budget to match price scale
    filtered_food = food_data[(food_data['Diet'] == diet_preference) & (food_data['Cuisine'] == cuisine)]
    
    food_with_prices_and_nutrition = []
    
    for _, row in filtered_food.iterrows():
        food_name = row['TranslatedRecipeName']
        ingredients = row['Ingredients']
        instructions = row['Instructions']  # Extract the recipe instructions
        estimated_price = estimate_price(ingredients, price_data)
        
        if estimated_price <= budget:
            nutrition_info = get_nutrition_info(food_name)
            if nutrition_info:
                food_details = {
                    'name': food_name,
                    'calories': nutrition_info['foods'][0]['nf_calories'],
                    'carbs': nutrition_info['foods'][0]['nf_total_carbohydrate'],
                    'protein': nutrition_info['foods'][0]['nf_protein'],
                    'fat': nutrition_info['foods'][0]['nf_total_fat'],
                    'price': estimated_price,
                    'instructions': instructions  # Include recipe instructions
                }
                food_with_prices_and_nutrition.append(food_details)
    
    return food_with_prices_and_nutrition
