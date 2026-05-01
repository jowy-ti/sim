import const
import random

class Server:
    def __init__(self, id, serviceTime):
        self.id = id
        self.status = const.FREE
        self.serviceTime = serviceTime
        self.current_event = None

    def is_available(self):
        return self.status == const.FREE
    
    def start_service(self, event):
        self.status = const.BUSY
        self.current_event = event
        
        # Kendall 'M' service: Exponential distribution
        service_duration = random.expovariate(self.serviceTime)
        return service_duration
        
    def start_service(self, event, current_time):
        """Prepares the server and returns the calculated service duration."""
        self.status = "BUSY"
        self.current_event = event
        self.last_state_change = current_time
        
        # Kendall 'M' service: Exponential distribution
        service_duration = random.expovariate(self.mu)
        return service_duration

    def end_service(self, current_time):
        """Clears the server and updates busy-time statistics."""
        duration = current_time - self.last_state_change
        self.total_busy_time += duration
        
        served_event = self.current_event
        self.status = "IDLE"
        self.current_event = None
        self.last_state_change = current_time
        
        return served_event