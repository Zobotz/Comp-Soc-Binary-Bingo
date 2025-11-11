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
    (1, "First person to MOOOOOO gets a sweet."),
    (2, "First person to hand the president a sock."),
    (3, "First person to call out the last 3 numbers called."),
    (4, "SWITCH CARDS!"),
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
