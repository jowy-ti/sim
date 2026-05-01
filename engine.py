import heapq
import random
from queue import Queue
from event import Event

class Engine:
    def __init__(self):
        self.clock: int = 0
        self.fec: list[Event] = []
        
    def event_list_update(self, event: Event):
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

    def process_arrival(self):
        print(f"[{self.clock:.2f}] Arrival. Queue: {self.queue}")
        # Schedule next arrival (Poisson process)
        self.schedule(random.expovariate(LAMBDA), ARRIVAL)
        
        if not self.server_busy:
            self.server_busy = True
            self.schedule(random.expovariate(MU), DEPARTURE)
        else:
            self.queue += 1

    def proces_departure(self):
        print(f"[{self.clock:.2f}] Departure. Queue: {self.queue}")
        if self.queue > 0:
            self.queue -= 1
            self.schedule(random.expovariate(MU), DEPARTURE)
        else:
            self.server_busy = False