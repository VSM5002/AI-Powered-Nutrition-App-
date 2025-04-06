from flask import Flask, render_template, request
import sqlite3
import csv
import requests  # For making API calls
from chat import generate_recipe  # Import the function from chat.py

app = Flask(__name__)

@app.route('/')
def index():
    # Render the home page with dietary restrictions
    dietary_restrictions = ['vegetarian','non-vegetarian','vegan', 'gluten-free', 'keto', 'diabetic-friendly']
    return render_template('index.html', dietary_restrictions=dietary_restrictions)

# Route to display vegetable prices
@app.route('/prices')
def show_prices():
    # Connect to the database
    conn = sqlite3.connect("prices/prices.db")
    cursor = conn.cursor()

    # Fetch the latest prices
    cursor.execute('''
        SELECT name, price, date FROM vegetable_prices
        WHERE date = (SELECT MAX(date) FROM vegetable_prices)
    ''')
    prices = cursor.fetchall()
    conn.close()

    # Pass the prices to the template
    return render_template('prices.html', prices=prices)


@app.route('/results', methods=['POST'])
def results():
    # Get user input from the form
    family_size = int(request.form.get('family_size'))
    dietary_restrictions = request.form.get('dietary_restrictions').lower()
    budget = float(request.form.get('budget'))

    # Generate a recipe using the Gemini API
    raw_response = generate_recipe(family_size, dietary_restrictions, budget)

    # Debugging: Log the raw response
    print("Gemini API Response:", raw_response)

    # Check if the API returned an error
    if isinstance(raw_response, str) and "Error" in raw_response:
        error_message = raw_response
        return render_template('result.html', error_message=error_message, recipe=None)
    elif not isinstance(raw_response, dict):
        try:
            # Attempt to parse raw_response as a dictionary
            import json
            raw_response = json.loads(raw_response)
        except (ValueError, TypeError):
            # If parsing fails, return a default error message
            error_message = "Unable to generate recipe at this time."
            return render_template('result.html', error_message=error_message, recipe=None)

    # Render the results page with the parsed recipe
    return render_template('result.html', error_message=None, recipe=raw_response)


@app.route('/calculate', methods=['POST'])
def calculate():
    # Get selected recipe ingredients and pantry items
    selected_ingredients = request.form.getlist('ingredients')
    pantry_items = request.form.getlist('pantry')

    # Fetch vegetable prices from the database
    conn = sqlite3.connect("prices/prices.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT name, price FROM vegetable_prices
        WHERE date = (SELECT MAX(date) FROM vegetable_prices)
    ''')
    prices = cursor.fetchall()
    conn.close()

    # Convert prices to a dictionary for easy lookup
    price_dict = {name.lower(): price for name, price in prices}

    # Calculate the total cost of missing ingredients
    missing_ingredients = [item for item in selected_ingredients if item not in pantry_items]
    total_cost = sum(price_dict.get(item.lower(), 0) for item in missing_ingredients)

    # Render the calculation result
    return render_template('calculate.html', total_cost=total_cost, missing_ingredients=missing_ingredients)

@app.route('/sample')
def sample_result():
    return render_template('sample_result.html')

if __name__ == '__main__':
    app.run(debug=True)