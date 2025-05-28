import pygame
from settings import current_width, current_height
from settings import volume
def reload_images():
    global BG_IMAGE, BUTTON_IMAGE
    try:
        BG_IMAGE = pygame.image.load("main-menu.jpg")
        BG_IMAGE = pygame.transform.scale(BG_IMAGE, (current_width, current_height))
    except:
        BG_IMAGE = None
    try:
        BUTTON_IMAGE = pygame.image.load("bigbutton.jpg")
        BUTTON_IMAGE = pygame.transform.scale(BUTTON_IMAGE, (int(current_width * 0.5), int(current_height * 0.2)))
    except:
        BUTTON_IMAGE = None
    pass
# Sprites do jogador
PLAYER_SPRITES = {
    "up": pygame.image.load("sprite_pcima.png").convert_alpha(),
    "down": pygame.image.load("sprite_pbaixo.png").convert_alpha(),
    "left": pygame.image.load("sprite_pesquerda.png").convert_alpha(),
    "right": pygame.image.load("sprite_pdireita.png").convert_alpha()
}
FIREBALL_FRAMES = [
    pygame.image.load("fireball_0.png").convert_alpha(),
    pygame.image.load("fireball_1.png").convert_alpha(),
    pygame.image.load("fireball_2.png").convert_alpha(),
    pygame.image.load("fireball_3.png").convert_alpha(),
    pygame.image.load("fireball_4.png").convert_alpha(),
]
# Inicialização dos assets
BG_IMAGE = None
BUTTON_IMAGE = None
reload_images()

hollowpurple_sound = pygame.mixer.Sound("hollowpurple_sound.wav")

fireball_sound = pygame.mixer.Sound("fireball_woosh.wav")

sound_effects = {
    "fireball": fireball_sound,
    "hollowpurple": hollowpurple_sound,
}
