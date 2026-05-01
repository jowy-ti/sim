from const import ServerState
import random
from event import Event

class Server:
    def __init__(self, name: str, serviceTime: int):
        self.name: str = name
        self.status = ServerState.FREE
        self.serviceTime = serviceTime
        self.current_event = None

        # Stats attributes
        self.total_busy_time = 0
        self.last_state_change = 0

    def is_available(self) -> bool:
        return self.status == ServerState.FREE
    
    def start_service(self, event: Event, current_time: int) -> float:
        self.status = ServerState.BUSY
        self.current_event = event
        self.last_state_change = current_time
        
        # Kendall 'M' service: Exponential distribution
        service_duration = random.expovariate(self.serviceTime)
        return service_duration

    def end_service(self, current_time: int) -> Event | None:
        duration = current_time - self.last_state_change
        self.total_busy_time += duration

        served_event = self.current_event
        self.status = ServerState.FREE
        self.current_event = None
        self.last_state_change = current_time
        
        return served_event