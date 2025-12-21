import argparse
import ray


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--actor-name",
        type=str,
        required=True,
        help="the name of the actor to connect to",
    )
    parser.add_argument(
        "--actor-namespace",
        type=str,
        required=True,
        help="the namespace of the actor to connect to",
    )
    args = parser.parse_args()
    tracker = ray.get_actor(namespace=args.actor_namespace, name=args.actor_name)
    object_references = [
        tracker.fetch_item.remote(item) for item in range(8)
    ]
    data = ray.get(object_references)
    print(data)
    print(ray.get(tracker.counts.remote()))