import pygame
import sys
import random
import os

# константы
TILE_SIZE = 50
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 10, 8  # размеры в клетках
size = SCREEN_WIDTH, SCREEN_HEIGHT = WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Перемещение Дарьи')


# загрузка изображ
def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname).convert()
    image.set_colorkey(WHITE)
    return image


sprite_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()

# хранилище спрайтов
tile_image = {'wall': load_image('box.png'),
              'empty': load_image('grass.png'),
              'portal': load_image('pl.png'),
              'kar': load_image('kar.jpeg'),
              'dora': load_image('dora.png'),
              'tree': load_image('tr.png'),
              'deb': load_image('deb.png')}


class ScreenFrame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = (0, 0, 500, 500)


class SpriteGroup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for inet in self:
            inet.get_event(event)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_image[tile_type]
        self.rect = self.image.get_rect().move(TILE_SIZE * pos_x, TILE_SIZE * pos_y)


class Player(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15,
                                               tile_height * self.pos[1] + 5)


# стоп работа
def terminate():
    pygame.quit()
    sys.exit()


# начало
def start_screen():
    intro_text = ["Перемещение Dorы", '',
                  "Герой двигается",
                  "Карта на месте"]
    fon = pygame.transform.scale(load_image('wtf1.jpeg'), size)
    screen.blit((fon), (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
                level[y][x] = '.'
            elif level[y][x] == '!':
                Tile('portal', x, y)
    return new_player, x, y


def move(hero, movement):
    x, y = hero.pos
    if movement == 'up':
        if y > 0 and level_map[y - 1][x] == '.':
            hero.move(x, y - 1)
    elif movement == 'down':
        if y < max_y - 1 and level_map[y + 1][x] == '.':
            hero.move(x, y + 1)
    elif movement == 'left':
        if x > 0 and level_map[y][x - 1] == '.':
            hero.move(x - 1, y)
    elif movement == 'right':
        if x < max_x - 1 and level_map[y][x + 1] == '.':
            hero.move(x + 1, y)


# цвета
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# карты уровней
LEVELS = [
    [
        "##########",
        "#P   C  X#",
        "#  ###   #",
        "#  #     #",
        "#  ###   #",
        "#    C   #",
        "#      ###",
        "##########"
    ],
    [
        "##########",
        "#P  C X  #",
        "#  ##### #",
        "#  #  C  #",
        "#  #  #  #",
        "#  ###   #",
        "# C    E #",
        "##########"
    ],
    [
        "##########",
        "#P    EX #",
        "#  ###C ##",
        "#  #     #",
        "#  ### C #",
        "#  #     #",
        "#      ###",
        "##########"
    ],
    [
        "##########",
        "#P C   X #",
        "# ####   #",
        "# #  C   #",
        "# #  ### #",
        "#    C   #",
        "#      ###",
        "##########"
    ]
]


class Game:
    def __init__(self):
        pygame.init()
        start_screen()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.level_index = 0
        self.score = 0
        self.enemies = []
        self.bonuses = []
        self.sprites = pygame.sprite.Group()
        self.load_level()

    def load_level(self):
        self.level = LEVELS[self.level_index]
        self.player_pos = None
        self.coins = []
        self.enemies = []
        self.bonuses = []
        self.sprites.empty()

        for y, row in enumerate(self.level):
            for x, cell in enumerate(row):
                if cell == 'P':
                    self.player_pos = [x, y]
                    self.sprites.add(Tile('empty', x, y))
                    self.player_sprite = Tile('dora', x, y)
                elif cell == 'C':
                    self.coins.append((x, y))
                    self.sprites.add(Tile('empty', x, y))
                    self.sprites.add(Tile('kar', x, y))
                elif cell == 'E':
                    self.enemies.append([x, y])
                    self.sprites.add(Tile('deb', x, y))
                elif cell == 'B':
                    self.bonuses.append((x, y))
                elif cell == ' ':
                    self.sprites.add(Tile('empty', x, y))
                elif cell == 'X':
                    self.sprites.add(Tile('portal', x, y))
                elif cell == '#':
                    self.sprites.add(Tile('tree', x, y))

    def draw_level(self):
        self.screen.fill(WHITE)
        for y, row in enumerate(self.level):
            for x, cell in enumerate(row):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if cell == "#":
                    pygame.draw.rect(self.screen, BLACK, rect)
                elif cell == ' ':
                    Tile('empty', x, y)
                elif cell == "X":
                    pygame.draw.rect(self.screen, BLUE, rect)
                elif (x, y) in self.coins:
                    Tile('kar', x, y)
                elif (x, y) in self.enemies:
                    pygame.draw.rect(self.screen, RED, rect)
                elif (x, y) in self.bonuses:
                    pygame.draw.circle(self.screen, ORANGE, rect.center, TILE_SIZE // 4)
        self.sprites.draw(self.screen)
        if self.player_sprite:
            self.screen.blit(self.player_sprite.image, self.player_sprite.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(f"Очки: {self.score}", True, PURPLE)
        self.screen.blit(text, (10, 10))

    def move_player(self, dx, dy):
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        if self.level[new_y][new_x] != "#":
            self.player_pos = [new_x, new_y]
            self.player_sprite.rect.topleft = (new_x * TILE_SIZE, new_y * TILE_SIZE)
            if self.level[new_y][new_x] == 'E':
                print(f'Вы проиграли( Ваши очки: {self.score}')
                terminate()
            if self.level[new_y][new_x] == "X":
                self.level_index += 1
                if self.level_index < len(LEVELS):
                    self.load_level()
                else:
                    print(f"ОГО! Наконец все уровни пройдены. Итоговые очки: {self.score}")
                    pygame.quit()
                    sys.exit()
            if (new_x, new_y) in self.coins:
                self.coins.remove((new_x, new_y))
                self.score += 10
                self.sprites.add(Tile('empty', new_x, new_y))
            if (new_x, new_y) in self.bonuses:
                self.bonuses.remove((new_x, new_y))
                self.score += 50

            if (new_x, new_y) in self.enemies:
                print("Вы проиграли!")
                pygame.quit()
                sys.exit()

    def run(self):
        # игровой цикл
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.move_player(0, -1)
                    elif event.key == pygame.K_DOWN:
                        self.move_player(0, 1)
                    elif event.key == pygame.K_LEFT:
                        self.move_player(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move_player(1, 0)

            self.draw_level()
            pygame.display.flip()
            self.clock.tick(10)


# начало
if __name__ == "__main__":
    Game().run()
