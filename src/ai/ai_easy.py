import random
import sqlite3
import numpy as np
import os
from pathlib import Path
from src.game.game_memory import GameMemory

class AIEasy:
    def __init__(self, player="player2"):
        self.player = player
        self.memory = GameMemory()
        self.current_game = []  # Pour enregistrer les coups de la partie en cours
    
    def choose_move(self, mancala):
        # Enregistrer l'état actuel
        current_board = mancala.board.copy()
        
        # D'abord, rechercher un coup basé sur les parties gagnées précédentes
        move = self.memory.find_similar_game(self.current_game)
        
        # Vérifier si le coup est valide
        if move is not None:
            # Vérifier que le coup est valide pour le joueur actuel
            if self.player == "player1" and 0 <= move <= 5 and mancala.board[move] > 0:
                # Enregistrer ce coup dans l'historique de la partie en cours
                self.current_game.append(move)
                return move
            elif self.player == "player2" and 7 <= move <= 12 and mancala.board[move] > 0:
                # Enregistrer ce coup dans l'historique de la partie en cours
                self.current_game.append(move)
                return move
        
        # Sinon, choisir un coup aléatoire
        move = self._choose_random_move(mancala)
        if move >= 0:
            # Enregistrer ce coup dans l'historique de la partie en cours
            self.current_game.append(move)
        return move
    
    def _choose_random_move(self, mancala):
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
        if self.current_game:
            # Utiliser la méthode store_game de GameMemory
            self.memory.store_game(self.current_game, winner)
            # Réinitialiser pour la prochaine partie
            self.current_game = []