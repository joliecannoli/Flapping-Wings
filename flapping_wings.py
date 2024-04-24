import pygame
import os  

pygame.init()
pygame.mixer.init() 
screen_width, screen_height = 1100, 600 
screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.Font('FFFFORWA.ttf', 10)

dragon_x, dragon_y = 400, 200
dragon_speed = 2
dragon_animation_delay = 400 
last_dragon_update = pygame.time.get_ticks()
dragon_index = 0

bat_x, bat_y = 400, 150
bat_speed = 2
bat_animation_delay = 400
last_bat_update = pygame.time.get_ticks() 
bat_index = 0

vertical_velocity_dragon = 0
vertical_velocity_bat = 0 

gravity = 0.5

def play_start_dragon_sound():   
    pygame.mixer.music.load("assets/sound_effects/wings_flapping.wav")
    pygame.mixer.music.play() 

button_click_sound = pygame.mixer.Sound("assets/sound_effects/button_click.wav")

def play_button_click_sound(): 
    button_click_sound.play() 

mountain_bg = pygame.image.load(os.path.join("assets/backgrounds", "mountains.png"))
cave_bg = pygame.image.load(os.path.join("assets/backgrounds", "cave.png"))
notre_dame_bg = pygame.image.load(os.path.join("assets/backgrounds", "notre_dame.png"))

mountain_bg = pygame.transform.scale(mountain_bg, (screen_width, screen_height))
cave_bg = pygame.transform.scale(cave_bg, (screen_width, screen_height))
notre_dame_bg = pygame.transform.scale(notre_dame_bg, (screen_width, screen_height))

current_bg = mountain_bg

dragon = [pygame.image.load(os.path.join("assets/characters/dragon", "dragon1.png")),
          pygame.image.load(os.path.join("assets/characters/dragon", "dragon2.png"))]

bat = [pygame.image.load(os.path.join("assets/characters/bat", "bat1.png")),
       pygame.image.load(os.path.join("assets/characters/bat", "bat2.png"))]

start_button = pygame.image.load(os.path.join("assets/buttons", "start.png"))
start_button = pygame.transform.scale(start_button, (220, 78))

left_arrow = pygame.image.load(os.path.join("assets/buttons", "arrow_left.png"))
right_arrow = pygame.image.load(os.path.join("assets/buttons", "arrow_right.png"))

left_arrow = pygame.transform.scale(left_arrow, (700, 300))
right_arrow = pygame.transform.scale(right_arrow, (700, 300))
    
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
    sprite_text = font.render("Select your character", True, (40, 60, 120))
    start_text = font.render("Press space key to begin", True, (40, 60, 120))

    sprite_text = pygame.transform.scale(sprite_text, (280, 50))

    screen.blit(current_bg, (0, 0))
    screen.blit(sprite_text, (395, 55))
    screen.blit(left_arrow, (0, 150))
    screen.blit(right_arrow, (370, 125))
    if is_dragon: 
        screen.blit(dragon[dragon_index], (dragon_x, dragon_y))
    else:
        resized_bat = pygame.transform.scale(bat[bat_index], (bat[bat_index].get_width() * 1.5, bat[bat_index].get_height() * 1.5))
        screen.blit(resized_bat, (bat_x, bat_y))
    screen.blit(start_text, (445, 400))
    pygame.display.update() 

def animate_dragon(): 
    global dragon_y, dragon_speed, last_dragon_update, dragon_index, vertical_velocity_dragon, gravity 
    current_time = pygame.time.get_ticks() 
    if current_time - last_dragon_update > dragon_animation_delay:  
            dragon_index = (dragon_index + 1) % len(dragon) 
            last_dragon_update = current_time 
    dragon_y += dragon_speed + vertical_velocity_dragon 
    vertical_velocity_dragon += gravity 
    if dragon_y > 220:
        dragon_y = 220
        vertical_velocity_dragon = 0
        play_start_dragon_sound()

def animate_bat():
    global bat_y, bat_speed, last_bat_update, bat_index, vertical_velocity_bat, gravity 
    current_time = pygame.time.get_ticks() 
    if current_time - last_bat_update > bat_animation_delay:
        bat_index = (bat_index + 1) % len(bat)
        last_bat_update = current_time 
    bat_y += bat_speed + vertical_velocity_bat
    vertical_velocity_bat += gravity 
    if bat_y > 180:
        bat_speed *= -1
        play_start_dragon_sound()
    elif bat_y < 150:
        bat_speed *= -1 
        play_start_dragon_sound()  

def main_loop():
    global current_bg, dragon_index, bat_index, is_dragon, vertical_velocity_dragon, vertical_velocity_bat, sprite_screen_displayed
    running = True
    current_screen ="start_screen"
    is_dragon = True 
    sprite_screen_displayed = False 
    while running: 
        if current_screen == "start_screen":
            display_start_screen() 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if current_bg == mountain_bg:
                            current_bg = cave_bg 
                        elif current_bg == cave_bg:
                            current_bg = notre_dame_bg
                        else: 
                            current_bg = mountain_bg
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button ==1:
                    start_button_rect = start_button.get_rect(topleft=(420, 450))
                    if start_button_rect.collidepoint(event.pos):
                        play_button_click_sound() 
                        current_screen = "settings_screen"
                        sprite_screen_displayed = True 

        elif current_screen == "settings_screen": 
            display_sprite_screen() 
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False 
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button ==1:
                        left_arrow_rect = left_arrow.get_rect(topleft=(0, 150))
                        right_arrow_rect = right_arrow.get_rect(topleft=(360, 125))
                        if left_arrow_rect.collidepoint(event.pos) or right_arrow_rect.collidepoint(event.pos):
                            play_button_click_sound()
                            is_dragon = not is_dragon 
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if is_dragon:
                                vertical_velocity_dragon = -8
                            else:
                                vertical_velocity_bat = -8

        if is_dragon:
            animate_dragon()
        else:
            animate_bat()


if __name__ == "__main__": 
    main_loop() 