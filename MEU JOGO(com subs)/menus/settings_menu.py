import pygame
import sys
from utils import set_resolution
from ui.widgets import Slider, Button
from settings import (
    current_width, current_height, volume, RESOLUTIONS, current_res_index, MAGIC_GOLD, MAGIC_PURPLE, DARK_GRAY,
    GREEN, GRAY, WHITE, RED, BG_COLOR, keybinds, FPS
)
from utils import draw_section_separator
from assets import reload_images



def settings_menu(screen, clock, FONT, SMALL_FONT, TINY_FONT, TITLE_FONT):
    global volume
    tab = 0  # 0 = Vídeo e Som, 1 = Keybinds
    slider = Slider(current_width // 2 - 250, 420, 500, 35, SMALL_FONT, volume)

    while True:
        mouse_pos = pygame.mouse.get_pos()

        # Fundo com gradiente
        screen.fill(BG_COLOR)

        # Título principal
        title = TITLE_FONT.render(" Definições Mágicas", True, MAGIC_GOLD)
        screen.blit(title, (current_width // 2 - title.get_width() // 2, 50))

        # Separador decorativo
        draw_section_separator(screen, 100, 200)

        # === TABS MELHORADAS ===
        tab_w, tab_h = 220, 60
        tab_btns = [
            Button(current_width // 2 - 240, 130, tab_w, tab_h, " Vídeo e Som", FONT,
                   MAGIC_PURPLE if tab == 0 else DARK_GRAY, active=(tab == 0)),
            Button(current_width // 2 + 20, 130, tab_w, tab_h, " Keybinds", FONT,
                   MAGIC_PURPLE if tab == 1 else DARK_GRAY, active=(tab == 1))
        ]

        for btn in tab_btns:
            btn.update(mouse_pos)
            btn.draw(screen)

        # === CONTEÚDO MELHORADO ===
        if tab == 0:
            # --- SECÇÃO DE VÍDEO ---
            video_title = TITLE_FONT.render(" Configurações de Vídeo", True, MAGIC_GOLD)
            screen.blit(video_title, (current_width // 2 - video_title.get_width() // 2, 220))

            res_label = SMALL_FONT.render("Resolução da Janela:", True, WHITE)
            screen.blit(res_label, (current_width // 2 - 450, 270))

            # Botões de resolução
            res_btns = []
            btn_w, btn_h = 220,70
            start_x = current_width // 2 - (len(RESOLUTIONS) * btn_w + (len(RESOLUTIONS) - 1) * 15) // 2

            for i, res in enumerate(RESOLUTIONS):
                x = start_x + i * (btn_w + 15)
                y = 300
                label = f"{res[0]}×{res[1]}"
                is_current = (i == current_res_index)
                btn = Button(x, y, btn_w, btn_h, label, SMALL_FONT, GREEN if is_current else GRAY, active=is_current)
                btn.update(mouse_pos)
                btn.draw(screen)
                res_btns.append(btn)

            # Separador
            draw_section_separator(screen, 370, 150)

            # --- SECÇÃO DE SOM ---
            audio_title = TITLE_FONT.render(" Configurações de Som", True, MAGIC_GOLD)
            screen.blit(audio_title, (current_width // 2 - audio_title.get_width() // 2, 380))

            vol_label = SMALL_FONT.render("Volume Geral:", True, WHITE)
            screen.blit(vol_label, (current_width // 2 - 250, 430))

            # Slider melhorado
            slider.draw(screen)

        if tab == 1:
            # --- SECÇÃO DE KEYBINDS ---
            keybinds_title = TITLE_FONT.render(" Configurações de Teclas", True, MAGIC_GOLD)
            screen.blit(keybinds_title, (current_width // 2 - keybinds_title.get_width() // 2, 220))

            draw_keybinds_menu_improved(screen, mouse_pos, FONT, TINY_FONT, SMALL_FONT)


        # === BOTÃO VOLTAR MELHORADO ===
        back_btn = Button(30, current_height - 90, 180, 60, "← Voltar", SMALL_FONT, RED)
        back_btn.update(mouse_pos)
        back_btn.draw(screen)

        # === EVENTOS ===
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tab_btns[0].is_clicked(mouse_pos, event):
                    tab = 0
                elif tab_btns[1].is_clicked(mouse_pos, event):
                    tab = 1
                if back_btn.is_clicked(mouse_pos, event):
                    volume = slider.value
                    return
                if tab == 0:
                    for idx, btn in enumerate(res_btns):
                        if btn.is_clicked(mouse_pos, event):
                            set_resolution(idx, screen)
                            reload_images()

            if tab == 0:
                slider.handle_event(event)
            if tab == 1:
                handle_keybinds_event(event, mouse_pos)

        if tab == 0:
            volume = slider.value

        pygame.display.flip()
        clock.tick(FPS)


# --- Keybinds menu ---
keybinds_list = [
    ("move_up", " Andar para cima"),
    ("move_left", " Andar para a esquerda"),
    ("move_down", " Andar para baixo"),
    ("move_right", " Andar para a direita"),
    ("fireball", " Lançar Fireball"),
    ("hollowpurple", "Lançar Hollow Purple")
]
keybinds_waiting = None


def draw_keybinds_menu_improved(surface, mouse_pos, FONT, TINY_FONT, SMALL_FONT):
    """Menu de keybinds com visual melhorado"""
    global keybinds_waiting

    start_y = 270
    for idx, (action, label) in enumerate(keybinds_list):
        y = start_y + idx * 70

        # Label da ação com melhor formatação
        label_surf = SMALL_FONT.render(label, True, WHITE)
        surface.blit(label_surf, (current_width // 2 - 300, y + 10))

        # Botão da keybind melhorado
        key_name = pygame.key.name(keybinds[action][0]).upper()
        is_waiting = (keybinds_waiting == (action, 0))
        btn_color = MAGIC_GOLD if is_waiting else MAGIC_PURPLE
        btn = Button(current_width // 2 - 50, y, 200, 50, key_name, SMALL_FONT, btn_color, active=is_waiting)
        btn.update(mouse_pos)
        btn.draw(surface)

        # Indicador visual quando à espera
        if is_waiting:
            waiting_text = TINY_FONT.render("Prima uma tecla que nao esteja a ser usada...", True, MAGIC_GOLD)
            surface.blit(waiting_text, (current_width // 2 + 160, y + 15))
            # Efeito piscante
            if pygame.time.get_ticks() % 1000 < 500:
                pygame.draw.rect(surface, MAGIC_GOLD, (current_width // 2 - 55, y - 5, 210, 60), 3, border_radius=8)


def handle_keybinds_event(event, mouse_pos):
    """Gestão melhorada de eventos de keybinds"""
    global keybinds_waiting
    if keybinds_waiting is None:
        start_y = 270
        for idx, (action, label) in enumerate(keybinds_list):
            y = start_y + idx * 70
            btn_rect = pygame.Rect(current_width // 2 - 50, y, 200, 50)
            if event.type == pygame.MOUSEBUTTONDOWN and btn_rect.collidepoint(mouse_pos):
                keybinds_waiting = (action, 0)
    else:
        if event.type == pygame.KEYDOWN:
            action, idx = keybinds_waiting
            # Verifica duplicados
            for k, v in keybinds.items():
                if event.key in v and (k != action or idx != 0):
                    return
            keybinds[action][idx] = event.key
            keybinds_waiting = None
        elif event.type == pygame.MOUSEBUTTONDOWN:
            keybinds_waiting = None
