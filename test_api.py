import requests
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Step 1: Fetch data from CoinGecko
url = "https://api.coingecko.com/api/v3/simple/price"
params = {
    "ids": "bitcoin,ethereum",
    "vs_currencies": "usd",
    "include_market_cap": "true",
    "include_24hr_change": "true",
    "include_last_updated_at": "true"
}

response = requests.get(url, params=params)
data = response.json()
print("Fetched:", data)

# Step 2: Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("DB_PASSWORD"),
    database="crypto_data"
)
cursor = conn.cursor()

# Step 3: Insert each coin's data into the table
for coin, info in data.items():
    cursor.execute(
        "INSERT INTO prices (coin, price_usd, market_cap, change_24h, last_updated_at) VALUES (%s, %s, %s, %s, %s)",
        (coin, info["usd"], info["usd_market_cap"], info["usd_24h_change"], info["last_updated_at"])
    )

conn.commit()
cursor.close()
conn.close()

print("Data inserted successfully!")