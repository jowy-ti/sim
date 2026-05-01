import heapq
import random

class Engine:
    def __init__(self):
        self.clock = 0
        self.cec = []
        self.fec = []
        self.queue = 0
        self.server_busy = False
        
    def schedule(self, delay, event_type):
        event_time = self.clock + delay
        # Tuple: (time, priority, type)
        heapq.heappush(self.fel, (event_time, event_type))

    def run(self, max_events):
        # Initial Arrival
        self.schedule(random.expovariate(LAMBDA), ARRIVAL)
        
        for _ in range(max_events):
            if not self.fel: break
            
            # THE ENGINE JUMP: Teleport to the next event
            self.clock, event_type = heapq.heappop(self.fel)
            
            if event_type == ARRIVAL:
                self.handle_arrival()
            elif event_type == DEPARTURE:
                self.handle_departure()

    def handle_arrival(self):
        print(f"[{self.clock:.2f}] Arrival. Queue: {self.queue}")
        # Schedule next arrival (Poisson process)
        self.schedule(random.expovariate(LAMBDA), ARRIVAL)
        
        if not self.server_busy:
            self.server_busy = True
            self.schedule(random.expovariate(MU), DEPARTURE)
        else:
            self.queue += 1

    def handle_departure(self):
        print(f"[{self.clock:.2f}] Departure. Queue: {self.queue}")
        if self.queue > 0:
            self.queue -= 1
            self.schedule(random.expovariate(MU), DEPARTURE)
        else:
            self.server_busy = False