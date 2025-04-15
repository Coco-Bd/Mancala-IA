import os
import json
import sqlite3

def initialize_files():
    """
    Initialize the database and settings files if they don't exist.
    Creates:
    - db/db.py (already exists, so we'll skip this)
    - db/settings.json (creates if it doesn't exist)
    - db/tictactoe.db (creates the database file)
    """
    # Get the base directory (jeu_morpion_1)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    db_dir = os.path.join(base_dir, 'jeu_morpion_1/db')
    
    # Ensure the db directory exists
    os.makedirs(db_dir, exist_ok=True)
    
    # Check if settings.json exists, create if it doesn't
    settings_path = os.path.join(db_dir, 'settings.json')
    if not os.path.exists(settings_path):
        default_settings = {
            "player_1": "Human",
            "player_2": "Human"
        }
        
        with open(settings_path, 'w') as f:
            json.dump(default_settings, f, indent=4)
    
    # Initialize the database
    db_path = os.path.join(db_dir, 'tictactoe.db')
    
    # Check if the database file exists
    db_exists = os.path.exists(db_path)
    
    # Connect to the database (this will create it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    
    # Create the games table if it doesn't exist
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
    conn.commit()
    conn.close()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
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