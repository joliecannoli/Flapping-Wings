import pygame
import os  

pygame.init()
pygame.mixer.init
screen_width, screen_height = 1100, 600 
screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.Font('FFFFORWA.ttf', 10)

dragon_x, dragon_y = 400, 200
dragon_speed = 2
dragon_animation_delay = 400 
last_dragon_update = pygame.time.get_ticks()
dragon_index = 0

def play_start_dragon_sound():   
    pygame.mixer.music.load("assets/sound_effects/wings_flapping.wav")
    pygame.mixer.music.play() 

def play_button_click_sound():
    pygame.mixer.music.load("assets/sound_effects/button_click.wav")
    pygame.mixer.music.play() 


mountain_bg = pygame.image.load(os.path.join("assets/backgrounds", "mountains.png"))
cave_bg = pygame.image.load(os.path.join("assets/backgrounds", "cave.png"))
notre_dame_bg = pygame.image.load(os.path.join("assets/backgrounds", "notre_dame.png"))

mountain_bg = pygame.transform.scale(mountain_bg, (screen_width, screen_height))
cave_bg = pygame.transform.scale(cave_bg, (screen_width, screen_height))
notre_dame_bg = pygame.transform.scale(notre_dame_bg, (screen_width, screen_height))

current_bg = mountain_bg

dragon = [pygame.image.load(os.path.join("assets/characters/dragon", "dragon1.png")),
          pygame.image.load(os.path.join("assets/characters/dragon", "dragon2.png"))]

start_button = pygame.image.load(os.path.join("assets/buttons", "start.png"))
start_button = pygame.transform.scale(start_button, (220, 78))
    
def display_start_screen():
    title = pygame.image.load(os.path.join("assets/misc", "title.png"))
    title = pygame.transform.scale(title, (240, 99))
    bg_text = font.render("Press right arrow key to change setting", True, (40, 60, 120))

    screen.blit(current_bg, (0, 0))
    screen.blit(start_button, (420, 450))
    screen.blit(title, (405, 50))
    screen.blit(bg_text, (395, 400))
    screen.blit(dragon[dragon_index], (dragon_x, dragon_y))
    pygame.display.update() 

def display_sprite_screen():
    left_arrow = pygame.image.load(os.path.join("assets/buttons", "arrow_left.png"))
    right_arrow = pygame.image.load(os.path.join("assets/buttons", "arrow_right.png"))
    sprite_text = font.render("Select your character", True, (40, 60, 120))
    start_text = font.render("Press space key to begin", True, (40, 60, 120))

    sprite_text = pygame.transform.scale(sprite_text, (280, 50))
    left_arrow = pygame.transform.scale(left_arrow, (700, 300))
    right_arrow = pygame.transform.scale(right_arrow, (700, 300))

    screen.blit(current_bg, (0, 0))
    screen.blit(sprite_text, (395, 55))
    screen.blit(left_arrow, (0, 150))
    screen.blit(right_arrow, (370, 125))
    screen.blit(dragon[dragon_index], (dragon_x, dragon_y))
    screen.blit(start_text, (445, 400))
    pygame.display.update() 

def animate_start_dragon(): 
    global dragon_y, dragon_speed, last_dragon_update, dragon_index
    current_time = pygame.time.get_ticks() 
    if current_time - last_dragon_update > dragon_animation_delay:  
            dragon_index = (dragon_index + 1) % len(dragon) 
            last_dragon_update = current_time 
    dragon_y += dragon_speed 
    if dragon_y > 220 or dragon_y < 185:
        dragon_speed *= -1
        play_start_dragon_sound()
    
def main_loop():
    global current_bg
    running = True
    current_screen ="start_screen"
    while running: 
        if current_screen == "start_screen":
            display_start_screen()
        elif current_screen == "settings_screen":
            display_sprite_screen() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button ==1:
                start_button_rect = start_button.get_rect(topleft=(420, 450))
                if start_button_rect.collidepoint(event.pos):
                    play_button_click_sound() 
                    current_screen = "settings_screen"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT: 
                    if current_bg == mountain_bg:
                        current_bg = cave_bg 
                    elif current_bg == cave_bg:
                        current_bg = notre_dame_bg
                    else: 
                        current_bg = mountain_bg 
        animate_start_dragon()

if __name__ == "__main__": 
    main_loop() 

 


    






