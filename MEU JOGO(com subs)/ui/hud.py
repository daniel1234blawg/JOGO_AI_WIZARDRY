import pygame
from settings import WHITE, GREEN, current_width, current_height, DARK_GRAY
import time
from classes.spells import *


def draw_health_bar(surface, x, y, w, h, hp, max_hp, font):
    pygame.draw.rect(surface, (60, 20, 20), (x, y, w, h), border_radius=3)
    fill_width = int(w * (hp / max_hp))
    pygame.draw.rect(surface, (237, 41, 57), (x, y, fill_width, h), border_radius=3)
    hp_label = font.render("HP", True, WHITE)
    surface.blit(hp_label, (x - hp_label.get_width() - 10, y + h // 2 - hp_label.get_height() // 2))
    value_text = font.render(f"{hp}/{max_hp}", True, WHITE)
    surface.blit(value_text, (x + w // 2 - value_text.get_width() // 2, y + h // 2 - value_text.get_height() // 2))

def draw_hud(surface, player, SMALL_FONT):
    bar_x = int(current_width * 0.35)
    bar_y = int(current_height * 0.9)
    bar_w = int(current_width * 0.30)
    bar_h = int(current_height * 0.05)
    draw_health_bar(surface, bar_x, bar_y, bar_w, bar_h, player.health, player.max_health, SMALL_FONT)

#firebal cooldown
def draw_fireball_cooldown(surface, fireball, keybinds, x, y, w, h, font, color):
    """Desenha barra de cooldown do fireball com visual melhorado"""
    pygame.draw.rect(surface, DARK_GRAY, (x, y, w, h), border_radius=8)
    pygame.draw.rect(surface, WHITE, (x, y, w, h), 2, border_radius=8)
    elapsed = time.time() - fireball.last_cast
    pct = min(elapsed / fireball.cooldown, 1.0)
    if pct < 1.0:
        progress_color = (255, 0, 0)
    else:
        progress_color = GREEN
    pygame.draw.rect(surface, progress_color, (x + 2, y + 2, (w - 4) * pct, h - 4), border_radius=6)
    keys_str = [pygame.key.name(k).upper() for k in keybinds["fireball"]]
    txt = f"Fireball [{'/'.join(keys_str)}]"
    txt_surf = font.render(txt, True, WHITE)
    surface.blit(txt_surf, (x + 10, y + h // 2 - txt_surf.get_height() // 2))
    if pct < 1.0:
        cooldown_txt = f"{fireball.cooldown - elapsed:.2f}s"
        cd_surf = font.render(cooldown_txt, True, (255, 180, 180))
    else:
        cd_surf = font.render("PRONTO", True, GREEN)
    surface.blit(cd_surf, (x + w - cd_surf.get_width() - 10, y + h // 2 - cd_surf.get_height() // 2))
#delete dps
def draw_hollowpurple_cooldown(surface, hollowpurple, keybinds, x, y, w, h, font, color):
    """Desenha barra de cooldown do fireball com visual melhorado"""
    pygame.draw.rect(surface, DARK_GRAY, (x, y, w, h), border_radius=8)
    pygame.draw.rect(surface, WHITE, (x, y, w, h), 2, border_radius=8)
    elapsed = time.time() - hollowpurple.last_cast
    pct = min(elapsed / hollowpurple.cooldown, 1.0)
    if pct < 1.0:
        progress_color = (255, 0, 0)
    else:
        progress_color = GREEN
    pygame.draw.rect(surface, progress_color, (x + 2, y + 2, (w - 4) * pct, h - 4), border_radius=6)
    keys_str = [pygame.key.name(k).upper() for k in keybinds["hollowpurple"]]
    txt = f"Hollow Purple [{'/'.join(keys_str)}]"
    txt_surf = font.render(txt, True, WHITE)
    surface.blit(txt_surf, (x + 10, y + h // 2 - txt_surf.get_height() // 2))
    if pct < 1.0:
        cooldown_txt = f"{hollowpurple.cooldown - elapsed:.2f}s"
        cd_surf = font.render(cooldown_txt, True, (255, 180, 180))
    else:
        cd_surf = font.render("PRONTO", True, GREEN)
    surface.blit(cd_surf, (x + w - cd_surf.get_width() - 10, y + h // 2 - cd_surf.get_height() // 2))

