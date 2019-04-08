# Dungeons1.0
# author: Charles Kanoy
# date: 2/10/2019

import pygame
import sys
from numpy import *
from threading import Timer
import tkinter as tk
from operator import itemgetter

pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)
image = pygame.image.load("Data/Hero.png")
pygame.display.set_icon(image)
pygame.display.set_caption("Dungeons")


# play background music
pygame.mixer.music.load("Data/labyrinth-of-time.mp3")
pygame.mixer.music.set_volume(.1)
pygame.mixer.music.play(-1)

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

# global game variables
level_count = 1
points = 0
adder = 0
health = 5
playerName = ""


def main():
    global playerName
    # display opening screen
    screen.fill(black)
    text_to_screen(screen=screen, text="Dungeons", x=100, y=250, color=white)
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
                elif event.key == pygame.K_SPACE:
                    get_init()


def get_init():
    # get player initials
    global playerName
    # display opening screen
    screen.fill(black)
    text_to_screen(screen=screen, text="Enter Initials", x=40, y=250, color=white)
    pygame.display.flip()

    while 1:
        # quit if necessary
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.unicode.isalpha():
                    playerName += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    playerName = playerName[:-1]
                elif event.key == pygame.K_SPACE:
                    game_setup()
                # show key input as it happens on screen
                screen.fill(black)
                text_to_screen(screen=screen, text="Enter Initials", x=40, y=250, color=white)
                text_to_screen(screen=screen, text=playerName, x=40, y=350, color=white)
                pygame.display.flip()


# setup game variables
def game_setup():
    # add base-game components
    door = Door(random.randint(0, scale - 1), random.randint(0, scale - 1), black)
    gamer = Player(random.randint(0, scale - 1), random.randint(0, scale - 1), 1, horse_brown)

    # add enemies
    vill = []
    for i in range(adder):
        enemy = Enemy(random.randint(0, scale - 1), random.randint(0, scale - 1), 1, 1, red, adder)
        vill.append(enemy)

    game_play(gamer, vill, door)


def write_score():
    global points
    global playerName

    file = open("Data/scores.txt", "a")
    file.write(playerName + " " + str(points) + "\n")


# run game when player indicates
def game_play(player, enemy, door):
    global adder
    global health

    while health > 0:
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
                elif event.key == pygame.K_SPACE:
                    player.fire(enemy, door)
                else:
                    player.move_player()
                for i in range(adder):
                    enemy[i].move(player)
                    if player.x == enemy[i].x and player.y == enemy[i].y:
                        health -= 1
                        enemy.remove(enemy[i])
                        adder -= 1
                        break

            print_screen(screen, player, door, enemy)
    game_over()


def game_over():
    write_score()
    sort_scores()

    # declare and adjust global variables
    global health
    global points
    global playerName
    playerName = ""
    points = 0
    health = 5

    screen.fill(black)
    text_to_screen(screen, "Game Over", 90, 250, 50, white)
    text_to_screen(screen, "Press space to continue", 100, 400, 20, white)
    pygame.display.flip()

    global level_count
    level_count = 1

    global adder
    adder = 0
    await_key()


# display the level the player is on
def show_level():
    global level_count
    level_count += 1

    # increase adder appropriately
    global adder
    if (level_count % 1) == 0:
        adder = level_count

    screen.fill(black)
    text_to_screen(screen=screen, text="Level " + str(level_count), x=140, y=250, color=white)
    text_to_screen(screen, "Press space to continue", 100, 400, 20, white)
    pygame.display.flip()

    await_key()


def sort_scores():
    with open("Data/scores.txt") as f:
        lines = [line.split(' ') for line in f]
    output = open("Data/scores.txt", "w")

    for line in sorted(lines, key=itemgetter(1), reverse=True):
        output.write(' '.join(line))

    output.close()

# def show_scores():


def await_key():
    while 1:
        # quit if necessary
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    game_setup()


# prints objects on the screen
def print_screen(screen, player, door, enemy):
    global level_count
    global playerName

    screen.fill(green)
    player.draw()
    door.draw()
    for i in range(adder):
        enemy[i].draw()

    # draw player UI on bottom of screen
    outline = pygame.rect.Rect(0, height, width, 200)
    pygame.draw.rect(screen, black, outline)
    text_to_screen(screen, playerName, width / 14, height + 20, 20, white)

    text_to_screen(screen, "Health", width / 2, height + 60, 20, white)
    health_bar = pygame.rect.Rect(width / 2, height + 80, health * 20, 10)
    pygame.draw.rect(screen, green, health_bar)

    text_to_screen(screen, "Level " + str(level_count), width / 14, height + 60, 20, white)

    text_to_screen(screen, "Points " + str(points), width / 14, height + 90, 20, white)
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
        self.face = DOWN


