# main.py
from src.ui.screen_menu import MenuScreen
from db.init_db import initialize_files
import pygame
import sys

def main():
    pygame.init()
    initialize_files()
    menu = MenuScreen()
    result = menu.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()