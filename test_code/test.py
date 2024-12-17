import gym
from gym import spaces
import numpy as np


class VirtualOrganismEnv(gym.Env):

    def __init__(self):
        super(VirtualOrganismEnv, self).__init__()
        # Define observation space: [x, y] of organism, [x, y] of food
        self.observation_space = spaces.Box(low=0,
                                            high=10,
                                            shape=(4, ),
                                            dtype=np.float32)
        # Define action space: up, down, left, right
        self.action_space = spaces.Discrete(4)
        self.reset()

    def reset(self):
        # Randomly place organism and food
        self.organism_pos = np.random.randint(0, 10, size=2)
        self.food_pos = np.random.randint(0, 10, size=2)
        self.steps = 0
        return np.concatenate(
            (self.organism_pos, self.food_pos)).astype(np.float32)

    def step(self, action):
        # Update organism position
        if action == 0: self.organism_pos[1] += 1  # up
        elif action == 1: self.organism_pos[1] -= 1  # down
        elif action == 2: self.organism_pos[0] -= 1  # left
        elif action == 3: self.organism_pos[0] += 1  # right

        # Bound positions within the grid
        self.organism_pos = np.clip(self.organism_pos, 0, 9)

        # Check if food is eaten
        done = np.array_equal(self.organism_pos, self.food_pos)
        reward = 10 if done else -0.1  # Reward for eating food, penalty for time

        # Limit steps to prevent infinite loops
        self.steps += 1
        if self.steps >= 100:
            done = True

        return np.concatenate(
            (self.organism_pos,
             self.food_pos)).astype(np.float32), reward, done, {}

    def render(self, mode='human'):
        print(f"Organism: {self.organism_pos}, Food: {self.food_pos}")


# Test the environment
env = VirtualOrganismEnv()
state = env.reset()
print("Initial State:", state)
for _ in range(10):
    action = env.action_space.sample()
    state, reward, done, _ = env.step(action)
    env.render()
    if done:
        print("Goal reached!")
        break
