import sqlite3

conn = sqlite3.connect("mancala_ai.db")
cursor = conn.cursor()

# Create a super simple table for games
cursor.execute("DROP TABLE IF EXISTS games")
cursor.execute("""
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    moves TEXT,         -- Simple string like "4;8;2;9;5;7"
    winner TEXT,        -- "player1" or "player2"
    count INTEGER DEFAULT 1
)
""")

# Create an index for faster lookups
cursor.execute("CREATE INDEX IF NOT EXISTS idx_moves ON games(moves)")

conn.commit()
conn.close()

print("Database schema created - simple version")