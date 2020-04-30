# Coronavirus Fight
import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from pygame.sprite import RenderUpdates
import os
import random
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50,50,50)
RED = (255, 0, 0)
GREEN = (87, 189, 36)
BLUE = (36, 189, 176)
YELLOW = (255, 248, 122)

pygame.font.init()

# Initialize the game screen
pygame.init()
width, height = 1200, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rona Rambo")

# Load images
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (width, height))
player = pygame.image.load("maledoc2.png")
virus = pygame.image.load("CoronaVirus.png")
virus = pygame.transform.scale(virus, (100, 75))

def create_surface_with_text(text, font_size, text_color, background_color):
    font = pygame.freetype.SysFont("comicsans", font_size, bold = True)
    surface, _ = font.render(text = text, fgcolor = text_color, bgcolor = background_color)
    return surface.convert_alpha()

class UIElement(Sprite):

    def __init__(self, center_position, text, font_size, text_color, background_color, action=None):
        """
        Args:
            center_position - tuple (x, y)
            text - string of text to write
            font_size - int
            background_color (background colour) - tuple (r, g, b)
            text_color (text colour) - tuple (r, g, b)
        """
        self.mouse_over = False  # indicates if the mouse is over the element

        # create the default image
        default_image = create_surface_with_text(text=text, font_size=font_size, text_color = text_color, background_color = background_color)

        # create the image that shows when mouse is over the element
        highlighted_image = create_surface_with_text(text=text, font_size=font_size * 1.5, text_color = text_color, background_color = background_color)

        # add both images and their rects to lists
        self.images = [default_image, highlighted_image]

        self.rects = [
            default_image.get_rect(center = int(center_position)),
            highlighted_image.get_rect(center = int(center_position))]

        self.action = action

        # calls the init method of the parent sprite class
        super().__init__()

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)


def main():
    pygame.init()

    screen = pygame.display.set_mode((width, height))
    game_state = GameState.TITLE
    title_font = pygame.font.SysFont("comicsans", 120)
    title_label = title_font.render("Rona Rambo", 1, BLACK)
    screen.blit(title_label, (600, 200))

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.NEWGAME:
            maingame()
            play_level(screen)

        if game_state == GameState.QUIT:
            pygame.quit()
            return

def title_screen(screen):
    start_btn = UIElement(
        center_position = (width/2, 300),
        font_size=30,
        text_color=WHITE,
        background_color=BLUE,
        text="Start",
        action = GameState.NEWGAME)

    quit_btn = UIElement(
        center_position=(width/2, 400),
        font_size=30,
        text_color=WHITE,
        background_color=BLUE,
        text="Quit",
        action=GameState.QUIT)

    buttons = RenderUpdates(start_btn, quit_btn)
    return game_loop(screen, buttons)

def play_level(screen,player):
    return_btn = UIElement(
        center_position=(140, 570),
        font_size = 30,
        text_color = WHITE,
        background_color = BLUE,
        text="Return to main menu",
        action = GameState.TITLE)

    buttons = RenderUpdates(return_btn)
    return game_loop(screen, buttons)

def game_loop(screen, buttons):
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(BLUE)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action

        buttons.draw(screen)
        pygame.display.flip()

class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1


# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """ The constructor of the class """
        pygame.sprite.Sprite.__init__(self)
        self.image = player
        # the nurse's position
        self.x = x
        self.y = y
        self.phitbox = (width / 2 +10, height / 2 -5,90, 340)

    def handle_keys(self):
        """ Handles Keys """
        key = pygame.key.get_pressed()
        dist = 4
        if key[pygame.K_DOWN]: # down key
            self.y += dist # move down
        elif key[pygame.K_UP]: # up key
            self.y -= dist # move up
        if key[pygame.K_RIGHT]: # right key
            self.x = self.x + dist # move right
        elif key[pygame.K_LEFT]: # left key
            self.x = self.x - dist # move left

    def draw(self, screen):
        # blit yourself at your current position
        screen.blit(player, (int(self.x), int(self.y)))
        self.phitbox = (self.x +10, self.y +17,90, 340)
        #pygame.draw.rect(screen, (255, 0, 0,), self.phitbox, 2)

# Right going Left Coronas
class Coronavirus(pygame.sprite.Sprite):
    def __init__(self, x, y, health=100):
        pygame.sprite.Sprite.__init__(self)
        self.image = virus
        self.x = x
        self.y = y
        self.health = health
        self.hitbox = (self.x +5, self.y, 90, 75)

    def draw(self, screen):
        screen.blit(virus, (int(self.x), int(self.y)))
        self.hitbox = (self.x +5, self.y,90, 75)
        #pygame.draw.rect(screen,(255,0,0),self.hitbox,2)

    def move(self):
        self.x = self.x + 2.5
        if self.x > width:
            self.x = -130
            self.y = random.randint(0, 500)

    def hit(self):
        print('hit')
        self.x = -130


