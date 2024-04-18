import pygame
import os 

pygame.init()

screen_width, screen_height = 1100, 600 
screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.Font('FFFFORWA.ttf', 10)

dragon_x, dragon_y = 400, 200
dragon_speed = 3
dragon_animation_delay = 400 
last_dragon_update = pygame.time.get_ticks()
start_dragon_index = 0

start_dragon = [pygame.image.load(os.path.join("assets/characters/dragon", "dragon1.png")),
                     pygame.image.load(os.path.join("assets/characters/dragon", "dragon2.png"))]

def start_screen():
    mountain_bg = pygame.image.load(os.path.join("assets/backgrounds", "mountains.png"))
    start_button = pygame.image.load(os.path.join("assets/buttons", "start.png"))
    title = pygame.image.load(os.path.join("assets/misc", "title.png"))

    mountain_bg = pygame.transform.scale(mountain_bg, (1100, 600))
    start_button = pygame.transform.scale(start_button, (220, 78))
    title = pygame.transform.scale(title, (240, 99))
    text = font.render("Press left and right arrow keys to change setting", True, (37, 55, 110))

    screen.blit(mountain_bg, (0, 0))
    screen.blit(start_button, (420, 450))
    screen.blit(title, (405, 50))
    screen.blit(text, (365, 400))
    screen.blit(start_dragon[start_dragon_index], (dragon_x, dragon_y))
    pygame.display.update() 

def start_dragon_animation(): 
    global dragon_y, dragon_speed, last_dragon_update, start_dragon_index
    current_time = pygame.time.get_ticks() 
    if current_time - last_dragon_update > dragon_animation_delay: 
            start_dragon_index = (start_dragon_index + 1) % len(start_dragon) 
            last_dragon_update = current_time 

    dragon_y += dragon_speed 
    if dragon_y > 210 or dragon_y < 180:
        dragon_speed *= -1
    
def main_loop():
    running = True
    while running: 
        start_screen() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        start_dragon_animation()

if __name__ == "__main__": 
    main_loop() 

 


    






