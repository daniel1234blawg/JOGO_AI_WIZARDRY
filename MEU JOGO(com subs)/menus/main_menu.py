import pygame
import sys
from ui.widgets import Button
from settings import *
from assets import *
from game.main_game import main_game
from menus.settings_menu import settings_menu

def main_menu(screen, FONT, SMALL_FONT, TINY_FONT, TITLE_FONT, clock):
    screen.blit(BG_IMAGE, (0, 0))
    while True:
        mouse_pos = pygame.mouse.get_pos()
        if BG_IMAGE:
            screen.blit(BG_IMAGE, (0, 0))
        else:
            screen.fill(BG_COLOR)
        b_w, b_h = int(current_width * 0.25), int(current_height * 0.10)
        buttons = [
            Button(current_width // 2 - b_w // 2, current_height // 2 - b_h * 2, b_w, b_h, "Jogar", FONT),
            Button(current_width // 2 - b_w // 2, current_height // 2, b_w, b_h, "Definições", FONT),
            Button(current_width // 2 - b_w // 2, current_height // 2 + b_h * 2, b_w, b_h, "Sair", FONT)
        ]
        for btn in buttons:
            btn.update(mouse_pos)
            btn.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].is_clicked(mouse_pos, event):
                    main_game(screen, FONT, SMALL_FONT, TINY_FONT, TITLE_FONT, clock)
                elif buttons[1].is_clicked(mouse_pos, event):
                    settings_menu(screen, clock, FONT, SMALL_FONT, TINY_FONT, TITLE_FONT)
                elif buttons[2].is_clicked(mouse_pos, event):
                    pygame.quit(); sys.exit()
        pygame.display.flip()
        clock.tick(FPS)