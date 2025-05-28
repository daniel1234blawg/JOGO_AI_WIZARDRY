import pygame
import sys
import os
import ctypes

# Inicializar o Pygame
pygame.init()

# Constantes
WINDOWED_WIDTH, WINDOWED_HEIGHT = 800, 600
VIRTUAL_WIDTH, VIRTUAL_HEIGHT = 800, 600
PLAYER_SIZE = 32
SPELL_SIZE = 8
PLAYER_SPEED = 4
SPELL_SPEED = 8

# Cores
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
RED = (255, 50, 50)
BG_COLOR = (30, 30, 30)

# Volume
VOLUME_SLIDER_WIDTH = 200
VOLUME_SLIDER_HEIGHT = 20
volume = 0.5
dragging_volume = False

# Direções
DIRS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}

# Constantes de UI
UI_SQUARE_SIZE = 100
UI_SQUARE_COLOR = (70, 70, 70)
UI_TEXT_COLOR = (255, 255, 255)
UI_COOLDOWN_COLOR = (255, 100, 100)

# Configuração de fonte
font = pygame.font.SysFont(None, 32)
small_font = pygame.font.SysFont(None, 24)

# Sistema de fullscreen
fullscreen = False
current_width, current_height = WINDOWED_WIDTH, WINDOWED_HEIGHT
virtual_screen = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))


def get_native_resolution():
    """Obtém a resolução nativa do monitor principal"""
    try:
        user32 = ctypes.windll.user32
        return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    except:
        info = pygame.display.Info()
        return (info.current_w, info.current_h)


