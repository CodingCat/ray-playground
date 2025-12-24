
from environments import Environment
from policy import Policy
from simulation_actor import SimulationActor
from training import update_policy, evaluate_policy

import ray

def train_policy_in_parallel(env: Environment, num_episode: int=1000,
                              num_simulations: int=4):
    policy = Policy(env)
    simulations = [SimulationActor.remote() for _ in range(num_simulations)]

    for ep in range(num_episode):
        print(f"starting training on epoch {ep}")
        policy_ref = ray.put(policy)
        # run rollouts in parallel
        futures = [
            sim.rollout.remote(policy_ref)
            for sim in simulations
        ]
        # gather all experience then update unified policy on driver
        all_xp = ray.get(futures)
        for xp in all_xp:
            update_policy(policy, xp)

    return policy

if __name__ == "__main__":
    ray.init(ignore_reinit_error=True)
    env = Environment((0, 0), (4, 4))
    
    policy = train_policy_in_parallel(env)
    evaluate_policy(env, policy)