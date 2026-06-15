from const import ServerState
from rng import RNG
from typing import Any

class Server:
    def __init__(self, id: int, type: int, attributes: Any, factors: Any, rng: RNG):
        self.id: int = id
        self.status = ServerState.FREE

        # Calculate the service time modified by active experimental factors
        self.service_time: float = self.calculate_servicetime(type, attributes, factors)

        # Define uniform deviation boundaries (bounds are +/- 10% of the calculated base service time)
        self.service_deviation: float = self.service_time/10
        self.rng = rng

    def available(self) -> bool:
        return self.status == ServerState.FREE
    
    def start_service(self) -> float:
        self.status = ServerState.BUSY

        # Map uniform standard distribution [0, 1) to interval range [-1, 1)
        scaled_random = 2 * self.rng.generate_number() - 1
        deviation = scaled_random * self.service_deviation

        return self.service_time + deviation

    def end_service(self):
        self.status = ServerState.FREE

    @staticmethod
    def calculate_servicetime(type: int, attributes: Any, factors: Any) -> float:
        service_time: float = attributes['mean']

        # Apply specific scaling formulas based on queue node classification
        match type:
            case 1:
                # Dynamic adjustment based on the Block Difficulty parameter
                service_time += (service_time * (factors['block_difficulty'] / 10))
            case 2:
                # Operational adjustment based on active networking Peer latency impact
                service_time += (service_time * (factors['peers'] / 10))
            case 3:
                # Data payload processing overhead scaling
                service_time += (service_time * (factors['block_data'] / 20))
            case _: pass        
        return service_time