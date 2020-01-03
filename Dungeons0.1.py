# Dungeons1.0
# author: Charles Kanoy
# date: 2/10/2019

import pygame
import sys
from numpy import *
import threading
import tkinter as tk
from operator import itemgetter
# from iteration_utilities import chained
from functools import partial

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
num_barriers = 0
level_count = 1
points = 0
adder = 1
health = 5
playerName = ""
board = [[0 for x in range(10)] for y in range(10)]
num_possible_power_ups = 2


# initialize array board
def board_init():
    for i in range(10):
        for j in range(10):
            board[i][j] = 0


# display array board
def print_board():
    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                     for row in board]))
    print('\n')


# main method called to begin game actions
def main():
    # show_scores()  # use temporarily for scoreboard modification
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
                    # move on to next step if continue occurs
                    get_init()


# initialize game space and playerName
def get_init():
    # get player initials
    global playerName

    # allow player to only enter 3 characters for initials
    while len(playerName) != 3:
        # quit if necessary
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.unicode.isalpha():
                    playerName += event.unicode.upper()
                elif event.key == pygame.K_BACKSPACE:
                    playerName = playerName[:-1]
                # show key input as it happens on screen
                screen.fill(black)
                text_to_screen(screen=screen, text="Enter Initials", x=40, y=250, color=white)
                text_to_screen(screen=screen, text=playerName, x=40, y=350, color=white)
                pygame.display.flip()

    # setup game based on input
    game_setup()


# setup game variables
def game_setup():
    global level_count
    # add player component
    gamer = Player(random.randint(0, scale - 1), random.randint(0, scale - 1), 1, horse_brown)

    door = Door(random.randint(0, scale - 1), random.randint(0, scale - 1), black)
    while gamer.x == door.x and gamer.y == door.y:
        door = Door(random.randint(0, scale - 1), random.randint(0, scale - 1), black)
    # add power up depending on random
    appears = random.randint(0, 100)
    if 0 <= appears <= 50:
        powerup = []
    else:
        choice = random.randint(0, num_possible_power_ups)
        if choice == 0:
            powerup = [Health()]
        else:
            powerup = [Treasure()]

    # add enemies
    vill = []
    if level_count != 1:
        for i in range(adder):
            enemy = Enemy(random.randint(0, scale - 1), random.randint(0, scale - 1), 1, 1, red, adder)
            vill.append(enemy)

    barrier = Barrier()
    # for j in range(num_barriers):
    if level_count == 1:
        for i in range(adder):
            while (gamer.x == barrier.x and gamer.y == barrier.y) or (door.x == barrier.x and door.y == barrier.y):
                barrier = Barrier()
    else:
        for i in range(adder):
            while (vill[i].x == barrier.x and vill[i].y == barrier.y) or \
                    (gamer.x == barrier.x and gamer.y == barrier.y) or (door.x == barrier.x and door.y == barrier.y):
                barrier = Barrier()

    game_play(gamer, vill, door, powerup, barrier)


# run game when player indicates
def game_play(player, enemy, door, powerup, barrier):
    # global variables
    global num_barriers

    # print_board() used when displaying array being saved
    while health > 0:
        # handle every event
        for event in pygame.event.get():
            # change levels if landed on door
            if player.x == door.x and player.y == door.y:
                show_level()
                game_setup()

            # quit if necessary
            elif event.type == pygame.QUIT:
                sys.exit()

            # handle keys
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    player.fire(enemy, door)
                else:
                    # for i in range(num_barriers):
                    player.move_player(barrier)
                    if len(powerup) != 0:
                        if powerup[0].check_collision(player):
                            powerup[0].boost(player)
                            powerup.remove(powerup[0])
                    # for i in range(num_barriers):
                    run_enemy(enemy, player, barrier)
                print_screen(screen, player, door, enemy, powerup, barrier)
                # board_init() used when displaying array being saved
    game_over()


# handle timed enemy
def run_enemy(enemy, player, barrier):
    # global variables
    global health
    global level_count

    if level_count != 1:
        for i in range(len(enemy)):
            enemy[i].move(player, barrier)
            if player.x == enemy[i].x and player.y == enemy[i].y:
                health -= 1
                enemy.remove(enemy[i])
                break


