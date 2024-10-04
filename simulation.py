import pygame   # This is the library used for creating and managing the game window, handling events, and rendering graphics.
import math
pygame.init()

WINDOW = pygame.display.set_mode((800, 800)) # a window of size 800x800 pixels for displaying the simulation
pygame.display.set_caption("Planet Simulation")

def main():
    
    run = True
    while run:
        for event in pygame.event.get():  # Gives a list of all the events (like keyboard presses, mouse movements, or window closing) that Pygame has detected.
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


main()                