import pygame   # This is the library used for creating and managing the game window, handling events, and rendering graphics.
import math
pygame.init()

WINDOW = pygame.display.set_mode((800, 800)) # a window of size 800x800 pixels for displaying the simulation
pygame.display.set_caption("Planet Simulation")


class Planet():

    # Constants
    AU = 149.6e6 * 1000 # in metres
    G = 6.67428e-11
    SCALE = 250/AU # 1 AU = 100 pixels
    TIMESTEP = 3600*24 # 1 day of planet at a time

    def __init__(self, x, y, radius, mass, color):
        
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.color = color

        self.sun = False
        self.distance_to_sun = 0
        self.orbit = []

        self.x_vel = 0
        self.y_vel = 0

def main():
    
    run = True
    clock =  pygame.time.Clock(); # The clock object allows you to manage the timing in your game loop by measuring 
                                  # how much time has passed and controlling the speed at which the game updates.

    while run:
        clock.tick(60)   # no matter how fast the computer is, the game will only run up to 60 frames per second.
        
        for event in pygame.event.get():  # Gives a list of all the events (like keyboard presses, mouse movements, or window closing) that Pygame has detected.
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


main()                