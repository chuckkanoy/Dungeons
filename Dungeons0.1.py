# Dungeons0.1
# author: Charles Kanoy
# date: 1/22/2019

import pygame
import sys

pygame.init()

# color palette
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 120, 0)

# directions
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4

# screen
size = height, width = 500, 500
screen = pygame.display.set_mode(size)
scale = 10
square = height / scale


class Level:
    def __init__(self, player):
        self.level = []
        self.new = []

        for i in range(scale):
            for j in range(scale):
                self.new.append(0)
            self.level.append(self.new)
            self.new = []

        self.level[player.y][player.x] = 1

    def update(self, player):
        # refresh the array
        self.level = []
        self.new = []

        for i in range(scale):
            for j in range(scale):
                self.new.append(0)
            self.level.append(self.new)
            self.new = []

        self.level[player.y][player.x] = 1

    def print_level_arr(self):
        for arr in self.level:
            line = ""
            for num in arr:
                line += str(num) + " "
            print(line)
        print('\n')


def main():
    # display opening screen
    screen.fill(black)
    text_to_screen(screen=screen, text="Welcome", x=120, y=175, color=white)
    text_to_screen(screen, "Press space to continue", 100, 250, 20, white)
    pygame.display.flip()

    while 1:
        # quit if necessary
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player, level = game_setup()
                    game_play(player, level)


# setup game variables
def game_setup():
    gamer = Player(0, 0, 1, 1)
    level = Level(gamer)
    level.print_level_arr()

    return gamer, level


# run game when player indicates
def game_play(player, level):
    while player.health > 0:
        # quit if necessary
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # handle keys
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                else:
                    player.move_player()
                    level.update(player)
                    level.print_level_arr()

            # reprints the screen
            screen.fill(red)
            player.draw()
            pygame.display.flip()


# apply text to screen
def text_to_screen(screen, text, x, y, size=50,
                   color=red, font_type='data/slkscr.ttf'):
    text = str(text)
    font = pygame.font.Font(font_type, size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))


# defines player in game
class Player:
    def __init__(self, x, y, vel, health):
        self.x = x
        self.y = y
        self.vel = vel
        self.health = health
        self.rect = pygame.rect.Rect(self.x * square, self.y * square, square, square)

    def draw(self):
        pygame.draw.rect(screen, black, self.rect)

    def move_player(self):
        actual = self.vel * square

        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            if not (self.x <= 0):
                self.rect.move_ip(-actual, 0)
                self.x -= self.vel
        if key[pygame.K_RIGHT]:
            if not (self.x >= scale - self.vel):
                self.rect.move_ip(actual, 0)
                self.x += self.vel
        if key[pygame.K_UP]:
            if not (self.y <= 0):
                self.rect.move_ip(0, -actual)
                self.y -= self.vel
        if key[pygame.K_DOWN]:
            if not (self.y >= scale - self.vel):
                self.rect.move_ip(0, actual)
                self.y += self.vel


main()
