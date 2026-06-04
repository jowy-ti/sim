class RNG:
    # Constants
    M: int = 2**31
    A: int = 1103515245
    C: int = 12345

    def __init__(self, seed: int):
        self.seed: int = seed

    def generate_number(self) -> float:
        self.seed = (self.A * self.seed + self.C) % self.M
        return float(self.seed / self.M)


