import pygame
import os
import sys
import random

FPS = 50
SIZE = WIDTH, HEIGHT = 510, 390
GRAVITY = 0.5
TILE_WIDTH = TILE_HEIGHT = 30

SCREEN = pygame.display.set_mode(SIZE)
CLOCK = pygame.time.Clock()
SCREEN_RECT = (0, 0, WIDTH, HEIGHT)
pygame.init()


def terminate():
    pygame.quit()
    sys.exit()


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
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    ball, output_x, output_y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('grass', x, y)
            elif level[y][x] == 'x':
                Tile('upper_gates', x, y)
            elif level[y][x] == 'o':
                Tile('lower_gates', x, y)
            elif level[y][x] == '@':
                Tile('grass', x, y)
                ball = Ball(x, y)
                output_x, output_y = x, y
    return ball, output_x, output_y


def start_screen():
    pygame.display.set_caption('Футбольчик. Главное меню')
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    SCREEN.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 302 <= event.pos[0] <= 421 and 287 <= event.pos[1] <= 325:
                    return
        pygame.display.flip()
        CLOCK.tick(FPS)


def rules_screen():
    pygame.display.set_caption('Футбольчик. Правила')
    rules_text = ['Правила (Нажмите на любую клавишу, чтобы вернуться в главное меню):',
                  'Игроки по очереди "пинают" мяч. Номер игрока, который делает ход,',
                  'можно определить по надписи в правой части экрана.',
                  'Цель игры - довести мяч до ворот противника и забить гол.',
                  'Ворота игрока 1 находятся вверху, игрока 2 - внизу.',
                  'Мяч может ходить вокруг себя на одну клетку.',
                  'Игрок может сделать три перемещения за один ход.',
                  'Перемещение определяется нажатием ЛКМ на клетку поля,',
                  'ход - нажатием клавиши ENTER. Чтобы отменить перемещения,',
                  'нажмите на ПКМ.',
                  'Когда игрок сделал ход, все его перемещения помечаются крестиками -',
                  'это значит, что на эти клетки ходить больше нельзя.',
                  'Если мяч попал в "ловушку" из таких крестиков, игрокам необходимо',
                  'перезапустить раунд.',
                  'Приятной игры!)']
    font = pygame.font.Font(None, 20)
    text_coord = 5
    SCREEN.fill((0, 0, 0))
    for line in rules_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        SCREEN.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        CLOCK.tick(FPS)


def whose_turn(is_player_1):
    font = pygame.font.Font(None, 30)
    if is_player_1:
        turn = font.render('Ход игрока 1', True, pygame.Color('blue'))
    else:
        turn = font.render('Ход игрока 2', True, pygame.Color('green'))
    turn_x, turn_y = TILE_WIDTH * 12, TILE_WIDTH * 7
    SCREEN.blit(turn, (turn_x, turn_y))


def create_firework(position):
    star_count = 40
    numbers = range(-5, 6)
    for _ in range(star_count):
        Star(position, random.choice(numbers), random.choice(numbers))


def check_movement(x_0, y_0, x, y):
    return x_0 - 1 <= x <= x_0 + 1 and y_0 - 1 <= y <= y_0 + 1


class Star(pygame.sprite.Sprite):
    star_images = [
        load_image('red.png', -1),
        load_image('orange.png', -1),
        load_image('yellow.png', -1),
        load_image('green.png', -1),
        load_image('blue.png', -1),
        load_image('purple.png', -1)
    ]
    fire = []
    for scale in (10, 12, 14, 16, 18, 20):
        random_star = random.choice(star_images)
        fire.append(pygame.transform.scale(random_star, (scale, scale)))
        star_images.remove(random_star)

    def __init__(self, pos, dx, dy):
        super().__init__(star_group, all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(SCREEN_RECT):
            self.kill()


class Field:
    def __init__(self, width, height, x, y, x0=0, y0=30, cell_size=30, color=(255, 255, 255)):
        self.field = [[0] * width for _ in range(height)]
        self.width, self.height = width, height
        self.left = x0
        self.top = y0
        self.cell_size = cell_size
        self.color = color
        self.field[x][y] = 1

    def set_view(self, x0, y0, cell_size, color=(255, 255, 255)):
        self.left = x0
        self.top = y0
        self.cell_size = cell_size
        self.color = color

    def render(self, screen):
        for i in range(self.width):
            for j in range(self.height):
                color = (255, 255, 255)
                if self.field[j][i]:
                    Cross(i, j + 1)
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

    def get_x(self, x):
        x -= self.left
        x = x // self.cell_size
        return x

    def on_click(self, coord):
        i, j = coord
        if i < 11 and j < 11:
            self.field[j][i] = 1

    def clear(self):
        for i in range(self.width):
            for j in range(self.height):
                self.field[j][i] = 0
        for sprite in holoball_group:
            holoball_group.remove(sprite)
        for sprite in cross_group:
            cross_group.remove(sprite)


class Tile(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__(tiles, all_sprites)
        self.image = tile_images[type]
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * x, TILE_HEIGHT * y)


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(ball_group, all_sprites)
        self.default_pos = self.default_x, self.default_y = x, y
        self.image = ball_image
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * x + 1.5, TILE_HEIGHT * y + 1.5)
        self.pos = x, y

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(TILE_WIDTH * x + 1.5, TILE_HEIGHT * y + 1.5)


