from engine import Engine
    
if __name__ == "__main__":
    env = Engine(1/4, 1/2, 1000.)
    env.run()
    wait_time = env.get_total_wait_time()

    print(f"total wait time:{wait_time}")
