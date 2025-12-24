
import argparse
from environments import Environment
from policy import Policy
from simulations import Simulation

import numpy as np

from typing import List, Tuple

def update_policy(policy: Policy, experiences: List[Tuple[int, int, int, int]],
                   weight: float=0.1, discount_factor: float = 0.9) -> None:
    for (state, action, reward, next_state) in experiences:
        next_max = np.max(policy.state_action_stable[next_state])
        value = policy.state_action_stable[state][action]
        new_value = (1 - weight) * value + weight * (reward + discount_factor * next_max)
        policy.state_action_stable[state][action] = new_value

def train_policy(env: Environment, num_episodes: int = 10000, weight: float = 0.1,
                 discount_factor: float = 0.9):
    policy = Policy(env)
    sim = Simulation(env)
    for _ in range(num_episodes):
        experiences = sim.rollout(policy)
        update_policy(policy, experiences, weight, discount_factor)
    return policy

def evaluate_policy(env: Environment, policy: Policy, num_episodes=10):
    simulation = Simulation(env)
    steps = 0
    for _ in range(num_episodes):
        experiences = simulation.rollout(policy)
        steps += len(experiences)
    
    print(f"{steps / num_episodes} steps on average for a total number of \
           {num_episodes} episodes")
    return steps / num_episodes

if __name__ == "__main__":
    env = Environment((0, 0), (4, 4))
    
    policy = train_policy(env)
    evaluate_policy(env, policy)

    # exp = sim.rollout(untrained_policy, render=False, epsilon = 1.0)

    #for row in untrained_policy.state_action_stable:
    #    print(row)
    # update_policy(untrained_policy, )