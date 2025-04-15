import sqlite3

conn = sqlite3.connect("mancala_ai.db")
cursor = conn.cursor()

# Table for storing complete games
cursor.execute("""
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    player1 TEXT,
    player2 TEXT,
    winner TEXT,
    total_moves INTEGER
)
""")

# Table for storing individual moves
cursor.execute("""
CREATE TABLE IF NOT EXISTS moves (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER,
    player TEXT,
    board_state TEXT,
    move_made INTEGER,
    result_state TEXT,
    FOREIGN KEY (game_id) REFERENCES games(id)
)
""")

conn.commit()
conn.close()