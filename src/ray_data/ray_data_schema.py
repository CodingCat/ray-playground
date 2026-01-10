import ray


if __name__ == "__main__":
    ds = ray.data.from_items([{"id":"abc", "value": 1}, {"id": "def", "value": 2}])
    # row based
    print(ds.take(1))
    # column based
    print(ds.take_batch(1))
    print(ds.schema())