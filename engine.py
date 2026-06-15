import heapq
from kqueue import KQueue
from event import Event
from const import EventType
from rng import RNG
from typing import Any, Dict
import math

class Engine:
    QUEUE0: str = 'Queue0' # Virtual queue
    END: str = 'END'

    def __init__(self, deadline: float, seed: int, routing_config: Any):
        self.clock: float = 0           # Current simulation logical time
        self.deadline: float = deadline # Global simulation ending
        self.fec: list[Event] = []      # Future Event Calendar (min-heap priority queue)
        self.rng = RNG(seed)

        # Extract operational input factor parameters from configuration
        self.mean_interarrival: float = routing_config['factors']['interarrival_rate']            
        self.topology: Dict[str, Any] = routing_config['topology']

        # Initialize the network nodes (KQueue instances) dynamically
        self.queues: Dict[str, KQueue] = self.queues_creation(routing_config['components'], routing_config['factors'], self.rng)

        # Statistics
        self.blocks_validated: int = 0

    def generator(self, id: int, next_move: float, type: EventType, queue_name: str, server_id: int):
        event = Event(id, next_move, type, queue_name, server_id)
        heapq.heappush(self.fec, event) # Maintains O(log N) temporal sort order

    def run(self):
        # Initial Arrival
        nextId: int = 0
        # Generates an event
        self.generator(nextId, self.calculate_next_arrival(), EventType.ARRIVAL, self.QUEUE0, -1)
        
        while self.fec:
            # Teleport to the next event
            event: Event = heapq.heappop(self.fec)
            self.clock = event.move_time

            # stops immediatly the simulation if deadline is reached
            if self.clock > self.deadline: 
                break
            
            if event.type == EventType.ARRIVAL:
                # routes to the first queue and generates new arrival
                self.process_arrival(event, nextId)
                nextId += 1
                
            elif event.type == EventType.DEPARTURE:
                # routes to the next queue and let the next event in the queue enter the server
                self.process_departure(event)

    def calculate_next_arrival(self) -> float:
        # Formulate exponential delay from uniform random float
        next = (self.mean_interarrival * math.log(self.rng.generate_number()))
        return self.clock - next

    def process_arrival(self, event: Event, nextId: int): 
        next_arrival = self.calculate_next_arrival()
        self.generator(nextId, next_arrival, EventType.ARRIVAL, self.QUEUE0, -1)
        self.route_next_queue(event)

    def process_departure(self, event: Event):
        event_queue: KQueue = self.queues[event.queue_name]
        event_queue.exit_server(event.server_id) # De-allocate active server lane
        server_exited: int = event.server_id

        # Queue Management: If entities are buffered, promote the next block to active service
        if event_queue.get_length() > 0:
            event_dequeued: Event = event_queue.dequeue(self.clock)
            service_time: float = event_queue.enter_server(server_exited) 

            # Schedule a departure event for the newly promoted entity
            self.generator(event_dequeued.id, self.clock + service_time, EventType.DEPARTURE, event_queue.name, server_exited)

        # Transition the current entity to its subsequent network routing phase
        self.route_next_queue(event)

    def route_next_queue(self, event: Event):
        next_queue_name: str = self.topology[event.queue_name]['next']
        
        # Terminal Condition: Success outcome indicator representing complete block validation
        if next_queue_name == self.END:
            self.blocks_validated += 1
            return

        next_queue: KQueue = self.queues[next_queue_name]
        free, server_id = next_queue.any_free_server()

        if not free:
            # Capacity Constrained: Buffer entity inside the localized queue structure
            next_queue.enqueue(self.clock, event)
        else:
            # Capacity Available: Execute immediate resource execution bypass loop
            next_queue.wait_times.append(0.0) # Tracks explicit zero-wait-time structural records
            service_time = next_queue.enter_server(server_id)
            self.generator(event.id, self.clock + service_time, EventType.DEPARTURE, next_queue_name, server_id)

    @staticmethod
    def queues_creation(components: Any, factors: Any, rng: RNG) -> Dict[str, KQueue]:
        """
        Factory method mapping components from config schemas into active KQueue object dicts.
        """
        return {name: KQueue(name, attrs, factors, rng) for name, attrs in components.items()}

    # Statistics
    
    def get_avg_wait_time_queue(self, queue: str) -> float:
        """
        Computes the average queuing delay time ($W_q$) for a specific network node.
        """
        avg_time, entries = self.queues[queue].get_wait_time()
        return avg_time / entries
    
    def get_avg_queue_length_queue(self, queue: str) -> float:
        """
        Calculates the time-weighted average queue length ($L_q$) using integration traces.
        """
        return self.queues[queue].get_length_x_duration() / self.deadline
    
    def get_total_transactions_completed(self) -> int:
        """
        Returns the cumulative block validation throughput response metric for DoE analysis.
        """
        return self.blocks_validated