import pygame


def draw_pause_menu(screen, font, width, height):
    # Semi-transparent overlay
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # RGBA: last value is transparency
    screen.blit(overlay, (0, 0))

    # Pause text
    text = font.render("PAUSED", True, (255, 255, 255))
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))

    # Instructions
    instr = font.render("Press ESC to resume", True, (200, 200, 200))
    screen.blit(instr, (width // 2 - instr.get_width() // 2, height // 2 + 40))