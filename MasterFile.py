import pygame, math


# 2 - Initialize the game
x = 75
y = 250
pygame.init()
width, height = 860, 522
screen = pygame.display.set_mode((width, height))

accuracy = [0,0]
handsanitizer = []

keys = [False, False, False, False]
playerpos = [x,y]

# 3 - Load images
player = pygame.image.load("female nurse.png")
player = pygame.transform.scale(player, (75,250))
hospitalbackground = pygame.image.load("background.png")
handsanitizerimg = pygame.image.load("handsanitizer .png")

# 4 - keep looping through
while 1:
    # 5 - clear the screen before drawing it again
    screen.fill(0)
    # 6 - draw the screen elements
    screen.blit(hospitalbackground, (0,0))
    screen.blit(player, (x,y))
    # 7 - update the screen
    pygame.display.flip()
    # 8 - loop through the events
    for event in pygame.event.get():
        pygame.display.init()
        pygame.display.flip()
        # check if the event is the X button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # if it is quit the game
                pygame.quit()
                exit(0)
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                x -= 5

            if keys[pygame.K_RIGHT]:
                x += 5

            if keys[pygame.K_UP]:
                y -= 5

            if keys[pygame.K_DOWN]:
                y += 5
        pygame.display.update()





