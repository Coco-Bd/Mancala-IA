class BaseAI:
    """Classe de base pour toutes les intelligences artificielles du jeu Mancala."""
    
    def __init__(self, player="player2"):
        self.player = player
        self.current_game = []  # Pour enregistrer les coups de la partie en cours
    
    def choose_move(self, mancala):
        """Méthode à implémenter par les sous-classes pour choisir un coup."""
        raise NotImplementedError("Les sous-classes doivent implémenter cette méthode")
    
    def record_game_result(self, winner):
        """Enregistre le résultat de la partie. À personnaliser dans les sous-classes."""
        self.current_game = []  # Réinitialiser pour la prochaine partie