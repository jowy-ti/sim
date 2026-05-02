from const import ServerState
import random

class Server:
    def __init__(self, id: int, serviceTime: float):
        self.id: int = id
        self.status = ServerState.FREE
        self.serviceTime = serviceTime

    def available(self) -> bool:
        return self.status == ServerState.FREE
    
    def start_service(self) -> float:
        self.status = ServerState.BUSY
        return random.expovariate(self.serviceTime)

    def end_service(self):
        self.status = ServerState.FREE