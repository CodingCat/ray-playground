import time

from environments import Environment
from policy import Policy

from typing import List, Tuple

class Simulation(object):
    
    def __init__(self, env: Environment) -> None:
        self.env = env

    def rollout(self, policy: Policy, render: bool = False, explore: bool = True,
                 epsilon: float = 0.1):
        experiences = list()
        state = self.env.reset()
        done = False
        while not done:
            action = policy.get_action(state, explore, epsilon)
            next_state, reward, done, _ = self.env.step(action)
            experiences.append((state, action, reward, next_state))
            state = next_state
            if render:
                time.sleep(0.05)
                self.env.render()
        return experiences

    