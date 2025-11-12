import sqlite3

# Connect to (or create) a database file
conn = sqlite3.connect("bingo.db")

# Create a cursor to interact with the database
cursor = conn.cursor()

# Create a table for bingo events
cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_number INTEGER NOT NULL,
    challenge TEXT
);
""")

# Example: inserting a few challenges
challenges = [
    (1, "First person to MOOOOOO gets a sweet!"),
    (2, "First person to hand the president a sock gets a sweet!"),
    (3, "First person to call out the last 3 numbers called gets a sweet!"),
    (4, "SWITCH CARDS!"),
    (5, "First person to high-five the bingo caller gets a sweet!"),
    (6, "First person to do their best robot impression gets a sweet!"),
    (7, "Everyone swap seats!"),
    (8, "Everyone with glasses, give someone else a thumbs up!"),
    (9, "First person to shout out the binary for 10 gets a sweet!"),
    (10, "Compliment the person next to you!"),
    (11, "Trade cards with someone you haven’t spoken to yet!"),
    (12, "Everyone with an even card number wave at someone across the room!"),
    (13, "If your card has the number 20, give yourself a round of applause!"),
    (14, "Everyone who’s new to CompSoc — you get a sweet!"),
    (15, "SWITCH CARDS!"),
    (16, "Clap three times if you’re still in the game!"),
    (17, "If you’re holding a pen, raise it and shout ‘BINARY BINGO!’"),
    (18, "Everyone who’s holding a drink, take a sip — cheers!"),
    (19, "First person to pretend to be a binary number wins!"),
    (20, "Everyone point dramatically at the ceiling!"),
    (21, "First person to do 5 star jumps gets a sweet!")
    (22, "Give someone a thumbs up!"),
    (23, "Introduce yourself to someone you don't know!"),
    (24, "Everyone point at who they think will win!"),
    (25, "First person to pretend their bingo card is a phone and answer it gets a sweet!"),
]

cursor.executemany("INSERT INTO events (event_number, challenge) VALUES (?, ?);", challenges)

# Save (commit) the changes
conn.commit()

# Retrieve and print all challenges
cursor.execute("SELECT * FROM events;")
for row in cursor.fetchall():
    print(row)

# Always close when done
conn.close()
