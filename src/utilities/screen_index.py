import pygame
from src.utilities.button import Button

class BaseScreen:
    """
    Base screen class that can be inherited by other screens to avoid code repetition.
    Includes common functionality like menu and quit buttons at the bottom of the screen.
    """
    def __init__(self, screen=None, screen_width=800, screen_height=600):
        """Initialize the base screen with common properties"""
        self.screen_width = screen_width
        self.screen_height = screen_height
        if screen is None:
            self.screen = pygame.display.set_mode((screen_width, screen_height))
        else:
            self.screen = screen
            
        # Chargement des polices
        self.title_font = pygame.font.SysFont("Arial", 36, bold=True)
        self.font = pygame.font.SysFont("Arial", 24)
        self.small_font = pygame.font.SysFont("Arial", 18)
        # Couleurs
        self.Beige = (240, 230, 200)  # Beige clair ##background color
        self.Gris = (50, 50, 50)   # Gris foncé  ##button color
        self.Marron = (180, 140, 100)  # Marron clair ##hover button
        self.Dark_Gris = (80, 80, 80)   # Gris foncé ##text color
        self.Or = (255, 215, 0)  # Or ##text button
        self.Vert = (120, 180, 120)  # Vert clair
        self.Dark_Vert = (100, 160, 100)  # Vert un peu plus foncé
        
        # Common buttons (menu and quit)
        button_width = 120
        button_height = 40
        button_y = screen_height - 50  # 50px from bottom
        
        self.menu_button = Button(
            20,  # Left margin
            button_y,
            button_width,
            button_height,
            "Menu",
            self.Gris,
            self.Marron,
            self.Or,
            action=self.return_to_menu
        )
        
        self.quit_button = Button(
            screen_width - 20 - button_width,  # Right margin
            button_y,
            button_width,
            button_height,
            "Quitter",
            self.Gris,
            self.Marron,
            self.Or,
            action=self.quit_game
        )
        
        self.active = True
    
    def return_to_menu(self):
        """Return to the main menu"""
        self.active = False
        from src.ui.screen_menu import MenuScreen
        MenuScreen().run()
        return "menu"
    
    def quit_game(self):
        """Quit the game"""
        self.active = False
        return "quit"
    
    def handle_common_events(self, event):
        """Handle common events for all screens"""
        if event.type == pygame.QUIT:
            self.active = False
            return "quit"
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                pos = pygame.mouse.get_pos()
                if self.menu_button.collidepoint(pos):
                    return self.return_to_menu()
                if self.quit_button.collidepoint(pos):
                    return self.quit_game()
        
        return None
    
    def draw_common_elements(self):
        """Draw elements common to all screens"""
        # Update button states
        mouse_pos = pygame.mouse.get_pos()
        self.menu_button.update(mouse_pos)
        self.quit_button.update(mouse_pos)
        
        # Draw buttons
        self.quit_button.draw(self.screen)
        self.menu_button.draw(self.screen)
        
    def draw_screen(self):
        """Base draw method to be overridden by child classes"""
        pass
    def run(self):
        """Base run method to be overridden by child classes"""
        clock = pygame.time.Clock()

        while self.active:
            # Handle events
            for event in pygame.event.get():
                result = self.handle_common_events(event)
                if result:
                    return result
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button.rect.collidepoint(pos):
                            button.action()
            
            # Clear the screen
            self.screen.fill(self.Beige)
            self.draw_screen()
            # Draw common elements
            self.draw_common_elements()
            
            # Update the display
            pygame.display.flip()
            clock.tick(60)
        
        return None