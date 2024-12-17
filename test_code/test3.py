import pygame
import numpy as np
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Virtual Organisms")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Clock
clock = pygame.time.Clock()


class Organism:

    def __init__(self,
                 x,
                 y,
                 size=5,
                 energy=100,
                 age=0,
                 max_age=None,
                 color=GREEN):
        self.x = x
        self.y = y
        self.size = size
        self.energy = energy
        self.age = age
        self.max_age = max_age if max_age else random.uniform(
            3, 6) * 30  # Random age in seconds
        self.color = color
        self.alive = True

    def move(self):
        if not self.alive:
            return
        self.x += random.randint(-5, 5)
        self.y += random.randint(-5, 5)
        self.x = max(0, min(SCREEN_WIDTH, self.x))
        self.y = max(0, min(SCREEN_HEIGHT, self.y))
        self.energy -= 1
        self.age += 1
        if self.energy <= 0 or self.age >= self.max_age or self.size > 12 * 5:  # Limit size
            self.alive = False

    def eat(self, food):
        if np.linalg.norm([self.x - food.x, self.y - food.y]) < self.size:
            self.energy += 20
            food.alive = False
            self.size += 1

    def mate(self, other):
        if self.alive and other.alive and np.linalg.norm(
            [self.x - other.x, self.y - other.y]) < 20:
            if self.energy > 50 and other.energy > 50:
                self.energy -= 25
                other.energy -= 25
                return self.reproduce(other)
        return []

    def reproduce(self, other):
        newborns = []
        for _ in range(random.randint(1, 2)):  # Maximum 2 offspring
            x = (self.x + other.x) // 2
            y = (self.y + other.y) // 2
            color = random.choice([self.color,
                                   other.color])  # Random inheritance of color
            newborns.append(Organism(x, y, size=5, energy=50, color=color))
        return newborns

    def render(self, surface):
        if self.alive:
            pygame.draw.circle(surface, self.color, (self.x, self.y),
                               self.size)


class Food:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True

    def render(self, surface):
        if self.alive:
            pygame.draw.circle(surface, RED, (self.x, self.y), 3)


# Initialize organisms and food
MAX_ORGAN_SIZE_W = int(SCREEN_WIDTH / 100)
MAX_ORGAN_SIZE_H = int(SCREEN_HEIGHT / 100)
organisms = [
    Organism(random.randint(0, MAX_ORGAN_SIZE_W),
             random.randint(0, MAX_ORGAN_SIZE_H)) for _ in range(20)
]

MAX_FOOD_SIZE_W = int(SCREEN_WIDTH / 100)
MAX_FOOD_SIZE_H = int(SCREEN_HEIGHT / 100)
food_items = [
    Food(random.randint(0, MAX_FOOD_SIZE_W),
         random.randint(0, MAX_FOOD_SIZE_H)) for _ in range(50)
]

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # Update organisms
    new_organisms = []
    for i, organism in enumerate(organisms):
        organism.move()
        for food in food_items:
            organism.eat(food)
        for other in organisms[i + 1:]:
            new_organisms.extend(organism.mate(other))
        organism.render(screen)

    organisms.extend(new_organisms)  # Add newborns

    # Remove dead organisms
    organisms = [o for o in organisms if o.alive]

    # Update food
    for food in food_items:
        food.render(screen)

    # Respawn food
    if not any(food.alive for food in food_items):
        food_items = [
            Food(random.randint(0, SCREEN_WIDTH),
                 random.randint(0, SCREEN_HEIGHT)) for _ in range(50)
        ]

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
