import pygame
import math
from settings import BLUE, keybinds, current_width, current_height
from assets import PLAYER_SPRITES
from utils import scale_image_aspect
from classes.spells import Fireball, HollowPurple


class Player:
    def __init__(self, x, y):
        self.scale = 1.8 #multiplier for player sprite size.
        self.rect = pygame.Rect(x, y, 40 * self.scale, 60 * self.scale)
        self.x = float(x)
        self.y = float(y)
        self.color = BLUE
        self.speed = 500
        self.facing = "up"
        self.spells = [Fireball(), HollowPurple()]
        self.health = 100
        self.max_health = 100

    def update(self, keys, dt, game_map):
        dx, dy = 0, 0
        if any(keys[k] for k in keybinds["move_up"]): dy -= 1
        if any(keys[k] for k in keybinds["move_down"]): dy += 1
        if any(keys[k] for k in keybinds["move_left"]): dx -= 1
        if any(keys[k] for k in keybinds["move_right"]): dx += 1

        if dx != 0 or dy != 0:
            length = math.hypot(dx, dy)
            dx /= length
            dy /= length
            if dx > 0:
                self.facing = "right"
            elif dx < 0:
                self.facing = "left"
            elif dy > 0:
                self.facing = "down"
            elif dy < 0:
                self.facing = "up"

        new_x = self.x + dx * self.speed * dt
        new_y = self.y + dy * self.speed * dt
        if not game_map.is_blocked(new_x, new_y):
            self.x = new_x
            self.y = new_y
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)



    def draw(self, surface):
        sprite = PLAYER_SPRITES[self.facing]
        sprite_scaled = scale_image_aspect(sprite, (self.rect.width, self.rect.height))
        surface.blit(sprite_scaled, self.rect.topleft)
