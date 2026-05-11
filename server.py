from const import ServerState
from rng import RNG

class Server:
    def __init__(self, id: int, serviceTime: float, service_deviation: float, rng: RNG):
        self.id: int = id
        self.status = ServerState.FREE
        self.serviceTime = serviceTime
        self.service_deviation = service_deviation
        self.rng = rng

    def available(self) -> bool:
        return self.status == ServerState.FREE
    
    def start_service(self) -> float:
        self.status = ServerState.BUSY
        deviation = (2*self.rng.generate_number() - 1) * self.service_deviation
        # print(self.serviceTime + deviation)
        return self.serviceTime + deviation

    def end_service(self):
        self.status = ServerState.FREE