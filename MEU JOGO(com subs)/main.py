import pygame

pygame.init()
from settings import current_width, current_height, get_fonts

screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
pygame.display.set_caption("Wizardry")

FONT, SMALL_FONT, TINY_FONT, TITLE_FONT = get_fonts()
clock = pygame.time.Clock()

from assets import reload_images
reload_images()

from menus.main_menu import main_menu

if __name__ == "__main__":
    main_menu(screen, FONT, SMALL_FONT, TINY_FONT, TITLE_FONT, clock)

