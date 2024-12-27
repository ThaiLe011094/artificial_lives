import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GRAY, LIGHT_BLUE
import random
import numpy as np


class Obstacle:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def render(self, surface):
        pygame.draw.rect(surface, GRAY,
                         (self.x, self.y, self.width, self.height))

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
            pygame.draw.rect(surface, LIGHT_BLUE,
                             (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 10)


class Environment:
    def __init__(self, organisms, predators, food_items):
        self.organisms = organisms
        self.predators = predators
        self.food_items = food_items

    def get_state(self, organism):
        closest_food = organism.find_closest_food(self.food_items, self.predators)
        closest_predator = organism.find_closest_predator(self.predators)
        state = [
            organism.x, organism.y, 
            organism.energy,
            closest_food.x if closest_food else 0,
            closest_food.y if closest_food else 0,
            closest_predator.x if closest_predator else 0,
            closest_predator.y if closest_predator else 0
        ]
        return np.array(state)

    def step(self, organism, action):
        # Define actions: 0 = up, 1 = down, 2 = left, 3 = right
        if action == 0:
            organism.y -= organism.speed
        elif action == 1:
            organism.y += organism.speed
        elif action == 2:
            organism.x -= organism.speed
        elif action == 3:
            organism.x += organism.speed

        # Calculate reward
        reward = -1  # Default reward for each step
        if organism.energy <= 0:
            reward -= 100  # Penalty for dying
        closest_food = organism.find_closest_food(self.food_items, self.predators)
        if closest_food and organism.x == closest_food.x and organism.y == closest_food.y:
            reward += 100  # Reward for finding food

        # Update state
        new_state = self.get_state(organism)
        done = not organism.alive
        return new_state, reward, done
