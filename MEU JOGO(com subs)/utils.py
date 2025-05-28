import pygame
from settings import MAGIC_PURPLE, MAGIC_GOLD, current_width


from settings import RESOLUTIONS  # Garante que RESOLUTIONS está acessível

def set_resolution(idx, screen):
    from settings import current_res_index, current_width, current_height
    global current_res_index, current_width, current_height
    current_res_index = idx
    current_width, current_height = RESOLUTIONS[idx]
    screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
    print(f"Resolução alterada para: {current_width}x{current_height}")
    return screen



def scale_image_aspect(img, box_size):
    bx, by = box_size
    ix, iy = img.get_size()
    scale_factor = min(bx / ix, by / iy)
    new_size = (int(ix * scale_factor), int(iy * scale_factor))
    if img.get_bitsize() < 24:
        if img.get_alpha():
            img = img.convert_alpha()
        else:
            img = img.convert()
    return pygame.transform.smoothscale(img, new_size)

def draw_section_separator(surface, y, width_offset=100):
    start_x = width_offset
    end_x = current_width - width_offset
    pygame.draw.line(surface, MAGIC_PURPLE, (start_x, y+10), (end_x, y+10), 3)
    center_x = current_width // 2
    pygame.draw.circle(surface, MAGIC_GOLD, (center_x, y+10), 4)
