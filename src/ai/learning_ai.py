import random
from src.game.game_memory import GameMemory
from src.ai.base_ai import BaseAI

class LearningAI(BaseAI):
    """IA avancée qui apprend des parties précédentes et applique des stratégies."""
    
    def __init__(self, player="player2"):
        """Initialise l'IA apprenante."""
        super().__init__(player)
        self.memory = GameMemory()
    
    def choose_move(self, mancala):
        """
        Détermine le meilleur coup à jouer en fonction de l'état actuel du jeu.
        
        Args:
            mancala: L'instance du plateau de jeu Mancala
            
        Returns:
            int: L'index du coup à jouer
        """
        # D'abord, essayer de trouver un coup similaire dans la mémoire
        next_move = self.memory.find_similar_game(self.current_game)
        
        # Vérifier si le coup suggéré est valide
        if next_move is not None:
            if self.player == "player1" and 0 <= next_move <= 5 and mancala.board[next_move] > 0:
                self.current_game.append(next_move)
                return next_move
            elif self.player == "player2" and 7 <= next_move <= 12 and mancala.board[next_move] > 0:
                self.current_game.append(next_move)
                return next_move
        
        # Utiliser une stratégie de repli si aucun coup n'est trouvé dans l'historique
        move = self._choose_strategic_move(mancala)
        if move >= 0:
            self.current_game.append(move)
            
        return move
    
    def _choose_strategic_move(self, mancala):
        """
        Choisit un coup stratégique lorsque l'historique ne fournit pas de suggestion.
        
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
        
        # 1. D'abord, chercher un coup qui donne un tour supplémentaire
        for i in well_range:
            if mancala.board[i] > 0:
                # Calculer où la dernière graine atterrira
                distance = mancala.board[i]
                landing = (i + distance) % 14
                
                # Vérifier si le dernier grain tombe dans le kalaha du joueur
                if (self.player == "player1" and landing == 6) or \
                   (self.player == "player2" and landing == 13):
                    return i
                
                # Ajouter aux coups valides pour une sélection ultérieure
                valid_moves.append(i)
        
        # 2. Ensuite, essayer de maximiser le nombre de graines collectées
        best_score = -1
        best_move = -1
        
        for move in valid_moves:
            # Simple heuristique: préférer les puits avec plus de graines
            score = mancala.board[move]
            if score > best_score:
                best_score = score
                best_move = move
        
        if best_move >= 0:
            return best_move
        
        # 3. Enfin, choisir un coup aléatoire parmi les valides
        if valid_moves:
            return random.choice(valid_moves)
        
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