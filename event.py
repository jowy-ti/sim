from __future__ import annotations
from const import EventType

class Event:
    def __init__(self, id: int, moveTime: float, type: EventType, queue_name: str, server_id: int):
        self.id: int = id                   
        self.move_time: float = moveTime    
        self.type: EventType = type         # Event classification (e.g., ARRIVAL, DEPARTURE)
        self.queue_name: str = queue_name   # actual queue where event takes place
        self.server_id: int = server_id     # Identifier of the active server handling the process (-1 if none)

    # Crucial for heapq / sorting
    def __lt__(self, other: Event) -> bool:
        return self.move_time < other.move_time
    
    def __repr__(self) -> str:
        return f"Event(id={self.id}, time={self.move_time:.2f}"