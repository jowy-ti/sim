from __future__ import annotations
from const import EventType

class Event:
    def __init__(self, id: int, moveTime: float, type: EventType, queue_name: str):
        self.id: int = id
        self.moveTime: float = moveTime
        self.type: EventType = type
        self.queue_name: str = queue_name

    # Crucial for heapq / sorting
    def __lt__(self, other: Event) -> bool:
        return self.moveTime < other.moveTime
    
    def __repr__(self) -> str:
        return f"Event(id={self.id}, time={self.moveTime:.2f}"