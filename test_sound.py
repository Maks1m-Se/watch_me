import pygame
import time
import random
import os

# Initialize Pygame
pygame.init()

random_ambient_sound = random.choice(os.listdir(r"assets\sounds\ambient_sounds"))
ambient_sound = os.path.join('assets', 'sounds', 'ambient_sounds', random_ambient_sound)
print(ambient_sound) 

# Load the sound
sound = pygame.mixer.Sound(ambient_sound)

# Play the sound
sound.play()
print('volume 1')

# Wait for a while to hear the sound
time.sleep(3)  # Sleep for 1 second

# Change the volume to 50%
sound.set_volume(0.8)
print('volume 0.8')

# Wait to observe the volume change
time.sleep(3)  # Sleep for 2 seconds

# Change the volume to 100%
sound.set_volume(0.5)
print('volume 0.5')

# Wait to observe the volume change
time.sleep(3)  # Sleep for 2 seconds

sound.set_volume(0.2)
print('volume 0.2')

# Wait to observe the volume change
time.sleep(3)  # Sleep for 2 seconds

sound.set_volume(0.1)
print('volume 0.1')

# Wait to observe the volume change
time.sleep(3)  # Sleep for 2 seconds


sound.set_volume(0.5)
print('volume 0.5')

# Wait to observe the volume change
time.sleep(3)  # Sleep for 2 seconds

sound.set_volume(1)
print('volume 1')

# Wait to observe the volume change
time.sleep(3)  # Sleep for 2 seconds

# Stop the sound and quit
pygame.mixer.stop()
pygame.quit()
