import numpy as np
import random
from collections import deque
import tensorflow as tf
# from keras.models import Sequential
# from tensorflow.python.keras.models import Sequential, load_model
from keras._tf_keras.keras.models import Sequential, load_model
# from keras.layers import Dense
# from tensorflow.python.keras.layers import Dense
from keras._tf_keras.keras.layers import Dense
# from keras.optimizers import Adam
# from tensorflow.python.keras.optimizer_v2 import adam  # *
from keras._tf_keras.keras.optimizers import Adam


class DQLAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()
        tf.compat.v1.enable_eager_execution()

    def _build_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        # model.compile(loss='mse', optimizer=adam.Adam(learning_rate=self.learning_rate))  # *
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma *
                          np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save(self, name):
        self.model.save(name, save_format='h5')

    def load(self, name):
        self.model = load_model(name)

    def clear_session(self):
        tf.keras.backend.clear_session()