import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

# URL of the grocery website (replace with a real URL)
GROCERY_URL = "https://vegetablemarketprice.com/market/karnataka/today"

# Database file
DB_FILE = "prices.db"

def scrape_prices():
    # Send a GET request to the grocery website
    response = requests.get(GROCERY_URL)
    if response.status_code != 200:
        print("Failed to fetch data from the website.")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract vegetable prices (update selectors based on the website structure)
    prices = []
    for item in soup.select(".vegetable-item"):
        name = item.select_one(".name").text.strip()
        price = item.select_one(".price").text.strip().replace("₹", "")
        prices.append((name, float(price)))

    # Save prices to the database
    save_to_database(prices)

def save_to_database(prices):
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vegetable_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    # Insert the scraped prices
    date = datetime.now().strftime("%Y-%m-%d")
    for name, price in prices:
        cursor.execute('''
            INSERT INTO vegetable_prices (name, price, date)
            VALUES (?, ?, ?)
        ''', (name, price, date))

    # Commit and close the connection
    conn.commit()
    conn.close()
    print("Prices saved to the database.")

if __name__ == "__main__":
    scrape_prices()