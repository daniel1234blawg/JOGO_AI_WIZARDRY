import pygame
import sys
import os
import ctypes

pygame.init()

# Configurações
VIRTUAL_WIDTH, VIRTUAL_HEIGHT = 800, 600
RESOLUTIONS = [
    (800, 600),
    (1280, 720),
    (1600, 900),
    (1920, 1080),
    "Borderless Fullscreen"
]
RES_INDEX_BORDERLESS = len(RESOLUTIONS) - 1

WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
RED = (255, 50, 50)
BG_COLOR = (30, 30, 30)
MENU_BG = (25, 25, 40)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 160, 210)

current_res_index = 0
fullscreen = False
current_width, current_height = 800, 600
volume = 0.5
dragging_volume = False
clock = pygame.time.Clock()

screen = None
virtual_screen = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

PLAYER_SIZE = 32
if os.path.exists("personagem.png"):
    personagem_img = pygame.image.load("personagem.png")
    personagem_img = pygame.transform.scale(personagem_img, (PLAYER_SIZE, PLAYER_SIZE))
else:
    personagem_img = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
    personagem_img.fill((50, 50, 255))

SPELL_SIZE = 8
SPELL_SPEED = 8
COOLDOWN_FIREBALL = 2500
last_spell_time = -COOLDOWN_FIREBALL
spells = []

