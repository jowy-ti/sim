from engine import Engine
    
if __name__ == "__main__":
    env = Engine(10, 4, 8, 2, 10000)
    env.run()
    avg_time = env.get_avg_wait_time()
    avg_queue_length = env.get_avg_queue_length()

    print(f"avg_wait_time:{avg_time:.4f}, avg_queue_length:{avg_queue_length:.5f}")