# Left going Right Coronas
class LeftCoronavirus(pygame.sprite.Sprite):
    def __init__(self, x, y, health=100):
        pygame.sprite.Sprite.__init__(self)
        self.image = virus
        self.x = x
        self.y = y
        self.health = health
        self.hitboxleft = (self.x +5, self.y, 90, 75)

    def drawleft(self, screen):
        screen.blit(virus, (int(self.x), int(self.y)))
        self.hitboxleft = (self.x +5, self.y,90, 75)
        #pygame.draw.rect(screen,(255,0,0),self.hitboxleft,2)

    def moveleft(self):
        self.x = self.x - 2.5
        if self.x < 0:
            self.x = width + 50
            self.y = random.randint(0, 500)

    def hitleft(self):
        print('hit')
        self.x = width + 50


# Main Game
def maingame():
    running = True
    FPS = 50
    lives = 5
    score = 0
    frame_rate = 60
    frame_count = 0
    start_time = 90
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 80)
    timer_font = pygame.font.SysFont("comicsans", 50)
    enemies = []
    enemiesleft = []
    wave_length = 1
    playerimage = Player(width / 2, height / 2 - 20)
    clock = pygame.time.Clock()

    # Update Screen
    def redraw_window():
        screen.blit(background, (0, 0))
        playerimage.draw(screen)
        # draw labels
        score_label = main_font.render(f"Score: {score}", 1, (255, 255, 255))
        screen.blit(score_label, (850, 10))
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        screen.blit(lives_label, (1030, 10))

        for rona in enemies:
            rona.draw(screen)

        for ronaleft in enemiesleft:
            ronaleft.drawleft(screen)

        pygame.display.update()

    while running:
        #while loop setup
        clock.tick(FPS)
        redraw_window()
        rona = Coronavirus(0, 100)
        rona.draw(screen)
        playerimage.handle_keys()
        playerimage.draw(screen)
        leftrona = LeftCoronavirus(width, 100)
        leftrona.drawleft(screen)
        for enemy in enemies:
            enemy.move()
        for leftenemy in enemiesleft:
            leftenemy.moveleft()
        
        total_seconds = start_time - (frame_count // frame_rate)
        if total_seconds < 0:
            total_seconds = 0
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        output_string = "Time left: {0:02}:{1:02}".format(minutes, seconds)
        text = timer_font.render(output_string, True, BLACK)
        screen.blit(text, [20, 50])
        frame_count += 1
        clock.tick(frame_rate)
        pygame.display.flip()

        pygame.display.update()

        #Generate additional viruses
        if len(enemies) == 0:
            wave_length += 2
            for i in range(wave_length):
                rona2 = Coronavirus(random.randint(-800, -150),
                                    random.randint(10, 500))  # instance of Coronavirus class
                enemies.append(rona2)
        if len(enemiesleft) == 0:
            wave_length += 1
            for i in range(wave_length):
                rona3 = LeftCoronavirus(random.randint(width, 1800),
                                        random.randint(10, 500))  # instance of Coronavirus class
                enemiesleft.append(rona3)

        #Virus Collision
        for enemy in enemies: #hitboxes: x,y,width,height
            if enemy.hitbox[1] + enemy.hitbox[3] > playerimage.phitbox[1]:
                if enemy.hitbox[0] + enemy.hitbox[2] > playerimage.phitbox[0]:
                    enemy.hit()
                    lives = lives - 1
        for leftenemy in enemiesleft: #hitboxes: x,y,width,height
            if leftenemy.hitboxleft[1] + leftenemy.hitboxleft[3] > playerimage.phitbox[1]:
                if leftenemy.hitboxleft[0] < playerimage.phitbox[0] + playerimage.phitbox[2]:
                    leftenemy.hitleft()
                    lives = lives - 1

        if lives <= 0:
            lost_label = lost_font.render(f"You lost! Score: {score} ", 1, RED)
            screen.blit(lost_label, (width/2, height/2))
            title_screen(screen)

        if pygame.time.get_ticks() >= 9000:
            lost_label = lost_font.render(f"You lost! Score: {score} ", 1, RED)
            screen.blit(lost_label, (width / 2, height / 2))
            title_screen(screen)





main()
