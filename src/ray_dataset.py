import ray 
ray.init(address="auto")

items = [{"name": str(i), "data": i} for i in range(10000)]
ds = ray.data.from_items(items)
ds.show(5)


squares = ds.map(lambda x: {"name": x["name"], "squared_data": x["data"] ** 2})

evens = squares.filter(lambda x: x["squared_data"] % 2 == 0)
evens.count()

cubes = evens.flat_map(lambda x: [{"squared": x["squared_data"],
                                    "cube": x["squared_data"] ** 3}])
sample = cubes.take(10)
print(sample)