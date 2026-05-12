from engine import Engine
import csv
    
if __name__ == "__main__":
    SEED = 30
    python_results: list[tuple[float,float]] = []
    for i in range(20):
        env = Engine(10, 4, 9, 2, 10000, SEED+i)
        env.run()
        avg_time = env.get_avg_wait_time()
        avg_queue_length = env.get_avg_queue_length()
        python_results.append((avg_time, avg_queue_length))
        print(f"avg_wait_time:{avg_time:.4f}, avg_queue_length:{avg_queue_length:.5f}")

        with open("python_results.csv", "w", newline="") as f:
            writer = csv.writer(f)

            writer.writerow(["avg_wait_time", "avg_queue_length"])

            for wait, queue in python_results:
                writer.writerow([wait, queue])