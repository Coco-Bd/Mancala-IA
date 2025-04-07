import pygame

class Button:
    def __init__(self, x, y, width, height, text='', color=(50, 50, 50), hover_color=(180, 140, 100), text_color=(255, 215, 0), font_size=24,action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font_size = font_size
        self.hovered = False
        self.action = action        
    def update(self, mouse_pos):
        # Vérifie si la souris est sur le bouton
        self.hovered = self.rect.collidepoint(mouse_pos)
    
    def draw(self, surface):
        # Dessine le bouton avec la couleur appropriée
        
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        
        # Dessine le texte du bouton
        font = pygame.font.SysFont(None, 36)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def collidepoint(self, pos):
        # Délègue à rect.collidepoint
        return self.rect.collidepoint(pos)
    