# defines player in game
class Player(GameObject):
    def __init__(self, x, y, vel, color):
        GameObject.__init__(self, x, y, color)
        self.vel = vel

    def draw(self):
        image = pygame.image.load('Data/hero.png')

        # change sprite direction
        if self.face == LEFT:
            image = pygame.transform.rotate(image, 270)
        elif self.face == UP:
            image = pygame.transform.rotate(image, 180)
        elif self.face == RIGHT:
            image = pygame.transform.rotate(image, 90)

        screen.blit(image, self.rect)

    def move_player(self):
        actual = self.vel * square

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            if not (self.x <= 0):
                self.rect.move_ip(-actual, 0)
                self.x -= self.vel
                self.face = LEFT
        elif key[pygame.K_RIGHT]:
            if not (self.x >= scale - self.vel):
                self.rect.move_ip(actual, 0)
                self.x += self.vel
                self.face = RIGHT
        elif key[pygame.K_UP]:
            if not (self.y <= 0):
                self.rect.move_ip(0, -actual)
                self.y -= self.vel
                self.face = UP
        elif key[pygame.K_DOWN]:
            if not (self.y >= scale - self.vel):
                self.rect.move_ip(0, actual)
                self.y += self.vel
                self.face = DOWN

    def fire(self, enemy, door):
        ice_x = self.x
        ice_y = self.y

        if self.face == RIGHT:
            while ice_x < height / square - 1:
                ice_x += 1
                self.draw_ice(ice_x, ice_y, enemy, door)
                if self.check_overlap(enemy, ice_x, ice_y):
                    break
        elif self.face == LEFT:
            while ice_x > 0:
                ice_x -= 1
                self.draw_ice(ice_x, ice_y, enemy, door)
                if self.check_overlap(enemy, ice_x, ice_y):
                    break
        elif self.face == DOWN:
            while ice_y < height / square - 1:
                ice_y += 1
                self.draw_ice(ice_x, ice_y, enemy, door)
                if self.check_overlap(enemy, ice_x, ice_y):
                    break
        elif self.face == UP:
            while ice_y > 0:
                ice_y -= 1
                self.draw_ice(ice_x, ice_y, enemy, door)
                if self.check_overlap(enemy, ice_x, ice_y):
                    break

    def draw_ice(self, ice_x, ice_y, enemy, door):
        # clock for firing
        clock = pygame.time.Clock()

        global screen
        print_screen(screen, self, door, enemy)

        ice_block = pygame.rect.Rect(ice_x * square, ice_y * square, square, square)

        pygame.draw.rect(screen, blue, ice_block)
        pygame.display.flip()

        clock.tick()

    def check_overlap(self, enemy, ice_x, ice_y):
        global adder
        global points
        for i in range(adder):
            if int(enemy[i].x) == ice_x and int(enemy[i].y) == ice_y:
                enemy.remove(enemy[i])
                adder -= 1
                points += 1
                return True


class Door(GameObject):
    def __init__(self, x, y, color):
        GameObject.__init__(self, x, y, color)

    def draw(self):
        pygame.draw.ellipse(screen, self.color, self.rect)


class Enemy(GameObject):
    def __init__(self, x, y, vel, health, color, count):
        GameObject.__init__(self, x, y, color)
        self.vel = vel
        self.health = health
        self.face = DOWN
        self.enemies = [count]

    def __getitem__(self, index):
        return self.enemies[index]

    def __setitem__(self, index, value):
        self.enemies.enemiesId[index] = value

    def draw(self):
        image = pygame.image.load('Data/monster.png')

        # change sprite direction
        if self.face == LEFT:
            image = pygame.transform.rotate(image, 270)
        elif self.face == UP:
            image = pygame.transform.rotate(image, 180)
        elif self.face == RIGHT:
            image = pygame.transform.rotate(image, 90)

        screen.blit(image, self.rect)

    def move(self, player):
        actual = self.vel * square
        x_dist = abs(self.x - player.x)
        y_dist = abs(self.y - player.y)

        if x_dist > y_dist:
            if self.x > player.x:
                self.rect.move_ip(-actual, 0)
                self.x -= self.vel
                self.face = LEFT
            elif self.x < player.x:
                self.rect.move_ip(actual, 0)
                self.x += self.vel
                self.face = RIGHT
        else:
            if self.y > player.y:
                self.rect.move_ip(0, -actual)
                self.y -= self.vel
                self.face = UP
            elif self.y < player.y:
                self.rect.move_ip(0, actual)
                self.y += self.vel
                self.face = DOWN


main()
