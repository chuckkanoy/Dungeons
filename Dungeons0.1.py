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

#screen
size = height, width = 500, 500
screen = pygame.display.set_mode(size)


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
    gamer = Player(50, 50, 1, 1)
    return gamer


# run game when player indicates
def game_play(player):
    screen.fill(red)
    while player.health > 0:
        # quit if necessary
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            pygame.display.flip()


# apply text to screen
def text_to_screen(screen, text, x, y, size=50,
                   color=red, font_type='data/slkscr.ttf'):
    text = str(text)
    font = pygame.font.Font(font_type, size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))


class Player:
    def __init__(self, x, y, vel, health):
        self.x = x
        self.y = y
        self.vel = vel
        self.health = health


main()
