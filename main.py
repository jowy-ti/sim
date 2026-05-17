from engine import Engine
import csv
import yaml
from typing import Any, Dict
    
if __name__ == "__main__":

    with open("topology.yml", "r") as file:
        config: Dict[str, Any] = yaml.safe_load(file)

    SEED = 30
    python_results: list[tuple[float,float]] = []

    queues = config['components']
    
    for i in range(5):
        env = Engine(5, 2, 100000, SEED+i, config)
        env.run()
        print(f"Replication {i}")
        for queue_name in queues:
            avg_time = env.get_avg_wait_time_queue(queue_name)
            avg_queue_length = env.get_avg_queue_length_queue(queue_name)
            python_results.append((avg_time, avg_queue_length))
            print(f"  {queue_name}: avg_wait_time:{avg_time:.4f}, avg_queue_length:{avg_queue_length:.5f}")

        with open("python_results.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["avg_wait_time", "avg_queue_length"])

            for wait, queue in python_results:
                writer.writerow([wait, queue])