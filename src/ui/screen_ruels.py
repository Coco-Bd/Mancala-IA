def draw_rules(self):
        """Affiche les règles du jeu dans une fenêtre popup au centre de l'écran."""
        # Vérifier si les règles doivent être affichées
        if not hasattr(self, 'show_rules_popup') or not self.show_rules_popup:
            return
            
        # Créer la popup
        popup_width = 600
        popup_height = 300
        popup_x = (self.screen_width - popup_width) // 2
        popup_y = (self.screen_height - popup_height) // 2
        
        # Dessiner le fond semi-transparent
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Fond noir semi-transparent
        self.screen.blit(overlay, (0, 0))
        
        # Dessiner la popup
        popup = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
        pygame.draw.rect(self.screen, self.Beige, popup, border_radius=15)
        pygame.draw.rect(self.screen, self.Dark_Gris, popup, width=3, border_radius=15)
        
        # Titre de la popup
        title_text = self.font.render("Règles du Mancala", True, self.Dark_Gris)
        self.screen.blit(title_text, (popup_x + popup_width//2 - title_text.get_width()//2, popup_y + 20))
        
        # Contenu des règles
        rules = [
            "• Jouez en sélectionnant un de vos trous",
            "• Les graines sont distribuées dans le sens anti-horaire",
            "• Si votre dernier grain tombe dans votre kalaha, rejouez",
            "• Si votre dernier grain tombe dans un trou vide, capturez les graines opposées"
        ]
        
        y_pos = popup_y + 70
        for rule in rules:
            rule_text = self.small_font.render(rule, True, self.Dark_Gris)
            self.screen.blit(rule_text, (popup_x + 30, y_pos))
            y_pos += 30
        
        # Bouton de fermeture
        close_button_rect = pygame.Rect(popup_x + popup_width//2 - 60, popup_y + popup_height - 50, 120, 30)
        pygame.draw.rect(self.screen, self.Dark_Gris, close_button_rect, border_radius=5)
        close_text = self.small_font.render("Fermer", True, self.Beige)
        self.screen.blit(close_text, (close_button_rect.centerx - close_text.get_width()//2, 
                                      close_button_rect.centery - close_text.get_height()//2))
        
        # Stocker la position du bouton pour la vérification des clics
        self.close_button_rect = close_button_rect
        