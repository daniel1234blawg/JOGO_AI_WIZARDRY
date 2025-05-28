import pygame
import sys
from classes.player import Player
from settings import current_width, current_height, BG_COLOR, FPS, keybinds, DARK_GRAY, WHITE, MAGIC_GOLD
from ui.hud import draw_hud
from ui.hud import draw_fireball_cooldown
from ui.hud import draw_hollowpurple_cooldown
from classes.spells import *

   # 20% normal speed


def main_game(screen, FONT, SMALL_FONT, TINY_FONT, TITLE_FONT, clock):
    player = Player(current_width // 2 - 32, current_height // 2 - 32)
    projectiles = []

    pending_hollowpurple = None


    slowmo_active = False
    slowmo_start_time = 0
    slowmo_duration = 1.5 # 2 segundos
    slowmo_factor = 0.2  # 30% da velocidade normal

    while True:
        dt = clock.tick(FPS) / 1000
        if slowmo_active:
            dt *= slowmo_factor
            if time.time() - slowmo_start_time >= slowmo_duration:
                slowmo_active = False
                if pending_hollowpurple:
                    spell, caster, projectiles, mouse_pos = pending_hollowpurple
                    spell._finish_cast(caster, projectiles, mouse_pos)
                    pending_hollowpurple = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for spell in player.spells:
                    if event.key in keybinds[spell.keybind_name] and spell.can_cast():
                        if isinstance(spell, HollowPurple) and spell.can_cast():
                            hollowpurple_sound.play()
                            mouse_pos = pygame.mouse.get_pos()
                            slowmo_active = True
                            slowmo_start_time = time.time()
                            pending_hollowpurple = (spell, player, projectiles, mouse_pos)
                            spell.last_cast = time.time()  # Inicia o cooldown
                        else:
                            spell.cast(player, projectiles, mouse_pos)
                if event.key == pygame.K_ESCAPE:
                    return

        keys = pygame.key.get_pressed()
        player.update(keys, dt)
        projectiles = [proj for proj in projectiles if proj.update()]
        screen.fill(BG_COLOR)
        player.draw(screen)
        for proj in projectiles:
            proj.draw(screen)

        draw_fireball_cooldown(
            screen,
            player.spells[0],
            keybinds,
            40, 40, 300, 36,
            SMALL_FONT,
            MAGIC_GOLD
        )
        draw_hollowpurple_cooldown(
            screen,
            player.spells[1],
            keybinds,
            40, 90, 450, 50,
            SMALL_FONT,
            MAGIC_GOLD
        )
        draw_hud(screen, player, SMALL_FONT)

        pygame.display.flip()
        clock.tick(FPS)