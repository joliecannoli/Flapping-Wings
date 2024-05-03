
import pygame
import os
import random  

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
is_space_pressed = False
vertical_velocity_dragon = 0 
gravity = 0.3
score = 0 
final_score = 0 
high_score = 0


button_click_sound = pygame.mixer.Sound("assets/sound_effects/button_click.wav")

def play_button_click_sound(): 
    button_click_sound.play() 

def play_flapping_sound():   
    pygame.mixer.music.load("assets/sound_effects/wings_flapping.wav")
    pygame.mixer.music.play()

def play_falling_sound():
    pygame.mixer.music.load("assets/sound_effects/collision_fall.wav")
    pygame.mixer.music.play()

mountain_bg = pygame.image.load(os.path.join("assets/backgrounds", "mountains.png"))
notre_dame_bg = pygame.image.load(os.path.join("assets/backgrounds", "notre_dame.png"))
mountain_bg = pygame.transform.scale(mountain_bg, (screen_width, screen_height))
notre_dame_bg = pygame.transform.scale(notre_dame_bg, (screen_width, screen_height))
current_bg = mountain_bg

dragon = [pygame.image.load(os.path.join("assets/characters/dragon", "dragon1.png")),
          pygame.image.load(os.path.join("assets/characters/dragon", "dragon2.png"))]
dragon_mask = pygame.mask.from_surface(dragon[0])  


start_button = pygame.image.load(os.path.join("assets/buttons", "start.png"))
start_button = pygame.transform.scale(start_button, (220, 78))
    
column_down = pygame.image.load(os.path.join("assets/obstacles/column", "column_down.png"))
column_up = pygame.image.load(os.path.join("assets/obstacles/column", "column_up.png"))

column_up = pygame.transform.scale(column_up, (100, 200))
column_down = pygame.transform.scale(column_down, (100, 200))
column_up_mask = pygame.mask.from_surface(column_up)
column_down_mask = pygame.mask.from_surface(column_down)

game_over = pygame.image.load(os.path.join("assets/misc", "game_over.png"))
game_over = pygame.transform.scale(game_over, (590, 350))

restart_button = pygame.image.load(os.path.join("assets/buttons", "restart.png"))
restart_button = pygame.transform.scale(restart_button, (500, 350))

quit_button = pygame.image.load(os.path.join("assets/buttons", "quit.png"))
quit_button = pygame.transform.scale(quit_button, (500, 350))


column_x = screen_width
columns = [{"x": screen_width, "y": random.randint(100, 400), "passed": False}]
column_gap = 200 
column_spacing = 300

def display_start_screen():
    title = pygame.image.load(os.path.join("assets/misc", "title.png"))
    title = pygame.transform.scale(title, (240, 99))
    bg_text = font.render("Press right arrow key to change setting", True, (40, 60, 120))

    screen.blit(current_bg, (0, 0))
    screen.blit(start_button, (420, 450))
    screen.blit(title, (420, 50))
    screen.blit(bg_text, (395, 400))
    screen.blit(dragon[dragon_index], (dragon_x, dragon_y))
    pygame.display.update() 

def display_sprite_screen():
    sprite_text = font.render("Select your character", True, (40, 60, 120))
    start_text = font.render("Press space key to begin", True, (40, 60, 120))

    sprite_text = pygame.transform.scale(sprite_text, (280, 50))

    screen.blit(current_bg, (0, 0))
    screen.blit(sprite_text, (395, 55))
    if is_dragon: 
        screen.blit(dragon[dragon_index], (dragon_x, dragon_y))
    screen.blit(start_text, (445, 400))
    pygame.display.update() 

def display_game_screen():
    global score, columns
    screen.blit(current_bg, (0, 0))
    screen.blit(dragon[dragon_index], (dragon_x, dragon_y))
    if current_bg in [mountain_bg]:
        screen.blit(column_up, (column_x, screen_height - column_up.get_height()))

    for column in columns:
        screen.blit(column_up, (column["x"], screen_height - column_up.get_height()))
        screen.blit(column_down, (column["x"], 0))  
        column["x"] -= 5  

        if column["x"] + column_up.get_width() < dragon_x and not column["passed"]:
            column["passed"] = True
            score +=1

        scorekeeping = font.render("Score: " + str(score), True, (40, 60, 120))
        screen.blit(scorekeeping, (1000, 20))

    if random.randint(0, 1000) < 10: 
        new_column_x = screen_width + random.randint(200, 400)
        new_column_y = random.randint(100, 400)
        if not any(abs(new_column_x - col["x"]) < column_up.get_width() for col in columns):
             columns.append({"x": new_column_x, "y": new_column_y, "passed": False})

        collision = any(abs(new_column_x - col["x"]) < column_up.get_width() + 100 for col in columns)
        if not collision:
            columns.append({"x": new_column_x, "y": new_column_y, "passed": False})
        pygame.display.update()  

def display_game_over_screen():
    falling_speed = 30
    global dragon_y, score, high_score, final_score 
    final_score = score 
    while True:
        final_score_text = font.render("Final Score: " + str(final_score), True, (40, 60, 120))
        high_score_text = font.render("High Score: " + str(high_score), True, (40, 60, 120))  # Render high score text
        screen.blit(current_bg, (0, 0))  
        screen.blit(game_over, (250, -50))
        screen.blit(restart_button, (300, 70))
        screen.blit(quit_button, (300, 200))
        screen.blit(final_score_text, (500, 280))
        screen.blit(high_score_text, (500, 400))  
        if score > high_score:
            high_score = score
        dragon_y += falling_speed
        if dragon_y >= screen_height - dragon[dragon_index].get_height():
            dragon_y = screen_height - dragon[dragon_index].get_height()
            screen.blit(dragon[dragon_index], (dragon_x, dragon_y))

            pygame.display.update()
            break
        screen.blit(dragon[dragon_index], (dragon_x, dragon_y))
        pygame.display.update()
                
