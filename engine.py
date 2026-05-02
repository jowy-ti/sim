import heapq
import random
from kqueue import KQueue
from event import Event
from const import EventType

class Engine:
    def __init__(self, arrival_rate: float):
        self.clock: float = 0
        self.fec: list[Event] = []
        self.arrival_rate: float = arrival_rate
        self.queue = KQueue("M/M/1", arrival_rate-1)

    def generator(self, id: int, last_move: float, priority_level: int, type: EventType):
        event = Event(id, last_move + random.expovariate(self.arrival_rate), priority_level, type)
        heapq.heappush(self.fec, event)

    def run(self):
        # Initial Arrival
        nextId = 0
        self.generator(nextId, 0, 0, EventType.ARRIVAL)
        
        while self.fec:
            # Teleport to the next event
            event: Event = heapq.heappop(self.fec)
            self.clock = event.moveTime
            
            if event.type == EventType.ARRIVAL:
                self.process_arrival(event)
                self.generator(nextId+1, event.moveTime, random.randint(0, 20), EventType.ARRIVAL)
            elif event.type == EventType.DEPARTURE:
                self.process_departure()
            
    def process_arrival(self, event: Event): 
        if not self.queue.any_free_server():
            self.queue.enqueue(self.clock, event)
        else:
            exit_time = self.queue.enter_server()
            self.generator(event.id, exit_time, event.priority_Level, EventType.DEPARTURE)

    def process_departure(self):
        self.queue.exit_server()
        
        if self.queue.get_length() > 0:
            event = self.queue.dequeue(self.clock)
            exit_time = self.queue.enter_server()
            self.generator(event.id, exit_time, event.priority_Level, EventType.DEPARTURE)