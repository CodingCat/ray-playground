
from environments import Environment
from policy import Policy
from simulations import Simulation

if __name__ == "__main__":
    env = Environment((0, 0), (4, 4))
    untrained_policy = Policy(env)
    sim = Simulation(env)

    exp = sim.rollout(untrained_policy, render=True, epsilon = 1.0)

    for row in untrained_policy.state_action_stable:
        print(row)