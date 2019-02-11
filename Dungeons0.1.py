# Dungeons1.0
# author: Charles Kanoy
# date: 2/10/2019

import pygame
from numpy import *

pygame.init()

# color palette
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (75, 114, 72)
horse_brown = (68, 58, 50)

# directions
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4

# screen
size = height, width = 500, 700
screen = pygame.display.set_mode(size)
scale = 10
square = height / scale
level_count = 1


def main():
    # display opening screen
    screen.fill(black)
    text_to_screen(screen=screen, text="Welcome", x=120, y=250, color=white)
    text_to_screen(screen, "Press space to continue", 100, 400, 20, white)
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
                    game_setup()


# setup game variables
def game_setup():
    gamer = Player(random.randint(0, scale - 1), random.randint(0, scale - 1), 1, 5, horse_brown)
    door = Door(random.randint(0, scale - 1), random.randint(0, scale - 1), black)
    vill = Enemy(random.randint(0, scale - 1), random.randint(0, scale - 1), 2, 1, red)

    global level_count
    level_count += 1

    game_play(gamer, vill, door)


# run game when player indicates
def game_play(player, enemy, door):
    while player.health > 0:
        # quit if necessary
        for event in pygame.event.get():

            # change levels if landed on door
            if player.x == door.x and player.y == door.y:
                show_level()
                game_setup()

            if event.type == pygame.QUIT:
                sys.exit()

            # handle keys
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                else:
                    player.move_player()
                    enemy.move(player)

                if player.x == enemy.x and player.y == enemy.y:
                    player.health -= 1

            print_screen(screen, player, door, enemy)

    game_over()


def game_over():
    screen.fill(black)
    text_to_screen(screen, "Game Over", 90, 250, 50, white)
    text_to_screen(screen, "Press space to continue", 100, 400, 20, white)
    pygame.display.flip()

    global level_count
    level_count = 1

    await_key()


# display the level the player is on
def show_level():
    global level_count
    screen.fill(black)
    text_to_screen(screen=screen, text="Level " + str(level_count), x=140, y=250, color=white)
    text_to_screen(screen, "Press space to continue", 100, 400, 20, white)
    pygame.display.flip()

    await_key()


def await_key():
    while 1:
        # quit if necessary
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

            # handle the next move
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_setup()


# prints objects on the screen
def print_screen(screen, player, door, enemy):
    screen.fill(green)
    player.draw()
    door.draw()
    enemy.draw()

    # draw player UI on bottom of screen
    outline = pygame.rect.Rect(0, height, width, 200)
    pygame.draw.rect(screen, black, outline)

    text_to_screen(screen, "Health", width / 2, height + 60, 20, green)
    health_bar = pygame.rect.Rect(width / 2, height + 80, player.health * 20, 10)
    pygame.draw.rect(screen, green, health_bar)
    pygame.display.flip()


# apply text to screen
def text_to_screen(screen, text, x, y, size=50,
                   color=red, font_type='data/slkscr.ttf'):
    text = str(text)
    font = pygame.font.Font(font_type, size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))


class GameObject:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.rect = pygame.rect.Rect(self.x * square, self.y * square, square, square)


# defines player in game
class Player(GameObject):
    def __init__(self, x, y, vel, health, color):
        GameObject.__init__(self, x, y, color)
        self.vel = vel
        self.health = health

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

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


class Door(GameObject):
    def __init__(self, x, y, color):
        GameObject.__init__(self, x, y, color)

    def draw(self):
        pygame.draw.ellipse(screen, self.color, self.rect)


class Enemy(GameObject):
    def __init__(self, x, y, vel, health, color):
        GameObject.__init__(self, x, y, color)
        self.vel = vel
        self.health = health

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self, player):
        actual = self.vel * square
        x_dist = abs(self.x - player.x)
        y_dist = abs(self.y - player.y)

        if x_dist > y_dist:
            if self.x > player.x :
                self.rect.move_ip(-actual, 0)
                self.x -= self.vel
            elif self.x < player.x:
                self.rect.move_ip(actual, 0)
                self.x += self.vel
        else:
            if self.y > player.y:
                self.rect.move_ip(0, -actual)
                self.y -= self.vel
            elif self.y < player.y:
                self.rect.move_ip(0, actual)
                self.y += self.vel

main()
