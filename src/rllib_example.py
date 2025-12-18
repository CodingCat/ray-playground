import ray
from ray.rllib.algorithms.ppo import PPOConfig

ray.init(address="auto")

algo = (
    PPOConfig()
    .environment("CartPole-v1")
    .framework("torch")
    .env_runners(num_env_runners=1)
    .build()
)

def headline(r):
    er = r.get("env_runners", {}).get("episode_return_mean")
    el = r.get("env_runners", {}).get("episode_len_mean")
    it = r.get("training_iteration")
    t  = r.get("time_this_iter_s")
    losses = r.get("learners", {}).get("default_policy", {})
    return {
        "iter": it,
        "episode_return_mean": er,
        "episode_len_mean": el,
        "time_this_iter_s": t,
        "policy_loss": float(losses.get("policy_loss")) if "policy_loss" in losses else None,
        "vf_loss": float(losses.get("vf_loss")) if "vf_loss" in losses else None,
        "entropy": float(losses.get("entropy")) if "entropy" in losses else None,
        "kl": float(losses.get("mean_kl_loss")) if "mean_kl_loss" in losses else None,
    }

for i in range(3):
    res = algo.train()
    print(headline(res))
