"""
import sys
import os

# Ajouter le chemin du projet au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import correct depuis le dossier ui
from src.game.mancala import MancalaBoard

def main():
    # Créer un jeu avec les dimensions par défaut
    ##game_display = MancalaUI()
    
    # Lancer la boucle de jeu
    ###game_display.run()
    # Test du jeu
    jeu = MancalaBoard()
    print("===\n",jeu,"\n===")

    jeu.make_move(2)  # Joueur 1 joue
    print(jeu)

    jeu.make_move(4)  # Joueur 2 joue
    print("===\n",jeu,"\n===")

    jeu.make_move(3)  # Joueur 1 joue
    print("===\n",jeu,"\n===")

if __name__ == "__main__":
    main()
"""

# main.py
from src.ui.screen_menu import MenuScreen
from db.init_db import initialize_files
import pygame
import sys

def main():
    pygame.init()
    initialize_files()
    menu = MenuScreen()
    result = menu.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()