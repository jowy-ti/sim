from collections import deque
from server import Server
from event import Event
from rng import RNG
from typing import Any

class KQueue:
    def __init__(self, name: str, attributes: Any, rng: RNG):
        self.name: str = name
        self.queue: deque[tuple[float, Event]] = deque()
        self.servers: list[Server] = self.servers_creation(attributes, rng)

        # Statistics
        self.wait_times: list[float] = []
        self.count_history: list[tuple[float, int]] = [] # Tracks (time, current_size)
    
    def any_free_server(self) -> tuple[bool, int]:
        cont = 0

        for server in self.servers:
            if server.available():
                return True, cont
            cont += 1

        return False, -1
    
    def get_length(self) -> int:
        return len(self.queue)

    def enqueue(self, current_time: float, event: Event):
        # Store the entry time inside the event object or a tuple
        self.queue.append((current_time, event))
        self.count_history.append((current_time, len(self.queue)))

    def dequeue(self, current_time: float) -> Event:
        if len(self.queue) == 0:
            print("Error trying to dequeue an empty queue")     

        entry_time, event = self.queue.popleft()

        # Calculate how long they were in the queue
        wait_time = current_time - entry_time
        self.wait_times.append(wait_time)
        self.count_history.append((current_time, len(self.queue)))

        return event
    
    @staticmethod
    def servers_creation(attributes: Any, rng: RNG) -> list[Server]:
        num_servers = attributes['servers']
        return [Server(i, attributes, rng) for i in range(num_servers)]

    def enter_server(self, server_id: int) -> float:
        return self.servers[server_id].start_service()
    
    def exit_server(self, server_id: int):
        self.servers[server_id].end_service()


    # Statistics

    def get_wait_time(self) -> float:
        return sum(self.wait_times)
    
    def get_length_x_duration(self) -> float:
        length_duration: float = 0
        prev_time: float = 0
        prev_length: int = 0

        for time, length in self.count_history:
            duration = time - prev_time
            length_duration += duration * prev_length
            prev_time = time
            prev_length = length
            
        return length_duration