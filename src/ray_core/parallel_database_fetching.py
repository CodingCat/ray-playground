import time
import argparse
from typing import Iterable, List, Sequence, Tuple
from custom_types import RetrieveResult, Batch, BatchResult

import ray
from ray.runtime_context import get_runtime_context



# ---------------------------
# Data
# ---------------------------
database: List[str] = [
    "Learning", "Ray",
    "Flexible", "Distributed", "Python", "for", "Machine", "Learning"
]

# ---------------------------
# Functions
# ---------------------------
def retrieve(item: int, db) -> RetrieveResult:
    time.sleep(item / 10.0)
    return item, db[item]


def print_runtime(input_data: Sequence[RetrieveResult], start_time: float) -> None:
    print(f"Runtime: {time.time() - start_time:.2f} seconds, data:")
    print(*input_data, sep="\n")


def chunked(seq: Sequence[int], size: int) -> Iterable[Batch]:
    for i in range(0, len(seq), size):
        yield seq[i : i + size]


@ray.remote
def retrieve_batch_task(items: Batch, db) -> BatchResult:
    ctx = get_runtime_context()
    print(f"retrieve_batch_task: running items={list(items)}, task_id={ctx.get_task_id()}")
    return [retrieve(i, db) for i in items]


# ---------------------------
# Main
# ---------------------------
def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1,
        help="How many items each Ray task fetches.",
    )
    args = parser.parse_args()

    if args.batch_size <= 0:
        raise ValueError("--batch-size must be >= 1")

    ray.init(ignore_reinit_error=True)

    db_object_ref = ray.put(database)

    indices: List[int] = list(range(8))

    start: float = time.time()

    refs: List[ray.ObjectRef[BatchResult]] = [
        retrieve_batch_task.remote(batch, db_object_ref)
        for batch in chunked(indices, args.batch_size)
    ]

    all_data = []

    while len(refs) > 0:
        finished, refs = ray.wait(refs, num_returns = 2, timeout = 7.0)
        data = ray.get(finished)
        print_runtime(data, start)
        all_data.extend(data)


if __name__ == "__main__":
    main()
