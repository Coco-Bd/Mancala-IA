import sqlite3

conn = sqlite3.connect("carrom_ai.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    player1 TEXT,
    player2 TEXT,
    winner TEXT,
    moves TEXT,
    score INTEGER
)
""")

conn.commit()
conn.close()