def detect_collision(dragon_x, dragon_y, dragon_width, dragon_height):
    dragon_rect = pygame.Rect(dragon_x, dragon_y, dragon_width, dragon_height)
    for column in columns:
        column_x = column["x"]
        column_up_y = screen_height - column_up.get_height()
        column_down_y = 0
        column_up_mask_offset = (column_x - dragon_x, column_up_y - dragon_y)
        column_down_mask_offset = (column_x - dragon_x, column_down_y - dragon_y)
        if dragon_rect.colliderect((column_x, column_up_y, column_up.get_width(), column_up.get_height())):
            if dragon_mask.overlap(column_up_mask, column_up_mask_offset):
                return True
        if dragon_rect.colliderect((column_x, column_down_y, column_down.get_width(), column_down.get_height())):
            if dragon_mask.overlap(column_down_mask, column_down_mask_offset):
                return True
    if dragon_y <= 0 or dragon_y + dragon_height >= screen_height:
        return True
    return False

def animate_dragon(current_screen): 
    global dragon_y, dragon_speed, last_dragon_update, dragon_index, vertical_velocity_dragon, gravity, is_space_pressed, is_game_over
    current_time = pygame.time.get_ticks() 
    if current_time - last_dragon_update > dragon_animation_delay and not is_game_over:  
        dragon_index = (dragon_index + 1) % len(dragon) 
        last_dragon_update = current_time
    
    if current_screen == "game_screen":
        dragon_y += dragon_speed + vertical_velocity_dragon
        vertical_velocity_dragon += gravity  

    if dragon_y <= 0: 
        is_game_over = True 

    dragon_rect = pygame.Rect(dragon_x, dragon_y, dragon[0].get_width(), dragon [0].get_height())
    for column in columns:
        column_x = column["x"]
        column_up_y = screen_height - column_up.get_height() 
        column_down_y = 0 
        column_up_mask_offset = (column_x - dragon_x, column_up_y - dragon_y)
        column_down_mask_offset = (column_x - dragon_x, column_down_y - dragon_y)
        if dragon_rect.colliderect((column_x, column_up_y, column_up.get_width(), column_up.get_height())):
            if dragon_mask.overlap(column_up_mask, column_up_mask_offset):
                is_game_over = True
        if dragon_rect.colliderect((column_x, column_down_y, column_down.get_width(), column_down.get_height())):
            if dragon_mask.overlap(column_down_mask, column_down_mask_offset):
                is_game_over = True

        if is_game_over:
            return

def main_loop():
    global is_dragon, current_bg, dragon_index, is_dragon, vertical_velocity_dragon, sprite_screen_displayed, is_space_pressed, dragon_y, column_x, columns, is_game_over, new_column_x, new_column_y, score 
    running = True
    current_screen ="start_screen"
    is_dragon = True 
    sprite_screen_displayed = False 
    is_game_over = False
    new_column_x = screen_width + random.randint(200, 400)
    new_column_y = random.randint(100, 400)
    while running:
        if current_screen == "start_screen":
            display_start_screen() 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if current_bg == mountain_bg:
                            current_bg = notre_dame_bg
                        else: 
                            current_bg = mountain_bg
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button ==1:
                    start_button_rect = start_button.get_rect(topleft=(420, 450))
                    if start_button_rect.collidepoint(event.pos):
                        play_button_click_sound() 
                        current_screen = "settings_screen"

        elif current_screen == "settings_screen":
            display_sprite_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_SPACE:
                        if is_dragon:
                            vertical_velocity_dragon = -8
                        current_screen = "game_screen"
                        sprite_screen_displayed = False
                elif event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_SPACE:
                        is_space_pressed = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        is_space_pressed = False 

        elif current_screen == "game_screen":
            display_game_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        is_space_pressed = True 
                        play_flapping_sound()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        is_space_pressed = False
            if detect_collision(dragon_x, dragon_y, dragon[0].get_width(), dragon[0].get_height()):
                play_falling_sound() 
                display_game_over_screen()
                current_screen = "game_over_screen"
                is_game_over = True
                pygame.display.update()
            else:
                animate_dragon(current_screen)

        elif current_screen == "game_over_screen":
            display_game_over_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    restart_button_rect = restart_button.get_rect(topleft=(300, 130))
                    quit_button_rect = quit_button.get_rect(topleft=(300, 250))
                    if restart_button_rect.collidepoint(event.pos):
                        score = 0 
                        play_button_click_sound()
                        is_game_over = False
                        dragon_y = 200 
                        column_x = screen_width 
                        columns.clear()  
                        columns.append({"x": new_column_x, "y": new_column_y, "passed": False})
                        is_space_pressed = False
                        current_screen = "start_screen"  
                    elif quit_button_rect.collidepoint(event.pos):
                        play_button_click_sound()
                        running = False

                   
        pygame.display.flip() 

        if is_dragon:
            if is_space_pressed: 
                vertical_velocity_dragon = -8 
            else: 
                vertical_velocity_dragon += gravity 
            animate_dragon(current_screen)

if __name__ == "__main__": 
    main_loop() 
