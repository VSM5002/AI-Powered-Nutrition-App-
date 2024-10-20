from flask import Flask, render_template, request
from ml_model import process_user_input

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    budget = float(request.form['budget'])
    diet_preference = request.form['diet']
    Cuisine = request.form['cuisine']
    
    recommended_foods = process_user_input(budget, diet_preference, Cuisine)
    
    return render_template('result.html',foods=recommended_foods)

if __name__ == '__main__':
    app.run(debug=True)
