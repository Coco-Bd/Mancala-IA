import pygame
from pygame.locals import MOUSEBUTTONDOWN
#from src.ui.screen_mancala import GameScreen
#from src.game.mancala import GameTable
from src.utilities.button import Button

from src.ui.screen_mancala import MancalaScreen   
from src.ui.screen_statistic import StatisticScreen
from src.ui.screen_settings import SettingsScreen

from src.utilities.screen_index import BaseScreen
class MenuScreen(BaseScreen):
    def __init__(self,screen=None, screen_width=800, screen_height=600):
        # Initialiser la classe parente
        super().__init__(screen, screen_width, screen_height)
        pygame.display.set_caption("Mancala")
        
        # Colors
        button_width = 200
        button_height = 60
        center_x = self.screen_width // 2 - button_width // 2
        
        # Buttons
        self.buttons = [
            Button(center_x, self.screen_height//2 - 100, button_width, button_height, "Play",  self.Gris,self.Marron,self.Or, action=self.play_game),
            Button(center_x, self.screen_height//2, button_width, button_height, "Statistics", self.Gris,self.Marron,self.Or, action=self.show_statistics),
            Button(center_x, self.screen_height//2 + 100, button_width, button_height, "settings", self.Gris,self.Marron,self.Or, action=self.settings),
        ]
        
        self.active = True
        
    
    def play_game(self):
        self.active = False  # Close the menu screen
        # Initialize game screen with current screen dimensions
        return MancalaScreen(self.screen, self.screen_width, self.screen_height).run()
    def show_statistics(self):
        # Add code to transition to the statistics screen
        return StatisticScreen('db/games.db').display_statistics() #gange a name of the database
    
    def settings(self):
        # Add code to transition to the settings screen
        return SettingsScreen(self.screen, self.screen_width, self.screen_height).run()
    
    def run(self):
        clock = pygame.time.Clock()
        while self.active:
            # Handle events
            for event in pygame.event.get():
                # Handle common events (quit, menu, etc.)
                common_result = self.handle_common_events(event)
                if common_result:
                    return common_result
                
                # Handle specific button clicks for this screen
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button.rect.collidepoint(pos):
                            return button.action()
            
            # Clear the screen
            self.screen.fill(self.Beige)
            
            # Draw the title
            title = self.title_font.render("Mancala", True, self.Dark_Gris)
            self.screen.blit(title, (self.screen_width//2 - title.get_width()//2, 50))
            
            # Draw buttons and update their states
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.update(mouse_pos)
                button.draw(self.screen)

            # Draw the quit button
            self.quit_button.draw(self.screen)
            pygame.display.flip()
            clock.tick(60)
        
        return "quit"