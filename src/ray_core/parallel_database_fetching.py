import time
import argparse
from typing import Iterable, List, Sequence, Tuple

import ray
from ray.runtime_context import get_runtime_context

# ---------------------------
# Types
# ---------------------------
RetrieveResult = Tuple[int, str]
Batch = Sequence[int]
BatchResult = List[RetrieveResult]

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
def retrieve(item: int) -> RetrieveResult:
    time.sleep(item / 10.0)
    return item, database[item]


def print_runtime(input_data: Sequence[RetrieveResult], start_time: float) -> None:
    print(f"Runtime: {time.time() - start_time:.2f} seconds, data:")
    print(*input_data, sep="\n")


def chunked(seq: Sequence[int], size: int) -> Iterable[Batch]:
    for i in range(0, len(seq), size):
        yield seq[i : i + size]


@ray.remote
def retrieve_batch_task(items: Batch) -> BatchResult:
    ctx = get_runtime_context()
    print(f"running items={list(items)}, task_id={ctx.get_task_id()}")
    return [retrieve(i) for i in items]


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

    indices: List[int] = list(range(8))

    start: float = time.time()

    refs: List[ray.ObjectRef[BatchResult]] = [
        retrieve_batch_task.remote(batch)
        for batch in chunked(indices, args.batch_size)
    ]

    batched: List[BatchResult] = ray.get(refs)
    data: List[RetrieveResult] = [x for batch in batched for x in batch]

    print_runtime(data, start)


if __name__ == "__main__":
    main()
