import pygame
import time
import math
from settings import RED, GREEN, current_width, current_height, PURPLE
from assets import fireball_sound, hollowpurple_sound
from assets import FIREBALL_FRAMES

class Spell:
    def __init__(self, name, keybind_name, color, cooldown=1.0):
        self.name = name
        self.keybind_name = keybind_name  # Ex: "fireball" ou "hollow_purple"
        self.color = color
        self.cooldown = cooldown
        self.last_cast = -float('inf')

    def can_cast(self):
        return time.time() - self.last_cast >= self.cooldown

class Fireball(Spell):
    def __init__(self):
        super().__init__("Fireball", "fireball", RED, cooldown=2.0)
        self.damage = 50
        self.speed = 17.5



    def cast(self, caster, projectiles, mouse_pos):
        if self.can_cast():
            x, y = caster.rect.midtop
            mx, my = mouse_pos
            dx = mx - x
            dy = my - y
            length = math.hypot(dx, dy)
            if length == 0:
                dx, dy = 0, -1
            else:
                dx /= length
                dy /= length
            projectiles.append(ProjectileFireball(x, y, dx, dy, self.color, self.speed, self.damage))
            fireball_sound.play()
            self.last_cast = time.time()
            return True
        return False

class ProjectileFireball:
    def __init__(self, x, y, dx, dy, color, speed, damage):
        self.x = float(x)
        self.y = float(y)
        self.dx = dx * speed
        self.dy = dy * speed
        self.color = color
        self.radius = 30
        self.damage = damage
        self.lifetime = 300
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        self.angle = math.degrees(math.atan2(dy, dx))
        # Animation state
        self.frames = FIREBALL_FRAMES
        self.frame_index = 0
        self.frame_timer = 1
        self.frame_speed = 5 # frames to wait before advancing (ajustavel for speed)

    def update(self, dt):
        self.x += self.dx
        self.y += self.dy
        self.rect.x = int(self.x - self.radius)
        self.rect.y = int(self.y - self.radius)
        self.lifetime -= 1

        # Animation update
        self.frame_timer += 1
        if self.frame_timer >= self.frame_speed:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)

        return self.lifetime > 0 and 0 <= self.x <= current_width and 0 <= self.y <= current_height
    #draw especifico do fireball
    def draw(self, surface):
        frame = self.frames[self.frame_index]
        scaled_frame = pygame.transform.scale(frame, (self.rect.width, self.rect.height))
        rotated_frame = pygame.transform.rotate(scaled_frame, -self.angle)
        rotated_rect = rotated_frame.get_rect(center=self.rect.center)
        surface.blit(rotated_frame, rotated_rect.topleft)



class HollowPurple(Spell):
    def __init__(self):
        super().__init__("Hollow Purple", "hollowpurple", RED, cooldown=15.0)
        self.damage = 300
        self.speed = 15

    def cast(self, caster, projectiles, mouse_pos):
        self.last_cast = time.time()
        return True

    def _finish_cast(self, caster, projectiles, mouse_pos):
        x, y = caster.rect.midtop
        mx, my = mouse_pos
        dx = mx - x
        dy = my - y
        length = math.hypot(dx, dy)
        if length == 0:
            dx, dy = 0, -1
        else:
            dx /= length
            dy /= length
        projectiles.append(ProjectileHollowPurple(x, y, dx, dy, self.color, self.speed, self.damage))




class ProjectileHollowPurple:
    def __init__(self, x, y, dx, dy, color, speed, damage):
        self.x = float(x)
        self.y = float(y)
        self.dx = dx * speed
        self.dy = dy * speed
        self.color = color
        self.radius = 30
        self.damage = damage
        self.lifetime = 300
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        self.angle = math.degrees(math.atan2(dy, dx))

        self.frames = FIREBALL_FRAMES
        self.frame_index = 0
        self.frame_timer = 1
        self.frame_speed = 5 # frames to wait before advancing (ajustavel for speed)

    def update(self, dt):
        self.x += self.dx
        self.y += self.dy
        self.rect.x = int(self.x - self.radius)
        self.rect.y = int(self.y - self.radius)
        self.lifetime -= 1

        # Animation update
        self.frame_timer += 1
        if self.frame_timer >= self.frame_speed:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)

        return self.lifetime > 0 and 0 <= self.x <= current_width and 0 <= self.y <= current_height
    #draw do hollow purple


    def draw(self, surface):
        pygame.draw.circle(surface, PURPLE, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), self.radius, 3)





