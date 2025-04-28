from src.ai.learning_ai import LearningAI
from src.ai.ai_easy import AIEasy

class AIGame:
    """Contrôleur principal pour gérer le jeu avec une IA."""
    
    def __init__(self, mancala, ai_type="Human", player="player2"):
        """
        Initialise le contrôleur de jeu avec l'IA spécifiée.
        
        Args:
            mancala: L'instance du plateau de jeu
            ai_type: Le type d'IA à utiliser ("learning" ou "easy")
        """
        self.board = mancala 
        self.ai_active = False
        
        if ai_type == "Human":
            return  
        self.ai_active = True
        
        # Sélectionner le type d'IA approprié
        if ai_type.lower() == "Easy_AI":
            self.ai = AIEasy(player)
        else:
            self.ai = LearningAI(player)
    
    def set_ai_player(self, player):
        """Définit pour quel joueur l'IA joue."""
        if not self.ai_active:
            return
        self.ai.player = player
        
    def player_move(self, pit_index):
        """Gère un mouvement du joueur humain."""
        if pit_index is None or self.board.finish_game:
            return False
            
        result = self.board.make_move_helper(pit_index)
        
        # Enregistrer ce coup dans la mémoire de l'IA
        if result:
            self.ai.current_game.append(pit_index)
        
        # Vérifier si la partie est terminée après le coup du joueur
        if self.board.finish_game:
            winner = self.determine_winner()
            self.ai.record_game_result(winner)
            
        return result
    
    def ai_move(self):
        """Gère le mouvement de l'IA."""
        if not self.ai_active:
            return
            
        # L'IA décide d'un coup
        move = self.ai.choose_move(self.board)
        
        if move is not None:
            # Effectuer le coup
            self.board.make_move_helper(move)
            
        else:
            # Aucun coup valide disponible pour l'IA, la partie devrait se terminer
            print("L'IA n'a pas de coup valide. Fin de partie.")
            self.board.finish_game = True
        
        # Vérifier si la partie est terminée
        if self.board.finish_game:
            winner = self.determine_winner()
            self.ai.record_game_result(winner)
    
    def determine_winner(self):
        """Détermine le gagnant de la partie."""
        score_p1 = self.board.get_score("player1")
        score_p2 = self.board.get_score("player2")
        
        if score_p1 > score_p2:
            return "player1"
        elif score_p2 > score_p1:
            return "player2"
        else:
            return "draw"