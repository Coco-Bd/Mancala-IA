import pygame
import sys
from pygame.locals import *
##from src.ui.screen_mancala import MancalaScreen
##from src.game.mancala import MancalaBoard
from src.utilities.button import Button
import pandas as pd
class MenuScreen:
    def __init__(self, screen_width=800, screen_height=600):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Tic Tac Toe - Menu")
        
        # Colors
        self.bg_color = (50, 50, 70)
        self.button_color = (100, 100, 180)
        self.hover_color = (120, 120, 200)
        self.text_color = (255, 255, 255)



        # Chargement des polices
        self.title_font = pygame.font.SysFont("Arial", 36, bold=True)
        self.font = pygame.font.SysFont("Arial", 24)
        self.small_font = pygame.font.SysFont("Arial", 18)
        # Couleurs
        self.Beige = (240, 230, 200)  # Beige clair
        self.Gris = (50, 50, 50)   # Gris foncé  ##button color
        self.Marron = (180, 140, 100)  # Marron clair ##hover button
        self.Dark_Gris = (80, 80, 80)   # Gris foncé
        self.Or = (255, 215, 0)  # Or ##text button
        self.Vert = (120, 180, 120)  # Vert clair
        self.Dark_Vert = (100, 160, 100)  # Vert un peu plus foncé
        
        # Font
        self.font = pygame.font.SysFont(None, 48)
        
        # Buttons
        self.buttons = [
            Button(self.screen_width//2 - 100, self.screen_height//2 - 70, 200, 60, "Play", self.Gris, self.Marron, self.Or, action=self.play_game),
            Button(self.screen_width//2 - 100, self.screen_height//2, 200, 60, "Statistics", self.Gris, self.Marron, self.Or, action=self.show_statistics),
            Button(self.screen_width//2 - 100, self.screen_height//2 + 70, 200, 60, "Leave", self.Gris, self.Marron, self.Or, action=self.quit_game)
        ]
        self.active = True

    def play_game(self):
        print("Starting game...")
        self.active = False  # Close the menu screen
        # Initialize game screen with current screen dimensions
        return 
        ##return MancalaScreen(self.screen, self.screen_width, self.screen_height).draw(MancalaBoard())
    def show_statistics(self):
        print("Showing statistics...")
        # Add code to transition to the statistics screen
        return "statistics"
    
    def quit_game(self):
        print("Quitting game...")
        self.active = False
        return "quit"
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.active = False
                return "quit"
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button.rect.collidepoint(pos):
                            return button.action()
                            
        return None
    
    def run(self):
        clock = pygame.time.Clock()
        
        while self.active:
            # Handle events
            result = self.handle_events()
            if result:
                return result
            
            # Draw
            self.screen.fill(self.Beige)
            title = self.title_font.render("MANCALA", True, self.Gris)
            self.screen.blit(title, (self.width//2 - title.get_width()//2, 50))
            for button in self.buttons:
                button.update(pygame.mouse.get_pos())
                button.draw(self.screen)
            
            pygame.display.flip()
            clock.tick(60)
        
        return "quit"
    
        """ def Menu(self):

        while self.in_menu and running:
            # Gérer les événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
            # Effacer l'écran et dessiner le fond
            self.screen.fill(self.Beige)
            
            # Titre du jeu
            title = self.title_font.render("MANCALA", True, self.Gris)
            self.screen.blit(title, (self.width//2 - title.get_width()//2, 50))
            
            # Création des boutons
            play_rect = pygame.Rect(self.width//2 - 100, self.height//2 - 70, 200, 60)
            options_rect = pygame.Rect(self.width//2 - 100, self.height//2, 200, 60)
            quit_rect = pygame.Rect(self.width//2 - 100, self.height//2 + 70, 200, 60)
            
            # Afficher et vérifier les interactions avec les boutons
            self.create_button("Jouer", play_rect, lambda: self.exit_menu_to_game())
            self.create_button("Options", options_rect, lambda: self.show_options())
            self.create_button("Quitter", quit_rect, lambda: self.quit_game())
            """