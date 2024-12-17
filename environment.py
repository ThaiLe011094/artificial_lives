import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GRAY, LIGHT_BLUE
import random

class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def render(self, surface):
        pygame.draw.rect(surface, GRAY, (self.x, self.y, self.width, self.height))

    @staticmethod
    def random():
        x = random.randint(0, SCREEN_WIDTH - 50)
        y = random.randint(0, SCREEN_HEIGHT - 50)
        width = random.randint(50, 150)
        height = random.randint(50, 150)
        return Obstacle(x, y, width, height)

class Weather:
    def __init__(self):
        self.type = random.choice(["clear", "rain", "storm"])
        self.duration = random.randint(300, 600)

    def apply_effects(self, organisms):
        if self.type == "rain":
            for organism in organisms:
                organism.energy -= 0.5  # Rain causes energy drain
        elif self.type == "storm":
            for organism in organisms:
                organism.energy -= 1
                organism.speed -= 1

    def render(self, surface):
        if self.type == "rain":
            pygame.draw.rect(surface, LIGHT_BLUE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 10)
