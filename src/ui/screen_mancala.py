import pygame
import pandas as pd
from src.game.mancala import MancalaBoard
from src.utilities.button import Button
from src.utilities.screen_index import BaseScreen

class MancalaScreen(BaseScreen):
    def __init__(self, screen, screen_width, screen_height):
        super().__init__(screen, screen_width, screen_height)
        pygame.display.set_caption("Mancala - Jeu")
        
        