# handle what happens upon player death
def game_over():
    # display sorted scores
    sort_scores()
    write_score()

    # declare and adjust global variables
    global health
    global points
    global playerName
    playerName = ""
    points = 0
    health = 5

    # display game over screen
    screen.fill(black)
    text_to_screen(screen, "Game Over", 90, 250, 50, white)
    text_to_screen(screen, "Press space to continue", 100, 400, 20, white)
    pygame.display.flip()

    global level_count
    level_count = 1

    global adder
    adder = 0
    while 1:
        # quit if necessary
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    show_scores()


# display the level the player is on
def show_level():
    global level_count
    level_count += 1

    # increase adder appropriately
    global adder
    if (level_count % 5) == 0:
        adder += 1

    screen.fill(black)
    text_to_screen(screen=screen, text="Level " + str(level_count), x=140, y=250, color=white)
    text_to_screen(screen, "Press space to continue", 100, 400, 20, white)
    pygame.display.flip()

    await_continue()


# sort scores in text document
def sort_scores():
    # declare local variables for use
    file = open("Data/scores.txt", "r")
    lines = file.readlines()
    file.close()

    # sort the list of lines read
    lines.sort(key = lambda x: (len(x), x), reverse = True)

    # write the sorted list to file
    file = open("Data/scores.txt", "w")
    for i in range(5):
        file.write(lines[i])


# write scores to a text document
def write_score():
    global points
    global playerName

    file = open("Data/scores.txt", "a")
    file.write(str(points) + " " + playerName + "\n")


# display scores to screen
def show_scores():
    # sort the scores before showing
    write_score()
    sort_scores()

    # read in file
    f = open("Data/scores.txt")
    line = f.readline()

    # fill in screen with details
    screen.fill(black)
    text_to_screen(screen=screen, text="High Scores", x=70, y=100, color=white)
    height_win = 180
    for i in range(5):
        text_to_screen(screen=screen, text=line.replace("\n", ""), x=140, y=height_win, color=white)
        line = f.readline()
        height_win += 60
    text_to_screen(screen, "Press space to continue", 100, 600, 20, white)
    pygame.display.flip()

    await_continue()


# waits for player to enter a specific key to followup with action
def await_continue():
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


# prints objects on the screen
def print_screen(screen, player, door, enemy, powerup, barrier):
    global level_count
    global playerName

    screen.fill(green)
    player.draw()
    door.draw()
    if len(powerup) != 0:
        powerup[0].draw()

    if level_count != 1:
        for i in range(len(enemy)):
            enemy[i].draw()

    """for i in range(num_barriers):
        print(num_barriers + " " + i)
        barriers[i].draw()"""
    barrier.draw()

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


# create base game object class for inheritance
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
        # change board variable
        board[y][x] = 1

    # draws player to screen
    def draw(self):
        image = pygame.image.load('Data/hero.png')  # adjust as needed if file changes

        # change sprite direction
        if self.face == LEFT:
            image = pygame.transform.rotate(image, 270)
        elif self.face == UP:
            image = pygame.transform.rotate(image, 180)
        elif self.face == RIGHT:
            image = pygame.transform.rotate(image, 90)

        screen.blit(image, self.rect)

    # handle what happens when player pushes keys
    def move_player(self, barrier):
        actual = self.vel * square

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            if not (self.x <= 0) and (self.y != barrier.y or self.x - 1 != barrier.x):
                self.rect.move_ip(-actual, 0)
                self.x -= self.vel
                self.face = LEFT
        elif key[pygame.K_RIGHT]:
            if not (self.x >= scale - self.vel) and (self.y != barrier.y or self.x + 1 != barrier.x):
                self.rect.move_ip(actual, 0)
                self.x += self.vel
                self.face = RIGHT
        elif key[pygame.K_UP]:
            if not (self.y <= 0) and (self.y - 1 != barrier.y or self.x != barrier.x):
                self.rect.move_ip(0, -actual)
                self.y -= self.vel
                self.face = UP
        elif key[pygame.K_DOWN]:
            if not (self.y >= scale - self.vel) and (self.y + 1 != barrier.y or self.x != barrier.x):
                self.rect.move_ip(0, actual)
                self.y += self.vel
                self.face = DOWN

        # change board variable
        board[self.y][self.x] = 1

    # handle space bar use
    def fire(self, enemy, door):
        ice_x = self.x
        ice_y = self.y

        if self.face == RIGHT:
            while ice_x < height / square - 1:
                ice_x += 1
                self.draw_ice(ice_x, ice_y, enemy, door)
                if self.check_collision(enemy, ice_x, ice_y):
                    break
        elif self.face == LEFT:
            while ice_x > 0:
                ice_x -= 1
                self.draw_ice(ice_x, ice_y, enemy, door)
                if self.check_collision(enemy, ice_x, ice_y):
                    break
        elif self.face == DOWN:
            while ice_y < height / square - 1:
                ice_y += 1
                self.draw_ice(ice_x, ice_y, enemy, door)
                if self.check_collision(enemy, ice_x, ice_y):
                    break
        elif self.face == UP:
            while ice_y > 0:
                ice_y -= 1
                self.draw_ice(ice_x, ice_y, enemy, door)
                if self.check_collision(enemy, ice_x, ice_y):
                    break

    # UNFINISHED: shows animation for player firing
    def draw_ice(self, ice_x, ice_y, enemy, door):
        # clock for firing
        clock = pygame.time.Clock()

        global screen
        # print_screen(screen, self, door, enemy) make animation

        ice_block = pygame.rect.Rect(ice_x * square, ice_y * square, square, square)

        pygame.draw.rect(screen, blue, ice_block)
        pygame.display.flip()

        clock.tick()

    # checks for collisions
    def check_collision(self, enemy, ice_x, ice_y):
        global points
        global level_count
        if level_count != 1:
            for i in range(len(enemy)):
                if int(enemy[i].x) == ice_x and int(enemy[i].y) == ice_y:
                    enemy.remove(enemy[i])
                    points += 1
                    return True


