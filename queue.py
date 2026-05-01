from queue import Queue
from event import Event

class SQueue:
    def __init__(self, name: str):
        self.name: str = name
        self.length: int = 0
        self.queue: Queue[tuple[int, Event]] = Queue(maxsize=0)

        # Statistics
        self.wait_times: list[int] = []
        self.count_history: list[tuple[int, int]] = [] # Tracks (time, current_size)

    def is_empty(self) -> bool:
        return self.queue.empty()

    def enqueue(self, event: Event, current_time: int):
        # Store the entry time inside the event object or a tuple
        self.queue.put((current_time, event))
        self.count_history.append((current_time, self.queue.qsize()))

    def dequeue(self, current_time: int) -> Event | None:
        if self.is_empty():
            return None
            
        queue_entry_time, event = self.queue.get()
        
        # Calculate how long they were in the queue
        wait_time = current_time - queue_entry_time
        self.wait_times.append(wait_time)
        
        self.count_history.append((current_time, self.queue.qsize()))
        return event

    def get_avg_wait(self):
        return sum(self.wait_times) / len(self.wait_times) if self.wait_times else 0