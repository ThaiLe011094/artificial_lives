import config
import pygame
import numpy as np
from environment import Environment
from dql import DQLAgent
from utils import reset_simulation

# Initialize environment and agent
state_size = 7  # Example state size
action_size = 4  # Example action size (up, down, left, right)
agent = DQLAgent(state_size, action_size)

# Create organisms, predators, and food items
organisms, predators, obstacles, food_items = reset_simulation()

env = Environment(organisms, predators, food_items)

episodes = 1000
batch_size = 128

# Add rendering
pygame.init()
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

for e in range(episodes):
    for organism in organisms:
        state = env.get_state(organism)
        state = np.reshape(state, [1, state_size])
        for time in range(500):
            action = agent.act(state)
            next_state, reward, done = env.step(organism, action)
            
            # Calculate reward based on distance to the closest food
            closest_food_distance = min([organism.distance_to(food) for food in food_items])
            reward = 10 / (closest_food_distance + 1)  # Higher reward for closer food
            if closest_food_distance < organism.size:
                reward += 50  # Extra reward for reaching the closest food
            reward = reward if not done else -10
            
            next_state = np.reshape(next_state, [1, state_size])
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            
            # Organism movement and interaction
            if organism.alive:
                organism.move(food_items, predators)
                for food in food_items:
                    organism.eat(food)
                organism.render(screen)
            
            # Render the environment
            screen.fill((0, 0, 0))  # Clear the screen with black
            for organism in organisms:
                organism.render(screen)

            # Render food
            for food in food_items:
                food.render(screen)
            pygame.display.flip()  # Update the full display surface to the screen

            if done:
                print(f"episode: {e}/{episodes}, score: {time}, e: {agent.epsilon:.2}")
                break
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)

# Save the trained model
agent.save("dql_model.h5")

# Quit rendering
pygame.quit()
