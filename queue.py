from queue import Queue
from event import Event

class SQueue:
    def __init__(self, name: str):
        self.name: str = name
        self.length: int = 0
        self.queue: Queue[Event] = Queue(maxsize=0)

        # Statistics
        self.wait_times = []
        self.count_history = [] # Tracks (time, current_size)

    def is_empty(self):
        return self.queue.empty()

    def enqueue(self, event: Event, current_time: int):
        # Store the entry time inside the event object or a tuple
        self.queue.put((event, current_time))
        self.count_history.append((current_time, self.queue.qsize()))

    def dequeue(self, current_time):
        if self.is_empty():
            return None
            
        event, queue_entry_time = self.queue.get()
        
        # Calculate how long they were in the queue
        wait_time = current_time - queue_entry_time
        self.wait_times.append(wait_time)
        
        self.count_history.append((current_time, len(self.buffer)))
        return event

    def get_avg_wait(self):
        return sum(self.wait_times) / len(self.wait_times) if self.wait_times else 0