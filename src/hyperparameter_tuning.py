from ray import tune
import ray
import math
import time


def training_function(config: dict):
    x, y = config["x"], config["y"]
    time.sleep(10)
    score = objective(x, y)
    tune.report({"score": score})


def objective(x: int, y: int):
    return math.sqrt((x**2 + y**2)/2)

ray.init(address="auto")

result = tune.run(
    training_function,
    config={
        "x": tune.grid_search([-1, -.5, 0, .5, 1]),
        "y": tune.grid_search([-1, -.5, 0, .5, 1])
    })

print(result.get_best_config(metric="score", mode="min"))