
import os
import json

class PlayerSelector:
    def __init__(self,mancala):
        self.mancala = mancala
        pass

    def check_player_type(self):
        try:
            settings_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "db", "settings.json")
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
                    self.player1_status = settings.get("player_1", "Human")
                    self.player2_status = settings.get("player_2", "Human")
        except Exception as e:
            print(f"Error loading settings: {e}")
            # Use default values if there's an error