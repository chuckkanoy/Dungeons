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


# create the layout for a level
def level_creation():
    level = []
    new = []
    for i in range(scale):
        for j in range(scale):
            new.append(0)
        level.append(new)
        new = []
    return level


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
    screen.fill(black)
    text_to_screen(screen=screen, text="Welcome", x=120, y=175, color=white)
    text_to_screen(screen, "Press space to continue", 100, 250, 20, white)
    pygame.display.flip()
    gamer = Player(0, 0, 1, 1)
    return gamer


# run game when player indicates
def game_play(player):
    while player.health > 0:
        # quit if necessary
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_DOWN:
                    player.move(DOWN)
                elif event.key == pygame.K_LEFT:
                    player.move(LEFT)
                elif event.key == pygame.K_UP:
                    player.move(UP)
                elif event.key == pygame.K_RIGHT:
                    player.move(RIGHT)

            screen.fill(red)
            player.draw(player.x, player.y)
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

    def draw(self, x, y):
        pygame.draw.rect(screen, black,
                         (fit_to_scale(x), fit_to_scale(y),
                          fit_to_scale(x + 1), fit_to_scale(y + 1)), 0)

    def move(self, direction):
        if direction == UP:
            self.y -= self.vel
        elif direction == RIGHT:
            self.x += self.vel
        elif direction == DOWN:
            self.y += self.vel
        elif direction == LEFT:
            self.x -= self.vel


main()
