from collections.abc import Iterable
import subprocess
import argparse
import mmh3
import ray
from typing import Sequence, Tuple, List

def map_function(document: List[str]) -> Iterable[Tuple[str, int]]:
    for word in document:
        yield word, 1


@ray.remote
def mapper(data: List[str], num_partitions: int) -> Sequence[Sequence[Tuple[str, int]]]:
    result = [[] for _ in range(num_partitions)]
    for word_count in map_function(data):
        partition_index = mmh3.hash(word_count[0], signed=False) % num_partitions
        result[partition_index].append(word_count)
    return result



if __name__ == "__main__":
    zen_of_python = subprocess.check_output(["python", "-c", "import this"])
    corpus = zen_of_python.split()

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
        mapper.remote(data, num_partitions)
        for data in partitioned_data
    ]

    map_results = ray.get(map_results_refs)

    for mapper_idx, partitions in enumerate(map_results):
        for part_idx, bucket in enumerate(partitions):
            print(f"Mapper {mapper_idx}, partition {part_idx}: {bucket[:2]}")


