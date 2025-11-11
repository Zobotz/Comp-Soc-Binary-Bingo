import sqlite3
import random
import time

# --- Setup ---
conn = sqlite3.connect("bingo.db")
cursor = conn.cursor()

# Function to get a random challenge
def get_random_challenge():
    cursor.execute("SELECT challenge FROM events")
    challenges = [row[0] for row in cursor.fetchall()]
    return random.choice(challenges)


print(get_random_challenge())

conn.close()
