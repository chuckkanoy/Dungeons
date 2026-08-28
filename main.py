# project: Dungeons
# author: Charles Kanoy
# version: 1.0.0

from py_compile import main

import pygame
import sys
import random
from time import sleep

# user defined files
import interface
from interface import text_to_screen, display_transition_screen, print_screen
from game_objects import Door, Player, Barrier, Health, Treasure, Enemy

OFF_CAMERA = 1000

class GameCabinet:
    num_barriers = 0
    level = 1
    enemy_increase_rate = 1
    num_possible_power_ups = 2
    player = player = Player(random.randint(0, interface.scale - 1), random.randint(0, interface.scale - 1), 1, interface.horse_brown)
    vill = []
    door = Door(random.randint(0, interface.scale - 1), random.randint(0, interface.scale - 1), interface.black)
    powerup = []
    game_objects = []
    barrier = Barrier()

    # main method called to begin game actions
    def main(self):
        # show_scores()  # use temporarily for scoreboard modification
        interface.load_interface()
        interface.play_background_music()
        
        interface.display_transition_screen("Dungeons")
        
        while self.is_game_running():
            self.setup_level()
            self.game_play()

    def is_game_running(self):
        retVal = True # default to game running
        
        if self.player.health <= 0:
            retVal = False
                    
        return retVal
        
    # initialize game space and name
    def get_player_data(self):
        # allow player to only enter 3 characters for initials
        while len(self.player.name) != 3:
            # quit if necessary
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    elif event.unicode.isalpha():
                        self.player.name += event.unicode.upper()
                    elif event.key == pygame.K_BACKSPACE:
                        self.player.name = self.player.name[:-1]
                    # show key input as it happens on screen
                    display_transition_screen("Enter initials:", self.player.name)


    # setup game variables
    def setup_level(self):
        while self.player.x == self.door.x and self.player.y == self.door.y:
            self.door = Door(random.randint(0, interface.scale - 1), random.randint(0, interface.scale - 1), interface.black)
        self.game_objects = [self.player, self.door]
        # add power interface.UP depending on random
        appears = random.randint(0, 100)
        if 0 <= appears <= 50:
            self.powerup = []
        else:
            choice = random.randint(0, self.num_possible_power_ups)
            if choice == 0:
                self.game_objects += [Health()]
            else:
                self.game_objects += [Treasure()]

        # add enemies
        vill = []
        if self.level != 1:
            for i in range(self.enemy_increase_rate):
                enemy = Enemy(random.randint(0, interface.scale - 1), random.randint(0, interface.scale - 1), 1, 1, interface.red, self.enemy_increase_rate)
                vill.append(enemy)
                self.game_objects += [enemy]

        barrier = Barrier()
        # for j in range(num_barriers):
        if self.level == 1:
            for i in range(self.enemy_increase_rate):
                while (self.player.x == barrier.x and self.player.y == barrier.y) or (self.door.x == barrier.x and self.door.y == barrier.y):
                    barrier = Barrier()
        else:
            for i in range(self.enemy_increase_rate):
                while (vill[i].x == barrier.x and vill[i].y == barrier.y) or \
                        (self.player.x == barrier.x and self.player.y == barrier.y) or (self.door.x == barrier.x and self.door.y == barrier.y):
                    barrier = Barrier()
        self.game_objects += [barrier]


    # run game when player indicates
    def game_play(self):
        # print_board() used when displaying array being saved
        while self.is_game_running():
            interface.print_screen(interface.screen, self.player, self.door, self.vill, self.powerup, self.barrier, self.level)
            interface.handle_user_input(self.player)
            for obj in self.game_objects:
                self.handle_object_collision(obj)
            sleep(0.01)
            # self.transition_level()
        self.game_over()


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
        
        self.get_player_data()
                        
        self.show_scores()


    # display the level the player is on
    def transition_level(self):
        self.level += 1

        # increase enemy_increase_rate appropriately
        if (self.level % 5) == 0:
            self.enemy_increase_rate += 1
            
        self.setup_level()
        print("transition level")
        
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
            file.write(lines[i])


    # write scores to a text document
    def write_score(self):
        global name

        file = open("data/scores.txt", "a")
        file.write(str(self.points) + " " + name + "\n")


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
    
    def handle_object_collision(self, obj):
        if self.player.x == obj.x and self.player.y == obj.y:
            if isinstance(obj, Health):
                self.player.health += 1
            elif isinstance(obj, Treasure):
                self.player.points += 5
                Treasure.x = OFF_CAMERA
                Treasure.y = OFF_CAMERA
            elif isinstance(obj, Enemy):
                self.player.health -= 1
            elif isinstance(obj, Door):
                self.transition_level()


if __name__ == "__main__":
    game = GameCabinet()
    game.main()
