import random
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GREEN, BLUE


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
        self.max_age = max_age if max_age else random.uniform(3, 6) * 30
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
        if self.energy <= 0 or self.age >= self.max_age or self.size > 60:  # Size limit
            self.alive = False

    def eat(self, food):
        if food.alive and abs(self.x -
                              food.x) < self.size and abs(self.y -
                                                          food.y) < self.size:
            self.energy += 20
            food.alive = False
            self.size += 1

    def mate(self, other):
        if self.alive and other.alive and abs(self.x - other.x) < 20 and abs(
                self.y - other.y) < 20:
            if self.energy > 50 and other.energy > 50:
                self.energy -= 25
                other.energy -= 25
                return self.reproduce(other)
        return []

    def reproduce(self, other):
        newborns = []
        for _ in range(random.randint(1, 2)):  # Max 2 offspring
            x = (self.x + other.x) // 2
            y = (self.y + other.y) // 2
            color = random.choice([self.color, other.color])
            newborns.append(Organism(x, y, size=5, energy=50, color=color))
        return newborns

    def render(self, surface):
        if self.alive:
            pygame.draw.circle(surface, self.color, (self.x, self.y),
                               self.size)

    @staticmethod
    def random():
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        color = random.choice([GREEN, BLUE])
        return Organism(x, y, color=color)
