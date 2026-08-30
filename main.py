# project: Dungeons
# author: Charles Kanoy
# version: 1.0.0

from py_compile import main

import pygame
import sys
import random
from time import sleep, time

# user defined files
import interface
from interface import text_to_screen, display_transition_screen, print_screen
from game_objects import Door, Player, Barrier, Health, Treasure, Enemy

MAX_HEALTH = 100

class GameCabinet:
    num_barriers = 0
    level = 1
    enemy_increase_rate = 1
    num_possible_power_ups = 2
    player = player = Player(random.randint(0, interface.scale - 1), random.randint(0, interface.scale - 1), 1, interface.horse_brown, MAX_HEALTH)
    enemies = []
    door = Door(random.randint(0, interface.scale - 1), random.randint(0, interface.scale - 1), interface.black)
    powerup = []
    game_objects = []
    barrier = Barrier()
    soundOn = False
    
    game_object_map = [[None] * interface.scale] * interface.scale

    # main method called to begin game actions
    def main(self):
        interface.load_interface()
        if self.soundOn:
            interface.play_background_music()
            
        interface.display_transition_screen("Dungeons")
        
        while self.is_game_running():
            self.setup_level()
            self.game_play()
            self.game_over()
            self.get_player_data()
            self.show_scores()
            

    def is_game_running(self):
        retVal = True # default to game running
        
        if self.player.health <= 0:
            retVal = False
                    
        return retVal
        
    # initialize game space and name
    def get_player_data(self):
        # allow player to only enter 3 characters for initials
        while True:
            # quit if necessary
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    elif event.unicode.isalpha() and len(self.player.name) < 3:
                        self.player.name += event.unicode.upper()
                    elif event.key == pygame.K_BACKSPACE:
                        self.player.name = self.player.name[:-1]
                    elif ((event.key == pygame.K_RETURN) or (event.key == pygame.K_SPACE)) and len(self.player.name) == 3:
                        return
            display_transition_screen("Enter initials:", self.player.name, await_space=False)


    # setup game variables
    def setup_level(self):
        # clear the object map on initial setup
        self.game_object_map = [[None for _ in range(interface.scale)] for _ in range(interface.scale)]
        
        self.add_object_to_map(self.player)
        self.add_object_to_map(self.door)
        
        # add power ups
        power_ups = []
        appears = random.randint(0, 2)
        if appears == 1:
            choice = random.randint(0, self.num_possible_power_ups)
            if choice == 0:
                power_ups += [Health()]
            else:
                power_ups += [Treasure()]
        for power_up in power_ups:
            self.add_object_to_map(power_up)
        
        # add enemies
        if self.level != 1:
            for i in range(self.enemy_increase_rate):
                enemy = Enemy(random.randint(0, interface.scale - 1), random.randint(0, interface.scale - 1), 1, 1, interface.red, self.enemy_increase_rate)
                self.enemies += [enemy]
                self.add_object_to_map(enemy)

        # for j in range(num_barriers):
        barrier = Barrier()
        self.add_object_to_map(barrier)
        self.display_board()
    
    def add_object_to_map(self, obj):
        while self.game_object_map[obj.y][obj.x] is not None:
            # iterate until a free space is found
            obj.set_position(random.randint(0, interface.scale - 1), random.randint(0, interface.scale - 1))
        self.game_object_map[obj.y][obj.x] = obj
        self.game_objects += [obj]
        
    def display_board(self):
        for y in self.game_object_map:
            string = ""
            for x in y:
                if isinstance(x, Barrier):
                    string += "1 "
                elif isinstance(x, Enemy):
                    string += "2 "
                elif isinstance(x, Player):
                    string += "3 "
                elif isinstance(x, Treasure):
                    string += "4 "
                elif isinstance(x, Health):
                    string += "5 "
                elif isinstance(x, Door):
                    string += "6 "
                else:
                    string += "0 "
            print(string)

    # run game when player indicates
    def game_play(self):
        while self.is_game_running():
            interface.print_screen(interface.screen, self.player, self.game_objects, self.level)
            interface.handle_user_input(self.player, self.game_object_map)
            for obj in self.game_objects:
                if isinstance(obj, list):
                    for item in obj:
                        self.handle_object_collision(item)
                else:
                    self.handle_object_collision(obj)
            for enemy in self.enemies:
                # TODO: add timers and use with enemy.movement_time
                enemy.move(self.player, self.barrier)
            sleep(0.01)


    # handle what happens upon player death
    def game_over(self):
        # display sorted scores
        self.sort_scores()
        self.write_score()

        # declare and adjust global variables
        name = ""
        self.points = 0
        health = 5

        display_transition_screen("Game Over")

        global level
        level = 1

        global enemy_increase_rate
        enemy_increase_rate = 0


    # display the level the player is on
    def transition_level(self):
        self.level += 1

        # increase enemy_increase_rate appropriately
        if (self.level % 5) == 0:
            self.enemy_increase_rate += 1
            
        self.setup_level()
        
        interface.display_transition_screen("Level " + str(self.level))


    # sort scores in text document
    def sort_scores(self):
        # declare local variables for use
        try:
            file = open("data/scores.txt", "r")
        except FileNotFoundError:
            file = open("data/scores.txt", "w")
            file.close()
            file = open("data/scores.txt", "r")
        lines = file.readlines()
        file.close()

        # sort the list of lines read
        lines.sort(key = lambda x: (len(x), x), reverse = True)

        # write the sorted list to file
        file = open("data/scores.txt", "w")
        for i in range(5):
            try:
                file.write(lines[i])
            except IndexError:
                pass


    # write scores to a text document
    def write_score(self):
        file = open("data/scores.txt", "a")
        file.write(str(self.player.points) + " " + self.player.name + "\n")


    # display scores to screen
    def show_scores(self):
        # sort the scores before showing
        self.write_score()
        self.sort_scores()

        # read in file
        f = open("data/scores.txt")
        line = f.readline()

        # fill in screen with details
        interface.screen.fill(interface.black)
        text_to_screen(screen=interface.screen, text="High Scores", x=70, y=100, color=interface.white)
        interface.height_win = 180
        for i in range(5):
            text_to_screen(screen=interface.screen, text=line.replace("\n", ""), x=140, y=interface.height_win, color=interface.white)
            line = f.readline()
            interface.height_win += 60
        text_to_screen(screen=interface.screen, text="Press space to continue", x=100, y=600, color=interface.white)
        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    elif event.key == pygame.K_SPACE:
                        return
            sleep(0.01)
    
    def handle_object_collision(self, obj):
        if self.player.x == obj.x and self.player.y == obj.y:
            if isinstance(obj, Health):
                if self.player.health < MAX_HEALTH:
                    self.player.health += obj.health
                self.game_objects.remove(obj)
            elif isinstance(obj, Treasure):
                self.player.points += 5
                self.game_objects.remove(obj)
            elif isinstance(obj, Enemy):
                self.player.health -= obj.damage
                self.game_objects.remove(obj)
            elif isinstance(obj, Door):
                self.transition_level()


if __name__ == "__main__":
    game = GameCabinet()
    game.main()
