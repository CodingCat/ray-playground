import random

class Discrete:
    def __init__(self, num_actions: int) -> None:
        self.num_actions = num_actions
    
    def sample(self) -> int:
        return random.randint(0, self.num_actions - 1)
    
