import sqlite3
import json
import os
import datetime
import pandas as pd

class GameMemory:
    def __init__(self, db_path="../../db/mancala_ai.db", context_length=2):
        """Initialize connection to the game memory database"""
        # Adjust the path to point to the db in the project root
        self.db_path = os.path.join(os.path.dirname(__file__), db_path)
        self.context_length = context_length  # How many previous moves to consider
        self._initialize_db()
    
    def _initialize_db(self):
        """Set up the database table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Single table for game patterns
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            board_state TEXT,
            move INTEGER,
            resulted_in_win INTEGER,
            play_count INTEGER DEFAULT 1
        )
        """)
        
        # Table for move sequences
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS move_sequences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            move_sequence TEXT,
            winner TEXT,
            play_count INTEGER DEFAULT 1
        )
        """)
        
        # Table for move responses
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS move_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            previous_moves TEXT,
            response_move INTEGER,
            resulted_in_win INTEGER,
            play_count INTEGER DEFAULT 1
        )
        """)
        
        # Table for games
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            moves TEXT,
            winner TEXT,
            count INTEGER DEFAULT 1
        )
        """)
        
        conn.commit()
        conn.close()
    
    def store_game(self, moves, winner):

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Convert moves to a simple string like "4;8;2;9"
        moves_str = ";".join(map(str, moves))
        
        # Check if we've seen this exact game before
        cursor.execute("SELECT id, count FROM games WHERE moves = ?", (moves_str,))
        result = cursor.fetchone()
        
        if result:
            # Update count for this game
            game_id, count = result
            cursor.execute("UPDATE games SET count = ? WHERE id = ?", (count + 1, game_id))
        else:
            # Store new game
            cursor.execute("INSERT INTO games (moves, winner, count) VALUES (?, ?, 1)", 
                          (moves_str, winner))
        
        conn.commit()
        conn.close()
    
    def find_best_move(self, board_state):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        board_state_str = json.dumps(board_state)
        
        # Find moves from this state and their win rates
        cursor.execute("""
        SELECT move, resulted_in_win, play_count,
               CAST(resulted_in_win AS FLOAT) / play_count AS win_rate
        FROM game_patterns
        WHERE board_state = ?
        ORDER BY win_rate DESC, play_count DESC
        """, (board_state_str,))
        
        results = cursor.fetchall()
        conn.close()
        
        # Return the move with the highest win rate, if any
        if results:
            best_move = results[0][0]
            return best_move
        
        return None
    
    def find_best_response(self, previous_moves):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Take only the last N moves for context
        context = previous_moves[-self.context_length:] if len(previous_moves) >= self.context_length else previous_moves
        context_json = json.dumps(context)
        
        # Find responses for this context and their win rates
        cursor.execute("""
        SELECT response_move, resulted_in_win, play_count,
               CAST(resulted_in_win AS FLOAT) / play_count AS win_rate
        FROM move_responses
        WHERE previous_moves = ?
        ORDER BY win_rate DESC, play_count DESC
        """, (context_json,))
        
        results = cursor.fetchall()
        conn.close()
        
        # Return the move with the highest win rate, if any
        if results:
            best_move = results[0][0]
            return best_move
        
        return None
    
    def find_similar_game(self, current_moves):
        if not current_moves:
            return None
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Convert current moves to string
        current_str = ";".join(map(str, current_moves))
        
        # Look for games that start with the same sequence
        search_pattern = current_str + "%"
        cursor.execute("""
        SELECT moves, winner, count FROM games 
        WHERE moves LIKE ? 
        ORDER BY count DESC
        LIMIT 5
        """, (search_pattern,))
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            return None
        
        # Find winning games for the current player's side
        current_player = "player1" if 0 <= current_moves[-1] <= 5 else "player2"
        next_player = "player2" if current_player == "player1" else "player1"
        
        winning_moves = []
        for moves_str, winner, count in results:
            if winner == next_player:  # Find games where the next player won
                # Extract the next move from this winning game
                all_moves = moves_str.split(";")
                if len(all_moves) > len(current_moves):
                    next_move = int(all_moves[len(current_moves)])
                    winning_moves.append((next_move, count))
        
        if winning_moves:
            # Choose the most common winning next move
            winning_moves.sort(key=lambda x: x[1], reverse=True)
            return winning_moves[0][0]
        
        return None
    
    def get_statistics(self):

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM game_patterns")
        pattern_count = cursor.fetchone()[0]
        
        cursor.execute("""
        SELECT COUNT(DISTINCT board_state) FROM game_patterns
        """)
        unique_positions = cursor.fetchone()[0]
        
        cursor.execute("""
        SELECT SUM(play_count) FROM game_patterns
        """)
        total_moves = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT COUNT(*) FROM move_sequences")
        sequence_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM move_responses")
        response_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "pattern_count": pattern_count,
            "unique_positions": unique_positions,
            "total_moves": total_moves,
            "sequence_count": sequence_count,
            "response_count": response_count
        }