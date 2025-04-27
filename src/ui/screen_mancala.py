import pygame
from src.utilities.screen_index import BaseScreen
from src.game.mancala import MancalaPlatter
from src.utilities.button import Button
class MancalaScreen(BaseScreen):
    """Écran de jeu pour le Mancala avec une représentation logique de la direction du jeu."""
    
    def __init__(self, screen=None, screen_width=800, screen_height=600):
        """Initialise l'écran du jeu Mancala."""
        super().__init__(screen, screen_width, screen_height)
        pygame.display.set_caption("Mancala")
        self.mancala = MancalaPlatter()
        self.kalaha_color = (255, 215, 0)
        self.well_color = (139, 69, 19)
        self.stone_color = (255, 0, 0)
        self.kalaha_width = 100
        self.kalaha_height = 200
        self.well_width = 80
        self.well_height = 80
        self.kalaha_x = [self.screen_width - self.kalaha_width - 20,20]
        self.kalaha_y = [self.screen_height // 2 - self.kalaha_height // 2, self.screen_height // 2 - self.kalaha_height // 2]
        self.pit_x = [self.kalaha_x[1] + self.well_width - 20, 
                self.kalaha_x[1] + 2 * (self.well_width + 20), 
                self.kalaha_x[1] + 3 * (self.well_width + 20), 
                self.kalaha_x[1] + 4 * (self.well_width + 20), 
                self.kalaha_x[1] + 5 * (self.well_width + 20), 
                self.kalaha_x[1] + 6 * (self.well_width + 20)]
        self.buttons = self.create_wall()
    def draw_screen(self):
        title = self.title_font.render("Mancala", True, (80, 80, 80))
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 20))
        self.draw_kalahas()
        self.update_score()
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)
            button.draw(self.screen)
        self.light_well()
        #self.draw_stones()


    def draw_kalahas(self):
        pygame.draw.rect(self.screen, self.kalaha_color, (self.kalaha_x[0], self.kalaha_y[0], self.kalaha_width, self.kalaha_height))
        pygame.draw.rect(self.screen, self.kalaha_color, (self.kalaha_x[1], self.kalaha_y[1], self.kalaha_width, self.kalaha_height))
    
    def create_wall(self):
        buttons = []
        for index in range(len(self.pit_x)):
            # Draw player 1 wells (top row)
            buttons.append(Button(self.pit_x[index] + 40, self.kalaha_y[0] - self.well_height + 90, 
               60, 60, str(self.mancala.board[index]), 
              color=self.well_color, hover_color=(180, 140, 100), 
              text_color=(255, 215, 0), font_size=24,
              action=lambda i=index: self.select_well(i)))
        for index in range(len(self.pit_x)):
            # Draw player 2 wells (bottom row)
            buttons.append(Button(self.pit_x[-index-1] + 40, self.kalaha_y[0] + self.well_height + 50, 
               60, 60, str(self.mancala.board[index+7]), 
              color=self.well_color, hover_color=(180, 140, 100), 
              text_color=(255, 215, 0), font_size=24,
              action=lambda i=index: self.select_well(i+7)))
            
        return buttons
    
    def select_well(self, index):
        if self.mancala.finish_game:
            return
        if ((self.mancala.current_player == "player1" and index in range(6)) or (self.mancala.current_player == "player2" and index in range(7, 14))) and self.mancala.board[index] > 0:
            self.mancala.make_move_helper(index)
        else:
            print("Invalid selection")

    def update_score(self):
        # Update the button text to reflect the current state of the game
        for index in range(len(self.buttons)):
            if index < 6:
                self.buttons[index].text = str(self.mancala.board[index])
            else:
                self.buttons[index].text = str(self.mancala.board[index+1])
        # Player 1 score (right kalaha)
        score1_text = self.font.render(str(self.mancala.board[6]), True, (255, 255, 255))
        score1_x = self.kalaha_x[0] + (self.kalaha_width - score1_text.get_width()) // 2
        score1_y = self.kalaha_y[0] + (self.kalaha_height - score1_text.get_height()) // 2
        self.screen.blit(score1_text, (score1_x, score1_y))

        # Player 2 score (left kalaha)
        score2_text = self.font.render(str(self.mancala.board[13]), True, (255, 255, 255))
        score2_x = self.kalaha_x[1] + (self.kalaha_width - score2_text.get_width()) // 2
        score2_y = self.kalaha_y[1] + (self.kalaha_height - score2_text.get_height()) // 2
        self.screen.blit(score2_text, (score2_x, score2_y))
       
        

        
    """def draw_stones(self):
        for i in range(len(self.mancala.board)):
            for j in range(self.mancala.board[i]):
                # Calculate the position of each stone
                x = self.pit_x[i] + (j % 2) * (self.well_width // 2)
                y = self.pit_y[i] + (j // 2) * (self.well_height // 2)
                pygame.draw.circle(self.screen, self.stone_color, (x, y), self.stone_radius)
                """

    def light_well(self):
        # Get the current player
        well_highlight_color = (255, 255, 0)  # Yellow highlight
        well_highlight_width = 3  # Width of the highlight border

        for index in range(6):
            # Calculate positions for both players' wells
            player1_well_pos = (self.pit_x[-index] + 40, self.kalaha_y[0] - self.well_height + 90, 60, 60)
            player2_well_pos = (self.pit_x[-index] + 40, self.kalaha_y[0] + self.well_height + 50, 60, 60)
            
            # Highlight wells based on current player
            if not self.mancala.finish_game:
                if self.mancala.current_player == "player1" and self.mancala.board[index] > 0:
                    # Highlight player 1's wells
                    pygame.draw.rect(self.screen, well_highlight_color, player1_well_pos, well_highlight_width)
                elif self.mancala.current_player == "player2" and self.mancala.board[index+7] > 0:
                    # Highlight player 2's wells
                    pygame.draw.rect(self.screen, well_highlight_color, player2_well_pos, well_highlight_width)
        