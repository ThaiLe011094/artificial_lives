import random
import math
import pygame
# from config import GREEN, SCREEN_WIDTH, SCREEN_HEIGHT
import config
import string
from typing import Final
import numpy as np
from dql import DQLAgent
import os

class Organism:
    def __init__(
            self,
            x,
            y,
            size=config.ORGANISM_SIZE,
            energy=config.ORGANISM_BASE_ENERGY,
            speed=config.ORGANISM_SPD,
            starvation_threshold=config.ORGANISM_STARVATION_THRESHOLD,
            # color=config.GREEN
        ):
        self.x = x
        self.y = y
        self.size = size
        self.energy = energy
        self.speed: Final[int] = speed  # Check constant, only works when checking using mypy
        self.alive = True
        self.starvation_threshold = starvation_threshold
        # self.color = color
        self.mating_cooldown = 0  # Time until this organism can mate again
        self.name = ''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits)
            for _ in range(config.NUMBER_OF_NAME_CHAR))
        # Randomly choose between two images
        image_path = random.choice(config.ORGANSIM_IMG_PATH)
        self.image = pygame.image.load(image_path)
        self.avatar = pygame.transform.scale(self.image, config.ORGANISM_IMG_SIZE)
        self.previous_x = x  # Store the previous x position

        # Initialize DQL agent
        state_size = 7
        action_size = 4
        self.agent = DQLAgent(state_size, action_size)
        model_path = "dql_model.h5"
        if os.path.exists(model_path):
            self.agent.load(model_path)   # Load the trained model

    # def move(self, food_items, predators):
    #     if not self.alive:
    #         return

    #     print(f"Moving organism {self.name} at position ({self.x}, {self.y}) with energy {self.energy}")

    #     # Check for nearby predators
    #     closest_predator = self.find_closest_predator(predators)
    #     if closest_predator and self.is_predator_in_field_of_view(closest_predator):
    #         print(f"Organism {self.name} is running away from predator at ({closest_predator.x}, {closest_predator.y})")
    #         self.run_away_from(closest_predator.x, closest_predator.y)
    #     # If starving, move toward the nearest food
    #     elif self.energy <= self.starvation_threshold:
    #         closest_food = self.find_closest_food(food_items)
    #         if closest_food:
    #             print(f"Organism {self.name} is starving and moving towards food at ({closest_food.x}, {closest_food.y})")
    #             self.move_toward(closest_food.x, closest_food.y)
    #     else:
    #         # Free movement
    #         try:
    #             dx = random.randint(-self.speed, self.speed)
    #             dy = random.randint(-self.speed, self.speed)
    #             self.x += dx
    #             self.y += dy
    #             print(f"Organism {self.name} moved freely by ({dx}, {dy}) to ({self.x}, {self.y})")
    #         except Exception as e:
    #             print(f"Exception occurred for organism {self.name}: {e}")
    #             raise Exception(f"self.speed: {self.speed}")

        # # Keep within screen bounds
        # self.x = max(0, min(config.SCREEN_WIDTH, self.x))
        # self.y = max(0, min(config.SCREEN_HEIGHT, self.y))
        # print(f"Organism {self.name} position adjusted to screen bounds: ({self.x}, {self.y})")

        # # Decrease energy due to movement
        # self.energy -= config.ORGANISM_ENERGY_DEPLETE_RATE
        # print(f"Organism {self.name} energy decreased to {self.energy}")

        # if self.energy <= 0:
        #     self.alive = False
        #     print(f"Organism {self.name} has died due to lack of energy")

    # def move(self, food_items, predators):  # not integrate deep q-learning yet
    #     if not self.alive:
    #         return

    #     closest_predator = self.find_closest_predator(predators)
    #     if closest_predator and self.is_predator_in_field_of_view(closest_predator):
    #         self.run_away_from(closest_predator.x, closest_predator.y)
    #     else:
    #         closest_food = self.find_closest_food(food_items, predators)
    #         if closest_food:
    #             self.move_toward(closest_food.x, closest_food.y)
    #         else:
    #             self.random_move()

    #     self.keep_within_bounds()
    #     self.energy -= config.ORGANISM_ENERGY_DEPLETE_RATE
    #     if self.energy <= 0:
    #         self.alive = False

    # def find_closest_food(self, food_items):
    #     closest_food = None
    #     min_distance = float('inf')
    #     for food in food_items:
    #         if food.alive:
    #             distance = math.sqrt((self.x - food.x) ** 2 + (self.y - food.y) ** 2)
    #             if distance < min_distance:
    #                 closest_food = food
    #                 min_distance = distance
    #     return closest_food

    def move(self, food_items, predators):  # integrate deep q-learning
        if not self.alive:
            return

        state = self.get_state(food_items, predators)
        state = np.reshape(state, [1, self.agent.state_size])
        action = self.agent.act(state)
        self.perform_action(action)

        self.keep_within_bounds()
        self.energy -= config.ORGANISM_ENERGY_DEPLETE_RATE
        if self.energy <= 0:
            self.alive = False

    def get_state(self, food_items, predators):
        closest_food = self.find_closest_food(food_items, predators)
        closest_predator = self.find_closest_predator(predators)
        state = [
            self.x, self.y, 
            self.energy,
            closest_food.x if closest_food else 0,
            closest_food.y if closest_food else 0,
            closest_predator.x if closest_predator else 0,
            closest_predator.y if closest_predator else 0
        ]
        return np.array(state)

    def perform_action(self, action):
        if action == 0:
            self.y -= self.speed
        elif action == 1:
            self.y += self.speed
        elif action == 2:
            self.x -= self.speed
        elif action == 3:
            self.x += self.speed

    def find_closest_food(self, food_items, predators):
        closest_food = None
        min_distance = float('inf')
        for food in food_items:
            if not self.is_food_near_predator(food, predators):
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
            self.previous_x = self.x  # Update previous x position
            self.x += self.speed * (dx / distance)
            self.y += self.speed * (dy / distance)

    def eat(self, food):
        if not self.alive or not food.alive:
            return
        distance = math.sqrt((self.x - food.x) ** 2 + (self.y - food.y) ** 2)
        if distance < self.size and self.energy <= self.starvation_threshold:
            food.alive = False
            self.energy += random.randint(40, 80)

    def get_hitbox(self):
        return pygame.Rect(
            self.x - self.size, self.y - self.size,
            config.ORGANISM_HITBOX_RADIUS, config.ORGANISM_HITBOX_RADIUS)

    def find_closest_predator(self, predators):
        closest_predator = None
        min_distance = float('inf')
        for predator in predators:
            if predator.alive:
                distance = math.sqrt((self.x - predator.x) ** 2 + (self.y - predator.y) ** 2)
                if distance < min_distance:
                    closest_predator = predator
                    min_distance = distance
        return closest_predator

    def is_food_near_predator(self, food, predators):
        for predator in predators:
            if predator.alive:
                distance = math.sqrt((food.x - predator.x) ** 2 + (food.y - predator.y) ** 2)
                if distance <= config.ORGANISM_FIELD_OF_VIEW:
                    return True
        return False

    def is_predator_in_field_of_view(self, predator):
        distance = math.sqrt((self.x - predator.x) ** 2 + (self.y - predator.y) ** 2)
        return distance <= config.ORGANISM_FIELD_OF_VIEW

    def run_away_from(self, predator_x, predator_y):
        dx = self.x - predator_x
        dy = self.y - predator_y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            self.previous_x = self.x  # Update previous x position
            self.x += self.speed * (dx / distance)
            self.y += self.speed * (dy / distance)

    def random_move(self):
        dx = random.randint(-self.speed, self.speed)
        dy = random.randint(-self.speed, self.speed)
        self.x += dx
        self.y += dy

    def keep_within_bounds(self):
        self.x = max(0, min(config.SCREEN_WIDTH, self.x))
        self.y = max(0, min(config.SCREEN_HEIGHT, self.y))

    def render(self, screen):
        if self.alive:
            # Determine if the image should be flipped
            if self.x > self.previous_x:
                directed_avatar = pygame.transform.flip(self.avatar, True, False)
            else:
                directed_avatar = self.avatar

            # pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)  # circle as avatar
            screen.blit(directed_avatar, (self.x - self.size, self.y - self.size))
            font = pygame.font.SysFont(None, 24)
            text = font.render(f'{self.name} ({int(self.energy)})', True, (255, 255, 255))
            screen.blit(text, (self.x - self.size, self.y - self.size - 20))

    @staticmethod
    def random():
        x = random.randint(0, config.SCREEN_WIDTH)
        y = random.randint(0, config.SCREEN_HEIGHT)
        return Organism(x, y)
