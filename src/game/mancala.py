import pandas as pd

class MancalaBoard:
    """Classe représentant le plateau du jeu Mancala."""
    
    def __init__(self):
        """Initialise un nouveau plateau de jeu Mancala."""
        # 6 trous + 1 kalaha par joueur
        self.board = pd.DataFrame([[4] * 6 + [0], [4] * 6 + [0]], index=["player1", "player2"], columns=range(7))
        self.current_player = "player1"
        self.game_over = False

    def __str__(self):
        """Retourne une représentation textuelle du plateau."""
        return str(self.board)


    def make_move(self, pit_index):
        """Effectue un coup à partir du trou sélectionné."""
        if self.game_over or pit_index not in range(6) or self.board.loc[self.current_player, pit_index] == 0:
            return

        self.make_move_helper(pit_index)

    def make_move_helper(self,index):
        actual_player = self.current_player
        other_player = "player2" if self.current_player == "player1" else "player1"
        stones = self.board.loc[self.current_player, index]
        self.board.loc[self.current_player, index] = 0
        while stones > 0:
            if index == 6:
                index = -1
                self.current_player = "player2" if self.current_player == "player1" else "player1"
            index += 1
            if index == 6 and self.current_player == other_player: ##metre l'index du tableau peut-etre (player 2 si on n'est usr cette case)
                continue
            self.board.loc[self.current_player, index] += 1
            stones -= 1


        # Capture si la dernière graine tombe dans un trou vide du joueur actuel
        if index < 6 and self.board.loc[actual_player, index] == 1 and self.board.loc[other_player, 5 - index] > 0:
            self.board.loc[actual_player, 6] += self.board.loc[other_player, 5 - index] + 1
            self.board.loc[actual_player, index] = 0
            self.board.loc[other_player, 5 - index] = 0
        # Vérifier si le jeu est terminé
        if self.board.loc[actual_player, :6].sum() == 0 or self.board.loc[other_player, :6].sum() == 0:
            self.game_over = True
        # Changer de joueur sauf si la dernière graine tombe dans son propre kalaha
        if index != 6:
            self.current_player = other_player







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