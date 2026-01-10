import ray


if __name__ == "__main__":
    ds = ray.data.range(1000)
    ds = ds.materialize()
    print(f"number of blocks {ds.num_blocks()}")
    print(ds.take_batch(50))
    print(ds.schema())

    print(f"number of blocks {ds.repartition(10).materialize().num_blocks()}")
    