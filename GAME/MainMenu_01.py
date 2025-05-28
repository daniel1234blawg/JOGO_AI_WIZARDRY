import pygame
import sys
import time
import math


# --- Configurações iniciais ---
pygame.init()
pygame.font.init()
FPS = 60

# Resoluções disponíveis
RESOLUTIONS = [
    (1280, 720),
    (1366, 768),
    (1600, 900),
    (1920, 1080)
]

VIRTUAL_WIDTH, VIRTUAL_HEIGHT = 1600, 900
current_res_index = 2  # Começa em 1600x900
current_width, current_height = RESOLUTIONS[current_res_index]

# Cores melhoradas (tema mágico)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (237, 41, 57)
GREEN = (50, 200, 50)
BLUE = (80, 200, 250)
MAGIC_PURPLE = (120, 80, 200)  # Roxo mágico
MAGIC_GOLD = (255, 215, 120)  # Dourado mágico
GRAY = (90, 90, 150)
DARK_GRAY = (50, 50, 80)  # Cinza mais escuro
LIGHT_GRAY = (140, 140, 180)  # Cinza mais claro
BG_COLOR = LIGHT_GRAY

# Fontes melhoradas
FONT = pygame.font.SysFont("arial", 36, bold=True)
SMALL_FONT = pygame.font.SysFont("arial", 24)
TINY_FONT = pygame.font.SysFont("arial", 18)
TITLE_FONT = pygame.font.SysFont("arial", 28, bold=True)

# Keybinds padrão (apenas as 5 ações pedidas)
DEFAULT_KEYBINDS = {
    "move_up": [pygame.K_w],
    "move_down": [pygame.K_s],
    "move_left": [pygame.K_a],
    "move_right": [pygame.K_d],
    "fireball": [pygame.K_f]
}
keybinds = {k: v[:] for k, v in DEFAULT_KEYBINDS.items()}

# Volume padrão (0-100)
volume = 75


# Função para escalar imagem mantendo proporção
def scale_image_aspect(img, box_size):
    bx, by = box_size
    ix, iy = img.get_size()
    scale_factor = min(bx / ix, by / iy)
    new_size = (int(ix * scale_factor), int(iy * scale_factor))
    # Converter para 32 bits se necessário
    if img.get_bitsize() < 24:
        if img.get_alpha():
            img = img.convert_alpha()
        else:
            img = img.convert()
    return pygame.transform.smoothscale(img, new_size)
#nao sei oq isto é
screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)

# Carregar sprites do personagem para cada direção
PLAYER_SPRITES = {
    "up": pygame.image.load("sprite_pcima.png").convert_alpha(),
    "down": pygame.image.load("sprite_pbaixo.png").convert_alpha(),
    "left": pygame.image.load("sprite_pesquerda.png").convert_alpha(),
    "right": pygame.image.load("sprite_pdireita.png").convert_alpha()
}



# --- Inicialização da janela ---
def reload_images():
    """Carrega e redimensiona imagens para a resolução atual"""
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


def set_resolution(index):
    """Define nova resolução e atualiza a janela"""
    global screen, current_width, current_height, current_res_index
    current_res_index = index
    current_width, current_height = RESOLUTIONS[index]
    screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
    reload_images()
    print(f"Resolução alterada para: {current_width}x{current_height}")


# Inicialização da janela
screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
pygame.display.set_caption("Jogo Demo - RPG Mágico")
clock = pygame.time.Clock()
reload_images()


# --- Classes do jogo (mantidas iguais) ---
class Spell:
    def __init__(self, name, key, color, cooldown=1.0):
        self.name = name
        self.key = key
        self.color = color
        self.cooldown = cooldown
        self.last_cast = -float('inf')

    def can_cast(self):
        return time.time() - self.last_cast >= self.cooldown


class Fireball(Spell):
    def __init__(self):
        super().__init__("Fireball", pygame.K_f, RED, cooldown=2.0)
        self.damage = 50
        self.speed = 15

    def cast(self, caster, projectiles, mouse_pos):
        if self.can_cast():
            x, y = caster.rect.center
            mx, my = mouse_pos
            dx = mx - x
            dy = my - y
            length = math.hypot(dx, dy)
            if length == 0:
                dx, dy = 0, -1  # Direção padrão para cima se o mouse estiver exatamente no centro
            else:
                dx /= length
                dy /= length
            projectiles.append(Projectile(x, y, dx, dy, self.color, self.speed, self.damage))
            self.last_cast = time.time()
            return True
        return False


