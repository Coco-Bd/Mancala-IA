import pygame
import sys
import os
import time

# Ajouter le chemin du projet au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.mancala import MancalaBoard

class MancalaUI:
    """Interface graphique pour le jeu Mancala."""
    
    def __init__(self, width=800, height=500):
        """Initialise l'interface graphique."""
        pygame.init()
        pygame.display.set_caption("Mancala")
        
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        
        # Chargement des polices
        self.title_font = pygame.font.SysFont("Arial", 36, bold=True)
        self.font = pygame.font.SysFont("Arial", 24)
        self.small_font = pygame.font.SysFont("Arial", 18)
        
        # Couleurs
        self.Beige = (240, 230, 200)  # Beige clair
        self.Gris = (50, 50, 50)   # Gris foncé
        self.Marron = (180, 140, 100)  # Marron clair
        self.Dark_Gris = (80, 80, 80)   # Gris foncé
        self.Or = (255, 215, 0)  # Or
        self.Vert = (120, 180, 120)  # Vert clair
        self.Dark_Vert = (100, 160, 100)  # Vert un peu plus foncé
        
        # État du jeu
        self.in_menu = True
        self.hover_button = None
        
        # Dimensions des éléments
        self.pit_radius = 40
        self.stone_radius = 8
        self.kalaha_width = 50
        self.kalaha_height = 120
        
    """def reset_game(self):
        self.board = MancalaBoard()
        self.selected_pit = None
        self.player_turn = 0  # 0 pour joueur 1, 1 pour joueur 2
        self.game_over = False
        self.winner = None
        
        # Positions des puits
        self.pits_positions = []
        
        # Puits du joueur 1 (bas)
        for i in range(6):
            x = 150 + i * 85
            y = self.height - 100
            self.pits_positions.append({"pos": (x, y), "player": 0, "index": i})
        
        # Puits du joueur 2 (haut)
        for i in range(6):
            x = 150 + (5-i) * 85
            y = 100
            self.pits_positions.append({"pos": (x, y), "player": 1, "index": i})
        
        # Positions des kalahas
        self.kalaha_positions = [
            {"pos": (650, self.height - 100), "player": 0},  # Joueur 1
            {"pos": (150, 100), "player": 1}                # Joueur 2
        ]
"""
    def create_button(self, text, rect, action=None):
        """Crée un bouton interactif."""
        mouse_pos = pygame.mouse.get_pos()
        button_color = self.Gris if rect.collidepoint(mouse_pos) else self.Marron
        
        # Dessiner le bouton
        pygame.draw.rect(self.screen, button_color, rect, border_radius=10)
        
        # Ajouter le texte
        button_text = self.font.render(text, True, self.Or)
        text_x = rect.x + (rect.width - button_text.get_width()) // 2
        text_y = rect.y + (rect.height - button_text.get_height()) // 2
        self.screen.blit(button_text, (text_x, text_y))
        
        # Vérifier le clic
        for event in pygame.event.get(pygame.MOUSEBUTTONDOWN):
            if event.button == 1 and rect.collidepoint(event.pos) and action:
                action()
        
        return rect.collidepoint(mouse_pos)

    def draw_puit(self, pos, stones_count, is_selected=False, is_clickable=False):
        """Dessine un puit avec le nombre de pierres spécifié."""
        x, y = pos
        # Dessiner le puit
        color = self.highlight_color if is_selected else self.Marron
        pygame.draw.circle(self.screen, color, (x, y), self.pit_radius)
        
        # Afficher le nombre de pierres
        text = self.small_font.render(str(stones_count), True, self.Or)
        self.screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))
        
        # Dessiner les pierres autour du puit
        if stones_count > 0:
            self.draw_stones(pos, stones_count)
        
        # Vérifier si le puit est cliquable et survolé
        if is_clickable:
            mouse_pos = pygame.mouse.get_pos()
            if (x - mouse_pos[0])**2 + (y - mouse_pos[1])**2 <= self.pit_radius**2:
                # Dessiner un contour pour indiquer que le puit est survolé
                pygame.draw.circle(self.screen, self.Marron, (x, y), self.pit_radius + 3, 3)
                return True
        return False

    def draw_stones(self, pos, count):
        """Dessine les pierres dans un puit."""
        x, y = pos
        # Limite le nombre de pierres affichées pour éviter l'encombrement
        visible_stones = min(count, 12)
        
        angle_step = 360 / visible_stones
        for i in range(visible_stones):
            angle = i * angle_step
            # Calcul de la position en coordonnées polaires
            stone_x = x + int((self.pit_radius * 0.6) * pygame.math.Vector2(1, 0).rotate(angle).x)
            stone_y = y + int((self.pit_radius * 0.6) * pygame.math.Vector2(1, 0).rotate(angle).y)
            pygame.draw.circle(self.screen, self.stone_color, (stone_x, stone_y), self.stone_radius)





    def Menu(self):
        """
        Affiche et gère le menu principal du jeu Mancala.
        Cette méthode:
        - Affiche le titre du jeu
        - Crée et rend les boutons interactifs du menu principal
        - Gère les événements utilisateur (survol et clics)
        - Traite les actions selon les boutons sélectionnés
        Interactions:
        - Le bouton "Jouer" lance une nouvelle partie
        - Le bouton "Option" permettra d'accéder aux paramètres du jeu
        - Le bouton "Quitter" ferme l'application
        La boucle s'exécute à 60 FPS et reste active tant que l'utilisateur
        est dans le menu principal (self.in_menu = True) et que le jeu est 
        en cours d'exécution (running = True).
        """
        """Affiche le menu principal."""
        running = True
        clock = pygame.time.Clock()

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

            pygame.display.flip()
            clock.tick(60)
    
        def exit_menu_to_game(self):
            """Quitte le menu et démarre le jeu."""
            self.in_menu = False
            self.reset_game()
            # Appeler la fonction de jeu
            self.game()
    
        def quit_game(self):
            """Quitte le jeu."""
            pygame.quit()
            sys.exit()
    
        def show_options(self):
            """Affiche le menu des options."""
            # Implémenter le menu des options
            def show_options(self):
                """Affiche le menu des options."""
                # Options de jeu
                options_running = True
                selected_option = 0  # 0: Joueur vs Joueur, 1: Joueur vs IA, 2: IA vs IA
                option_titles = ["Joueur vs Joueur", "Joueur vs IA", "IA vs IA"]
                
                while options_running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            mouse_pos = pygame.mouse.get_pos()
                            
                            # Vérifier les clics sur les options
                            for i in range(3):
                                option_rect = pygame.Rect(self.width//2 - 120, 180 + i*60, 240, 40)
                                if option_rect.collidepoint(mouse_pos):
                                    selected_option = i
                            
                            # Vérifier le clic sur le bouton retour
                            back_button = pygame.Rect(self.width//2 - 100, self.height - 100, 200, 50)
                            if back_button.collidepoint(mouse_pos):
                                options_running = False
                    
                    # Dessiner l'écran d'options
                    self.screen.fill(self.Beige)
                    
                    # Titre
                    title = self.title_font.render("OPTIONS", True, self.Gris)
                    self.screen.blit(title, (self.width//2 - title.get_width()//2, 50))
                    
                    # Sous-titre
                    subtitle = self.font.render("Mode de jeu:", True, self.Gris)
                    self.screen.blit(subtitle, (self.width//2 - subtitle.get_width()//2, 120))
                    
                    # Options de jeu
                    for i in range(3):
                        option_rect = pygame.Rect(self.width//2 - 120, 180 + i*60, 240, 40)
                        is_selected = (i == selected_option)
                        
                        # Dessiner la case d'option
                        check_box = pygame.Rect(self.width//2 - 100, 190 + i*60, 20, 20)
                        pygame.draw.rect(self.screen, self.Gris, check_box, 2)
                        
                        if is_selected:
                            # Dessiner une coche dans la case
                            pygame.draw.rect(self.screen, self.Gris, pygame.Rect(check_box.x+4, check_box.y+4, 12, 12))
                        
                        # Afficher le texte de l'option
                        option_text = self.small_font.render(option_titles[i], True, self.Gris)
                        self.screen.blit(option_text, (self.width//2 - 70, 190 + i*60))
                    
                    # Bouton retour
                    back_button = pygame.Rect(self.width//2 - 100, self.height - 100, 200, 50)
                    self.create_button("Retour", back_button)
                    
                    pygame.display.flip()
                
                # Sauvegarder l'option sélectionnée
                self.game_mode = selected_option

        def game(self):
            """Fonction principale qui gère le déroulement du jeu."""
            # Code pour le jeu ici
            running = True
            clock = pygame.time.Clock()
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        # Gérer le clic de la souris
                        self.handle_click(event.pos)
                
                # Dessiner le jeu
                self.draw_game()
                pygame.display.flip()
                clock.tick(60)
            pygame.quit()
            sys.exit()
            self.menu()