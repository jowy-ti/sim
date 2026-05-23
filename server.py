from const import ServerState
from rng import RNG
from typing import Any

class Server:
    def __init__(self, id: int, type: int, attributes: Any, factors: Any, rng: RNG):
        self.id: int = id
        self.status = ServerState.FREE
        self.service_time: float = self.calculate_servicetime(type, attributes, factors)
        self.service_deviation: float = self.service_time/10
        self.rng = rng

    def available(self) -> bool:
        return self.status == ServerState.FREE
    
    def start_service(self) -> float:
        self.status = ServerState.BUSY
        deviation = (2*self.rng.generate_number() - 1) * self.service_deviation
        # print(self.serviceTime + deviation)
        return self.service_time + deviation

    def end_service(self):
        self.status = ServerState.FREE

    @staticmethod
    def calculate_servicetime(type: int, attributes: Any, factors: Any) -> float:
        service_time: float = attributes['mean']

        match type:
            case 1:
                service_time += (service_time * (factors['block_difficulty'] / 10))
            case 2:
                service_time += (service_time * (factors['peers'] / 5))
            case 3:
                service_time += (service_time * (factors['transactions_to_verify'] / 10))
            case _: pass

        # match type:
        #     case 1:
        #         service_time += (service_time * (factors['block_difficulty'] / 10)) - (service_time * (factors['computational_resources'] / 10))
        #     case 2:
        #         service_time += service_time * (factors['peers'] / 5) - (service_time * (factors['computational_resources'] / 10))
        #     case 3:
        #         service_time += (service_time * (factors['block_difficulty'] / 10)) - (service_time * (factors['computational_resources'] / 10) * 1.5)
        #     case _: pass
        
        return service_time