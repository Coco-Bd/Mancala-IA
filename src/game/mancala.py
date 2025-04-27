import numpy as np

class MancalaPlatter:
    """Classe représentant le plateau du jeu Mancala."""
    
    def __init__(self):
        """Initialise un nouveau plateau de jeu Mancala."""
        # 6 trous + 1 kalaha par joueur
        self.board = np.array([4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0])
        self.current_player = "player1"
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
        stones = self.board[index]
        self.board[index] = 0
        while stones > 0:
            index = (index + 1) % 14
            if (index == 7 and self.current_player == "player2") or(index == 14 and self.current_player == "player1"): ##metre l'index du tableau peut-etre (player 2 si on n'est usr cette case)
                continue
            else:
                self.board[index] += 1
                stones -= 1
        # Capture si la dernière graine tombe dans un trou vide du joueur actuel
        oponent_index = 12 - index
        if (index < 6 and self.board[index] == 1 and self.board[oponent_index] > 0 and self.current_player == "player1"):
            self.board[6] += self.board[oponent_index] + 1
            self.board[index] = 0
            self.board[oponent_index] = 0
        # Vérifier si le jeu est terminé
        if self.board[:6].sum() == 0 or self.board[7:14].sum() == 0:
            self.finish_game = True
        # Changer de joueur sauf si la dernière graine tombe dans son propre kalaha
        if index != 6 or index != 13:
            self.current_player = "player2" if self.current_player == "player1" else "player1"







    """def make_move_helper(self, pit_index):
    ###Distribue les graines sur le plateau.###
        player = self.current_player
        opponent = "player2" if player == "player1" else "player1"
        stones = self.board.loc[player, pit_index]
        self.board.loc[player, pit_index] = 0
        index = pit_index
        print("stones:",stones,"index:",index)
        while stones > 0:
            index = (index + 1) % 7  # Passer au trou suivant
            print("index:",index)
            # Ne pas déposer dans le kalaha adverse
            if index == 6 and player != self.current_player:
                continue
            
            self.board.loc[player if index < 6 else opponent][index] += 1
            stones -= 1

        # Capture si la dernière graine tombe dans un trou vide du joueur actuel
        if index < 6 and self.board.loc[player, index] == 1 and self.board.loc[opponent, 5 - index] > 0:
            self.board.loc[player, 6] += self.board.loc[opponent, 5 - index] + 1
            self.board.loc[player, index] = 0
            self.board.loc[opponent, 5 - index] = 0

        # Vérifier si le jeu est terminé
        if self.board.loc[player, :6].sum() == 0 or self.board.loc[opponent, :6].sum() == 0:
            self.game_over = True

        # Changer de joueur sauf si la dernière graine tombe dans son propre kalaha
        if index != 6:
            self.current_player = opponent

"""