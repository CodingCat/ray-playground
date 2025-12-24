import ray

from simulations import Simulation
from src.ray_core.rl_maze_solving.environments import Environment

@ray.remote
class SimulationActor(Simulation):
    def __init__(self) -> None:
        self.env = Environment(seeker=(0, 0), goal=(4, 4))
        