def toggle_fullscreen():
    global fullscreen, current_width, current_height, screen
    fullscreen = not fullscreen

    if fullscreen:
        native_w, native_h = get_native_resolution()
        flags = pygame.NOFRAME | pygame.HWSURFACE | pygame.DOUBLEBUF
        screen = pygame.display.set_mode((native_w, native_h), flags)
    else:
        flags = pygame.SCALED | pygame.RESIZABLE
        screen = pygame.display.set_mode((WINDOWED_WIDTH, WINDOWED_HEIGHT), flags)
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{(get_native_resolution()[0] - WINDOWED_WIDTH) // 2},100"

    current_width, current_height = screen.get_size()
    pygame.display.quit()
    pygame.display.init()


# Configuração inicial da janela
os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode((WINDOWED_WIDTH, WINDOWED_HEIGHT), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption("Mage Spellcaster Prototype")

clock = pygame.time.Clock()

# Jogador
player_pos = [VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT // 2]
player_dir = "DOWN"

personagem_img = pygame.image.load("personagem.png").convert_alpha()
personagem_img = pygame.transform.scale(personagem_img, (PLAYER_SIZE, PLAYER_SIZE))

# Feitiços
COOLDOWN_fireball = 2500
last_spell_time = -COOLDOWN_fireball
spells = []

# Estados do jogo
STATE_MENU = "menu"
STATE_GAME = "game"
STATE_KEYBINDS = "keybinds"
game_state = STATE_MENU

# Teclas configuráveis
keybinds = {
    "fireball": [pygame.K_f, pygame.K_SPACE],
    "up": [pygame.K_w, pygame.K_UP],
    "down": [pygame.K_s, pygame.K_DOWN],
    "left": [pygame.K_a, pygame.K_LEFT],
    "right": [pygame.K_d, pygame.K_RIGHT]
}
keybind_names = {
    "fireball": "Bola de fogo",
    "up": "Mover Cima",
    "down": "Mover Baixo",
    "left": "Mover Esquerda",
    "right": "Mover Direita"
}
waiting_for_key = None


def key_name(key):
    return pygame.key.name(key).upper()


def draw_volume_slider():
    slider_x = (VIRTUAL_WIDTH - VOLUME_SLIDER_WIDTH) // 2
    slider_y = VIRTUAL_HEIGHT - 120
    pygame.draw.rect(virtual_screen, (100, 100, 100), (slider_x, slider_y, VOLUME_SLIDER_WIDTH, VOLUME_SLIDER_HEIGHT))
    handle_x = slider_x + int(volume * VOLUME_SLIDER_WIDTH)
    pygame.draw.circle(virtual_screen, (200, 200, 200), (handle_x, slider_y + VOLUME_SLIDER_HEIGHT // 2), 10)
    txt = small_font.render(f"Volume: {int(volume * 100)}%", True, (220, 220, 220))
    virtual_screen.blit(txt, (slider_x + VOLUME_SLIDER_WIDTH + 15, slider_y - 5))


def draw_fireball_ui():
    square_x = (VIRTUAL_WIDTH - UI_SQUARE_SIZE) // 2
    square_y = VIRTUAL_HEIGHT - UI_SQUARE_SIZE - 10

    pygame.draw.rect(virtual_screen, UI_SQUARE_COLOR, (square_x, square_y, UI_SQUARE_SIZE, UI_SQUARE_SIZE))
    text_surface = small_font.render("fireball", True, UI_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(square_x + UI_SQUARE_SIZE // 2, square_y + UI_SQUARE_SIZE // 2 - 10))
    virtual_screen.blit(text_surface, text_rect)

    cooldown_remaining = max(0, (COOLDOWN_fireball - (pygame.time.get_ticks() - last_spell_time)) / 1000)
    cooldown_text = f"{cooldown_remaining:.1f}s" if cooldown_remaining > 0 else "Ready"
    cooldown_surface = small_font.render(cooldown_text, True, UI_COOLDOWN_COLOR)
    cooldown_rect = cooldown_surface.get_rect(topright=(square_x + UI_SQUARE_SIZE - 5, square_y + 5))
    virtual_screen.blit(cooldown_surface, cooldown_rect)

    keybind_text = f"Keys: {key_name(keybinds['fireball'][0])}, {key_name(keybinds['fireball'][1])}"
    keybind_surface = small_font.render(keybind_text, True, UI_TEXT_COLOR)
    keybind_rect = keybind_surface.get_rect(center=(square_x + UI_SQUARE_SIZE // 2, square_y + UI_SQUARE_SIZE - 16))
    virtual_screen.blit(keybind_surface, keybind_rect)


def draw_button(rect, text, mouse_pos):
    color = (100, 160, 210) if rect.collidepoint(mouse_pos) else (70, 130, 180)
    pygame.draw.rect(virtual_screen, color, rect)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    virtual_screen.blit(text_surface, text_rect)


def main_menu():
    global game_state, volume, dragging_volume

    play_button = pygame.Rect(VIRTUAL_WIDTH // 2 - 100, VIRTUAL_HEIGHT // 2 - 60, 200, 50)
    quit_button = pygame.Rect(VIRTUAL_WIDTH // 2 - 100, VIRTUAL_HEIGHT // 2 + 10, 200, 50)
    keybind_button = pygame.Rect(VIRTUAL_WIDTH // 2 - 100, VIRTUAL_HEIGHT // 2 + 80, 200, 50)
    fullscreen_button = pygame.Rect(VIRTUAL_WIDTH - 130, 10, 120, 40)

    while game_state == STATE_MENU:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                toggle_fullscreen()

            if event.type == pygame.MOUSEBUTTONDOWN:
                slider_rect = pygame.Rect((VIRTUAL_WIDTH - VOLUME_SLIDER_WIDTH) // 2, VIRTUAL_HEIGHT - 120,
                                          VOLUME_SLIDER_WIDTH, VOLUME_SLIDER_HEIGHT)
                if slider_rect.collidepoint(event.pos):
                    dragging_volume = True

                if event.button == 1:
                    mouse_pos = (event.pos[0] * VIRTUAL_WIDTH // current_width,
                                 event.pos[1] * VIRTUAL_HEIGHT // current_height)

                    if play_button.collidepoint(mouse_pos):
                        game_state = STATE_GAME
                    elif quit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                    elif keybind_button.collidepoint(mouse_pos):
                        game_state = STATE_KEYBINDS
                    elif fullscreen_button.collidepoint(mouse_pos):
                        toggle_fullscreen()

            elif event.type == pygame.MOUSEMOTION and dragging_volume:
                mouse_x = event.pos[0] * VIRTUAL_WIDTH // current_width
                slider_start = (VIRTUAL_WIDTH - VOLUME_SLIDER_WIDTH) // 2
                new_volume = (mouse_x - slider_start) / VOLUME_SLIDER_WIDTH
                volume = max(0.0, min(1.0, new_volume))
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_volume = False

        virtual_screen.fill((25, 25, 40))
        mouse_pos = (pygame.mouse.get_pos()[0] * VIRTUAL_WIDTH // current_width,
                     pygame.mouse.get_pos()[1] * VIRTUAL_HEIGHT // current_height)

        # Título
        title_surface = font.render("Mage Spellcaster", True, (255, 220, 120))
        title_rect = title_surface.get_rect(center=(VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT // 2 - 120))
        virtual_screen.blit(title_surface, title_rect)

        # Botões
        draw_button(play_button, "Jogar", mouse_pos)
        draw_button(quit_button, "Sair", mouse_pos)
        draw_button(keybind_button, "Teclas", mouse_pos)
        draw_button(fullscreen_button, "Fullscreen", mouse_pos)

        # Elementos de UI
        draw_volume_slider()
        instructions = small_font.render(
            f"Pressione {key_name(keybinds['fireball'][0])} ou {key_name(keybinds['fireball'][1])} para atirar",
            True, (180, 180, 180))
        virtual_screen.blit(instructions, (VIRTUAL_WIDTH // 2 - instructions.get_width() // 2, VIRTUAL_HEIGHT - 60))

        scaled_screen = pygame.transform.scale(virtual_screen, (current_width, current_height))
        screen.blit(scaled_screen, (0, 0))
        pygame.display.flip()
        clock.tick(60)


def keybind_menu():
    global game_state, waiting_for_key
    actions = list(keybinds.keys())
    buttons = []
    start_y = VIRTUAL_HEIGHT // 2 - (len(actions) * 35)

    for i, action in enumerate(actions):
        rect1 = pygame.Rect(VIRTUAL_WIDTH // 2 - 200, start_y + i * 60, 140, 50)
        rect2 = pygame.Rect(VIRTUAL_WIDTH // 2 + 60, start_y + i * 60, 140, 50)
        buttons.append((action, 0, rect1))
        buttons.append((action, 1, rect2))

    back_button = pygame.Rect(VIRTUAL_WIDTH // 2 - 100, VIRTUAL_HEIGHT - 80, 200, 50)

    while game_state == STATE_KEYBINDS:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = STATE_MENU

                if waiting_for_key:
                    action, index = waiting_for_key
                    keybinds[action][index] = event.key
                    waiting_for_key = None

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = (event.pos[0] * VIRTUAL_WIDTH // current_width,
                             event.pos[1] * VIRTUAL_HEIGHT // current_height)
                for action, index, rect in buttons:
                    if rect.collidepoint(mouse_pos):
                        waiting_for_key = (action, index)
                if back_button.collidepoint(mouse_pos):
                    game_state = STATE_MENU

        virtual_screen.fill((15, 15, 30))
        mouse_pos = (pygame.mouse.get_pos()[0] * VIRTUAL_WIDTH // current_width,
                     pygame.mouse.get_pos()[1] * VIRTUAL_HEIGHT // current_height)

        # Título
        title_surface = font.render("Configurar Teclas", True, (255, 220, 120))
        title_rect = title_surface.get_rect(center=(VIRTUAL_WIDTH // 2, 80))
        virtual_screen.blit(title_surface, title_rect)

        # Botões
        for action, index, rect in buttons:
            color = (100, 160, 210) if rect.collidepoint(mouse_pos) else (70, 130, 180)
            pygame.draw.rect(virtual_screen, color, rect)
            key_text = key_name(keybinds[action][index]) if not waiting_for_key == (action, index) else "..."
            text_surface = small_font.render(key_text, True, WHITE)
            text_rect = text_surface.get_rect(center=rect.center)
            virtual_screen.blit(text_surface, text_rect)

            if index == 0:
                action_label = small_font.render(keybind_names[action], True, (200, 200, 200))
                virtual_screen.blit(action_label, (rect.x - 160, rect.y + 15))

        draw_button(back_button, "Voltar", mouse_pos)

        # Instruções
        instr_text = "Clique em uma tecla para alterar" if not waiting_for_key else "Pressione a nova tecla..."
        instructions = small_font.render(instr_text, True, (180, 180, 180))
        virtual_screen.blit(instructions, (VIRTUAL_WIDTH // 2 - instructions.get_width() // 2, VIRTUAL_HEIGHT - 40))

        scaled_screen = pygame.transform.scale(virtual_screen, (current_width, current_height))
        screen.blit(scaled_screen, (0, 0))
        pygame.display.flip()
        clock.tick(60)


# Main game loop
while True:
    if game_state == STATE_MENU:
        main_menu()
    elif game_state == STATE_KEYBINDS:
        keybind_menu()
    else:
        virtual_screen.fill(BG_COLOR)

        # Movimento do jogador
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if any(keys[k] for k in keybinds["up"]): dy -= 1
        if any(keys[k] for k in keybinds["down"]): dy += 1
        if any(keys[k] for k in keybinds["left"]): dx -= 1
        if any(keys[k] for k in keybinds["right"]): dx += 1

        if dx != 0 or dy != 0:
            length = (dx ** 2 + dy ** 2) ** 0.5
            dx_normalized = dx / length
            dy_normalized = dy / length
        else:
            dx_normalized = dy_normalized = 0

        player_pos[0] = max(0, min(VIRTUAL_WIDTH - PLAYER_SIZE, player_pos[0] + dx_normalized * PLAYER_SPEED))
        player_pos[1] = max(0, min(VIRTUAL_HEIGHT - PLAYER_SIZE, player_pos[1] + dy_normalized * PLAYER_SPEED))

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    toggle_fullscreen()

                if event.key in keybinds["fireball"]:
                    current_time = pygame.time.get_ticks()
                    if current_time - last_spell_time >= COOLDOWN_fireball:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        mouse_x = mouse_x * VIRTUAL_WIDTH // current_width
                        mouse_y = mouse_y * VIRTUAL_HEIGHT // current_height

                        player_center_x = player_pos[0] + PLAYER_SIZE // 2
                        player_center_y = player_pos[1] + PLAYER_SIZE // 2
                        dir_x = mouse_x - player_center_x
                        dir_y = mouse_y - player_center_y
                        length = (dir_x ** 2 + dir_y ** 2) ** 0.5

                        if length != 0:
                            dir_x /= length
                            dir_y /= length
                        else:
                            dir_x, dir_y = 0, 0

                        spell_x = player_center_x - SPELL_SIZE // 2
                        spell_y = player_center_y - SPELL_SIZE // 2
                        spells.append({
                            "pos": [spell_x, spell_y],
                            "dir_vector": [dir_x, dir_y],
                            "hitbox": pygame.Rect(
                                spell_x - SPELL_SIZE,
                                spell_y - SPELL_SIZE,
                                SPELL_SIZE * 2,
                                SPELL_SIZE * 2
                            )
                        })
                        last_spell_time = current_time

        # Atualizar projéteis
        for spell in spells:
            spell["pos"][0] += spell["dir_vector"][0] * SPELL_SPEED
            spell["pos"][1] += spell["dir_vector"][1] * SPELL_SPEED
            spell["hitbox"].center = (spell["pos"][0], spell["pos"][1])

        spells = [s for s in spells if 0 <= s["pos"][0] <= VIRTUAL_WIDTH and 0 <= s["pos"][1] <= VIRTUAL_HEIGHT]

        # Desenhar elementos
        virtual_screen.blit(personagem_img, player_pos)
        for spell in spells:
            pygame.draw.circle(virtual_screen, RED, (int(spell["pos"][0]), int(spell["pos"][1])), SPELL_SIZE)

        draw_fireball_ui()

        # Atualizar display
        scaled_screen = pygame.transform.scale(virtual_screen, (current_width, current_height))
        screen.blit(scaled_screen, (0, 0))
        pygame.display.flip()
        clock.tick(60)
