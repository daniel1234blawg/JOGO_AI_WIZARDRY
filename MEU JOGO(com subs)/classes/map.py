import pygame
import pytmx
from pytmx.util_pygame import load_pygame
from shapely.geometry import Point, Polygon
from classes.player import Player
class Map:
    def __init__(self, filename):
        print(f"Carregando mapa: {filename}")

        try:
            self.tmx_data = load_pygame(filename, pixelalpha=True)
            print(f"Mapa carregado com sucesso!")
            print(f"Dimensões: {self.tmx_data.width}x{self.tmx_data.height}")
            print(f"Tamanho dos tiles: {self.tmx_data.tilewidth}x{self.tmx_data.tileheight}")
        except Exception as e:
            print(f"ERRO ao carregar mapa: {e}")
            return



        self.tmx_data = load_pygame(filename)
        self.tilewidth = self.tmx_data.tilewidth
        self.tileheight = self.tmx_data.tileheight
        self.barriers = []
        self.spawn_point = (0, 0)
        self.camera_offset = (0, 0)
        self.draw_order = [
            "Base", "PSombra", "Pedra", "SSombra", "Paredes",
            "PObjetos", "TilesSobPObjetos", "jogador",
            "Barreiras e Pontos", "SObjetos", "TilesSobSObjetos", "ObjetosParede"
        ]

        # Carrega objetos e camadas
        self._load_objects()
        self._load_tile_layers()

        print(f"Spawn point: {self.spawn_point}")
        print(f"Barreiras carregadas: {len(self.barriers)}")
        print(f"Camadas de tiles: {list(self.tile_layers.keys())}")


    def _load_objects(self):
        for layer in self.tmx_data.layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                print(f"Camada de objetos encontrada: {layer.name}")
                for obj in layer:
                    print(f"  Objeto: {obj.name} | Tipo: {obj.type} | Posição: ({obj.x}, {obj.y})")
                    if obj.name == "Spawn" and obj.type == "point":
                        self.spawn_point = (obj.x, obj.y)
                    elif obj.type == "barrier":
                        self._add_barrier(obj)
                        print(f"!!! Barreira adicionada em: ({obj.x}, {obj.y})")
                        print(f"Total de barreiras carregadas: {len(self.barriers)}")

    def _add_barrier(self, obj):
        if hasattr(obj, 'points'):
            poly = Polygon([(pt[0] + obj.x, pt[1] + obj.y) for pt in obj.points])
        else:
            poly = Polygon([
                (obj.x, obj.y),
                (obj.x + obj.width, obj.y),
                (obj.x + obj.width, obj.y + obj.height),
                (obj.x, obj.y + obj.height)
            ])
        self.barriers.append(poly)

    def _load_tile_layers(self):
        self.tile_layers = {}
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                self.tile_layers[layer.name] = layer

    def update_camera(self, player, screen_width, screen_height):
        self.camera_offset = (
            player.rect.centerx - screen_width // 2,
            player.rect.centery - screen_height // 2
        )

    def is_blocked(self, x, y):
        point = Point(x, y)
        for barrier in self.barriers:
            if barrier.contains(point):
                return True
        return False

    def draw(self, screen):
        # Debug: verifica se as camadas existem
        if not self.tile_layers:
            print("Nenhuma camada de tiles carregada!")
            return

        for layer_name in self.draw_order:
            if layer_name == "jogador":
                continue  # Skip player layer

            layer = self.tile_layers.get(layer_name)
            if layer:
                for x, y, gid in layer:
                    if gid:  # Só desenha se o gid não for 0
                        tile = self.tmx_data.get_tile_image_by_gid(gid)
                        if tile:
                            pos_x = x * self.tilewidth - self.camera_offset[0]
                            pos_y = y * self.tileheight - self.camera_offset[1]
                            screen.blit(tile, (x * self.tilewidth - self.camera_offset[0], y * self.tileheight - self.camera_offset[1]))