from enum import Enum, auto

class EventType(Enum):
    ARRIVAL = auto()
    DEPARTURE = auto()

class ServerState(Enum):
    FREE = auto()
    BUSY = auto()