import random
from abc import ABC, abstractmethod

from constants import Action


class Agent(ABC):
    @abstractmethod
    def get_action(self, state):
        pass

    def update_with_reward(self, state, action, reward, next_state, done):
        pass


class RandomAgent(Agent):
    def get_action(self, state):
        return random.choice(list(Action))