class Projectile:
    def __init__(self, x, y, dx, dy, color, speed=15, damage=50):
        self.x = float(x)
        self.y = float(y)
        self.dx = dx * speed
        self.dy = dy * speed
        self.color = color
        self.radius = 20
        self.damage = damage
        self.lifetime = 300  # Frames até desaparecer
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.x = int(self.x - self.radius)
        self.rect.y = int(self.y - self.radius)
        self.lifetime -= 1
        return self.lifetime > 0 and 0 <= self.x <= current_width and 0 <= self.y <= current_height

    def draw(self, surface):
        # Desenha projétil com efeito visual
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 60)
        self.color = BLUE
        self.speed = 6
        self.facing = "up"
        self.spells = [Fireball()]
        self.health = 100
        self.max_health = 100

    def update(self, keys):
        dx, dy = 0, 0
        if any(keys[k] for k in keybinds["move_up"]): dy -= 1
        if any(keys[k] for k in keybinds["move_down"]): dy += 1
        if any(keys[k] for k in keybinds["move_left"]): dx -= 1
        if any(keys[k] for k in keybinds["move_right"]): dx += 1

        # Normalizar o vetor de movimento se necessário
        if dx != 0 or dy != 0:
            length = math.hypot(dx, dy)
            dx /= length
            dy /= length

            # Atualizar direção
            if dx > 0:
                self.facing = "right"
            elif dx < 0:
                self.facing = "left"
            elif dy > 0:
                self.facing = "down"
            elif dy < 0:
                self.facing = "up"

        # Movimento com limites da tela
        new_x = self.rect.x + dx * self.speed
        new_y = self.rect.y + dy * self.speed
        self.rect.x = max(0, min(int(new_x), current_width - self.rect.width))
        self.rect.y = max(0, min(int(new_y), current_height - self.rect.height))

    def draw(self, surface):
        # Escolhe o sprite correto conforme a direção
        sprite = PLAYER_SPRITES[self.facing]
        # Redimensiona o sprite para o tamanho do rect do player (mantém proporção)
        sprite_scaled = scale_image_aspect(sprite, (self.rect.width, self.rect.height))
        # Desenha o sprite na posição do rect
        surface.blit(sprite_scaled, self.rect.topleft)


