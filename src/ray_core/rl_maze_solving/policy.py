import numpy as np
import random
from environments import Environment

class Policy:

    def __init__(self, env: Environment) -> None:
        self.state_action_stable = [
            [0 for _ in range(env.action_space.num_actions)]
            for _ in range(env.observation_space.num_actions)
        ]
        self.action_space = env.action_space
    
    def get_action(self, state: int, explore: bool = True, epsilon: float = 0.1) -> int:
        if explore and random.uniform(0, 1) < epsilon:
            return self.action_space.sample()
        return np.argmax(self.state_action_stable[state])
