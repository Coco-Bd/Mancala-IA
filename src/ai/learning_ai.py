import random
from src.game.game_memory import GameMemory

class LearningAI:
    def __init__(self, player_name="AI"):
        """Initialize the learning AI player"""
        self.name = player_name
        self.memory = GameMemory()
        self.current_game = []  # Just store the moves
        
    def get_move(self, board, player):
        """Decide on a move based on the current game state"""
        # First, try to find a similar game from memory
        next_move = self.memory.find_similar_game(self.current_game)
        
        # Check if the suggested move is valid
        if next_move is not None:
            if player == "player1" and 0 <= next_move <= 5 and board[next_move] > 0:
                return next_move
            elif player == "player2" and 7 <= next_move <= 12 and board[next_move] > 0:
                return next_move
        
        # Fallback to basic strategy
        return self._choose_fallback_move(board, player)
    
    def update_last_move_result(self, board):
        """Not needed for this simple implementation"""
        pass
    
    def record_game_result(self, winner):
        """Record the completed game to the database"""
        if self.current_game:
            self.memory.store_game(self.current_game, winner)
            # Reset for the next game
            self.current_game = []
    
    def _choose_fallback_move(self, board, player):
        """Choose a move when no historical data is available"""
        if player == "player1":
            valid_moves = [i for i in range(6) if board[i] > 0]
        else:  # player2
            valid_moves = [i for i in range(7, 13) if board[i] > 0]
        
        if not valid_moves:
            return None
            
        # First, try to find a move that gives an extra turn
        for move in valid_moves:
            if player == "player1" and board[move] == 6 - move:  # Will end in player's store
                return move
            elif player == "player2" and board[move] == 13 - move:  # Will end in player's store
                return move
                
        # Otherwise, choose a random valid move
        return random.choice(valid_moves)