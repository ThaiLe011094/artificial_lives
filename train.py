import numpy as np
from environment import Environment
from dql import DQLAgent
from organisms import Organism
from predators import Predator
from food import Food
from utils import reset_simulation
import config

# Initialize environment and agent
state_size = 7  # Example state size
action_size = 4  # Example action size (up, down, left, right)
agent = DQLAgent(state_size, action_size)

# Create organisms, predators, and food items
organisms, predators, obstacles, food_items = reset_simulation()

env = Environment(organisms, predators, food_items)

episodes = 1000
batch_size = 32

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
            if done:
                print(f"episode: {e}/{episodes}, score: {time}, e: {agent.epsilon:.2}")
                break
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)

# Save the trained model
agent.save("dql_model.h5")
