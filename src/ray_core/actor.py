from abc import ABC
import argparse
import ray
import time
from typing import List

@ray.remote
class DataTracker(ABC):
    def __init__(self):
        super().__init__()
        self._counts = 0
        self._database: List[str] = [
            "Learning", "Ray", "Flexible", "Distributed", "Python",
              "for", "Machine", "Learning"
        ]

    def inc(self) -> None:
        self._counts += 1
    
    def counts(self) -> int:
        return self._counts
    
    def fetch_item(self, item) -> str:
        time.sleep(item/10.)
        self.inc()
        return self._database[item]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--long-running-actor",
        action="store_true",
        help="Whether to make the actor as long running",
    )
    args = parser.parse_args()
    if not args.long_running_actor:
        tracker = DataTracker.remote()
    else:
        tracker = DataTracker.options(
            name = "data_tracker",
            lifetime = "detached",
            namespace = "ray_core_example",
            get_if_exists = True
        ).remote()
    object_references = [
        tracker.fetch_item.remote(item) for item in range(8)
    ]
    data = ray.get(object_references)
    print(data)
    print(ray.get(tracker.counts.remote()))