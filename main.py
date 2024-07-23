import pygame
import random
import math 
import numpy as np
import os

# Initialize pygame modules
pygame.init()
pygame.font.init()
pygame.mixer.init()


# Set up constants
WIDTH, HEIGHT = 800, 800
MAX_DISTANC = WIDTH
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


# Create the game window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WATCH ME!")


# Game elements and attributes
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 30
MONSTER_VEL = 1
PLAYER_VEL = 3
MONSTER_WIDTH, MONSTER_HEIGHT = 30, 30
PLAYER_WIDTH, PLAYER_HEIGHT = 20, 20
draw_blood = False
stop_mixer = False
blood_list = []
blood_stain_list = []


# Load game assets
PLAYER_IMAGE = pygame.image.load(
    os.path.join('assets', 'images', 'player.png')
    )
PLAYER = pygame.transform.rotate(
    pygame.transform.scale(PLAYER_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT)), 0
    )

MONSTER_IMAGE = pygame.image.load(
    os.path.join('assets', 'images', 'monster-removebg-preview.png')
    )
MONSTER = pygame.transform.rotate(
    pygame.transform.scale(MONSTER_IMAGE, (MONSTER_WIDTH, MONSTER_HEIGHT)), 0
    )

CONCRETE = pygame.transform.scale(
    pygame.image.load(os.path.join('assets', 'images', 'concrete.jpg')),
    (WIDTH, HEIGHT)
    )

possessed_laugh_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'collide', 'possessed-laugh-94851.mp3'))
slit_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'kill', '104045__willhiccups__knife-slits-1.mp3'))
monster_eating_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'kill', '472598__audiopapkin__monster-sound-effects-14.wav'))
eating_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'kill', '712065__audiopapkin__monster-eating.wav'))

# # Create a mask surface to represent the visible area
# mask = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
# mask.set_alpha(200)  # Set the initial transparency (200 for slight transparency)


# Function to draw game window
def draw_window(monster, player):
    WIN.blit(CONCRETE, (0, 0))
    WIN.blit(MONSTER, (monster.x, monster.y))
    



    ####### TEST Darkness ######
    
    # mouse position
    mouse_pos = pygame.mouse.get_pos()
    print('mouse_pos', mouse_pos)

    ## lines light cone
    light_angle = 45
    beta_l = - light_angle/2
    beta_r = light_angle/2

    
    v_lamp_pos = np.array([player.x + PLAYER_WIDTH/2, player.y])
    v_middle = np.array([v_lamp_pos[0]-mouse_pos[0], v_lamp_pos[1]-mouse_pos[1]])


    # Convert beta to radians
    beta_rad_l = math.radians(beta_l)
    beta_rad_r = math.radians(beta_r)

    # Calculate the rotated vector v2 using the rotation matrix
    rotation_matrix_l = np.array([[math.cos(beta_rad_l), -math.sin(beta_rad_l)],
                                  [math.sin(beta_rad_l), math.cos(beta_rad_l)]])
    
    rotation_matrix_r = np.array([[math.cos(beta_rad_r), -math.sin(beta_rad_r)],
                                  [math.sin(beta_rad_r), math.cos(beta_rad_r)]])


    v_left = np.dot(rotation_matrix_l, v_middle)
    v_right = np.dot(rotation_matrix_r, v_middle)

    
    #normalize and elongate the vectors
    v_left_norm = np.linalg.norm(v_left)
    v_right_norm = np.linalg.norm(v_right)
    len_factor = 100
    v_left_len = v_left / v_left_norm * len_factor
    v_right_len = v_right / v_right_norm * len_factor
    # use normalized and elongated vectors


    print('v_middle:', v_middle)
    print('v_left:', v_left)
    print('v_right:', v_right)
    print('v_left_len:', v_left_len)
    print('v_right_len:', v_right_len)


    light_line_middle, light_line_left, light_line_right = v_middle*1+v_lamp_pos, v_left_len*100+v_lamp_pos, v_right_len*100+v_lamp_pos

    pygame.draw.line(WIN, (0, 0, 0), v_lamp_pos, light_line_middle, width=3)
    pygame.draw.line(WIN, (200, 0, 0), v_lamp_pos, light_line_left, width=10)
    pygame.draw.line(WIN, (0, 200, 0), v_lamp_pos, light_line_right, width=10)

    reflextion_middle = light_line_middle-2*(light_line_middle-v_lamp_pos)
    reflextion_right = light_line_right-2*(light_line_right-v_lamp_pos)
    reflextion_left = light_line_left-2*(light_line_left-v_lamp_pos)

    pygame.draw.line(WIN, (0, 0, 0), v_lamp_pos, reflextion_middle, width=2)
    pygame.draw.line(WIN, (200, 0, 0), v_lamp_pos, reflextion_left, width=7)
    pygame.draw.line(WIN, (0, 200, 0), v_lamp_pos, reflextion_right, width=7)

    vector_darkness = [light_line_left,
                       light_line_right,
                       reflextion_left,
                       v_lamp_pos,
                       reflextion_right
                       ]
    

    pygame.draw.polygon(WIN, (0, 0, 0, 100), vector_darkness)
    # mask = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, ) Trasparency
    # mask.set_alpha(200)

    ###### END TEST Darkness ######

    WIN.blit(PLAYER, (player.x, player.y))

    

    pygame.display.update()


