# Dungeons0.1
# author: Charles Kanoy
# date: 12/27/2018

import pygame
import sys


pygame.init()

def main():

    size = width, height = 400, 600
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    while 1:
        # quit if necessary
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(black)
        text_to_screen(screen=screen, text="Welcome", x=40, y=175, color=(0, 0, 255))
        text_to_screen(screen, "Press space to continue", 40, 250, 20, (0, 0, 255))
        pygame.display.flip()


# apply text to screen
def text_to_screen(screen, text, x, y, size=50,
                   color=(200, 000, 000), font_type='data/slkscr.ttf'):

        text = str(text)
        font = pygame.font.Font(font_type, size)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))

main()