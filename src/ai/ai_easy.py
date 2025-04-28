import random
from src.game.game_memory import GameMemory
from src.ai.base_ai import BaseAI

class AIEasy(BaseAI):
    """IA simple qui utilise l'historique ou joue aléatoirement."""
    
    def __init__(self, player="player2"):
        """Initialise l'IA facile."""
        super().__init__(player)
        self.memory = GameMemory()
    
    def choose_move(self, mancala):
        """
        Choisit le meilleur coup basé sur l'historique ou aléatoirement.
        
        Args:
            mancala: L'instance du plateau de jeu Mancala
            
        Returns:
            int: L'index du coup à jouer
        """
        # D'abord, rechercher un coup basé sur les parties gagnées précédentes
        move = self.memory.find_similar_game(self.current_game)
        
        # Vérifier si le coup est valide
        if move is not None:
            # Vérifier que le coup est valide pour le joueur actuel
            if self.player == "player1" and 0 <= move <= 5 and mancala.board[move] > 0:
                self.current_game.append(move)
                return move
            elif self.player == "player2" and 7 <= move <= 12 and mancala.board[move] > 0:
                self.current_game.append(move)
                return move
        
        # Sinon, choisir un coup aléatoire
        move = self._choose_random_move(mancala)
        if move >= 0:
            self.current_game.append(move)
            
        return move
    
    def _choose_random_move(self, mancala):
        """
        Choisit un coup aléatoire parmi les coups valides.
        
        Args:
            mancala: L'instance du plateau de jeu Mancala
            
        Returns:
            int: L'index du coup à jouer
        """
        valid_moves = []
        
        # Déterminer les trous valides selon le joueur
        if self.player == "player1":
            well_range = range(0, 6)
        else:  # player2
            well_range = range(7, 13)
        
        # Collecter tous les coups valides (trous non vides)
        for i in well_range:
            if mancala.board[i] > 0:
                valid_moves.append(i)
        
        # Choisir aléatoirement parmi les coups valides
        if valid_moves:
            return random.choice(valid_moves)
        
        # Si aucun coup valide (ne devrait pas arriver normalement)
        return -1
    
    def record_game_result(self, winner):
        """
        Enregistre le résultat d'une partie terminée.
        
        Args:
            winner: Le joueur qui a gagné ("player1" ou "player2")
        """
        if self.current_game:
            self.memory.store_game(self.current_game, winner)
            # Réinitialiser pour la prochaine partie
            super().record_game_result(winner)