class HoloBall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(holoball_group, all_sprites)
        self.image = holoball_image
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * x + 1.5, TILE_HEIGHT * y + 1.5)
        self.pos = x, y

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(TILE_WIDTH * x + 1.5, TILE_HEIGHT * y + 1.5)


class Score(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(tiles, all_sprites)
        self.image = score_image
        self.rect = self.image.get_rect().move(TILE_WIDTH * x, TILE_HEIGHT * y)

    def update(self, player_1, player_2):
        font = pygame.font.Font(None, 60)
        score_1 = font.render(str(player_1), True, pygame.Color('blue'))
        score_2 = font.render(str(player_2), True, pygame.Color('green'))
        x_1, y_1 = self.rect.x + 18, self.rect.y + 13
        x_2, y_2 = self.rect.x + 78, self.rect.y + 13
        SCREEN.blit(score_1, (x_1, y_1))
        SCREEN.blit(score_2, (x_2, y_2))


class Cross(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(cross_group, all_sprites)
        self.image = tile_images['cross']
        self.x = x
        self.y = y
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * x + 1.5, TILE_HEIGHT * y + 1.5)


class Button(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__(button_group, all_sprites)
        self.image = button_images[type]
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * x, TILE_HEIGHT * y)
        self.type = type

    def get_event(self, event):
        if self.rect.collidepoint(event.pos):
            return self.type
        return ''


tile_images = {
    'grass': load_image('grass.png', -1),
    'upper_gates': load_image('upper_gates.png', -1),
    'lower_gates': load_image('lower_gates.png', -1),
    'cross': load_image('cross.png', -1)
}
button_images = {
    'main_menu': load_image('to_main_menu.png', -1),
    'restart': load_image('restart.png', -1),
    'rules': load_image('rules.png', -1)
}
ball_image = load_image('ball.png', -1)
holoball_image = load_image('holoball.png', -1)
score_image = load_image('score.png', -1)
all_sprites = pygame.sprite.Group()
tiles = pygame.sprite.Group()
ball_group = pygame.sprite.Group()
holoball_group = pygame.sprite.Group()
button_group = pygame.sprite.Group()
cross_group = pygame.sprite.Group()
star_group = pygame.sprite.Group()


if __name__ == '__main__':
    start_screen()
    level_map = load_level('field.txt')
    ball, ball_x, ball_y = generate_level(level_map)
    pygame.display.set_caption('Футбольчик')
    field = Field(11, 11, ball_x, ball_y - 1)
    to_main_menu_btn = Button('main_menu', 12, 1)
    restart_btn = Button('restart', 12, 9)
    rules_btn = Button('rules', 12, 12)
    score = Score(12, 4)
    h_ball_x, h_ball_y = ball.default_pos
    ballnow_x, ballnow_y = ball.default_pos
    count = 0
    coords = [(5, 6)]
    player_1, player_2 = 0, 0
    running = True
    player_1_turn = True
    moving = True
    goal_1 = False
    goal_2 = False
    goal_confirmed = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not field.in_field(*event.pos):
                        x, y = event.pos
                        upper_gates = 91 <= x <= 240 and 0 <= y <= 30
                        lower_gates = 91 <= x <= 240 and 361 <= y <= 390
                        movement_available = (check_movement(h_ball_x, h_ball_y, x // TILE_WIDTH,
                                                             y // TILE_HEIGHT) and count < 3)
                        if upper_gates and count < 3:
                            if movement_available:
                                moving = True
                                x = field.get_x(x)
                                HoloBall(x, 0)
                                h_ball_x, h_ball_y = x, 0
                                coords.append((x, 0))
                                count = 4
                                goal_1 = True
                        elif lower_gates and count < 3:
                            if movement_available:
                                moving = True
                                x = field.get_x(x)
                                HoloBall(x, 12)
                                h_ball_x, h_ball_y = x, 12
                                coords.append((x, 12))
                                count = 4
                                goal_2 = True
                        else:
                            for btn in button_group:
                                type = btn.get_event(event)
                                if type:
                                    break
                            if type:
                                if type == 'main_menu':
                                    h_ball_x, h_ball_y = ball.default_pos
                                    ballnow_x, ballnow_y = ball.default_pos
                                    count = 0
                                    coords = [(5, 6)]
                                    player_1, player_2 = 0, 0
                                    player_1_turn = True
                                    moving = True
                                    goal_1 = False
                                    goal_2 = False
                                    goal_confirmed = False
                                    start_screen()
                                elif type == 'restart':
                                    field.clear()
                                    ball.move(ball.default_x, ball.default_y)
                                    coords = [(5, 6)]
                                    count = 0
                                    h_ball_x, h_ball_y = ball.default_pos
                                    ballnow_x, ballnow_y = ball.default_pos
                                    field.field[ball_x][ball_y - 1] = 1
                                    player_1_turn = True
                                    goal_1, goal_2, goal_confirmed = False, False, False
                                elif type == 'rules':
                                    rules_screen()
                    else:
                        x, y = field.get_cell(*event.pos)
                        if (x, y + 1) not in coords:
                            moving = True
                            movement_available = check_movement(h_ball_x, h_ball_y, x, y + 1) and count < 3
                            if movement_available:
                                HoloBall(x, y + 1)
                                h_ball_x, h_ball_y = x, y + 1
                                coords.append((x, y + 1))
                                count += 1
                elif event.button == 3:
                    h_ball_x, h_ball_y = ball.pos
                    for sprite in holoball_group:
                        holoball_group.remove(sprite)
                    if not goal_1 and not goal_2:
                        for i in range(count):
                            del coords[-1]
                    else:
                        for i in range(count - 1):
                            del coords[-1]
                        goal_1, goal_2 = False, False
                    count = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    x1, y1 = coords[-1]
                    if ballnow_x != x1 or ballnow_y != y1:
                        moving = False
                        if player_1_turn:
                            player_1_turn = False
                        else:
                            player_1_turn = True
                        count = 0
                    if goal_1 or goal_2:
                        create_firework((h_ball_x * TILE_WIDTH + 15, h_ball_y * TILE_HEIGHT + 15))
                        goal_confirmed = True
        star_group.update()
        SCREEN.fill((0, 0, 0))
        tiles.draw(SCREEN)
        button_group.draw(SCREEN)
        if moving:
            holoball_group.draw(SCREEN)
        else:
            ballnow_x, ballnow_y = coords[-1]
            ball.move(ballnow_x, ballnow_y)
            for coord in coords:
                if 0 <= coord[0] <= field.width and 0 <= coord[1] - 1 <= field.height:
                    field.on_click((coord[0], coord[1] - 1))
            for sprite in holoball_group:
                holoball_group.remove(sprite)
        if goal_confirmed:
            if goal_1:
                player_2 += 1
            elif goal_2:
                player_1 += 1
            field.clear()
            ball.move(ball.default_x, ball.default_y)
            coords = [(5, 6)]
            count = 0
            h_ball_x, h_ball_y = ball.default_pos
            ballnow_x, ballnow_y = ball.default_pos
            field.field[ball_x][ball_y - 1] = 1
            player_1_turn = True
            goal_1, goal_2, goal_confirmed = False, False, False
        whose_turn(player_1_turn)
        cross_group.draw(SCREEN)
        ball_group.draw(SCREEN)
        score.update(player_1, player_2)
        star_group.draw(SCREEN)
        CLOCK.tick(FPS)
        field.render(SCREEN)
        pygame.display.flip()
    pygame.quit()
