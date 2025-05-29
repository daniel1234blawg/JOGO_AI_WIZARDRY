import pygame
from ui.widgets import Button
from settings import *
import sys

def draw_pause_menu(screen, font, width, height, volume_slider):
    # Semi-transparent overlay
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    # Create buttons
    btn_w, btn_h = 200, 60
    resume_btn = Button(
        width // 2 - btn_w // 2, height // 2 - 100,
        btn_w, btn_h, "Resume", font, MAGIC_PURPLE
    )
    quit_btn = Button(
        width // 2 - btn_w // 2, height // 2,
        btn_w, btn_h, "Quit", font, RED
    )

    # Vertical volume slider in bottom right
    slider_size = 200
    volume_slider.rect = pygame.Rect(
        width - 70, height - slider_size - 20,
        40, slider_size
    )

    while True:
        mouse_pos = pygame.mouse.get_pos()

        # Update UI elements
        resume_btn.update(mouse_pos)
        quit_btn.update(mouse_pos)

        #volume_slider.update()

        # Draw elements
        resume_btn.draw(screen)
        quit_btn.draw(screen)
        volume_slider.draw(screen)

        # Title
        title = font.render("PAUSED", True, MAGIC_GOLD)
        screen.blit(title, (width // 2 - title.get_width() // 2, height // 2 - 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_btn.is_clicked(mouse_pos, event):
                    return "resume"
                elif quit_btn.is_clicked(mouse_pos, event):
                    pygame.quit()
                    sys.exit()
                    return "quit"
            volume_slider.handle_event(event)

        pygame.display.flip()