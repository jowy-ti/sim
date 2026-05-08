from engine import Engine
    
if __name__ == "__main__":
    env = Engine(10, 4, 8, 2, 1000)
    env.run()
    wait_time = env.get_total_wait_time()
    avg_time = env.get_avg_wait_time()

    print(f"total wait time:{wait_time:.2f}, avg:{avg_time:.3f}")
