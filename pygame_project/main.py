import pygame
import os


FPS = 50
size = WIDTH, HEIGHT = 510, 390
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
    ball, output_x, output_y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('grass', x, y)
            elif level[y][x] == 'x':
                Tile('gates', x, y)
            elif level[y][x] == '@':
                Tile('grass', x, y)
                ball = Ball(x, y)
                output_x, output_y = x, y
    return ball, output_x, output_y


class Field:
    def __init__(self, width, height, x, y, x0=0, y0=30, cell_size=30, color=(255, 255, 255)):
        self.field = [[0] * width for _ in range(height)]
        self.width, self.height = width, height
        self.left = x0
        self.top = y0
        self.cell_size = cell_size
        self.color = color

    def set_view(self, x0, y0, cell_size, color=(255, 255, 255)):
        self.left = x0
        self.top = y0
        self.cell_size = cell_size
        self.color = color

    def render(self, screen):
        for i in range(self.width):
            for j in range(self.height):
                if not self.field[j][i]:
                    color = (255, 255, 255)
                else:
                    color = (255, 0, 0)
                pygame.draw.rect(screen, color, ((i * self.cell_size + self.left, j * self.cell_size + self.top),
                                                      (self.cell_size, self.cell_size)), 1)

    def get_cell(self, x, y):
        if self.in_field(x, y):
            x -= self.left
            x = x // self.cell_size
            y -= self.top
            y = y // self.cell_size
            return x, y
        return None

    def in_field(self, x, y):
        if x < self.left or y < self.top or x > self.left + self.width * self.cell_size or \
                                y > self.top + self.height * self.cell_size:
            return False
        return True

    def on_click(self, mousepos):
        i, j = self.get_cell(*mousepos)
        self.field[j][i] = 1


class Tile(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__(tiles, all_sprites)
        self.image = tile_images[type]
        self.rect = self.image.get_rect().move(
            tile_width * x, tile_height * y)


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(ball_group, all_sprites)
        self.image = ball_image
        self.rect = self.image.get_rect().move(
            tile_width * x, tile_height * y)
        self.pos = x, y

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * x + 1.5, tile_height * y + 1.5)


tile_width = tile_height = 30
tile_images = {
    'grass': load_image('grass.png', -1),
    'gates': load_image('gates.png', -1)
}
ball_image = load_image('ball.png', -1)
all_sprites = pygame.sprite.Group()
tiles = pygame.sprite.Group()
ball_group = pygame.sprite.Group()


def check(ball, end_pos):
    x_0, y_0 = ball.pos
    x, y = end_pos
    sx = abs(x - x_0)
    sy = abs(y - y_0)
    return sx <= 3 and sy <= 3


if __name__ == '__main__':
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    running = True
    level_map = load_level('field.txt')
    ball, ball_x, ball_y = generate_level(load_level('field.txt'))
    field = Field(11, 11, ball_x, ball_y)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                end_pos = field.get_cell(*event.pos)
                movement_avaliable = check(ball, end_pos)
                if movement_avaliable:
                    x, y = end_pos
                    ball.move(x, y + 1)
        screen.fill((0, 0, 0))
        tiles.draw(screen)
        ball_group.draw(screen)
        clock.tick(FPS)
        field.render(screen)
        pygame.display.flip()
    pygame.quit()
