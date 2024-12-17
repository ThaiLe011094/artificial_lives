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
    def __init__(self, x, y, size=5, energy=100, age=0):
        self.x = x
        self.y = y
        self.size = size
        self.energy = energy
        self.age = age
        self.alive = True

    def move(self):
        if not self.alive:
            return
        # Random movement
        self.x += random.randint(-5, 5)
        self.y += random.randint(-5, 5)
        # Keep within bounds
        self.x = max(0, min(SCREEN_WIDTH, self.x))
        self.y = max(0, min(SCREEN_HEIGHT, self.y))
        # Decrease energy and increase age
        self.energy -= 1
        self.age += 0.1
        if self.energy <= 0 or self.age > 100:
            self.alive = False

    def eat(self, food):
        if np.linalg.norm([self.x - food.x, self.y - food.y]) < self.size:
            self.energy += 20
            food.alive = False
            self.size += 1  # Grow in size

    def render(self, surface):
        if self.alive:
            pygame.draw.circle(surface, GREEN, (self.x, self.y), self.size)

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True

    def render(self, surface):
        if self.alive:
            pygame.draw.circle(surface, RED, (self.x, self.y), 3)

# Initialize organisms and food
MAX_ORGAN_SIZE_W = int(SCREEN_WIDTH/100)
MAX_ORGAN_SIZE_H = int(SCREEN_HEIGHT/100)
organisms = [Organism(random.randint(0, MAX_ORGAN_SIZE_W), random.randint(0, MAX_ORGAN_SIZE_H)) for _ in range(20)]

MAX_FOOD_SIZE_W = int(SCREEN_WIDTH/100)
MAX_FOOD_SIZE_H = int(SCREEN_HEIGHT/100)
food_items = [Food(random.randint(0, MAX_FOOD_SIZE_W), random.randint(0, MAX_FOOD_SIZE_H)) for _ in range(50)]

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # Update organisms
    for organism in organisms:
        organism.move()
        for food in food_items:
            organism.eat(food)
        organism.render(screen)

    # Update food
    for food in food_items:
        food.render(screen)

    # Respawn food if all are eaten
    if not any(food.alive for food in food_items):
        food_items = [Food(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(50)]

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
