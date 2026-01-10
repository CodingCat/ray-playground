import ray


if __name__ == "__main__":
    ds = ray.data.range(1000)
    print(ds.count())
    print(ds.take_batch(50))
    print(ds.schema())