import pygame
import os


pygame.init()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as mes:
        print("Can't load image: ", mes)
        raise SystemExit(mes)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    ball, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('grass', x, y)
            elif level[y][x] == 'x':
                Tile('gates', x, y)
            elif level[y][x] == '@':
                Tile('grass', x, y)
                ball = Ball(x, y)
    return ball


class Field:
    def __init__(self):
        self.map = load_level('field.txt')
        self.left = 0
        self.top = 0
        self.cell_size = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__(tiles, all_sprites)
        self.image = tile_images[type]
        self.rect = self.image.get_rect().move(
            tile_width * x, tile_height * y)


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(ball_group, all_sprites)


tile_width = tile_height = 50
tile_images = {
    'grass': load_image('grass.png'),
    'gates': load_image('gates.png')
}
ball_image = load_image('ball.png')
all_sprites = pygame.sprite.Group()
tiles = pygame.sprite.Group()
ball_group = pygame.sprite.Group()