player_pos = [VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT // 2]

keybinds = {
    "fireball": [pygame.K_f, pygame.K_SPACE],
    "up": [pygame.K_w, pygame.K_UP],
    "down": [pygame.K_s, pygame.K_DOWN],
    "left": [pygame.K_a, pygame.K_LEFT],
    "right": [pygame.K_d, pygame.K_RIGHT]
}
keybind_names = {
    "fireball": "Lançar Feitiço",
    "up": "Mover Cima",
    "down": "Mover Baixo",
    "left": "Mover Esquerda",
    "right": "Mover Direita"
}
waiting_for_key = None

STATE_MENU, STATE_GAME, STATE_SETTINGS, STATE_VIDEO, STATE_KEYBINDS = 0, 1, 2, 3, 4
game_state = STATE_MENU

def get_native_resolution():
    try:
        user32 = ctypes.windll.user32
        return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    except:
        info = pygame.display.Info()
        return (info.current_w, info.current_h)

def set_resolution(index):
    global screen, current_width, current_height, fullscreen, current_res_index
    current_res_index = index
    if RESOLUTIONS[index] == "Borderless Fullscreen":
        current_width, current_height = get_native_resolution()
        screen = pygame.display.set_mode((current_width, current_height), pygame.NOFRAME)
        fullscreen = True
    else:
        current_width, current_height = RESOLUTIONS[index]
        screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
        fullscreen = False

def scale_mouse(pos):
    sx = current_width / VIRTUAL_WIDTH
    sy = current_height / VIRTUAL_HEIGHT
    return (pos[0] / sx, pos[1] / sy)

def key_name(key):
    return pygame.key.name(key).upper()

def draw_button(rect, text, mouse_pos):
    color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(virtual_screen, color, rect)
    text_surf = pygame.font.SysFont(None, 32).render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    virtual_screen.blit(text_surf, text_rect)

def draw_volume_slider():
    slider_x = (VIRTUAL_WIDTH - 200) // 2
    slider_y = VIRTUAL_HEIGHT - 120
    pygame.draw.rect(virtual_screen, (100, 100, 100), (slider_x, slider_y, 200, 20))
    handle_x = slider_x + int(volume * 200)
    pygame.draw.circle(virtual_screen, (200, 200, 200), (handle_x, slider_y + 10), 8)
    text = pygame.font.SysFont(None, 24).render(f"Volume: {int(volume * 100)}%", True, WHITE)
    virtual_screen.blit(text, (slider_x + 220, slider_y - 2))

def draw_fireball_ui():
    square_x = (VIRTUAL_WIDTH - 100) // 2
    square_y = VIRTUAL_HEIGHT - 100 - 10
    pygame.draw.rect(virtual_screen, (70, 70, 70), (square_x, square_y, 100, 100))
    text_surface = pygame.font.SysFont(None, 24).render("fireball", True, WHITE)
    text_rect = text_surface.get_rect(center=(square_x + 50, square_y + 40))
    virtual_screen.blit(text_surface, text_rect)
    cooldown_remaining = max(0, (COOLDOWN_FIREBALL - (pygame.time.get_ticks() - last_spell_time)) / 1000)
    cooldown_text = f"{cooldown_remaining:.1f}s" if cooldown_remaining > 0 else "Ready"
    cooldown_surface = pygame.font.SysFont(None, 24).render(cooldown_text, True, (255, 100, 100))
    cooldown_rect = cooldown_surface.get_rect(topright=(square_x + 95, square_y + 5))
    virtual_screen.blit(cooldown_surface, cooldown_rect)
    keybind_text = f"Keys: {key_name(keybinds['fireball'][0])}, {key_name(keybinds['fireball'][1])}"
    keybind_surface = pygame.font.SysFont(None, 24).render(keybind_text, True, WHITE)
    keybind_rect = keybind_surface.get_rect(center=(square_x + 50, square_y + 100 - 16))
    virtual_screen.blit(keybind_surface, keybind_rect)

def main_menu():
    global game_state, volume, dragging_volume, current_res_index
    play_button = pygame.Rect(300, 200, 200, 50)
    settings_button = pygame.Rect(300, 260, 200, 50)
    quit_button = pygame.Rect(300, 320, 200, 50)
    fullscreen_button = pygame.Rect(VIRTUAL_WIDTH - 130, 10, 120, 40)
    while game_state == STATE_MENU:
        virtual_screen.fill(MENU_BG)
        mouse_pos = scale_mouse(pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                new_index = RES_INDEX_BORDERLESS if not fullscreen else 0
                set_resolution(new_index)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_button.collidepoint(mouse_pos):
                        game_state = STATE_GAME
                    elif settings_button.collidepoint(mouse_pos):
                        game_state = STATE_SETTINGS
                    elif quit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                    elif fullscreen_button.collidepoint(mouse_pos):
                        new_index = RES_INDEX_BORDERLESS if not fullscreen else 0
                        set_resolution(new_index)
                    slider_rect = pygame.Rect((VIRTUAL_WIDTH - 200) // 2, VIRTUAL_HEIGHT - 120, 200, 20)
                    if slider_rect.collidepoint(mouse_pos):
                        global dragging_volume
                        dragging_volume = True
            elif event.type == pygame.MOUSEMOTION and dragging_volume:
                mouse_x = mouse_pos[0]
                global volume
                volume = max(0.0, min(1.0, (mouse_x - (VIRTUAL_WIDTH - 200) // 2) / 200))
            elif event.type == pygame.MOUSEBUTTONUP:
                global dragging_volume
                dragging_volume = False
        draw_button(play_button, "Play", mouse_pos)
        draw_button(settings_button, "Settings", mouse_pos)
        draw_button(quit_button, "Quit", mouse_pos)
        draw_button(fullscreen_button, "Fullscreen", mouse_pos)
        draw_volume_slider()
        help_text = pygame.font.SysFont(None, 24).render("F11 ou botão para Fullscreen", True, WHITE)
        virtual_screen.blit(help_text, (10, VIRTUAL_HEIGHT - 30))
        screen.blit(pygame.transform.scale(virtual_screen, (current_width, current_height)), (0, 0))
        pygame.display.flip()
        clock.tick(60)

def settings_menu():
    global game_state
    video_button = pygame.Rect(300, 200, 200, 50)
    keybinds_button = pygame.Rect(300, 260, 200, 50)
    back_button = pygame.Rect(10, 10, 100, 30)
    while game_state == STATE_SETTINGS:
        virtual_screen.fill(MENU_BG)
        mouse_pos = scale_mouse(pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if video_button.collidepoint(mouse_pos):
                    game_state = STATE_VIDEO
                elif keybinds_button.collidepoint(mouse_pos):
                    game_state = STATE_KEYBINDS
                elif back_button.collidepoint(mouse_pos):
                    game_state = STATE_MENU
        draw_button(video_button, "Video Settings", mouse_pos)
        draw_button(keybinds_button, "Keybinds", mouse_pos)
        draw_button(back_button, "Voltar", mouse_pos)
        screen.blit(pygame.transform.scale(virtual_screen, (current_width, current_height)), (0, 0))
        pygame.display.flip()
        clock.tick(60)

def video_menu():
    global game_state, current_res_index
    buttons = [pygame.Rect(100, 100 + i * 40, 600, 30) for i in range(len(RESOLUTIONS))]
    back_btn = pygame.Rect(10, 10, 100, 30)
    while game_state == STATE_VIDEO:
        virtual_screen.fill(MENU_BG)
        mouse_pos = scale_mouse(pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, btn in enumerate(buttons):
                    if btn.collidepoint(mouse_pos):
                        set_resolution(i)
                if back_btn.collidepoint(mouse_pos):
                    game_state = STATE_SETTINGS
        font = pygame.font.SysFont(None, 32)
        for i, res in enumerate(RESOLUTIONS):
            color = (255, 255, 0) if i == current_res_index else (200, 200, 200)
            text = f"{res[0]}x{res[1]}" if isinstance(res, tuple) else res
            virtual_screen.blit(font.render(text, True, color), (100, 100 + i * 40))
        draw_button(back_btn, "Voltar", mouse_pos)
        screen.blit(pygame.transform.scale(virtual_screen, (current_width, current_height)), (0, 0))
        pygame.display.flip()
        clock.tick(60)

def keybinds_menu():
    global game_state, waiting_for_key
    actions = list(keybinds.keys())
    buttons = []
    start_y = 100
    for i, action in enumerate(actions):
        rect1 = pygame.Rect(100, start_y + i * 60, 200, 40)
        rect2 = pygame.Rect(320, start_y + i * 60, 200, 40)
        buttons.append((action, 0, rect1))
        buttons.append((action, 1, rect2))
    back_btn = pygame.Rect(10, 10, 100, 30)
    while game_state == STATE_KEYBINDS:
        virtual_screen.fill(MENU_BG)
        mouse_pos = scale_mouse(pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and waiting_for_key:
                action, index = waiting_for_key
                keybinds[action][index] = event.key
                waiting_for_key = None
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for action, index, rect in buttons:
                    if rect.collidepoint(mouse_pos):
                        waiting_for_key = (action, index)
                if back_btn.collidepoint(mouse_pos):
                    game_state = STATE_SETTINGS
        font = pygame.font.SysFont(None, 28)
        for action, index, rect in buttons:
            color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(virtual_screen, color, rect)
            key_display = key_name(keybinds[action][index]) if not waiting_for_key == (action, index) else "..."
            text = f"{keybind_names[action]} {index+1}: {key_display}" if index == 0 else f"{key_display}"
            text_surf = font.render(text, True, WHITE)
            text_rect = text_surf.get_rect(center=rect.center)
            virtual_screen.blit(text_surf, text_rect)
        draw_button(back_btn, "Voltar", mouse_pos)
        screen.blit(pygame.transform.scale(virtual_screen, (current_width, current_height)), (0, 0))
        pygame.display.flip()
        clock.tick(60)

def game_loop():
    global last_spell_time, game_state
    while game_state == STATE_GAME:
        virtual_screen.fill(BG_COLOR)
        mouse_pos = scale_mouse(pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = STATE_MENU
                if event.key == pygame.K_F11:
                    global fullscreen, current_res_index
                    current_res_index = RES_INDEX_BORDERLESS if not fullscreen else 0
                    set_resolution(current_res_index)
                if event.key in keybinds["fireball"]:
                    current_time = pygame.time.get_ticks()
                    if current_time - last_spell_time >= COOLDOWN_FIREBALL:
                        px = player_pos[0] + PLAYER_SIZE // 2
                        py = player_pos[1] + PLAYER_SIZE // 2
                        dx = mouse_pos[0] - px
                        dy = mouse_pos[1] - py
                        dist = (dx ** 2 + dy ** 2) ** 0.5
                        if dist > 0:
                            spells.append({
                                "pos": [px, py],
                                "dir": [dx / dist, dy / dist]
                            })
                            last_spell_time = current_time
        keys = pygame.key.get_pressed()
        move_dir = [0, 0]
        if any(keys[k] for k in keybinds['up']): move_dir[1] -= 1
        if any(keys[k] for k in keybinds['down']): move_dir[1] += 1
        if any(keys[k] for k in keybinds['left']): move_dir[0] -= 1
        if any(keys[k] for k in keybinds['right']): move_dir[0] += 1
        if move_dir[0] or move_dir[1]:
            length = (move_dir[0] ** 2 + move_dir[1] ** 2) ** 0.5
            move_dir[0] /= length
            move_dir[1] /= length
        player_pos[0] = max(0, min(VIRTUAL_WIDTH - PLAYER_SIZE, player_pos[0] + move_dir[0] * PLAYER_SPEED))
        player_pos[1] = max(0, min(VIRTUAL_HEIGHT - PLAYER_SIZE, player_pos[1] + move_dir[1] * PLAYER_SPEED))
        for spell in spells[:]:
            spell["pos"][0] += spell["dir"][0] * SPELL_SPEED
            spell["pos"][1] += spell["dir"][1] * SPELL_SPEED
            if not (0 <= spell["pos"][0] <= VIRTUAL_WIDTH and 0 <= spell["pos"][1] <= VIRTUAL_HEIGHT):
                spells.remove(spell)
        virtual_screen.blit(personagem_img, player_pos)
        for spell in spells:
            pygame.draw.circle(virtual_screen, RED, (int(spell["pos"][0]), int(spell["pos"][1])), SPELL_SIZE)
        draw_fireball_ui()
        screen.blit(pygame.transform.scale(virtual_screen, (current_width, current_height)), (0, 0))
        pygame.display.flip()
        clock.tick(60)

while True:
    if game_state == STATE_MENU:
        main_menu()
    elif game_state == STATE_GAME:
        game_loop()
    elif game_state == STATE_SETTINGS:
        settings_menu()
    elif game_state == STATE_VIDEO:
        video_menu()
    elif game_state == STATE_KEYBINDS:
        keybinds_menu()
