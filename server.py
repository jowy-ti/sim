from const import ServerState
import random

class Server:
    def __init__(self, id: int, serviceTime: float, service_deviation: float):
        self.id: int = id
        self.status = ServerState.FREE
        self.serviceTime = serviceTime
        self.service_deviation = service_deviation

    def available(self) -> bool:
        return self.status == ServerState.FREE
    
    def start_service(self) -> float:
        self.status = ServerState.BUSY
        min = self.serviceTime - self.service_deviation
        max = self.serviceTime + self.service_deviation
        return random.uniform(min, max)

    def end_service(self):
        self.status = ServerState.FREE