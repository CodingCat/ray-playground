import ray
from ray.runtime_context import get_runtime_context
from parallel_database_fetching import retrieve, retrieve_batch_task, chunked, RetrieveResult, database
from typing import Tuple

@ray.remote
def follow_up_task(retrieved_result: RetrieveResult) -> Tuple[RetrieveResult, RetrieveResult]:
    follow_up_result = (
        [
            retrieve(item + 1, database) for (item, _) in retrieved_result
        ]
    )
    ctx = get_runtime_context()
    print(f"follow_up_task: running items={list(retrieved_result)}, task_id={ctx.get_task_id()}")
    return retrieved_result, follow_up_result

def main() -> None:
    ray.init(ignore_reinit_error=True)

    db_object_ref = ray.put(database)

    retrieve_refs = (
        [
            retrieve_batch_task.remote(batch, db_object_ref)
            for batch in chunked([0, 2, 4, 6], 1)
        ]
    )
    follow_up_refs = [follow_up_task.remote(ref) for ref in retrieve_refs]

    [print(data) for data in ray.get(follow_up_refs)]


if __name__ == "__main__":
    main()