# class for movement between levels
class Door(GameObject):
    def __init__(self, x, y, color):
        GameObject.__init__(self, x, y, color)

    # draws door (hole)
    def draw(self):
        image = pygame.image.load('Data/door.png')  # adjust as needed if file changes
        screen.blit(image, self.rect)
        # change board variable
        board[self.y][self.x] = 2


# class for enemy objects
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

    # draws individual enemy
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

    # moves individual enemies
    def move(self, player, barrier):
        actual = self.vel * square
        x_dist = abs(self.x - player.x)
        y_dist = abs(self.y - player.y)

        if x_dist > y_dist:
            if self.x > player.x and (self.x - 1 != barrier.x or self.y != barrier.y):
                self.rect.move_ip(-actual, 0)
                self.x -= self.vel
                self.face = LEFT
            elif self.x < player.x and (self.x + 1 != barrier.x or self.y != barrier.y):
                self.rect.move_ip(actual, 0)
                self.x += self.vel
                self.face = RIGHT
        else:
            if self.y > player.y and (self.x != barrier.x or self.y - 1 != barrier.y):
                self.rect.move_ip(0, -actual)
                self.y -= self.vel
                self.face = UP
            elif self.y < player.y and (self.x != barrier.x or self.y + 1 != barrier.y):
                self.rect.move_ip(0, actual)
                self.y += self.vel
                self.face = DOWN

        board[self.y][self.x] = 3


# class for barriers
class Barrier(GameObject):
    def __init__(self):
        GameObject.__init__(self, random.randint(0, scale - 1), random.randint(0, scale - 1), black)

    def draw(self):
        image = pygame.image.load('Data/boulder.png')  # adjust as needed if file changes
        screen.blit(image, self.rect)


# class for power ups in game
class PowerUp(GameObject):
    def __init__(self, color):
        GameObject.__init__(self, random.randint(0, scale - 1), random.randint(0, scale - 1), color)

    # checks for collisions
    def check_collision(self, player):
        if self.x == player.x and self.y == player.y:
            return True


# class for health power up
class Health(PowerUp):
    def __init__(self):
        PowerUp.__init__(self, red)

    def draw(self):
        image = pygame.image.load('Data/heart.png')  # adjust as needed if file changes
        screen.blit(image, self.rect)
        # change board variable
        board[self.y][self.x] = 5

    # cause special effect on player variable
    def boost(self, player):
        global health

        if self.check_collision(player):
            health += 1


# class for treasure power up
class Treasure(PowerUp):
    def __init__(self):
        PowerUp.__init__(self, horse_brown)

    def draw(self):
        image = pygame.image.load('Data/chest.png')  # adjust as needed if file changes
        screen.blit(image, self.rect)
        # change board variable
        board[self.y][self.x] = 6

    # cause special effect on player variable
    def boost(self, player):
        global points

        if self.check_collision(player):
            points += 5


main()