# Function drawing blood
def drawing_blood(player):
    global draw_blood
    if draw_blood:

        WIN.blit(CONCRETE, (0, 0))

        BLOOD_COLOR = (random.randint(90,255),
                       random.randint(0, 5),
                       random.randint(0, 5))
        
        blood_size_factor = random.randint(1, 50)
        blood_distance = int((290/blood_size_factor)**1.4)
        blood = {
            'color': BLOOD_COLOR,
            'position': (player.x + PLAYER_WIDTH//2 + random.randint(-blood_distance, blood_distance),
                         player.y + PLAYER_HEIGHT//2 + random.randint(-blood_distance, blood_distance)),
            'radius': int(blood_size_factor/1.5),
            'alpha': random.randint(1, int(250 * math.exp(-0.09 * blood_size_factor) + 1))
        }

        blood_stain = {
            'color': (130,0,0),
            'position': (player.x + PLAYER_WIDTH//2,
                         player.y + PLAYER_HEIGHT//2),
            'radius': random.randint(5, 10),
            'alpha': 30
        }

        blood_list.append(blood)
        blood_stain_list.append(blood_stain)

        # Draw blood stains
        for blood_stain in blood_stain_list:
            blood_stain_surf = pygame.Surface((blood_stain['radius']*2, blood_stain['radius']*2), pygame.SRCALPHA)
            pygame.draw.circle(blood_stain_surf, blood_stain['color'] + (blood_stain['alpha'],), (blood_stain['radius'], blood_stain['radius']), blood_stain['radius'])
            WIN.blit(blood_stain_surf, (blood_stain['position'][0] - blood_stain['radius'], blood_stain['position'][1] - blood_stain['radius']))

        # draw player and monster
        mon_rand_x = random.choice([-2,-1,-1,-1,-1,0,0,0,0,1,1,1,1,2,-10,10])
        mon_rand_y = random.choice([-2,-1,-1,-1,-1,0,0,0,0,1,1,1,1,2,-10,10])
        player.x += random.choice([-3,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0-1,0,0,0,0,0,3,7])
        player.y += random.choice([-4,-2-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,3,4])
        
        WIN.blit(PLAYER, (player.x, player.y))
        WIN.blit(MONSTER, (player.x + mon_rand_x, player.y + mon_rand_y))

        # Draw blood splatters
        for blood in blood_list:
            blood_surf = pygame.Surface((blood['radius']*2, blood['radius']*2), pygame.SRCALPHA)
            pygame.draw.circle(blood_surf, blood['color'] + (blood['alpha'],), (blood['radius'], blood['radius']), blood['radius'])
            WIN.blit(blood_surf, (blood['position'][0] - blood['radius'], blood['position'][1] - blood['radius']))
        
        
        
        pygame.display.update()
            


# Function movement of the monster
def handle_monster_movement(monster, player):
    # Calculate the direction vector from the monster to the player
    dx = player.x - monster.x
    dy = player.y - monster.y

    # Calculate the angle between the monster and the player
    angle = math.atan2(dy, dx)
    # Calculate the X and Y components of the velocity using trigonometric functions
    vel_x = MONSTER_VEL * math.cos(angle)
    vel_y = MONSTER_VEL * math.sin(angle)

    # Update the monster's position
    monster.x += vel_x
    monster.y += vel_y
    #print(vel_x, vel_y)


# Function player movement
def handle_player_movement(keys_pressed, player):
    if keys_pressed[pygame.K_a]: # LEFT
        player.x -= PLAYER_VEL
    if keys_pressed[pygame.K_d]: # RIGHT
        player.x += PLAYER_VEL
    if keys_pressed[pygame.K_w]: # UP
        player.y -= PLAYER_VEL
    if keys_pressed[pygame.K_s]: # DOWN
        player.y += PLAYER_VEL



### Main game loop ###
def main():
    global PLAYER_VEL, draw_blood, stop_mixer
    
    monster_rect = pygame.Rect(WIDTH // 5 * 1, HEIGHT // 2,
                               MONSTER_WIDTH, MONSTER_HEIGHT)
    player_rect = pygame.Rect(WIDTH // 5 * 4, HEIGHT // 2,
                              PLAYER_WIDTH, PLAYER_HEIGHT)
    
    clock = pygame.time.Clock()
    run = True

    # Initialize variables to track time for sound play
    last_monster_sound_play_time = pygame.time.get_ticks()
    last_ambient_sound_play_time = pygame.time.get_ticks()
    sound_interval_monster = 20000 #random.randint(15000, 30000) # 15-30 seconds in milliseconds (1000 ms per second)
    sound_interval_ambient = 60000
    random_monster_sound = random.choice(os.listdir(r"assets\sounds\monster_sounds"))
    monster_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds',
                                                    'monster_sounds', random_monster_sound))
    random_ambient_sound = random.choice(os.listdir(r"assets\sounds\ambient_sounds"))
    ambient_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds',
                                                    'ambient_sounds', random_ambient_sound))

    ambient_sound.play()
    while run:
        
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_ESCAPE]: #ESCAPE
            run = False
            pygame.quit()
        
        handle_monster_movement(monster_rect, player_rect)

        if not draw_blood:
            handle_player_movement(keys_pressed, player_rect)
            draw_window(monster_rect, player_rect)

        # Check for collision between monster and player (you can play the sound here)
        if monster_rect.colliderect(player_rect):
            PLAYER_VEL = 0
            draw_blood = True
            if not stop_mixer:
                pygame.mixer.stop()
                stop_mixer = True
                possessed_laugh_sound.play()
                slit_sound.play()
                monster_eating_sound.play()
                eating_sound.play()
            
            drawing_blood(player_rect)
            
        # Check if 15 seconds have passed since the last sound play
        current_time = pygame.time.get_ticks()
        

        # monster sound
        if current_time - last_monster_sound_play_time >= sound_interval_monster:
            random_monster_sound = random.choice(os.listdir(r"assets\sounds\monster_sounds"))
            monster_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds',
                                                    'monster_sounds', random_monster_sound))
            monster_sound.play()
            last_monster_sound_play_time = current_time

        # distance monster player & monster sound volume
        dist_monster_player = math.hypot(monster_rect.x-player_rect.x,
                                         monster_rect.y-player_rect.y)
        dist_monster_player_rel = dist_monster_player/MAX_DISTANC
        monster_sound_vol = 1 - dist_monster_player_rel
        monster_sound.set_volume(monster_sound_vol)
        ambient_sound.set_volume(monster_sound_vol)
        

        # ambient sound
        if current_time - last_ambient_sound_play_time >= sound_interval_ambient:
            random_ambient_sound = random.choice(os.listdir(r"assets\sounds\ambient_sounds"))
            ambient_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds',
                                                    'ambient_sounds', random_ambient_sound))
            ambient_sound.play()

            last_ambient_sound_play_time = current_time


        ### Debugging ###
        #debugging space
        print('\n\n', '---Debugging---', '\n')
        print('current time: ', current_time)
        print('dist_monster_player: ', round(dist_monster_player, 2))
        print('dist_monster_player_rel: ', round(dist_monster_player_rel, 2))
        print('monster_sound_vol: ', round(monster_sound_vol, 2))
        print('get monster_sound vol: ', monster_sound.get_volume())
        print('get ambient_sound vol: ', ambient_sound.get_volume())
        print('draw_blood: ', draw_blood)
        print('stop_mixer: ', stop_mixer)

    main()

if __name__ == "__main__":
    main()