import pygame
import math

pygame.init()

# Window setup
WIDTH, HEIGHT = 800, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

# Colors
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)

class Planet:
    # Constants
    AU = 149.6e6 * 1000  # in metres
    G = 6.67428e-11  # Gravitational constant
    SCALE = 220 / AU  # Scale for drawing: 1 AU = 100 pixels
    TIMESTEP = 3600 * 24  # One day in seconds

    def __init__(self, x, y, radius, mass, color):
        self.x = x  # Position in meters
        self.y = y
        self.radius = radius  # Radius for drawing
        self.mass = mass
        self.color = color

        self.sun = False
        self.distance_to_sun = 0
        self.orbit = []

        self.x_vel = 0  # Velocity in meters per second
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        # Draw the orbit path
        if len(self.orbit) > 2:
            updated_orbit = [(point[0] * self.SCALE + WIDTH / 2, point[1] * self.SCALE + HEIGHT / 2) for point in self.orbit]
            pygame.draw.lines(win, self.color, False, updated_orbit, 2)

        pygame.draw.circle(win, self.color, (int(x), int(y)), self.radius)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2  # F = G * m1 * m2 / r^2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y

    def update_position(self, planets):
        total_fx, total_fy = 0, 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        # Update velocity (acceleration = F / m)
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        # Update position based on velocity
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP

        # Save orbit history for drawing
        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    # Create the Sun (massive object at the center)
    sun = Planet(0, 0, 30, 1.98892 * 10**30, YELLOW)
    sun.sun = True

    # Create planets with initial positions and velocities
    earth = Planet(-Planet.AU, 0, 16, 5.9742 * 10**24, BLUE)
    earth.y_vel = 29.783 * 1000  # Earth's orbital velocity in m/s

    mars = Planet(-1.524 * Planet.AU, 0, 12, 6.39 * 10**23, RED)
    mars.y_vel = 24.077 * 1000  # Mars' orbital velocity in m/s

    venus = Planet(0.723 * Planet.AU, 0, 14, 4.8685 * 10**24, WHITE)
    venus.y_vel = -35.02 * 1000  # Venus' orbital velocity in m/s (clockwise)

    mercury = Planet(0.387 * Planet.AU, 0, 8, 3.30 * 10**23, GRAY)
    mercury.y_vel = -47.87 * 1000  # Mercury's orbital velocity in m/s (clockwise)

    planets = [sun, earth, mars, venus, mercury]

    while run:
        clock.tick(60)  # Limit to 60 frames per second
        WINDOW.fill((0, 0, 0))  # Clear the screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Update and draw each planet
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WINDOW)

        pygame.display.update()

    pygame.quit()


main()
