import numpy as np

class MancalaPlatter:
    """Classe représentant le plateau du jeu Mancala."""
    
    def __init__(self):
        """Initialise un nouveau plateau de jeu Mancala."""
        # 6 trous + 1 kalaha par joueur
        self.board = np.array([4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0])
        self.current_player = "player1"
        self.player1_kalahas = 6
        self.player2_kalahas = 13
        self.player1_wells = range(0, 6)
        self.player2_wells = range(7, 13)
        self.finish_game = False

    def __str__(self):
        """Retourne une représentation textuelle du plateau."""
        return str(self.board)

    def make_move(self, index):
        """Effectue un coup à partir du trou sélectionné."""
        if self.finish_game or index not in range(12) or self.board[index] == 0:
            return
        self.make_move_helper(index)

    def make_move_helper(self,index):
        if self.finish_game:
            return False
        stones = self.board[index]
        self.board[index] = 0
        while stones > 0:
            index = (index + 1) % 14
            if (index == self.player1_kalahas and self.current_player == "player2") or(index == self.player2_kalahas and self.current_player == "player1"): ##metre l'index du tableau peut-etre (player 2 si on n'est usr cette case)
                continue
            else:
                self.board[index] += 1
                stones -= 1
        # Capture si la dernière graine tombe dans un trou vide du joueur actuel
        oponent_index = 12 - index
        if (index < self.player1_kalahas and self.board[index] == 1 and self.board[oponent_index] > 0 and self.current_player == "player1"):
            self.board[self.player1_kalahas] += self.board[oponent_index] + 1
            self.board[index] = 0
            self.board[oponent_index] = 0
        # Vérifier si le jeu est terminé
        self.check_game_over()
        # Changer de joueur sauf si la dernière graine tombe dans son propre kalaha
        if index != self.player1_kalahas or index != self.player2_kalahas:
            self.current_player = "player2" if self.current_player == "player1" else "player1"


    def check_game_over(self):
        """Check if the game is over (one player has no stones in their pits)"""
        player1_stones = self.board[self.player1_wells].sum()
        player2_stones = self.board[self.player2_wells].sum()
        
        if player1_stones == 0 or player2_stones == 0:
            self.board[self.player1_kalahas] += player1_stones
            self.board[self.player2_kalahas] += player2_stones
            self.board[self.player1_wells] = 0
            self.board[self.player2_wells] = 0
            self.finish_game = True
        return self.finish_game
    def get_score(self, player):
        """Get the current score for the given player"""
        if player == "player1":
            return self.board[6]  # Player 1's store
        else:  # player2
            return self.board[13]  # Player 2's store
