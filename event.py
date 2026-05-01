from __future__ import annotations
from const import EventType

class Event:
    def __init__(self, id: int, moveTime: int, priorityLevel: int, type: EventType):
        self.id: int = id
        self.moveTime: int = moveTime
        self.priority_Level: int = priorityLevel
        self.type: EventType = type


    # Crucial for heapq / sorting
    def __lt__(self, other: Event) -> bool:
        if self.moveTime == other.moveTime:
            # Secondary sort by priority level if times are equal
            return self.priority_Level < other.priority_Level
        return self.moveTime < other.moveTime
    
    def __repr__(self) -> str:
        return f"Event(id={self.id}, time={self.moveTime:.2f}"