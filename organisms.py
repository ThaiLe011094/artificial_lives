import random
import math
import pygame
# from config import GREEN, SCREEN_WIDTH, SCREEN_HEIGHT
import config

class Organism:
    def __init__(
            self,
            x,
            y,
            size=config.ORGANISM_SIZE,
            energy=config.ORGANISM_BASE_ENERGY,
            speed=config.ORGANISM_SPD,
            starvation_threshold=config.ORGANISM_STARVATION_THRESHOLD,
            color=config.GREEN
        ):
        self.x = x
        self.y = y
        self.size = size
        self.energy = energy
        self.speed = speed
        self.alive = True
        self.starvation_threshold = starvation_threshold
        self.color = color
        self.mating_cooldown = 0  # Time until this organism can mate again

    def move(self, food_items):
        if not self.alive:
            return

        # If starving, move toward the nearest food
        if self.energy <= self.starvation_threshold:
            closest_food = self.find_closest_food(food_items)
            if closest_food:
                self.move_toward(closest_food.x, closest_food.y)
        else:
            # Free movement
            try:
                self.x += random.randint(-self.speed, self.speed)
                self.y += random.randint(-self.speed, self.speed)
            except ValueError:
                print("self.speed:", self.speed)

        # Keep within screen bounds
        self.x = max(0, min(config.SCREEN_WIDTH, self.x))
        self.y = max(0, min(config.SCREEN_HEIGHT, self.y))

        # Decrease energy due to movement
        self.energy -= config.ORGANISM_ENERGY_DEPLETE_RATE
        if self.energy <= 0:
            self.alive = False
        print("organism:", self.energy)

    def find_closest_food(self, food_items):
        closest_food = None
        min_distance = float('inf')
        for food in food_items:
            if food.alive:
                distance = math.sqrt((self.x - food.x) ** 2 + (self.y - food.y) ** 2)
                if distance < min_distance:
                    closest_food = food
                    min_distance = distance
        return closest_food

    def move_toward(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            self.x += self.speed * (dx / distance)
            self.y += self.speed * (dy / distance)

    def eat(self, food):
        if not self.alive or not food.alive:
            return
        distance = math.sqrt((self.x - food.x) ** 2 + (self.y - food.y) ** 2)
        if distance < self.size and self.energy <= self.starvation_threshold:
            food.alive = False
            self.energy += random.randint(20, 40)

    def render(self, surface):
        if self.alive:
            pygame.draw.circle(surface, config.GREEN, (int(self.x), int(self.y)), self.size)

    @staticmethod
    def random():
        x = random.randint(0, config.SCREEN_WIDTH)
        y = random.randint(0, config.SCREEN_HEIGHT)
        return Organism(x, y)
