import pygame
import random
import math 
import os

# Initialize pygame modules
pygame.init()
pygame.font.init()
pygame.mixer.init()


# Set up constants
WIDTH, HEIGHT = 1000, 1000
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


# Load game assets
PLAYER_IMAGE = pygame.image.load(
    os.path.join('assets', 'images', 'player.png')
    )
PLAYER = pygame.transform.rotate(
    pygame.transform.scale(PLAYER_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT)), 0
    )

MONSTER_IMAGE = pygame.image.load(
    os.path.join('assets', 'images', 'monster.png')
    )
MONSTER = pygame.transform.rotate(
    pygame.transform.scale(MONSTER_IMAGE, (MONSTER_WIDTH, MONSTER_HEIGHT)), 0
    )

CONCRETE = pygame.transform.scale(
    pygame.image.load(os.path.join('assets', 'images', 'concrete.jpg')),
    (WIDTH, HEIGHT)
    )

#DARKNESS = pygame.draw.polygon()

# Create a mask surface to represent the visible area
mask = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
mask.set_alpha(200)  # Set the initial transparency (200 for slight transparency)


# Function to draw game window
def draw_window(monster, player):
    WIN.blit(CONCRETE, (0, 0))
    WIN.blit(MONSTER, (monster.x, monster.y))
    WIN.blit(PLAYER, (player.x, player.y))

    #Darkness
    vector_darkness = [[900, 300], [600, 400], [600, 300]]


    pygame.draw.polygon(WIN, (0, 0, 0, 127), vector_darkness)
    

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

# Function monster sounds
def handle_monster_sound():
    random_monster_sound = random.choice(os.listdir(r"assets\sounds\monster_sounds"))
    monster_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds',
                                                    'monster_sounds', random_monster_sound))
    monster_sound.play()

# Function ambient sounds
def handle_ambient_sound():
    random_ambient_sound = random.choice(os.listdir(r"assets\sounds\ambient_sounds"))
    ambient_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds',
                                                    'ambient_sounds', random_ambient_sound))
    ambient_sound.play()


### Main game loop ###
def main():
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
    #handle_monster_sound() #beginning sound

    handle_ambient_sound()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        keys_pressed = pygame.key.get_pressed()
        handle_player_movement(keys_pressed, player_rect)
        handle_monster_movement(monster_rect, player_rect)
    
        draw_window(monster_rect, player_rect)

        # Check for collision between monster and player (you can play the sound here)
        if monster_rect.colliderect(player_rect):
            pygame.mixer.Sound(os.path.join('assets', 'sounds',
                                            'collide',
                                            'possessed-laugh-94851.mp3')).play()
            
        # Check if 15 seconds have passed since the last sound play
        current_time = pygame.time.get_ticks()
        print(current_time)
        # monster sound
        if current_time - last_monster_sound_play_time >= sound_interval_monster:
            handle_monster_sound()
            last_monster_sound_play_time = current_time
        # ambient sound
        if current_time - last_ambient_sound_play_time >= sound_interval_ambient:
            handle_ambient_sound()
            last_ambient_sound_play_time = current_time

    main()

if __name__ == "__main__":
    main()