import sqlite3
import numpy as np
from pathlib import Path

import matplotlib.pyplot as plt

class StatisticScreen:
    def __init__(self, db_path):
        self.db_path = db_path
        
    def display_statistics(self):
        # Create PyQt UI elements for the buttons
        
        # Create the database connection
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Query to get counts of each outcome
        cursor.execute("SELECT winner, COUNT(*) FROM games GROUP BY winner")
        results = cursor.fetchall()
        
        # Initialize counters
        x_wins = 0
        o_wins = 0
        Egalites = 0
        
        # Process results
        for winner, count in results:
            if winner == 'X':
                x_wins = count
            elif winner == 'O':
                o_wins = count
            elif winner == 'Egalite':
                Egalites = count
        
        conn.close()
        
        # Create bar chart
        categories = ['X Wins', 'O Wins', 'Egalite']
        values = [x_wins, o_wins, Egalites]
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(categories, values, color=['blue', 'red', 'green'])
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{height}', ha='center', va='bottom')
        
        plt.title('Tic-Tac-Toe Statistics')
        plt.xlabel('Outcome')
        plt.ylabel('Number of Games')
        plt.tight_layout()
        
        plt.show()
