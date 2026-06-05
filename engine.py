import heapq
from kqueue import KQueue
from event import Event
from const import EventType
from rng import RNG
from typing import Any, Dict
import math

class Engine:
    QUEUE0: str = 'Queue0'
    END: str = 'END'

    def __init__(self, deadline: float, seed: int, routing_config: Any):
        self.clock: float = 0
        self.deadline: float = deadline
        self.fec: list[Event] = []
        self.mean_interarrival: float = routing_config['factors']['interarrival_rate']
        self.rng = RNG(seed)
        self.topology: Dict[str, Any] = routing_config['topology']
        self.queues: Dict[str, KQueue] = self.queues_creation(routing_config['components'], routing_config['factors'], self.rng)

        # Statistics
        self.blocks_validated: int = 0

    def generator(self, id: int, next_move: float, type: EventType, queue_name: str, server_id: int):
        event = Event(id, next_move, type, queue_name, server_id)
        heapq.heappush(self.fec, event)

    def run(self):
        # Initial Arrival
        nextId = 0
        self.generator(nextId, self.calculate_next_arrival(), EventType.ARRIVAL, self.QUEUE0, -1)
        
        while self.fec:
            # Teleport to the next event
            event: Event = heapq.heappop(self.fec)
            self.clock = event.move_time

            if self.clock > self.deadline: 
                break
            
            if event.type == EventType.ARRIVAL:
                self.process_arrival(event)
                next_arrival = self.calculate_next_arrival()
                self.generator(nextId, next_arrival, EventType.ARRIVAL, self.QUEUE0, -1)

                nextId += 1
                
            elif event.type == EventType.DEPARTURE:
                self.process_departure(event)

    def calculate_next_arrival(self) -> float:
        next = (self.mean_interarrival * math.log(self.rng.generate_number()))
        # print(f"next: {next}")
        return self.clock - next

    def process_arrival(self, event: Event): 
        self.route_next_queue(event)

    def process_departure(self, event: Event):
        event_queue: KQueue = self.queues[event.queue_name]
        event_queue.exit_server(event.server_id)
        server_exited: int = event.server_id

        if event_queue.get_length() > 0:
            event_dequeued: Event = event_queue.dequeue(self.clock)
            service_time: float = event_queue.enter_server(server_exited)
            self.generator(event_dequeued.id, self.clock + service_time, EventType.DEPARTURE, event_queue.name, server_exited)

        self.route_next_queue(event)

    def route_next_queue(self, event: Event):
        next_queue_name: str = self.topology[event.queue_name]['next']
        
        if next_queue_name == self.END:
            self.blocks_validated += 1
            return

        next_queue: KQueue = self.queues[next_queue_name]
        free, server_id = next_queue.any_free_server()

        if not free:
            next_queue.enqueue(self.clock, event)
        else:
            next_queue.wait_times.append(0.0)
            service_time = next_queue.enter_server(server_id)
            self.generator(event.id, self.clock + service_time, EventType.DEPARTURE, next_queue_name, server_id)

    @staticmethod
    def queues_creation(components: Any, factors: Any, rng: RNG) -> Dict[str, KQueue]:
        return {name: KQueue(name, attrs, factors, rng) for name, attrs in components.items()}

    # Statistics
    
    def get_avg_wait_time_queue(self, queue: str) -> float:
        avg_time, entries = self.queues[queue].get_wait_time()
        return avg_time / entries
    
    def get_avg_queue_length_queue(self, queue: str) -> float:
        return self.queues[queue].get_length_x_duration() / self.deadline
    
    def get_total_transactions_completed(self) -> int:
        return self.blocks_validated