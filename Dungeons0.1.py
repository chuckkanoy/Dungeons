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


class Level:
    def __init__(self, x, y):
        self.rect = pygame.rect.Rect((x, y, scale, scale))

    @staticmethod
    def create_level(character):
        level = []
        new = []
        for i in range(scale):
            for j in range(scale):
                new.append(0)
            level.append(new)
            new = []

        level[character.x][character.y] = 1
        return level

    # draw level
    def draw_level(self, level):
        x, y = width / scale, height / scale

        for i in range(scale):
            for j in range(scale):
                if level[i][j] == 1:
                    pygame.draw.rect(screen, black, self.rect)


def main():
    while 1:
        # quit if necessary
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            player = game_setup()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_play(player)


# setup game variables and opening screen
def game_setup():
    # set up opening screen
    screen.fill(black)
    text_to_screen(screen=screen, text="Welcome", x=120, y=175, color=white)
    text_to_screen(screen, "Press space to continue", 100, 250, 20, white)
    pygame.display.flip()

    gamer = Player(0, 0, width / scale, 1)
    return gamer


# run game when player indicates
def game_play(player):
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
                    player.move()
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


# fits parameters within dimension scale
def fit_to_scale(num):
    result = num * (height / scale)
    return result


class Player:
    def __init__(self, x, y, vel, health):
        self.x = x
        self.y = y
        self.vel = vel
        self.health = health
        self.rect = pygame.rect.Rect(self.x, self.y, height / scale, width / scale)

    def draw(self):
        pygame.draw.rect(screen, black, self.rect)

    def move(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            if not (self.x <= 0):
                self.rect.move_ip(-self.vel, 0)
                self.x -= self.vel
        if key[pygame.K_RIGHT]:
            if not (self.x >= width - self.vel):
                self.rect.move_ip(self.vel, 0)
                self.x += self.vel
        if key[pygame.K_UP]:
            if not (self.y <= 0):
                self.rect.move_ip(0, -self.vel)
                self.y -= self.vel
        if key[pygame.K_DOWN]:
            if not (self.y >= height - self.vel):
                self.rect.move_ip(0, self.vel)
                self.y += self.vel


main()
