import pygame
import random

import interface
from timer import Timer

# create base game object class for inheritance
class GameObject:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.rect = pygame.rect.Rect(self.x * interface.square, self.y * interface.square, interface.square, interface.square)
        self.face = interface.DOWN
        
    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = x * interface.square
        self.rect.y = y * interface.square


# class for movement between levels
class Door(GameObject):
    def __init__(self, x, y, color):
        GameObject.__init__(self, x, y, color)

    # draws door (hole)
    def draw(self):
        image = pygame.image.load('data/door.png')  # adjust as needed if file changes
        interface.screen.blit(image, self.rect)
        
        
# defines player in game
class Player(GameObject):
    def __init__(self, x, y, vel, color, health):
        GameObject.__init__(self, x, y, color)
        self.vel = vel
        self.name = ""
        self.health = health
        self.points = 0

    # draws player to screen
    def draw(self):
        image = pygame.image.load('data/hero.png')  # adjust as needed if file changes

        interface.screen.blit(image, self.rect)

    # handle what happens when player pushes keys
    def move(self, direction):
        if direction == interface.UP and self.y > 0:
            self.rect.move_ip(0, -self.vel * interface.square)
            self.y -= self.vel
        elif direction == interface.DOWN and self.y < interface.scale - 1:
            self.rect.move_ip(0, self.vel * interface.square)
            self.y += self.vel
        elif direction == interface.LEFT and self.x > 0:
            self.rect.move_ip(-self.vel * interface.square, 0)
            self.x -= self.vel
        elif direction == interface.RIGHT and self.x < interface.scale - 1:
            self.rect.move_ip(self.vel * interface.square, 0)
            self.x += self.vel

    # handle space bar use
    def fire(self, enemy, door):
        ice_x = self.x
        ice_y = self.y

        if self.face == interface.RIGHT:
            while ice_x < interface.height / interface.square - 1:
                ice_x += 1
                self.draw_ice(ice_x, ice_y, enemy, door)
                if self.check_collision(enemy, ice_x, ice_y):
                    break
        elif self.face == interface.LEFT:
            while ice_x > 0:
                ice_x -= 1
                self.draw_ice(ice_x, ice_y, enemy, door)
                if self.check_collision(enemy, ice_x, ice_y):
                    break
        elif self.face == interface.DOWN:
            while ice_y < interface.height / interface.square - 1:
                ice_y += 1
                self.draw_ice(ice_x, ice_y, enemy, door)
                if self.check_collision(enemy, ice_x, ice_y):
                    break
        elif self.face == interface.UP:
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

        ice_block = pygame.rect.Rect(ice_x * interface.square, ice_y * interface.square, interface.square, interface.square)

        pygame.draw.rect(interface.screen, interface.blue, ice_block)
        pygame.display.flip()

        clock.tick()

    # checks for collisions
    def check_collision(self, enemy, ice_x, ice_y):
        global points
        
        for i in range(len(enemy)):
            if int(enemy[i].x) == ice_x and int(enemy[i].y) == ice_y:
                enemy.remove(enemy[i])
                points += 1
                return True
            
    # handle timed enemy
    def run_enemy(self, enemy, barrier, level):
        if level != 1:
            for i in range(len(enemy)):
                enemy[i].move(self, barrier)
                if self.x == enemy[i].x and self.y == enemy[i].y:
                    self.health -= 1
                    enemy.remove(enemy[i])
                    break
               
                
# class for barriers
class Barrier(GameObject):
    def __init__(self):
        GameObject.__init__(self, random.randint(0, interface.scale - 1), random.randint(0, interface.scale - 1), interface.black)

    def draw(self):
        image = pygame.image.load('data/boulder.png')  # adjust as needed if file changes
        interface.screen.blit(image, self.rect)


# class for enemy objects
class Enemy(GameObject):
    def __init__(self, x, y, vel, health, color, count):
        GameObject.__init__(self, x, y, color)
        self.vel = vel
        self.health = health
        self.face = interface.DOWN
        self.enemies = [count]
        self.damage = 10
        self.move_timer = Timer(0.5)

    # draws individual enemy
    def draw(self):
        image = pygame.image.load('data/monster.png')

        # change sprite direction
        if self.face == interface.LEFT:
            image = pygame.transform.rotate(image, 270)
        elif self.face == interface.UP:
            image = pygame.transform.rotate(image, 180)
        elif self.face == interface.RIGHT:
            image = pygame.transform.rotate(image, 90)

        interface.screen.blit(image, self.rect)

    # moves individual enemies
    def move(self, player, game_objects):
        if self.move_timer.is_expired():
            self.move_timer.reset()
            actual = self.vel * interface.square
            x_dist = abs(self.x - player.x)
            y_dist = abs(self.y - player.y)

            if x_dist > y_dist:
                if self.x > player.x and 0 <= (self.x - 1) < interface.scale and (not isinstance(game_objects[self.y][self.x - 1], (Barrier, Enemy))):
                    self.rect.move_ip(-actual, 0)
                    self.x -= self.vel
                elif self.x < player.x and 0 <= (self.x + 1) < interface.scale and (not isinstance(game_objects[self.y][self.x + 1], (Barrier, Enemy))):
                    self.rect.move_ip(actual, 0)
                    self.x += self.vel
            else:
                if self.y > player.y and 0 <= (self.y - 1) < interface.scale and (not isinstance(game_objects[self.y - 1][self.x], (Barrier, Enemy))):
                    self.rect.move_ip(0, -actual)
                    self.y -= self.vel
                elif self.y < player.y and 0 <= (self.y + 1) < interface.scale and (not isinstance(game_objects[self.y + 1][self.x], (Barrier, Enemy))):
                    self.rect.move_ip(0, actual)
                    self.y += self.vel


# class for power ups in game
class PowerUp(GameObject):
    def __init__(self, color):
        GameObject.__init__(self, random.randint(0, interface.scale - 1), random.randint(0, interface.scale - 1), color)

    # checks for collisions
    def check_collision(self, player):
        if self.x == player.x and self.y == player.y:
            return True


# class for health power interface.UP
class Health(PowerUp):
    def __init__(self):
        PowerUp.__init__(self, interface.red)
        self.health = 10

    def draw(self):
        image = pygame.image.load('data/heart.png')  # adjust as needed if file changes
        interface.screen.blit(image, self.rect)


# class for treasure power interface.UP
class Treasure(PowerUp):
    def __init__(self):
        PowerUp.__init__(self, interface.horse_brown)

    def draw(self):
        image = pygame.image.load('data/chest.png')  # adjust as needed if file changes
        interface.screen.blit(image, self.rect)