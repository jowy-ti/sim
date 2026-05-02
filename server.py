from const import ServerState
import random

class Server:
    def __init__(self, name: str, serviceTime: float):
        self.name: str = name
        self.status = ServerState.FREE
        self.serviceTime = serviceTime

    def available(self) -> bool:
        return self.status == ServerState.FREE
    
    def start_service(self) -> float:
        self.status = ServerState.BUSY
        service_duration = random.expovariate(self.serviceTime)
        return service_duration

    def end_service(self):
        self.status = ServerState.FREE