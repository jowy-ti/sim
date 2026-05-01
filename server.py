import const
import random
from event import Event

class Server:
    def __init__(self, id: int, serviceTime: int):
        self.id = id
        self.status = const.FREE
        self.serviceTime = serviceTime
        self.current_event = None

        # Stats attributes
        self.total_busy_time = 0
        self.last_state_change = 0

    def is_available(self):
        return self.status == const.FREE
    
    def start_service(self, event: Event, current_time: int):
        self.status = const.BUSY
        self.current_event = event
        self.last_state_change = current_time
        
        # Kendall 'M' service: Exponential distribution
        service_duration = random.expovariate(self.serviceTime)
        return service_duration

    def end_service(self, current_time: int):
        duration = current_time - self.last_state_change
        self.total_busy_time += duration

        served_event = self.current_event
        self.status = const.FREE
        self.current_event = None
        self.last_state_change = current_time
        
        return served_event