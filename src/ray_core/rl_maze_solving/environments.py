import os

from typing import Tuple
from discrete import Discrete

class Environment:
    def __init__(self, seeker: Tuple[int, int], goal: Tuple[int, int]):
        self.seeker = seeker
        self.goal = goal
        self.action_space = Discrete(4)
        self.observation_space = Discrete(5 * 5)

    def info(self) -> str:
        return str({'seeker': self.seeker, 'goal': self.goal})
    
    def get_observation(self) -> int:
        return 5 * self.seeker[0] + self.seeker[1]

    def reset(self) -> int:
        self.seeker = (0, 0)
        return self.get_observation()
    
    def get_reward(self) -> int:
        return 1 if self.seeker == self.goal else 0
    
    def is_done(self) -> bool:
        return self.seeker == self.goal
        

    def step(self, action: int) -> Tuple[int, int, bool, str]:
        match action:
            case 0:
                self.seeker = (max(self.seeker[0] - 1, 0), self.seeker[1])
            case 1:
                self.seeker = (min(self.seeker[0] + 1, 4), self.seeker[1])
            case 2:
                self.seeker = (self.seeker[0], max(0, self.seeker[1] - 1))
            case 3:
                self.seeker = (self.seeker[0], min(4, self.seeker[1] + 1))
            case x:
                raise ValueError(f"invalid action {x}")
        obs = self.get_observation()
        rew = self.get_reward()
        done = self.is_done()
        return obs, rew, done, self.info()
    
    def render(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

        grid = [['|' for _ in range(5)] + ["|\n"] for _ in range(5)]
        grid[self.goal[0]][self.goal[1]] = '|G'
        grid[self.seeker[0]][self.seeker[1]] = '|S'
        print(''.join([''.join(grid_row) for grid_row in grid]))
