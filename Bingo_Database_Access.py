import sqlite3
import random
import time

# --- Setup ---
conn = sqlite3.connect("bingo.db")
cursor = conn.cursor()

# Function to get a random challenge
def get_random_challenge():
    try:
        conn = sqlite3.connect("bingo.db")
        cursor = conn.cursor()
        cursor.execute("SELECT challenge FROM events")
        challenges = [row[0] for row in cursor.fetchall()]
        conn.close()

        if not challenges:
            return "No challenges found in database!"

        # Return (not print!) a random one
        return random.choice(challenges)

    except Exception as e:
        return f"Error reading database: {e}"
