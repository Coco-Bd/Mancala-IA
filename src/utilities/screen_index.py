"""
screen_index.py - Contains screen-related constants for the Tic Tac Toe game
"""
class ScreenSettings:
    # Window dimensions
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 600
    WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
    
    # Colors (R, G, B)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    GRAY = (200, 200, 200)
    LIGHT_GRAY = (230, 230, 230)
    DARK_GRAY = (100, 100, 100)
    
    # Game board
    BOARD_SIZE = 3
    CELL_SIZE = WINDOW_WIDTH // BOARD_SIZE
    LINE_WIDTH = 4
    
    # Game states
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2
    
    # Text settings
    TITLE_FONT_SIZE = 50
    NORMAL_FONT_SIZE = 30
    SMALL_FONT_SIZE = 20