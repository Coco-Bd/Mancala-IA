import sqlite3
import os
from pathlib import Path

class GameMemory:
    """Gère l'enregistrement et la récupération des données de jeu."""
    
    def __init__(self, db_path=None):
        """
        Initialise la connexion à la base de données de mémoire de jeu.
        
        Args:
            db_path: Chemin vers la base de données (facultatif)
        """
        if db_path is None:
            # Chemin par défaut relatif au dossier du projet
            base_dir = Path(__file__).parent.parent.parent
            self.db_path = os.path.join(base_dir, "db", "mancala_ai.db")
        else:
            self.db_path = db_path
            
        # S'assurer que le répertoire de la base de données existe
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        self._initialize_db()
    
    def _initialize_db(self):
        """Configure la table de base de données si elle n'existe pas."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table simple pour les jeux
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            moves TEXT,         -- Chaîne simple comme "4;8;2;9;5;7"
            winner TEXT,        -- "player1" ou "player2"
            count INTEGER DEFAULT 1
        )
        """)
        
        # Créer un index pour des recherches plus rapides
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_moves ON games(moves)")
        
        conn.commit()
        conn.close()
    
    def store_game(self, moves, winner):
        """
        Enregistre une partie terminée dans la base de données.
        
        Args:
            moves: Liste des coups joués
            winner: Le joueur gagnant ("player1" ou "player2")
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Convertir les coups en une chaîne simple comme "4;8;2;9"
        moves_str = ";".join(map(str, moves))
        
        # Vérifier si nous avons déjà vu cette partie exacte
        cursor.execute("SELECT id, count FROM games WHERE moves = ?", (moves_str,))
        result = cursor.fetchone()
        
        if result:
            # Mettre à jour le nombre d'occurrences pour cette partie
            game_id, count = result
            cursor.execute("UPDATE games SET count = ? WHERE id = ?", (count + 1, game_id))
        else:
            # Enregistrer une nouvelle partie
            cursor.execute("INSERT INTO games (moves, winner, count) VALUES (?, ?, 1)", 
                          (moves_str, winner))
        
        conn.commit()
        conn.close()
    
    def find_similar_game(self, current_moves):
        """
        Recherche une partie similaire dans l'historique.
        
        Args:
            current_moves: Coups joués jusqu'à présent
            
        Returns:
            int ou None: Le prochain coup suggéré ou None si aucune correspondance
        """
        if not current_moves:
            return None
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Convertir les coups actuels en chaîne
        current_str = ";".join(map(str, current_moves))
        
        # Rechercher des parties qui commencent par la même séquence
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
        
        # Déterminer le joueur actuel basé sur le dernier coup
        current_player = "player1" if len(current_moves) % 2 == 0 else "player2"
        
        winning_moves = []
        for moves_str, winner, count in results:
            if winner == current_player:  # Trouver des parties où le joueur actuel a gagné
                # Extraire le prochain coup de cette partie gagnante
                all_moves = moves_str.split(";")
                if len(all_moves) > len(current_moves):
                    next_move = int(all_moves[len(current_moves)])
                    winning_moves.append((next_move, count))
        
        if winning_moves:
            # Choisir le coup suivant gagnant le plus courant
            winning_moves.sort(key=lambda x: x[1], reverse=True)
            return winning_moves[0][0]
        
        return None