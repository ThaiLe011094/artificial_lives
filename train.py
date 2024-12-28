import numpy as np
from environment import Environment
from dql import DQLAgent
from organisms import Organism
from predators import Predator
from food import Food
from utils import reset_simulation
import config
import pygame

# Initialize environment and agent
state_size = 7  # Example state size
action_size = 4  # Example action size (up, down, left, right)
agent = DQLAgent(state_size, action_size)
# agent.clear_session()  # Clear the session

# Create organisms, predators, and food items
organisms, predators, obstacles, food_items = reset_simulation()

env = Environment(organisms, predators, food_items)

episodes = 1000
batch_size = 128


# add rendering
pygame.init()
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))


for e in range(episodes):
    for organism in organisms:
        state = env.get_state(organism)
        state = np.reshape(state, [1, state_size])
        for time in range(500):
            action = agent.act(state)
            next_state, reward, done = env.step(organism, action)
            reward = reward if not done else -10
            next_state = np.reshape(next_state, [1, state_size])
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            
            # Organism movement and interaction
            organisms = [o for o in organisms if o.alive]
            for organism in organisms:
                organism.move(food_items, predators)
                for food in food_items:
                    organism.eat(food)
                organism.render(screen)
            
            # Predator interaction
            predators = [p for p in predators if p.alive]
            for predator in predators:
                predator.move(organisms)
                predator.hunt(organisms)
                predator.render(screen)
            
            # Render the environment
            screen.fill((0, 0, 0))  # Clear the screen with black
            for organism in organisms:
                organism.render(screen)
            for predator in predators:
                predator.render(screen)

            # Render food
            # Update food
            for food in food_items:
                food.render(screen)
            pygame.display.flip()  # Update the full display surface to the screen
            # clock.tick(60)
            # End rendering

            if done:
                print(f"episode: {e}/{episodes}, score: {time}, e: {agent.epsilon:.2}")
                break
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)

# Save the trained model
agent.save("dql_model.h5")

# quit rendering
pygame.quit()