# --- Botão melhorado com efeitos visuais ---
class Button:
    def __init__(self, x, y, w, h, text, color=GRAY, active=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = (min(255, color[0] + 50), min(255, color[1] + 50), min(255, color[2] + 50))
        self.active_color = MAGIC_GOLD if active else color
        self.is_hovered = False
        self.active = active

    def set_active(self, active):
        """Define se o botão está ativo (selecionado)"""
        self.active = active

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface):
        # Cor baseada no estado
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

        # Desenhar botão
        if BUTTON_IMAGE and not self.is_hovered and not self.active:
            scaled_img = scale_image_aspect(BUTTON_IMAGE, self.rect.size)
            img_rect = scaled_img.get_rect(center=self.rect.center)
            surface.blit(scaled_img, img_rect.topleft)
        else:
            pygame.draw.rect(surface, color, self.rect, border_radius=8)
            pygame.draw.rect(surface, border_color, self.rect, border_width, border_radius=8)

        # Desenhar texto
        text_color = BLACK if self.active else WHITE
        txt_surf = FONT.render(self.text, True, text_color)
        surface.blit(txt_surf,
                     (self.rect.centerx - txt_surf.get_width() // 2, self.rect.centery - txt_surf.get_height() // 2))

    def is_clicked(self, mouse_pos, event):
        return self.rect.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1


# --- Slider melhorado ---
class Slider:
    def __init__(self, x, y, w, h, value=75):
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
        # Barra base com efeito mágico
        pygame.draw.rect(surface, DARK_GRAY, self.rect, border_radius=12)
        pygame.draw.rect(surface, MAGIC_PURPLE, self.rect, 2, border_radius=12)

        # Barra de progresso com gradiente
        fill_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2,
                                int((self.rect.width - 4) * (self.value / 100)), self.rect.height - 4)
        pygame.draw.rect(surface, BLUE, fill_rect, border_radius=10)

        # Botão circular brilhante
        knob_x = self.rect.x + int(self.rect.width * (self.value / 100))
        pygame.draw.circle(surface, MAGIC_GOLD, (knob_x, self.rect.centery), self.rect.height // 2 + 4)
        pygame.draw.circle(surface, WHITE, (knob_x, self.rect.centery), self.rect.height // 2 + 1, 2)

        # Valor com estilo
        txt = SMALL_FONT.render(f"{self.value}%", True, MAGIC_GOLD)
        surface.blit(txt, (self.rect.right + 20, self.rect.centery - txt.get_height() // 2))


# --- Interface melhorada ---
def draw_fireball_cooldown(surface, fireball, keybinds, x, y, w, h):
    """Desenha barra de cooldown do fireball com visual melhorado"""
    pygame.draw.rect(surface, DARK_GRAY, (x, y, w, h), border_radius=8)
    pygame.draw.rect(surface, WHITE, (x, y, w, h), 2, border_radius=8)
    elapsed = time.time() - fireball.last_cast
    pct = min(elapsed / fireball.cooldown, 1.0)
    if pct < 1.0:
        progress_color = (200, 50, 50)
    else:
        progress_color = GREEN
    pygame.draw.rect(surface, progress_color, (x + 2, y + 2, (w - 4) * pct, h - 4), border_radius=6)
    keys_str = [pygame.key.name(k).upper() for k in keybinds["fireball"]]
    txt = f"Fireball [{'/'.join(keys_str)}]"
    txt_surf = SMALL_FONT.render(txt, True, WHITE)
    surface.blit(txt_surf, (x + 10, y + h // 2 - txt_surf.get_height() // 2))
    if pct < 1.0:
        cooldown_txt = f"{fireball.cooldown - elapsed:.2f}s"
        cd_surf = SMALL_FONT.render(cooldown_txt, True, (255, 180, 180))
    else:
        cd_surf = SMALL_FONT.render("PRONTO", True, GREEN)
    surface.blit(cd_surf, (x + w - cd_surf.get_width() - 10, y + h // 2 - cd_surf.get_height() // 2))




# --- Função para desenhar separadores visuais ---
def draw_section_separator(surface, y, width_offset=100):
    """Desenha uma linha separadora mágica"""
    start_x = width_offset
    end_x = current_width - width_offset
    # Linha principal
    pygame.draw.line(surface, MAGIC_PURPLE, (start_x, y), (end_x, y), 2)
    # Detalhes mágicos
    center_x = current_width // 2
    pygame.draw.circle(surface, MAGIC_GOLD, (center_x, y), 4)


# --- Menus ---
def main_menu():
    """Menu principal com 3 botões: Jogar, Definições, Sair"""
    while True:
        mouse_pos = pygame.mouse.get_pos()
        if BG_IMAGE:
            screen.blit(BG_IMAGE, (0, 0))
        else:
            screen.fill(BG_COLOR)

        # Botões principais
        b_w, b_h = int(current_width * 0.25), int(current_height * 0.10)
        buttons = [
            Button(current_width // 2 - b_w // 2, current_height // 2 - b_h * 2, b_w, b_h, "Jogar", GREEN),
            Button(current_width // 2 - b_w // 2, current_height // 2, b_w, b_h, "Definições", BLUE),
            Button(current_width // 2 - b_w // 2, current_height // 2 + b_h * 2, b_w, b_h, "Sair", RED)
        ]

        for btn in buttons:
            btn.update(mouse_pos)
            btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].is_clicked(mouse_pos, event):
                    main_game(keybinds)
                elif buttons[1].is_clicked(mouse_pos, event):
                    settings_menu()
                elif buttons[2].is_clicked(mouse_pos, event):
                    pygame.quit();
                    sys.exit()

        pygame.display.flip()
        clock.tick(FPS)


def settings_menu():
    """Menu de definições MELHORADO com organização visual superior"""
    global volume
    tab = 0  # 0 = Vídeo e Som, 1 = Keybinds
    slider = Slider(current_width // 2 - 250, 420, 500, 35, volume)

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
            Button(current_width // 2 - 240, 130, tab_w, tab_h, " Vídeo e Som",
                   MAGIC_PURPLE if tab == 0 else DARK_GRAY, active=(tab == 0)),
            Button(current_width // 2 + 20, 130, tab_w, tab_h, " Keybinds",
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
            screen.blit(res_label, (current_width // 2 - 250, 270))

            # Botões de resolução melhorados
            res_btns = []
            btn_w, btn_h = 200,70
            btn_font = SMALL_FONT
            start_x = current_width // 2 - (len(RESOLUTIONS) * btn_w + (len(RESOLUTIONS) - 1) * 15) // 2

            for i, res in enumerate(RESOLUTIONS):
                x = start_x + i * (btn_w + 15)
                y = 300
                label = f"{res[0]}×{res[1]}"
                is_current = (i == current_res_index)
                btn = Button(x, y, btn_w, btn_h, label, GREEN if is_current else GRAY, active=is_current)
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

        else:
            # --- SECÇÃO DE KEYBINDS ---
            kb_title = TITLE_FONT.render(" Configuração de Teclas", True, MAGIC_GOLD)
            screen.blit(kb_title, (current_width // 2 - kb_title.get_width() // 2, 220))

            draw_keybinds_menu_improved(screen, mouse_pos)

        # === BOTÃO VOLTAR MELHORADO ===
        back_btn = Button(30, current_height - 90, 180, 60, "← Voltar", RED)
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
                            set_resolution(idx)

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
    ("fireball", " Lançar Fireball")
]
keybinds_waiting = None


def draw_keybinds_menu_improved(surface, mouse_pos):
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
        btn = Button(current_width // 2 - 50, y, 200, 50, key_name, btn_color, active=is_waiting)
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


def draw_health_bar(surface, x, y, w, h, hp, max_hp):
    pygame.draw.rect(surface, (60, 20, 20), (x, y, w, h), border_radius=3)
    fill_width = int(w * (hp / max_hp))
    pygame.draw.rect(surface, (237, 41, 57), (x, y, fill_width, h), border_radius=3)
    hp_label = FONT.render("HP", True, WHITE)
    surface.blit(hp_label, (x - hp_label.get_width() - 10, y + h // 2 - hp_label.get_height() // 2))
    value_text = FONT.render(f"{hp}/{max_hp}", True, WHITE)
    surface.blit(
        value_text,
        (x + w // 2 - value_text.get_width() // 2, y + h // 2 - value_text.get_height() // 2)
    )

def draw_hud(surface, player):
    # Posição e tamanho relativos à resolução atual
    bar_x = int(current_width * 0.35)   # 3% da largura
    bar_y = int(current_height * 0.9)  # 3% da altura
    bar_w = int(current_width * 0.30)   # 30% da largura
    bar_h = int(current_height * 0.05)  # 5% da altura

    draw_health_bar(surface, bar_x, bar_y, bar_w, bar_h, player.health, player.max_health)


# --- Loop principal do jogo --
def main_game(keybinds):
    player = Player(current_width // 2 - 32, current_height // 2 - 32)
    projectiles = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                # Lançar fireball na direção do mouse
                for spell in player.spells:
                    if event.key in keybinds["fireball"]:
                        mouse_pos = pygame.mouse.get_pos()
                        if spell.cast(player, projectiles, mouse_pos):
                            continue
                if event.key == pygame.K_ESCAPE:
                    return

        # Atualizar jogador
        keys = pygame.key.get_pressed()
        player.update(keys)

        # Atualizar projéteis (remover os que saíram de tela)
        projectiles = [proj for proj in projectiles if proj.update()]

        # Desenhar tudo
        screen.fill(BG_COLOR)
        player.draw(screen)
        for proj in projectiles:
            proj.draw(screen)

        # Interface
        draw_fireball_cooldown(screen, player.spells[0], keybinds, 40, 40, 300, 36)
        draw_hud(screen, player)

        pygame.display.flip()
        clock.tick(FPS)


# --- Iniciar o jogo ---
if __name__ == "__main__":
    main_menu()
