import time
import pygame
import sys
from classes.player import Player
from classes.map import Map
from classes.spells import *
from settings import current_width, current_height, BG_COLOR, FPS, keybinds, DARK_GRAY, WHITE, MAGIC_GOLD
from ui.hud import draw_hud
from ui.hud import draw_fireball_cooldown
from ui.hud import draw_hollowpurple_cooldown
from menus.pause_menu import draw_pause_menu
from ui.widgets import Slider, Button

SMALL_FONT = pygame.font.SysFont("arial", 24)
volume_slider = Slider(0, 0, 40, 200, SMALL_FONT, vertical=True)


background_img = pygame.image.load("ceu.png").convert()
background_img = pygame.transform.smoothscale(background_img, (current_width, current_height))

def main_game(screen, FONT, SMALL_FONT, TINY_FONT, TITLE_FONT, clock):
    game_map = Map("tiled/wizardry.tmx")
    player = Player(current_width // 2 - 32, current_height // 2 - 32)
    projectiles = []
    #«pause stuff
    paused = False
    pause_start_time = 0
    #pause stuff »
    pending_hollowpurple = None


    slowmo_active = False
    slowmo_start_time = 0
    slowmo_duration = 1.5 # 2 segundos
    slowmo_factor = 0.2  # 30% da velocidade normal

    while True:
        dt = clock.tick(FPS) / 1000

        game_map.update_camera(player, current_width, current_height)



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
                            spell.last_cast = time.time()
                        else:
                            spell.cast(player, projectiles, mouse_pos)
                if event.key == pygame.K_ESCAPE:
                    if not paused:
                        paused = True
                        pause_start_time = time.time()
                    else:
                        paused_duration = time.time() - pause_start_time
                        for spell in player.spells:
                            spell.last_cast += paused_duration

        # --- Atualizações (só ocorrem se não estiver pausado) ---
        if not paused:
            keys = pygame.key.get_pressed()
            player.update(keys, dt, game_map)

            projectiles = [proj for proj in projectiles if proj.update(dt)]
            cooldown_now = time.time()
        else:
            cooldown_now = pause_start_time  # "congela" o tempo das cooldowns
        if paused:
            result = draw_pause_menu(screen, FONT, current_width, current_height, volume_slider)
            if result == "quit":
                pygame.quit()
                sys.exit()
            elif result == "resume":
                paused = False
                continue

        screen_x = player.x - game_map.camera_offset[0]
        screen_y = player.y - game_map.camera_offset[1]
        screen.blit(background_img, (screen_x, screen_y))
        game_map.draw(screen)
        for proj in projectiles:
            proj.draw(screen)

        player.draw(screen)
        draw_fireball_cooldown(
            screen, player.spells[0], keybinds, 40, 40, 300, 36, SMALL_FONT, MAGIC_GOLD, cooldown_now
        )
        draw_hollowpurple_cooldown(
            screen, player.spells[1], keybinds, 40, 90, 450, 50, SMALL_FONT, MAGIC_GOLD, cooldown_now
        )
        draw_hud(screen, player, SMALL_FONT)

        if paused:
            draw_pause_menu(screen, FONT, current_width, current_height, volume_slider)

        pygame.display.flip()
        clock.tick(FPS)