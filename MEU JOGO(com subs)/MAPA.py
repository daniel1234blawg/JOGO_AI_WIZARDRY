import pygame
import pytmx
from pytmx.util_pygame import load_pygame
from shapely.geometry import Point, Polygon

# Configurações da tela e jogador
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLAYER_SPEED = 3

# Inicializa Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mapa")
clock = pygame.time.Clock()

# Carrega o mapa
tmx_data = load_pygame("tiled/wizardry.tmx")

# Carrega a imagem do jogador
player_img = pygame.image.load("sprite_pbaixo.png").convert_alpha()
player_rect = player_img.get_rect()

# Inicializa variáveis
spawn_point = (0, 0)
barriers = []
tilewidth, tileheight = tmx_data.tilewidth, tmx_data.tileheight

# Extrai informações do mapa
tile_layers = {}
for layer in tmx_data.visible_layers:
    if isinstance(layer, pytmx.TiledTileLayer):
        tile_layers[layer.name] = layer

# Define spawn e barreiras
for layer in tmx_data.layers:
    if isinstance(layer, pytmx.TiledObjectGroup):
        for obj in layer:
            if obj.name == "Spawn" and obj.type == "point":
                spawn_point = (obj.x, obj.y)
            elif obj.type == "barrier":
                if hasattr(obj, 'points'):
                    poly = Polygon([(pt[0] + obj.x, pt[1] + obj.y) for pt in obj.points])
                else:
                    poly = Polygon([
                        (obj.x, obj.y),
                        (obj.x + obj.width, obj.y),
                        (obj.x + obj.width, obj.y + obj.height),
                        (obj.x, obj.y + obj.height)
                    ])
                barriers.append(poly)

# Ponto de partida do jogador
player_rect.center = spawn_point

# Ordem de camadas de tile
DRAW_ORDER = ["Base", "PSombra", "Pedra", "SSombra", "Paredes", "PObjetos", "TilesSobPObjetos", "jogador", "Barreiras e Pontos", "SObjetos", "TilesSobSObjetos", "ObjetosParede"]

# Verifica colisão com barreiras
def is_blocked(x, y):
    point = Point(x, y)
    for barrier in barriers:
        if barrier.contains(point):
            return True
    return False

# Extrai objetos desenháveis com y-sorting
def get_drawable_objects():
    drawables = []

    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledObjectGroup):
            for obj in layer:
                if obj.type == "skip":
                    image = tmx_data.get_tile_image_by_gid(obj.gid)
                    if image:
                        screen.blit(image, (obj.x - camera_offset[0], obj.y - camera_offset[1]))
                elif obj.gid:
                    image = tmx_data.get_tile_image_by_gid(obj.gid)
                    if image:
                        pos = (obj.x - camera_offset[0], obj.y - camera_offset[1])
                        bottom = obj.y + obj.height
                        drawables.append((bottom, image, pos))

    # Adiciona jogador
    pos = (player_rect.x - camera_offset[0], player_rect.y - camera_offset[1])
    drawables.append((player_rect.bottom, player_img, pos))

    # Ordena por profundidade (Y)
    drawables.sort(key=lambda x: x[0])
    return drawables

# Loop principal
running = True
while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    dx = dy = 0
    if keys[pygame.K_LEFT]: dx -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]: dx += PLAYER_SPEED
    if keys[pygame.K_UP]: dy -= PLAYER_SPEED
    if keys[pygame.K_DOWN]: dy += PLAYER_SPEED

    new_x = player_rect.centerx + dx
    new_y = player_rect.centery + dy
    if not is_blocked(new_x, new_y):
        player_rect.centerx = new_x
        player_rect.centery = new_y

    camera_offset = (
        player_rect.centerx - SCREEN_WIDTH // 2,
        player_rect.centery - SCREEN_HEIGHT // 2
    )

    screen.fill((0, 0, 0))

    for layer_name in DRAW_ORDER:
        if layer_name != "jogador":
            layer = tile_layers.get(layer_name)
            if layer:
                for x, y, gid in layer:
                    tile = tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        screen.blit(tile, (
                            x * tilewidth - camera_offset[0],
                            y * tileheight - camera_offset[1]
                        ))
        else:
            drawables = get_drawable_objects()
            for _, img, pos in drawables:
                screen.blit(img, pos)

    pygame.display.flip()

pygame.quit()
