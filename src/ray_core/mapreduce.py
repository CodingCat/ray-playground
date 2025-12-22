from collections.abc import Iterable
import subprocess
import argparse
import mmh3
import ray
from typing import Sequence, Tuple, List, Dict

def map_function(document: List[str]) -> Iterable[Tuple[str, int]]:
    for word in document:
        yield word, 1


@ray.remote
def mapper(data: List[str], num_partitions: int) -> Sequence[List[Tuple[str, int]]]:
    result = [list[Tuple[str, int]]() for _ in range(num_partitions)]
    for word, count in map_function(data):
        partition_index = mmh3.hash(word, signed=False) % num_partitions
        result[partition_index].append((word, count))
    return tuple(result)


@ray.remote
def reducer(*mapper_output: List[Tuple[str, int]]) -> Dict[str, int]:
    result: Dict[str, int] = {}
    for bucket in mapper_output:
        for word, count in bucket:
            result[word] = result.setdefault(word, 0) + count
    return result


if __name__ == "__main__":
    zen_of_python = subprocess.check_output(["python", "-c", "import this"])
    corpus = zen_of_python.decode("utf-8").split()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--num-partitions",
        type=int,
        required=True,
        help="num_partitions mapper writes to",
    )
    parser.add_argument(
        "--input-chunks",
        type=int,
        required=True,
        help="number of input chunks",
    )

    args = parser.parse_args()
    num_partitions = args.num_partitions
    num_input_chunks = args.input_chunks

    chunk = int(len(corpus) / num_input_chunks)
    partitioned_data = [
        corpus[i * chunk: (i + 1) * chunk] for i in range(num_input_chunks)
    ]
    
    map_results_refs = [
        mapper.options(num_returns=num_partitions).remote(data, num_partitions)
        for data in partitioned_data
    ]

    reduce_refs = [
        reducer.remote(*[map_results_refs[m][p] for m in range(num_input_chunks)])
        for p in range(num_partitions)
    ]

    reduced_dicts: List[Dict[str, int]] = ray.get(reduce_refs)

    final: Dict[str, int] = {}
    for d in reduced_dicts:
        final.update(d)

    items = list(final.items())
    items.sort(key=lambda x: (-x[1], x[0]))
    print("Top 20:")
    for w, c in items[:20]:
        print(w, c)



