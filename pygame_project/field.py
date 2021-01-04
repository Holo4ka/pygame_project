import pygame
import os


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


class Field:
    def __init__(self, width, height, left=10, top=50, cell_size=30, color=(255, 255, 255)):
        self.field = [[0] * width for _ in range(height)]
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.color = color

    def set_view(self, left, top, cell_size, color):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.color = color

    def render(self, screen):
        for i in range(self.width):
            for j in range(self.height):
                if self.field[j][i]:
                    color = (0, 0, 255)
                else:
                    color = (0, 0, 0)
                pygame.draw.rect(screen, color, ((self.left + i * self.cell_size,
                                                  self.top + j * self.cell_size),
                                                 (self.cell_size, self.cell_size)))
                pygame.draw.rect(screen, self.color, ((self.left + i * self.cell_size,
                                                       self.top + j * self.cell_size),
                                                      (self.cell_size, self.cell_size)), 1)
                if ((self.width - 5) // 2 - 1) < i < (self.width - ((self.width - 5) // 2)) and (
                        j == 0 or j == self.height - 1):
                    if j == 0:
                        pygame.draw.rect(screen, self.color, ((self.left + i * self.cell_size,
                                                               self.top - self.cell_size),
                                                              (self.cell_size, self.cell_size)), 1)
                    elif j == self.height - 1:
                        pygame.draw.rect(screen, self.color, ((self.left + i * self.cell_size,
                                                               self.top + self.cell_size * self.height),
                                                              (self.cell_size, self.cell_size)), 1)

    def on_click(self, mousepos):
        if self.get_cell(*mousepos):
            i, j = self.get_cell(*mousepos)
            self.field[j][i] = 1

    def get_cell(self, x, y):
        if self.in_field(x, y):
            x -= self.left
            x = x // self.cell_size
            y -= self.top
            y = y // self.cell_size
            return x, y
        return None

    def in_field(self, x, y):
        return self.left < x < self.left + self.width * self.cell_size and \
               self.top < y < self.top + self.height * self.cell_size


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    field = Field(11, 11)
    running = True
    size = (500, 500)
    screen = pygame.display.set_mode(size)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for row in field.field:
                    print(row)
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = field.get_cell(*event.pos)
        screen.fill((0, 0, 0))
        field.render(screen)
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()
