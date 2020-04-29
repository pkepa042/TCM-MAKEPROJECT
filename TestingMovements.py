import pygame
from pygame.locals import *
import time


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50,50,50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Game Fonts
myfont = None

def text_format(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColor)

    return newText


class Nurse(object):  # represents the Nurse/player, not the game
    def __init__(self):
        """ The constructor of the class """
        self.image = pygame.image.load("female nurse.png")
        self.image = pygame.transform.scale(self.image, (75,250))
        # the nurse's position
        self.x = 75
        self.y = 300

    def handle_keys(self):
        """ Handles Keys """
        key = pygame.key.get_pressed()
        dist = 10
        #if key[pygame.K_DOWN]: # down key
            #self.y += dist # move down
        #elif key[pygame.K_UP]: # up key
            #self.y -= dist # move up
        if key[pygame.K_RIGHT]: # right key
            self.x += dist # move right
        elif key[pygame.K_LEFT]: # left key
            self.x -= dist # move left

    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        surface.blit(self.image, (self.x, self.y))

def timer():
    counting_time = pygame.time.get_ticks() - start_time
    counting_minutes = str(counting_time/60000).zfill(2)
    counting_seconds = str((counting_time%60000)/1000).zfill(2)
    counting_millisecond = str(counting_time%1000).zfill(3)

    counting_string = "%s:%s:%s" % (counting_minutes, counting_seconds, counting_millisecond)

    counting_text = font.render(str(counting_string), 1, BLACK)
    counting_rect = counting_text.get_rect(center = screen.get_rect().center)

    screen.blit(counting_text, counting_rect)

pygame.init()
width, height = 1200, 600
screen = pygame.display.set_mode((width, height))
hospitalbackground = pygame.image.load("background.png")
hospitalbackground = pygame.transform.scale(hospitalbackground, (1200, 600))

nurse = Nurse() # create an instance
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()

pygame.display.set_caption("Rona Rambo")
font = pygame.font.SysFont("comicsans", 30)

running = True
while running:
    # handle every event since the last frame.
    pygame.init()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() # quit the screen
            running = False

    nurse.handle_keys() # handle the keys

    screen.blit(hospitalbackground, (0, 0))
    nurse.draw(screen) # draw the nurse to the screen

    timertext = font.render("Time Left: " + str((90000-pygame.time.get_ticks())/60000) + ":" + str((90000-pygame.time.get_ticks())/1000%60).zfill(2), True, BLACK)
    textRect = timertext.get_rect()
    textRect.topleft = [20,50]
    screen.blit(timertext, textRect)


    pygame.display.update() # update the screen




