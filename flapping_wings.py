import pygame
pygame.init()

screen_width, screen_height = 1100, 600 
game_window = pygame.display.set_mode((screen_width, screen_height))

running = True
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    




