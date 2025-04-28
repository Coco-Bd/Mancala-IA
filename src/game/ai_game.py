from src.ai.learning_ai import LearningAI

class AIGame:
    def __init__(self,mancala):
        self.board = mancala
        self.ai = LearningAI("AI_Player")
        
    def player_move(self, pit_index):
        """Handle a move by the human player"""
        if self.board.current_player == "player1":
            result = self.board.make_move_helper(pit_index)
            
            if result:
                # Record this move in the AI's memory
                self.ai.current_game.append(pit_index)
            
            # Check game over after player's move
            if self.board.finish_game:
                winner = self.determine_winner()
                self.ai.record_game_result(winner)
                
            return result
        return False
    
    def ai_move(self):
        """Handle a move by the AI player"""
        # AI decides on a move
        move = self.ai.get_move(self.board.board, self.board.current_player)
        
        if move is not None:
            # Make the move
            self.board.make_move_helper(move)
            
            # Record this move in the AI's memory
            self.ai.current_game.append(move)
        else:
            # No valid moves available for AI, game should end
            print("AI has no valid moves. Game over.")
            self.board.finish_game = True
        
        # Check if the game is over
        if self.board.finish_game:
            winner = self.determine_winner()
            self.ai.record_game_result(winner)
    
    def determine_winner(self):
        """Determine the winner of the game"""
        score_p1 = self.board.get_score("player1")
        score_p2 = self.board.get_score("player2")
        
        if score_p1 > score_p2:
            return "player1"
        elif score_p2 > score_p1:
            return "player2"
        else:
            return "draw"