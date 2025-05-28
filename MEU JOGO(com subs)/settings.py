import pygame


# --- Configurações iniciais (res e fps) ---
FPS = 60

RESOLUTIONS = [
    (1280, 720),
    (1366, 768),
    (1600, 900),
    (1920, 1080)
]

VIRTUAL_WIDTH, VIRTUAL_HEIGHT = 1600, 900
current_res_index = 2
current_width, current_height = RESOLUTIONS[current_res_index]

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (237, 41, 57)
GREEN = (50, 200, 50)
BLUE = (80, 200, 250)
MAGIC_PURPLE = (120, 80, 200)
MAGIC_GOLD = (255, 215, 120)
GRAY = (90, 90, 150)
DARK_GRAY = (50, 50, 80)
LIGHT_GRAY = (140, 140, 180)
PURPLE = (170, 70, 255)
BG_COLOR = LIGHT_GRAY


# Keybinds padrão
DEFAULT_KEYBINDS = {
    "move_up": [pygame.K_w],
    "move_down": [pygame.K_s],
    "move_left": [pygame.K_a],
    "move_right": [pygame.K_d],
    "fireball": [pygame.K_f],
    "hollowpurple": [pygame.K_c]
}

keybinds = {k: v[:] for k, v in DEFAULT_KEYBINDS.items()}

volume = 75


def get_fonts():
    FONT = pygame.font.SysFont("arial", 36, bold=True)
    SMALL_FONT = pygame.font.SysFont("arial", 24)
    TINY_FONT = pygame.font.SysFont("arial", 18)
    TITLE_FONT = pygame.font.SysFont("arial", 28, bold=True)
    return FONT, SMALL_FONT, TINY_FONT, TITLE_FONT



SLOWMO_DURATION = 2.0
SLOWMO_FACTOR = 0.3