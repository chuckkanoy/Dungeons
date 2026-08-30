import pygame
import sys
import time

from game_objects import Barrier
import interface

# screen
size = height, width = 500, 700
screen = pygame.display.set_mode(size)
scale = 10
square = height / scale

# directions
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4

# color palette
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (75, 114, 72)
horse_brown = (68, 58, 50)

def play_background_music():
    # play background music
    pygame.mixer.music.load("data/labyrinth-of-time.mp3")
    pygame.mixer.music.set_volume(.1)
    pygame.mixer.music.play(-1)
    
def load_interface():
    pygame.init()
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    image = pygame.image.load("data/Hero.png")
    pygame.display.set_icon(image)
    pygame.display.set_caption("Dungeons")
    # pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    
# apply text to screen
def text_to_screen(screen, text, x, y, size=40,
                   color=red, font_type='data/slkscr.ttf'):
    text = str(text)
    font = pygame.font.Font(font_type, size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))
    
def display_transition_screen(text1, text2 = "Press space to continue", await_space=True):
    # display transition screen
    screen.fill(black)
    text_to_screen(screen=screen, text=text1, x=100, y=250, color=white)
    text_to_screen(screen=screen, text=text2, x=100, y=400, color=white)
    pygame.display.flip()
    
    while await_space:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    return
        time.sleep(0.01)
    
# prints objects on the screen
def print_screen(screen, player, game_objects, level):
    screen.fill(green)
    if len(game_objects) != 0:
        for obj in game_objects:
            if isinstance(obj, list):
                for item in obj:
                    item.draw()
            else:
                obj.draw()

    # draw player UI on bottom of screen
    outline = pygame.rect.Rect(0, height, width, 200)
    pygame.draw.rect(screen, black, outline)

    text_to_screen(screen=screen, text="Health", x=width / 2, y=height + 60, color=white)
    health_bar = pygame.rect.Rect(width / 2, height + 80, player.health, 10)
    max_health = pygame.rect.Rect(width / 2, height + 80, 100, 10)
    pygame.draw.rect(screen, white, max_health)
    pygame.draw.rect(screen, green, health_bar)

    text_to_screen(screen=screen, text="Level " + str(level), x=width / 14, y=height + 60, color=white)

    text_to_screen(screen=screen, text="Points " + str(player.points), x=width / 14, y=height + 90, color=white)
    pygame.display.flip()
    
def handle_user_input(player, object_map):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_UP:
                if not isinstance(object_map[player.y - 1][player.x], Barrier):
                    player.move(UP)
            elif event.key == pygame.K_DOWN:
                if (player.y + 1 < interface.scale) and (not isinstance(object_map[player.y + 1][player.x], Barrier)):
                    player.move(DOWN)
            elif event.key == pygame.K_LEFT:
                if not isinstance(object_map[player.y][player.x - 1], Barrier):
                    player.move(LEFT)
            elif event.key == pygame.K_RIGHT:
                if (player.x + 1 < interface.scale) and (not isinstance(object_map[player.y][player.x + 1], Barrier)):
                    player.move(RIGHT)