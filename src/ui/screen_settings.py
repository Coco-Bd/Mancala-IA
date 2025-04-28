import pygame
from pygame.locals import MOUSEBUTTONDOWN, KEYDOWN, K_UP, K_DOWN, K_RETURN, K_SPACE
from src.utilities.screen_index import BaseScreen
import json
import os

class SettingsScreen(BaseScreen):
    def __init__(self, screen=None, screen_width=800, screen_height=600):
        # Initialiser la classe parente
        super().__init__(screen, screen_width, screen_height)
        self.title = "Settings"
        
        # Configuration options
        self.options = [
            {"name": "Player 1", "options": ["Human", "Easy AI","Learning AI"], "current": 0},
            {"name": "Player 2", "options": ["Human", "Easy AI","Learning AI"], "current": 0},
        ]
        
        self.selected_option = 0
        self.option_font = pygame.font.Font(None, 32)
        self.description_font = pygame.font.Font(None, 24)
        
        
        # Layout settings
        self.option_spacing = 60
        self.start_y = 120
        self.option_width = 400
        self.option_height = 40
        
        # Cursor (animation)
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_blink_speed = 500  # milliseconds
        
        # Description of options (appears on hover)
        self.descriptions = {
            "Player 1": "Set the first player as human or easy AI or learning AI",
            "Player 2": "Set the second player as human or easy AI or learning AI",
        }
        
        # Currently hovered option
        self.hovered_option = -1

    def run(self):
        """Main loop for the settings screen"""
        clock = pygame.time.Clock()
        last_time = pygame.time.get_ticks()
        
        while self.active:
            current_time = pygame.time.get_ticks()
            
            # Handle events
            result = self.handle_events()
            if result:
                return result
            
            # Update cursor blink
            if current_time - last_time > self.cursor_blink_speed:
                self.cursor_visible = not self.cursor_visible
                last_time = current_time
            
            # Clear the screen
            self.screen.fill(self.Beige)
            
            # Draw the title and options and descriptions
            self.draw_title()
            self.draw_options()
            self.draw_descriptions()
            # Draw common elements (Menu, Quit buttons)
            self.draw_common_elements()
            
            # Mettre à jour l'affichage
            pygame.display.flip()
            clock.tick(60)
        
        return "quit"
    
    def handle_events(self):
        """Handle all events for this screen"""
        for event in pygame.event.get():
            # Handle common events (menu, exit, etc.)
            common_result = self.handle_common_events(event)
            if common_result:
                return common_result
            
            # Handle mouse events
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_mouse_click(event.pos)
                elif event.button == 4:  # Scroll up
                    self.select_previous_option()
                elif event.button == 5: # Scroll down
                    self.select_next_option()
            
            # Handle keyboard events
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    self.select_previous_option()
                elif event.key == K_DOWN:
                    self.select_next_option()
                elif event.key == K_RETURN or event.key == K_SPACE:
                    self.cycle_selected_option()
        
        # Update hovered option
        self.update_hover()
        
        return None
    
    def select_previous_option(self):
        """Select the previous option in the list"""
        self.selected_option = (self.selected_option - 1) % len(self.options)
        # Reset cursor blink
        self.cursor_visible = True
        self.cursor_timer = pygame.time.get_ticks()
    
    def select_next_option(self):
        """Select the next option in the list"""
        self.selected_option = (self.selected_option + 1) % len(self.options)
        # Reset cursor blink
        self.cursor_visible = True
        self.cursor_timer = pygame.time.get_ticks()
    
    def cycle_selected_option(self):
        """Cycle through values for the currently selected option"""
        option = self.options[self.selected_option]
        option["current"] = (option["current"] + 1) % len(option["options"])
        self.save_settings()
    
    def update_hover(self):
        """Update the hovered option based on mouse position"""
        mouse_pos = pygame.mouse.get_pos()
        # Reset hovered option
        self.hovered_option = -1
        
        # Check if mouse is over an option
        for i, option in enumerate(self.options):
            option_rect = pygame.Rect(
                (self.screen_width - self.option_width) // 2,
                self.start_y + i * self.option_spacing,
                self.option_width,
                self.option_height
            )
            
            if option_rect.collidepoint(mouse_pos):
                self.hovered_option = i
                break
    
    def handle_mouse_click(self, pos):
        """Handle mouse clicks on options"""
        # Check if clicked on an option
        for i, option in enumerate(self.options):
            option_rect = pygame.Rect(
                (self.screen_width - self.option_width) // 2,
                self.start_y + i * self.option_spacing,
                self.option_width,
                self.option_height
            )
            
            if option_rect.collidepoint(pos):
                # If click is on the currently selected option, cycle its value
                if i == self.selected_option:
                    self.cycle_selected_option()
                # Otherwise, select this option
                else:
                    self.selected_option = i
                    # Reset cursor blink
                    self.cursor_visible = True
                    self.cursor_timer = pygame.time.get_ticks()
                break
            
            # Check if click is on the left arrow (decrease value)
            left_arrow_rect = pygame.Rect(
                (self.screen_width - self.option_width) // 2 - 30,
                self.start_y + i * self.option_spacing,
                30,
                self.option_height
            )
            
            if left_arrow_rect.collidepoint(pos):
                self.selected_option = i
                option["current"] = (option["current"] - 1) % len(option["options"])
                self.save_settings()
                break
            
            # Check if click is on the right arrow (increase value)
            right_arrow_rect = pygame.Rect(
                (self.screen_width + self.option_width) // 2,
                self.start_y + i * self.option_spacing,
                30,
                self.option_height
            )
            
            if right_arrow_rect.collidepoint(pos):
                self.selected_option = i
                option["current"] = (option["current"] + 1) % len(option["options"])
                self.save_settings()
                break
    
    def draw_title(self):
        """Draw the screen title"""
        title = self.title_font.render(self.title, True, self.Dark_Gris)
        title_rect = title.get_rect(center=(self.screen_width // 2, 50))
        self.screen.blit(title, title_rect)
        
        # Optional: Add a separator line
        pygame.draw.line(
            self.screen,
            self.Beige,
            (self.screen_width // 4, 85),
            (self.screen_width * 3 // 4, 85),
            2
        )
    
    def draw_options(self):
        """Draw all the settings options"""
        for i, option in enumerate(self.options):
            # Determine colors based on selection and hover
            # Use more distinctive colors for better visibility
            if i == self.selected_option:
                name_color = self.Marron  # Keep selected option name in brown
                value_color = (50, 120, 180)  # Blue for selected option value
            elif i == self.hovered_option:
                name_color = (160, 82, 45)  # Sienna - lighter brown for hover
                value_color = (70, 130, 180)  # Steel blue for hover value
            else:
                name_color = (80, 80, 80)  # Darker gray for normal text
                value_color = (100, 100, 100)  # Medium gray for values
            # Calculate the position for the option
            y_pos = self.start_y + i * self.option_spacing
            
            # Draw the option name
            name_text = self.option_font.render(option["name"], True, name_color)
            name_rect = name_text.get_rect(
                midleft=(
                    (self.screen_width - self.option_width) // 2,
                    y_pos + self.option_height // 2
                )
            )
            self.screen.blit(name_text, name_rect)
            
            # Draw the cursor if the option is selected
            if i == self.selected_option and self.cursor_visible:
                cursor_x = name_rect.left - 20
                cursor_y = y_pos + self.option_height // 2
                pygame.draw.polygon(
                    self.screen,
                    self.Marron,
                    [
                        (cursor_x, cursor_y - 10),
                        (cursor_x + 10, cursor_y),
                        (cursor_x, cursor_y + 10)
                    ]
                )
            
            # Load current settings from JSON file if exists
            try:
                settings_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "db", "settings.json")
                if os.path.exists(settings_path):
                    with open(settings_path, 'r') as f:
                        saved_settings = json.load(f)
                        # Update current option if matching setting exists in file
                        option_name = option["name"].lower().replace(" ", "_")
                        if option_name in saved_settings:
                            saved_value = saved_settings[option_name]
                            if saved_value in option["options"]:
                                option["current"] = option["options"].index(saved_value)
            except Exception as e:
                print(f"Error loading settings: {e}")
                
            # Draw the current value
            value = option["options"][option["current"]]
            value_text = self.option_font.render(value, True, value_color)
            value_rect = value_text.get_rect(
                midright=(
                    (self.screen_width + self.option_width) // 2,
                    y_pos + self.option_height // 2
                )
            )
            self.screen.blit(value_text, value_rect)
            
            # Draw arrows for changing values
            left_arrow_x = value_rect.left - 20
            right_arrow_x = value_rect.right + 10
            arrow_y = y_pos + self.option_height // 2
            
            pygame.draw.polygon(
                self.screen,
                value_color,
                [
                    (left_arrow_x, arrow_y),
                    (left_arrow_x - 10, arrow_y - 5),
                    (left_arrow_x - 10, arrow_y + 5)
                ]
            )
            
            pygame.draw.polygon(
                self.screen,
                value_color,
                [
                    (right_arrow_x, arrow_y),
                    (right_arrow_x + 10, arrow_y - 5),
                    (right_arrow_x + 10, arrow_y + 5)
                ]
            )
    
    def draw_descriptions(self):
        """Draw the description for the currently hovered or selected option"""
        # Get the index of the option to show
        index_to_show = self.hovered_option if self.hovered_option >= 0 else self.selected_option
        
        if index_to_show >= 0:
            option = self.options[index_to_show]
            description = self.descriptions.get(option["name"], "")
            
            description_text = self.description_font.render(description, True, self.Gris)
            description_rect = description_text.get_rect(
                center=(self.screen_width // 2, self.start_y + len(self.options) * self.option_spacing + 40)
            )
            self.screen.blit(description_text, description_rect)
    
    def save_settings(self):
        """Save the current settings to a file or database"""
        # Implement saving logic here
        # Create a dictionary of settings
        settings = {}
        for option in self.options:
            option_name = option["name"].lower().replace(" ", "_")
            option_value = option["options"][option["current"]].replace(" ", "_")
            settings[option_name] = option_value

        # Save to a JSON file

        # Ensure the directory exists
        save_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "db")
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, "settings.json")

        # Write the settings to the file
        with open(save_path, "w") as f:
            json.dump(settings, f, indent=4)
        pass
    
    def get_settings(self):
        """Return the current settings as a dictionary"""
        return {
            "player1": self.options[0]["options"][self.options[0]["current"]],
            "player2": self.options[1]["options"][self.options[1]["current"]],
        }