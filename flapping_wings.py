import pygame
import os  

pygame.init()
screen_width, screen_height = 1100, 600 
screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.Font('FFFFORWA.ttf', 10)

dragon_x, dragon_y = 400, 200
dragon_speed = 2
dragon_animation_delay = 400 
last_dragon_update = pygame.time.get_ticks()
start_dragon_index = 0

mountain_bg = pygame.image.load(os.path.join("assets/backgrounds", "mountains.png"))
cave_bg = pygame.image.load(os.path.join("assets/backgrounds", "cave.png"))
notre_dame_bg = pygame.image.load(os.path.join("assets/backgrounds", "notre_dame.png"))

mountain_bg = pygame.transform.scale(mountain_bg, (screen_width, screen_height))
cave_bg = pygame.transform.scale(cave_bg, (screen_width, screen_height))
notre_dame_bg = pygame.transform.scale(notre_dame_bg, (screen_width, screen_height))

current_bg = mountain_bg


start_dragon = [pygame.image.load(os.path.join("assets/characters/dragon", "dragon1.png")),
                     pygame.image.load(os.path.join("assets/characters/dragon", "dragon2.png"))]

def start_screen():
    start_button = pygame.image.load(os.path.join("assets/buttons", "start.png"))
    title = pygame.image.load(os.path.join("assets/misc", "title.png"))

    start_button = pygame.transform.scale(start_button, (220, 78))
    title = pygame.transform.scale(title, (240, 99))
    text = font.render("Press right arrow key to change setting", True, (40, 60, 120))

    screen.blit(current_bg, (0, 0))
    screen.blit(start_button, (420, 450))
    screen.blit(title, (405, 50))
    screen.blit(text, (395, 400))
    screen.blit(start_dragon[start_dragon_index], (dragon_x, dragon_y))
    pygame.display.update() 

def start_dragon_animation(): 
    global dragon_y, dragon_speed, last_dragon_update, start_dragon_index
    current_time = pygame.time.get_ticks() 
    if current_time - last_dragon_update > dragon_animation_delay: 
            start_dragon_index = (start_dragon_index + 1) % len(start_dragon) 
            last_dragon_update = current_time 
    dragon_y += dragon_speed 
    if dragon_y > 215 or dragon_y < 185:
        dragon_speed *= -1
    

def main_loop():
    global current_bg
    running = True
    while running: 
        start_screen() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT: 
                if current_bg == mountain_bg:
                    current_bg = cave_bg 
                elif current_bg == cave_bg:
                    current_bg = notre_dame_bg
                else: 
                    current_bg = mountain_bg 
        start_dragon_animation()

if __name__ == "__main__": 
    main_loop() 

 


    






