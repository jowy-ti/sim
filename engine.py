import heapq
import random
from kqueue import KQueue
from event import Event
from const import EventType
from rng import RNG

class Engine:
    def __init__(self, arrival_rate: float, arrival_deviation: float, service_time: float, service_deviation: float, deadline: float, seed: int):
        self.clock: float = 0
        self.deadline: float = deadline
        self.fec: list[Event] = []
        self.arrival_rate: float = arrival_rate
        self.arrival_deviation: float = arrival_deviation
        self.rng = RNG(seed)
        self.queue = KQueue("M/M/1", service_time, service_deviation, self.rng)
        self.total_arrivals = 0

    def generator(self, id: int, next_move: float, priority_level: int, type: EventType):
        event = Event(id, next_move, priority_level, type)
        heapq.heappush(self.fec, event)

    def run(self):
        # Initial Arrival
        nextId = 0
        self.generator(nextId, self.calculate_next_arrival(), random.randint(0, 20), EventType.ARRIVAL)
        
        while self.fec:
            # Teleport to the next event
            event: Event = heapq.heappop(self.fec)
            self.clock = event.moveTime

            if self.clock > self.deadline: 
                break
            
            if event.type == EventType.ARRIVAL:
                self.process_arrival(event)
                next_arrival = self.calculate_next_arrival()
                self.generator(nextId, next_arrival, random.randint(0, 20), EventType.ARRIVAL)

                nextId += 1
                self.total_arrivals += 1
                
            elif event.type == EventType.DEPARTURE:
                self.process_departure()

    def calculate_next_arrival(self) -> float:
        deviation = (2*self.rng.generate_number() - 1) * self.arrival_deviation
        # print(self.arrival_rate + deviation)
        return self.clock + self.arrival_rate + deviation
            
    def process_arrival(self, event: Event): 
        if not self.queue.any_free_server():
            self.queue.enqueue(self.clock, event)
        else:
            service_time = self.queue.enter_server()
            self.generator(event.id, self.clock + service_time, event.priority_Level, EventType.DEPARTURE)

    def process_departure(self):
        self.queue.exit_server()
        
        if self.queue.get_length() > 0:
            event = self.queue.dequeue(self.clock)
            service_time = self.queue.enter_server()
            self.generator(event.id, self.clock + service_time, event.priority_Level, EventType.DEPARTURE)

    def get_total_wait_time(self) -> float:
        return self.queue.get_wait_time()
    
    def get_avg_wait_time(self) -> float:
        return self.queue.get_wait_time() / self.total_arrivals
    
    def get_avg_queue_length(self) -> float:
        return self.queue.get_length_x_duration() / self.deadline