import pygame
from settings import *
from assets import BUTTON_IMAGE
from utils import scale_image_aspect



class Button:
    def __init__(self, x, y, w, h, text, font, color=GRAY, active=False):
        self.font = font
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = (min(255, color[0] + 50), min(255, color[1] + 50), min(255, color[2] + 50))
        self.active_color = MAGIC_GOLD if active else color
        self.is_hovered = False
        self.active = active

    def set_active(self, active):
        self.active = active

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface):
        txt_surf = self.font.render(self.text, True, BLACK)
        if self.active:
            color = MAGIC_GOLD
            border_color = WHITE
            border_width = 3
        elif self.is_hovered:
            color = self.hover_color
            border_color = MAGIC_PURPLE
            border_width = 2
        else:
            color = self.color
            border_color = LIGHT_GRAY
            border_width = 1

        if BUTTON_IMAGE and not self.is_hovered and not self.active:
            scaled_img = scale_image_aspect(BUTTON_IMAGE, self.rect.size)
            img_rect = scaled_img.get_rect(center=self.rect.center)
            surface.blit(scaled_img, img_rect.topleft)
        else:
            pygame.draw.rect(surface, color, self.rect, border_radius=8)
            pygame.draw.rect(surface, border_color, self.rect, border_width, border_radius=8)

        if self.active:
            text_color = (0, 0, 0)
        else:
            text_color = WHITE
        txt_surf = self.font.render(self.text, True, text_color)
        surface.blit(txt_surf,
                     (self.rect.centerx - txt_surf.get_width() // 2, self.rect.centery - txt_surf.get_height() // 2))

    def is_clicked(self, mouse_pos, event):
        return self.rect.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1

class Slider:
    def __init__(self, x, y, w, h, font, value=75):
        self.font = font
        self.rect = pygame.Rect(x, y, w, h)
        self.value = value
        self.dragging = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            rel_x = event.pos[0] - self.rect.x
            rel_x = max(0, min(rel_x, self.rect.width))
            self.value = int((rel_x / self.rect.width) * 100)

    def draw(self, surface):
        pygame.draw.rect(surface, DARK_GRAY, self.rect, border_radius=12)
        pygame.draw.rect(surface, MAGIC_PURPLE, self.rect, 2, border_radius=12)
        fill_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2,
                                int((self.rect.width - 4) * (self.value / 100)), self.rect.height - 4)
        pygame.draw.rect(surface, BLUE, fill_rect, border_radius=10)
        knob_x = self.rect.x + int(self.rect.width * (self.value / 100))
        pygame.draw.circle(surface, MAGIC_GOLD, (knob_x, self.rect.centery), self.rect.height // 2 + 4)
        pygame.draw.circle(surface, WHITE, (knob_x, self.rect.centery), self.rect.height // 2 + 1, 2)
        txt = self.font.render(f"{self.value}%", True, MAGIC_GOLD)
        surface.blit(txt, (self.rect.right + 20, self.rect.centery - txt.get_height() // 2))
